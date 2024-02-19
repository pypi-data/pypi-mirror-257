"""Utility classes and functions to deal with the byoa manifest file"""

from functools import wraps
from pathlib import Path
from typing import Any, Optional

import toml

from byoa import MANIFEST_FILE
from byoa.exceptions import NoManifestFoundException, UnknownKeyException


def check_manifest(function):
    """Checks wether the byoa manifest file exists in the current directory

    Use this decorator to ensure that no statement is executed if the manifest file is missing.
    """

    @wraps(function)  # ensures the docstring is also wrapped
    def wrapper(*args, **kwargs):
        if not Path(MANIFEST_FILE).exists():
            raise NoManifestFoundException

        function(*args, **kwargs)

    return wrapper


class Manifest:
    """Object representation of the byoa manifest file

    Args:
      from_file (bool): if True, will read and load the byoa manifest file.
        Defaults to True.
    """

    POSSIBLE_KEYS = ["name", "slug", "summary", "description", "author"]
    """List of used keys."""

    def __init__(self, from_file=True) -> None:
        if from_file and not Path(MANIFEST_FILE).exists():
            raise NoManifestFoundException

        if not from_file:
            self.__manifest = {}
        else:
            self.__manifest = toml.load(MANIFEST_FILE)

    def set(self, key: str, value):
        """Sets the manifest key/value pair

        Args:
          key (str): The key
          value: The value

        Raises:
          UnknownKeyException: If the key is unknown
        """

        if key not in self.POSSIBLE_KEYS:
            raise UnknownKeyException(key)

        self.__manifest.update({key: value})

    def get(self, key: str) -> Optional[Any]:
        """Returns the value of attribute 'key'

        Args:
          key (str): The key

        Returns:
          Optional[Any]: The value if it exists
        """

        return self.__manifest.get(key)

    def save(self, directory=Path(".")):
        """Saves the manifest as a file

        Args:
          directory (pathlib.Path): The directory in which the file will be saved,
            defaults to the current directory
        """
        with open(directory.joinpath(MANIFEST_FILE), mode="w", encoding="utf-8") as file:
            toml.dump(self.__manifest, file)

    @property
    def name(self):
        """Name of the processor"""
        return self.get("name")

    @property
    def slug(self):
        """Human-readable, unique identifier of the processor"""
        return self.get("slug")

    @property
    def summary(self):
        """A short sentence describing the processor"""
        return self.get("summary")

    @property
    def description(self):
        """Description of the project"""
        return self.get("description")

    @property
    def author(self):
        """Author(s) of the project"""
        return self.get("author")
