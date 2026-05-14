#!/usr/bin/env python3
"""Reset the database by dropping all tables and recreating them."""

import sys
from pathlib import Path
import os

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from taskforge.database import Base, engine, create_tables
from taskforge.config import settings


def reset_database():
    """Reset the database by dropping and recreating all tables."""
    print(f"Database URL: {settings.database_url}")

    # Confirm action
    confirm = input("This will delete all data in the database. Are you sure? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        return

    try:
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)

        print("Creating all tables...")
        create_tables()

        print("Database reset successfully!")

        # Ask if user wants to seed demo data
        seed = input("Would you like to seed demo data? (yes/no): ")
        if seed.lower() == 'yes':
            print("Seeding demo data...")
            from seed_demo_data import seed_demo_data
            seed_demo_data()
            print("Demo data seeded!")

    except Exception as e:
        print(f"Error resetting database: {e}")
        raise


if __name__ == "__main__":
    reset_database()