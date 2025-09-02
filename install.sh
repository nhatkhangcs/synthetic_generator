#!/bin/bash

# SynGen Installation Script
# This script installs all dependencies for the SynGen project

set -e  # Exit on any error

echo "🚀 Installing SynGen Dependencies"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install production dependencies
echo "📚 Installing production dependencies..."
pip install -r requirements/requirements.txt

# Install development dependencies (optional)
read -p "🤔 Do you want to install development dependencies? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔧 Installing development dependencies..."
    pip install -r requirements/requirements-dev.txt
fi

# Install the package in development mode
echo "📦 Installing SynGen in development mode..."
pip install -e .

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "🎯 Next steps:"
echo "   1. Activate the virtual environment: source .venv/bin/activate"
echo "   2. Run examples: python examples/basic_usage.py"
echo "   3. Run tests: python -m pytest tests/"
echo ""
echo "📖 For more information, see the README.md file" 