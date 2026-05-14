"""Integration tests for database operations."""

from taskforge.database import create_tables, reset_database, SessionLocal


def test_create_tables():
    """Test creating database tables."""
    # Tables should be created during app startup
    # This test just verifies no exceptions are raised
    create_tables()


def test_database_session():
    """Test database session creation and usage."""
    db = SessionLocal()
    try:
        # Test basic query
        result = db.execute("SELECT 1")
        assert result.fetchone()[0] == 1
    finally:
        db.close()


def test_reset_database():
    """Test resetting database."""
    # Create some data first
    db = SessionLocal()
    try:
        from taskforge.models.user import User
        user = User(name="Test User", email="test@example.com")
        db.add(user)
        db.commit()

        # Verify user exists
        users = db.query(User).all()
        assert len(users) == 1
    finally:
        db.close()

    # Reset database
    reset_database()

    # Verify data is gone
    db = SessionLocal()
    try:
        from taskforge.models.user import User
        users = db.query(User).all()
        assert len(users) == 0
    finally:
        db.close()