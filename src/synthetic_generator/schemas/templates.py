"""
Template loader for SynGen.

This module provides pre-built templates for common use cases
in synthetic data generation.
"""

from typing import Dict, Any
from .base import DataSchema, ColumnSchema, DataType, DistributionType


class TemplateLoader:
    """Loader for pre-built data schemas."""

    _templates = {
        "customer_data": {
            "columns": [
                {
                    "name": "customer_id",
                    "data_type": "integer",
                    "distribution": "uniform",
                    "parameters": {"low": 1, "high": 10000},
                    "unique": True,
                },
                {
                    "name": "first_name",
                    "data_type": "name",
                    "distribution": "categorical",
                    "parameters": {
                        "categories": ["John", "Jane", "Bob", "Alice", "Charlie"]
                    },
                },
                {
                    "name": "last_name",
                    "data_type": "name",
                    "distribution": "categorical",
                    "parameters": {
                        "categories": ["Smith", "Johnson", "Williams", "Brown", "Jones"]
                    },
                },
                {
                    "name": "email",
                    "data_type": "email",
                    "distribution": "categorical",
                    "parameters": {
                        "categories": ["john.smith@email.com", "jane.johnson@email.com"]
                    },
                },
                {
                    "name": "age",
                    "data_type": "integer",
                    "distribution": "normal",
                    "parameters": {"mean": 35, "std": 10},
                    "min_value": 18,
                    "max_value": 80,
                },
                {
                    "name": "income",
                    "data_type": "float",
                    "distribution": "normal",
                    "parameters": {"mean": 50000, "std": 20000},
                    "min_value": 20000,
                    "max_value": 200000,
                },
                {
                    "name": "is_active",
                    "data_type": "boolean",
                    "distribution": "categorical",
                    "parameters": {
                        "categories": [True, False],
                        "probabilities": [0.8, 0.2],
                    },
                },
            ]
        },
        "ecommerce_data": {
            "columns": [
                {
                    "name": "order_id",
                    "data_type": "integer",
                    "distribution": "uniform",
                    "parameters": {"low": 1, "high": 50000},
                    "unique": True,
                },
                {
                    "name": "customer_id",
                    "data_type": "integer",
                    "distribution": "uniform",
                    "parameters": {"low": 1, "high": 1000},
                },
                {
                    "name": "product_id",
                    "data_type": "integer",
                    "distribution": "uniform",
                    "parameters": {"low": 1, "high": 100},
                },
                {
                    "name": "quantity",
                    "data_type": "integer",
                    "distribution": "poisson",
                    "parameters": {"lam": 2},
                    "min_value": 1,
                    "max_value": 10,
                },
                {
                    "name": "price",
                    "data_type": "float",
                    "distribution": "normal",
                    "parameters": {"mean": 50, "std": 20},
                    "min_value": 5,
                    "max_value": 200,
                },
                {
                    "name": "order_date",
                    "data_type": "date",
                    "distribution": "uniform",
                    "parameters": {
                        "start_date": "2023-01-01",
                        "end_date": "2024-12-31",
                    },
                },
                {
                    "name": "payment_method",
                    "data_type": "categorical",
                    "distribution": "categorical",
                    "parameters": {
                        "categories": ["credit_card", "debit_card", "paypal", "cash"],
                        "probabilities": [0.4, 0.3, 0.2, 0.1],
                    },
                },
            ],
            "correlations": {
                "quantity": {"price": -0.3},  # Higher quantity, lower price per item
                "customer_id": {"order_id": 0.1},  # Slight correlation
            },
        },
        "medical_data": {
            "columns": [
                {
                    "name": "patient_id",
                    "data_type": "integer",
                    "distribution": "uniform",
                    "parameters": {"low": 1, "high": 10000},
                    "unique": True,
                },
                {
                    "name": "age",
                    "data_type": "integer",
                    "distribution": "normal",
                    "parameters": {"mean": 45, "std": 15},
                    "min_value": 0,
                    "max_value": 100,
                },
                {
                    "name": "gender",
                    "data_type": "categorical",
                    "distribution": "categorical",
                    "parameters": {
                        "categories": ["M", "F"],
                        "probabilities": [0.48, 0.52],
                    },
                },
                {
                    "name": "height_cm",
                    "data_type": "float",
                    "distribution": "normal",
                    "parameters": {"mean": 170, "std": 10},
                    "min_value": 100,
                    "max_value": 220,
                },
                {
                    "name": "weight_kg",
                    "data_type": "float",
                    "distribution": "normal",
                    "parameters": {"mean": 70, "std": 15},
                    "min_value": 30,
                    "max_value": 150,
                },
                {
                    "name": "blood_pressure_systolic",
                    "data_type": "integer",
                    "distribution": "normal",
                    "parameters": {"mean": 120, "std": 15},
                    "min_value": 80,
                    "max_value": 200,
                },
                {
                    "name": "blood_pressure_diastolic",
                    "data_type": "integer",
                    "distribution": "normal",
                    "parameters": {"mean": 80, "std": 10},
                    "min_value": 50,
                    "max_value": 120,
                },
                {
                    "name": "cholesterol_mgdl",
                    "data_type": "integer",
                    "distribution": "normal",
                    "parameters": {"mean": 200, "std": 40},
                    "min_value": 100,
                    "max_value": 400,
                },
                {
                    "name": "diabetes",
                    "data_type": "boolean",
                    "distribution": "categorical",
                    "parameters": {
                        "categories": [True, False],
                        "probabilities": [0.1, 0.9],
                    },
                },
            ],
            "correlations": {
                "height_cm": {"weight_kg": 0.6},
                "age": {"blood_pressure_systolic": 0.4},
                "weight_kg": {"blood_pressure_systolic": 0.3},
                "age": {"diabetes": 0.2},
            },
        },
        "financial_data": {
            "columns": [
                {
                    "name": "transaction_id",
                    "data_type": "integer",
                    "distribution": "uniform",
                    "parameters": {"low": 1, "high": 100000},
                    "unique": True,
                },
                {
                    "name": "account_id",
                    "data_type": "integer",
                    "distribution": "uniform",
                    "parameters": {"low": 1, "high": 5000},
                },
                {
                    "name": "amount",
                    "data_type": "float",
                    "distribution": "normal",
                    "parameters": {"mean": 1000, "std": 500},
                    "min_value": 10,
                    "max_value": 10000,
                },
                {
                    "name": "transaction_type",
                    "data_type": "categorical",
                    "distribution": "categorical",
                    "parameters": {
                        "categories": ["deposit", "withdrawal", "transfer", "payment"],
                        "probabilities": [0.3, 0.25, 0.25, 0.2],
                    },
                },
                {
                    "name": "timestamp",
                    "data_type": "datetime",
                    "distribution": "uniform",
                    "parameters": {
                        "start_datetime": "2023-01-01",
                        "end_datetime": "2024-12-31",
                    },
                },
                {
                    "name": "merchant_category",
                    "data_type": "categorical",
                    "distribution": "categorical",
                    "parameters": {
                        "categories": [
                            "retail",
                            "food",
                            "transport",
                            "entertainment",
                            "utilities",
                        ],
                        "probabilities": [0.3, 0.25, 0.2, 0.15, 0.1],
                    },
                },
            ]
        },
    }

    @classmethod
    def load(cls, template_name: str) -> DataSchema:
        """
        Load a template by name.

        Args:
            template_name: Name of the template

        Returns:
            Data schema template
        """
        if template_name not in cls._templates:
            available_templates = list(cls._templates.keys())
            raise ValueError(
                f"Template '{template_name}' not found. "
                f"Available templates: {available_templates}"
            )

        template_data = cls._templates[template_name]
        return DataSchema.from_dict(template_data)

    @classmethod
    def list_templates(cls) -> list[str]:
        """List all available templates."""
        return list(cls._templates.keys())

    @classmethod
    def get_template_info(cls, template_name: str) -> Dict[str, Any]:
        """Get information about a template."""
        if template_name not in cls._templates:
            raise ValueError(f"Template '{template_name}' not found")

        template_data = cls._templates[template_name]
        return {
            "name": template_name,
            "columns": len(template_data["columns"]),
            "has_correlations": "correlations" in template_data,
            "description": cls._get_template_description(template_name),
        }

    @classmethod
    def _get_template_description(cls, template_name: str) -> str:
        """Get description for a template."""
        descriptions = {
            "customer_data": "Customer information including demographics and contact details",
            "ecommerce_data": "E-commerce transaction data with product and order information",
            "medical_data": "Medical patient data with health metrics and demographics",
            "financial_data": "Financial transaction data with amounts and categories",
        }
        return descriptions.get(template_name, "No description available")


def load_template_schema(template_name: str) -> DataSchema:
    """Convenience function to load template schema."""
    return TemplateLoader.load(template_name)
