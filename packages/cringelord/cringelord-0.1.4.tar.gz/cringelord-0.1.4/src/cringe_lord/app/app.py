import json
import os

from cringe_lord.app.src_directory import (
    directory as directory_parser
)
from cringe_lord.app.src_directory import file as file_parser
from cringe_lord.app.cringe_config.creator import create
from cringe_lord.app.src_directory.exceptions import NamedCallDetected
from cringe_lord.app.cringe_config.exceptions import SettingNotFoundError


def load_from_app_dir(config_path, app_dir, environment_name=None):
    try:
        setting_names = _get_env_call_var_names(app_dir)
    except NamedCallDetected:
        settings = get_all_settings(config_path, environment_name)
    else:
        settings = _get_settings(config_path, setting_names, environment_name)

    load_settings(settings)


def load_all(config_path, environment_name=None):
    settings = get_all_settings(config_path, environment_name)
    load_settings(settings)


def _get_env_call_var_names(app_dir):
    paths = directory_parser.find_all_python_files_in_directory(app_dir)

    var_names = []
    for path in paths:
        var_names.extend(file_parser.find_env_call_var_names(path))

    return var_names


def _get_settings(config_path, setting_names, environment_name):
    cringe_config = create(config_path)

    settings = {}
    for setting_name in setting_names:
        try:
            setting = cringe_config.get_setting(setting_name, environment_name)
        except SettingNotFoundError:
            continue
        else:
            settings.update({setting_name: setting})

    return settings


def get_all_settings(config_path, environment_name):
    cringe_config = create(config_path)

    return cringe_config.get_all_settings(environment_name)


def load_settings(settings):
    for setting_name, setting_value in settings.items():
        setting_env_key = setting_name.lower()

        if isinstance(setting_value, str):
            setting_env_value = setting_value
        else:
            setting_env_value = json.dumps(setting_value)

        os.environ[setting_env_key] = setting_env_value
