"""
Data export functionality for SynGen.
"""

import pandas as pd
from typing import Dict, Any


class DataExporter:
    """Export data to various formats."""

    def export(self, data: pd.DataFrame, format_type: str, **kwargs):
        """Export data to specified format."""
        if format_type == "csv":
            return self._export_csv(data, **kwargs)
        elif format_type == "json":
            return self._export_json(data, **kwargs)
        elif format_type == "parquet":
            return self._export_parquet(data, **kwargs)
        elif format_type == "excel":
            return self._export_excel(data, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

    def _export_csv(self, data: pd.DataFrame, **kwargs):
        """Export to CSV format."""
        filepath = kwargs.pop("filepath", "synthetic_data.csv")
        return data.to_csv(filepath, index=False, **kwargs)

    def _export_json(self, data: pd.DataFrame, **kwargs):
        """Export to JSON format."""
        filepath = kwargs.pop("filepath", "synthetic_data.json")
        return data.to_json(filepath, orient="records", **kwargs)

    def _export_parquet(self, data: pd.DataFrame, **kwargs):
        """Export to Parquet format."""
        filepath = kwargs.pop("filepath", "synthetic_data.parquet")
        return data.to_parquet(filepath, index=False, **kwargs)

    def _export_excel(self, data: pd.DataFrame, **kwargs):
        """Export to Excel format."""
        filepath = kwargs.pop("filepath", "synthetic_data.xlsx")
        return data.to_excel(filepath, index=False, **kwargs)
