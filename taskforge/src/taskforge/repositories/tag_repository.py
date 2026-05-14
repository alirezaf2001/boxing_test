"""Tag repository."""

from typing import List, Optional

from sqlalchemy.orm import Session

from taskforge.models.tag import Tag


class TagRepository:
    """Repository for tag operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create_tag(self, name: str) -> Tag:
        """Create a new tag."""
        tag = Tag(name=name)
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def get_tag(self, tag_id: int) -> Optional[Tag]:
        """Get a tag by ID."""
        return self.db.query(Tag).filter(Tag.id == tag_id).first()

    def get_tag_by_name(self, name: str) -> Optional[Tag]:
        """Get a tag by name."""
        return self.db.query(Tag).filter(Tag.name == name).first()

    def get_tags(self) -> List[Tag]:
        """Get all tags."""
        return self.db.query(Tag).all()

    def get_tasks_by_tag(self, tag: Tag) -> List[dict]:
        """Get tasks associated with a tag."""
        tasks = []
        for task in tag.tasks:
            tasks.append({
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "priority": task.priority,
                "due_date": task.due_date,
            })
        return tasks

    def add_tag_to_task(self, task_id: int, tag: Tag) -> None:
        """Add a tag to a task."""
        from taskforge.models.task import Task
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task and tag not in task.tags:
            task.tags.append(tag)
            self.db.commit()

    def remove_tag_from_task(self, task_id: int, tag: Tag) -> None:
        """Remove a tag from a task."""
        from taskforge.models.task import Task
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task and tag in task.tags:
            task.tags.remove(tag)
            self.db.commit()

    def delete_tag(self, tag: Tag) -> None:
        """Delete a tag."""
        self.db.delete(tag)
        self.db.commit()