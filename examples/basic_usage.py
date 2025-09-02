"""
Basic usage examples for Synthetic Generator.

This file demonstrates how to use the Synthetic Generator library for
synthetic data generation with various features.
"""

import pandas as pd
import numpy as np
from synthetic_generator import (
    generate_data,
    infer_schema,
    load_template,
    validate_data,
    DataSchema,
    ColumnSchema,
    DataType,
    DistributionType,
)


def example_1_basic_generation():
    """Example 1: Basic data generation with schema definition."""
    print("=== Example 1: Basic Data Generation ===")

    # Define a simple schema
    schema = DataSchema(
        columns=[
            ColumnSchema(
                name="age",
                data_type=DataType.INTEGER,
                distribution=DistributionType.NORMAL,
                parameters={"mean": 30, "std": 10},
                min_value=18,
                max_value=80,
            ),
            ColumnSchema(
                name="income",
                data_type=DataType.FLOAT,
                distribution=DistributionType.NORMAL,
                parameters={"mean": 50000, "std": 20000},
                min_value=20000,
                max_value=200000,
            ),
            ColumnSchema(
                name="city",
                data_type=DataType.CATEGORICAL,
                distribution=DistributionType.CATEGORICAL,
                parameters={
                    "categories": ["New York", "Los Angeles", "Chicago", "Houston"],
                    "probabilities": [0.3, 0.25, 0.25, 0.2],
                },
            ),
        ]
    )

    # Generate data
    data = generate_data(schema, n_samples=1000, seed=42)
    print(f"Generated {len(data)} samples")
    print(data.head())
    print("\nData statistics:")
    print(data.describe())
    print("\n" + "=" * 50 + "\n")


def example_2_template_usage():
    """Example 2: Using pre-built templates."""
    print("=== Example 2: Using Templates ===")

    # Load a customer data template
    schema = load_template("customer_data")

    # Generate data
    data = generate_data(schema, n_samples=500, seed=123)
    print(f"Generated {len(data)} customer records")
    print(data.head())
    print("\n" + "=" * 50 + "\n")


def example_3_schema_inference():
    """Example 3: Inferring schema from existing data."""
    print("=== Example 3: Schema Inference ===")

    # Create some sample data
    sample_data = pd.DataFrame(
        {
            "user_id": range(1, 101),
            "age": np.random.normal(35, 10, 100).astype(int),
            "salary": np.random.normal(60000, 15000, 100),
            "department": np.random.choice(["IT", "HR", "Sales", "Marketing"], 100),
            "is_manager": np.random.choice([True, False], 100, p=[0.2, 0.8]),
        }
    )

    print("Original data:")
    print(sample_data.head())

    # Infer schema
    inferred_schema = infer_schema(sample_data)
    print(f"\nInferred schema has {len(inferred_schema.columns)} columns")

    # Generate new data based on inferred schema
    new_data = generate_data(inferred_schema, n_samples=200, seed=456)
    print(f"\nGenerated {len(new_data)} new samples based on inferred schema:")
    print(new_data.head())
    print("\n" + "=" * 50 + "\n")


def example_4_correlations():
    """Example 4: Working with correlations."""
    print("=== Example 4: Correlations ===")

    # Define schema with correlations
    schema = DataSchema(
        columns=[
            ColumnSchema(
                name="height",
                data_type=DataType.FLOAT,
                distribution=DistributionType.NORMAL,
                parameters={"mean": 170, "std": 10},
                min_value=150,
                max_value=200,
            ),
            ColumnSchema(
                name="weight",
                data_type=DataType.FLOAT,
                distribution=DistributionType.NORMAL,
                parameters={"mean": 70, "std": 15},
                min_value=40,
                max_value=120,
            ),
            ColumnSchema(
                name="age",
                data_type=DataType.INTEGER,
                distribution=DistributionType.NORMAL,
                parameters={"mean": 30, "std": 8},
                min_value=18,
                max_value=65,
            ),
        ],
        correlations={
            "height": {"weight": 0.7},  # Height and weight are correlated
            "age": {"weight": 0.3},  # Age and weight have some correlation
        },
    )

    # Generate data
    data = generate_data(schema, n_samples=1000, seed=789)

    print("Generated data with correlations:")
    print(data.head())

    # Check actual correlations
    correlation_matrix = data.corr()
    print(f"\nActual correlation matrix:")
    print(correlation_matrix)
    print("\n" + "=" * 50 + "\n")


