"""
Base schema classes for SynGen data generation.
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
import pandas as pd
from enum import Enum


class DataType(Enum):
    """Supported data types for synthetic data generation."""

    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    CATEGORICAL = "categorical"
    EMAIL = "email"
    PHONE = "phone"
    ADDRESS = "address"
    NAME = "name"
    JSON = "json"


class DistributionType(Enum):
    """Supported distribution types."""

    NORMAL = "normal"
    UNIFORM = "uniform"
    EXPONENTIAL = "exponential"
    GAMMA = "gamma"
    BETA = "beta"
    WEIBULL = "weibull"
    POISSON = "poisson"
    BINOMIAL = "binomial"
    GEOMETRIC = "geometric"
    CATEGORICAL = "categorical"
    CONSTANT = "constant"


@dataclass
class ColumnSchema:
    """Schema definition for a single column."""

    name: str
    data_type: DataType
    distribution: DistributionType
    parameters: Dict[str, Any] = field(default_factory=dict)

    # Constraints
    min_value: Optional[Union[int, float, str]] = None
    max_value: Optional[Union[int, float, str]] = None
    unique: bool = False
    nullable: bool = True
    null_probability: float = 0.0

    # Formatting
    format_string: Optional[str] = None
    pattern: Optional[str] = None

    # Dependencies
    depends_on: Optional[List[str]] = None
    conditional_rules: Optional[Dict[str, Any]] = None

    def validate(self) -> List[str]:
        """Validate the column schema."""
        errors = []

        # Validate data type and distribution compatibility
        if self.data_type in [DataType.INTEGER, DataType.FLOAT]:
            if self.distribution not in [
                DistributionType.NORMAL,
                DistributionType.UNIFORM,
                DistributionType.EXPONENTIAL,
                DistributionType.GAMMA,
                DistributionType.BETA,
                DistributionType.WEIBULL,
                DistributionType.POISSON,
                DistributionType.BINOMIAL,
                DistributionType.GEOMETRIC,
                DistributionType.CONSTANT,
            ]:
                errors.append(
                    f"Distribution {self.distribution} not compatible with {self.data_type}"
                )

        elif self.data_type == DataType.CATEGORICAL:
            if self.distribution not in [
                DistributionType.CATEGORICAL,
                DistributionType.CONSTANT,
            ]:
                errors.append(
                    f"Distribution {self.distribution} not compatible with categorical data"
                )

        # Validate null probability
        if not 0 <= self.null_probability <= 1:
            errors.append("null_probability must be between 0 and 1")

        # NOTE: Do NOT strictly require distribution parameters at schema validation time.
        # Many schemas are inferred without exact statistical parameters. Parameter presence
        # will be validated (and defaulted) later in generator logic when sampling.
        # This intentionally relaxes checks for: NORMAL (mean/std), UNIFORM (low/high or dates),
        # and CATEGORICAL (categories), etc.

        return errors


@dataclass
class DataSchema:
    """Complete schema definition for synthetic data generation."""

    columns: List[ColumnSchema]
    correlations: Optional[Dict[str, Dict[str, float]]] = None
    constraints: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Validate schema after initialization."""
        errors = self.validate()
        if errors:
            raise ValueError(f"Schema validation failed: {errors}")

    def validate(self) -> List[str]:
        """Validate the complete schema."""
        errors = []

        # Validate individual columns
        column_names = set()
        for column in self.columns:
            if column.name in column_names:
                errors.append(f"Duplicate column name: {column.name}")
            column_names.add(column.name)

            column_errors = column.validate()
            errors.extend([f"{column.name}: {error}" for error in column_errors])

        # Validate dependencies
        for column in self.columns:
            if column.depends_on:
                for dep in column.depends_on:
                    if dep not in column_names:
                        errors.append(
                            f"Column {column.name} depends on undefined column {dep}"
                        )

        # Validate correlations
        if self.correlations:
            for col1, corr_dict in self.correlations.items():
                if col1 not in column_names:
                    errors.append(
                        f"Correlation matrix references undefined column: {col1}"
                    )
                for col2, corr_value in corr_dict.items():
                    if col2 not in column_names:
                        errors.append(
                            f"Correlation matrix references undefined column: {col2}"
                        )
                    if not -1 <= corr_value <= 1:
                        errors.append(
                            f"Correlation value must be between -1 and 1: {corr_value}"
                        )

        return errors

    def to_dict(self) -> Dict[str, Any]:
        """Convert schema to dictionary."""

        def convert_numpy_types(obj):
            """Convert numpy types to native Python types for JSON serialization."""
            import numpy as np

            if hasattr(obj, "item"):  # numpy scalar types
                return obj.item()
            elif isinstance(obj, np.bool_):  # numpy boolean
                return bool(obj)
            elif hasattr(obj, "dtype"):  # numpy arrays and other numpy types
                if obj.dtype.kind in ["b"]:  # boolean
                    return bool(obj)
                elif obj.dtype.kind in ["i", "u"]:  # integer
                    return int(obj)
                elif obj.dtype.kind in ["f"]:  # float
                    return float(obj)
                else:
                    return obj.tolist()
            elif isinstance(obj, (list, tuple)):
                return [convert_numpy_types(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: convert_numpy_types(value) for key, value in obj.items()}
            else:
                return obj

        return {
            "columns": [
                {
                    "name": col.name,
                    "data_type": col.data_type.value,
                    "distribution": col.distribution.value,
                    "parameters": convert_numpy_types(col.parameters),
                    "min_value": convert_numpy_types(col.min_value),
                    "max_value": convert_numpy_types(col.max_value),
                    "unique": col.unique,
                    "nullable": col.nullable,
                    "null_probability": convert_numpy_types(col.null_probability),
                    "format_string": col.format_string,
                    "pattern": col.pattern,
                    "depends_on": col.depends_on,
                    "conditional_rules": convert_numpy_types(col.conditional_rules),
                }
                for col in self.columns
            ],
            "correlations": convert_numpy_types(self.correlations),
            "constraints": convert_numpy_types(self.constraints),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataSchema":
        """Create schema from dictionary."""
        columns = []
        for col_data in data["columns"]:
            column = ColumnSchema(
                name=col_data["name"],
                data_type=DataType(col_data["data_type"].lower()),
                distribution=DistributionType(col_data["distribution"].lower()),
                parameters=col_data.get("parameters", {}),
                min_value=col_data.get("min_value"),
                max_value=col_data.get("max_value"),
                unique=col_data.get("unique", False),
                nullable=col_data.get("nullable", True),
                null_probability=col_data.get("null_probability", 0.0),
                format_string=col_data.get("format_string"),
                pattern=col_data.get("pattern"),
                depends_on=col_data.get("depends_on"),
                conditional_rules=col_data.get("conditional_rules"),
            )
            columns.append(column)

        return cls(
            columns=columns,
            correlations=data.get("correlations"),
            constraints=data.get("constraints"),
        )

    @classmethod
    def infer(
        cls, data: pd.DataFrame, sample_size: Optional[int] = None
    ) -> "DataSchema":
        """Infer schema from existing data."""
        from .inference import SchemaInferrer

        return SchemaInferrer.infer(data, sample_size)

    def validate_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Validate generated data against this schema."""
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "statistics": {},
            "checks_passed": 0,
            "total_checks": 0,
            "check_details": [],
        }

        # Check if all required columns exist
        schema_columns = {col.name for col in self.columns}
        data_columns = set(data.columns)

        missing_columns = schema_columns - data_columns
        extra_columns = data_columns - schema_columns

        # Add check details for basic checks
        if missing_columns:
            results["errors"].append(f"Missing columns: {missing_columns}")
            results["valid"] = False
            results["check_details"].append(
                {
                    "type": "basic",
                    "name": "Column existence validation",
                    "status": "failed",
                    "description": f"Missing required columns: {missing_columns}",
                }
            )
        else:
            results["check_details"].append(
                {
                    "type": "basic",
                    "name": "Column existence validation",
                    "status": "passed",
                    "description": "All required columns are present",
                }
            )

        if extra_columns:
            results["warnings"].append(f"Extra columns: {extra_columns}")
            results["check_details"].append(
                {
                    "type": "basic",
                    "name": "Extra columns check",
                    "status": "warning",
                    "description": f"Found extra columns: {extra_columns}",
                }
            )

        # Check data integrity
        if data.empty:
            results["errors"].append("Data is empty")
            results["valid"] = False
            results["check_details"].append(
                {
                    "type": "basic",
                    "name": "Data integrity check",
                    "status": "failed",
                    "description": "Data contains no rows",
                }
            )
        else:
            results["check_details"].append(
                {
                    "type": "basic",
                    "name": "Data integrity check",
                    "status": "passed",
                    "description": f"Data contains {len(data)} rows",
                }
            )

        # Validate each column
        for column in self.columns:
            if column.name not in data.columns:
                continue

            col_data = data[column.name]
            col_stats = {
                "null_count": col_data.isnull().sum(),
                "unique_count": col_data.nunique(),
                "total_rows": len(col_data),
                "min_value": (
                    col_data.min()
                    if col_data.dtype in ["int32", "float32", "int64", "float64"]
                    else None
                ),
                "max_value": (
                    col_data.max()
                    if col_data.dtype in ["int32", "float32", "int64", "float64"]
                    else None
                ),
            }
            results["statistics"][column.name] = col_stats

            # Check null probability
            actual_null_prob = col_data.isnull().mean()
            if abs(actual_null_prob - column.null_probability) > 0.1:
                warning_msg = f"Column {column.name}: Expected null probability {column.null_probability}, got {actual_null_prob:.3f}"
                results["warnings"].append(warning_msg)
                results["check_details"].append(
                    {
                        "type": "column",
                        "column": column.name,
                        "name": "Null probability validation",
                        "status": "warning",
                        "description": warning_msg,
                    }
                )
            else:
                results["check_details"].append(
                    {
                        "type": "column",
                        "column": column.name,
                        "name": "Null probability validation",
                        "status": "passed",
                        "description": f"Null probability {actual_null_prob:.3f} is within expected range",
                    }
                )

            # Check uniqueness constraint
            if column.unique and col_data.nunique() != len(col_data):
                error_msg = f"Column {column.name}: Expected unique values"
                results["errors"].append(error_msg)
                results["valid"] = False
                results["check_details"].append(
                    {
                        "type": "column",
                        "column": column.name,
                        "name": "Uniqueness constraint",
                        "status": "failed",
                        "description": error_msg,
                    }
                )
            elif column.unique:
                results["check_details"].append(
                    {
                        "type": "column",
                        "column": column.name,
                        "name": "Uniqueness constraint",
                        "status": "passed",
                        "description": "All values are unique as required",
                    }
                )

            # Check data type compatibility (basic check)

            type_warning = None

            if (
                column.data_type == DataType.INTEGER
                and not pd.api.types.is_integer_dtype(col_data)
            ):
                type_warning = f"Column {column.name}: Expected integer type"

            elif column.data_type == DataType.FLOAT and not pd.api.types.is_float_dtype(
                col_data
            ):
                type_warning = f"Column {column.name}: Expected float type"

            elif (
                column.data_type == DataType.STRING
                and not pd.api.types.is_string_dtype(col_data)
            ):
                type_warning = f"Column {column.name}: Expected string type"

            if type_warning:
                results["warnings"].append(type_warning)
                results["check_details"].append(
                    {
                        "type": "column",
                        "column": column.name,
                        "name": "Data type compatibility",
                        "status": "warning",
                        "description": type_warning,
                    }
                )
            else:
                results["check_details"].append(
                    {
                        "type": "column",
                        "column": column.name,
                        "name": "Data type compatibility",
                        "status": "passed",
                        "description": f"Data type {col_data.dtype} is compatible",
                    }
                )

        # Calculate checks passed and total checks based on actual check details
        total_checks = len(results["check_details"])
        checks_passed = len(
            [check for check in results["check_details"] if check["status"] == "passed"]
        )

        results["checks_passed"] = checks_passed
        results["total_checks"] = total_checks

        return results
