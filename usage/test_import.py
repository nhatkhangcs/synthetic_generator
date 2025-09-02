import pytest
import synthetic_generator as sg

import types
from typing import Set, Tuple, Type


def test_data_type_enum_values():
    """Test that DataType enum has expected values."""
    from synthetic_generator import DataType

    expected_types = {
        "INTEGER",
        "FLOAT",
        "STRING",
        "BOOLEAN",
        "DATE",
        "DATETIME",
        "CATEGORICAL",
    }

    for expected_type in expected_types:
        assert hasattr(DataType, expected_type), f"DataType.{expected_type} not found"


def test_distribution_type_enum_values():
    """Test that DistributionType enum has expected values."""
    from synthetic_generator import DistributionType

    expected_distributions = {
        "NORMAL",
        "UNIFORM",
        "EXPONENTIAL",
        "GAMMA",
        "BETA",
        "WEIBULL",
        "POISSON",
        "BINOMIAL",
        "GEOMETRIC",
        "CATEGORICAL",
    }

    for expected_dist in expected_distributions:
        assert hasattr(
            DistributionType, expected_dist
        ), f"DistributionType.{expected_dist} not found"


if __name__ == "__main__":
    print("Running import tests...")
    test_data_type_enum_values()
    test_distribution_type_enum_values()
    print("✅ All import tests passed!")
