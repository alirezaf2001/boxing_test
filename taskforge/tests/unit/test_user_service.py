"""Unit tests for user service."""

import pytest

from taskforge.exceptions import NotFoundError


def test_create_user(user_service):
    """Test creating a user."""
    user = user_service.create_user(name="John Doe", email="john@example.com")
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.timezone == "UTC"


def test_get_user_no_user(user_service):
    """Test getting user when none exists."""
    user = user_service.get_user()
    assert user is None


def test_get_user_with_user(user_service):
    """Test getting user when one exists."""
    user_service.create_user(name="Jane Doe", email="jane@example.com")
    user = user_service.get_user()
    assert user is not None
    assert user.name == "Jane Doe"


def test_update_user_no_user(user_service):
    """Test updating user when none exists."""
    with pytest.raises(NotFoundError):
        user_service.update_user(name="New Name")


def test_update_user_with_user(user_service):
    """Test updating user when one exists."""
    user_service.create_user(name="John Doe", email="john@example.com")
    updated_user = user_service.update_user(name="Jane Doe", timezone="EST")
    assert updated_user.name == "Jane Doe"
    assert updated_user.timezone == "EST"
    assert updated_user.email == "john@example.com"


def test_delete_user_no_user(user_service):
    """Test deleting user when none exists."""
    with pytest.raises(NotFoundError):
        user_service.delete_user()


def test_delete_user_with_user(user_service):
    """Test deleting user when one exists."""
    user_service.create_user(name="John Doe", email="john@example.com")
    user_service.delete_user()
    user = user_service.get_user()
    assert user is None