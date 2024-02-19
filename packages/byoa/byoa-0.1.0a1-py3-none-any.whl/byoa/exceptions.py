"""BYOA exceptions"""

from byoa import MANIFEST_FILE


class ByoaException(Exception):
    """Base BYOA error"""


class NoManifestFoundException(ByoaException):
    """Raised when the byoa manifest file is missing"""

    def __init__(self):
        super().__init__(
            f"No '{MANIFEST_FILE}' file found, make sure that you are inside a BYOA project."
        )


class UnknownKeyException(ByoaException):
    """Raised when the configuration key is not handled

    Args:
        key (str): The unknown configuration key
    """

    def __init__(self, key: str):
        super().__init__(f"Unknown configuration key '{key}'.")


class MissingContextValue(ByoaException):
    """Raised when an context value is missing"""

    def __init__(self, key: str):
        super().__init__(f"Missing context value for '{key}'")


class APIError(ByoaException):
    """Raised when an error occures communicating to the API"""
