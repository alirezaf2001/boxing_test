"""Reminder service."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from taskforge.repositories.reminder_repository import ReminderRepository
from taskforge.repositories.task_repository import TaskRepository
from taskforge.models.reminder import Reminder
from taskforge.exceptions import NotFoundError, ValidationError


class ReminderService:
    """Service for reminder operations."""

    def __init__(self, db: Optional[Session] = None):
        """Initialize service with database session."""
        from taskforge.database import SessionLocal
        self.db = db or SessionLocal()
        self.reminder_repository = ReminderRepository(self.db)
        self.task_repository = TaskRepository(self.db)

    def create_reminder(self, message: str, remind_at: datetime, task_id: int) -> Reminder:
        """Create a new reminder."""
        if not message.strip():
            raise ValidationError("Reminder message cannot be empty")

        task = self.task_repository.get_task(task_id)
        if not task:
            raise NotFoundError(f"Task with ID {task_id} not found")

        if remind_at <= datetime.utcnow():
            raise ValidationError("Reminder time must be in the future")

        return self.reminder_repository.create_reminder(
            message=message, remind_at=remind_at, task_id=task_id
        )

    def get_reminder(self, reminder_id: int) -> Optional[Reminder]:
        """Get a reminder by ID."""
        return self.reminder_repository.get_reminder(reminder_id=reminder_id)

    def get_reminders(self, status: str = "pending") -> List[Reminder]:
        """Get reminders by status."""
        return self.reminder_repository.get_reminders(status=status)

    def get_upcoming_reminders(self) -> List[Reminder]:
        """Get upcoming reminders."""
        return self.reminder_repository.get_upcoming_reminders()

    def dismiss_reminder(self, reminder_id: int) -> Reminder:
        """Dismiss a reminder."""
        reminder = self.get_reminder(reminder_id)
        if not reminder:
            raise NotFoundError(f"Reminder with ID {reminder_id} not found")
        return self.reminder_repository.dismiss_reminder(reminder)

    def delete_reminder(self, reminder_id: int) -> None:
        """Delete a reminder."""
        reminder = self.get_reminder(reminder_id)
        if not reminder:
            raise NotFoundError(f"Reminder with ID {reminder_id} not found")
        self.reminder_repository.delete_reminder(reminder)