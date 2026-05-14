"""Logging configuration for TaskForge."""

import logging
import sys
from pathlib import Path

from taskforge.config import settings


def setup_logging():
    """Configure logging for the application."""
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Create logger
    logger = logging.getLogger("taskforge")
    logger.setLevel(log_level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if log_file is specified)
    if settings.log_file:
        log_path = Path(settings.log_file)
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Global logger instance
logger = setup_logging()