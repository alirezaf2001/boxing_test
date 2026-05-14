"""Tag API routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from taskforge.api.dependencies import get_db
from taskforge.schemas.tag_schema import TagCreate, TagResponse
from taskforge.services.tag_service import TagService

router = APIRouter()


@router.post("/", response_model=TagResponse)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    """Create a new tag."""
    try:
        tag_service = TagService(db)
        return tag_service.create_tag(**tag.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[TagResponse])
def get_tags(db: Session = Depends(get_db)):
    """Get all tags."""
    try:
        tag_service = TagService(db)
        return tag_service.get_tags()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{tag_name}", response_model=TagResponse)
def get_tag(tag_name: str, db: Session = Depends(get_db)):
    """Get a tag by name."""
    try:
        tag_service = TagService(db)
        tag = tag_service.get_tag(tag_name=tag_name)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        return tag
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{tag_name}/tasks/{task_id}")
def add_tag_to_task(tag_name: str, task_id: int, db: Session = Depends(get_db)):
    """Add a tag to a task."""
    try:
        tag_service = TagService(db)
        tag_service.add_tag_to_task(task_id=task_id, tag_name=tag_name)
        return {"message": f"Tag '{tag_name}' added to task {task_id}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{tag_name}/tasks/{task_id}")
def remove_tag_from_task(tag_name: str, task_id: int, db: Session = Depends(get_db)):
    """Remove a tag from a task."""
    try:
        tag_service = TagService(db)
        tag_service.remove_tag_from_task(task_id=task_id, tag_name=tag_name)
        return {"message": f"Tag '{tag_name}' removed from task {task_id}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{tag_name}/tasks", response_model=List[dict])
def get_tasks_by_tag(tag_name: str, db: Session = Depends(get_db)):
    """Get tasks by tag."""
    try:
        tag_service = TagService(db)
        return tag_service.get_tasks_by_tag(tag_name=tag_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{tag_name}")
def delete_tag(tag_name: str, db: Session = Depends(get_db)):
    """Delete a tag."""
    try:
        tag_service = TagService(db)
        tag_service.delete_tag(name=tag_name)
        return {"message": f"Tag '{tag_name}' deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))