def example_5_constraints():
    """Example 5: Working with constraints."""
    print("=== Example 5: Constraints ===")

    # Define schema with constraints
    schema = DataSchema(
        columns=[
            ColumnSchema(
                name="employee_id",
                data_type=DataType.INTEGER,
                distribution=DistributionType.UNIFORM,
                parameters={"low": 1, "high": 10000},
                unique=True,
            ),
            ColumnSchema(
                name="salary",
                data_type=DataType.FLOAT,
                distribution=DistributionType.NORMAL,
                parameters={"mean": 50000, "std": 15000},
                min_value=30000,
                max_value=100000,
            ),
            ColumnSchema(
                name="bonus",
                data_type=DataType.FLOAT,
                distribution=DistributionType.UNIFORM,
                parameters={"low": 0, "high": 10000},
                depends_on=["salary"],
                conditional_rules={
                    "rules": [
                        {
                            "condition": {"salary": {"operator": ">", "value": 70000}},
                            "value": 5000,
                        },
                        {
                            "condition": {"salary": {"operator": ">", "value": 50000}},
                            "value": 3000,
                        },
                    ],
                    "default": 1000,
                },
            ),
        ]
    )

    # Generate data
    data = generate_data(schema, n_samples=500, seed=999)

    print("Generated data with constraints:")
    print(data.head())

    # Validate the data
    validation_results = validate_data(data, schema)
    print(f"\nValidation results:")
    print(f"Valid: {validation_results['valid']}")
    if validation_results["errors"]:
        print(f"Errors: {validation_results['errors']}")
    if validation_results["warnings"]:
        print(f"Warnings: {validation_results['warnings']}")
    print("\n" + "=" * 50 + "\n")


def example_6_medical_data():
    """Example 6: Medical data example."""
    print("=== Example 6: Medical Data ===")

    # Load medical data template
    schema = load_template("medical_data")

    # Generate data
    data = generate_data(schema, n_samples=1000, seed=111)

    print("Generated medical data:")
    print(data.head())

    # Show some statistics
    print(f"\nData shape: {data.shape}")
    print(f"Age range: {data['age'].min()} - {data['age'].max()}")
    print(f"Gender distribution:\n{data['gender'].value_counts()}")
    print(f"Diabetes prevalence: {data['diabetes'].mean():.2%}")
    print("\n" + "=" * 50 + "\n")


def example_7_export_data():
    """Example 7: Exporting generated data."""
    print("=== Example 7: Data Export ===")

    # Generate some data
    schema = load_template("customer_data")
    data = generate_data(schema, n_samples=100, seed=222)

    # Export to different formats
    from synthetic_generator.export import export_data

    # Export to CSV
    export_data(data, "csv", filepath="customer_data.csv")
    print("Exported to customer_data.csv")

    # Export to JSON
    export_data(data, "json", filepath="customer_data.json")
    print("Exported to customer_data.json")

    # Export to Excel
    export_data(data, "excel", filepath="customer_data.xlsx")
    print("Exported to customer_data.xlsx")

    print("Data export completed!")
    print("\n" + "=" * 50 + "\n")


def main():
    """Run all examples."""
    print("Synthetic Generator Synthetic Data Generation Examples")
    print("=" * 50)

    try:
        example_1_basic_generation()
        example_2_template_usage()
        example_3_schema_inference()
        example_4_correlations()
        example_5_constraints()
        example_6_medical_data()
        example_7_export_data()

        print("All examples completed successfully!")

    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
