""" Configuration utility modules """

import importlib
from typing import Any, Callable


def get_class_from_dot_path(path: str) -> Callable:
    """Imports module from dot notation string path"""
    module_path, class_name = path.rsplit(".", 1)
    try:
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ModuleNotFoundError, AttributeError) as exp:
        raise ValueError(f"Provided log check class path <{path}> is invalid") from exp


def safe_access(variable: Any, attribute_path: str) -> Any:
    """Returns the end attribute value by first checking the existence of intermediary attributes

    Args:
        variable (Any): variable for attribute access
        attribute_path (str): dot notated string
    Returns:
        final attribute value from the dot notated string
    Raises:
        TypeError: When intermediate attribute is None

    """
    current_path_list = attribute_path.split(".")
    last_variable = variable
    while current_path_list:
        current_attribute = current_path_list.pop(0)
        current_attribute_value = getattr(last_variable, current_attribute)
        if current_attribute_value is None:
            raise TypeError(
                f"Attempting to perform illegal operationn with a None object {current_attribute}"
            )
        last_variable = current_attribute_value

    return last_variable
