"""Pytest configuration and fixtures."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from taskforge.database import Base
from taskforge.config import settings


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine."""
    # Use in-memory SQLite for tests
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_engine):
    """Create test database session."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def user_service(db_session):
    """Create user service for testing."""
    from taskforge.services.user_service import UserService
    return UserService(db_session)


@pytest.fixture
def project_service(db_session):
    """Create project service for testing."""
    from taskforge.services.project_service import ProjectService
    return ProjectService(db_session)


@pytest.fixture
def task_service(db_session):
    """Create task service for testing."""
    from taskforge.services.task_service import TaskService
    return TaskService(db_session)


@pytest.fixture
def tag_service(db_session):
    """Create tag service for testing."""
    from taskforge.services.tag_service import TagService
    return TagService(db_session)


@pytest.fixture
def note_service(db_session):
    """Create note service for testing."""
    from taskforge.services.note_service import NoteService
    return NoteService(db_session)


@pytest.fixture
def reminder_service(db_session):
    """Create reminder service for testing."""
    from taskforge.services.reminder_service import ReminderService
    return ReminderService(db_session)


@pytest.fixture
def report_service(db_session):
    """Create report service for testing."""
    from taskforge.services.report_service import ReportService
    return ReportService(db_session)


@pytest.fixture
def client(db_session):
    """Create FastAPI test client."""
    from fastapi.testclient import TestClient
    from taskforge.api.main import app
    from taskforge.api.dependencies import get_db

    def override_get_db():
        return db_session

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)