"""CLI tests for project commands."""

from typer.testing import CliRunner

from taskforge.cli.main import app


def test_create_project_command():
    """Test create project CLI command."""
    runner = CliRunner()
    result = runner.invoke(app, ["project", "create", "Test Project", "--description", "A test project"])
    assert result.exit_code == 0
    assert "Project created successfully" in result.output


def test_list_projects_command():
    """Test list projects CLI command."""
    runner = CliRunner()

    # Create some projects
    runner.invoke(app, ["project", "create", "Project 1"])
    runner.invoke(app, ["project", "create", "Project 2"])

    result = runner.invoke(app, ["project", "list"])
    assert result.exit_code == 0
    assert "Project 1" in result.output
    assert "Project 2" in result.output


def test_get_project_command():
    """Test get project CLI command."""
    runner = CliRunner()

    # Create a project
    runner.invoke(app, ["project", "create", "Test Project"])

    result = runner.invoke(app, ["project", "get", "1"])
    assert result.exit_code == 0
    assert "Test Project" in result.output


def test_update_project_command():
    """Test update project CLI command."""
    runner = CliRunner()

    # Create a project
    runner.invoke(app, ["project", "create", "Old Name"])

    result = runner.invoke(app, ["project", "update", "1", "--name", "New Name"])
    assert result.exit_code == 0
    assert "Project updated successfully" in result.output


def test_archive_project_command():
    """Test archive project CLI command."""
    runner = CliRunner()

    # Create a project
    runner.invoke(app, ["project", "create", "Test Project"])

    result = runner.invoke(app, ["project", "archive", "1"])
    assert result.exit_code == 0
    assert "Project archived successfully" in result.output


def test_delete_project_command():
    """Test delete project CLI command."""
    runner = CliRunner()

    # Create a project
    runner.invoke(app, ["project", "create", "Test Project"])

    result = runner.invoke(app, ["project", "delete", "1"])
    assert result.exit_code == 0
    assert "Project deleted successfully" in result.output