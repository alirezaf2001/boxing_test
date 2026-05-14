"""Note API routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from taskforge.api.dependencies import get_db
from taskforge.schemas.note_schema import NoteCreate, NoteUpdate, NoteResponse
from taskforge.services.note_service import NoteService

router = APIRouter()


@router.post("/", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    """Create a new note."""
    try:
        note_service = NoteService(db)
        return note_service.create_note(**note.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[NoteResponse])
def get_notes(
    project_id: int = None,
    task_id: int = None,
    db: Session = Depends(get_db)
):
    """Get notes."""
    try:
        note_service = NoteService(db)
        return note_service.get_notes(project_id=project_id, task_id=task_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """Get a note by ID."""
    try:
        note_service = NoteService(db)
        note = note_service.get_note(note_id=note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        return note
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db)
):
    """Update a note."""
    try:
        note_service = NoteService(db)
        return note_service.update_note(
            note_id=note_id, **note_update.dict(exclude_unset=True)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Delete a note."""
    try:
        note_service = NoteService(db)
        note_service.delete_note(note_id=note_id)
        return {"message": "Note deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/search/{query}", response_model=List[NoteResponse])
def search_notes(query: str, db: Session = Depends(get_db)):
    """Search notes."""
    try:
        note_service = NoteService(db)
        return note_service.search_notes(query=query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))