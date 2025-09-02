"""
Data schema definitions for SynGen.

This module provides classes and utilities for defining data schemas,
including automatic schema inference and template loading.
"""

from .base import DataSchema, ColumnSchema, DataType, DistributionType
from .inference import SchemaInferrer
from .templates import TemplateLoader

__all__ = [
    "DataSchema",
    "ColumnSchema",
    "DataType",
    "DistributionType",
    "SchemaInferrer",
    "TemplateLoader",
    "load_template",
]


def load_template(template_name: str) -> DataSchema:
    """Load a pre-built template for common use cases."""
    return TemplateLoader.load(template_name)
