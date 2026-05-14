"""Project schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectBase(BaseModel):
    """Base project schema."""
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(ProjectBase):
    """Schema for project response."""
    id: int
    archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True