"""
Logic or interacting with AST subscript objects, irrespective of Cringe Lord's
    application logic.

This module should contain only general functionality related to
    AST Subscripts. It should not contain anything specific to Cringe Lord.
"""

import ast

from cringe_lord.app.src_directory.ast_visitor.exceptions import (
    IncorrectASTFormatError
)


SLICE_ATTRIBUTE_NAME = "slice"
VALUE_ATTRIBUTE_NAME = "value"

EMPTY_ATTR_MSG_TEMPLATE = "Subscript should have a non-empty {} attribute."
MISSING_ATTR_MSG_TEMPLATE = "Subscript should have a {} attribute."


def get_slice(subscript):
    return _get_attribute(subscript, SLICE_ATTRIBUTE_NAME)


def get_value_string(subscript):
    _validate_subscript(subscript)

    value = get_value(subscript)

    if isinstance(value, ast.Attribute):
        return value.attr

    if isinstance(value, ast.Name):
        return value.id


def get_value(subscript):
    _validate_subscript(subscript)

    return _get_attribute(subscript, VALUE_ATTRIBUTE_NAME)


def _get_attribute(subscript, attribute_name):
    _validate_subscript(subscript)

    return getattr(subscript, attribute_name)


def _validate_subscript(subscript):
    if not isinstance(subscript, ast.Subscript):
        raise IncorrectASTFormatError("Subscript should be ast.Subscript.")

    if not hasattr(subscript, SLICE_ATTRIBUTE_NAME):
        raise IncorrectASTFormatError(
            MISSING_ATTR_MSG_TEMPLATE.format(SLICE_ATTRIBUTE_NAME)
        )

    if not hasattr(subscript, VALUE_ATTRIBUTE_NAME):
        raise IncorrectASTFormatError(
            MISSING_ATTR_MSG_TEMPLATE.format(VALUE_ATTRIBUTE_NAME)
        )

    if not subscript.slice:
        raise IncorrectASTFormatError(
            EMPTY_ATTR_MSG_TEMPLATE.format(SLICE_ATTRIBUTE_NAME)
        )

    if not subscript.value:
        raise IncorrectASTFormatError(
            EMPTY_ATTR_MSG_TEMPLATE.format(VALUE_ATTRIBUTE_NAME)
        )
