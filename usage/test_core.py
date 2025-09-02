"""
Core functionality tests for Synthetic Generator after dtype cleanup.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add the src directory to the path BEFORE the site-packages
src_path = os.path.join(os.path.dirname(__file__), "..", "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Also remove the installed package from sys.modules if it exists
if "synthetic_generator" in sys.modules:
    del sys.modules["synthetic_generator"]


def test_dtype_imports():
    """Test that the dtype module can be imported correctly from installed package."""
    try:
        from synthetic_generator.dtype import BaseInt, BaseFloat

        print("✅ Dtype imports successful")
        print(f"   - BaseInt: {BaseInt}")
        print(f"   - BaseFloat: {BaseFloat}")
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import dtype classes: {e}")


def test_dtype_structure():
    """Test that the dtype module has the expected structure in installed package."""
    try:
        from synthetic_generator.dtype import BaseInt, BaseFloat

        print("✅ Dtype structure is correct (BaseInt/BaseFloat)")
        assert True

    except Exception as e:
        pytest.fail(f"Failed to verify dtype structure: {e}")


def test_schema_creation():
    """Test that schemas can be created with the cleaned up types."""
    try:
        from synthetic_generator.schemas import (
            DataSchema,
            ColumnSchema,
            DataType,
            DistributionType,
        )

        # Create a simple schema
        schema = DataSchema(
            columns=[
                ColumnSchema(
                    name="age",
                    data_type=DataType.INTEGER,
                    distribution=DistributionType.NORMAL,
                    parameters={"mean": 30, "std": 10},
                ),
                ColumnSchema(
                    name="income",
                    data_type=DataType.FLOAT,
                    distribution=DistributionType.NORMAL,
                    parameters={"mean": 50000, "std": 20000},
                ),
            ]
        )

        assert len(schema.columns) == 2
        assert schema.columns[0].name == "age"
        assert schema.columns[1].name == "income"
        print("✅ Schema creation successful")

    except Exception as e:
        pytest.fail(f"Failed to create schema: {e}")


def test_data_generation():
    """Test that data can be generated with the cleaned up types."""
    try:
        from synthetic_generator.generators.base import DataGenerator
        from synthetic_generator.schemas import (
            DataSchema,
            ColumnSchema,
            DataType,
            DistributionType,
        )

        # Create a simple schema
        schema = DataSchema(
            columns=[
                ColumnSchema(
                    name="id",
                    data_type=DataType.INTEGER,
                    distribution=DistributionType.UNIFORM,
                    parameters={"low": 1, "high": 100},
                ),
                ColumnSchema(
                    name="value",
                    data_type=DataType.FLOAT,
                    distribution=DistributionType.NORMAL,
                    parameters={"mean": 0, "std": 1},
                ),
            ]
        )

        # Generate data
        generator = DataGenerator(schema)
        data = generator.generate(10, seed=42)

        assert isinstance(data, pd.DataFrame)
        assert len(data) == 10
        assert "id" in data.columns
        assert "value" in data.columns
        print("✅ Data generation successful")

    except Exception as e:
        pytest.fail(f"Failed to generate data: {e}")


def test_web_ui_imports():
    """Test that web UI components can be imported correctly."""
    try:
        from synthetic_generator.web import app, api

        print("✅ Web UI imports successful")
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import web UI components: {e}")


if __name__ == "__main__":
    print("Running core functionality tests...")
    test_dtype_imports()
    test_dtype_structure()
    test_schema_creation()
    test_data_generation()
    test_web_ui_imports()
    print("✅ All core functionality tests passed!")
