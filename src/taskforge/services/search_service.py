"""Search service."""

from typing import List, Dict, Any, Optional

from sqlalchemy.orm import Session

from taskforge.repositories.task_repository import TaskRepository
from taskforge.repositories.note_repository import NoteRepository
from taskforge.repositories.project_repository import ProjectRepository


class SearchService:
    """Service for searching across entities."""

    def __init__(self, db: Optional[Session] = None):
        """Initialize service with database session."""
        from taskforge.database import SessionLocal
        self.db = db or SessionLocal()
        self.task_repository = TaskRepository(self.db)
        self.note_repository = NoteRepository(self.db)
        self.project_repository = ProjectRepository(self.db)

    def search_all(self, query: str) -> Dict[str, List[Any]]:
        """Search across all entities."""
        tasks = self.task_repository.search_tasks(query)
        notes = self.note_repository.search_notes(query)
        projects = self.project_repository.get_projects()

        # Filter projects by name
        matching_projects = [p for p in projects if query.lower() in p.name.lower()]

        return {
            "tasks": tasks,
            "notes": notes,
            "projects": matching_projects,
        }

    def search_tasks_by_tag(self, tag_name: str) -> List[Dict[str, Any]]:
        """Search tasks by tag."""
        from taskforge.repositories.tag_repository import TagRepository
        tag_repo = TagRepository(self.db)
        tag = tag_repo.get_tag_by_name(tag_name)
        if not tag:
            return []
        return tag_repo.get_tasks_by_tag(tag)