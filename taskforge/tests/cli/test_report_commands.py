"""CLI tests for report commands."""

from typer.testing import CliRunner

from taskforge.cli.main import app


def test_productivity_report_command():
    """Test productivity report CLI command."""
    runner = CliRunner()
    result = runner.invoke(app, ["report", "productivity"])
    assert result.exit_code == 0
    assert "Productivity Report" in result.output


def test_project_report_command():
    """Test project report CLI command."""
    runner = CliRunner()
    result = runner.invoke(app, ["report", "projects"])
    assert result.exit_code == 0
    assert "Project Report" in result.output


def test_task_report_command():
    """Test task report CLI command."""
    runner = CliRunner()
    result = runner.invoke(app, ["report", "tasks"])
    assert result.exit_code == 0
    assert "Task Report" in result.output


def test_export_productivity_report_command():
    """Test export productivity report CLI command."""
    runner = CliRunner()
    result = runner.invoke(app, ["report", "export-productivity", "--format", "json"])
    assert result.exit_code == 0
    assert "Report exported successfully" in result.output


def test_export_project_report_command():
    """Test export project report CLI command."""
    runner = CliRunner()
    result = runner.invoke(app, ["report", "export-projects", "--format", "json"])
    assert result.exit_code == 0
    assert "Report exported successfully" in result.output