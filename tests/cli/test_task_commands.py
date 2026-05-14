"""CLI tests for task commands."""

from typer.testing import CliRunner

from taskforge.cli.main import app


def test_create_task_command():
    """Test create task CLI command."""
    runner = CliRunner()
    result = runner.invoke(app, ["task", "create", "Test Task", "--description", "A test task"])
    assert result.exit_code == 0
    assert "Task created successfully" in result.output


def test_list_tasks_command():
    """Test list tasks CLI command."""
    runner = CliRunner()

    # Create some tasks
    runner.invoke(app, ["task", "create", "Task 1"])
    runner.invoke(app, ["task", "create", "Task 2"])

    result = runner.invoke(app, ["task", "list"])
    assert result.exit_code == 0
    assert "Task 1" in result.output
    assert "Task 2" in result.output


def test_get_task_command():
    """Test get task CLI command."""
    runner = CliRunner()

    # Create a task
    runner.invoke(app, ["task", "create", "Test Task"])

    result = runner.invoke(app, ["task", "get", "1"])
    assert result.exit_code == 0
    assert "Test Task" in result.output


def test_update_task_command():
    """Test update task CLI command."""
    runner = CliRunner()

    # Create a task
    runner.invoke(app, ["task", "create", "Old Title"])

    result = runner.invoke(app, ["task", "update", "1", "--title", "New Title", "--priority", "high"])
    assert result.exit_code == 0
    assert "Task updated successfully" in result.output


def test_complete_task_command():
    """Test complete task CLI command."""
    runner = CliRunner()

    # Create a task
    runner.invoke(app, ["task", "create", "Test Task"])

    result = runner.invoke(app, ["task", "complete", "1"])
    assert result.exit_code == 0
    assert "Task completed successfully" in result.output


def test_search_tasks_command():
    """Test search tasks CLI command."""
    runner = CliRunner()

    # Create tasks
    runner.invoke(app, ["task", "create", "Buy groceries"])
    runner.invoke(app, ["task", "create", "Write report"])

    result = runner.invoke(app, ["task", "search", "report"])
    assert result.exit_code == 0
    assert "Write report" in result.output
    assert "Buy groceries" not in result.output


def test_delete_task_command():
    """Test delete task CLI command."""
    runner = CliRunner()

    # Create a task
    runner.invoke(app, ["task", "create", "Test Task"])

    result = runner.invoke(app, ["task", "delete", "1"])
    assert result.exit_code == 0
    assert "Task deleted successfully" in result.output