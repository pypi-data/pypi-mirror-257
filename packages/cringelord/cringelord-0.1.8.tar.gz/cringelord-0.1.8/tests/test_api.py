import inspect
import os
import pathlib
from unittest.mock import patch

import pytest

from cringelord import api
from cringelord.app.exceptions import MissingConfigValueError


FILE_PATH = pathlib.Path(inspect.getsourcefile(lambda: 0)).resolve()
DIR_PATH = pathlib.Path(inspect.getsourcefile(lambda: 0)).resolve().parent


class TestAPI:
    class TestGetSetting:
        class TestDeserialization:
            @pytest.mark.parametrize(
                ("serialized_value", "deserialized_value"),
                [
                    ("42", 42),
                    ("4.2", 4.2),
                    ("normal_string", "normal_string"),
                    ('{"name": 42}', {"name": 42}),
                    ('{"dict": {"name": 42}}', {"dict": {"name": 42}}),
                    ("[1, 2, 3]", [1, 2, 3]),
                    ("[1, [1, 2, 3], 3]", [1, [1, 2, 3], 3]),
                    ('{"name": [1, 2, 3]}', {"name": [1, 2, 3]})
                ],
                ids=[
                    "int",
                    "float",
                    "string",
                    "dict_with_int",
                    "nested_dict",
                    "list",
                    "nested_list",
                    "dict_with_list"
                ]
            )
            def test_float(
                    self,
                    serialized_value,
                    deserialized_value,
                    monkeypatch
            ):
                setting_name = "setting_name"
                monkeypatch.setenv(
                    setting_name,
                    serialized_value
                )

                actual_value = api.get_cringe_setting(setting_name)

                assert actual_value == deserialized_value

        class TestMissingConfig:
            typo_setting_name = "my_seting"
            correct_setting_name = "my_setting"

            def test_typo_in_request(self, monkeypatch):
                monkeypatch.setenv(
                    self.correct_setting_name,
                    "does not matter"
                )

                with pytest.raises(MissingConfigValueError):
                    api.get_cringe_setting(self.typo_setting_name)

            def test_typo_in_env(self, monkeypatch):
                monkeypatch.setenv(
                    self.typo_setting_name,
                    "does not matter"
                )

                with pytest.raises(MissingConfigValueError):
                    api.get_cringe_setting(self.correct_setting_name)

    class TestLoad:
        @patch("cringelord.app.app.load_from_app_dir")
        def test_paths(self, mock_app):
            environment_name = "environment_name"

            api.load(FILE_PATH, DIR_PATH, environment_name)

            mock_app.assert_called_with(FILE_PATH, DIR_PATH, environment_name)

        @patch("cringelord.app.app.load_from_app_dir")
        def test_path_strings(self, mock_app):
            config_path = str(FILE_PATH)
            app_dir = str(DIR_PATH)
            environment_name = "environment_name"

            api.load(config_path, app_dir, environment_name)

            mock_app.assert_called_with(FILE_PATH, DIR_PATH, environment_name)

        @patch("cringelord.app.app.load_from_app_dir")
        def test_get_environment_name_from_env(self, mock_app):
            environment_name = "environment_name_in_env"
            os.environ[api.ENVIRONMENT_NAME_KEY] = environment_name

            api.load(FILE_PATH, DIR_PATH)

            mock_app.assert_called_with(FILE_PATH, DIR_PATH, environment_name)

        @patch("cringelord.app.app.load_from_app_dir")
        @pytest.mark.parametrize(
            "environment_name",
            [
                "FULLY UPPER CASE",
                "Capitalized",
                "MiXeD CaSe"
            ]
        )
        def test_upper_case_environment_name(self, mock_app, environment_name):
            expected_environment_name = environment_name.lower()

            api.load(FILE_PATH, DIR_PATH, environment_name)

            mock_app.assert_called_with(
                FILE_PATH,
                DIR_PATH,
                expected_environment_name)

    class TestLoadAll:
        @patch("cringelord.app.app.load_all")
        def test_paths(self, mock_app):
            environment_name = "environment_name"

            api.load_all(FILE_PATH, environment_name)

            mock_app.assert_called_with(FILE_PATH, environment_name)

        @patch("cringelord.app.app.load_all")
        def test_path_strings(self, mock_app):
            config_path = str(FILE_PATH)
            environment_name = "environment_name"

            api.load_all(config_path, environment_name)

            mock_app.assert_called_with(FILE_PATH, environment_name)

        @patch("cringelord.app.app.load_all")
        def test_get_environment_name_from_env(self, mock_app):
            environment_name = "environment_name_in_env"
            os.environ[api.ENVIRONMENT_NAME_KEY] = environment_name

            api.load_all(FILE_PATH)

            mock_app.assert_called_with(FILE_PATH, environment_name)

        @patch("cringelord.app.app.load_all")
        @pytest.mark.parametrize(
            "environment_name",
            [
                "FULLY UPPER CASE",
                "Capitalized",
                "MiXeD CaSe"
            ]
        )
        def test_upper_case_environment_name(self, mock_app, environment_name):
            expected_environment_name = environment_name.lower()

            api.load_all(FILE_PATH, environment_name)

            mock_app.assert_called_with(FILE_PATH, expected_environment_name)
