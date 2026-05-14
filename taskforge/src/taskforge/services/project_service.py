"""Project service."""

from typing import List, Optional

from sqlalchemy.orm import Session

from taskforge.repositories.project_repository import ProjectRepository
from taskforge.models.project import Project
from taskforge.exceptions import NotFoundError, ValidationError


class ProjectService:
    """Service for project operations."""

    def __init__(self, db: Optional[Session] = None):
        """Initialize service with database session."""
        from taskforge.database import SessionLocal
        self.db = db or SessionLocal()
        self.repository = ProjectRepository(self.db)

    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        """Create a new project."""
        if not name.strip():
            raise ValidationError("Project name cannot be empty")

        existing = self.repository.get_project_by_name(name)
        if existing:
            raise ValidationError(f"Project with name '{name}' already exists")

        return self.repository.create_project(name=name, description=description)

    def get_project(self, project_id: int) -> Optional[Project]:
        """Get a project by ID."""
        return self.repository.get_project(project_id=project_id)

    def get_projects(self, status: str = "all") -> List[Project]:
        """Get projects by status."""
        return self.repository.get_projects(status=status)

    def get_project_by_name(self, name: str) -> Optional[Project]:
        """Get a project by name."""
        return self.repository.get_project_by_name(name=name)

    def update_project(self, project_id: int, name: Optional[str] = None,
                      description: Optional[str] = None) -> Project:
        """Update project information."""
        project = self.get_project(project_id)
        if not project:
            raise NotFoundError(f"Project with ID {project_id} not found")

        if name is not None and not name.strip():
            raise ValidationError("Project name cannot be empty")

        if name is not None:
            existing = self.repository.get_project_by_name(name)
            if existing and existing.id != project_id:
                raise ValidationError(f"Project with name '{name}' already exists")

        return self.repository.update_project(project, name=name, description=description)

    def archive_project(self, project_id: int) -> Project:
        """Archive a project."""
        project = self.get_project(project_id)
        if not project:
            raise NotFoundError(f"Project with ID {project_id} not found")
        return self.repository.archive_project(project)

    def unarchive_project(self, project_id: int) -> Project:
        """Unarchive a project."""
        project = self.get_project(project_id)
        if not project:
            raise NotFoundError(f"Project with ID {project_id} not found")
        return self.repository.unarchive_project(project)

    def delete_project(self, project_id: int) -> None:
        """Delete a project."""
        project = self.get_project(project_id)
        if not project:
            raise NotFoundError(f"Project with ID {project_id} not found")
        self.repository.delete_project(project)