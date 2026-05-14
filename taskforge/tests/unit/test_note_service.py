"""Unit tests for note service."""

import pytest

from taskforge.exceptions import NotFoundError, ValidationError


def test_create_note(note_service):
    """Test creating a note."""
    note = note_service.create_note(content="This is a test note")
    assert note.content == "This is a test note"


def test_create_note_empty_content(note_service):
    """Test creating a note with empty content."""
    with pytest.raises(ValidationError):
        note_service.create_note(content="")


def test_create_note_with_project(note_service, project_service):
    """Test creating a note linked to a project."""
    project = project_service.create_project(name="Test Project")
    note = note_service.create_note(
        content="Project note", project_name="Test Project"
    )
    assert note.project_id == project.id


def test_create_note_with_task(note_service, task_service):
    """Test creating a note linked to a task."""
    task = task_service.create_task(title="Test Task")
    note = note_service.create_note(content="Task note", task_id=task.id)
    assert note.task_id == task.id


def test_create_note_project_not_found(note_service):
    """Test creating a note with non-existent project."""
    with pytest.raises(NotFoundError):
        note_service.create_note(content="Note", project_name="Non-existent")


def test_create_note_task_not_found(note_service):
    """Test creating a note with non-existent task."""
    with pytest.raises(NotFoundError):
        note_service.create_note(content="Note", task_id=999)


def test_get_note(note_service):
    """Test getting a note by ID."""
    note = note_service.create_note(content="Test note")
    retrieved = note_service.get_note(note.id)
    assert retrieved.content == "Test note"


def test_get_note_not_found(note_service):
    """Test getting a non-existent note."""
    retrieved = note_service.get_note(999)
    assert retrieved is None


def test_get_notes(note_service):
    """Test getting all notes."""
    note_service.create_note(content="Note 1")
    note_service.create_note(content="Note 2")
    notes = note_service.get_notes()
    assert len(notes) == 2


def test_get_notes_by_project(note_service, project_service):
    """Test getting notes by project."""
    project = project_service.create_project(name="Test Project")
    note_service.create_note(content="Project note", project_name="Test Project")
    note_service.create_note(content="General note")

    notes = note_service.get_notes(project_name="Test Project")
    assert len(notes) == 1
    assert notes[0].project_id == project.id


def test_search_notes(note_service):
    """Test searching notes."""
    note_service.create_note(content="Meeting notes from today")
    note_service.create_note(content="Shopping list")
    results = note_service.search_notes("meeting")
    assert len(results) == 1
    assert "meeting" in results[0].content.lower()


def test_update_note(note_service):
    """Test updating a note."""
    note = note_service.create_note(content="Old content")
    updated = note_service.update_note(note.id, content="New content")
    assert updated.content == "New content"


def test_update_note_not_found(note_service):
    """Test updating a non-existent note."""
    with pytest.raises(NotFoundError):
        note_service.update_note(999, content="New content")


def test_delete_note(note_service):
    """Test deleting a note."""
    note = note_service.create_note(content="Test note")
    note_service.delete_note(note.id)
    retrieved = note_service.get_note(note.id)
    assert retrieved is None