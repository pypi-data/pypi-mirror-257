from cringe_lord.app.src_directory.ast_visitor import environment_call
from cringe_lord.app.src_directory.ast_visitor.shared.call import (
    get_called_function_name,
    get_called_sub_function_name
)


GET_CRINGE_SETTING = "get_cringe_setting"
CRINGE_LORD = "cringe_lord"


def is_get_cringe_setting_call(call):
    if not get_called_function_name(call) == GET_CRINGE_SETTING:
        return False

    if called_sub_function_name := get_called_sub_function_name(call):
        return called_sub_function_name == CRINGE_LORD

    return True


def get_value(call):
    return environment_call.get_value(call)
