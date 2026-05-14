"""Reminder repository."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from taskforge.models.reminder import Reminder


class ReminderRepository:
    """Repository for reminder operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create_reminder(self, message: str, remind_at: datetime, task_id: int) -> Reminder:
        """Create a new reminder."""
        reminder = Reminder(message=message, remind_at=remind_at, task_id=task_id)
        self.db.add(reminder)
        self.db.commit()
        self.db.refresh(reminder)
        return reminder

    def get_reminder(self, reminder_id: int) -> Optional[Reminder]:
        """Get a reminder by ID."""
        return self.db.query(Reminder).filter(Reminder.id == reminder_id).first()

    def get_reminders(self, status: str = "pending") -> List[Reminder]:
        """Get reminders by status."""
        query = self.db.query(Reminder)
        if status == "pending":
            query = query.filter(Reminder.dismissed == False)
        elif status == "dismissed":
            query = query.filter(Reminder.dismissed == True)
        return query.all()

    def get_upcoming_reminders(self) -> List[Reminder]:
        """Get upcoming reminders."""
        now = datetime.utcnow()
        return self.db.query(Reminder).filter(
            Reminder.remind_at > now,
            Reminder.dismissed == False
        ).order_by(Reminder.remind_at).all()

    def dismiss_reminder(self, reminder: Reminder) -> Reminder:
        """Dismiss a reminder."""
        reminder.dismissed = True
        self.db.commit()
        self.db.refresh(reminder)
        return reminder

    def delete_reminder(self, reminder: Reminder) -> None:
        """Delete a reminder."""
        self.db.delete(reminder)
        self.db.commit()