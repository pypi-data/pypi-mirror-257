"""Input and output base objects"""


import json
from typing import Optional, Self

from pydantic import BaseModel, ValidationError


class InputModel(BaseModel):
    """A base class for defining the input schema of a processor"""

    @classmethod
    def from_file(cls, input_data_path: str) -> Optional[Self]:
        """Load and return the input data from JSON file.

        Args:
          input_data_path(str): Path to the JSON file where the input is stored

        Returns:
          Optional[Self]: The object loaded from the input file if loading was sucessful
        """

        with open(input_data_path, "r", encoding="utf-8") as file:
            input_data = json.load(file)

            try:
                input_model = cls(**input_data)
                return input_model

            except ValidationError as e:
                print(f"Input validation error: {e.errors()}")
                return None


class OutputModel(BaseModel):
    """A base class for defining the ouput schema of a processor"""
