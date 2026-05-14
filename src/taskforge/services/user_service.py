"""User service."""

from typing import Optional

from sqlalchemy.orm import Session

from taskforge.repositories.user_repository import UserRepository
from taskforge.models.user import User
from taskforge.exceptions import NotFoundError


class UserService:
    """Service for user operations."""

    def __init__(self, db: Optional[Session] = None):
        """Initialize service with database session."""
        from taskforge.database import SessionLocal
        self.db = db or SessionLocal()
        self.repository = UserRepository(self.db)

    def create_user(self, name: str, email: str, timezone: str = "UTC") -> User:
        """Create a new user."""
        return self.repository.create_user(name=name, email=email, timezone=timezone)

    def get_user(self) -> Optional[User]:
        """Get the current user."""
        return self.repository.get_user()

    def update_user(self, name: Optional[str] = None, email: Optional[str] = None,
                   timezone: Optional[str] = None) -> User:
        """Update user information."""
        user = self.get_user()
        if not user:
            raise NotFoundError("User not found")
        return self.repository.update_user(user, name=name, email=email, timezone=timezone)

    def delete_user(self) -> None:
        """Delete the current user."""
        user = self.get_user()
        if not user:
            raise NotFoundError("User not found")
        self.repository.delete_user(user)