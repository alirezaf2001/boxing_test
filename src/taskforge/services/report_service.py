"""Report service."""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from sqlalchemy.orm import Session

from taskforge.repositories.task_repository import TaskRepository
from taskforge.repositories.project_repository import ProjectRepository


class ReportService:
    """Service for generating reports."""

    def __init__(self, db: Optional[Session] = None):
        """Initialize service with database session."""
        from taskforge.database import SessionLocal
        self.db = db or SessionLocal()
        self.task_repository = TaskRepository(self.db)
        self.project_repository = ProjectRepository(self.db)

    def generate_daily_summary(self, date: str = None) -> Dict[str, Any]:
        """Generate daily task summary."""
        if date:
            report_date = datetime.fromisoformat(date)
        else:
            report_date = datetime.utcnow().date()

        start_date = datetime.combine(report_date, datetime.min.time())
        end_date = datetime.combine(report_date, datetime.max.time())

        # Get all tasks created or updated on this date
        all_tasks = self.task_repository.get_tasks()
        total_tasks = len(all_tasks)
        completed_tasks = len([t for t in all_tasks if t.completed])
        pending_tasks = total_tasks - completed_tasks

        # Get overdue tasks
        overdue_tasks = self.task_repository.get_overdue_tasks()
        overdue_count = len(overdue_tasks)

        return {
            "date": report_date.isoformat(),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "overdue_tasks": overdue_count,
        }

    def generate_weekly_summary(self, end_date: str = None) -> Dict[str, Any]:
        """Generate weekly productivity summary."""
        if end_date:
            end = datetime.fromisoformat(end_date)
        else:
            end = datetime.utcnow()

        start = end - timedelta(days=7)

        # Get all tasks
        all_tasks = self.task_repository.get_tasks()
        total_tasks = len(all_tasks)
        completed_tasks = len([t for t in all_tasks if t.completed])

        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        average_per_day = completed_tasks / 7

        return {
            "week_start": start.date().isoformat(),
            "week_end": end.date().isoformat(),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": completion_rate,
            "average_per_day": average_per_day,
        }

    def generate_project_report(self, project_id: int) -> Dict[str, Any]:
        """Generate project progress report."""
        project = self.project_repository.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")

        tasks = self.task_repository.get_tasks(project_id=project_id)
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.completed])
        pending_tasks = total_tasks - completed_tasks
        overdue_tasks = len([t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and not t.completed])

        progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return {
            "project_name": project.name,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "progress_percentage": progress_percentage,
            "overdue_tasks": overdue_tasks,
        }

    def generate_overdue_report(self) -> Dict[str, Any]:
        """Generate overdue tasks report."""
        overdue_tasks = self.task_repository.get_overdue_tasks()

        task_details = []
        for task in overdue_tasks:
            task_details.append({
                "id": task.id,
                "title": task.title,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "priority": task.priority,
                "project": task.project.name if task.project else None,
            })

        return {
            "overdue_tasks": task_details,
        }