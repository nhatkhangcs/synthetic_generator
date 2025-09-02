#!/usr/bin/env python3
"""
Test script to verify all README examples are runnable.
"""

import sys
import traceback

def test_quick_api():
    """Test Quick API examples from README."""
    print("Testing Quick API examples...")
    
    try:
        from synthetic_generator.quick import dataset, fit
        
        # Test 1: From a template
        print("  - Testing dataset from template...")
        df = dataset(template="customer_data", rows=100, seed=42)
        print(f"    ✓ Generated {len(df)} rows from customer_data template")
        
        # Test 2: From data (fit then sample)
        print("  - Testing fit and sample...")
        model = fit(df)  # Use the generated data as input
        df2 = model.sample(50, seed=123)
        print(f"    ✓ Generated {len(df2)} rows from fitted model")
        
        return True
    except Exception as e:
        print(f"    ✗ Quick API test failed: {e}")
        traceback.print_exc()
        return False

def test_template_usage():
    """Test template usage examples from README."""
    print("Testing template usage examples...")
    
    try:
        from synthetic_generator import load_template, generate_data
        
        # Load a pre-built template
        print("  - Testing load_template...")
        schema = load_template("customer_data")
        print(f"    ✓ Loaded customer_data template with {len(schema.columns)} columns")
        
        # Generate data
        print("  - Testing generate_data from template...")
        data = generate_data(schema, n_samples=100, seed=123)
        print(f"    ✓ Generated {len(data)} samples")
        print(f"    ✓ Data shape: {data.shape}")
        
        return True
    except Exception as e:
        print(f"    ✗ Template usage test failed: {e}")
        traceback.print_exc()
        return False

def test_schema_inference():
    """Test schema inference examples from README."""
    print("Testing schema inference examples...")
    
    try:
        import pandas as pd
        from synthetic_generator import infer_schema, generate_data
        
        # Create some sample data
        print("  - Creating sample data...")
        existing_data = pd.DataFrame({
            'age': [25, 30, 35, 40, 45],
            'salary': [50000, 60000, 70000, 80000, 90000],
            'department': ['IT', 'HR', 'Sales', 'IT', 'HR']
        })
        print(f"    ✓ Created sample data with {len(existing_data)} rows")
        
        # Infer schema
        print("  - Testing infer_schema...")
        schema = infer_schema(existing_data)
        print(f"    ✓ Inferred schema with {len(schema.columns)} columns")
        
        # Generate new data based on inferred schema
        print("  - Testing generate_data from inferred schema...")
        new_data = generate_data(schema, n_samples=50, seed=456)
        print(f"    ✓ Generated {len(new_data)} new samples")
        
        return True
    except Exception as e:
        print(f"    ✗ Schema inference test failed: {e}")
        traceback.print_exc()
        return False

def test_correlations():
    """Test correlations example from README."""
    print("Testing correlations example...")
    
    try:
        from synthetic_generator import DataSchema, ColumnSchema, DataType, DistributionType, generate_data
        
        # Define schema with correlations
        print("  - Creating schema with correlations...")
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
            ],
            correlations={
                "height": {"weight": 0.7},  # Height and weight correlation
            },
        )
        print(f"    ✓ Created schema with {len(schema.columns)} columns and correlations")
        
        # Generate data
        print("  - Testing generate_data with correlations...")
        data = generate_data(schema, n_samples=100, seed=789)
        print(f"    ✓ Generated {len(data)} samples with correlations")
        
        return True
    except Exception as e:
        print(f"    ✗ Correlations test failed: {e}")
        traceback.print_exc()
        return False

def test_constraints():
    """Test constraints example from README."""
    print("Testing constraints example...")
    
    try:
        from synthetic_generator import DataSchema, ColumnSchema, DataType, DistributionType, generate_data
        
        # Define schema with constraints
        print("  - Creating schema with constraints...")
        schema = DataSchema(
            columns=[
                ColumnSchema(
                    name="salary",
                    data_type=DataType.FLOAT,
                    distribution=DistributionType.NORMAL,
                    parameters={"mean": 50000, "std": 15000},
                    min_value=30000,        # Minimum value
                    max_value=100000,       # Maximum value
                    unique=False,           # Not unique (would be hard with normal distribution)
                    nullable=True,          # Allow null values
                    null_probability=0.05   # 5% null probability
                ),
            ]
        )
        print(f"    ✓ Created schema with constraints")
        
        # Generate data
        print("  - Testing generate_data with constraints...")
        data = generate_data(schema, n_samples=100, seed=999)
        print(f"    ✓ Generated {len(data)} samples with constraints")
        
        return True
    except Exception as e:
        print(f"    ✗ Constraints test failed: {e}")
        traceback.print_exc()
        return False

def test_validation():
    """Test validation example from README."""
    print("Testing validation example...")
    
    try:
        from synthetic_generator import validate_data, load_template, generate_data
        
        # Generate some data first
        print("  - Generating test data...")
        schema = load_template("customer_data")
        data = generate_data(schema, n_samples=50, seed=111)
        print(f"    ✓ Generated {len(data)} test samples")
        
        # Validate generated data
        print("  - Testing validate_data...")
        results = validate_data(data, schema)
        print(f"    ✓ Validation completed")
        print(f"    ✓ Valid: {results['valid']}")
        if results['errors']:
            print(f"    ✓ Errors: {len(results['errors'])} found")
        if results['warnings']:
            print(f"    ✓ Warnings: {len(results['warnings'])} found")
        
        return True
    except Exception as e:
        print(f"    ✗ Validation test failed: {e}")
        traceback.print_exc()
        return False

def test_export():
    """Test export example from README."""
    print("Testing export example...")
    
    try:
        from synthetic_generator.export import export_data
        from synthetic_generator import load_template, generate_data
        
        # Generate some data first
        print("  - Generating test data...")
        schema = load_template("customer_data")
        data = generate_data(schema, n_samples=20, seed=222)
        print(f"    ✓ Generated {len(data)} test samples")
        
        # Export to various formats
        print("  - Testing export to CSV...")
        export_data(data, 'csv', filepath='test_data.csv')
        print("    ✓ Exported to CSV")
        
        print("  - Testing export to JSON...")
        export_data(data, 'json', filepath='test_data.json')
        print("    ✓ Exported to JSON")
        
        print("  - Testing export to Excel...")
        export_data(data, 'excel', filepath='test_data.xlsx')
        print("    ✓ Exported to Excel")
        
        print("  - Testing export to Parquet...")
        export_data(data, 'parquet', filepath='test_data.parquet')
        print("    ✓ Exported to Parquet")
        
        return True
    except Exception as e:
        print(f"    ✗ Export test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all README example tests."""
    print("Testing README Examples for Synthetic Generator v0.0.7")
    print("=" * 60)
    
    tests = [
        test_quick_api,
        test_template_usage,
        test_schema_inference,
        test_correlations,
        test_constraints,
        test_validation,
        test_export,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"    ✗ Test {test.__name__} crashed: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All README examples are working correctly!")
        return 0
    else:
        print("❌ Some README examples have issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
