import ast

import pytest

from cringe_lord.app.src_directory.ast_visitor.exceptions import (
    IncorrectASTFormatError
)
from cringe_lord.app.src_directory.ast_visitor.shared.subscript import (
    get_slice,
    get_value,
    get_value_string
)


DIRECT_VALUE_STRING = "value_string"
INDIRECT_VALUE_STRING = "indirect_value_string"

CONSTANT_SLICE = ast.Constant(value="constant_slice")
VARIABLE_SLICE = ast.Name(id="variable_slice")
DIRECT_CALL_VALUE = ast.Name(id=DIRECT_VALUE_STRING)
INDIRECT_CALL_VALUE = ast.Attribute(
    value=ast.Name(id=INDIRECT_VALUE_STRING),
    attr=DIRECT_VALUE_STRING
)

INDIRECT_CALL_CONSTANT_SUBSCRIPT = ast.Subscript(
    slice=CONSTANT_SLICE,
    value=INDIRECT_CALL_VALUE
)
DIRECT_CALL_CONSTANT_SUBSCRIPT = ast.Subscript(
    slice=CONSTANT_SLICE,
    value=DIRECT_CALL_VALUE
)
INDIRECT_CALL_VARIABLE_SUBSCRIPT = ast.Subscript(
    slice=VARIABLE_SLICE,
    value=INDIRECT_CALL_VALUE
)
DIRECT_CALL_VARIABLE_SUBSCRIPT = ast.Subscript(
    slice=VARIABLE_SLICE,
    value=DIRECT_CALL_VALUE
)


class TestSubscript:
    @pytest.mark.parametrize(
        "not_subscript",
        [
            ast.Name(id="name"),
            "not_subscript_string",
            10,
            1.0,
            ast.Call()
        ]
    )
    @pytest.mark.parametrize(
        "method",
        [get_slice, get_value, get_value_string]
    )
    def test_raises_error_if_not_subscript(self, not_subscript, method):
        with pytest.raises(IncorrectASTFormatError):
            method(not_subscript)

    @pytest.mark.parametrize(
        "method",
        [get_slice, get_value, get_value_string]
    )
    def test_raises_error_if_no_slice(self, method):
        no_slice_subscript = ast.Subscript(value=DIRECT_CALL_VALUE)

        with pytest.raises(IncorrectASTFormatError):
            method(no_slice_subscript)

    @pytest.mark.parametrize(
        "method",
        [get_slice, get_value, get_value_string]
    )
    def test_raises_error_if_none_slice(self, method):
        none_slice_subscript = ast.Subscript(
            value=DIRECT_CALL_VALUE,
            slice=None
        )

        with pytest.raises(IncorrectASTFormatError):
            method(none_slice_subscript)

    @pytest.mark.parametrize(
        "method",
        [get_slice, get_value, get_value_string]
    )
    def test_raises_error_if_no_value(self, method):
        no_value_subscript = ast.Subscript(slice=CONSTANT_SLICE)

        with pytest.raises(IncorrectASTFormatError):
            method(no_value_subscript)

    @pytest.mark.parametrize(
        "method",
        [get_slice, get_value, get_value_string]
    )
    def test_raises_error_if_none_value(self, method):
        none_value_subscript = ast.Subscript(
            slice=CONSTANT_SLICE,
            value=None
        )

        with pytest.raises(IncorrectASTFormatError):
            method(none_value_subscript)

    class TestGetSlice:
        @pytest.mark.parametrize(
            "subscript",
            [
                INDIRECT_CALL_CONSTANT_SUBSCRIPT,
                DIRECT_CALL_CONSTANT_SUBSCRIPT
            ],
            ids=[
                "indirect_call_constant",
                "direct_call_constant"
            ]
        )
        def test_from_string(self, subscript):
            assert get_slice(subscript) == CONSTANT_SLICE

        @pytest.mark.parametrize(
            "subscript",
            [
                INDIRECT_CALL_VARIABLE_SUBSCRIPT,
                DIRECT_CALL_VARIABLE_SUBSCRIPT
            ],
            ids=[
                "indirect_call_variable",
                "direct_call_variable"
            ]
        )
        def test_from_variable(self, subscript):
            assert get_slice(subscript) == VARIABLE_SLICE

    class TestGetValue:
        @pytest.mark.parametrize(
            "subscript",
            [
                DIRECT_CALL_CONSTANT_SUBSCRIPT,
                DIRECT_CALL_VARIABLE_SUBSCRIPT
            ],
            ids=[
                "direct_constant",
                "direct_variable"
            ]
        )
        def test_direct_call(self, subscript):
            assert get_value(subscript) == DIRECT_CALL_VALUE

        @pytest.mark.parametrize(
            "subscript",
            [
                INDIRECT_CALL_CONSTANT_SUBSCRIPT,
                INDIRECT_CALL_VARIABLE_SUBSCRIPT
            ],
            ids=[
                "indirect_constant",
                "indirect_variable"
            ]
        )
        def test_indirect_call(self, subscript):
            assert get_value(subscript) == INDIRECT_CALL_VALUE

    class TestGetValueString:
        @pytest.mark.parametrize(
            "subscript",
            [
                INDIRECT_CALL_CONSTANT_SUBSCRIPT,
                DIRECT_CALL_CONSTANT_SUBSCRIPT,
                INDIRECT_CALL_VARIABLE_SUBSCRIPT,
                DIRECT_CALL_VARIABLE_SUBSCRIPT
            ],
            ids=[
                "indirect_call_constant",
                "direct_call_constant",
                "indirect_call_variable",
                "direct_call_variable"
            ]
        )
        def test_direct_call(self, subscript):
            assert get_value_string(subscript) == DIRECT_VALUE_STRING
