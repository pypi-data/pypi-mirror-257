import pytest

from cringelord.app.cringe_config.environment import Environment
from cringelord.app.cringe_config.cringe_config import CringeConfig
from cringelord.app.cringe_config.exceptions import (
    SettingNotFoundError,
    NoSuchEnvironmentError
)


METADATA_KEY1 = "metadata_key1"
METADATA_VALUE1 = "metadata_value1"
METADATA_KEY2 = "metadata_key2"
METADATA_VALUE2 = "metadata_value2"
METADATA = {METADATA_KEY1: METADATA_VALUE1, METADATA_KEY2: METADATA_VALUE2}
ENVIRONMENT1_KEY = "env1"
ENVIRONMENT1_NAME = "environment1"
ENVIRONMENT1_DESCRIPTION = "Description for environment1"
ENVIRONMENT1_SETTING1_KEY = "setting1"
ENVIRONMENT1_SETTING1_VALUE = "env1_value1"
ENVIRONMENT1_SETTING2_KEY = "setting2"
ENVIRONMENT1_SETTING2_VALUE = "env1_value2"
ENVIRONMENT1_SETTINGS = {
    ENVIRONMENT1_SETTING1_KEY: ENVIRONMENT1_SETTING1_VALUE,
    ENVIRONMENT1_SETTING2_KEY: ENVIRONMENT1_SETTING2_VALUE
}
ENVIRONMENT1_ALIASES = ["environment1_alias1", "environment1_alias2", 10]
ENVIRONMENT1 = Environment(
    name=ENVIRONMENT1_NAME,
    description=ENVIRONMENT1_DESCRIPTION,
    aliases=ENVIRONMENT1_ALIASES,
    settings=ENVIRONMENT1_SETTINGS
)
ENVIRONMENT2_KEY = "env2"
ENVIRONMENT2_NAME = "environment2"
ENVIRONMENT2_DESCRIPTION = "Description for environment2"
ENVIRONMENT2_SETTING1_KEY = "setting1"
ENVIRONMENT2_SETTING1_VALUE = "env2_value1"
ENVIRONMENT2_SETTING2_KEY = "setting2"
ENVIRONMENT2_SETTING2_VALUE = "env2_value2"
ENVIRONMENT2_SETTINGS = {
    ENVIRONMENT2_SETTING1_KEY: ENVIRONMENT2_SETTING1_VALUE,
    ENVIRONMENT2_SETTING2_KEY: ENVIRONMENT2_SETTING2_VALUE
}
ENVIRONMENT2_ALIASES = ["environment2_alias1", "environment2_alias2", 20]
ENVIRONMENT2 = Environment(
    name=ENVIRONMENT2_NAME,
    description=ENVIRONMENT2_DESCRIPTION,
    aliases=ENVIRONMENT2_ALIASES,
    settings=ENVIRONMENT2_SETTINGS
)
ENVIRONMENT_CONFIG = {
    ENVIRONMENT1_KEY: ENVIRONMENT1,
    ENVIRONMENT2_KEY: ENVIRONMENT2
}
GENERAL_CONFIG_KEY1 = "general_config_key1"
GENERAL_CONFIG_VALUE1 = "general_config_value1"
GENERAL_CONFIG_KEY2 = "general_config_key2"
GENERAL_CONFIG_VALUE2 = "general_config_value2"
GENERAL_CONFIG = {
    GENERAL_CONFIG_KEY1: GENERAL_CONFIG_VALUE1,
    GENERAL_CONFIG_KEY2: GENERAL_CONFIG_VALUE2
}
CRINGE_CONFIG = CringeConfig(
    metadata=METADATA,
    environment_config=ENVIRONMENT_CONFIG,
    general_config=GENERAL_CONFIG
)


