#!/usr/bin/env python3
"""
Fog Computing Simulator - Web Interface Startup Script
=====================================================

This script starts the web interface for the fog computing simulation platform.
It handles dependency installation, configuration setup, and server startup.
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required Python packages."""
    print("\n📦 Installing Python dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_configuration():
    """Setup configuration files."""
    print("\n🔧 Setting up configuration...")
    
    # Copy config.json from parent directory if it exists
    parent_config = Path("../config.json")
    if parent_config.exists():
        import shutil
        shutil.copy(parent_config, "config.json")
        print("✅ Configuration copied from parent directory")
    else:
        print("ℹ️  Using default configuration")
    
    return True

def start_server():
    """Start the Flask server."""
    print("\n🚀 Starting Fog Computing Simulator Web Interface")
    print("=" * 60)
    print("📡 Server will be available at: http://localhost:5000")
    print("🌐 Web interface will open automatically")
    print("\n💡 Features available:")
    print("   • Real-time simulation control")
    print("   • Interactive configuration management")
    print("   • Live performance monitoring")
    print("   • Advanced analytics and visualization")
    print("   • Node failure simulation")
    print("   • Comprehensive documentation")
    print("\n🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Start the Flask app
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        return False

def open_browser():
    """Open web browser after a short delay."""
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Web interface opened in browser")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("   Please open http://localhost:5000 manually")

def main():
    """Main startup function."""
    print("🌐 Fog Computing Simulator - Web Interface")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    # Setup configuration
    if not setup_configuration():
        return 1
    
    # Start browser in background thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start server
    try:
        start_server()
        return 0
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
