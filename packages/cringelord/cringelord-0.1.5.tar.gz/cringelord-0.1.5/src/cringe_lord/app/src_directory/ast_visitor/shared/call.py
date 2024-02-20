"""
Logic or interacting with AST call objects, irrespective of Cringe Lord's
    application logic.

This module should contain only general functionality related to AST Calls. It
    should not contain anything specific to Cringe Lord.
"""

import ast
from typing_extensions import Annotated

from pydantic import validate_call, Field

from cringe_lord.app.src_directory.ast_visitor.exceptions import (
    ArgNotFoundError,
    IncorrectASTFormatError,
    KeywordNotFoundError,
    ValueNotFoundError
)


@validate_call
def get_argument_value(
        call,
        name: str = None,
        position: Annotated[int, Field(strict=True, ge=0)] = 0,
):
    """
    Retrieves the value of an argument from a function call
        in an Abstract Syntax Tree (AST).

    Args:
        call (ast.Call): The (AST) call node.
        name (str): The name of the argument.
        position (Optional, int): The position of the argument.

    Returns:
        The argument's value.
    """
    _validate_call(call)

    if not call.args and not call.keywords:
        return None

    if name:
        return _get_value_from_keywords(call, name)

    if call.args:
        return _get_value_from_args(call, position)

    raise ValueNotFoundError("Couldn't find the value you're looking for.")


def get_called_function_name(call):
    _validate_call(call)

    function = get_called_function(call)

    try:
        return function.attr
    except AttributeError:
        return function.id


def get_called_sub_function_name(call):
    _validate_call(call)

    function = get_called_function(call)

    if sub_function := _get_sub_function(function):
        if hasattr(sub_function, "id"):
            return sub_function.id

        if hasattr(sub_function, "attr"):
            return sub_function.attr

    return None


def _get_sub_function(function):
    if not hasattr(function, "value"):
        return None

    return function.value


def get_called_function(call):
    _validate_call(call)

    return call.func


def _validate_call(call):
    """
    Unfortunately, Pydantic does not support validation of ASTs, so we'll
        have to do it ourselves.
    Args:
        call (ast.Call): The (AST) call node.

    Raises:
        IncorrectASTFormatError: If the AST is not correctly formatted.
    """
    if not isinstance(call, ast.Call):
        raise IncorrectASTFormatError("Call must be an ast.Call.")

    if not hasattr(call, "func"):
        raise IncorrectASTFormatError("Call must have function.")

    if not hasattr(call, "args"):
        raise IncorrectASTFormatError("Call must have args.")

    if not hasattr(call, "keywords"):
        raise IncorrectASTFormatError("Call must have keywords.")

    if not isinstance(call.keywords, list):
        raise IncorrectASTFormatError("Keywords must be a list.")

    if not isinstance(call.args, list):
        raise IncorrectASTFormatError("Args must be a list.")


def _get_value_from_keywords(call, keyword_name):
    for keyword in call.keywords:
        if keyword.arg == keyword_name:
            return keyword.value

    raise KeywordNotFoundError(keyword_name)


def has_keyword(call, keyword_name):
    _validate_call(call)

    if not (keywords := call.keywords):
        return False

    for keyword in keywords:
        if keyword.arg == keyword_name:
            return True

    return False


def _get_value_from_args(call, position):
    try:
        return call.args[position]
    except IndexError:
        raise ArgNotFoundError(position)
