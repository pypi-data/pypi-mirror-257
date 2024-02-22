import os

from pydantic import constr, DirectoryPath, FilePath, validate_call

from cringelord.app import app
from cringelord.app.util import (
    get_raw_setting_value_from_env,
    to_python_object
)


ENVIRONMENT_NAME_KEY = "ENVIRONMENT_NAME"


@validate_call
def get_cringe_setting(name: str):
    """
    Retrieves a setting's value as a Python object from the environment
        configured by Cringe Lord.

    If you require the serialized value as-is, you should request it directly
        via 'os.environ["setting_name"]'.

    Args:
        name (str): The name of the setting.

    Returns:
        The setting's value de-serialized into a Python object.

    Raises:
        MissingConfigValueError: If you're requesting a setting that's not
            present in the environment.
            We chose to raise an exception instead of returning a default
            value, because the writer of the script should be aware that
            (s)he's missing configuration values. This approach, for example,
            clarifies that you've made a typo, preventing nasty bugs.
    """
    raw_setting_value = get_raw_setting_value_from_env(name)

    return to_python_object(raw_setting_value)


@validate_call
def load(
        config_path: FilePath,
        app_dir: DirectoryPath,
        environment_name: constr(to_lower=True) = None
):
    if not environment_name:
        environment_name = os.getenv(ENVIRONMENT_NAME_KEY)

    app.load_from_app_dir(config_path, app_dir, environment_name)


@validate_call
def load_all(
        config_path: FilePath,
        environment_name: constr(to_lower=True) = None
):
    if not environment_name:
        environment_name = os.getenv(ENVIRONMENT_NAME_KEY)

    app.load_all(config_path, environment_name)
