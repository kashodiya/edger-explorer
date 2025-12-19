#!/usr/bin/env python3
"""
Startup script for EDGAR Explorer
"""
import os
import sys
import subprocess

def main():
    # Check if EDGAR_IDENTITY is set
    if not os.getenv("EDGAR_IDENTITY"):
        print("⚠️  EDGAR_IDENTITY environment variable not set!")
        print("The SEC requires you to identify yourself when accessing their data.")
        print("\nPlease set your identity:")
        print("  export EDGAR_IDENTITY='Your Name your.email@example.com'")
        print("  # or on Windows:")
        print("  set EDGAR_IDENTITY=Your Name your.email@example.com")
        print("\nThen run: uv run python run.py")
        return 1
    
    print("🚀 Starting EDGAR Explorer...")
    print(f"📧 Using identity: {os.getenv('EDGAR_IDENTITY')}")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📊 Access the web interface in your browser")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        # Run the FastAPI server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down EDGAR Explorer...")
        return 0

if __name__ == "__main__":
    sys.exit(main())