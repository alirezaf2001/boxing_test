"""API tests for task endpoints."""

from fastapi.testclient import TestClient

from taskforge.api.main import app


def test_create_task(client: TestClient):
    """Test creating a task via API."""
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "A test task"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "A test task"
    assert not data["completed"]


def test_get_tasks(client: TestClient):
    """Test getting tasks via API."""
    # Create tasks
    client.post("/tasks/", json={"title": "Task 1"})
    client.post("/tasks/", json={"title": "Task 2"})

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_task(client: TestClient):
    """Test getting a specific task via API."""
    # Create task
    create_response = client.post(
        "/tasks/",
        json={"title": "Test Task"}
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"


def test_update_task(client: TestClient):
    """Test updating a task via API."""
    # Create task
    create_response = client.post(
        "/tasks/",
        json={"title": "Old Title"}
    )
    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "New Title", "priority": "high"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["priority"] == "high"


def test_complete_task(client: TestClient):
    """Test completing a task via API."""
    # Create task
    create_response = client.post(
        "/tasks/",
        json={"title": "Test Task"}
    )
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"]


def test_search_tasks(client: TestClient):
    """Test searching tasks via API."""
    # Create tasks
    client.post("/tasks/", json={"title": "Buy groceries"})
    client.post("/tasks/", json={"title": "Write report"})

    response = client.get("/tasks/search/report")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "report" in data[0]["title"].lower()


def test_delete_task(client: TestClient):
    """Test deleting a task via API."""
    # Create task
    create_response = client.post(
        "/tasks/",
        json={"title": "Test Task"}
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    # Verify deleted
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404