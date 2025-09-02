"""
Temporal generators for SynGen.

This module provides generators for temporal data types
such as dates and datetimes.
"""

import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, Any


class TemporalGenerator:
    """Generator for temporal data types."""

    def __init__(self):
        """Initialize the temporal generator."""
        pass

    def generate_dates(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate dates."""
        dates = []

        start_date = parameters.get("start_date", datetime(2020, 1, 1))
        end_date = parameters.get("end_date", datetime(2024, 12, 31))

        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)

        # Convert to date objects
        start_date = start_date.date()
        end_date = end_date.date()

        # Calculate date range
        date_range = (end_date - start_date).days

        for _ in range(n_samples):
            # Generate random days offset
            days_offset = random.randint(0, date_range)
            random_date = start_date + timedelta(days=days_offset)

            # Format date
            format_str = parameters.get("format", "%Y-%m-%d")
            date_str = random_date.strftime(format_str)
            dates.append(date_str)

        return np.array(dates)

    def generate_datetimes(
        self, parameters: Dict[str, Any], n_samples: int
    ) -> np.ndarray:
        """Generate datetimes."""
        datetimes = []

        start_datetime = parameters.get("start_datetime", datetime(2020, 1, 1))
        end_datetime = parameters.get("end_datetime", datetime(2024, 12, 31))

        if isinstance(start_datetime, str):
            start_datetime = datetime.fromisoformat(start_datetime)
        if isinstance(end_datetime, str):
            end_datetime = datetime.fromisoformat(end_datetime)

        # Calculate time range in seconds
        time_range = (end_datetime - start_datetime).total_seconds()

        for _ in range(n_samples):
            # Generate random seconds offset
            seconds_offset = random.randint(0, int(time_range))
            random_datetime = start_datetime + timedelta(seconds=seconds_offset)

            # Format datetime
            format_str = parameters.get("format", "%Y-%m-%d %H:%M:%S")
            datetime_str = random_datetime.strftime(format_str)
            datetimes.append(datetime_str)

        return np.array(datetimes)
