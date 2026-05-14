"""Project API routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from taskforge.api.dependencies import get_db
from taskforge.schemas.project_schema import ProjectCreate, ProjectUpdate, ProjectResponse
from taskforge.services.project_service import ProjectService

router = APIRouter()


@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project."""
    try:
        project_service = ProjectService(db)
        return project_service.create_project(**project.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ProjectResponse])
def get_projects(
    status: str = "all",
    db: Session = Depends(get_db)
):
    """Get projects."""
    try:
        project_service = ProjectService(db)
        return project_service.get_projects(status=status)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a project by ID."""
    try:
        project_service = ProjectService(db)
        project = project_service.get_project(project_id=project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Update a project."""
    try:
        project_service = ProjectService(db)
        return project_service.update_project(
            project_id=project_id, **project_update.dict(exclude_unset=True)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{project_id}/archive", response_model=ProjectResponse)
def archive_project(project_id: int, db: Session = Depends(get_db)):
    """Archive a project."""
    try:
        project_service = ProjectService(db)
        return project_service.archive_project(project_id=project_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{project_id}/unarchive", response_model=ProjectResponse)
def unarchive_project(project_id: int, db: Session = Depends(get_db)):
    """Unarchive a project."""
    try:
        project_service = ProjectService(db)
        return project_service.unarchive_project(project_id=project_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project."""
    try:
        project_service = ProjectService(db)
        project_service.delete_project(project_id=project_id)
        return {"message": "Project deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))