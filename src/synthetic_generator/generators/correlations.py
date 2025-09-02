"""
Correlation manager for SynGen.

This module provides functionality to handle correlations
between variables in synthetic data generation.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


class CorrelationManager:
    """Manager for handling correlations between variables."""

    def __init__(self):
        """Initialize the correlation manager."""
        pass

    def apply_correlations(
        self, df: pd.DataFrame, correlations: Dict[str, Dict[str, float]]
    ) -> pd.DataFrame:
        """
        Apply correlations to the DataFrame.

        Args:
            df: Input DataFrame
            correlations: Dictionary of correlation specifications

        Returns:
            DataFrame with applied correlations
        """
        if not correlations:
            return df

        # Get numeric columns only
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

        # Convert DataFrame to numpy array for easier manipulation
        data = df.values
        columns = df.columns.tolist()

        # Apply correlations only for numeric columns
        for col1, corr_dict in correlations.items():
            if col1 not in columns or col1 not in numeric_columns:
                continue

            col1_idx = columns.index(col1)

            for col2, target_corr in corr_dict.items():
                if col2 not in columns or col2 not in numeric_columns or col1 == col2:
                    continue

                col2_idx = columns.index(col2)

                # Apply correlation
                data = self._apply_correlation(data, col1_idx, col2_idx, target_corr)

        # Convert back to DataFrame
        return pd.DataFrame(data, columns=columns)

    def _apply_correlation(
        self, data: np.ndarray, col1_idx: int, col2_idx: int, target_corr: float
    ) -> np.ndarray:
        """
        Apply correlation between two columns.

        Args:
            data: Data array
            col1_idx: Index of first column
            col2_idx: Index of second column
            target_corr: Target correlation coefficient

        Returns:
            Modified data array
        """
        # Check if both columns are numeric
        col1_data = data[:, col1_idx]
        col2_data = data[:, col2_idx]

        # Convert to numeric if possible, skip if not
        try:
            col1_numeric = pd.to_numeric(col1_data, errors="coerce")
            col2_numeric = pd.to_numeric(col2_data, errors="coerce")

            # Check if we have enough numeric data
            if (
                pd.isna(col1_numeric).sum() > len(col1_numeric) * 0.5
                or pd.isna(col2_numeric).sum() > len(col2_numeric) * 0.5
            ):
                return data  # Skip correlation if too much non-numeric data

            # Get current correlation
            current_corr = np.corrcoef(col1_numeric, col2_numeric)[0, 1]

            if np.isnan(current_corr):
                return data

            # Calculate adjustment factor
            if abs(current_corr) < 1e-6:
                # No current correlation, create one
                adjustment = target_corr
            else:
                # Adjust existing correlation
                adjustment = target_corr / current_corr

            # Apply adjustment to second column
            mean_col2 = np.mean(col2_numeric)
            adjusted_col2 = mean_col2 + adjustment * (col2_numeric - mean_col2)

            # Update the data array
            data[:, col2_idx] = adjusted_col2

        except (ValueError, TypeError):
            # If conversion fails, skip correlation
            pass

        return data

    def calculate_correlations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate correlation matrix for the DataFrame.

        Args:
            df: Input DataFrame

        Returns:
            Correlation matrix
        """
        return df.corr()

    def validate_correlations(
        self, df: pd.DataFrame, target_correlations: Dict[str, Dict[str, float]]
    ) -> Dict[str, Any]:
        """
        Validate that target correlations are achieved.

        Args:
            df: Generated DataFrame
            target_correlations: Target correlation specifications

        Returns:
            Validation results
        """
        results = {"valid": True, "errors": [], "warnings": [], "correlations": {}}

        actual_corr_matrix = self.calculate_correlations(df)

        for col1, corr_dict in target_correlations.items():
            if col1 not in df.columns:
                results["errors"].append(f"Column {col1} not found in data")
                results["valid"] = False
                continue

            for col2, target_corr in corr_dict.items():
                if col2 not in df.columns:
                    results["errors"].append(f"Column {col2} not found in data")
                    results["valid"] = False
                    continue

                actual_corr = actual_corr_matrix.loc[col1, col2]

                # Check if correlation is within acceptable range
                tolerance = 0.1  # 10% tolerance
                if abs(actual_corr - target_corr) > tolerance:
                    results["warnings"].append(
                        f"Correlation between {col1} and {col2}: "
                        f"target={target_corr:.3f}, actual={actual_corr:.3f}"
                    )

                results["correlations"][f"{col1}_{col2}"] = {
                    "target": target_corr,
                    "actual": actual_corr,
                    "difference": abs(actual_corr - target_corr),
                }

        return results
