"""CLI commands for report generation."""

import typer

from taskforge.services.report_service import ReportService

app = typer.Typer()


@app.command()
def daily(date: str = typer.Option(None, "--date", help="Date for report (YYYY-MM-DD)")):
    """Generate daily task summary."""
    try:
        report_service = ReportService()
        report = report_service.generate_daily_summary(date=date)

        typer.echo("Daily Task Summary")
        typer.echo("==================")
        typer.echo(f"Date: {report['date']}")
        typer.echo(f"Total Tasks: {report['total_tasks']}")
        typer.echo(f"Completed: {report['completed_tasks']}")
        typer.echo(f"Pending: {report['pending_tasks']}")
        typer.echo(f"Overdue: {report['overdue_tasks']}")
    except Exception as e:
        typer.echo(f"Error generating daily report: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def weekly(date: str = typer.Option(None, "--date", help="End date for weekly report (YYYY-MM-DD)")):
    """Generate weekly productivity summary."""
    try:
        report_service = ReportService()
        report = report_service.generate_weekly_summary(end_date=date)

        typer.echo("Weekly Productivity Summary")
        typer.echo("===========================")
        typer.echo(f"Week: {report['week_start']} to {report['week_end']}")
        typer.echo(f"Total Tasks: {report['total_tasks']}")
        typer.echo(f"Completed: {report['completed_tasks']}")
        typer.echo(f"Completion Rate: {report['completion_rate']:.1f}%")
        typer.echo(f"Average per Day: {report['average_per_day']:.1f}")
    except Exception as e:
        typer.echo(f"Error generating weekly report: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def project(project_id: int = typer.Argument(..., help="Project ID")):
    """Generate project progress report."""
    try:
        report_service = ReportService()
        report = report_service.generate_project_report(project_id=project_id)

        typer.echo(f"Project Progress Report: {report['project_name']}")
        typer.echo("=" * (25 + len(report['project_name'])))
        typer.echo(f"Total Tasks: {report['total_tasks']}")
        typer.echo(f"Completed: {report['completed_tasks']}")
        typer.echo(f"Pending: {report['pending_tasks']}")
        typer.echo(f"Progress: {report['progress_percentage']:.1f}%")
        typer.echo(f"Overdue Tasks: {report['overdue_tasks']}")
    except Exception as e:
        typer.echo(f"Error generating project report: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def overdue():
    """Generate overdue tasks report."""
    try:
        report_service = ReportService()
        report = report_service.generate_overdue_report()

        typer.echo("Overdue Tasks Report")
        typer.echo("====================")
        typer.echo(f"Total Overdue: {len(report['overdue_tasks'])}")

        for task in report['overdue_tasks']:
            typer.echo(f"- {task['title']} (Due: {task['due_date']}, Priority: {task['priority']})")
    except Exception as e:
        typer.echo(f"Error generating overdue report: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def export(
    report_type: str = typer.Argument(..., help="Report type (daily/weekly/project/overdue)"),
    format: str = typer.Option("json", "--format", help="Export format (json/csv)"),
    output: str = typer.Option(None, "--output", help="Output file path"),
    project_id: int = typer.Option(None, "--project-id", help="Project ID for project reports"),
    date: str = typer.Option(None, "--date", help="Date for daily/weekly reports"),
):
    """Export report to file."""
    try:
        report_service = ReportService()

        if report_type == "daily":
            data = report_service.generate_daily_summary(date=date)
        elif report_type == "weekly":
            data = report_service.generate_weekly_summary(end_date=date)
        elif report_type == "project":
            if not project_id:
                typer.echo("Project ID required for project reports", err=True)
                raise typer.Exit(1)
            data = report_service.generate_project_report(project_id=project_id)
        elif report_type == "overdue":
            data = report_service.generate_overdue_report()
        else:
            typer.echo(f"Unknown report type: {report_type}", err=True)
            raise typer.Exit(1)

        if format == "json":
            from taskforge.exporters.json_exporter import JSONExporter
            exporter = JSONExporter()
        elif format == "csv":
            from taskforge.exporters.csv_exporter import CSVExporter
            exporter = CSVExporter()
        else:
            typer.echo(f"Unknown format: {format}", err=True)
            raise typer.Exit(1)

        file_path = exporter.export(data, output)
        typer.echo(f"Report exported to {file_path}")
    except Exception as e:
        typer.echo(f"Error exporting report: {e}", err=True)
        raise typer.Exit(1)