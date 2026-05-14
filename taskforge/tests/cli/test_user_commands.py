"""CLI tests for user commands."""

from typer.testing import CliRunner

from taskforge.cli.main import app


def test_create_user_command():
    """Test create user CLI command."""
    runner = CliRunner()
    result = runner.invoke(app, ["user", "create", "John Doe", "john@example.com"])
    assert result.exit_code == 0
    assert "User created successfully" in result.output


def test_get_user_command():
    """Test get user CLI command."""
    runner = CliRunner()

    # First create a user
    runner.invoke(app, ["user", "create", "Jane Doe", "jane@example.com"])

    result = runner.invoke(app, ["user", "get"])
    assert result.exit_code == 0
    assert "Jane Doe" in result.output


def test_update_user_command():
    """Test update user CLI command."""
    runner = CliRunner()

    # First create a user
    runner.invoke(app, ["user", "create", "John Doe", "john@example.com"])

    result = runner.invoke(app, ["user", "update", "--name", "Jane Doe", "--timezone", "EST"])
    assert result.exit_code == 0
    assert "User updated successfully" in result.output


def test_delete_user_command():
    """Test delete user CLI command."""
    runner = CliRunner()

    # First create a user
    runner.invoke(app, ["user", "create", "John Doe", "john@example.com"])

    result = runner.invoke(app, ["user", "delete"])
    assert result.exit_code == 0
    assert "User deleted successfully" in result.output