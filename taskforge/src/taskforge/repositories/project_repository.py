"""Project repository."""

from typing import List, Optional

from sqlalchemy.orm import Session

from taskforge.models.project import Project


class ProjectRepository:
    """Repository for project operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        """Create a new project."""
        project = Project(name=name, description=description)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_project(self, project_id: int) -> Optional[Project]:
        """Get a project by ID."""
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_projects(self, status: str = "all") -> List[Project]:
        """Get projects by status."""
        query = self.db.query(Project)
        if status == "active":
            query = query.filter(Project.archived == False)
        elif status == "archived":
            query = query.filter(Project.archived == True)
        return query.all()

    def get_project_by_name(self, name: str) -> Optional[Project]:
        """Get a project by name."""
        return self.db.query(Project).filter(Project.name == name).first()

    def update_project(self, project: Project, name: Optional[str] = None,
                      description: Optional[str] = None) -> Project:
        """Update project information."""
        if name is not None:
            project.name = name
        if description is not None:
            project.description = description

        self.db.commit()
        self.db.refresh(project)
        return project

    def archive_project(self, project: Project) -> Project:
        """Archive a project."""
        project.archived = True
        self.db.commit()
        self.db.refresh(project)
        return project

    def unarchive_project(self, project: Project) -> Project:
        """Unarchive a project."""
        project.archived = False
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete_project(self, project: Project) -> None:
        """Delete a project."""
        self.db.delete(project)
        self.db.commit()