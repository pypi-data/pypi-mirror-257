"""
High level logic for parsing a given Python src file.
"""

from pathlib import Path
from typing import Set

from pydantic import validate_call

from .src_code import get_env_call_var_names


@validate_call(validate_return=True)
def find_env_call_var_names(python_file_path: Path) -> Set[str]:
    """
    Finds all calls to environment variables in a given Python file.

    Args:
        python_file_path: The path to the Python file.

    Returns:
        A list of the names of all variables that were called by the Python
            file.
    """
    src_code = python_file_path.read_text()

    return get_env_call_var_names(src_code)
