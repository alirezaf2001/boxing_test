"""Note schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NoteBase(BaseModel):
    """Base note schema."""
    content: str
    project_id: Optional[int] = None
    task_id: Optional[int] = None


class NoteCreate(NoteBase):
    """Schema for creating a note."""
    pass


class NoteUpdate(BaseModel):
    """Schema for updating a note."""
    content: Optional[str] = None


class NoteResponse(NoteBase):
    """Schema for note response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True