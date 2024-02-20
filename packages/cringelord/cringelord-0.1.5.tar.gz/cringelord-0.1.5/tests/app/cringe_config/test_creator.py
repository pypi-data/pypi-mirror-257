from pathlib import Path

import pytest
import yaml

from cringe_lord.app.cringe_config.creator import create
from cringe_lord.app.cringe_config.cringe_config import CringeConfig
from cringe_lord.app.cringe_config.exceptions import (
    CringeConfigNotFoundError,
    InvalidCringeConfigPathError,
    InvalidCringeConfigYamlError
)


CONFIG_DICT = {
    "metadata": {
        "metadata": {
            "author": "Thomas Vanhelden",
            "company": "Cegeka"
        }
    },
    "environment_config": {
        "production": {
            "name": "Production",
            "description": "Production Environment",
            "aliases": [
                "prod",
                "production"
            ],
            "settings": {
                "usd_pim_id": 1234,
                "analytics_pim_id": 4321
            }
        },
        "acceptance": {
            "name": "Acceptance",
            "description": "Acceptance Environment",
            "aliases": [
                "acc",
                "acceptance"
            ],
            "settings": {
                "usd_pim_id": 5678,
                "analytics_pim_id": 8765
            }
        }
    },
    "general_config": {
        "pim_api": {
            "service_name": "pim_api",
            "username": "pim_soc_srvc_account"
        }
    }
}


@pytest.fixture(scope="function")
def config_path(tmp_path):
    config_path = tmp_path / "cringe_config.yaml"
    config_path.write_text(yaml.dump(CONFIG_DICT))

    return config_path


@pytest.fixture(scope="function")
def non_existing_config_path(tmp_path):
    return tmp_path / "cringe_config.yaml"


class TestCreator:
    def test_create_config(self, config_path):
        expected_config = CringeConfig(**CONFIG_DICT)

        actual_config = create(config_path)

        assert actual_config == expected_config

    def test_create_config_from_string(self, config_path):
        expected_config = CringeConfig(**CONFIG_DICT)

        actual_config = create(str(config_path))

        assert actual_config == expected_config

    def test_raises_error_non_existing_file(self, non_existing_config_path):
        with pytest.raises(CringeConfigNotFoundError):
            create(non_existing_config_path)

    def test_raises_error_non_existing_path(self):
        with pytest.raises(CringeConfigNotFoundError):
            create(Path("/some/non/existing/path"))

    def test_raises_error_no_path(self):
        with pytest.raises(InvalidCringeConfigPathError):
            create(["this", "is", "not", "a", "path"])

    def test_raises_error_not_a_file(self, tmp_path):
        with pytest.raises(CringeConfigNotFoundError):
            create(tmp_path)

    def test_raises_error_invalid_yaml(self, tmp_path):
        invalid_yaml = """
        if __name__ == "__main__":
            print("This is not a yaml file."
        """
        config_path = tmp_path / "cringe_config.yaml"
        config_path.write_text(invalid_yaml)

        with pytest.raises(InvalidCringeConfigYamlError):
            create(config_path)
