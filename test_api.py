#!/usr/bin/env python3
"""
Test script for the Log Generator Application
"""

import requests
import time
import json

BASE_URL = "http://localhost:8080"

def test_api():
    """Test the API endpoints"""
    print("Testing Log Generator Application API...")
    
    try:
        # Test health endpoint
        print("\n1. Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        
        # Test status endpoint
        print("\n2. Testing status endpoint...")
        response = requests.get(f"{BASE_URL}/api/status")
        print(f"Status: {response.status_code} - {response.json()}")
        
        # Test system info
        print("\n3. Testing system info endpoint...")
        response = requests.get(f"{BASE_URL}/api/system")
        system_info = response.json()
        print(f"System info: {response.status_code}")
        print(f"  CPU: {system_info.get('cpu_percent', 'N/A')}%")
        print(f"  Memory: {system_info.get('memory', {}).get('percent', 'N/A')}%")
        print(f"  Disk: {system_info.get('disk', {}).get('percent', 'N/A'):.1f}%")
        
        # Start log generation
        print("\n4. Starting log generation...")
        response = requests.post(f"{BASE_URL}/api/start")
        print(f"Start logging: {response.status_code} - {response.json()}")
        
        # Wait a bit and check stats
        print("\n5. Waiting 10 seconds to check statistics...")
        time.sleep(10)
        
        response = requests.get(f"{BASE_URL}/api/stats")
        stats = response.json()
        print(f"Statistics: {response.status_code}")
        print(f"  Logs generated: {stats.get('logs_generated', 'N/A')}")
        print(f"  Total size: {stats.get('total_log_size_mb', 'N/A')} MB")
        print(f"  Rate: {stats.get('current_log_rate_bytes_per_sec', 'N/A'):.2f} bytes/sec")
        
        # Check log files
        print("\n6. Checking log files...")
        response = requests.get(f"{BASE_URL}/api/logs/info")
        log_info = response.json()
        print(f"Log files: {response.status_code}")
        print(f"  Total files: {log_info.get('total_files', 'N/A')}")
        print(f"  Total size: {log_info.get('total_size_mb', 'N/A')} MB")
        
        # Stop log generation
        print("\n7. Stopping log generation...")
        response = requests.post(f"{BASE_URL}/api/stop")
        print(f"Stop logging: {response.status_code} - {response.json()}")
        
        print("\n✅ All tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the application.")
        print("Make sure the application is running on port 8080.")
        print("Run: python app.py")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_api()