import json
import os

from cringe_lord.app.util import get_setting_from_env


class TestGetSettingFromEnv:
    def test_returns_setting_value_if_exists(self, mocker):
        # Arrange
        setting_name = "setting_that_exists"
        expected_value = "db.example.com"

        mocker.patch.dict(os.environ, {setting_name: expected_value})

        # Act
        actual_value = get_setting_from_env(setting_name)

        # Assert
        assert actual_value == expected_value

    #  Returns None if the setting does not exist in the environment.
    def test_returns_none_if_setting_does_not_exist(self, mocker):
        # Arrange
        setting_name = "setting_doesnt_exist"

        # Act
        actual_value = get_setting_from_env(setting_name)

        # Assert
        assert actual_value is None

    #  Parses the value as JSON if it is valid JSON.
    def test_parses_value_as_json_if_valid_json(self, mocker):
        # Arrange
        setting_name = "valid_json_setting"
        expected_value = {"host": "db.example.com", "port": 5432}

        mocker.patch.dict(os.environ, {setting_name: json.dumps(expected_value)})

        # Act
        actual_value = get_setting_from_env(setting_name)

        # Assert
        assert actual_value == expected_value

    #  Returns the value as is if it is not valid JSON.
    def test_returns_value_as_is_if_not_valid_json(self, mocker):
        # Arrange
        setting_name = "not_valid_json_setting"
        expected_value = "db.example.com"

        mocker.patch.dict(os.environ, {setting_name: expected_value})

        # Act
        actual_value = get_setting_from_env(setting_name)

        # Assert
        assert actual_value == expected_value
