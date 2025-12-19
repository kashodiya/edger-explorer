#!/usr/bin/env python3
"""
Setup script for EDGAR Explorer
"""
import os
import sys
import subprocess

def check_uv():
    """Check if UV is installed"""
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ UV is installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ UV is not installed")
    print("\nPlease install UV first:")
    print("  # On macOS and Linux:")
    print("  curl -LsSf https://astral.sh/uv/install.sh | sh")
    print("\n  # On Windows:")
    print("  powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"")
    return False

def setup_project():
    """Setup the project dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run(["uv", "sync"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_edgar_identity():
    """Check if EDGAR identity is set"""
    identity = os.getenv("EDGAR_IDENTITY")
    if identity:
        print(f"✅ EDGAR identity is set: {identity}")
        return True
    else:
        print("⚠️  EDGAR identity is not set")
        print("\nThe SEC requires you to identify yourself when accessing their data.")
        print("Please set the EDGAR_IDENTITY environment variable:")
        print("\n  # Linux/Mac:")
        print("  export EDGAR_IDENTITY='Your Name your.email@example.com'")
        print("\n  # Windows Command Prompt:")
        print("  set EDGAR_IDENTITY=Your Name your.email@example.com")
        print("\n  # Windows PowerShell:")
        print("  $env:EDGAR_IDENTITY='Your Name your.email@example.com'")
        return False

def main():
    print("🚀 Setting up EDGAR Explorer...")
    print("=" * 50)
    
    # Check UV installation
    if not check_uv():
        return 1
    
    # Setup project
    if not setup_project():
        return 1
    
    # Check EDGAR identity
    identity_set = check_edgar_identity()
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    
    if identity_set:
        print("\n🎉 You're ready to go! Run the application with:")
        print("  uv run python run.py")
    else:
        print("\n⚠️  Don't forget to set your EDGAR identity before running:")
        print("  export EDGAR_IDENTITY='Your Name your.email@example.com'")
        print("  uv run python run.py")
    
    print("\n📖 For more information, see README.md")
    return 0

if __name__ == "__main__":
    sys.exit(main())