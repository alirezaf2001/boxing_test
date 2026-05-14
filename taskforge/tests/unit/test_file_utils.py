"""Unit tests for file utilities."""

import tempfile
from pathlib import Path

from taskforge.utils.file_utils import (
    ensure_directory,
    get_file_size,
    get_file_extension,
    is_file_readable,
    find_files_by_extension,
)


def test_ensure_directory():
    """Test ensuring directory exists."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir) / "test" / "nested" / "dir"
        ensure_directory(test_dir)
        assert test_dir.exists()
        assert test_dir.is_dir()


def test_get_file_size():
    """Test getting file size."""
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(b"Hello, World!")
        temp_file.flush()
        size = get_file_size(Path(temp_file.name))
        assert size == 13


def test_get_file_extension():
    """Test getting file extension."""
    assert get_file_extension(Path("test.txt")) == "txt"
    assert get_file_extension(Path("test.TXT")) == "TXT"
    assert get_file_extension(Path("test")) == ""
    assert get_file_extension(Path("test.tar.gz")) == "gz"


def test_is_file_readable():
    """Test checking if file is readable."""
    with tempfile.NamedTemporaryFile() as temp_file:
        assert is_file_readable(Path(temp_file.name))

    # Test non-existent file
    assert not is_file_readable(Path("/non/existent/file"))


def test_find_files_by_extension():
    """Test finding files by extension."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test files
        (temp_path / "file1.txt").write_text("content")
        (temp_path / "file2.txt").write_text("content")
        (temp_path / "file3.py").write_text("content")
        (temp_path / "subdir").mkdir()
        (temp_path / "subdir" / "file4.txt").write_text("content")

        txt_files = find_files_by_extension(temp_path, "txt")
        assert len(txt_files) == 3

        py_files = find_files_by_extension(temp_path, "py")
        assert len(py_files) == 1