import os

import pytest
import yaml

from cringe_lord.app import load_settings, load_from_app_dir, load_all
from cringe_lord.app.util import get_setting_from_env
from cringe_lord.app.cringe_config.exceptions import CringeConfigNotFoundError


VALID_CONSTANTS = {
        "VAR1",
        "VAR2",
        "VAR3",
        "VAR4",
        "VAR5",
        "VAR6",
        "VAR7",
        "VAR8",
        "VAR9",
        "VAR10",
        "VAR11",
        "VAR12",
        "VAR13",
        "VAR14",
        "VAR15",
        "VAR16",
        "VAR17",
        "VAR18"
    }

CONSTANTS1 = {
    "VAR1",
    "VAR2",
    "VAR3",
    "VAR4",
    "VAR5",
    "VAR6"
}

CONSTANTS2 = {
    "VAR7",
    "VAR8",
    "VAR9",
    "VAR10",
    "VAR11",
    "VAR12"
}

CONSTANTS3 = {
    "VAR13",
    "VAR14",
    "VAR15",
    "VAR16",
    "VAR17",
    "VAR18"
}

SRC_CODE_MIXED_CONSTANTS1 = """
import os

environ["VAR1"]
os.environ["VAR2"]
getenv("VAR3")
for x in range(10):
    print(f"Some other code {x}")
print("VAR4: " + getenv("VAR4", None))
print("VAR5: " + getenv("VAR5", default=None))
print("VAR6: " + getenv(key="VAR6", default=None))
"""

SRC_CODE_MIXED_CONSTANTS2 = """
import os

os.getenv("VAR7")
os.getenv("VAR8", None)
os.getenv("VAR9", default=None)
print("VAR10: " + os.getenv(key="VAR10", default=None))
print("VAR11: " + environ.get("VAR11"))
print("VAR12: " + environ.get("VAR12", None))

for x in range(10):
    print(f"Some other code {x}")

"""

SRC_CODE_MIXED_CONSTANTS3 = """
import os

for x in range(10):
    print(f"Some other code {x}")

environ.get("VAR13", default=None)
environ.get(key="VAR14", default=None)
os.environ.get("VAR15")
print("VAR16: " + os.environ.get("VAR16", None))
print("VAR17: " + os.environ.get("VAR17", default=None))
print("VAR18: " + os.environ.get(key="VAR18", default=None))
"""

SRC_CODE_WITH_VARIABLE = """
import os

for x in range(10):
    print(f"Some other code {x}")
    
my_var = "value_of_my_var"

environ.get("VAR13", default=None)
environ.get(key="VAR14", default=None)
os.environ.get("VAR15")
print("VAR16: " + os.environ.get("VAR16", None))
print("VAR17: " + os.environ.get("VAR17", default=None))
print("VAR18: " + os.environ.get(key=my_var, default=None))
"""

SRC_CODE_WITH_SETTING_NOT_IN_CONFIG = """
import os

for x in range(10):
    print(f"Some other code {x}")
    
environ.get("VAR13", default=None)
environ.get(key="VAR14", default=None)
os.environ.get("VAR15")
print("VAR16: " + os.environ.get("VAR16", None))
print("VAR17: " + os.environ.get("VAR17", default=None))
print("VAR18: " + os.environ.get(key="does_not_exist", default=None))
"""


@pytest.fixture(scope="function")
def nested_directory(tmp_path):
    directory = tmp_path / "test_directory"
    directory.mkdir()

    python_file_paths = []

    python_file_path1 = directory / "file1.py"
    python_file_path1.touch()
    python_file_paths.append(python_file_path1)
    python_file_path2 = directory / "file2.py"
    python_file_path2.touch()
    python_file_paths.append(python_file_path2)

    subdirectory1 = directory / "subdirectory"
    subdirectory1.mkdir()

    python_file_path3 = subdirectory1 / "file3.py"
    python_file_path3.touch()
    python_file_paths.append(python_file_path3)

    return directory, python_file_paths


