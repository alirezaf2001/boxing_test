"""Task service."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from taskforge.repositories.task_repository import TaskRepository
from taskforge.repositories.project_repository import ProjectRepository
from taskforge.models.task import Task
from taskforge.exceptions import NotFoundError, ValidationError


class TaskService:
    """Service for task operations."""

    def __init__(self, db: Optional[Session] = None):
        """Initialize service with database session."""
        from taskforge.database import SessionLocal
        self.db = db or SessionLocal()
        self.task_repository = TaskRepository(self.db)
        self.project_repository = ProjectRepository(self.db)

    def create_task(self, title: str, description: Optional[str] = None,
                   priority: str = "medium", due_date: Optional[datetime] = None,
                   project_name: Optional[str] = None) -> Task:
        """Create a new task."""
        if not title.strip():
            raise ValidationError("Task title cannot be empty")

        if priority not in ["low", "medium", "high", "urgent"]:
            raise ValidationError("Invalid priority. Must be low, medium, high, or urgent")

        project_id = None
        if project_name:
            project = self.project_repository.get_project_by_name(project_name)
            if not project:
                raise NotFoundError(f"Project '{project_name}' not found")
            project_id = project.id

        return self.task_repository.create_task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            project_id=project_id
        )

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return self.task_repository.get_task(task_id=task_id)

    def get_tasks(self, status: str = "active", project_name: Optional[str] = None,
                 priority: Optional[str] = None) -> List[Task]:
        """Get tasks with filters."""
        project_id = None
        if project_name:
            project = self.project_repository.get_project_by_name(project_name)
            if project:
                project_id = project.id

        return self.task_repository.get_tasks(
            status=status, project_id=project_id, priority=priority
        )

    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description."""
        return self.task_repository.search_tasks(query=query)

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None, priority: Optional[str] = None,
                   due_date: Optional[datetime] = None, project_name: Optional[str] = None) -> Task:
        """Update task information."""
        task = self.get_task(task_id)
        if not task:
            raise NotFoundError(f"Task with ID {task_id} not found")

        if title is not None and not title.strip():
            raise ValidationError("Task title cannot be empty")

        if priority is not None and priority not in ["low", "medium", "high", "urgent"]:
            raise ValidationError("Invalid priority. Must be low, medium, high, or urgent")

        project_id = None
        if project_name:
            project = self.project_repository.get_project_by_name(project_name)
            if not project:
                raise NotFoundError(f"Project '{project_name}' not found")
            project_id = project.id

        return self.task_repository.update_task(
            task, title=title, description=description, priority=priority,
            due_date=due_date, project_id=project_id
        )

    def complete_task(self, task_id: int) -> Task:
        """Mark a task as completed."""
        task = self.get_task(task_id)
        if not task:
            raise NotFoundError(f"Task with ID {task_id} not found")
        return self.task_repository.complete_task(task)

    def incomplete_task(self, task_id: int) -> Task:
        """Mark a task as incomplete."""
        task = self.get_task(task_id)
        if not task:
            raise NotFoundError(f"Task with ID {task_id} not found")
        return self.task_repository.incomplete_task(task)

    def delete_task(self, task_id: int) -> None:
        """Delete a task."""
        task = self.get_task(task_id)
        if not task:
            raise NotFoundError(f"Task with ID {task_id} not found")
        self.task_repository.delete_task(task)