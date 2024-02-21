import ast

import pytest

from cringelord.app.src_directory.ast_visitor.get_cringe_setting_call import (
    is_get_cringe_setting_call,
    get_value
)
from cringelord.app.src_directory.exceptions import NamedCallDetected


IMPORT_CALL = ast.parse("""
get_cringe_setting("import_call")
""").body[0].value
NON_IMPORT_CALL = ast.parse("""
cringelord.get_cringe_setting("setting_name")
""").body[0].value
NAMED_CALL = ast.parse("""
cringelord.get_cringe_setting(variable_name)
""").body[0].value


class TestGetCringeSettingCall:
    def test_is_get_cringe_setting_call(self):
        assert is_get_cringe_setting_call(IMPORT_CALL)
        assert is_get_cringe_setting_call(NON_IMPORT_CALL)

    def test_get_value(self):
        assert get_value(IMPORT_CALL) == "import_call"
        assert get_value(NON_IMPORT_CALL) == "setting_name"

    def test_named_call_raises_error(self):
        with pytest.raises(NamedCallDetected):
            get_value(NAMED_CALL)
