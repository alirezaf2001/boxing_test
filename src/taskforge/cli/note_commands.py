"""CLI commands for note management."""

import typer

from taskforge.services.note_service import NoteService

app = typer.Typer()


@app.command()
def create(
    content: str = typer.Argument(..., help="Note content"),
    project: str = typer.Option(None, "--project", help="Project name"),
    task_id: int = typer.Option(None, "--task-id", help="Task ID"),
):
    """Create a new note."""
    try:
        note_service = NoteService()
        note = note_service.create_note(
            content=content, project_name=project, task_id=task_id
        )
        typer.echo(f"Note created (ID: {note.id})")
    except Exception as e:
        typer.echo(f"Error creating note: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def list(
    project: str = typer.Option(None, "--project", help="Filter by project name"),
    task_id: int = typer.Option(None, "--task-id", help="Filter by task ID"),
):
    """List notes."""
    try:
        note_service = NoteService()
        notes = note_service.get_notes(project_name=project, task_id=task_id)

        if not notes:
            typer.echo("No notes found.")
            return

        for note in notes:
            project_name = f" (Project: {note.project.name})" if note.project else ""
            task_title = f" (Task: {note.task.title})" if note.task else ""
            typer.echo(f"Note {note.id}: {note.content[:50]}...{project_name}{task_title}")
    except Exception as e:
        typer.echo(f"Error listing notes: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def update(
    note_id: int = typer.Argument(..., help="Note ID"),
    content: str = typer.Option(..., "--content", help="New note content"),
):
    """Update a note."""
    try:
        note_service = NoteService()
        note = note_service.update_note(note_id=note_id, content=content)
        typer.echo(f"Note updated: {note.content[:50]}...")
    except Exception as e:
        typer.echo(f"Error updating note: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def delete(note_id: int = typer.Argument(..., help="Note ID")):
    """Delete a note."""
    try:
        confirm = typer.confirm("Are you sure you want to delete this note?")
        if not confirm:
            typer.echo("Operation cancelled.")
            return

        note_service = NoteService()
        note_service.delete_note(note_id=note_id)
        typer.echo("Note deleted.")
    except Exception as e:
        typer.echo(f"Error deleting note: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def search(query: str = typer.Argument(..., help="Search query")):
    """Search notes by content."""
    try:
        note_service = NoteService()
        notes = note_service.search_notes(query=query)

        if not notes:
            typer.echo("No notes found matching the query.")
            return

        for note in notes:
            project_name = f" (Project: {note.project.name})" if note.project else ""
            task_title = f" (Task: {note.task.title})" if note.task else ""
            typer.echo(f"Note {note.id}: {note.content[:50]}...{project_name}{task_title}")
    except Exception as e:
        typer.echo(f"Error searching notes: {e}", err=True)
        raise typer.Exit(1)