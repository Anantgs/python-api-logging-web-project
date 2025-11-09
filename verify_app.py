#!/usr/bin/env python3
"""
Simple verification script to test the application locally
"""

import subprocess
import time
import json
import sys
import threading
from urllib.request import urlopen
from urllib.error import URLError

def run_app():
    """Run the Flask application in a subprocess"""
    cmd = [r"C:\Users\Dell\OneDrive\Desktop\TEST\.venv\Scripts\python.exe", "app.py"]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def test_endpoint(url, description):
    """Test a single endpoint"""
    try:
        with urlopen(url) as response:
            data = json.loads(response.read().decode())
            print(f"✅ {description}: SUCCESS")
            print(f"   Response: {json.dumps(data, indent=2)}")
            return True
    except URLError as e:
        print(f"❌ {description}: FAILED - {e}")
        return False
    except Exception as e:
        print(f"❌ {description}: ERROR - {e}")
        return False

def main():
    print("Starting Log Generator Application Test...")
    print("=" * 50)
    
    # Start the application
    print("Starting the application...")
    app_process = run_app()
    
    # Wait for the application to start
    print("Waiting 5 seconds for the application to start...")
    time.sleep(5)
    
    # Test endpoints
    base_url = "http://localhost:8080"
    
    tests = [
        (f"{base_url}/", "Home endpoint"),
        (f"{base_url}/api/health", "Health check"),
        (f"{base_url}/api/status", "Status endpoint"),
        (f"{base_url}/api/stats", "Statistics endpoint"),
        (f"{base_url}/api/system", "System info endpoint"),
        (f"{base_url}/api/logs/info", "Log info endpoint"),
    ]
    
    print("\nTesting API endpoints...")
    print("-" * 30)
    
    success_count = 0
    for url, description in tests:
        if test_endpoint(url, description):
            success_count += 1
        print()
    
    print(f"Test Results: {success_count}/{len(tests)} endpoints working")
    
    # Cleanup
    print("Stopping the application...")
    app_process.terminate()
    app_process.wait()
    
    if success_count == len(tests):
        print("\n🎉 All tests passed! The application is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {len(tests) - success_count} tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())