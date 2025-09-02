#!/usr/bin/env python3
"""
Test the updated README examples to ensure they work.
"""

def test_quick_api_example():
    """Test the updated Quick API example."""
    print("Testing Quick API example...")
    
    from synthetic_generator.quick import dataset, fit
    import pandas as pd
    
    # 1) From a template
    df = dataset(template="customer_data", rows=100, seed=42)
    print(f"✓ Generated {len(df)} rows from template")
    
    # 2) From your data (fit then sample)
    sample_data = pd.DataFrame({
        'age': [25, 30, 35, 40, 45],
        'salary': [50000, 60000, 70000, 80000, 90000]
    })
    model = fit(sample_data)
    df2 = model.sample(50, seed=123)
    print(f"✓ Generated {len(df2)} rows from fitted model")
    
    return True

def test_template_example():
    """Test the template example."""
    print("Testing template example...")
    
    from synthetic_generator import load_template, generate_data
    
    # Load a pre-built template
    schema = load_template("customer_data")
    
    # Generate data
    data = generate_data(schema, n_samples=100, seed=123)
    print(f"✓ Generated {len(data)} samples")
    print(f"✓ Data shape: {data.shape}")
    
    return True

def test_schema_inference_example():
    """Test the schema inference example."""
    print("Testing schema inference example...")
    
    import pandas as pd
    from synthetic_generator import infer_schema, generate_data
    
    # Create sample data (or load from file)
    existing_data = pd.DataFrame({
        'age': [25, 30, 35, 40, 45],
        'salary': [50000, 60000, 70000, 80000, 90000],
        'department': ['IT', 'HR', 'Sales', 'IT', 'HR']
    })
    
    # Infer schema
    schema = infer_schema(existing_data)
    
    # Generate new data based on inferred schema
    new_data = generate_data(schema, n_samples=100, seed=456)
    print(f"✓ Generated {len(new_data)} new samples")
    
    return True

def test_privacy_example():
    """Test the privacy example."""
    print("Testing privacy example...")
    
    from synthetic_generator import load_template, generate_data
    
    schema = load_template("customer_data")
    data = generate_data(schema, n_samples=100, seed=42)
    print(f"✓ Generated {len(data)} samples")
    
    return True

def main():
    """Run all tests."""
    print("Testing Updated README Examples")
    print("=" * 40)
    
    tests = [
        test_quick_api_example,
        test_template_example,
        test_schema_inference_example,
        test_privacy_example,
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            print()
    
    print("=" * 40)
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All updated README examples work correctly!")
        return 0
    else:
        print("❌ Some examples still have issues.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
