from typing import Any, Dict, List

from pydantic import BaseModel
from pydantic import (
    constr,
    field_validator,
    model_validator,
    validate_call
)

from cringelord.app.cringe_config.exceptions import (
    NoSuchEnvironmentError,
    SettingNotFoundError
)
from cringelord.app.cringe_config.environment import Environment
from cringelord.app.cringe_config.util import list_to_dict


class CringeConfig(BaseModel):
    metadata: Dict[str, Any] | None = {}
    environment_config: Dict[constr(to_lower=True), Environment] | None = {}
    general_config: Dict[str, Any] | None = {}

    def __bool__(self):
        fields = (self.metadata, self.environment_config, self.general_config)

        return any(fields)

    @property
    def environments(self) -> List[Environment]:
        return list(self.environment_config.values())

    @validate_call
    def get_all_settings(self, environment_name: str | None = None):
        environment_settings = self._get_environment_settings(environment_name)

        return self.general_config | environment_settings

    @validate_call
    def _get_environment_settings(self, environment_name: str | None = None):
        if environment := self.get_environment(environment_name):
            return environment.settings

    @validate_call
    def get_setting(
            self,
            setting_name: str,
            environment_name: str | None = None
    ):
        try:
            return self.get_setting_from_env(setting_name, environment_name)
        except SettingNotFoundError:
            return self.get_setting_from_general_config(setting_name)

    def get_setting_from_general_config(self, setting_name):
        try:
            return self.general_config[setting_name]
        except KeyError:
            raise SettingNotFoundError(setting_name)

    @validate_call
    def get_setting_from_env(
            self,
            setting_name: str,
            environment_name: str | None = None
    ):
        environment = self.get_environment(environment_name)

        if environment:
            return environment.get_setting(setting_name)

        raise SettingNotFoundError(setting_name)

    @validate_call
    def get_environment(self, environment_name=None):
        if not environment_name:
            return self._get_first_environment()

        try:
            return self._get_environment_by_key(environment_name)
        except KeyError:
            return self._get_environment_by_other_name(environment_name)

    def _get_first_environment(self):
        if environments := self.environments:
            return environments[0]

    @validate_call
    def _get_environment_by_key(self, environment_name: constr(to_lower=True)):
        return self.environment_config[environment_name]

    @validate_call
    def _get_environment_by_other_name(
            self,
            environment_name: constr(to_lower=True)
    ):
        for environment in self.environments:
            if environment.has_name(environment_name):
                return environment

        raise NoSuchEnvironmentError(environment_name)

    @field_validator("metadata", mode="before")
    def metadata_to_dict(cls, metadata: Dict[str, Any] | List[Dict[str, Any]]):
        if not metadata:
            return {}

        if isinstance(metadata, dict):
            return metadata

        for item in metadata:
            if len(item) != 1:
                raise ValueError("Only single key/value pairs are supported.")

        return list_to_dict(metadata)

    @field_validator("environment_config", mode="before")
    def environment_config_to_dict(
            cls,
            environment_config: Dict[str, Environment]
            | List[Dict[str, Environment]]
    ):
        if not environment_config:
            return {}

        if isinstance(environment_config, dict):
            return environment_config

        for item in environment_config:
            if len(item) != 1:
                raise ValueError("Only single key/value pairs are supported.")

        return list_to_dict(environment_config)

    @field_validator("general_config", mode="before")
    def general_config_to_dict(
            cls,
            general_config: Dict[str, Any] | List[Dict[str, Any]]
    ):
        if not general_config:
            return {}

        if isinstance(general_config, dict):
            return general_config

        for item in general_config:
            if len(item) != 1:
                raise ValueError("Only single key/value pairs are supported.")

        return list_to_dict(general_config)

    @model_validator(mode="after")
    def environments_should_contain_the_same_settings(self):
        if not self.environments:
            return self

        first_environment = self.environments[0]
        first_environment_setting_names = first_environment.setting_names

        settings_are_the_same = all(
            environment.setting_names == first_environment_setting_names
            for environment in self.environments[1:]
        )

        if not settings_are_the_same:
            raise ValueError("The environments contain different settings.")

        return self
