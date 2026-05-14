"""Unit tests for task service."""

import pytest
from datetime import datetime, timedelta

from taskforge.exceptions import NotFoundError, ValidationError


def test_create_task(task_service):
    """Test creating a task."""
    task = task_service.create_task(title="Test Task", description="A test task")
    assert task.title == "Test Task"
    assert task.description == "A test task"
    assert task.priority == "medium"
    assert not task.completed


def test_create_task_empty_title(task_service):
    """Test creating a task with empty title."""
    with pytest.raises(ValidationError):
        task_service.create_task(title="")


def test_create_task_invalid_priority(task_service):
    """Test creating a task with invalid priority."""
    with pytest.raises(ValidationError):
        task_service.create_task(title="Test", priority="invalid")


def test_create_task_with_project(task_service, project_service):
    """Test creating a task with a project."""
    project = project_service.create_project(name="Test Project")
    task = task_service.create_task(
        title="Test Task", project_name="Test Project"
    )
    assert task.project_id == project.id


def test_create_task_project_not_found(task_service):
    """Test creating a task with non-existent project."""
    with pytest.raises(NotFoundError):
        task_service.create_task(title="Test", project_name="Non-existent")


def test_get_task(task_service):
    """Test getting a task by ID."""
    task = task_service.create_task(title="Test Task")
    retrieved = task_service.get_task(task.id)
    assert retrieved.title == "Test Task"


def test_get_task_not_found(task_service):
    """Test getting a non-existent task."""
    retrieved = task_service.get_task(999)
    assert retrieved is None


def test_get_tasks(task_service):
    """Test getting all tasks."""
    task_service.create_task(title="Task 1")
    task_service.create_task(title="Task 2")
    tasks = task_service.get_tasks()
    assert len(tasks) == 2


def test_get_tasks_active_only(task_service):
    """Test getting only active tasks."""
    task_service.create_task(title="Active Task")
    completed = task_service.create_task(title="Completed Task")
    task_service.complete_task(completed.id)

    active_tasks = task_service.get_tasks(status="active")
    assert len(active_tasks) == 1
    assert active_tasks[0].title == "Active Task"


def test_search_tasks(task_service):
    """Test searching tasks."""
    task_service.create_task(title="Buy groceries", description="Milk and bread")
    task_service.create_task(title="Write report", description="Quarterly report")
    results = task_service.search_tasks("report")
    assert len(results) == 1
    assert "report" in results[0].title.lower()


def test_update_task(task_service):
    """Test updating a task."""
    task = task_service.create_task(title="Old Title", priority="low")
    updated = task_service.update_task(
        task.id, title="New Title", priority="high"
    )
    assert updated.title == "New Title"
    assert updated.priority == "high"


def test_update_task_not_found(task_service):
    """Test updating a non-existent task."""
    with pytest.raises(NotFoundError):
        task_service.update_task(999, title="New Title")


def test_complete_task(task_service):
    """Test completing a task."""
    task = task_service.create_task(title="Test Task")
    completed = task_service.complete_task(task.id)
    assert completed.completed


def test_incomplete_task(task_service):
    """Test marking a task as incomplete."""
    task = task_service.create_task(title="Test Task")
    task_service.complete_task(task.id)
    incomplete = task_service.incomplete_task(task.id)
    assert not incomplete.completed


def test_delete_task(task_service):
    """Test deleting a task."""
    task = task_service.create_task(title="Test Task")
    task_service.delete_task(task.id)
    retrieved = task_service.get_task(task.id)
    assert retrieved is None