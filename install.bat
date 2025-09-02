@echo off
REM SynGen Installation Script for Windows
REM This script installs all dependencies for the SynGen project

echo 🚀 Installing SynGen Dependencies
echo ==================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python version: %PYTHON_VERSION%

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install production dependencies
echo 📚 Installing production dependencies...
pip install -r requirements\requirements.txt

REM Ask about development dependencies
set /p INSTALL_DEV="🤔 Do you want to install development dependencies? (y/n): "
if /i "%INSTALL_DEV%"=="y" (
    echo 🔧 Installing development dependencies...
    pip install -r requirements\requirements-dev.txt
)

REM Install the package in development mode
echo 📦 Installing SynGen in development mode...
pip install -e .

echo.
echo ✅ Installation completed successfully!
echo.
echo 🎯 Next steps:
echo    1. Activate the virtual environment: .venv\Scripts\activate
echo    2. Run examples: python examples\basic_usage.py
echo    3. Run tests: python -m pytest tests\
echo.
echo 📖 For more information, see the README.md file
pause 