"""Tag service."""

from typing import List, Optional

from sqlalchemy.orm import Session

from taskforge.repositories.tag_repository import TagRepository
from taskforge.repositories.task_repository import TaskRepository
from taskforge.models.tag import Tag
from taskforge.exceptions import NotFoundError, ValidationError


class TagService:
    """Service for tag operations."""

    def __init__(self, db: Optional[Session] = None):
        """Initialize service with database session."""
        from taskforge.database import SessionLocal
        self.db = db or SessionLocal()
        self.tag_repository = TagRepository(self.db)
        self.task_repository = TaskRepository(self.db)

    def create_tag(self, name: str) -> Tag:
        """Create a new tag."""
        if not name.strip():
            raise ValidationError("Tag name cannot be empty")

        existing = self.tag_repository.get_tag_by_name(name)
        if existing:
            raise ValidationError(f"Tag with name '{name}' already exists")

        return self.tag_repository.create_tag(name=name)

    def get_tag(self, tag_name: str) -> Optional[Tag]:
        """Get a tag by name."""
        return self.tag_repository.get_tag_by_name(tag_name)

    def get_tags(self) -> List[Tag]:
        """Get all tags."""
        return self.tag_repository.get_tags()

    def get_tasks_by_tag(self, tag_name: str) -> List[dict]:
        """Get tasks associated with a tag."""
        tag = self.get_tag(tag_name)
        if not tag:
            raise NotFoundError(f"Tag '{tag_name}' not found")
        return self.tag_repository.get_tasks_by_tag(tag)

    def add_tag_to_task(self, task_id: int, tag_name: str) -> None:
        """Add a tag to a task."""
        tag = self.get_tag(tag_name)
        if not tag:
            raise NotFoundError(f"Tag '{tag_name}' not found")

        task = self.task_repository.get_task(task_id)
        if not task:
            raise NotFoundError(f"Task with ID {task_id} not found")

        self.tag_repository.add_tag_to_task(task_id, tag)

    def remove_tag_from_task(self, task_id: int, tag_name: str) -> None:
        """Remove a tag from a task."""
        tag = self.get_tag(tag_name)
        if not tag:
            raise NotFoundError(f"Tag '{tag_name}' not found")

        task = self.task_repository.get_task(task_id)
        if not task:
            raise NotFoundError(f"Task with ID {task_id} not found")

        self.tag_repository.remove_tag_from_task(task_id, tag)

    def delete_tag(self, name: str) -> None:
        """Delete a tag."""
        tag = self.get_tag(name)
        if not tag:
            raise NotFoundError(f"Tag '{name}' not found")
        self.tag_repository.delete_tag(tag)