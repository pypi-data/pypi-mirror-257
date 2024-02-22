import json
import os

from cringelord.app.exceptions import MissingConfigValueError


def get_raw_setting_value_from_env(setting_name):
    try:
        return os.environ[setting_name]
    except KeyError:
        raise MissingConfigValueError(setting_name)


def to_python_object(raw_value):
    try:
        return json.loads(raw_value)
    except json.decoder.JSONDecodeError:
        return raw_value
