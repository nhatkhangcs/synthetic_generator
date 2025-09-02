"""
Quick API for Synthetic Generator.

Provides simplified, high-level functions for common data generation tasks.
"""

import pandas as pd
from typing import Union, Dict, Any, Optional
from .schemas import DataSchema
from .generators.base import DataGenerator
from .schemas.inference import infer_schema_from_data
from .schemas.templates import load_template_schema


class QuickModel:
    """A fitted model that can generate data."""

    def __init__(self, schema: DataSchema):
        self.schema = schema

    def sample(self, n_samples: int, seed: Optional[int] = None) -> pd.DataFrame:
        """Generate n_samples from the fitted model."""
        generator = DataGenerator(self.schema)
        return generator.generate(n_samples, seed)


def dataset(
    template: Optional[str] = None,
    schema: Optional[Union[Dict[str, Any], DataSchema]] = None,
    rows: int = 1000,
    seed: Optional[int] = None,
) -> pd.DataFrame:
    """
    Generate a dataset quickly from a template or schema.

    Args:
        template: Name of a pre-built template
        schema: Custom schema dictionary or DataSchema object
        rows: Number of rows to generate
        seed: Random seed for reproducibility

    Returns:
        DataFrame with synthetic data

    Examples:
        # From template
        df = dataset(template='customer_data', rows=500)

        # From custom schema
        df = dataset(schema={'columns': [...]}, rows=1000)
    """
    if template and schema:
        raise ValueError("Provide either template OR schema, not both")

    if not template and not schema:
        raise ValueError("Must provide either template or schema")

    # Load template if specified
    if template:
        schema = load_template_schema(template)
    elif isinstance(schema, dict):
        schema = DataSchema.from_dict(schema)

    # Generate data
    generator = DataGenerator(schema)
    return generator.generate(rows, seed)


def fit(
    data_or_path: Union[pd.DataFrame, str], sample_size: Optional[int] = None
) -> QuickModel:
    """
    Fit a model to existing data for later sampling.

    Args:
        data_or_path: DataFrame or path to data file
        sample_size: Number of samples to use for inference

    Returns:
        QuickModel that can generate similar data

    Examples:
        # From DataFrame
        model = fit(my_dataframe)
        new_data = model.sample(1000)

        # From file path
        model = fit('data.csv')
        new_data = model.sample(500)
    """
    if isinstance(data_or_path, str):
        # Load from file
        if data_or_path.endswith(".csv"):
            # Try to detect delimiter automatically
            try:
                data = pd.read_csv(data_or_path, sep=None, engine="python")
            except:
                # Fallback to comma delimiter
                data = pd.read_csv(data_or_path)
        elif data_or_path.endswith(".json"):
            data = pd.read_json(data_or_path)
        elif data_or_path.endswith(".xlsx"):
            data = pd.read_excel(data_or_path)
        elif data_or_path.endswith(".parquet"):
            data = pd.read_parquet(data_or_path)
        else:
            raise ValueError(
                "Unsupported file format. Use .csv, .json, .xlsx, or .parquet"
            )
    else:
        data = data_or_path

    # Infer schema
    schema = infer_schema_from_data(data, sample_size)

    # Return fitted model
    return QuickModel(schema)
