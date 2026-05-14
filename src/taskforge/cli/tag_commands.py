"""CLI commands for tag management."""

import typer

from taskforge.services.tag_service import TagService

app = typer.Typer()


@app.command()
def create(name: str = typer.Argument(..., help="Tag name")):
    """Create a new tag."""
    try:
        tag_service = TagService()
        tag = tag_service.create_tag(name=name)
        typer.echo(f"Tag created: {tag.name}")
    except Exception as e:
        typer.echo(f"Error creating tag: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def list():
    """List all tags."""
    try:
        tag_service = TagService()
        tags = tag_service.get_tags()

        if not tags:
            typer.echo("No tags found.")
            return

        for tag in tags:
            typer.echo(f"{tag.name} (used in {len(tag.tasks)} tasks)")
    except Exception as e:
        typer.echo(f"Error listing tags: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def add(
    task_id: int = typer.Argument(..., help="Task ID"),
    tag_name: str = typer.Argument(..., help="Tag name"),
):
    """Add a tag to a task."""
    try:
        tag_service = TagService()
        tag_service.add_tag_to_task(task_id=task_id, tag_name=tag_name)
        typer.echo(f"Tag '{tag_name}' added to task {task_id}")
    except Exception as e:
        typer.echo(f"Error adding tag: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def remove(
    task_id: int = typer.Argument(..., help="Task ID"),
    tag_name: str = typer.Argument(..., help="Tag name"),
):
    """Remove a tag from a task."""
    try:
        tag_service = TagService()
        tag_service.remove_tag_from_task(task_id=task_id, tag_name=tag_name)
        typer.echo(f"Tag '{tag_name}' removed from task {task_id}")
    except Exception as e:
        typer.echo(f"Error removing tag: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def search(tag_name: str = typer.Argument(..., help="Tag name")):
    """Search tasks by tag."""
    try:
        tag_service = TagService()
        tasks = tag_service.get_tasks_by_tag(tag_name=tag_name)

        if not tasks:
            typer.echo(f"No tasks found with tag '{tag_name}'.")
            return

        for task in tasks:
            status_indicator = "[✓]" if task.completed else "[ ]"
            priority_indicator = f"[{task.priority.upper()}]"
            project_name = f" ({task.project.name})" if task.project else ""
            typer.echo(f"{status_indicator} {priority_indicator} {task.title}{project_name}")
    except Exception as e:
        typer.echo(f"Error searching by tag: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def delete(name: str = typer.Argument(..., help="Tag name")):
    """Delete a tag."""
    try:
        confirm = typer.confirm("Are you sure you want to delete this tag?")
        if not confirm:
            typer.echo("Operation cancelled.")
            return

        tag_service = TagService()
        tag_service.delete_tag(name=name)
        typer.echo(f"Tag '{name}' deleted.")
    except Exception as e:
        typer.echo(f"Error deleting tag: {e}", err=True)
        raise typer.Exit(1)