"""Validation utility functions."""

import re
from typing import List


def validate_email(email: str) -> bool:
    """Validate email address format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_priority(priority: str) -> bool:
    """Validate task priority."""
    return priority in ["low", "medium", "high", "urgent"]


def validate_project_name(name: str) -> bool:
    """Validate project name."""
    if not name or not name.strip():
        return False
    # Check for invalid characters
    return not re.search(r'[<>:"/\\|?*]', name)


def validate_tag_name(name: str) -> bool:
    """Validate tag name."""
    if not name or not name.strip():
        return False
    # Tags can contain letters, numbers, spaces, hyphens, underscores
    return re.match(r'^[a-zA-Z0-9\s\-_]+$', name) is not None