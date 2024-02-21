import pydantic

import pytest

from cringelord.app.src_directory.directory import (
    find_all_python_files_in_directory
)


@pytest.fixture(scope="function")
def nested_directory(tmp_path):
    directory = tmp_path / "test_directory"
    directory.mkdir()

    python_file_paths = []

    python_file_path1 = directory / "file1.py"
    python_file_path1.touch()
    python_file_paths.append(python_file_path1)
    python_file_path2 = directory / "file2.py"
    python_file_path2.touch()
    python_file_paths.append(python_file_path2)

    subdirectory1 = directory / "subdirectory"
    subdirectory1.mkdir()

    python_file_path3 = subdirectory1 / "file3.py"
    python_file_path3.touch()
    python_file_paths.append(python_file_path3)

    return directory, python_file_paths


class TestFindAllPythonFilesInDirectory:
    def test_returns_all_python_files(self, nested_directory):
        directory, python_file_paths = nested_directory

        actual_python_files = find_all_python_files_in_directory(directory)

        assert set(actual_python_files) == set(python_file_paths)

    def test_returns_empty_list_if_directory_not_exist(self, tmp_path):
        directory = tmp_path / "test_directory"

        with pytest.raises(NotADirectoryError):
            find_all_python_files_in_directory(directory)

    def test_returns_empty_list_if_no_python_files_found(self, tmp_path):
        directory = tmp_path / "test_directory"
        directory.mkdir()
        (directory / "non_python_file.txt").touch()

        result = find_all_python_files_in_directory(directory)

        assert result == []

    def test_returns_file_paths_sorted_by_depth(self, tmp_path):
        # Create a temporary directory with Python files
        directory = tmp_path / "test_directory"
        directory.mkdir()
        (directory / "file1.py").touch()
        (directory / "subdirectory").mkdir()
        (directory / "subdirectory" / "file2.py").touch()
        (directory / "subdirectory" / "subsubdirectory").mkdir()
        (directory / "subdirectory" / "subsubdirectory" / "file3.py").touch()

        expected = [
            directory / "file1.py",
            directory / "subdirectory" / "file2.py",
            directory / "subdirectory" / "subsubdirectory" / "file3.py"
        ]

        result = find_all_python_files_in_directory(directory)

        assert result == expected

    def test_returns_file_paths_with_py_extension_only(self, tmp_path):
        directory = tmp_path / "test_directory"
        directory.mkdir()
        (directory / "file1.py").touch()
        (directory / "file2.txt").touch()

        expected = [
            directory / "file1.py"
        ]

        result = find_all_python_files_in_directory(directory)

        assert (directory / "file2.txt") not in result
        assert result == expected

    def test_raises_validation_error_when_path_is_none(self):
        with pytest.raises(pydantic.ValidationError):
            find_all_python_files_in_directory(None)

    def test_raises_validation_error_when_no_path_provided(self):
        with pytest.raises(pydantic.ValidationError):
            find_all_python_files_in_directory()

    def test_raises_error_if_directory_path_is_file_path(self, tmp_path):
        file_path = tmp_path / "test_file.txt"
        file_path.touch()

        with pytest.raises(NotADirectoryError):
            find_all_python_files_in_directory(file_path)

    def test_raises_error_if_directory_path_is_symbolic_link_to_file(
            self,
            tmp_path
    ):
        file_path = tmp_path / "test_file.txt"
        file_path.touch()

        link_path = tmp_path / "test_link"
        link_path.symlink_to(file_path)

        with pytest.raises(NotADirectoryError):
            find_all_python_files_in_directory(link_path)

    def test_raises_error_if_path_is_symlink_to_nonexistent_directory(
            self,
            tmp_path
    ):
        link_path = tmp_path / "test_link"
        link_path.symlink_to("nonexistent_directory")

        with pytest.raises(NotADirectoryError):
            find_all_python_files_in_directory(link_path)
