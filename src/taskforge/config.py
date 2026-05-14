"""Configuration management for TaskForge."""

import os
from pathlib import Path
from typing import Optional

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "sqlite:///./taskforge.db"

    # Application
    app_name: str = "TaskForge"
    app_version: str = "0.1.0"
    debug: bool = False

    # User settings
    default_timezone: str = "UTC"
    default_date_format: str = "%Y-%m-%d"
    default_time_format: str = "%H:%M:%S"

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False

    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = "taskforge.log"

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Database path
def get_database_path() -> Path:
    """Get the database file path."""
    if settings.database_url.startswith("sqlite:///"):
        db_path = settings.database_url.replace("sqlite:///", "")
        return Path(db_path)
    return Path("./taskforge.db")

# Data directory
def get_data_directory() -> Path:
    """Get the application data directory."""
    data_dir = Path.home() / ".taskforge"
    data_dir.mkdir(exist_ok=True)
    return data_dir