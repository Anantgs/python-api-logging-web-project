import asyncio
import logging
import os
import time
import threading
import psutil
from datetime import datetime
from flask import Flask, jsonify, render_template, request
from logging.handlers import RotatingFileHandler
import random
import string

app = Flask(__name__)

# Configuration
PORT = 8080
LOG_DIR = "/var/log/python-api-logging"
LOG_FILE = os.path.join(LOG_DIR, "app.log")
TARGET_LOG_SIZE_PER_MINUTE = 10 * 1024 * 1024  # 0.01 GB (10 MB) in bytes
LOG_ENTRY_SIZE = 1024  # Size of each log entry in bytes

# Application statistics
app_stats = {
    "start_time": None,
    "logs_generated": 0,
    "total_log_size": 0,
    "current_log_rate": 0,
    "status": "stopped"
}

class LogGenerator:
    def __init__(self):
        self.running = False
        self.thread = None
        
    def setup_logging(self):
        """Setup logging configuration"""
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
            
        # Create a custom logger
        self.logger = logging.getLogger('AppLogger')
        self.logger.setLevel(logging.INFO)
        
        # Create rotating file handler (100MB per file, keep 20 files)
        handler = RotatingFileHandler(
            LOG_FILE, 
            maxBytes=100*1024*1024,  # 100MB
            backupCount=20
        )
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(handler)
        
    def generate_log_entry(self, size):
        """Generate a log entry of specified size"""
        # Generate random string to fill the log entry
        base_message = "Application log entry - "
        remaining_size = size - len(base_message) - 100  # Leave space for timestamp and formatting
        
        if remaining_size > 0:
            random_data = ''.join(random.choices(string.ascii_letters + string.digits, k=remaining_size))
            return f"{base_message}{random_data}"
        else:
            return base_message
            
    def log_generation_worker(self):
        """Worker thread for generating logs"""
        entries_per_minute = TARGET_LOG_SIZE_PER_MINUTE // LOG_ENTRY_SIZE
        interval = 60.0 / entries_per_minute  # Time between log entries
        
        self.logger.info("Log generation started")
        
        while self.running:
            start_time = time.time()
            
            # Generate log entry
            log_message = self.generate_log_entry(LOG_ENTRY_SIZE)
            self.logger.info(log_message)
            
            # Update statistics
            app_stats["logs_generated"] += 1
            app_stats["total_log_size"] += LOG_ENTRY_SIZE
            app_stats["current_log_rate"] = LOG_ENTRY_SIZE / interval  # bytes per second
            
            # Sleep to maintain the target rate
            elapsed = time.time() - start_time
            sleep_time = max(0, interval - elapsed)
            time.sleep(sleep_time)
            
    def start(self):
        """Start log generation"""
        if not self.running:
            self.setup_logging()
            self.running = True
            app_stats["status"] = "running"
            app_stats["start_time"] = datetime.now().isoformat()
            self.thread = threading.Thread(target=self.log_generation_worker, daemon=True)
            self.thread.start()
            
    def stop(self):
        """Stop log generation"""
        self.running = False
        app_stats["status"] = "stopped"
        if self.thread:
            self.thread.join(timeout=1)

# Global log generator instance
log_generator = LogGenerator()

# Web Routes
@app.route('/')
def home():
    """Home page with web interface"""
    return render_template('index.html', stats=app_stats)

@app.route('/api/status')
def get_status():
    """Get application status"""
    return jsonify({
        "status": app_stats["status"],
        "start_time": app_stats["start_time"],
        "uptime_seconds": (
            (datetime.now() - datetime.fromisoformat(app_stats["start_time"])).total_seconds()
            if app_stats["start_time"] else 0
        )
    })

@app.route('/api/stats')
def get_stats():
    """Get application statistics"""
    return jsonify({
        "logs_generated": app_stats["logs_generated"],
        "total_log_size_bytes": app_stats["total_log_size"],
        "total_log_size_mb": round(app_stats["total_log_size"] / (1024 * 1024), 2),
        "total_log_size_gb": round(app_stats["total_log_size"] / (1024 * 1024 * 1024), 2),
        "current_log_rate_bytes_per_sec": app_stats["current_log_rate"],
        "target_rate_gb_per_minute": 0.01,
        "status": app_stats["status"]
    })

@app.route('/api/system')
def get_system_info():
    """Get system resource information"""
    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "percent": psutil.virtual_memory().percent,
            "used": psutil.virtual_memory().used
        },
        "disk": {
            "total": psutil.disk_usage('.').total,
            "used": psutil.disk_usage('.').used,
            "free": psutil.disk_usage('.').free,
            "percent": (psutil.disk_usage('.').used / psutil.disk_usage('.').total) * 100
        }
    })

@app.route('/api/logs/info')
def get_log_info():
    """Get information about log files"""
    log_files = []
    total_size = 0
    
    if os.path.exists(LOG_DIR):
        for filename in os.listdir(LOG_DIR):
            if filename.startswith('app.log'):
                filepath = os.path.join(LOG_DIR, filename)
                if os.path.isfile(filepath):
                    size = os.path.getsize(filepath)
                    total_size += size
                    log_files.append({
                        "filename": filename,
                        "size_bytes": size,
                        "size_mb": round(size / (1024 * 1024), 2),
                        "modified": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                    })
    
    return jsonify({
        "log_directory": LOG_DIR,
        "total_files": len(log_files),
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "total_size_gb": round(total_size / (1024 * 1024 * 1024), 2),
        "files": log_files
    })

@app.route('/api/start', methods=['POST'])
def start_logging():
    """Start log generation"""
    if app_stats["status"] == "running":
        return jsonify({"message": "Log generation is already running"}), 400
    
    log_generator.start()
    return jsonify({"message": "Log generation started", "status": app_stats["status"]})

@app.route('/api/stop', methods=['POST'])
def stop_logging():
    """Stop log generation"""
    if app_stats["status"] == "stopped":
        return jsonify({"message": "Log generation is already stopped"}), 400
    
    log_generator.stop()
    return jsonify({"message": "Log generation stopped", "status": app_stats["status"]})

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "log-generator",
        "port": PORT
    })

if __name__ == '__main__':
    print(f"Starting Log Generator Application on port {PORT}")
    print(f"Target log generation rate: 0.01 GB (10 MB) per minute")
    print(f"Log entry size: {LOG_ENTRY_SIZE} bytes")
    print(f"Estimated entries per minute: {TARGET_LOG_SIZE_PER_MINUTE // LOG_ENTRY_SIZE}")
    print("\nAvailable API endpoints:")
    print("  GET  /                    - Home page")
    print("  GET  /api/status          - Application status")
    print("  GET  /api/stats           - Log generation statistics")
    print("  GET  /api/system          - System resource information")
    print("  GET  /api/logs/info       - Log files information")
    print("  GET  /api/health          - Health check")
    print("  POST /api/start           - Start log generation")
    print("  POST /api/stop            - Stop log generation")
    
    # Start the Flask application
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)