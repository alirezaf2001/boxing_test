"""CLI commands for task management."""

import typer
from typing import Optional

from taskforge.services.task_service import TaskService

app = typer.Typer()


@app.command()
def create(
    title: str = typer.Argument(..., help="Task title"),
    description: str = typer.Option("", "--description", help="Task description"),
    project: str = typer.Option(None, "--project", help="Project name"),
    priority: str = typer.Option("medium", "--priority", help="Task priority (low/medium/high/urgent)"),
    due_date: str = typer.Option(None, "--due-date", help="Due date (YYYY-MM-DD)"),
):
    """Create a new task."""
    try:
        task_service = TaskService()
        task = task_service.create_task(
            title=title,
            description=description,
            project_name=project,
            priority=priority,
            due_date=due_date,
        )
        typer.echo(f"Task created: {task.title} (ID: {task.id})")
    except Exception as e:
        typer.echo(f"Error creating task: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def list(
    status: str = typer.Option("active", "--status", help="Filter by status (active/completed/all)"),
    project: str = typer.Option(None, "--project", help="Filter by project name"),
    priority: str = typer.Option(None, "--priority", help="Filter by priority"),
):
    """List tasks."""
    try:
        task_service = TaskService()
        tasks = task_service.get_tasks(
            status=status, project_name=project, priority=priority
        )

        if not tasks:
            typer.echo("No tasks found.")
            return

        for task in tasks:
            status_indicator = "[✓]" if task.completed else "[ ]"
            priority_indicator = f"[{task.priority.upper()}]"
            project_name = f" ({task.project.name})" if task.project else ""
            typer.echo(f"{status_indicator} {priority_indicator} {task.title}{project_name}")
    except Exception as e:
        typer.echo(f"Error listing tasks: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def update(
    task_id: int = typer.Argument(..., help="Task ID"),
    title: str = typer.Option(None, "--title", help="New task title"),
    description: str = typer.Option(None, "--description", help="New task description"),
    priority: str = typer.Option(None, "--priority", help="New task priority"),
    due_date: str = typer.Option(None, "--due-date", help="New due date"),
):
    """Update a task."""
    try:
        task_service = TaskService()
        task = task_service.update_task(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
        )
        typer.echo(f"Task updated: {task.title}")
    except Exception as e:
        typer.echo(f"Error updating task: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def complete(task_id: int = typer.Argument(..., help="Task ID")):
    """Mark a task as completed."""
    try:
        task_service = TaskService()
        task = task_service.complete_task(task_id=task_id)
        typer.echo(f"Task completed: {task.title}")
    except Exception as e:
        typer.echo(f"Error completing task: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def incomplete(task_id: int = typer.Argument(..., help="Task ID")):
    """Mark a task as incomplete."""
    try:
        task_service = TaskService()
        task = task_service.incomplete_task(task_id=task_id)
        typer.echo(f"Task marked as incomplete: {task.title}")
    except Exception as e:
        typer.echo(f"Error updating task: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def delete(task_id: int = typer.Argument(..., help="Task ID")):
    """Delete a task."""
    try:
        confirm = typer.confirm("Are you sure you want to delete this task?")
        if not confirm:
            typer.echo("Operation cancelled.")
            return

        task_service = TaskService()
        task_service.delete_task(task_id=task_id)
        typer.echo("Task deleted.")
    except Exception as e:
        typer.echo(f"Error deleting task: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def search(query: str = typer.Argument(..., help="Search query")):
    """Search tasks by title or description."""
    try:
        task_service = TaskService()
        tasks = task_service.search_tasks(query=query)

        if not tasks:
            typer.echo("No tasks found matching the query.")
            return

        for task in tasks:
            status_indicator = "[✓]" if task.completed else "[ ]"
            priority_indicator = f"[{task.priority.upper()}]"
            project_name = f" ({task.project.name})" if task.project else ""
            typer.echo(f"{status_indicator} {priority_indicator} {task.title}{project_name}")
    except Exception as e:
        typer.echo(f"Error searching tasks: {e}", err=True)
        raise typer.Exit(1)