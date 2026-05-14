"""Report schemas."""

from typing import Any, Dict

from pydantic import BaseModel


class ReportResponse(BaseModel):
    """Schema for report response."""
    report_type: str
    data: Dict[str, Any]
    generated_at: str