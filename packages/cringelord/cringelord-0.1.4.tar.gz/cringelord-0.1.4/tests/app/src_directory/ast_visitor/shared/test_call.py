import ast

from pydantic import ValidationError
import pytest

from cringe_lord.app.src_directory.ast_visitor.shared.call import (
    get_argument_value,
    has_keyword
)
from cringe_lord.app.src_directory.ast_visitor.exceptions import (
    ArgNotFoundError,
    IncorrectASTFormatError,
    KeywordNotFoundError,
    ValueNotFoundError
)


ARG_AT_POS0 = ast.Constant(value="string_value")
ARG_AT_POS1 = ast.Constant(value=10)
VARIABLE_ARG = ast.Name(id="variable_value")

KEYWORD_NAME1 = "keyword_name1"
KEYWORD_VALUE1 = ast.Constant(value="keyword_value1")
KEYWORD1 = ast.keyword(
    arg=KEYWORD_NAME1,
    value=KEYWORD_VALUE1
)
KEYWORD_NAME2 = "keyword_name2"
KEYWORD_VALUE2 = ast.Constant(value="keyword_value2")
KEYWORD2 = ast.keyword(
    arg=KEYWORD_NAME2,
    value=KEYWORD_VALUE2
)
KEYWORD_WITH_VARIABLE1 = ast.keyword(
    arg="keyword_name1",
    value=ast.Name(id="keyword_value1")
)
KEYWORD_WITH_VARIABLE2 = ast.keyword(
    arg="keyword_name2",
    value=ast.Name(id="keyword_value2")
)

CALL_ARGS_ONLY = ast.Call(
    func=ast.Name(id="function_name"),
    args=[ARG_AT_POS0, ARG_AT_POS1],
    keywords=[]
)
CALL_KEYWORDS_ONLY = ast.Call(
    func=ast.Name(id="function_name"),
    args=[],
    keywords=[KEYWORD1, KEYWORD2]
)

MIXED_CALL = ast.Call(
    func=ast.Name(id="function_name"),
    args=[ARG_AT_POS0, ARG_AT_POS1],
    keywords=[KEYWORD_WITH_VARIABLE1, KEYWORD_WITH_VARIABLE2]
)


