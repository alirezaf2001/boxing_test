"""Main CLI application using Typer."""

import typer

from taskforge.cli import (
    user_commands,
    project_commands,
    task_commands,
    tag_commands,
    note_commands,
    reminder_commands,
    report_commands,
)

app = typer.Typer(
    name="taskforge",
    help="TaskForge - A local productivity and workflow management app",
    add_completion=False,
)

# Add subcommands
app.add_typer(user_commands.app, name="user", help="User profile management")
app.add_typer(project_commands.app, name="project", help="Project management")
app.add_typer(task_commands.app, name="task", help="Task management")
app.add_typer(tag_commands.app, name="tag", help="Tag management")
app.add_typer(note_commands.app, name="note", help="Note management")
app.add_typer(reminder_commands.app, name="reminder", help="Reminder management")
app.add_typer(report_commands.app, name="report", help="Report generation")

@app.callback()
def callback():
    """TaskForge CLI - Manage your productivity workflow."""
    pass


if __name__ == "__main__":
    app()