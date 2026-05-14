"""Date utility functions."""

from datetime import datetime
from typing import Optional


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string into datetime object."""
    try:
        # Try ISO format first
        return datetime.fromisoformat(date_str)
    except ValueError:
        pass

    # Try common formats
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%m/%d/%Y",
        "%d/%m/%Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    return None


def format_date(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime object to string."""
    return dt.strftime(format_str)