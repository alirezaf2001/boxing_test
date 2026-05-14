#!/usr/bin/env python3
"""Seed the database with demo data for testing and development."""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datetime import datetime, timedelta
from taskforge.database import SessionLocal, create_tables
from taskforge.models.user import User
from taskforge.models.project import Project
from taskforge.models.task import Task
from taskforge.models.tag import Tag
from taskforge.models.note import Note
from taskforge.models.reminder import Reminder
from taskforge.models.task_tag import TaskTag


def seed_demo_data():
    """Seed the database with demo data."""
    print("Creating database tables...")
    create_tables()

    db = SessionLocal()
    try:
        print("Seeding demo data...")

        # Create user
        user = User(
            name="Demo User",
            email="demo@example.com",
            timezone="UTC"
        )
        db.add(user)
        db.commit()
        print(f"Created user: {user.name}")

        # Create projects
        projects = [
            Project(name="Work Projects", description="Professional tasks and projects"),
            Project(name="Personal", description="Personal tasks and goals"),
            Project(name="Learning", description="Courses, books, and skill development"),
        ]

        for project in projects:
            db.add(project)
        db.commit()
        print(f"Created {len(projects)} projects")

        # Create tags
        tags = [
            Tag(name="urgent", color="#FF0000"),
            Tag(name="important", color="#FFA500"),
            Tag(name="low-priority", color="#00FF00"),
            Tag(name="bug", color="#FF00FF"),
            Tag(name="feature", color="#0000FF"),
        ]

        for tag in tags:
            db.add(tag)
        db.commit()
        print(f"Created {len(tags)} tags")

        # Create tasks
        tasks = [
            Task(
                title="Review quarterly reports",
                description="Analyze Q4 financial reports and prepare summary",
                project_id=projects[0].id,
                priority="high",
                due_date=datetime.now().date() + timedelta(days=3)
            ),
            Task(
                title="Update project documentation",
                description="Update README and API documentation",
                project_id=projects[0].id,
                priority="medium",
                due_date=datetime.now().date() + timedelta(days=7)
            ),
            Task(
                title="Grocery shopping",
                description="Buy groceries for the week",
                project_id=projects[1].id,
                priority="medium",
                due_date=datetime.now().date() + timedelta(days=1)
            ),
            Task(
                title="Read 'Clean Code' book",
                description="Complete chapter 5-8 of Clean Code",
                project_id=projects[2].id,
                priority="low",
                due_date=datetime.now().date() + timedelta(days=14)
            ),
            Task(
                title="Fix login bug",
                description="Users unable to login with special characters in password",
                project_id=projects[0].id,
                priority="high",
                status="completed",
                completed_at=datetime.now() - timedelta(hours=2)
            ),
            Task(
                title="Implement dark mode",
                description="Add dark mode toggle to user interface",
                project_id=projects[0].id,
                priority="medium",
                status="completed",
                completed_at=datetime.now() - timedelta(days=1)
            ),
        ]

        for task in tasks:
            db.add(task)
        db.commit()
        print(f"Created {len(tasks)} tasks")

        # Add tags to tasks
        task_tags = [
            TaskTag(task_id=tasks[0].id, tag_id=tags[0].id),  # urgent
            TaskTag(task_id=tasks[0].id, tag_id=tags[1].id),  # important
            TaskTag(task_id=tasks[4].id, tag_id=tags[3].id),  # bug
            TaskTag(task_id=tasks[5].id, tag_id=tags[4].id),  # feature
        ]

        for task_tag in task_tags:
            db.add(task_tag)
        db.commit()
        print(f"Created {len(task_tags)} task-tag relationships")

        # Create notes
        notes = [
            Note(
                title="Meeting Notes - Sprint Planning",
                content="""Discussed upcoming sprint goals:
- Complete user authentication
- Implement task filtering
- Add export functionality
- Review performance metrics

Action items:
- John: Update task schema
- Jane: Implement filtering logic
- Bob: Add export endpoints""",
                project_id=projects[0].id
            ),
            Note(
                title="Book Notes - Chapter 3",
                content="""Key takeaways from Clean Code Chapter 3:

1. Functions should be small
2. Functions should do one thing
3. One level of abstraction per function
4. Reading code from top to bottom
5. Use descriptive names

Examples of good function names:
- renderPageWithSetupsAndTeardowns() → too long
- renderPage() → better""",
                project_id=projects[2].id
            ),
            Note(
                title="Bug Investigation",
                content="""Login bug investigation:

Symptoms:
- Users with special chars in password can't login
- Error: "Invalid password format"

Root cause:
- Password validation regex too restrictive
- Missing URL encoding for special characters

Fix:
- Update regex pattern
- Add proper encoding/decoding""",
                task_id=tasks[4].id
            ),
        ]

        for note in notes:
            db.add(note)
        db.commit()
        print(f"Created {len(notes)} notes")

        # Create reminders
        reminders = [
            Reminder(
                title="Team standup",
                reminder_datetime=datetime.now() + timedelta(hours=2),
                note="Daily standup meeting at 10 AM"
            ),
            Reminder(
                title="Submit expense report",
                reminder_datetime=datetime.now() + timedelta(days=1, hours=9),
                note="Monthly expense report due"
            ),
            Reminder(
                title="Doctor appointment",
                reminder_datetime=datetime.now() + timedelta(days=5, hours=14),
                note="Annual checkup with Dr. Smith"
            ),
            Reminder(
                title="Project deadline",
                reminder_datetime=datetime.now() + timedelta(days=3),
                task_id=tasks[0].id,
                note="Quarterly reports due"
            ),
        ]

        for reminder in reminders:
            db.add(reminder)
        db.commit()
        print(f"Created {len(reminders)} reminders")

        print("\nDemo data seeded successfully!")
        print("\nSummary:")
        print(f"- 1 user")
        print(f"- {len(projects)} projects")
        print(f"- {len(tags)} tags")
        print(f"- {len(tasks)} tasks ({sum(1 for t in tasks if t.status == 'completed')} completed)")
        print(f"- {len(notes)} notes")
        print(f"- {len(reminders)} reminders")
        print(f"- {len(task_tags)} task-tag relationships")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()