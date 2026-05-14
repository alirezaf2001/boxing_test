"""CLI commands for project management."""

import typer

from taskforge.services.project_service import ProjectService

app = typer.Typer()


@app.command()
def create(
    name: str = typer.Argument(..., help="Project name"),
    description: str = typer.Option("", "--description", help="Project description"),
):
    """Create a new project."""
    try:
        project_service = ProjectService()
        project = project_service.create_project(name=name, description=description)
        typer.echo(f"Project created: {project.name}")
    except Exception as e:
        typer.echo(f"Error creating project: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def list(
    status: str = typer.Option("all", "--status", help="Filter by status (active/archived/all)"),
):
    """List projects."""
    try:
        project_service = ProjectService()
        projects = project_service.get_projects(status=status)

        if not projects:
            typer.echo("No projects found.")
            return

        for project in projects:
            status_indicator = "[ARCHIVED]" if project.archived else "[ACTIVE]"
            typer.echo(f"{status_indicator} {project.name} - {project.description or 'No description'}")
    except Exception as e:
        typer.echo(f"Error listing projects: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def update(
    project_id: int = typer.Argument(..., help="Project ID"),
    name: str = typer.Option(None, "--name", help="New project name"),
    description: str = typer.Option(None, "--description", help="New project description"),
):
    """Update a project."""
    try:
        project_service = ProjectService()
        project = project_service.update_project(
            project_id=project_id, name=name, description=description
        )
        typer.echo(f"Project updated: {project.name}")
    except Exception as e:
        typer.echo(f"Error updating project: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def archive(project_id: int = typer.Argument(..., help="Project ID")):
    """Archive a project."""
    try:
        project_service = ProjectService()
        project = project_service.archive_project(project_id=project_id)
        typer.echo(f"Project archived: {project.name}")
    except Exception as e:
        typer.echo(f"Error archiving project: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def unarchive(project_id: int = typer.Argument(..., help="Project ID")):
    """Unarchive a project."""
    try:
        project_service = ProjectService()
        project = project_service.unarchive_project(project_id=project_id)
        typer.echo(f"Project unarchived: {project.name}")
    except Exception as e:
        typer.echo(f"Error unarchiving project: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def delete(project_id: int = typer.Argument(..., help="Project ID")):
    """Delete a project."""
    try:
        confirm = typer.confirm("Are you sure you want to delete this project?")
        if not confirm:
            typer.echo("Operation cancelled.")
            return

        project_service = ProjectService()
        project_service.delete_project(project_id=project_id)
        typer.echo("Project deleted.")
    except Exception as e:
        typer.echo(f"Error deleting project: {e}", err=True)
        raise typer.Exit(1)