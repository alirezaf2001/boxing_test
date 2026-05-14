"""API tests for user endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from taskforge.api.main import app


def test_create_user(client: TestClient, db_session: Session):
    """Test creating a user via API."""
    response = client.post(
        "/users/",
        json={"name": "John Doe", "email": "john@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"


def test_get_user(client: TestClient, db_session: Session):
    """Test getting user via API."""
    # Create user first
    client.post(
        "/users/",
        json={"name": "Jane Doe", "email": "jane@example.com"}
    )

    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Doe"


def test_get_user_not_found(client: TestClient):
    """Test getting user when none exists."""
    response = client.get("/users/")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_user(client: TestClient, db_session: Session):
    """Test updating user via API."""
    # Create user first
    client.post(
        "/users/",
        json={"name": "John Doe", "email": "john@example.com"}
    )

    response = client.put(
        "/users/",
        json={"name": "Jane Doe", "timezone": "EST"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["timezone"] == "EST"
    assert data["email"] == "john@example.com"