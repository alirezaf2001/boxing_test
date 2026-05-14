"""Task repository."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from taskforge.models.task import Task


class TaskRepository:
    """Repository for task operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create_task(self, title: str, description: Optional[str] = None,
                   priority: str = "medium", due_date: Optional[datetime] = None,
                   project_id: Optional[int] = None) -> Task:
        """Create a new task."""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            project_id=project_id
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_tasks(self, status: str = "active", project_id: Optional[int] = None,
                 priority: Optional[str] = None) -> List[Task]:
        """Get tasks with filters."""
        query = self.db.query(Task)

        if status == "active":
            query = query.filter(Task.completed == False)
        elif status == "completed":
            query = query.filter(Task.completed == True)

        if project_id is not None:
            query = query.filter(Task.project_id == project_id)

        if priority is not None:
            query = query.filter(Task.priority == priority)

        return query.all()

    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description."""
        search_filter = f"%{query}%"
        return self.db.query(Task).filter(
            (Task.title.ilike(search_filter)) |
            (Task.description.ilike(search_filter))
        ).all()

    def update_task(self, task: Task, title: Optional[str] = None,
                   description: Optional[str] = None, priority: Optional[str] = None,
                   due_date: Optional[datetime] = None, project_id: Optional[int] = None) -> Task:
        """Update task information."""
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if due_date is not None:
            task.due_date = due_date
        if project_id is not None:
            task.project_id = project_id

        self.db.commit()
        self.db.refresh(task)
        return task

    def complete_task(self, task: Task) -> Task:
        """Mark a task as completed."""
        task.completed = True
        self.db.commit()
        self.db.refresh(task)
        return task

    def incomplete_task(self, task: Task) -> Task:
        """Mark a task as incomplete."""
        task.completed = False
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task: Task) -> None:
        """Delete a task."""
        self.db.delete(task)
        self.db.commit()

    def get_overdue_tasks(self) -> List[Task]:
        """Get overdue tasks."""
        now = datetime.utcnow()
        return self.db.query(Task).filter(
            Task.due_date < now,
            Task.completed == False
        ).all()