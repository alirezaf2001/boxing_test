"""Reminder schemas."""

from datetime import datetime

from pydantic import BaseModel


class ReminderBase(BaseModel):
    """Base reminder schema."""
    message: str
    remind_at: datetime
    task_id: int


class ReminderCreate(ReminderBase):
    """Schema for creating a reminder."""
    pass


class ReminderResponse(ReminderBase):
    """Schema for reminder response."""
    id: int
    dismissed: bool
    created_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True