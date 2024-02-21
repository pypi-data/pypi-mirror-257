import ast

import pytest

from cringelord.app.src_directory.ast_visitor.environ_get_call import (
    is_environ_get_call,
    get_value
)
from cringelord.app.src_directory.exceptions import NamedCallDetected


STRING_VALUE1 = "string_value1"
STRING_VALUE2 = "string_value2"

STRING_ARGUMENT1 = ast.Constant(value=STRING_VALUE1)
STRING_ARGUMENT2 = ast.Constant(value=STRING_VALUE2)
VARIABLE_ARGUMENT = ast.Name(id="variable")

ENVIRON_GET_CALL_PARAMS = {
    "func": ast.Attribute(
        value=ast.Name(id="environ"),
        attr="get"
    ),
    "args": [],
    "keywords": []
}
OS_ENVIRON_GET_CALL_PARAMS = {
    "func": ast.Attribute(
        value=ast.Attribute(
            value=ast.Name(id="os"),
            attr="environ"
        ),
        attr="get"
    ),
    "args": [],
    "keywords": []
}


class TestEnvironGetCall:
    class TestIsEnvironGetCall:
        @pytest.mark.parametrize(
            "call_params",
            [
                ENVIRON_GET_CALL_PARAMS,
                OS_ENVIRON_GET_CALL_PARAMS
            ],
            ids=[
                "environ_get",
                "os_environ_get"
            ]
        )
        def test(self, call_params):
            call = ast.Call(**call_params)

            assert is_environ_get_call(call)

        def test_returns_false_if_not_getenv_call(self):
            call = ast.Call(
                func=ast.Name(id="not_getenv"),
                args=[],
                keywords=[]
            )

            assert not is_environ_get_call(call)

    class TestGetValue:
        @pytest.mark.parametrize(
            "call_params",
            [
                ENVIRON_GET_CALL_PARAMS,
                OS_ENVIRON_GET_CALL_PARAMS
            ],
            ids=[
                "environ_get",
                "os_environ_get"
            ]
        )
        def test_single_arg(self, call_params):
            call = ast.Call(**call_params)
            call.args = [STRING_ARGUMENT1]

            assert get_value(call) == STRING_VALUE1

        @pytest.mark.parametrize(
            "call_params",
            [
                ENVIRON_GET_CALL_PARAMS,
                OS_ENVIRON_GET_CALL_PARAMS
            ],
            ids=[
                "environ_get",
                "os_environ_get"
            ]
        )
        def test_multiple_args(self, call_params):
            call = ast.Call(**call_params)
            call.args = [STRING_ARGUMENT1, STRING_ARGUMENT2]

            assert get_value(call) == STRING_VALUE1

        @pytest.mark.parametrize(
            "call_params",
            [
                ENVIRON_GET_CALL_PARAMS,
                OS_ENVIRON_GET_CALL_PARAMS
            ],
            ids=[
                "environ_get",
                "os_environ_get"
            ]
        )
        def test_single_keyword(self, call_params):
            call = ast.Call(**call_params)
            call.keywords = [
                ast.keyword(
                    arg="key",
                    value=STRING_ARGUMENT1
                )
            ]

            assert get_value(call) == STRING_VALUE1

        @pytest.mark.parametrize(
            "call_params",
            [
                ENVIRON_GET_CALL_PARAMS,
                OS_ENVIRON_GET_CALL_PARAMS
            ],
            ids=[
                "environ_get",
                "os_environ_get"
            ]
        )
        def test_keywords(self, call_params):
            call = ast.Call(**call_params)
            call.keywords = [
                ast.keyword(
                    arg="key",
                    value=STRING_ARGUMENT1
                ),
                ast.keyword(
                    arg="default",
                    value=None
                )
            ]

            assert get_value(call) == STRING_VALUE1

        @pytest.mark.parametrize(
            "call_params",
            [
                ENVIRON_GET_CALL_PARAMS,
                OS_ENVIRON_GET_CALL_PARAMS
            ],
            ids=[
                "environ_get",
                "os_environ_get"
            ]
        )
        def test_args_and_keywords(self, call_params):
            call = ast.Call(**call_params)
            call.args = [STRING_ARGUMENT1]
            call.keywords = [
                ast.keyword(
                    arg="default",
                    value=None
                )
            ]

            assert get_value(call) == STRING_VALUE1

        @pytest.mark.parametrize(
            "call_params",
            [
                ENVIRON_GET_CALL_PARAMS,
                OS_ENVIRON_GET_CALL_PARAMS
            ],
            ids=[
                "environ_get",
                "os_environ_get"
            ]
        )
        def test_raises_exception_if_value_is_variable(self, call_params):
            call = ast.Call(**call_params)
            call.args = [VARIABLE_ARGUMENT]

            with pytest.raises(NamedCallDetected):
                get_value(call)
