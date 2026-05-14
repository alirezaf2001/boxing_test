"""JSON exporter."""

import json
from pathlib import Path
from typing import Any


class JSONExporter:
    """Exporter for JSON format."""

    def export(self, data: Any, filename: str = None) -> str:
        """Export data to JSON file."""
        if not filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"taskforge_export_{timestamp}.json"

        file_path = Path(filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

        return str(file_path)