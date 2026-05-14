"""User API routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from taskforge.api.dependencies import get_db
from taskforge.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from taskforge.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    try:
        user_service = UserService(db)
        return user_service.create_user(**user.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=UserResponse)
def get_user(db: Session = Depends(get_db)):
    """Get current user."""
    try:
        user_service = UserService(db)
        user = user_service.get_user()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/", response_model=UserResponse)
def update_user(user_update: UserUpdate, db: Session = Depends(get_db)):
    """Update current user."""
    try:
        user_service = UserService(db)
        return user_service.update_user(**user_update.dict(exclude_unset=True))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))