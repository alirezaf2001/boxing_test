"""Task API routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from taskforge.api.dependencies import get_db
from taskforge.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from taskforge.services.task_service import TaskService

router = APIRouter()


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    try:
        task_service = TaskService(db)
        return task_service.create_task(**task.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    status: str = "active",
    project_id: int = None,
    priority: str = None,
    db: Session = Depends(get_db)
):
    """Get tasks."""
    try:
        task_service = TaskService(db)
        return task_service.get_tasks(
            status=status, project_id=project_id, priority=priority
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a task by ID."""
    try:
        task_service = TaskService(db)
        task = task_service.get_task(task_id=task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update a task."""
    try:
        task_service = TaskService(db)
        return task_service.update_task(
            task_id=task_id, **task_update.dict(exclude_unset=True)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    """Mark a task as completed."""
    try:
        task_service = TaskService(db)
        return task_service.complete_task(task_id=task_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{task_id}/incomplete", response_model=TaskResponse)
def incomplete_task(task_id: int, db: Session = Depends(get_db)):
    """Mark a task as incomplete."""
    try:
        task_service = TaskService(db)
        return task_service.incomplete_task(task_id=task_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    try:
        task_service = TaskService(db)
        task_service.delete_task(task_id=task_id)
        return {"message": "Task deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/search/{query}", response_model=List[TaskResponse])
def search_tasks(query: str, db: Session = Depends(get_db)):
    """Search tasks."""
    try:
        task_service = TaskService(db)
        return task_service.search_tasks(query=query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))