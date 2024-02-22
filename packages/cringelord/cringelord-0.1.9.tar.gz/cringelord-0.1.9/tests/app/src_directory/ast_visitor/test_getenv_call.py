import ast

import pytest

from cringelord.app.src_directory.ast_visitor.getenv_call import (
    is_getenv_call,
    get_value
)
from cringelord.app.src_directory.ast_visitor.exceptions import (
    IncorrectASTFormatError
)
from cringelord.app.src_directory.exceptions import NamedCallDetected


GETENV_STRING = "getenv"
TEST_STRING1 = "test_string1"
TEST_STRING2 = "test_string1"
OS_STRING = "os"
OS_NAME = ast.Name(id=OS_STRING)
NOT_OS_STRING = "not_os"
NOT_OS_NAME = ast.Name(id=NOT_OS_STRING)

STRING_ARGUMENT1 = ast.Constant(value=TEST_STRING1)
STRING_ARGUMENT2 = ast.Constant(value=TEST_STRING2)
VARIABLE_ARGUMENT = ast.Name(id="variable")


OS_GETENV_STRING_CALL = ast.Call(
    func=ast.Attribute(value=OS_NAME, attr=GETENV_STRING),
    args=[],
    keywords=[]
)
GETENV_STRING_CALL = ast.Call(
    func=ast.Name(id=GETENV_STRING),
    args=[],
    keywords=[]
)
OS_GETENV_VARIABLE_CALL = ast.Call(
    func=ast.Attribute(value=OS_NAME, attr=GETENV_STRING),
    args=[VARIABLE_ARGUMENT],
    keywords=[]
)
GETENV_VARIABLE_CALL = ast.Call(
    func=ast.Name(id=GETENV_STRING),
    args=[VARIABLE_ARGUMENT],
    keywords=[]
)
GETENV_CALL_BUT_NOT_OS = ast.Call(
    func=ast.Attribute(value=NOT_OS_NAME, attr=GETENV_STRING),
    args=[],
    keywords=[]
)


class TestGetEnvCall:
    @pytest.mark.parametrize(
        "input_",
        [
            "not a call",
            10,
            1.0,
            ast.Subscript()
        ],
        ids=[
            "not a call",
            "int",
            "float",
            "ast.call"
        ]
    )
    @pytest.mark.parametrize(
        "method",
        [
            is_getenv_call,
            get_value
        ],
        ids=[
            "is_environ_subscript",
            "get_value"
        ]
    )
    def test_raises_invalid_ast_if_not_call(self, input_, method):
        with pytest.raises(IncorrectASTFormatError):
            method(input_)

    class TestIsGetEnvCall:
        @pytest.mark.parametrize(
            "valid_input",
            [
                OS_GETENV_STRING_CALL,
                GETENV_STRING_CALL,
                OS_GETENV_VARIABLE_CALL,
                GETENV_VARIABLE_CALL
            ],
            ids=[
                "os_getenv_string_call",
                "getenv_string_call",
                "os_getenv_variable_call",
                "getenv_variable_call"
            ]
        )
        def test(self, valid_input):
            assert is_getenv_call(valid_input)

        def test_false_if_not_os_getenv_call(self):
            """
            When the function is called 'getenv' but it's not called on
                the OS module, it should return false.
            """
            assert not is_getenv_call(GETENV_CALL_BUT_NOT_OS)

    class TestGetValue:
        def test_single_arg(self):
            call = ast.Call(
                func=ast.Attribute(value=OS_NAME, attr=GETENV_STRING),
                args=[STRING_ARGUMENT1],
                keywords=[]
            )

            assert get_value(call) == TEST_STRING1

        def test_args_only(self):
            call = ast.Call(
                func=ast.Attribute(value=OS_NAME, attr=GETENV_STRING),
                args=[STRING_ARGUMENT1, STRING_ARGUMENT2],
                keywords=[]
            )

            assert get_value(call) == TEST_STRING1

        def test_keywords_only(self):
            call = ast.Call(
                func=ast.Attribute(value=OS_NAME, attr=GETENV_STRING),
                args=[],
                keywords=[
                    ast.keyword(
                        arg="key",
                        value=STRING_ARGUMENT1
                    ),
                    ast.keyword(
                        arg="default",
                        value=None
                    )
                ]
            )

            assert get_value(call) == TEST_STRING1

        def test_keywords_and_args(self):
            call = ast.Call(
                func=ast.Attribute(value=OS_NAME, attr=GETENV_STRING),
                args=[STRING_ARGUMENT1],
                keywords=[
                    ast.keyword(
                        arg="default",
                        value=None
                    )
                ]
            )

            assert get_value(call) == TEST_STRING1

        def test_keywords_and_args_key_keyword(self):
            call = ast.Call(
                func=ast.Attribute(value=OS_NAME, attr=GETENV_STRING),
                args=[STRING_ARGUMENT1],
                keywords=[
                    ast.keyword(
                        arg="key",
                        value=STRING_ARGUMENT2
                    )
                ]
            )

            assert get_value(call) == TEST_STRING2

        @pytest.mark.parametrize(
            "call",
            [
                OS_GETENV_VARIABLE_CALL,
                GETENV_VARIABLE_CALL
            ],
            ids=[
                "os_getenv_variable_call",
                "getenv_variable_call"
            ]
        )
        def test_raises_named_call_detected_for_variable_argument(self, call):
            with pytest.raises(NamedCallDetected):
                get_value(call)
