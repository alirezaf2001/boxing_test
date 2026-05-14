"""Note repository."""

from typing import List, Optional

from sqlalchemy.orm import Session

from taskforge.models.note import Note


class NoteRepository:
    """Repository for note operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create_note(self, content: str, project_id: Optional[int] = None,
                   task_id: Optional[int] = None) -> Note:
        """Create a new note."""
        note = Note(content=content, project_id=project_id, task_id=task_id)
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def get_note(self, note_id: int) -> Optional[Note]:
        """Get a note by ID."""
        return self.db.query(Note).filter(Note.id == note_id).first()

    def get_notes(self, project_id: Optional[int] = None,
                 task_id: Optional[int] = None) -> List[Note]:
        """Get notes with filters."""
        query = self.db.query(Note)

        if project_id is not None:
            query = query.filter(Note.project_id == project_id)

        if task_id is not None:
            query = query.filter(Note.task_id == task_id)

        return query.all()

    def search_notes(self, query: str) -> List[Note]:
        """Search notes by content."""
        search_filter = f"%{query}%"
        return self.db.query(Note).filter(Note.content.ilike(search_filter)).all()

    def update_note(self, note: Note, content: Optional[str] = None) -> Note:
        """Update note content."""
        if content is not None:
            note.content = content

        self.db.commit()
        self.db.refresh(note)
        return note

    def delete_note(self, note: Note) -> None:
        """Delete a note."""
        self.db.delete(note)
        self.db.commit()