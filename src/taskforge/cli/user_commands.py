"""CLI commands for user management."""

import typer

from taskforge.services.user_service import UserService

app = typer.Typer()


@app.command()
def create(
    name: str = typer.Option(..., "--name", help="User name"),
    email: str = typer.Option(..., "--email", help="User email"),
    timezone: str = typer.Option("UTC", "--timezone", help="User timezone"),
):
    """Create a new user profile."""
    try:
        user_service = UserService()
        user = user_service.create_user(name=name, email=email, timezone=timezone)
        typer.echo(f"User created: {user.name} ({user.email})")
    except Exception as e:
        typer.echo(f"Error creating user: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def update(
    name: str = typer.Option(None, "--name", help="New user name"),
    email: str = typer.Option(None, "--email", help="New user email"),
    timezone: str = typer.Option(None, "--timezone", help="New user timezone"),
):
    """Update the current user profile."""
    try:
        user_service = UserService()
        user = user_service.update_user(name=name, email=email, timezone=timezone)
        typer.echo(f"User updated: {user.name} ({user.email})")
    except Exception as e:
        typer.echo(f"Error updating user: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def show():
    """Show current user profile."""
    try:
        user_service = UserService()
        user = user_service.get_user()
        if user:
            typer.echo(f"Name: {user.name}")
            typer.echo(f"Email: {user.email}")
            typer.echo(f"Timezone: {user.timezone}")
            typer.echo(f"Created: {user.created_at}")
        else:
            typer.echo("No user profile found. Create one with 'user create'.")
    except Exception as e:
        typer.echo(f"Error showing user: {e}", err=True)
        raise typer.Exit(1)