"""Unit tests for reminder service."""

import pytest
from datetime import datetime, timedelta

from taskforge.exceptions import NotFoundError, ValidationError


def test_create_reminder(reminder_service, task_service):
    """Test creating a reminder."""
    task = task_service.create_task(title="Test Task")
    future_time = datetime.utcnow() + timedelta(hours=1)

    reminder = reminder_service.create_reminder(
        message="Don't forget!", remind_at=future_time, task_id=task.id
    )
    assert reminder.message == "Don't forget!"
    assert reminder.task_id == task.id
    assert not reminder.dismissed


def test_create_reminder_empty_message(reminder_service, task_service):
    """Test creating a reminder with empty message."""
    task = task_service.create_task(title="Test Task")
    future_time = datetime.utcnow() + timedelta(hours=1)

    with pytest.raises(ValidationError):
        reminder_service.create_reminder(
            message="", remind_at=future_time, task_id=task.id
        )


def test_create_reminder_past_time(reminder_service, task_service):
    """Test creating a reminder with past time."""
    task = task_service.create_task(title="Test Task")
    past_time = datetime.utcnow() - timedelta(hours=1)

    with pytest.raises(ValidationError):
        reminder_service.create_reminder(
            message="Past reminder", remind_at=past_time, task_id=task.id
        )


def test_create_reminder_task_not_found(reminder_service):
    """Test creating a reminder for non-existent task."""
    future_time = datetime.utcnow() + timedelta(hours=1)

    with pytest.raises(NotFoundError):
        reminder_service.create_reminder(
            message="Test", remind_at=future_time, task_id=999
        )


def test_get_reminder(reminder_service, task_service):
    """Test getting a reminder by ID."""
    task = task_service.create_task(title="Test Task")
    future_time = datetime.utcnow() + timedelta(hours=1)
    reminder = reminder_service.create_reminder(
        message="Test", remind_at=future_time, task_id=task.id
    )

    retrieved = reminder_service.get_reminder(reminder.id)
    assert retrieved.message == "Test"


def test_get_reminder_not_found(reminder_service):
    """Test getting a non-existent reminder."""
    retrieved = reminder_service.get_reminder(999)
    assert retrieved is None


def test_get_reminders(reminder_service, task_service):
    """Test getting all reminders."""
    task = task_service.create_task(title="Test Task")
    future_time = datetime.utcnow() + timedelta(hours=1)

    reminder_service.create_reminder(
        message="Reminder 1", remind_at=future_time, task_id=task.id
    )
    reminder_service.create_reminder(
        message="Reminder 2", remind_at=future_time, task_id=task.id
    )

    reminders = reminder_service.get_reminders()
    assert len(reminders) == 2


def test_get_upcoming_reminders(reminder_service, task_service):
    """Test getting upcoming reminders."""
    task = task_service.create_task(title="Test Task")
    future_time = datetime.utcnow() + timedelta(hours=1)
    past_time = datetime.utcnow() - timedelta(hours=1)

    reminder_service.create_reminder(
        message="Future", remind_at=future_time, task_id=task.id
    )
    reminder_service.create_reminder(
        message="Past", remind_at=past_time, task_id=task.id
    )

    upcoming = reminder_service.get_upcoming_reminders()
    assert len(upcoming) == 1
    assert upcoming[0].message == "Future"


def test_dismiss_reminder(reminder_service, task_service):
    """Test dismissing a reminder."""
    task = task_service.create_task(title="Test Task")
    future_time = datetime.utcnow() + timedelta(hours=1)
    reminder = reminder_service.create_reminder(
        message="Test", remind_at=future_time, task_id=task.id
    )

    dismissed = reminder_service.dismiss_reminder(reminder.id)
    assert dismissed.dismissed


def test_dismiss_reminder_not_found(reminder_service):
    """Test dismissing a non-existent reminder."""
    with pytest.raises(NotFoundError):
        reminder_service.dismiss_reminder(999)


def test_delete_reminder(reminder_service, task_service):
    """Test deleting a reminder."""
    task = task_service.create_task(title="Test Task")
    future_time = datetime.utcnow() + timedelta(hours=1)
    reminder = reminder_service.create_reminder(
        message="Test", remind_at=future_time, task_id=task.id
    )

    reminder_service.delete_reminder(reminder.id)
    retrieved = reminder_service.get_reminder(reminder.id)
    assert retrieved is None