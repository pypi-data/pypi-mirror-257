from cringelord.app.src_directory.ast_visitor import environment_call
from cringelord.app.src_directory.ast_visitor.shared.call import (
    get_called_function_name,
    get_called_sub_function_name
)


GET = "get"
ENVIRON = "environ"


def is_environ_get_call(call):
    if not get_called_function_name(call) == GET:
        return False

    return get_called_sub_function_name(call) == ENVIRON


def get_value(call):
    return environment_call.get_value(call)
