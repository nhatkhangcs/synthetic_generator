"""
Main data generator class for SynGen.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from ..schemas import DataSchema, ColumnSchema, DataType, DistributionType
from .distributions import DistributionGenerator
from .correlations import CorrelationManager
from .constraints import ConstraintManager


class DataGenerator:
    """Main class for generating synthetic data based on a schema."""

    def __init__(
        self, schema: DataSchema, constraints: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the data generator.

        Args:
            schema: Data schema defining the structure
            constraints: Additional constraints for data generation
        """
        self.schema = schema
        self.constraints = constraints or {}
        self.distribution_generator = DistributionGenerator()
        self.correlation_manager = CorrelationManager()
        self.constraint_manager = ConstraintManager()

        # Validate schema
        errors = schema.validate()
        if errors:
            raise ValueError(f"Invalid schema: {errors}")

    def generate(self, n_samples: int, seed: Optional[int] = None) -> pd.DataFrame:
        """
        Generate synthetic data.

        Args:
            n_samples: Number of samples to generate
            seed: Random seed for reproducibility

        Returns:
            DataFrame with synthetic data
        """
        if seed is not None:
            np.random.seed(seed)

        # Sort columns by dependencies
        ordered_columns = self._topological_sort()

        # Generate data for each column
        data = {}

        for column in ordered_columns:
            # Generate base data
            column_data = self._generate_column_data(column, n_samples, data)

            # Apply constraints
            column_data = self.constraint_manager.apply_constraints(
                column_data, column, self.constraints
            )

            data[column.name] = column_data

        # Create DataFrame
        df = pd.DataFrame(data)

        # Apply correlations if specified
        if self.schema.correlations:
            df = self.correlation_manager.apply_correlations(
                df, self.schema.correlations
            )

        # Apply global constraints
        df = self.constraint_manager.apply_global_constraints(
            df, self.schema.constraints
        )

        return df

    def _topological_sort(self) -> List[ColumnSchema]:
        """Sort columns by dependencies to ensure proper generation order."""
        columns = {col.name: col for col in self.schema.columns}
        visited = set()
        temp_visited = set()
        result = []

        def visit(column_name: str):
            if column_name in temp_visited:
                raise ValueError(f"Circular dependency detected: {column_name}")
            if column_name in visited:
                return

            temp_visited.add(column_name)
            column = columns[column_name]

            if column.depends_on:
                for dep in column.depends_on:
                    visit(dep)

            temp_visited.remove(column_name)
            visited.add(column_name)
            result.append(column)

        for column in self.schema.columns:
            if column.name not in visited:
                visit(column.name)

        return result

    def _generate_column_data(
        self, column: ColumnSchema, n_samples: int, existing_data: Dict[str, pd.Series]
    ) -> pd.Series:
        """Generate data for a single column."""

        # Handle dependencies
        if column.depends_on:
            return self._generate_dependent_data(column, n_samples, existing_data)

        # Generate base data based on distribution
        base_data = self.distribution_generator.generate(
            column.distribution, column.data_type, column.parameters, n_samples
        )

        # Apply data type conversion first
        base_data = self._apply_data_type(base_data, column.data_type)

        # Apply null values AFTER data type conversion using pandas Series
        if column.nullable and column.null_probability > 0:
            null_mask = np.random.random(n_samples) < column.null_probability
            # Convert to pandas Series to properly handle null values
            base_data = pd.Series(base_data)
            base_data[null_mask] = None
            base_data = base_data.values

        # Apply value constraints
        if column.min_value is not None or column.max_value is not None:
            base_data = self._apply_value_constraints(base_data, column)

        # Apply uniqueness constraint
        if column.unique:
            base_data = self._ensure_uniqueness(base_data)

        return pd.Series(base_data, name=column.name)

    def _generate_dependent_data(
        self, column: ColumnSchema, n_samples: int, existing_data: Dict[str, pd.Series]
    ) -> pd.Series:
        """Generate data for columns that depend on other columns."""

        if not column.depends_on:
            raise ValueError(f"Column {column.name} has no dependencies")

        # Get dependent columns data
        dep_data = {dep: existing_data[dep] for dep in column.depends_on}

        # Apply conditional rules
        if column.conditional_rules:
            return self._apply_conditional_rules(column, dep_data, n_samples)

        # Default: generate based on distribution but with dependency awareness
        base_data = self.distribution_generator.generate(
            column.distribution, column.data_type, column.parameters, n_samples
        )

        # Apply data type conversion
        base_data = self._apply_data_type(base_data, column.data_type)

        return pd.Series(base_data, name=column.name)

    def _apply_conditional_rules(
        self, column: ColumnSchema, dep_data: Dict[str, pd.Series], n_samples: int
    ) -> pd.Series:
        """Apply conditional rules for dependent data generation."""

        rules = column.conditional_rules
        result = np.empty(n_samples, dtype=object)

        for i in range(n_samples):
            # Evaluate conditions for this sample
            condition_met = False

            for rule in rules.get("rules", []):
                condition = rule.get("condition", {})
                value = rule.get("value")

                # Check if condition is met
                if self._evaluate_condition(condition, dep_data, i):
                    result[i] = value
                    condition_met = True
                    break

            # Use default value if no condition met
            if not condition_met:
                result[i] = rules.get("default", None)

        return pd.Series(result, name=column.name)

    def _evaluate_condition(
        self, condition: Dict[str, Any], dep_data: Dict[str, pd.Series], index: int
    ) -> bool:
        """Evaluate a condition for a specific sample."""

        for dep_col, cond in condition.items():
            if dep_col not in dep_data:
                continue

            value = dep_data[dep_col].iloc[index]
            operator = cond.get("operator", "==")
            target = cond.get("value")

            if operator == "==":
                if value != target:
                    return False
            elif operator == "!=":
                if value == target:
                    return False
            elif operator == ">":
                if value <= target:
                    return False
            elif operator == "<":
                if value >= target:
                    return False
            elif operator == ">=":
                if value < target:
                    return False
            elif operator == "<=":
                if value > target:
                    return False
            elif operator == "in":
                if value not in target:
                    return False
            elif operator == "not_in":
                if value in target:
                    return False

        return True

    def _apply_data_type(self, data: np.ndarray, data_type: DataType) -> np.ndarray:
        """Apply data type conversion."""

        if data_type == DataType.INTEGER:
            # Handle NaN values for integer conversion
            if np.any(np.isnan(data)):
                # Convert to float first to handle NaN, then convert to nullable integer
                return data.astype(float)
            else:
                return data.astype(int)
        elif data_type == DataType.FLOAT:
            return data.astype(float)
        elif data_type == DataType.BOOLEAN:
            # Handle NaN values for boolean conversion
            if np.any(np.isnan(data)):
                return data.astype(float)  # Use float to preserve NaN
            else:
                return data.astype(bool)
        elif data_type == DataType.STRING:
            return data.astype(str)
        elif data_type in [
            DataType.EMAIL,
            DataType.ADDRESS,
            DataType.NAME,
            DataType.PHONE,
        ]:
            # For specialized text types, we need to generate proper data
            # The distribution generator should have already called the text generator
            return data.astype(str)
        else:
            return data

    def _apply_value_constraints(
        self, data: np.ndarray, column: ColumnSchema
    ) -> np.ndarray:
        """Apply min/max value constraints."""

        if column.min_value is not None:
            data = np.maximum(data, column.min_value)

        if column.max_value is not None:
            data = np.minimum(data, column.max_value)

        return data

    def _ensure_uniqueness(self, data: np.ndarray) -> np.ndarray:
        """Ensure unique values in the data."""

        unique_data = np.unique(data)
        if len(unique_data) < len(data):
            # Generate additional unique values
            additional_needed = len(data) - len(unique_data)

            if additional_needed <= len(unique_data):
                # We can sample without replacement
                additional_values = np.random.choice(
                    unique_data, size=additional_needed, replace=False
                )
            else:
                # We need more values than available, so sample with replacement
                # and add some variation
                additional_values = np.random.choice(
                    unique_data, size=additional_needed, replace=True
                )

                # Add some variation to make them more unique
                if hasattr(
                    additional_values[0], "dtype"
                ) and additional_values.dtype in [
                    "int64",
                    "int32",
                    "float64",
                    "float32",
                ]:
                    # For numeric data, add small random offsets
                    variation = np.random.normal(0, 0.1, additional_needed)
                    additional_values = additional_values + variation
                else:
                    # For string data, append numbers
                    additional_values = [
                        f"{val}_{i}" for i, val in enumerate(additional_values)
                    ]

            data = np.concatenate([unique_data, additional_values])

        # Shuffle to randomize order
        np.random.shuffle(data)
        return data
