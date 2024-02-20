"""Custom errors for FIAT."""


class DriverNotFoundError(Exception):
    """_summary_."""

    def __init__(self, gog, path):
        self.base = f"{gog} data"
        self.msg = f"Extension of file: {path.name} is not recoqnized"
        super(DriverNotFoundError, self).__init__(self.base)

    def __str__(self):
        return f"{self.base} -> {self.msg}"
