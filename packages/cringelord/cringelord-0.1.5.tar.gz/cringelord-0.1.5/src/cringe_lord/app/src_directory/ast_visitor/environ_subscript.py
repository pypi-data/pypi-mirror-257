"""
Logic for parsing subscript nodes.
"""

import ast

from cringe_lord.app.src_directory.exceptions import NamedCallDetected
from .shared import subscript as helper

INDICATOR = "environ"

from .exceptions import IncorrectASTFormatError


def is_environ_subscript(subscript):
    _validate_subscript(subscript)

    return helper.get_value_string(subscript) == INDICATOR


def get_value(subscript):
    _validate_subscript(subscript)

    value = helper.get_slice(subscript)

    if isinstance(value, ast.Constant):
        return value.s

    raise NamedCallDetected


def _validate_subscript(subscript):
    if not isinstance(subscript, ast.Subscript):
        raise IncorrectASTFormatError("Subscript should be ast.Subscript.")
