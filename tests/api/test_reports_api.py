"""API tests for report endpoints."""

from fastapi.testclient import TestClient

from taskforge.api.main import app


def test_get_productivity_report(client: TestClient):
    """Test getting productivity report via API."""
    response = client.get("/reports/productivity")
    assert response.status_code == 200
    data = response.json()
    assert "total_tasks" in data
    assert "completed_tasks" in data
    assert "completion_rate" in data


def test_get_project_report(client: TestClient):
    """Test getting project report via API."""
    response = client.get("/reports/projects")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_task_report(client: TestClient):
    """Test getting task report via API."""
    response = client.get("/reports/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_export_productivity_report(client: TestClient):
    """Test exporting productivity report via API."""
    response = client.get("/reports/productivity/export?format=json")
    assert response.status_code == 200
    data = response.json()
    assert "total_tasks" in data

    response = client.get("/reports/productivity/export?format=csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]


def test_export_project_report(client: TestClient):
    """Test exporting project report via API."""
    response = client.get("/reports/projects/export?format=json")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    response = client.get("/reports/projects/export?format=csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]