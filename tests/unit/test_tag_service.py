"""Unit tests for tag service."""

import pytest

from taskforge.exceptions import NotFoundError, ValidationError


def test_create_tag(tag_service):
    """Test creating a tag."""
    tag = tag_service.create_tag(name="urgent")
    assert tag.name == "urgent"


def test_create_tag_empty_name(tag_service):
    """Test creating a tag with empty name."""
    with pytest.raises(ValidationError):
        tag_service.create_tag(name="")


def test_create_tag_duplicate_name(tag_service):
    """Test creating a tag with duplicate name."""
    tag_service.create_tag(name="urgent")
    with pytest.raises(ValidationError):
        tag_service.create_tag(name="urgent")


def test_get_tag(tag_service):
    """Test getting a tag by name."""
    tag_service.create_tag(name="important")
    tag = tag_service.get_tag("important")
    assert tag.name == "important"


def test_get_tag_not_found(tag_service):
    """Test getting a non-existent tag."""
    tag = tag_service.get_tag("nonexistent")
    assert tag is None


def test_get_tags(tag_service):
    """Test getting all tags."""
    tag_service.create_tag(name="tag1")
    tag_service.create_tag(name="tag2")
    tags = tag_service.get_tags()
    assert len(tags) == 2


def test_add_tag_to_task(tag_service, task_service):
    """Test adding a tag to a task."""
    tag = tag_service.create_tag(name="urgent")
    task = task_service.create_task(title="Test Task")

    tag_service.add_tag_to_task(task.id, "urgent")
    tasks = tag_service.get_tasks_by_tag("urgent")
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test Task"


def test_add_tag_to_task_tag_not_found(tag_service, task_service):
    """Test adding non-existent tag to task."""
    task = task_service.create_task(title="Test Task")
    with pytest.raises(NotFoundError):
        tag_service.add_tag_to_task(task.id, "nonexistent")


def test_add_tag_to_task_task_not_found(tag_service):
    """Test adding tag to non-existent task."""
    tag_service.create_tag(name="urgent")
    with pytest.raises(NotFoundError):
        tag_service.add_tag_to_task(999, "urgent")


def test_remove_tag_from_task(tag_service, task_service):
    """Test removing a tag from a task."""
    tag = tag_service.create_tag(name="urgent")
    task = task_service.create_task(title="Test Task")
    tag_service.add_tag_to_task(task.id, "urgent")

    tag_service.remove_tag_from_task(task.id, "urgent")
    tasks = tag_service.get_tasks_by_tag("urgent")
    assert len(tasks) == 0


def test_delete_tag(tag_service):
    """Test deleting a tag."""
    tag_service.create_tag(name="urgent")
    tag_service.delete_tag("urgent")
    tag = tag_service.get_tag("urgent")
    assert tag is None


def test_delete_tag_not_found(tag_service):
    """Test deleting a non-existent tag."""
    with pytest.raises(NotFoundError):
        tag_service.delete_tag("nonexistent")