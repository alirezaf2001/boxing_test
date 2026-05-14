"""Unit tests for report service."""

import pytest
from datetime import datetime, timedelta


def test_generate_daily_summary(report_service, task_service):
    """Test generating daily summary."""
    task_service.create_task(title="Task 1")
    task_service.create_task(title="Task 2")
    completed = task_service.create_task(title="Task 3")
    task_service.complete_task(completed.id)

    report = report_service.generate_daily_summary()
    assert report["total_tasks"] == 3
    assert report["completed_tasks"] == 1
    assert report["pending_tasks"] == 2


def test_generate_weekly_summary(report_service, task_service):
    """Test generating weekly summary."""
    # Create some tasks
    for i in range(5):
        task = task_service.create_task(title=f"Task {i}")
        if i < 2:  # Complete 2 tasks
            task_service.complete_task(task.id)

    report = report_service.generate_weekly_summary()
    assert report["total_tasks"] == 5
    assert report["completed_tasks"] == 2
    assert "completion_rate" in report
    assert "average_per_day" in report


def test_generate_project_report(report_service, project_service, task_service):
    """Test generating project report."""
    project = project_service.create_project(name="Test Project")

    # Create tasks in project
    task1 = task_service.create_task(title="Task 1", project_name="Test Project")
    task2 = task_service.create_task(title="Task 2", project_name="Test Project")
    task_service.complete_task(task1.id)

    # Create overdue task
    overdue_task = task_service.create_task(
        title="Overdue Task",
        project_name="Test Project",
        due_date=datetime.utcnow() - timedelta(days=1)
    )

    report = report_service.generate_project_report(project.id)
    assert report["project_name"] == "Test Project"
    assert report["total_tasks"] == 3
    assert report["completed_tasks"] == 1
    assert report["pending_tasks"] == 2
    assert report["overdue_tasks"] == 1


def test_generate_project_report_not_found(report_service):
    """Test generating report for non-existent project."""
    with pytest.raises(ValueError):
        report_service.generate_project_report(999)


def test_generate_overdue_report(report_service, task_service):
    """Test generating overdue report."""
    # Create regular task
    task_service.create_task(title="Regular Task")

    # Create overdue task
    task_service.create_task(
        title="Overdue Task",
        due_date=datetime.utcnow() - timedelta(days=1)
    )

    report = report_service.generate_overdue_report()
    assert len(report["overdue_tasks"]) == 1
    assert report["overdue_tasks"][0]["title"] == "Overdue Task"