@pytest.fixture(scope="function")
def nested_directory_all_constants(nested_directory):
    directory, python_file_paths = nested_directory

    python_file_path1 = python_file_paths[0]
    python_file_path2 = python_file_paths[1]
    python_file_path3 = python_file_paths[2]

    python_file_path1.write_text(SRC_CODE_MIXED_CONSTANTS1)
    python_file_path2.write_text(SRC_CODE_MIXED_CONSTANTS2)
    python_file_path3.write_text(SRC_CODE_MIXED_CONSTANTS3)

    return directory


@pytest.fixture(scope="function")
def nested_directory_with_variable(nested_directory):
    directory, python_file_paths = nested_directory

    python_file_path1 = python_file_paths[0]

    python_file_path1.write_text(SRC_CODE_WITH_VARIABLE)

    return directory


@pytest.fixture(scope="function")
def nested_directory_with_non_existing_setting(nested_directory):
    directory, python_file_paths = nested_directory

    python_file_path1 = python_file_paths[0]

    python_file_path1.write_text(SRC_CODE_WITH_SETTING_NOT_IN_CONFIG)

    return directory


@pytest.fixture(scope="function")
def nested_directory_constants1(nested_directory):
    directory, python_file_paths = nested_directory

    python_file_path1 = python_file_paths[0]

    python_file_path1.write_text(SRC_CODE_MIXED_CONSTANTS1)

    return directory


@pytest.fixture(scope="function")
def nested_directory_constants2(nested_directory):
    directory, python_file_paths = nested_directory

    python_file_path2 = python_file_paths[1]

    python_file_path2.write_text(SRC_CODE_MIXED_CONSTANTS2)

    return directory


@pytest.fixture(scope="function")
def nested_directory_constants3(nested_directory):
    directory, python_file_paths = nested_directory

    python_file_path3 = python_file_paths[2]

    python_file_path3.write_text(SRC_CODE_MIXED_CONSTANTS3)

    return directory


@pytest.fixture(scope="function")
def set_settings():
    """
    Fill this fixture with the settings you load into the environment, so that
        we can clean them up after the test function.
    """

    set_settings = []

    yield set_settings

    for setting_name in set_settings:
        del os.environ[setting_name]


CONFIG_DICT = {
    "metadata": {
        "metadata": {
            "author": "Thomas Vanhelden",
            "company": "Cegeka"
        }
    },
    "environment_config": {
        "production_key": {
            "name": "production_name",
            "description": "Production Environment",
            "aliases": [
                "production_alias1",
                "production_alias2"
            ],
            "settings": {
                "VAR1": "var1_value_production",
                "VAR2": 2.0,
                "VAR3": False,
                "VAR4": 5,
                "VAR5": "var5_value_production",
                "VAR6": "var6_value_production",
                "VAR7": "var7_value_production",
                "VAR8": "var8_value_production",
                "VAR9": "var9_value_production",
                "VAR10": ["var10", "value", "production"],
                "VAR11": {"var": 11, "value": "production"},
                "VAR12": {
                    "var": ["var", 12],
                    "value": {
                        "key": "value",
                        "production": ["prod", "uction"]
                    }
                }
            }
        },
        "acceptance_key": {
            "name": "acceptance_name",
            "description": "Acceptance Environment",
            "aliases": [
                "acceptance_alias1",
                "acceptance_alias2"
            ],
            "settings": {
                "VAR1": "var1_value_acceptance",
                "VAR2": 3.0,
                "VAR3": True,
                "VAR4": 4,
                "VAR5": "var5_value_acceptance",
                "VAR6": "var6_value_acceptance",
                "VAR7": "var7_value_acceptance",
                "VAR8": "var8_value_acceptance",
                "VAR9": "var9_value_acceptance",
                "VAR10": ["var10", "value", "acceptance"],
                "VAR11": {"var": 11, "value": "acceptance"},
                "VAR12": {
                    "var": ["var", 12],
                    "value": {
                        "key": "value",
                        "acceptance": ["acc", "eptance"]
                    }
                }
            }
        }
    },
    "general_config": {
        "VAR13": "var13_general_value",
        "VAR14": "var14_general_value",
        "VAR15": "var15_general_value",
        "VAR16": "var16_general_value",
        "VAR17": "var17_general_value",
        "VAR18": "var18_general_value"
    }
}

