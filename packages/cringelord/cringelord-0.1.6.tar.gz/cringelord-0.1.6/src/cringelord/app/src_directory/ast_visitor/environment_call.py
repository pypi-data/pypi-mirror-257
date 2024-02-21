import ast

from cringelord.app.src_directory.ast_visitor.shared.call import (
    get_argument_value,
    has_keyword
)
from cringelord.app.src_directory.exceptions import NamedCallDetected


def get_value(call):
    if has_keyword(call, "key"):
        value = get_argument_value(call, name="key")
    else:
        value = get_argument_value(call, position=0)

    if not value:
        return None

    if isinstance(value, ast.Constant):
        return value.s

    raise NamedCallDetected
