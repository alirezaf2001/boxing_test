"""Report API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from taskforge.api.dependencies import get_db
from taskforge.services.report_service import ReportService

router = APIRouter()


@router.get("/daily")
def get_daily_summary(date: str = None, db: Session = Depends(get_db)):
    """Get daily task summary."""
    try:
        report_service = ReportService(db)
        return report_service.generate_daily_summary(date=date)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/weekly")
def get_weekly_summary(end_date: str = None, db: Session = Depends(get_db)):
    """Get weekly productivity summary."""
    try:
        report_service = ReportService(db)
        return report_service.generate_weekly_summary(end_date=end_date)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/project/{project_id}")
def get_project_report(project_id: int, db: Session = Depends(get_db)):
    """Get project progress report."""
    try:
        report_service = ReportService(db)
        return report_service.generate_project_report(project_id=project_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/overdue")
def get_overdue_report(db: Session = Depends(get_db)):
    """Get overdue tasks report."""
    try:
        report_service = ReportService(db)
        return report_service.generate_overdue_report()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/export/{report_type}")
def export_report(
    report_type: str,
    format: str = "json",
    project_id: int = None,
    date: str = None,
    db: Session = Depends(get_db)
):
    """Export report to file."""
    try:
        report_service = ReportService(db)

        if report_type == "daily":
            data = report_service.generate_daily_summary(date=date)
        elif report_type == "weekly":
            data = report_service.generate_weekly_summary(end_date=date)
        elif report_type == "project":
            if not project_id:
                raise HTTPException(status_code=400, detail="Project ID required for project reports")
            data = report_service.generate_project_report(project_id=project_id)
        elif report_type == "overdue":
            data = report_service.generate_overdue_report()
        else:
            raise HTTPException(status_code=400, detail=f"Unknown report type: {report_type}")

        if format == "json":
            from taskforge.exporters.json_exporter import JSONExporter
            exporter = JSONExporter()
        elif format == "csv":
            from taskforge.exporters.csv_exporter import CSVExporter
            exporter = CSVExporter()
        else:
            raise HTTPException(status_code=400, detail=f"Unknown format: {format}")

        file_path = exporter.export(data)
        return {"file_path": file_path, "message": f"Report exported to {file_path}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))