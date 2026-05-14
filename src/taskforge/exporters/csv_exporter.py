"""CSV exporter."""

import csv
from pathlib import Path
from typing import Any, Dict, List


class CSVExporter:
    """Exporter for CSV format."""

    def export(self, data: Any, filename: str = None) -> str:
        """Export data to CSV file."""
        if not filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"taskforge_export_{timestamp}.csv"

        file_path = Path(filename)

        # Handle different data structures
        if isinstance(data, dict):
            self._export_dict_to_csv(data, file_path)
        elif isinstance(data, list):
            self._export_list_to_csv(data, file_path)
        else:
            # Convert to dict
            self._export_dict_to_csv({"data": data}, file_path)

        return str(file_path)

    def _export_dict_to_csv(self, data: Dict[str, Any], file_path: Path) -> None:
        """Export dictionary to CSV."""
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for key, value in data.items():
                writer.writerow([key, str(value)])

    def _export_list_to_csv(self, data: List[Any], file_path: Path) -> None:
        """Export list to CSV."""
        if not data:
            return

        # Get fieldnames from first item if it's a dict
        if isinstance(data[0], dict):
            fieldnames = list(data[0].keys())
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow({k: str(v) for k, v in row.items()})
        else:
            # Simple list
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for item in data:
                    writer.writerow([str(item)])