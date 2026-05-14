"""Unit tests for date utilities."""

from datetime import datetime

from taskforge.utils.date_utils import parse_date, format_date


def test_parse_date_iso():
    """Test parsing ISO date format."""
    dt = parse_date("2024-01-15T10:30:00")
    assert dt is not None
    assert dt.year == 2024
    assert dt.month == 1
    assert dt.day == 15


def test_parse_date_simple():
    """Test parsing simple date format."""
    dt = parse_date("2024-01-15")
    assert dt is not None
    assert dt.year == 2024
    assert dt.month == 1
    assert dt.day == 15


def test_parse_date_invalid():
    """Test parsing invalid date."""
    dt = parse_date("invalid-date")
    assert dt is None


def test_format_date():
    """Test formatting date."""
    dt = datetime(2024, 1, 15, 10, 30, 0)
    formatted = format_date(dt)
    assert formatted == "2024-01-15 10:30:00"


def test_format_date_custom_format():
    """Test formatting date with custom format."""
    dt = datetime(2024, 1, 15)
    formatted = format_date(dt, "%Y-%m-%d")
    assert formatted == "2024-01-15"