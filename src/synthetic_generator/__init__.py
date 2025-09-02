"""
Synthetic Generator - A comprehensive Python library for generating synthetic data.

This library provides tools for creating realistic synthetic datasets with various
distributions, correlations, and constraints for machine learning and data science applications.
"""

from typing import Optional, Dict, Any
import pandas as pd

__version__ = "0.0.8"

# Core imports
from .schemas import DataSchema, ColumnSchema, DataType, DistributionType
from .generators.base import DataGenerator
from .schemas.inference import infer_schema_from_data
from .schemas.templates import load_template_schema


# Main function
def generate_data(
    schema: DataSchema, n_samples: int = 1000, seed: Optional[int] = None
) -> pd.DataFrame:
    """Generate synthetic data based on a schema."""
    generator = DataGenerator(schema)
    return generator.generate(n_samples, seed)


# Convenience functions
def infer_schema(data: pd.DataFrame, sample_size: Optional[int] = None) -> DataSchema:
    """Infer schema from existing data."""
    return infer_schema_from_data(data, sample_size)


def load_template(name: str) -> DataSchema:
    """Load a pre-built template schema."""
    return load_template_schema(name)


def validate_data(data: pd.DataFrame, schema: DataSchema) -> Dict[str, Any]:
    """Validate generated data against a schema."""
    return schema.validate_data(data)
