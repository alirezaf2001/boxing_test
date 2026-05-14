"""Unit tests for validation utilities."""

from taskforge.utils.validation_utils import (
    validate_email,
    validate_priority,
    validate_project_name,
    validate_tag_name,
)


def test_validate_email_valid():
    """Test validating valid email."""
    assert validate_email("user@example.com")
    assert validate_email("test.email+tag@domain.co.uk")


def test_validate_email_invalid():
    """Test validating invalid email."""
    assert not validate_email("invalid-email")
    assert not validate_email("user@")
    assert not validate_email("@example.com")


def test_validate_priority_valid():
    """Test validating valid priority."""
    assert validate_priority("low")
    assert validate_priority("medium")
    assert validate_priority("high")
    assert validate_priority("urgent")


def test_validate_priority_invalid():
    """Test validating invalid priority."""
    assert not validate_priority("critical")
    assert not validate_priority("")
    assert not validate_priority("LOW")


def test_validate_project_name_valid():
    """Test validating valid project name."""
    assert validate_project_name("My Project")
    assert validate_project_name("Project-123")
    assert validate_project_name("Project_123")


def test_validate_project_name_invalid():
    """Test validating invalid project name."""
    assert not validate_project_name("")
    assert not validate_project_name("Project<")
    assert not validate_project_name("Project>")
    assert not validate_project_name("Project|")


def test_validate_tag_name_valid():
    """Test validating valid tag name."""
    assert validate_tag_name("urgent")
    assert validate_tag_name("high priority")
    assert validate_tag_name("tag-123")
    assert validate_tag_name("tag_123")


def test_validate_tag_name_invalid():
    """Test validating invalid tag name."""
    assert not validate_tag_name("")
    assert not validate_tag_name("tag@name")
    assert not validate_tag_name("tag#name")