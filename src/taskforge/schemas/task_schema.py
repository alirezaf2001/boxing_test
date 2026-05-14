"""Task schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    """Base task schema."""
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None
    project_id: Optional[int] = None


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    project_id: Optional[int] = None


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True