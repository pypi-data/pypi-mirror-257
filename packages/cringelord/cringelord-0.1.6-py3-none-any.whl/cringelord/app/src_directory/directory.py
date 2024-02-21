"""
Logic to walk a given directory.
"""

from pathlib import Path
from typing import List

from pydantic import validate_call


PYTHON_FILE_PATTERN = "*.py"
EXCLUDED_PATHS = (
    ".venv",
    "venv"
)


@validate_call(validate_return=True)
def find_all_python_files_in_directory(directory: Path) -> List[Path]:
    """
    Takes a directory path as an input and returns a list with all the
        file paths of Python files (.py) within that directory
        and its subdirectories.

    Example Usage:
        from pathlib import Path

        # Get all Python file paths in the current directory
        file_paths = get_all_python_file_paths()

        # Get all Python file paths in a specific directory
        file_paths = get_all_python_file_paths(Path("path/to/directory"))

        # Iterate over the file paths
        for file_path in file_paths:
            print(file_path)
        Expected Output:
        path/to/file1.py
        path/to/file2.py
        ...

    Args:
        directory: A string or Path object representing the directory path.
            If not provided, the current directory is used as the default.

    Returns:
        A list of file paths of all Python files (.py) within the specified
            directory and its subdirectories.
    """
    if not directory.exists() or not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory.as_posix()}")

    python_file_paths = [
        python_file_path
        for python_file_path in directory.rglob(PYTHON_FILE_PATTERN)
        if not any(excluded_path in python_file_path.as_posix() for excluded_path in
                   EXCLUDED_PATHS)
    ]

    return python_file_paths
