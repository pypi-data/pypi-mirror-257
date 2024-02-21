import json
import os
from typing import Any

from pydantic import constr, validate_call


DEFAULT_VALUE = None


@validate_call
def get_setting_from_env(setting_name: constr(to_lower=True)) -> Any:
    """
    Best practice method to get a setting from the environment.

    Args:
        setting_name (str): The name of the setting.

    Returns:
        The setting's value.
    """
    value = _get_value(setting_name)

    return _parse_value(value)


def _get_value(setting_name):
    try:
        return os.environ[setting_name]
    except KeyError:
        return None


def _parse_value(value):
    try:
        return json.loads(value)
    except json.decoder.JSONDecodeError:
        return value
    except TypeError:
        return DEFAULT_VALUE
