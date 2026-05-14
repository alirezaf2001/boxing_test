"""Reminder model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from taskforge.database import Base


class Reminder(Base):
    """Reminder model."""

    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    remind_at = Column(DateTime, nullable=False)
    dismissed = Column(Boolean, default=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    task = relationship("Task", back_populates="reminders")