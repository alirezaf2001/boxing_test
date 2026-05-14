"""Unit tests for search service."""

from taskforge.services.search_service import SearchService


def test_search_all(db_session, task_service, note_service):
    """Test searching across all entities."""
    search_service = SearchService(db_session)

    # Create test data
    task_service.create_task(title="Buy groceries", description="Milk and bread")
    note_service.create_note(content="Meeting notes")

    results = search_service.search_all("meeting")
    assert "tasks" in results
    assert "notes" in results
    assert "projects" in results
    assert len(results["notes"]) == 1


def test_search_tasks_by_tag(db_session, tag_service, task_service):
    """Test searching tasks by tag."""
    search_service = SearchService(db_session)

    # Create test data
    tag = tag_service.create_tag(name="urgent")
    task = task_service.create_task(title="Urgent task")
    tag_service.add_tag_to_task(task.id, "urgent")

    results = search_service.search_tasks_by_tag("urgent")
    assert len(results) == 1
    assert results[0]["title"] == "Urgent task"