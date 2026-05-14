"""CLI commands for reminder management."""

import typer

from taskforge.services.reminder_service import ReminderService

app = typer.Typer()


@app.command()
def create(
    task_id: int = typer.Argument(..., help="Task ID"),
    message: str = typer.Option(..., "--message", help="Reminder message"),
    remind_at: str = typer.Option(..., "--remind-at", help="Reminder date/time (YYYY-MM-DD HH:MM)"),
):
    """Create a reminder for a task."""
    try:
        reminder_service = ReminderService()
        reminder = reminder_service.create_reminder(
            task_id=task_id, message=message, remind_at=remind_at
        )
        typer.echo(f"Reminder created for task {task_id}")
    except Exception as e:
        typer.echo(f"Error creating reminder: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def list(
    status: str = typer.Option("pending", "--status", help="Filter by status (pending/dismissed/all)"),
):
    """List reminders."""
    try:
        reminder_service = ReminderService()
        reminders = reminder_service.get_reminders(status=status)

        if not reminders:
            typer.echo("No reminders found.")
            return

        for reminder in reminders:
            status_indicator = "[DISMISSED]" if reminder.dismissed else "[PENDING]"
            typer.echo(f"{status_indicator} Task {reminder.task_id}: {reminder.message} (at {reminder.remind_at})")
    except Exception as e:
        typer.echo(f"Error listing reminders: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def dismiss(reminder_id: int = typer.Argument(..., help="Reminder ID")):
    """Dismiss a reminder."""
    try:
        reminder_service = ReminderService()
        reminder = reminder_service.dismiss_reminder(reminder_id=reminder_id)
        typer.echo(f"Reminder dismissed for task {reminder.task_id}")
    except Exception as e:
        typer.echo(f"Error dismissing reminder: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def upcoming():
    """List upcoming reminders."""
    try:
        reminder_service = ReminderService()
        reminders = reminder_service.get_upcoming_reminders()

        if not reminders:
            typer.echo("No upcoming reminders.")
            return

        for reminder in reminders:
            typer.echo(f"Task {reminder.task_id}: {reminder.message} (at {reminder.remind_at})")
    except Exception as e:
        typer.echo(f"Error listing upcoming reminders: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def delete(reminder_id: int = typer.Argument(..., help="Reminder ID")):
    """Delete a reminder."""
    try:
        confirm = typer.confirm("Are you sure you want to delete this reminder?")
        if not confirm:
            typer.echo("Operation cancelled.")
            return

        reminder_service = ReminderService()
        reminder_service.delete_reminder(reminder_id=reminder_id)
        typer.echo("Reminder deleted.")
    except Exception as e:
        typer.echo(f"Error deleting reminder: {e}", err=True)
        raise typer.Exit(1)