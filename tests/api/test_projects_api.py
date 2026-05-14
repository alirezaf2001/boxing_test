"""API tests for project endpoints."""

from fastapi.testclient import TestClient

from taskforge.api.main import app


def test_create_project(client: TestClient):
    """Test creating a project via API."""
    response = client.post(
        "/projects/",
        json={"name": "Test Project", "description": "A test project"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "A test project"
    assert not data["archived"]


def test_get_projects(client: TestClient):
    """Test getting projects via API."""
    # Create projects
    client.post("/projects/", json={"name": "Project 1"})
    client.post("/projects/", json={"name": "Project 2"})

    response = client.get("/projects/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_project(client: TestClient):
    """Test getting a specific project via API."""
    # Create project
    create_response = client.post(
        "/projects/",
        json={"name": "Test Project"}
    )
    project_id = create_response.json()["id"]

    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"


def test_get_project_not_found(client: TestClient):
    """Test getting non-existent project."""
    response = client.get("/projects/999")
    assert response.status_code == 404


def test_update_project(client: TestClient):
    """Test updating a project via API."""
    # Create project
    create_response = client.post(
        "/projects/",
        json={"name": "Old Name"}
    )
    project_id = create_response.json()["id"]

    response = client.put(
        f"/projects/{project_id}",
        json={"name": "New Name", "description": "New description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["description"] == "New description"


def test_archive_project(client: TestClient):
    """Test archiving a project via API."""
    # Create project
    create_response = client.post(
        "/projects/",
        json={"name": "Test Project"}
    )
    project_id = create_response.json()["id"]

    response = client.put(f"/projects/{project_id}/archive")
    assert response.status_code == 200
    data = response.json()
    assert data["archived"]


def test_delete_project(client: TestClient):
    """Test deleting a project via API."""
    # Create project
    create_response = client.post(
        "/projects/",
        json={"name": "Test Project"}
    )
    project_id = create_response.json()["id"]

    response = client.delete(f"/projects/{project_id}")
    assert response.status_code == 200

    # Verify deleted
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 404