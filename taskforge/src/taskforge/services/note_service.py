"""Note service."""

from typing import List, Optional

from sqlalchemy.orm import Session

from taskforge.repositories.note_repository import NoteRepository
from taskforge.repositories.project_repository import ProjectRepository
from taskforge.repositories.task_repository import TaskRepository
from taskforge.models.note import Note
from taskforge.exceptions import NotFoundError, ValidationError


class NoteService:
    """Service for note operations."""

    def __init__(self, db: Optional[Session] = None):
        """Initialize service with database session."""
        from taskforge.database import SessionLocal
        self.db = db or SessionLocal()
        self.note_repository = NoteRepository(self.db)
        self.project_repository = ProjectRepository(self.db)
        self.task_repository = TaskRepository(self.db)

    def create_note(self, content: str, project_name: Optional[str] = None,
                   task_id: Optional[int] = None) -> Note:
        """Create a new note."""
        if not content.strip():
            raise ValidationError("Note content cannot be empty")

        project_id = None
        if project_name:
            project = self.project_repository.get_project_by_name(project_name)
            if not project:
                raise NotFoundError(f"Project '{project_name}' not found")
            project_id = project.id

        if task_id:
            task = self.task_repository.get_task(task_id)
            if not task:
                raise NotFoundError(f"Task with ID {task_id} not found")

        return self.note_repository.create_note(
            content=content, project_id=project_id, task_id=task_id
        )

    def get_note(self, note_id: int) -> Optional[Note]:
        """Get a note by ID."""
        return self.note_repository.get_note(note_id=note_id)

    def get_notes(self, project_name: Optional[str] = None,
                 task_id: Optional[int] = None) -> List[Note]:
        """Get notes with filters."""
        project_id = None
        if project_name:
            project = self.project_repository.get_project_by_name(project_name)
            if project:
                project_id = project.id

        return self.note_repository.get_notes(project_id=project_id, task_id=task_id)

    def search_notes(self, query: str) -> List[Note]:
        """Search notes by content."""
        return self.note_repository.search_notes(query=query)

    def update_note(self, note_id: int, content: Optional[str] = None) -> Note:
        """Update note content."""
        note = self.get_note(note_id)
        if not note:
            raise NotFoundError(f"Note with ID {note_id} not found")

        if content is not None and not content.strip():
            raise ValidationError("Note content cannot be empty")

        return self.note_repository.update_note(note, content=content)

    def delete_note(self, note_id: int) -> None:
        """Delete a note."""
        note = self.get_note(note_id)
        if not note:
            raise NotFoundError(f"Note with ID {note_id} not found")
        self.note_repository.delete_note(note)