"""
Constraint manager for SynGen.

This module provides functionality to handle constraints
and validation in synthetic data generation.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from ..schemas import ColumnSchema


class ConstraintManager:
    """Manager for handling constraints and validation."""

    def __init__(self):
        """Initialize the constraint manager."""
        pass

    def apply_constraints(
        self, data: pd.Series, column: ColumnSchema, global_constraints: Dict[str, Any]
    ) -> pd.Series:
        """
        Apply constraints to a column.

        Args:
            data: Column data
            column: Column schema
            global_constraints: Global constraints

        Returns:
            Constrained data
        """
        # Apply column-specific constraints
        if column.min_value is not None:
            data = data.clip(lower=column.min_value)

        if column.max_value is not None:
            data = data.clip(upper=column.max_value)

        # Apply uniqueness constraint
        if column.unique:
            data = self._ensure_uniqueness(data)

        # Apply pattern constraints
        if column.pattern:
            data = self._apply_pattern_constraint(data, column.pattern)

        # Apply global constraints
        if global_constraints:
            data = self._apply_global_constraints(data, column.name, global_constraints)

        return data

    def apply_global_constraints(
        self, df: pd.DataFrame, constraints: Optional[Dict[str, Any]]
    ) -> pd.DataFrame:
        """
        Apply global constraints to the entire DataFrame.

        Args:
            df: Input DataFrame
            constraints: Global constraints

        Returns:
            Constrained DataFrame
        """
        if not constraints:
            return df

        # Apply row-level constraints
        if "row_constraints" in constraints:
            df = self._apply_row_constraints(df, constraints["row_constraints"])

        # Apply cross-column constraints
        if "cross_column_constraints" in constraints:
            df = self._apply_cross_column_constraints(
                df, constraints["cross_column_constraints"]
            )

        # Apply data quality constraints
        if "quality_constraints" in constraints:
            df = self._apply_quality_constraints(df, constraints["quality_constraints"])

        return df

    def _ensure_uniqueness(self, data: pd.Series) -> pd.Series:
        """Ensure unique values in the data."""
        unique_values = data.unique()

        if len(unique_values) < len(data):
            # Generate additional unique values
            additional_needed = len(data) - len(unique_values)

            if hasattr(data.iloc[0], "dtype"):
                # Numeric data
                min_val = data.min()
                max_val = data.max()
                additional_values = np.random.uniform(
                    min_val, max_val, additional_needed
                )
            else:
                # String data
                additional_values = [f"unique_{i}" for i in range(additional_needed)]

            # Combine and shuffle
            all_values = np.concatenate([unique_values, additional_values])
            np.random.shuffle(all_values)

            return pd.Series(all_values[: len(data)], index=data.index, name=data.name)

        return data

    def _apply_pattern_constraint(self, data: pd.Series, pattern: str) -> pd.Series:
        """Apply pattern constraint to string data."""
        import re

        # For now, just validate the pattern
        # In a full implementation, you might want to generate data that matches the pattern
        if data.dtype == "object":
            # Check if all values match the pattern
            for value in data:
                if pd.notna(value) and not re.match(pattern, str(value)):
                    # Replace with a default value or generate a matching value
                    pass

        return data

    def _apply_global_constraints(
        self, data: pd.Series, column_name: str, constraints: Dict[str, Any]
    ) -> pd.Series:
        """Apply global constraints to a column."""

        # Apply column-specific global constraints
        if column_name in constraints:
            col_constraints = constraints[column_name]

            # Apply value range constraints
            if "min_value" in col_constraints:
                data = data.clip(lower=col_constraints["min_value"])

            if "max_value" in col_constraints:
                data = data.clip(upper=col_constraints["max_value"])

            # Apply value set constraints
            if "allowed_values" in col_constraints:
                allowed_values = col_constraints["allowed_values"]
                data = data.apply(
                    lambda x: (
                        x if x in allowed_values else np.random.choice(allowed_values)
                    )
                )

        return data

    def _apply_row_constraints(
        self, df: pd.DataFrame, row_constraints: Dict[str, Any]
    ) -> pd.DataFrame:
        """Apply row-level constraints."""

        for constraint in row_constraints:
            condition = constraint.get("condition", {})
            action = constraint.get("action", "drop")

            # Apply condition
            mask = self._evaluate_row_condition(df, condition)

            if action == "drop":
                df = df[~mask]
            elif action == "modify":
                modification = constraint.get("modification", {})
                df = self._apply_row_modification(df, mask, modification)

        return df

    def _apply_cross_column_constraints(
        self, df: pd.DataFrame, cross_constraints: Dict[str, Any]
    ) -> pd.DataFrame:
        """Apply cross-column constraints."""

        for constraint in cross_constraints:
            condition = constraint.get("condition", {})
            action = constraint.get("action", "modify")

            # Apply condition
            mask = self._evaluate_cross_column_condition(df, condition)

            if action == "modify":
                modification = constraint.get("modification", {})
                df = self._apply_cross_column_modification(df, mask, modification)

        return df

    def _apply_quality_constraints(
        self, df: pd.DataFrame, quality_constraints: Dict[str, Any]
    ) -> pd.DataFrame:
        """Apply data quality constraints."""

        # Apply missing value constraints
        if "max_missing_ratio" in quality_constraints:
            max_ratio = quality_constraints["max_missing_ratio"]
            for col in df.columns:
                missing_ratio = df[col].isnull().mean()
                if missing_ratio > max_ratio:
                    # Reduce missing values
                    n_missing = int(len(df) * max_ratio)
                    missing_indices = df[col].isnull().nlargest(n_missing).index
                    df.loc[missing_indices, col] = df[col].median()  # Fill with median

        # Apply outlier constraints
        if "max_outlier_ratio" in quality_constraints:
            max_ratio = quality_constraints["max_outlier_ratio"]
            for col in df.select_dtypes(include=[np.number]).columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
                outlier_ratio = outliers.mean()

                if outlier_ratio > max_ratio:
                    # Reduce outliers
                    n_outliers = int(len(df) * max_ratio)
                    outlier_indices = outliers.nlargest(n_outliers).index
                    df.loc[outlier_indices, col] = df[col].median()

        return df

    def _evaluate_row_condition(
        self, df: pd.DataFrame, condition: Dict[str, Any]
    ) -> pd.Series:
        """Evaluate a row-level condition."""
        mask = pd.Series(True, index=df.index)

        for col, cond in condition.items():
            if col not in df.columns:
                continue

            operator = cond.get("operator", "==")
            value = cond.get("value")

            if operator == "==":
                mask &= df[col] == value
            elif operator == "!=":
                mask &= df[col] != value
            elif operator == ">":
                mask &= df[col] > value
            elif operator == "<":
                mask &= df[col] < value
            elif operator == ">=":
                mask &= df[col] >= value
            elif operator == "<=":
                mask &= df[col] <= value
            elif operator == "in":
                mask &= df[col].isin(value)
            elif operator == "not_in":
                mask &= ~df[col].isin(value)

        return mask

    def _evaluate_cross_column_condition(
        self, df: pd.DataFrame, condition: Dict[str, Any]
    ) -> pd.Series:
        """Evaluate a cross-column condition."""
        mask = pd.Series(True, index=df.index)

        # Example: col1 > col2
        if "comparison" in condition:
            comp = condition["comparison"]
            col1 = comp.get("column1")
            col2 = comp.get("column2")
            operator = comp.get("operator", ">")

            if col1 in df.columns and col2 in df.columns:
                if operator == ">":
                    mask &= df[col1] > df[col2]
                elif operator == "<":
                    mask &= df[col1] < df[col2]
                elif operator == ">=":
                    mask &= df[col1] >= df[col2]
                elif operator == "<=":
                    mask &= df[col1] <= df[col2]
                elif operator == "==":
                    mask &= df[col1] == df[col2]
                elif operator == "!=":
                    mask &= df[col1] != df[col2]

        return mask

    def _apply_row_modification(
        self, df: pd.DataFrame, mask: pd.Series, modification: Dict[str, Any]
    ) -> pd.DataFrame:
        """Apply row modification."""
        df_copy = df.copy()

        for col, value in modification.items():
            if col in df.columns:
                df_copy.loc[mask, col] = value

        return df_copy

    def _apply_cross_column_modification(
        self, df: pd.DataFrame, mask: pd.Series, modification: Dict[str, Any]
    ) -> pd.DataFrame:
        """Apply cross-column modification."""
        df_copy = df.copy()

        for col, rule in modification.items():
            if col in df.columns:
                if rule.get("type") == "function":
                    # Apply a function to the column
                    func_name = rule.get("function")
                    if func_name == "mean":
                        df_copy.loc[mask, col] = df[col].mean()
                    elif func_name == "median":
                        df_copy.loc[mask, col] = df[col].median()
                    elif func_name == "mode":
                        df_copy.loc[mask, col] = (
                            df[col].mode().iloc[0]
                            if not df[col].mode().empty
                            else df[col].median()
                        )

        return df_copy