class TestCall:
    class TestGetArgumentValue:
        def test_mixed_call(self):
            assert get_argument_value(MIXED_CALL) == ARG_AT_POS0
            assert get_argument_value(MIXED_CALL, position=1) == ARG_AT_POS1

        def test_by_position(self):
            assert get_argument_value(CALL_ARGS_ONLY, position=0) == ARG_AT_POS0
            assert get_argument_value(CALL_ARGS_ONLY, position=1) == ARG_AT_POS1

        def test_no_position_should_return_first_arg(self):
            result_no_position = get_argument_value(CALL_ARGS_ONLY)
            result_default_position = get_argument_value(
                CALL_ARGS_ONLY,
                position=0
            )

            assert result_no_position == result_default_position

        def test_by_name(self):
            result1 = get_argument_value(
                CALL_KEYWORDS_ONLY,
                name=KEYWORD_NAME1
            )
            result2 = get_argument_value(
                CALL_KEYWORDS_ONLY,
                name=KEYWORD_NAME2
            )

            assert result1 == KEYWORD_VALUE1
            assert result2 == KEYWORD_VALUE2

        def test_raises_exception_when_no_name_without_arguments(self):
            with pytest.raises(ValueNotFoundError):
                get_argument_value(CALL_KEYWORDS_ONLY)

        def test_raises_exception_when_call_is_incorrectly_formatted(self):
            empty_call = ast.Call()
            no_args_call = ast.Call(func=ast.Name(id="function_name"), keywords=[])
            no_keywords_call = ast.Call(func=ast.Name(id="function_name"), args=[])

            with pytest.raises(IncorrectASTFormatError):
                get_argument_value(empty_call)

            with pytest.raises(IncorrectASTFormatError):
                get_argument_value(no_args_call, position=10)

            with pytest.raises(IncorrectASTFormatError):
                get_argument_value(no_keywords_call, name="does_not_exist")

        def test_returns_argument_value_at_specified_position_if_exists(self):
            assert get_argument_value(CALL_ARGS_ONLY, position=0) == ARG_AT_POS0
            assert get_argument_value(CALL_ARGS_ONLY, position=1) == ARG_AT_POS1

        def test_raises_exception_if_argument_does_not_exist_at_position(self):
            with pytest.raises(ArgNotFoundError):
                get_argument_value(CALL_ARGS_ONLY, position=99999999)

        def test_raises_exception_if_keyword_doesnt_exist(self):
            with pytest.raises(KeywordNotFoundError):
                get_argument_value(CALL_KEYWORDS_ONLY, name="does_not_exist")

        def test_raises_error_not_a_call(self):
            with pytest.raises(IncorrectASTFormatError):
                get_argument_value(call="this is not a call")

        def test_raises_exception_keywords_not_a_list(self):
            with pytest.raises(IncorrectASTFormatError):
                get_argument_value(ast.Call(keywords="this is not a list"))

        def test_raises_exception_args_not_a_list(self):
            with pytest.raises(IncorrectASTFormatError):
                get_argument_value(ast.Call(args="this is not a list"))

        def test_raises_exception_position_not_int(self):
            with pytest.raises(ValidationError):
                get_argument_value(ast.Call(), position="this is not an int")

        def test_raises_exception_name_not_string(self):
            with pytest.raises(ValidationError):
                get_argument_value(ast.Call(), name=10)

        def test_raises_exception_position_less_than_zero(self):
            with pytest.raises(ValidationError):
                get_argument_value(ast.Call(), position=-1)

        def test_raises_exception_non_list_keywords(self):
            input_call = ast.Call(
                func=ast.Name(id="function_name"),
                keywords="not_list",
                args=[]
            )

            with pytest.raises(IncorrectASTFormatError):
                get_argument_value(input_call, position=0)

        def test_raises_exception_non_list_args(self):
            input_call = ast.Call(
                func=ast.Name(id="function_name"),
                keywords=[],
                args="not_a_list"
            )

            with pytest.raises(IncorrectASTFormatError):
                get_argument_value(input_call, position=0)

        def test_raises_exception_missing_keywords(self):
            input_call = ast.Call(
                func=ast.Name(id="function_name"),
                args=[]
            )

            with pytest.raises(IncorrectASTFormatError):
                get_argument_value(input_call, position=0)

        def test_raises_exception_missing_args(self):
            input_call = ast.Call(
                func=ast.Name(id="function_name"),
                keywords=[]
            )

            with pytest.raises(IncorrectASTFormatError):
                get_argument_value(input_call, position=0)

    class TestHasKeyword:
        def test_returns_true_if_call_has_keyword_with_given_name(self):
            call = ast.Call(
                func=ast.Name(id='function_name'),
                args=[],
                keywords=[ast.keyword(
                    arg='keyword_name',
                    value=ast.Constant(value='value')
                )]
            )

            assert has_keyword(call, 'keyword_name')

        def test_returns_false_if_call_has_no_keyword_with_given_name(self):
            call = ast.Call(
                func=ast.Name(id='function_name'),
                args=[],
                keywords=[ast.keyword(
                    arg='keyword_name',
                    value=ast.Constant(value='value')
                )]
            )

            assert not has_keyword(call, "does not exist")

        def test_returns_false_if_call_has_no_keywords(self):
            call = ast.Call(
                func=ast.Name(id='function_name'),
                args=[],
                keywords=[]
            )

            assert not has_keyword(call, "no keywords to have")

        def test_works_correctly_when_call_has_both_keywords_and_args(self):
            call = ast.Call(
                func=ast.Name(id='function_name'),
                args=[ast.Constant(value='arg_value')],
                keywords=[
                    ast.keyword(
                        arg='keyword_name',
                        value=ast.Constant(value='value')
                    )
                ]
            )

            assert has_keyword(call, 'keyword_name')
