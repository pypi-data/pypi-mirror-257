import ast

import pytest

from cringelord.app.src_directory.ast_visitor.environ_subscript import (
    get_value,
    is_environ_subscript
)
from cringelord.app.src_directory.exceptions import NamedCallDetected
from cringelord.app.src_directory.ast_visitor.exceptions import (
    IncorrectASTFormatError
)


ENVIRON_STRING = "environ"
TEST_STRING = "test_string"

STRING_SLICE = ast.Constant(value=TEST_STRING)
VARIABLE_SLICE = ast.Name(id="variable")
ENVIRON_VALUE = ast.Name(id=ENVIRON_STRING)
OS_ENVIRON_VALUE = ast.Attribute(value=ast.Name(id="os"), attr=ENVIRON_STRING)

OS_ENVIRON_STRING_SUBSCRIPT = ast.Subscript(
    slice=STRING_SLICE,
    value=OS_ENVIRON_VALUE
)
ENVIRON_STRING_SUBSCRIPT = ast.Subscript(
    slice=STRING_SLICE,
    value=ENVIRON_VALUE
)
OS_ENVIRON_VARIABLE_SUBSCRIPT = ast.Subscript(
    slice=VARIABLE_SLICE,
    value=OS_ENVIRON_VALUE
)
ENVIRON_VARIABLE_SUBSCRIPT = ast.Subscript(
    slice=VARIABLE_SLICE,
    value=ENVIRON_VALUE
)


class TestEnvironSubscript:
    @pytest.mark.parametrize(
        "input_",
        [
            "not a subscript",
            10,
            1.0,
            ast.Call()
        ],
        ids=[
            "not_a_subscript",
            "int",
            "float",
            "ast.call"
        ]
    )
    @pytest.mark.parametrize(
        "method",
        [
            is_environ_subscript,
            get_value
        ],
        ids=[
            "is_environ_subscript",
            "get_value"
        ]
    )
    def test_raises_invalid_ast_if_not_subscript(self, input_, method):
        with pytest.raises(IncorrectASTFormatError):
            method(input_)

    class TestIsEnvironSubscript:
        @pytest.mark.parametrize(
            "subscript",
            [
                OS_ENVIRON_STRING_SUBSCRIPT,
                ENVIRON_STRING_SUBSCRIPT,
                OS_ENVIRON_VARIABLE_SUBSCRIPT,
                ENVIRON_VARIABLE_SUBSCRIPT
            ],
            ids=[
                "os_environ_string",
                "environ_string",
                "os_environ_variable",
                "environ_variable"
            ]
        )
        def test(self, subscript):
            assert is_environ_subscript(subscript)

    class TestGetValue:
        @pytest.mark.parametrize(
            "subscript",
            [
                OS_ENVIRON_STRING_SUBSCRIPT,
                ENVIRON_STRING_SUBSCRIPT
            ],
            ids=[
                "os_environ_string",
                "environ_string",
            ]
        )
        def test(self, subscript):
            assert get_value(subscript) == TEST_STRING

        @pytest.mark.parametrize(
            "subscript",
            [
                OS_ENVIRON_VARIABLE_SUBSCRIPT,
                ENVIRON_VARIABLE_SUBSCRIPT
            ],
            ids=[
                "os_environ_variable",
                "environ_variable"
            ]
        )
        def test_raises_error_for_variable(self, subscript):
            with pytest.raises(NamedCallDetected):
                get_value(subscript)