ENVIRONMENT_SETTINGS = [
    "VAR1",
    "VAR2",
    "VAR3",
    "VAR4",
    "VAR5",
    "VAR6",
    "VAR7",
    "VAR8",
    "VAR9",
    "VAR10",
    "VAR11",
    "VAR12"
]
GENERAL_SETTINGS = [
    "VAR13",
    "VAR14",
    "VAR15",
    "VAR16",
    "VAR17",
    "VAR18"
]


@pytest.fixture(scope="function")
def config_path(tmp_path):
    config_path = tmp_path / "cringe_config.yaml"
    config_path.write_text(yaml.dump(CONFIG_DICT))

    return config_path


@pytest.fixture(scope="function")
def non_existing_config_path(tmp_path):
    return tmp_path / "cringe_config.yaml"


def get_setting_from_config_dict(setting_name, environment_name=None):
    if environment_name:
        environment = CONFIG_DICT["environment_config"][environment_name]
        return environment["settings"][setting_name]
    else:
        return CONFIG_DICT["general_config"][setting_name]


def get_environment_from_alias(alias):
    for environment in CONFIG_DICT["environment_config"]:
        if alias in CONFIG_DICT["environment_config"][environment]["aliases"]:
            return environment


def get_environment_from_name(name):
    for environment in CONFIG_DICT["environment_config"]:
        if name == CONFIG_DICT["environment_config"][environment]["name"]:
            return environment


