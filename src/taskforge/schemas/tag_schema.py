"""Tag schemas."""

from datetime import datetime
from typing import List

from pydantic import BaseModel


class TagBase(BaseModel):
    """Base tag schema."""
    name: str


class TagCreate(TagBase):
    """Schema for creating a tag."""
    pass


class TagResponse(TagBase):
    """Schema for tag response."""
    id: int
    created_at: datetime
    tasks: List[dict] = []  # Simplified task representation

    class Config:
        """Pydantic config."""
        from_attributes = True