class TestCringeConfig:
    def test_create_with_dicts(self):
        metadata = {"key": "value"}
        environment_config = {"env1": Environment(name="env1")}
        general_config = {"key": "value"}

        config = CringeConfig(
            metadata=metadata,
            environment_config=environment_config,
            general_config=general_config
        )

        assert config.metadata == metadata
        assert config.environment_config == environment_config
        assert config.general_config == general_config

    def test_raises_value_error_multi_dict_metadata(self):
        metadata = [{"key1": "value"}, {"key2": "value2", "key3": "value3"}]

        environment_config = {"env1": Environment(name="env1")}
        general_config = {"key": "value"}

        with pytest.raises(ValueError):
            CringeConfig(
                metadata=metadata,
                environment_config=environment_config,
                general_config=general_config
            )

    def test_raises_value_error_multi_dict_environment_config(self):
        metadata = {"key": "value"}
        environment_config = [
            {
                "env1": Environment(name="env1"),
                "env2": Environment(name="env2")
            }
        ]
        general_config = {"key": "value"}

        with pytest.raises(ValueError):
            CringeConfig(
                metadata=metadata,
                environment_config=environment_config,
                general_config=general_config
            )

    def test_raises_value_error_multi_dict_general_config(self):
        metadata = {"key": "value"}
        environment_config = [
            {
                "env1": Environment(name="env1"),
                "env2": Environment(name="env2")
            }
        ]
        general_config = [{"key": "value", "key2": "value2"}]

        with pytest.raises(ValueError):
            CringeConfig(
                metadata=metadata,
                environment_config=environment_config,
                general_config=general_config
            )

    def test_create_with_lists(self):
        input_metadata = [
            {"metadata_key1": "metadata_value1"},
            {"metadata_key2": "metadata_value2"}
        ]
        input_environment_config = [
            {"env1": Environment(name="env1")},
            {"env2": Environment(name="env2")}
        ]
        input_general_config = [
            {"general_config_key1": "general_config_value1"},
            {"general_config_key2": "general_config_value2"}
        ]
        expected_metadata = {
            "metadata_key1": "metadata_value1",
            "metadata_key2": "metadata_value2"
        }
        expected_environment_config = {
            "env1": Environment(name="env1"),
            "env2": Environment(name="env2")
        }
        expected_general_config = {
            "general_config_key1": "general_config_value1",
            "general_config_key2": "general_config_value2"
        }

        config = CringeConfig(
            metadata=input_metadata,
            environment_config=input_environment_config,
            general_config=input_general_config
        )

        assert config.metadata == expected_metadata
        assert config.environment_config == expected_environment_config
        assert config.general_config == expected_general_config

    def test_create_without_values(self):
        config = CringeConfig()

        assert config.metadata == {}
        assert config.environment_config == {}
        assert config.general_config == {}

    def test_create_with_none_values(self):
        config = CringeConfig(
            metadata=None,
            environment_config=None,
            general_config=None
        )

        assert config.metadata == {}
        assert config.environment_config == {}
        assert config.general_config == {}

    def test_create_with_empty_lists(self):
        config = CringeConfig(
            metadata=[],
            environment_config=[],
            general_config=[]
        )

        assert config.metadata == {}
        assert config.environment_config == {}
        assert config.general_config == {}

    def test_create_with_empty_dicts(self):
        config = CringeConfig(
            metadata={},
            environment_config={},
            general_config={}
        )

        assert config.metadata == {}
        assert config.environment_config == {}
        assert config.general_config == {}

    def test_get_setting_from_general_config(self):
        setting_name = "key"
        setting_value = "value"
        general_config = {setting_name: setting_value}
        config = CringeConfig(general_config=general_config)

        result = config.get_setting_from_general_config(setting_name)

        assert result == setting_value

    def test_get_complex_setting_from_general_config(self):
        setting_name = "key2"
        setting_value = {
            "key1": "value1",
            "key2": {"other_key": ["other_value1", "other_value2"]}
        }
        general_config = {setting_name: setting_value}
        config = CringeConfig(general_config=general_config)

        result = config.get_setting_from_general_config(setting_name)

        assert result == setting_value

    def test_get_setting_from_general_config_list(self):
        setting_name = "key"
        setting_value = "value"
        general_config = [{setting_name: setting_value}]
        config = CringeConfig(general_config=general_config)

        result = config.get_setting_from_general_config(setting_name)

        assert result == setting_value

    def test_get_complex_setting_from_general_config_list(self):
        setting_name = "key2"
        setting_value = [
            {"key1": "value1"},
            {"key2": {"other_key": ["other_value1", "other_value2"]}}
        ]
        general_config = {setting_name: setting_value}
        config = CringeConfig(general_config=general_config)

        result = config.get_setting_from_general_config(setting_name)

        assert result == setting_value

    def test_get_setting_from_env(self):
        setting_name = "key1"
        setting_value1 = "value1"
        environment_name1 = "env1"
        settings1 = {setting_name: setting_value1}
        environment1 = Environment(name=environment_name1, settings=settings1)
        setting_value2 = "value2"
        environment_name2 = "env2"
        settings2 = {setting_name: setting_value2}
        environment2 = Environment(name=environment_name2, settings=settings2)
        environment_config = {
            environment_name1: environment1,
            environment_name2: environment2
        }
        config = CringeConfig(environment_config=environment_config)

        result1 = config.get_setting_from_env(setting_name, environment_name1)
        result2 = config.get_setting_from_env(setting_name, environment_name2)

        assert result1 == setting_value1
        assert result2 == setting_value2

    def test_raises_error_get_setting_from_env_non_existing(self):
        settings = {
            "setting1": "setting1_value",
            "setting2": "setting2_value"
        }
        environment = Environment(
            name="environment_name",
            settings=settings
        )
        config = CringeConfig(
            environment_config={"environment_key": environment},
            general_config={
                "general_setting1": "general_setting1_value",
                "general_setting2": "general_setting2_value"
            }
        )

        with pytest.raises(SettingNotFoundError):
            config.get_setting_from_env("does_not_exist", "environment_name")

    def test_raises_error_get_setting_from_env_non_existing_env(self):
        config = CringeConfig(
            environment_config=None,
            general_config={
                "general_setting1": "general_setting1_value",
                "general_setting2": "general_setting2_value"
            }
        )

        with pytest.raises(SettingNotFoundError):
            config.get_setting_from_env("does_not_exist")

    def test_get_environment_by_name(self):
        environment_name = "env1"
        environment = Environment(name=environment_name)
        environment_config = {environment_name: environment}
        config = CringeConfig(environment_config=environment_config)

        result = config.get_environment(environment_name)

        assert result == environment

    def test_get_first_environment_without_name(self):
        environment_name = "env1"
        environment = Environment(name="env1")
        environment_config = {environment_name: environment}
        config = CringeConfig(environment_config=environment_config)

        result = config.get_environment()

        assert result == environment

    def test_get_setting_without_environment_name(self):
        setting_name = "setting1"
        setting_value = "value1"
        settings = {setting_name: setting_value}
        environment = Environment(settings=settings)
        environment_config = {"env1": environment}
        config = CringeConfig(environment_config=environment_config)

        result_without_env_name = config.get_setting(setting_name)
        result_with_env_name = config.get_setting(
            setting_name,
            environment_name="env1"
        )

        assert result_with_env_name == result_without_env_name

    def test_get_setting_without_environment_name_multiple_environments(self):
        setting_name = "setting"
        setting_value1 = "value1"
        setting_value2 = "value2"
        settings1 = {setting_name: setting_value1}
        settings2 = {setting_name: setting_value2}
        environment1 = Environment(settings=settings1)
        environment2 = Environment(settings=settings2)
        environment_config = {"env1": environment1, "env2": environment2}
        config = CringeConfig(environment_config=environment_config)

        result_without_env_name = config.get_setting(setting_name)
        result_with_env_name = config.get_setting(
            setting_name,
            environment_name="env2"
        )

        assert result_without_env_name == setting_value1
        assert result_with_env_name == setting_value2

    def test_raise_setting_not_found_error_from_general_config(self):
        setting_name = "key"
        config = CringeConfig()

        with pytest.raises(SettingNotFoundError):
            config.get_setting_from_general_config(setting_name)

    def test_raise_setting_not_found_error_from_environment(self):
        setting_name = "key"
        environment_name = "env1"
        environment = Environment(name=environment_name)
        environment_config = {environment_name: environment}
        config = CringeConfig(environment_config=environment_config)

        with pytest.raises(SettingNotFoundError):
            config.get_setting_from_env(setting_name, environment_name)

    def test_raise_setting_not_found_error(self):
        with pytest.raises(SettingNotFoundError):
            CRINGE_CONFIG.get_setting("Does not exist")

    def test_raise_no_such_environment_error(self):
        with pytest.raises(NoSuchEnvironmentError):
            CRINGE_CONFIG.get_environment("does not exist")

    def test_raise_value_error_for_different_settings_in_environments(self):
        environment1 = Environment(name="env1", settings={"key1": "value1"})
        environment2 = Environment(name="env2", settings={"key2": "value2"})
        environment_config = {"env1": environment1, "env2": environment2}

        with pytest.raises(ValueError):
            CringeConfig(environment_config=environment_config)

    def test_handle_empty_environment_config(self):
        config = CringeConfig()

        result = config.get_environment()

        assert result is None

    def test_get_setting_by_environment_key(self):
        environment_key = "env1"
        setting = "setting"
        expected_value = "value"
        settings = {setting: expected_value}
        environment = Environment(name="environment1", settings=settings)
        environment_config = {environment_key: environment}
        config = CringeConfig(environment_config=environment_config)

        actual_value = config.get_setting(
            setting,
            environment_name=environment_key
        )

        assert actual_value == expected_value

    def test_get_setting_by_environment_name(self):
        environment_name = "environment1"
        setting = "setting"
        expected_value = "value"
        settings = {setting: expected_value}
        environment = Environment(name=environment_name, settings=settings)
        environment_config = {"env1": environment}
        config = CringeConfig(environment_config=environment_config)

        actual_value = config.get_setting(
            setting,
            environment_name=environment_name
        )

        assert actual_value == expected_value

    @pytest.mark.parametrize("alias", ["environ1", "my_environment", 10])
    def test_get_setting_by_environment_alias(self, alias):
        setting = "setting"
        expected_value = "value"
        settings = {setting: expected_value}
        environment = Environment(
            name="environment1",
            settings=settings,
            aliases=[alias]
        )
        environment_config = {"env1": environment}
        config = CringeConfig(environment_config=environment_config)

        actual_value = config.get_setting(
            setting,
            environment_name=str(alias)
        )

        assert actual_value == expected_value

    def test_get_setting_from_first_environment(self):
        actual_value1 = CRINGE_CONFIG.get_setting(
            ENVIRONMENT1_SETTING1_KEY,
            ENVIRONMENT1_KEY
        )
        actual_value2 = CRINGE_CONFIG.get_setting(
            ENVIRONMENT1_SETTING2_KEY,
            ENVIRONMENT1_KEY
        )

        assert actual_value1 == ENVIRONMENT1_SETTING1_VALUE
        assert actual_value2 == ENVIRONMENT1_SETTING2_VALUE

    def test_get_setting_from_second_environment(self):
        actual_value1 = CRINGE_CONFIG.get_setting(
            ENVIRONMENT2_SETTING1_KEY,
            ENVIRONMENT2_KEY
        )
        actual_value2 = CRINGE_CONFIG.get_setting(
            ENVIRONMENT2_SETTING2_KEY,
            ENVIRONMENT2_KEY
        )

        assert actual_value1 == ENVIRONMENT2_SETTING1_VALUE
        assert actual_value2 == ENVIRONMENT2_SETTING2_VALUE

    def test_get_setting_from_general_config_with_environments(self):
        actual_value1 = CRINGE_CONFIG.get_setting(
            GENERAL_CONFIG_KEY1,
            ENVIRONMENT1_KEY
        )
        actual_value2 = CRINGE_CONFIG.get_setting(
            GENERAL_CONFIG_KEY2,
            ENVIRONMENT2_KEY
        )

        assert actual_value1 == GENERAL_CONFIG_VALUE1
        assert actual_value2 == GENERAL_CONFIG_VALUE2

    def test_setting_in_env_gets_priority_over_general_config(self):
        setting_name = "setting_name"
        setting_value_environment = "environment_value"
        setting_value_general_config = "general_config_value"
        environment_name = "env1"
        environment = Environment(
            name=environment_name,
            settings={setting_name: setting_value_environment}
        )
        config = CringeConfig(
            environment_config={environment_name: environment},
            general_config={setting_name: setting_value_general_config}
        )

        actual_value = config.get_setting(setting_name)
        actual_value_env = config.get_setting(setting_name, environment_name)

        assert actual_value == actual_value_env == setting_value_environment

    def test_get_all_settings(self):
        expected_result = {
            "setting1": "setting1_value",
            "setting2": "setting2_value",
            "general_setting1": "general_setting1_value",
            "general_setting2": "general_setting2_value"
        }

        settings = {
            "setting1": "setting1_value",
            "setting2": "setting2_value"
        }
        environment = Environment(
            name="environment_name",
            settings=settings
        )
        config = CringeConfig(
            environment_config={"environment_key": environment},
            general_config={
                "general_setting1": "general_setting1_value",
                "general_setting2": "general_setting2_value"
            }
        )

        actual_result = config.get_all_settings()

        assert expected_result == actual_result