class TestApp:
    class TestLoadAll:
        @pytest.mark.parametrize(
            "environment_key",
            [
                "production_key",
                "acceptance_key"
            ]
        )
        def test(self, config_path, environment_key):
            load_all(config_path, environment_key)

            for var_name in VALID_CONSTANTS:
                actual_setting = get_setting_from_env(var_name)
                if var_name in GENERAL_SETTINGS:
                    expected_setting = get_setting_from_config_dict(
                        var_name
                    )
                else:
                    expected_setting = get_setting_from_config_dict(
                        var_name,
                        environment_key
                    )

                assert actual_setting == expected_setting

    class TestMain:
        @pytest.mark.parametrize(
            "key",
            [
                "production_key",
                "acceptance_key"
            ]
        )
        def test_environment_key(
                self,
                config_path,
                nested_directory_all_constants,
                key
        ):
            environment_name = key
            load_from_app_dir(
                config_path,
                nested_directory_all_constants,
                environment_name
            )
            for var_name in VALID_CONSTANTS:
                actual_setting = get_setting_from_env(var_name)
                if var_name in GENERAL_SETTINGS:
                    expected_setting = get_setting_from_config_dict(
                        var_name
                    )
                else:
                    expected_setting = get_setting_from_config_dict(
                        var_name,
                        environment_name
                    )

                assert actual_setting == expected_setting

        @pytest.mark.parametrize(
            "alias",
            [
                "production_alias1",
                "production_alias2",
                "acceptance_alias1",
                "acceptance_alias2"
            ]
        )
        def test_alias(
                self,
                config_path,
                nested_directory_all_constants,
                alias
        ):
            environment_name = get_environment_from_alias(alias)

            load_from_app_dir(
                config_path,
                nested_directory_all_constants,
                alias
            )
            for var_name in VALID_CONSTANTS:
                actual_setting = get_setting_from_env(var_name)
                if var_name in GENERAL_SETTINGS:
                    expected_setting = get_setting_from_config_dict(
                        var_name
                    )
                else:
                    expected_setting = get_setting_from_config_dict(
                        var_name,
                        environment_name
                    )

                assert actual_setting == expected_setting

        @pytest.mark.parametrize(
            "name",
            [
                "production_name",
                "acceptance_name"
            ]
        )
        def test_name(
                self,
                config_path,
                nested_directory_all_constants,
                name
        ):
            environment_name = get_environment_from_name(name)

            load_from_app_dir(
                config_path,
                nested_directory_all_constants,
                name
            )
            for var_name in VALID_CONSTANTS:
                actual_setting = get_setting_from_env(var_name)
                if var_name in GENERAL_SETTINGS:
                    expected_setting = get_setting_from_config_dict(
                        var_name
                    )
                else:
                    expected_setting = get_setting_from_config_dict(
                        var_name,
                        environment_name
                    )

                assert actual_setting == expected_setting

        def test_non_existing_setting_wont_be_added(
            self,
            config_path,
            nested_directory_with_non_existing_setting
        ):
            load_from_app_dir(
                config_path,
                nested_directory_with_non_existing_setting,
                "production_key"
            )

            assert not get_setting_from_env("does_not_exist")

        def test_all_settings_when_variable_in_code(
            self,
            config_path,
            nested_directory_with_variable
        ):
            load_from_app_dir(
                config_path,
                nested_directory_with_variable,
                "production_key"
            )
            for var_name in VALID_CONSTANTS:
                actual_setting = get_setting_from_env(var_name)
                if var_name in GENERAL_SETTINGS:
                    expected_setting = get_setting_from_config_dict(
                        var_name
                    )
                else:
                    expected_setting = get_setting_from_config_dict(
                        var_name,
                        "production_key"
                    )

                assert actual_setting == expected_setting

        def test_error_non_existing_path(
                self,
                non_existing_config_path,
                nested_directory_all_constants
        ):
            with pytest.raises(CringeConfigNotFoundError):
                load_from_app_dir(
                    non_existing_config_path,
                    nested_directory_all_constants,
                    "production_key"
                )

        def test_constants1(self, config_path, nested_directory_constants1):
            load_from_app_dir(
                config_path,
                nested_directory_constants1,
                "production_key"
            )
            for var_name in CONSTANTS1:
                actual_setting = get_setting_from_env(var_name)

                expected_setting = get_setting_from_config_dict(
                    var_name,
                    "production_key"
                )

                assert actual_setting == expected_setting

        def test_constants2(self, config_path, nested_directory_constants2):
            load_from_app_dir(
                config_path,
                nested_directory_constants2,
                "production_key"
            )
            for var_name in CONSTANTS2:
                actual_setting = get_setting_from_env(var_name)

                expected_setting = get_setting_from_config_dict(
                    var_name,
                    "production_key"
                )

                assert actual_setting == expected_setting

        def test_constants3(self, config_path, nested_directory_constants3):
            load_from_app_dir(
                config_path,
                nested_directory_constants3,
                "production_key"
            )
            for var_name in CONSTANTS3:
                actual_setting = get_setting_from_env(var_name)

                expected_setting = get_setting_from_config_dict(
                    var_name
                )

                assert actual_setting == expected_setting

    class TestLoadSettings:
        @pytest.mark.parametrize(
            "settings_to_load",
            [
                {},
                {"setting1": "value1"},
                {"setting1": "value1", "setting2": "value2"},
            ],
            ids=[
                "no_settings",
                "single_setting",
                "multiple_settings",
            ]
        )
        def test_load_setting(self, set_settings, settings_to_load):
            set_settings.extend(list(settings_to_load.keys()))

            load_settings(settings_to_load)

            for setting_name, setting_value in settings_to_load.items():
                assert os.environ[setting_name] == setting_value
