from pathlib import Path

from pydantic_yaml import parse_yaml_file_as

from .cringe_config import CringeConfig
from .exceptions import (
    CringeConfigNotFoundError,
    InvalidCringeConfigYamlError,
    InvalidCringeConfigPathError
)


def create(config_path):
    if not isinstance(config_path, (str, Path)):
        raise InvalidCringeConfigPathError(config_path)

    if isinstance(config_path, str):
        config_path = Path(config_path)

    if not config_path.is_file():
        raise CringeConfigNotFoundError(config_path)

    if not (cringe_config := parse_yaml_file_as(CringeConfig, config_path)):
        raise InvalidCringeConfigYamlError(config_path)

    return cringe_config
