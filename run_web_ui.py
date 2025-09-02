#!/usr/bin/env python3
"""
Simple launcher script for Synthetic Generator Web UI.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.synthetic_generator.web import run_app

if __name__ == "__main__":
    print("🚀 Starting Synthetic Generator Web UI...")
    print("📊 Dashboard will be available at: http://localhost:8000")
    print("🔧 API endpoints at: http://localhost:8000/api")
    print("📚 Documentation at: http://localhost:8000/about")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)

    try:
        run_app(host="0.0.0.0", port=8000, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Synthetic Generator Web UI...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting web UI: {e}")
        sys.exit(1)
