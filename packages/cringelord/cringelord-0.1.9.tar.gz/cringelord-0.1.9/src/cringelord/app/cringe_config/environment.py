from typing import Any, Dict, List

from pydantic import BaseModel
from pydantic import constr, field_validator, validate_call

from .exceptions import SettingNotFoundError
from .util import list_to_dict, sanitize_name


class Environment(BaseModel):
    name: constr(to_lower=True) | None = None
    description: str | None = None
    aliases: List[constr(to_lower=True)] | None = []
    settings: Dict[constr(to_lower=True), Any] | None = {}

    @property
    def setting_names(self):
        return list(self.settings.keys())

    @validate_call
    def get_setting(self, setting_name: constr(to_lower=True)) -> Any:
        try:
            return self.settings[setting_name]
        except KeyError:
            raise SettingNotFoundError(setting_name)

    @validate_call
    def has_name(self, name: constr(to_lower=True)) -> bool:
        return self.name == name or name in self.aliases

    @field_validator("settings", mode="before")
    def settings_to_dict(cls, settings: Dict[str, Any] | List[Dict[str, Any]]):
        if not settings:
            return {}

        if isinstance(settings, dict):
            return settings

        for setting in settings:
            if len(setting) != 1:
                raise ValueError("Only single key/value pairs are supported.")

        return list_to_dict(settings)

    @field_validator("aliases", mode="before")
    def validate_aliases(cls, aliases):
        if not aliases:
            return []

        result = []

        for alias in aliases:
            if not alias:
                continue

            try:
                result.append(str(alias))
            except TypeError:
                continue

        return result

    @field_validator("settings", mode="after")
    def sanitize_setting_names(cls, settings):
        result = {}

        for setting_name, setting_values in settings.items():
            sanitized_name = sanitize_name(setting_name)

            result[sanitized_name] = setting_values

        return result
