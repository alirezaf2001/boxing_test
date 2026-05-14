"""User repository."""

from typing import Optional

from sqlalchemy.orm import Session

from taskforge.models.user import User


class UserRepository:
    """Repository for user operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create_user(self, name: str, email: str, timezone: str = "UTC") -> User:
        """Create a new user."""
        user = User(name=name, email=email, timezone=timezone)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self) -> Optional[User]:
        """Get the first (and typically only) user."""
        return self.db.query(User).first()

    def update_user(self, user: User, name: Optional[str] = None,
                   email: Optional[str] = None, timezone: Optional[str] = None) -> User:
        """Update user information."""
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if timezone is not None:
            user.timezone = timezone

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User) -> None:
        """Delete a user."""
        self.db.delete(user)
        self.db.commit()