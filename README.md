# Synthetic Generator

A comprehensive Python library for generating synthetic data with various distributions, correlations, and constraints for machine learning and data science applications.

[![PyPI version](https://badge.fury.io/py/synthetic-generator.svg)](https://badge.fury.io/py/synthetic-generator)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Table of Contents

- [Synthetic Generator](#synthetic-generator)
  - [📋 Table of Contents](#-table-of-contents)
  - [🌟 Features](#-features)
    - [Core Data Generation](#core-data-generation)
    - [Main Features](#main-features)
    - [User Experience](#user-experience)
  - [🎯 Why Synthetic Generator?](#-why-synthetic-generator)
  - [🚀 Quick Start](#-quick-start)
    - [Installation](#installation)
    - [Quick Generate (CLI)](#quick-generate-cli)
    - [Quick API (Python)](#quick-api-python)
    - [Using Templates](#using-templates)
    - [Schema Inference](#schema-inference)
  - [📚 Detailed Documentation](#-detailed-documentation)
    - [Data Types](#data-types)
    - [Distributions](#distributions)
    - [Correlations](#correlations)
    - [Constraints](#constraints)
    - [Dependencies](#dependencies)
  - [🎯 Use Cases](#-use-cases)
    - [Customer Data](#customer-data)
    - [Medical Data](#medical-data)
    - [Financial Data](#financial-data)
    - [E-commerce Data](#e-commerce-data)
  - [🔧 Advanced Features](#-advanced-features)
    - [Optional Web Interface](#optional-web-interface)

    - [Data Validation](#data-validation)
    - [Data Export](#data-export)
  - [📊 Available Templates](#-available-templates)
  - [📦 Package Information](#-package-information)
  - [🛠️ Development](#️-development)
    - [Installation for Development](#installation-for-development)
    - [Running Tests](#running-tests)
    - [Running Examples](#running-examples)
  - [🤝 Contributing](#-contributing)
    - [Development Setup](#development-setup)
  - [📄 License](#-license)
  - [🚀 Getting Started](#-getting-started)
  - [📞 Contact](#-contact)
  - [🙏 Acknowledgments](#-acknowledgments)

## 🌟 Features

### Core Data Generation
- **Multiple Distributions**: Normal, Uniform, Exponential, Gamma, Beta, Weibull, Poisson, Binomial, Geometric, Categorical
- **Data Types**: Integer, Float, String, Boolean, Date, DateTime, Email, Phone, Address, Name
- **Correlations**: Define relationships between variables with correlation matrices
- **Constraints**: Value ranges, uniqueness, null probabilities, pattern matching
- **Dependencies**: Generate data based on other columns with conditional rules

### Main Features
- **Schema Inference**: Automatically detect data types and constraints from existing data (no distribution inference)
- **Templates**: Pre-built schemas for common use cases (customer data, medical data, e-commerce, financial)
- **Privacy**: Basic anonymization support
- **Validation**: Comprehensive data validation against schemas (data types and constraints only)
- **Export**: Multiple format support (CSV, JSON, Parquet, Excel)

### User Experience
- **Easy-to-Use API**: Simple, intuitive interface for data generation
- **Web Interface**: Modern, responsive web UI for interactive data generation
- **Flexible Configuration**: Support for both programmatic and configuration-based setup
- **Reproducibility**: Seed-based random generation for consistent results
- **Performance**: Optimized for large-scale data generation

## 🎯 Why Synthetic Generator?

Synthetic Generator is designed to make synthetic data generation simple, flexible, and powerful. Whether you're:
- **Testing applications** with realistic data
- **Training machine learning models** with diverse datasets
- **Prototyping** without sensitive information
- **Data augmentation** for research purposes

This library provides all the tools you need to create high-quality synthetic data that maintains the statistical properties of your original data while ensuring privacy and flexibility.

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (Recommended)
pip install synthetic-generator

# Install from GitHub (Development)
git clone https://github.com/nhatkhangcs/synthetic_generator.git
cd synthetic-generator
pip install -e .
```

### Quick Generate (CLI)

```bash
# From a built-in template
synthetic-generator generate --template customer_data --rows 10000 --out customers.parquet

# From your real data (fit then sample)
synthetic-generator generate --in real.csv --rows 5000 --out synthetic.csv
```

### Quick API (Python)

```python
from synthetic_generator.quick import dataset, fit
import pandas as pd

# 1) From a template
df = dataset(template="customer_data", rows=1000, seed=42)

# 2) From your data (fit then sample)
# Create sample data or load from file
sample_data = pd.DataFrame({
    'age': [25, 30, 35, 40, 45],
    'salary': [50000, 60000, 70000, 80000, 90000]
})
model = fit(sample_data)
df2 = model.sample(500, seed=123)
```

### Using Templates

```python
from synthetic_generator import load_template, generate_data

# Load a pre-built template
schema = load_template("customer_data")

# Generate data
data = generate_data(schema, n_samples=500, seed=123)
print(data.head())
```

### Schema Inference

```python
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
new_data = generate_data(schema, n_samples=1000, seed=456)
```

## 📚 Detailed Documentation

### Data Types

Synthetic Generator supports various data types:

- **Numeric**: `INTEGER`, `FLOAT`
- **Text**: `STRING`, `EMAIL`, `PHONE`, `ADDRESS`, `NAME`
- **Categorical**: `CATEGORICAL`, `BOOLEAN`
- **Temporal**: `DATE`, `DATETIME`

### Distributions

Available statistical distributions:

- **Continuous**: `NORMAL`, `UNIFORM`, `EXPONENTIAL`, `GAMMA`, `BETA`, `WEIBULL`
- **Discrete**: `POISSON`, `BINOMIAL`, `GEOMETRIC`
- **Categorical**: `CATEGORICAL`, `CONSTANT`

### Correlations

Define relationships between variables:

```python
schema = DataSchema(
    columns=[...],
    correlations={
        "height": {"weight": 0.7},  # Height and weight correlation
        "age": {"income": 0.4}      # Age and income correlation
    }
)
```

### Constraints

Apply various constraints to your data:

```python
ColumnSchema(
    name="salary",
    data_type=DataType.FLOAT,
    distribution=DistributionType.NORMAL,
    parameters={"mean": 50000, "std": 15000},
    min_value=30000,        # Minimum value
    max_value=100000,       # Maximum value
    unique=True,            # Unique values
    nullable=True,          # Allow null values
    null_probability=0.05   # 5% null probability
)
```

### Dependencies

Generate data based on other columns:

```python
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
                "value": 5000
            }
        ],
        "default": 1000
    }
)
```

## 🎯 Use Cases

### Customer Data
Generate realistic customer profiles with demographics, contact information, and preferences.

### Medical Data
Create synthetic patient data with health metrics, demographics, and medical conditions.

### Financial Data
Generate transaction data with realistic amounts, categories, and temporal patterns.

### E-commerce Data
Create order and product data with realistic relationships and business rules.

## 🔧 Advanced Features

### Optional Web Interface

You can install and run the web UI if needed:

```bash
pip install synthetic-generator[web]
synthetic-generator web  # http://localhost:8000
```

![Web Interface](branding/UI/UI_new.png)

![Templates](branding/UI/templates.png)

![Schema Inference](branding/UI/schema.png)

Web UI tips (v0.0.7+):
- Templates: clicking "Use Template" navigates to the Generator and auto-populates columns and parameters.
- Export: after generating data, export directly from the Generator page via the built-in Export panel (CSV, JSON, Excel, Parquet). There is no separate Export page.
- Schema Inference: Only infers data types and constraints, not distributions. Users can manually specify distributions in the Generator.
- Null Probability: Fixed issue where 100% null probability wasn't being applied correctly.
- JSON Serialization: Fixed NaN values in generated data to properly serialize as null in JSON.

### Data Generation

```python
# Generate data with custom parameters
from synthetic_generator import load_template, generate_data

schema = load_template("customer_data")
data = generate_data(schema, n_samples=1000, seed=42)
```

### Data Validation

```python
from synthetic_generator import validate_data

# Validate generated data
results = validate_data(data, schema)
print(f"Valid: {results['valid']}")
print(f"Errors: {results['errors']}")
print(f"Warnings: {results['warnings']}")
```

### Data Export

```python
from synthetic_generator.export import export_data

# Export to various formats
export_data(data, 'csv', filepath='data.csv')
export_data(data, 'json', filepath='data.json')
export_data(data, 'excel', filepath='data.xlsx')
export_data(data, 'parquet', filepath='data.parquet')
```

## 📊 Available Templates

- `customer_data`: Customer information with demographics
- `ecommerce_data`: E-commerce transaction data
- `medical_data`: Medical patient data with health metrics
- `financial_data`: Financial transaction data

## 📦 Package Information

- **PyPI**: https://pypi.org/project/synthetic-generator/
- **Version**: 0.0.8
- **Python**: 3.8+
- **Dependencies**: pandas, pydantic, numpy, scipy

## 🛠️ Development

### Installation for Development

```bash
git clone https://github.com/nhatkhangcs/synthetic_generator.git
cd synthetic_generator
make install_dev
```

### Running Tests

```bash
make test
```

### Running Examples

```bash
python examples/basic_usage.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/nhatkhangcs/synthetic_generator.git
cd synthetic_generator
make install_dev
```

## 📄 License

Synthetic Generator is released under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

## 🚀 Getting Started

For a quick start guide, see [QUICKSTART.md](QUICKSTART.md).

For detailed examples, check the [examples/](examples/) directory.

## 📞 Contact

**Vo Hoang Nhat Khang**  
**Maintainer & Developer**  
<small>Synthetic Generator - Python Package</small>

**Contact via:**
- **Email:** nhatkhangcs@gmail.com
- **GitHub:** [nhatkhangcs](https://github.com/nhatkhangcs)
- **PyPI:** [synthetic-generator](https://pypi.org/project/synthetic-generator/)

## 🙏 Acknowledgments

Thanks to all contributors and the open-source community for making this project possible.

---

Happy coding with Synthetic Generator! 🚀
