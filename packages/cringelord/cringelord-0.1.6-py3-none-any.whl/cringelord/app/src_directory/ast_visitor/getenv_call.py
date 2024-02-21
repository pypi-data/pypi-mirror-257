from cringelord.app.src_directory.ast_visitor import environment_call
from cringelord.app.src_directory.ast_visitor.shared.call import (
    get_called_function_name,
    get_called_sub_function_name
)


GETENV = "getenv"
OS = "os"


def is_getenv_call(call):
    if not get_called_function_name(call) == GETENV:
        return False

    if called_sub_function_name := get_called_sub_function_name(call):
        return called_sub_function_name == OS

    return True


def get_value(call):
    return environment_call.get_value(call)
