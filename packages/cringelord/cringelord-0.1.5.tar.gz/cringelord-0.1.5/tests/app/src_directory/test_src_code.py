import pytest

from cringe_lord.app.src_directory.src_code import get_env_call_var_names
from cringe_lord.app.src_directory.exceptions import NamedCallDetected


class TestGetEnvCallVarNames:
    def test_empty_string_input(self):
        src_code = ""

        result = get_env_call_var_names(src_code)

        assert result == set()

    @pytest.mark.parametrize(
        "src_code",
        [
            "value = os.getenv('')",
            "value = os.environ.get('')",
            "value = getenv('')",
            "value = environ.get('')",
        ]
    )
    def test_empty_string_call(self, src_code):
        expected_result = set()

        actual_result = get_env_call_var_names(src_code)

        assert actual_result == expected_result

    @pytest.mark.parametrize(
        "src_code",
        [
            "value = os.getenv()",
            "value = os.environ.get()",
            "value = getenv()",
            "value = environ.get()",
        ]
    )
    def test_no_var_names_for_empty_call(self, src_code):
        expected_result = set()

        actual_result = get_env_call_var_names(src_code)

        assert actual_result == expected_result

    @pytest.mark.parametrize(
        "src_code",
        [
            "value = environ.get(var)",
            "value = os.environ.get(var)",
            "value = environ.get(var, None)",
            "value = os.environ.get(var, None)",
            "value = environ.get(var, default=None)",
            "value = os.environ.get(var, default=None)",
            "value = environ.get(key=var, default=None)",
            "value = os.environ.get(key=var, default=None)",
            "value = getenv(var)",
            "value = os.getenv(var)",
            "value = getenv(var, None)",
            "value = os.getenv(var, None)",
            "value = getenv(var, default=None)",
            "value = os.getenv(var, default=None)",
            "value = getenv(key=var, default=None)",
            "value = os.getenv(key=var, default=None)",
            "value = environ[var]",
            "value = os.environ[var]"
        ]
    )
    def test_raises_named_call_detected_single_line(self, src_code):
        with pytest.raises(NamedCallDetected):
            get_env_call_var_names(src_code)

    @pytest.mark.parametrize(
        "src_code",
        [
            "value = environ.get('variable')",
            "value = environ.get('variable', None)",
            "value = environ.get(key='variable', default=None)",
            "value = environ.get('variable', default=None)",
            "value = os.environ.get('variable')",
            "value = os.environ.get('variable', None)",
            "value = os.environ.get(key='variable', default=None)",
            "value = os.environ.get('variable', default=None)",
            "value = getenv('variable')",
            "value = getenv('variable', None)",
            "value = getenv(key='variable', default=None)",
            "value = getenv('variable', default=None)",
            "value = os.getenv('variable')",
            "value = os.getenv('variable', None)",
            "value = os.getenv(key='variable', default=None)",
            "value = os.getenv('variable', default=None)",
            "value = environ['variable']",
            "value = os.environ['variable']",
            "value = get_cringe_setting('variable')",
            "value = cringe_lord.get_cringe_setting('variable')"
        ]
    )
    def test_get_variable_from_correct_single_line_input(self, src_code):
        expected_output = {"variable"}

        actual_output = get_env_call_var_names(src_code)

        assert actual_output == expected_output

    @pytest.mark.parametrize(
        "src_code",
        [
            "environ.get('variable1')\nos.environ.get('variable2', None)",
            "environ.get(key='variable1', default=None)\n"
            "os.environ.get('variable2', default=None)",
            "getenv('variable1')\nos.getenv('variable2', None)",
            "getenv(key='variable1', default=None)\n"
            "os.getenv('variable2', default=None)",
            "environ['variable1']\nos.environ['variable2']"
        ]
    )
    def test_get_variables_from_correct_multiline_input(self, src_code):
        expected_output = {"variable1", "variable2"}

        actual_output = get_env_call_var_names(src_code)

        assert actual_output == expected_output
