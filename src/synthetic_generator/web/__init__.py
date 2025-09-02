"""
Web UI module for Synthetic Generator.

Provides a web interface for generating synthetic data with an intuitive
graphical interface.
"""

from .app import create_app, run_app
from .api import api_bp

__all__ = ["create_app", "run_app", "api_bp"]
