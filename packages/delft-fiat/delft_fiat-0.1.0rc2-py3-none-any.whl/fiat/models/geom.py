"""Geom model of FIAT."""

import os
import time
from concurrent.futures import ProcessPoolExecutor, wait
from multiprocessing import Process
from pathlib import Path

from fiat.cfg import ConfigReader
from fiat.check import (
    check_duplicate_columns,
    check_exp_columns,
    check_geom_extent,
    check_internal_srs,
    check_vs_srs,
)
from fiat.gis import geom, overlay
from fiat.gis.crs import get_srs_repr
from fiat.io import (
    open_exp,
    open_geom,
)
from fiat.log import setup_mp_log, spawn_logger
from fiat.models.base import BaseModel
from fiat.models.util import (
    GEOM_MIN_CHUNK,
    GEOM_MIN_WRITE_CHUNK,
    csv_def_file,
    csv_temp_file,
    geom_resolve,
    geom_threads,
    geom_worker,
)
from fiat.util import create_1d_chunk

logger = spawn_logger("fiat.model.geom")


class GeomModel(BaseModel):
    """Geometry model.

    Needs the following settings in order to be run: \n
    - exposure.csv.file
    - exposure.geom.file1
    - output.geom.file1

    Parameters
    ----------
    cfg : ConfigReader
        ConfigReader object containing the settings.
    """

    _method = {
        "area": overlay.clip,
        "centroid": overlay.pin,
    }

    def __init__(
        self,
        cfg: ConfigReader | dict,
    ):
        super().__init__(cfg)

        # Setup the geometry model
        self._read_exposure_data()
        self._read_exposure_geoms()
        self._set_chunking()
        self._set_num_threads()
        self._queue = self._mp_manager.Queue(maxsize=10000)

    def __del__(self):
        BaseModel.__del__(self)

    def _clean_up(self):
        """_summary_."""
        _p = self.cfg.get("output.path.tmp")
        for _f in _p.glob("*"):
            os.unlink(_f)
        os.rmdir(_p)

    def _read_exposure_data(self):
        """_summary_."""
        path = self.cfg.get("exposure.csv.file")
        logger.info(f"Reading exposure data ('{path.name}')")

        # Setting the keyword arguments from settings file
        kw = {"index": "Object ID"}
        kw.update(
            self.cfg.generate_kwargs("exposure.csv.settings"),
        )
        data = open_exp(path, **kw)
        ##checks
        logger.info("Executing exposure data checks...")

        # Check for mandatory columns
        check_exp_columns(data.columns)

        # Check for duplicate columns
        check_duplicate_columns(data._dup_cols)

        ## Information for output
        _ex = None
        if self.cfg["hazard.risk"]:
            _ex = ["Risk (EAD)"]
        cols = data.create_all_columns(
            self.cfg.get("hazard.band_names"),
            _ex,
        )
        self.cfg["output.new_columns"] = cols

        ## When all is done, add it
        self.exposure_data = data

    def _read_exposure_geoms(self):
        """_summary_."""
        _d = {}
        _found = [item for item in list(self.cfg) if "exposure.geom.file" in item]
        for file in _found:
            path = self.cfg.get(file)
            logger.info(
                f"Reading exposure geometry '{file.split('.')[-1]}' ('{path.name}')"
            )
            data = open_geom(str(path))
            ## checks
            logger.info("Executing exposure geometry checks...")

            # check the internal srs of the file
            _int_srs = check_internal_srs(
                data.get_srs(),
                path.name,
            )

            # check if file srs is the same as the model srs
            if not check_vs_srs(self.srs, data.get_srs()):
                logger.warning(
                    f"Spatial reference of '{path.name}' \
('{get_srs_repr(data.get_srs())}') does not match \
the model spatial reference ('{get_srs_repr(self.srs)}')"
                )
                logger.info(f"Reprojecting '{path.name}' to '{get_srs_repr(self.srs)}'")
                data = geom.reproject(data, self.srs.ExportToWkt())

            # check if it falls within the extent of the hazard map
            check_geom_extent(
                data.bounds,
                self.hazard_grid.bounds,
            )

            # Add to the dict
            _d[file.rsplit(".", 1)[1]] = data
        # When all is done, add it
        self.exposure_geoms = _d

    def _set_chunking(self):
        """_summary_."""
        # Determine maximum geometry dataset size
        max_geom_size = max(
            [item.count for item in self.exposure_geoms.values()],
        )
        # Set calculations chunk size
        self.chunk = max_geom_size
        _chunk = self.cfg.get("global.geom.chunk")
        if _chunk is not None:
            self.chunk = max(GEOM_MIN_CHUNK, _chunk)

        # Set cache size for outgoing data
        _out_chunk = self.cfg.get("output.geom.settings.chunk")
        if _out_chunk is None:
            _out_chunk = GEOM_MIN_WRITE_CHUNK
        self.cfg["output.geom.settings.chunk"] = _out_chunk

        # Determine amount of threads
        self.nchunk = max_geom_size // self.chunk
        if self.nchunk == 0:
            self.nchunk = 1
        # Constrain by max threads
        if self.max_threads < self.nchunk:
            logger.warning(
                f"Less threads ({self.max_threads}) available than \
calculated chunks ({self.nchunk})"
            )
            self.nchunk = self.max_threads

        # Set the 1D chunks
        self.chunks = create_1d_chunk(
            max_geom_size,
            self.nchunk,
        )

    def _set_num_threads(self):
        """_summary_."""
        self.nthreads = geom_threads(
            self.max_threads,
            self.hazard_grid.count,
            self.nchunk,
        )

    def resolve(
        self,
    ):
        """Create permanent output.

        This is done but reading, loading and sorting the temporary output within
        the `.tmp` folder within the output folder. \n

        - This method might become private.
        """
        # Define the outgoing file
        out_csv = "output.csv"
        if "output.csv.name" in self.cfg:
            out_csv = self.cfg["output.csv.name"]
        self.cfg["output.csv.name"] = out_csv

        # Create an empty csv file for the separate thread to till
        csv_def_file(
            Path(self.cfg["output.path"], out_csv),
            self.exposure_data.columns + tuple(self.cfg["output.new_columns"]),
        )

        # Do the same for the geometry files
        for key in self.exposure_geoms.keys():
            _add = key[-1]
            # Define outgoing dataset
            out_geom = f"spatial{_add}.gpkg"
            if f"output.geom.name{_add}" in self.cfg:
                out_geom = self.cfg[f"output.geom.name{_add}"]
            self.cfg[f"output.geom.name{_add}"] = out_geom
            with open_geom(
                Path(self.cfg.get("output.path"), out_geom), mode="w", overwrite=True
            ) as _w:
                pass

        # If more than one thread, start a pool
        if self.nthreads > 1:
            futures = []
            with ProcessPoolExecutor(max_workers=self.nthreads) as Pool:
                csv_lock = self._mp_manager.Lock()
                geom_lock = self._mp_manager.Lock()
                for chunk in self.chunks:
                    # Submit the all chunks
                    fs = Pool.submit(
                        geom_resolve,
                        self.cfg,
                        self.exposure_data,
                        self.exposure_geoms,
                        chunk,
                        csv_lock,
                        geom_lock,
                    )
                    futures.append(fs)
            wait(futures)

        # When there is only 1 thread neccessary
        # just use process directly
        else:
            p = Process(
                target=geom_resolve,
                args=(
                    self.cfg,
                    self.exposure_data,
                    self.exposure_geoms,
                    self.chunks[0],
                    None,
                    None,
                ),
            )
            p.start()
            logger.info("Busy...")
            p.join()

    def run(
        self,
    ):
        """Run the geometry model with provided settings.

        Generates output in the specified `output.path` directory.
        """
        # Setup lock list for refs
        locks = []

        # Get band names for logging
        _nms = self.cfg.get("hazard.band_names")

        # Setup the mp logger for missing stuff
        _receiver = setup_mp_log(
            self._queue, "missing", level=2, dst=self.cfg.get("output.path")
        )

        logger.info("Starting the calculations")

        # Start the receiver (which is in a seperate thread)
        _receiver.start()

        logger.info(f"Using number of threads: {self.nthreads}")

        # If there are more than a hazard band in the dataset
        # Use a pool to execute the calculations
        if self.nthreads > 1:
            futures = []
            with ProcessPoolExecutor(max_workers=self.nthreads) as Pool:
                _s = time.time()
                for idx in range(self.hazard_grid.count):
                    # Create a lock
                    nlock = self._mp_manager.Lock()
                    locks.append(nlock)

                    # Log for the current hazard map
                    logger.info(
                        f"Submitting jobs for the calculations \
in regards to band: '{_nms[idx]}'"
                    )

                    # Create the temp file plus header
                    csv_temp_file(
                        self.cfg["output.path.tmp"],
                        idx + 1,
                        self.exposure_data.meta["index_name"],
                        self.exposure_data.create_specific_columns(_nms[idx]),
                    )

                    # Loop through all the chunks
                    for chunk in self.chunks:
                        fs = Pool.submit(
                            geom_worker,
                            self.cfg,
                            self._queue,
                            self.hazard_grid,
                            idx + 1,
                            self.vulnerability_data,
                            self.exposure_data,
                            self.exposure_geoms,
                            chunk,
                            nlock,
                        )
                        futures.append(fs)
            logger.info("Busy...")

            # Wait for the children to finish their calculations
            wait(futures)

        # If there is only one hazard band present, call Process directly
        # No need for the extra overhead the Pool provides
        else:
            logger.info("Submitting a job for the calculations in a seperate process")
            _s = time.time()

            # Create the temp file plus header
            csv_temp_file(
                self.cfg["output.path.tmp"],
                1,
                self.exposure_data.meta["index_name"],
                self.exposure_data.create_specific_columns(_nms[0]),
            )

            # Start the calculations
            p = Process(
                target=geom_worker,
                args=(
                    self.cfg,
                    self._queue,
                    self.hazard_grid,
                    1,
                    self.vulnerability_data,
                    self.exposure_data,
                    self.exposure_geoms,
                    self.chunks[0],
                    None,
                ),
            )
            p.start()
            logger.info("Busy...")
            p.join()
        _e = time.time() - _s

        logger.info(f"Calculations time: {round(_e, 2)} seconds")
        # After the calculations are done, close the receiver
        _receiver.close()
        _receiver.close_handlers()
        if _receiver.count > 0:
            logger.warning(
                f"Some objects had missing data. For more info: \
'missing.log' in '{self.cfg.get('output.path')}'"
            )
        else:
            os.unlink(
                Path(self.cfg.get("output.path"), "missing.log"),
            )

        logger.info("Producing model output from temporary files")
        # Patch output from the seperate processes back together
        self.resolve()
        logger.info(f"Output generated in: '{self.cfg['output.path']}'")

        if not self._keep_temp:
            logger.info("Deleting temporary files...")
            self._clean_up()

        logger.info("Geom calculation are done!")
