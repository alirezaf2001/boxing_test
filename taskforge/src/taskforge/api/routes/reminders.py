"""Reminder API routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from taskforge.api.dependencies import get_db
from taskforge.schemas.reminder_schema import ReminderCreate, ReminderResponse
from taskforge.services.reminder_service import ReminderService

router = APIRouter()


@router.post("/", response_model=ReminderResponse)
def create_reminder(reminder: ReminderCreate, db: Session = Depends(get_db)):
    """Create a new reminder."""
    try:
        reminder_service = ReminderService(db)
        return reminder_service.create_reminder(**reminder.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ReminderResponse])
def get_reminders(
    status: str = "pending",
    db: Session = Depends(get_db)
):
    """Get reminders."""
    try:
        reminder_service = ReminderService(db)
        return reminder_service.get_reminders(status=status)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """Get a reminder by ID."""
    try:
        reminder_service = ReminderService(db)
        reminder = reminder_service.get_reminder(reminder_id=reminder_id)
        if not reminder:
            raise HTTPException(status_code=404, detail="Reminder not found")
        return reminder
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{reminder_id}/dismiss", response_model=ReminderResponse)
def dismiss_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """Dismiss a reminder."""
    try:
        reminder_service = ReminderService(db)
        return reminder_service.dismiss_reminder(reminder_id=reminder_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """Delete a reminder."""
    try:
        reminder_service = ReminderService(db)
        reminder_service.delete_reminder(reminder_id=reminder_id)
        return {"message": "Reminder deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/upcoming/all", response_model=List[ReminderResponse])
def get_upcoming_reminders(db: Session = Depends(get_db)):
    """Get upcoming reminders."""
    try:
        reminder_service = ReminderService(db)
        return reminder_service.get_upcoming_reminders()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))