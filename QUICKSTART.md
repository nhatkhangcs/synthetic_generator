# Synthetic Generator Quick Start Guide

## 🚀 Installation

### Option 1: Using the installation script (Recommended)

**macOS/Linux:**
```bash
./install.sh
```

**Windows:**
```cmd
install.bat
```

### Option 2: Manual installation

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements/requirements.txt
pip install -e .
```

## ✅ Verify Installation

```bash
python verify_installation.py
```

## 🎯 Quick Examples

### Basic Data Generation

```python
from synthetic_generator import generate_data, DataSchema, ColumnSchema, DataType, DistributionType

# Define schema
schema = DataSchema(
    columns=[
        ColumnSchema(
            name="age",
            data_type=DataType.INTEGER,
            distribution=DistributionType.NORMAL,
            parameters={"mean": 30, "std": 10},
            min_value=18,
            max_value=80
        ),
        ColumnSchema(
            name="income",
            data_type=DataType.FLOAT,
            distribution=DistributionType.NORMAL,
            parameters={"mean": 50000, "std": 20000}
        )
    ]
)

# Generate data
data = generate_data(schema, n_samples=1000, seed=42)
print(data.head())
```

### Using Templates

```python
from synthetic_generator import load_template, generate_data

# Load pre-built template
schema = load_template("customer_data")

# Generate data
data = generate_data(schema, n_samples=500, seed=123)
print(data.head())
```

### Schema Inference

```python
import pandas as pd
from synthetic_generator import infer_schema, generate_data

# Load existing data
existing_data = pd.read_csv("your_data.csv")

# Infer schema
schema = infer_schema(existing_data)

# Generate new data
new_data = generate_data(schema, n_samples=1000, seed=456)
```

## 📊 Available Templates

- `customer_data`: Customer information with demographics
- `ecommerce_data`: E-commerce transaction data
- `medical_data`: Medical patient data with health metrics
- `financial_data`: Financial transaction data

## 🔧 Key Features

### Data Types
- **Numeric**: `INTEGER`, `FLOAT`
- **Text**: `STRING`, `EMAIL`, `PHONE`, `ADDRESS`, `NAME`
- **Categorical**: `CATEGORICAL`, `BOOLEAN`
- **Temporal**: `DATE`, `DATETIME`

### Distributions
- **Continuous**: `NORMAL`, `UNIFORM`, `EXPONENTIAL`, `GAMMA`, `BETA`, `WEIBULL`
- **Discrete**: `POISSON`, `BINOMIAL`, `GEOMETRIC`
- **Categorical**: `CATEGORICAL`, `CONSTANT`

### Constraints
- Value ranges (`min_value`, `max_value`)
- Uniqueness (`unique=True`)
- Null probabilities (`null_probability`)
- Dependencies between columns

## 🎯 Next Steps

1. **Run Examples**: `python examples/basic_usage.py`
2. **Read Documentation**: Check the main `README.md`
3. **Explore Templates**: Try different pre-built templates
4. **Create Custom Schemas**: Define your own data structures

## 🆘 Getting Help

- **Documentation**: See `README.md` for detailed documentation
- **Examples**: Check the `examples/` directory
- **Tests**: Run `python tests/test_basic_functionality.py`
- **Verification**: Run `python verify_installation.py`

## 🚨 Troubleshooting

### Common Issues

1. **Import Error**: Make sure you've activated the virtual environment
2. **Module Not Found**: Run `pip install -e .` to install the package
3. **Dependency Conflicts**: Use a fresh virtual environment

### Reset Installation

```bash
# Remove virtual environment
rm -rf .venv

# Reinstall
./install.sh
```

---

Happy generating! 🎉 