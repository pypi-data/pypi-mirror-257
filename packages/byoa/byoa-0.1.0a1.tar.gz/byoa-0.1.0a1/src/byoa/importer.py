""""Import module"""

import importlib

from pydantic import BaseModel


class ModelImportError(Exception):
    """Exception raised when an error occures when importing a model class"""


def get_model_class_from_string(import_string: str) -> BaseModel:
    """Returns the model class designated from the import string

    Args:
        import_string (str): The import string in the written in the module>:<class> format

    Returns:
        BaseModel: The model class
    """
    module_str, _, class_str = import_string.partition(":")

    try:
        module = importlib.import_module(module_str)
    except ModuleNotFoundError as e:
        raise ModelImportError(f"Could not find module {module_str}") from e

    model_class = getattr(module, class_str)

    if not issubclass(model_class, BaseModel):
        raise ModelImportError(
            f"The class `{class_str}` is not a subclass of `pydantic.BaseModel`"
        )

    return model_class
