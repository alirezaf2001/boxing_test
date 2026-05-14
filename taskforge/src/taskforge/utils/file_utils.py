"""File utility functions."""

from pathlib import Path
from typing import Optional


def ensure_directory(path: Path) -> None:
    """Ensure directory exists, create if necessary."""
    path.mkdir(parents=True, exist_ok=True)


def get_file_size(file_path: Path) -> int:
    """Get file size in bytes."""
    return file_path.stat().st_size


def get_file_extension(file_path: Path) -> str:
    """Get file extension without the dot."""
    return file_path.suffix.lstrip('.')


def is_file_readable(file_path: Path) -> bool:
    """Check if file is readable."""
    return file_path.exists() and file_path.is_file() and file_path.stat().st_mode & 0o400


def find_files_by_extension(directory: Path, extension: str) -> list[Path]:
    """Find all files with given extension in directory."""
    return list(directory.rglob(f"*.{extension.lstrip('.')}"))