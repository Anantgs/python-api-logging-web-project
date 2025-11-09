#!/usr/bin/env python3
"""
Demo script to show the log generation functionality
"""

import subprocess
import time
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError

def make_request(url, method='GET', data=None):
    """Make an HTTP request"""
    try:
        if method == 'POST':
            req = Request(url, data=b'', method='POST')
        else:
            req = Request(url, method=method)
            
        with urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error making request to {url}: {e}")
        return None

def format_bytes(bytes_value):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} TB"

def main():
    print("🚀 Log Generator Application Demo")
    print("=" * 50)
    
    # Start the application
    print("Starting the application...")
    cmd = [r"C:\Users\Dell\OneDrive\Desktop\TEST\.venv\Scripts\python.exe", "app.py"]
    app_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("Waiting 3 seconds for the application to start...")
    time.sleep(3)
    
    base_url = "http://localhost:8080"
    
    try:
        # Show initial status
        print("\n📊 Initial Status:")
        status = make_request(f"{base_url}/api/status")
        stats = make_request(f"{base_url}/api/stats")
        if status and stats:
            print(f"   Status: {status['status']}")
            print(f"   Logs generated: {stats['logs_generated']}")
            print(f"   Total size: {format_bytes(stats['total_log_size_bytes'])}")
        
        # Start log generation
        print("\n🏁 Starting log generation...")
        result = make_request(f"{base_url}/api/start", method='POST')
        if result:
            print(f"   Result: {result['message']}")
        
        # Monitor for 30 seconds
        print("\n📈 Monitoring log generation for 30 seconds...")
        print("   Time | Logs Generated | Total Size | Rate (MB/s)")
        print("   -----|----------------|------------|------------")
        
        for i in range(6):  # 6 intervals of 5 seconds each
            time.sleep(5)
            stats = make_request(f"{base_url}/api/stats")
            if stats:
                rate_mb_s = stats['current_log_rate_bytes_per_sec'] / (1024 * 1024)
                print(f"   {(i+1)*5:2d}s  | {stats['logs_generated']:14,} | {format_bytes(stats['total_log_size_bytes']):>10} | {rate_mb_s:8.2f}")
        
        # Show log files info
        print("\n📁 Log Files Information:")
        log_info = make_request(f"{base_url}/api/logs/info")
        if log_info:
            print(f"   Directory: {log_info['log_directory']}")
            print(f"   Total files: {log_info['total_files']}")
            print(f"   Total size: {format_bytes(log_info['total_size_bytes'])}")
            
            if log_info['files']:
                print("   Files:")
                for file_info in log_info['files'][:5]:  # Show first 5 files
                    print(f"     - {file_info['filename']}: {format_bytes(file_info['size_bytes'])}")
        
        # Show system impact
        print("\n💻 System Resource Usage:")
        system_info = make_request(f"{base_url}/api/system")
        if system_info:
            print(f"   CPU Usage: {system_info['cpu_percent']:.1f}%")
            print(f"   Memory Usage: {system_info['memory']['percent']:.1f}%")
            print(f"   Disk Usage: {system_info['disk']['percent']:.1f}%")
        
        # Stop log generation
        print("\n🛑 Stopping log generation...")
        result = make_request(f"{base_url}/api/stop", method='POST')
        if result:
            print(f"   Result: {result['message']}")
        
        # Final stats
        print("\n📊 Final Statistics:")
        stats = make_request(f"{base_url}/api/stats")
        if stats:
            print(f"   Total logs generated: {stats['logs_generated']:,}")
            print(f"   Total size: {format_bytes(stats['total_log_size_bytes'])}")
            print(f"   Target rate: {stats['target_rate_gb_per_minute']} GB/minute")
            
            # Calculate actual rate
            if stats['logs_generated'] > 0:
                actual_rate_mb_min = (stats['total_log_size_bytes'] / (1024**2)) * (60/30)  # 30 seconds of generation
                print(f"   Actual rate (projected): {actual_rate_mb_min:.2f} MB/minute")
        
        print("\n✅ Demo completed successfully!")
        print("\n💡 The application is designed to generate 0.01 GB (10 MB) of logs per minute.")
        print("   In this 30-second demo, it should have generated ~5 MB of logs.")
        print("   You can start the application manually and let it run longer to see the full 10 MB/minute rate.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
    finally:
        # Cleanup
        print("\n🧹 Stopping the application...")
        app_process.terminate()
        app_process.wait()
        print("   Application stopped.")

if __name__ == "__main__":
    main()