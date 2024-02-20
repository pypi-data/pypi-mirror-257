import pydantic
import pytest

from cringe_lord.app.src_directory.file import find_env_call_var_names
from cringe_lord.app.src_directory.exceptions import NamedCallDetected


SRC_CODE_CONSTANTS = """
import os

environ["VAR1"]
os.environ["VAR2"]
getenv("VAR3")
getenv("VAR4", None)
getenv("VAR5", default=None)
getenv(key="VAR6", default=None)
os.getenv("VAR7")
os.getenv("VAR8", None)
os.getenv("VAR9", default=None)
os.getenv(key="VAR10", default=None)
environ.get("VAR11")
environ.get("VAR12", None)
environ.get("VAR13", default=None)
environ.get(key="VAR14", default=None)
os.environ.get("VAR15")
os.environ.get("VAR16", None)
os.environ.get("VAR17", default=None)
os.environ.get(key="VAR18", default=None)
"""

SRC_CODE_CONSTANTS_STRINGS = """
import os

print("VAR1: " + environ["VAR1"])
print("VAR2: " + os.environ["VAR2"])
print("VAR3: " + getenv("VAR3"))
print("VAR4: " + getenv("VAR4", None))
print("VAR5: " + getenv("VAR5", default=None))
print("VAR6: " + getenv(key="VAR6", default=None))
print("VAR7: " + os.getenv("VAR7"))
print("VAR8: " + os.getenv("VAR8", None))
print("VAR9: " + os.getenv("VAR9", default=None))
print("VAR10: " + os.getenv(key="VAR10", default=None))
print("VAR11: " + environ.get("VAR11"))
print("VAR12: " + environ.get("VAR12", None))
print("VAR13: " + environ.get("VAR13", default=None))
print("VAR14: " + environ.get(key="VAR14", default=None))
print("VAR15: " + os.environ.get("VAR15"))
print("VAR16: " + os.environ.get("VAR16", None))
print("VAR17: " + os.environ.get("VAR17", default=None))
print("VAR18: " + os.environ.get(key="VAR18", default=None))
"""

VALID_CONSTANTS = {
            "VAR1",
            "VAR2",
            "VAR3",
            "VAR4",
            "VAR5",
            "VAR6",
            "VAR7",
            "VAR8",
            "VAR9",
            "VAR10",
            "VAR11",
            "VAR12",
            "VAR13",
            "VAR14",
            "VAR15",
            "VAR16",
            "VAR17",
            "VAR18"
        }

SRC_CODE_VARIABLES = """
import os

var = "my_var"

environ[var]
os.environ[var]
getenv(var)
getenv(var, None)
getenv(var, default=None)
getenv(key=var, default=None)
os.getenv(var)
os.getenv(var, None)
os.getenv(var, default=None)
os.getenv(key=var, default=None)
environ.get(var)
environ.get(var, None)
environ.get(var, default=None)
environ.get(key=var, default=None)
os.environ.get(var)
os.environ.get(var, None)
os.environ.get(var, default=None)
os.environ.get(key=var, default=None)
"""

SRC_CODE_VARIABLES_STRINGS = """
import os

var = "my_var"

print("VAR1: " + environ[var])
print("VAR2: " + os.environ[var])
print("VAR3: " + getenv(var))
print("VAR4: " + getenv(var, None))
print("VAR5: " + getenv(var, default=None))
print("VAR6: " + getenv(var, default=None))
print("VAR7: " + os.getenv(var))
print("VAR8: " + os.getenv(var, None))
print("VAR9: " + os.getenv(var, default=None))
print("VAR10: " + os.getenv(key=var, default=None))
print("VAR11: " + environ.get(var))
print("VAR12: " + environ.get(var, None))
print("VAR13: " + environ.get(var, default=None))
print("VAR14: " + environ.get(key=var, default=None))
print("VAR15: " + os.environ.get(var))
print("VAR16: " + os.environ.get(var, None))
print("VAR17: " + os.environ.get(var, default=None))
print("VAR18: " + os.environ.get(key=var, default=None))
"""

SRC_CODE_ONE_VARIABLE = """
import os

var = "my_var"

environ["VAR1"]
os.environ["VAR2"]
getenv("VAR3")
getenv("VAR4", None)
getenv("VAR5", default=None)
getenv(key="VAR6", default=None)
os.getenv("VAR7")
os.getenv("VAR8", None)
os.getenv("VAR9", default=None)
os.getenv(key="VAR10", default=None)
environ.get("VAR11")
environ.get("VAR12", None)
environ.get("VAR13", default=None)
environ.get(key="VAR14", default=None)
os.environ.get("VAR15")
os.environ.get("VAR16", None)
os.environ.get("VAR17", default=None)
os.environ.get(key=var, default=None)
"""


class TestFindEnvCallVarNames:
    @pytest.mark.parametrize(
        "src_code",
        [
            SRC_CODE_CONSTANTS_STRINGS,
            SRC_CODE_CONSTANTS
        ],
        ids=[
            "src_code_constants_strings",
            "src_code_constants",
        ],
    )
    def test_valid_file_path(self, tmp_path, src_code):
        python_file = tmp_path / "test.py"
        python_file.write_text(src_code)

        result = find_env_call_var_names(python_file)

        assert result == VALID_CONSTANTS

    @pytest.mark.parametrize(
        "src_code",
        [
            SRC_CODE_CONSTANTS_STRINGS,
            SRC_CODE_CONSTANTS
        ],
        ids=[
            "src_code_constants_strings",
            "src_code_constants",
        ],
    )
    def test_valid_file_string(self, tmp_path, src_code):
        python_file = tmp_path / "test.py"
        python_file.write_text(src_code)
        python_file_string = str(python_file)

        result = find_env_call_var_names(python_file_string)

        assert result == VALID_CONSTANTS

    def test_no_calls(self, tmp_path):
        python_file = tmp_path / "test.py"
        python_file.write_text('print("Hello, world!")')

        result = find_env_call_var_names(python_file)

        assert result == set()

    def test_raises_exception_for_nonexistent_file_path(self):
        with pytest.raises(FileNotFoundError):
            find_env_call_var_names("does_not_exist.py")

    def test_raises_exception_invalid_file_path_type(self):
        with pytest.raises(pydantic.ValidationError):
            find_env_call_var_names(123)

    def test_invalid_encoding(self, tmp_path):
        python_file = tmp_path / "test.py"
        python_file.write_bytes(b'\x80')

        with pytest.raises(UnicodeDecodeError):
            find_env_call_var_names(python_file)

    def test_raises_syntax_error_for_invalid_syntax(self, tmp_path):
        python_file = tmp_path / "test.py"
        python_file.write_text('print("Hello, world!"')

        with pytest.raises(SyntaxError):
            find_env_call_var_names(python_file)

    def test_invalid_indentation(self, tmp_path):
        python_file = tmp_path / "test.py"
        python_file.write_text('if True:\nprint("Hello, world!")')

        with pytest.raises(IndentationError):
            find_env_call_var_names(python_file)

    @pytest.mark.parametrize(
        "src_code",
        [
            SRC_CODE_VARIABLES_STRINGS,
            SRC_CODE_VARIABLES,
            SRC_CODE_ONE_VARIABLE
        ],
        ids=[
            "src_code_variables_strings",
            "src_code_variables",
            "src_code_one_variable"
        ],
    )
    def test_raises_named_call_detected(self, tmp_path, src_code):
        python_file = tmp_path / "test.py"
        python_file.write_text(src_code)

        with pytest.raises(NamedCallDetected):
            find_env_call_var_names(python_file)

