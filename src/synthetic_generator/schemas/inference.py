"""
Schema inference for SynGen.

This module provides functionality to automatically infer
data schemas from existing data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from .base import DataSchema, ColumnSchema, DataType, DistributionType


class SchemaInferrer:
    """Class for inferring data schemas from existing data."""

    @staticmethod
    def infer(data: pd.DataFrame, sample_size: Optional[int] = None) -> DataSchema:
        """
        Infer schema from existing data.

        Args:
            data: Input DataFrame
            sample_size: Number of samples to use for inference

        Returns:
            Inferred data schema
        """
        # Sample data if specified
        if sample_size and sample_size < len(data):
            data = data.sample(n=sample_size, random_state=42)

        columns = []

        for col_name in data.columns:
            col_data = data[col_name]
            column_schema = SchemaInferrer._infer_column_schema(col_name, col_data)
            columns.append(column_schema)

        return DataSchema(columns=columns)

    @staticmethod
    def _infer_column_schema(column_name: str, column_data: pd.Series) -> ColumnSchema:
        """Infer schema for a single column."""

        # Determine data type
        data_type = SchemaInferrer._infer_data_type(column_data)

        # Use default distribution without any data analysis
        distribution, parameters = SchemaInferrer._get_default_distribution_no_inference(data_type)

        # Determine constraints
        constraints = SchemaInferrer._infer_constraints(column_data, data_type)

        return ColumnSchema(
            name=column_name,
            data_type=data_type,
            distribution=distribution,
            parameters=parameters,
            **constraints,
        )

    @staticmethod
    def _infer_data_type(column_data: pd.Series) -> DataType:
        """Infer data type from column data."""

        # Handle missing values
        non_null_data = column_data.dropna()

        if len(non_null_data) == 0:
            return DataType.STRING

        # Check for boolean first (before numeric)
        if pd.api.types.is_bool_dtype(column_data):
            return DataType.BOOLEAN

        # Check for numeric types
        if pd.api.types.is_numeric_dtype(column_data):
            if pd.api.types.is_integer_dtype(column_data):
                return DataType.INTEGER
            else:
                return DataType.FLOAT

        # Check for datetime
        if pd.api.types.is_datetime64_any_dtype(column_data):
            return DataType.DATETIME

        # Check for date (simplified check)
        try:
            # Try to convert to datetime to see if it's a date
            pd.to_datetime(column_data.iloc[0])
            return DataType.DATE
        except:
            pass

        # Check for specific text patterns
        sample_values = non_null_data.head(100).astype(str)

        # Check for email pattern
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if sample_values.str.match(email_pattern).mean() > 0.8:
            return DataType.EMAIL

        # Check for phone pattern
        phone_pattern = r"^[\+]?[1-9][\d]{0,15}$"
        if (
            sample_values.str.replace(r"[^\d+]", "", regex=True)
            .str.match(phone_pattern)
            .mean()
            > 0.8
        ):
            return DataType.PHONE

        # Check for address pattern (contains street, city, state, zip)
        address_indicators = ["street", "avenue", "road", "drive", "lane", "court"]
        if any(
            indicator in " ".join(sample_values).lower()
            for indicator in address_indicators
        ):
            return DataType.ADDRESS

        # Check for name pattern (first last format)
        name_pattern = r"^[A-Z][a-z]+ [A-Z][a-z]+$"
        if sample_values.str.match(name_pattern).mean() > 0.7:
            return DataType.NAME

        # Check for categorical
        unique_ratio = len(non_null_data.unique()) / len(non_null_data)
        if unique_ratio < 0.1:  # Less than 10% unique values
            return DataType.CATEGORICAL

        return DataType.STRING

    @staticmethod
    def _get_default_distribution_no_inference(data_type: DataType) -> tuple[DistributionType, Dict[str, Any]]:
        """Get default distribution without any data analysis or inference."""
        if data_type in [DataType.INTEGER, DataType.FLOAT]:
            return DistributionType.UNIFORM, {"low": 0.0, "high": 100.0}
        elif data_type == DataType.CATEGORICAL:
            return DistributionType.CATEGORICAL, {"categories": ["A", "B", "C"]}
        elif data_type == DataType.BOOLEAN:
            return DistributionType.CATEGORICAL, {"categories": [True, False]}
        else:
            # For all other data types (STRING, EMAIL, PHONE, etc.)
            return DistributionType.UNIFORM, {}



    @staticmethod
    def _infer_constraints(
        column_data: pd.Series, data_type: DataType
    ) -> Dict[str, Any]:
        """Infer constraints for a column."""
        constraints = {}

        non_null_data = column_data.dropna()

        if len(non_null_data) == 0:
            return constraints

        # Nullability
        null_count = column_data.isna().sum()
        constraints["nullable"] = bool(null_count > 0)
        if null_count > 0:
            constraints["null_probability"] = float(null_count / len(column_data))

        # Uniqueness
        constraints["unique"] = bool(len(non_null_data.unique()) == len(non_null_data))

        # Value constraints for numeric data
        if data_type in [DataType.INTEGER, DataType.FLOAT]:
            constraints["min_value"] = float(non_null_data.min())
            constraints["max_value"] = float(non_null_data.max())

        # Pattern constraints for text data
        if data_type in [
            DataType.STRING,
            DataType.EMAIL,
            DataType.PHONE,
            DataType.NAME,
            DataType.ADDRESS,
        ]:
            # Check for common patterns
            sample_values = non_null_data.head(100).astype(str)

            # Check if all values follow a pattern
            if data_type == DataType.EMAIL:
                email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                if sample_values.str.match(email_pattern).all():
                    constraints["pattern"] = email_pattern

            elif data_type == DataType.PHONE:
                phone_pattern = r"^[\+]?[1-9][\d]{0,15}$"
                if (
                    sample_values.str.replace(r"[^\d+]", "", regex=True)
                    .str.match(phone_pattern)
                    .all()
                ):
                    constraints["pattern"] = phone_pattern

        return constraints


def infer_schema_from_data(
    data: pd.DataFrame, sample_size: Optional[int] = None
) -> DataSchema:
    """Convenience function to infer schema from data."""
    return SchemaInferrer.infer(data, sample_size)
