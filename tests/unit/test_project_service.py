"""Unit tests for project service."""

import pytest

from taskforge.exceptions import NotFoundError, ValidationError


def test_create_project(project_service):
    """Test creating a project."""
    project = project_service.create_project(name="Test Project", description="A test project")
    assert project.name == "Test Project"
    assert project.description == "A test project"
    assert not project.archived


def test_create_project_empty_name(project_service):
    """Test creating a project with empty name."""
    with pytest.raises(ValidationError):
        project_service.create_project(name="")


def test_create_project_duplicate_name(project_service):
    """Test creating a project with duplicate name."""
    project_service.create_project(name="Test Project")
    with pytest.raises(ValidationError):
        project_service.create_project(name="Test Project")


def test_get_project(project_service):
    """Test getting a project by ID."""
    project = project_service.create_project(name="Test Project")
    retrieved = project_service.get_project(project.id)
    assert retrieved.name == "Test Project"


def test_get_project_not_found(project_service):
    """Test getting a non-existent project."""
    retrieved = project_service.get_project(999)
    assert retrieved is None


def test_get_projects(project_service):
    """Test getting all projects."""
    project_service.create_project(name="Project 1")
    project_service.create_project(name="Project 2")
    projects = project_service.get_projects()
    assert len(projects) == 2


def test_get_projects_active_only(project_service):
    """Test getting only active projects."""
    project_service.create_project(name="Active Project")
    archived = project_service.create_project(name="Archived Project")
    project_service.archive_project(archived.id)

    active_projects = project_service.get_projects(status="active")
    assert len(active_projects) == 1
    assert active_projects[0].name == "Active Project"


def test_update_project(project_service):
    """Test updating a project."""
    project = project_service.create_project(name="Old Name", description="Old desc")
    updated = project_service.update_project(
        project.id, name="New Name", description="New desc"
    )
    assert updated.name == "New Name"
    assert updated.description == "New desc"


def test_update_project_not_found(project_service):
    """Test updating a non-existent project."""
    with pytest.raises(NotFoundError):
        project_service.update_project(999, name="New Name")


def test_archive_project(project_service):
    """Test archiving a project."""
    project = project_service.create_project(name="Test Project")
    archived = project_service.archive_project(project.id)
    assert archived.archived


def test_unarchive_project(project_service):
    """Test unarchiving a project."""
    project = project_service.create_project(name="Test Project")
    project_service.archive_project(project.id)
    unarchived = project_service.unarchive_project(project.id)
    assert not unarchived.archived


def test_delete_project(project_service):
    """Test deleting a project."""
    project = project_service.create_project(name="Test Project")
    project_service.delete_project(project.id)
    retrieved = project_service.get_project(project.id)
    assert retrieved is None