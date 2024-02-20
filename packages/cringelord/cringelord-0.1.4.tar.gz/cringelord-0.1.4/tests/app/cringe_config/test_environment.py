import pytest

from cringe_lord.app.cringe_config.environment import Environment
from cringe_lord.app.cringe_config.exceptions import SettingNotFoundError


class TestEnvironment:
    def test_create_instance_with_standard_input(self):
        input_name = "env1"
        input_description = "description1"
        input_aliases = ["alias1"]
        input_settings = {"setting1": "value1", "setting2": "value2"}

        environment = Environment(
            name=input_name,
            description=input_description,
            aliases=input_aliases,
            settings=input_settings
        )

        assert environment.name == input_name
        assert environment.description == input_description
        assert environment.aliases == input_aliases
        assert environment.settings == input_settings

    def test_create_instance_with_list_settings(self):
        input_settings = [
            {"setting1": "value1"},
            {"setting2": "value2"}
        ]
        expected_settings = {"setting1": "value1", "setting2": "value2"}

        actual_settings = Environment(
            name="env1",
            description="description1",
            aliases=["alias1"],
            settings=input_settings
        ).settings

        assert expected_settings == actual_settings

    def test_create_instance_with_list_settings_nested(self):
        input_settings = [
            {"setting1": {"nested_setting1": ["nested", "value1"]}},
            {"setting2": "value2"}
        ]
        expected_settings = {
            "setting1": {"nested_setting1": ["nested", "value1"]},
            "setting2": "value2"
        }

        actual_settings = Environment(
            name="env1",
            description="description1",
            aliases=["alias1"],
            settings=input_settings
        ).settings

        assert expected_settings == actual_settings

    def test_get_setting(self):
        input_settings = {"setting1": "value1", "setting2": "value2"}

        result = Environment(settings=input_settings).get_setting("setting1")

        assert result == "value1"

    def test_alias_cant_convert_to_string(self):
        class NoStr:
            def __str__(self):
                raise TypeError

        input_aliases = ["alias1", NoStr(), "alias2"]
        expected_aliases = ["alias1", "alias2"]

        actual_aliases = Environment(aliases=input_aliases).aliases

        assert actual_aliases == expected_aliases

    def test_get_nested_setting(self):
        input_settings = {
            "setting1": {"nested_setting1": ["nested", "value1"]},
            "setting2": "value2"
        }

        result = Environment(settings=input_settings).get_setting("setting1")

        assert result == {"nested_setting1": ["nested", "value1"]}

    def test_get_setting_upper_case(self):
        input_settings = {"setting1": "value1", "setting2": "value2"}

        result = Environment(settings=input_settings).get_setting("SeTTing1")

        assert result == "value1"

    def test_get_setting_lower_case(self):
        input_settings = {"SeTTing1": "value1", "setting2": "value2"}

        result = Environment(settings=input_settings).get_setting("setting1")

        assert result == "value1"

    def test_get_setting_non_sanitized_name(self):
        input_settings = {"set.ti ng-1": "value1", "setting2": "value2"}

        environment = Environment(settings=input_settings)
        result = environment.get_setting("set_ti_ng_1")

        assert result == "value1"

    def test_has_name_or_alias(self):
        environment = Environment(name="env1", aliases=["alias1"])

        result1 = environment.has_name("env1")
        result2 = environment.has_name("alias1")
        result3 = environment.has_name("env2")

        assert result1 is True
        assert result2 is True
        assert result3 is False

    def test_sanitize_setting_names(self):
        input_settings = {
            "Setting 1": "value1",
            "Setting-2": "value2",
            "Setting.3": "value3"
        }
        expected_output = {
            "setting_1": "value1",
            "setting_2": "value2",
            "setting_3": "value3"
        }

        actual_output = Environment(settings=input_settings).settings

        assert actual_output == expected_output

    def test_empty_aliases(self):
        input_aliases = ["alias1", "", "alias2", None, "alias3"]
        expected_output = ["alias1", "alias2", "alias3"]

        actual_output = Environment(aliases=input_aliases).aliases

        assert expected_output == actual_output

    def test_none_aliases(self):
        input_aliases = None
        expected_output = []

        actual_output = Environment(aliases=input_aliases).aliases

        assert expected_output == actual_output

    def test_no_aliases(self):
        expected_output = []

        actual_output = Environment().aliases

        assert expected_output == actual_output

    def test_empty_list_aliases(self):
        input_aliases = []
        expected_output = []

        actual_output = Environment(aliases=input_aliases).aliases

        assert expected_output == actual_output

    def test_aliases_can_be_converted_to_string(self):
        input_aliases = [1, 2, 3]
        expected_output = ["1", "2", "3"]

        actual_output = Environment(aliases=input_aliases).aliases

        assert expected_output == actual_output

    def test_multiple_key_value_pairs_in_settings(self):
        input_settings = [
            {"setting1": "value1", "setting2": "value2"},
            {"setting3": "value3"}
        ]

        with pytest.raises(ValueError):
            Environment(settings=input_settings)

    def test_none_values_for_name_and_description(self):
        environment = Environment(name=None, description=None)

        assert environment.name is None
        assert environment.description is None

    def test_empty_list_of_aliases(self):
        environment = Environment(aliases=[])

        assert environment.aliases == []

    def test_empty_dictionary_of_settings(self):
        environment = Environment(settings={})

        assert environment.settings == {}

    def test_empty_list_of_settings(self):
        environment = Environment(settings=[])

        assert environment.settings == {}

    def test_get_setting_setting_not_found_error(self):
        settings = {"setting1": "value1", "setting2": "value2"}
        environment = Environment(settings=settings)

        with pytest.raises(SettingNotFoundError):
            environment.get_setting("setting3")

    def test_empty_settings(self):
        environment = Environment(settings=None)

        assert environment.settings == {}

    def test_no_settings(self):
        environment = Environment()

        assert environment.settings == {}
