"""Custom exceptions for TaskForge."""


class TaskForgeError(Exception):
    """Base exception for TaskForge errors."""
    pass


class NotFoundError(TaskForgeError):
    """Raised when a resource is not found."""
    pass


class ValidationError(TaskForgeError):
    """Raised when validation fails."""
    pass


class DatabaseError(TaskForgeError):
    """Raised when database operations fail."""
    pass


class ConfigurationError(TaskForgeError):
    """Raised when configuration is invalid."""
    pass