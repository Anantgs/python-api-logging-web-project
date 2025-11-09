# Log Generator Application

A Python Flask application that generates 0.01 GB (10 MB) of logs per minute and provides monitoring APIs. This application is designed to run on Linux systems and stores logs in `/var/log/python-api-logging/`.

## Features

- **Controlled log generation**: Generates approximately 0.01 GB (10 MB) of logs per minute
- **RESTful API**: Comprehensive monitoring endpoints
- **System monitoring**: CPU, memory, and disk usage information
- **Log file rotation**: Automatic rotation to prevent disk space issues
- **Real-time statistics**: Track log generation in real-time
- **Linux optimized**: Stores logs in standard Linux location (`/var/log/`)

## Requirements

- Linux operating system
- Python 3.7+
- Flask
- psutil
- sudo access (for creating log directory)

## Quick Setup

1. Run the automated setup script:
```bash
chmod +x setup_linux.sh
./setup_linux.sh
```

This will:
- Create a virtual environment
- Install Python dependencies
- Create the log directory at `/var/log/python-api-logging/`
- Set proper permissions
- Make scripts executable

## Manual Installation

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create log directory:
```bash
sudo mkdir -p /var/log/python-api-logging
sudo chown $USER:$USER /var/log/python-api-logging
sudo chmod 755 /var/log/python-api-logging
```

## Usage

1. Start the application using the startup script:
```bash
./start_app.sh
```

Or manually:
```bash
source venv/bin/activate
python3 app.py
```

2. The application will start on port 8080 and display available endpoints.

3. Test the API endpoints:
```bash
./test_api.sh
```

## API Endpoints

### Monitoring Endpoints

- **GET /** - Home page with basic information
- **GET /api/status** - Application status and uptime
- **GET /api/stats** - Log generation statistics
- **GET /api/system** - System resource information (CPU, memory, disk)
- **GET /api/logs/info** - Information about generated log files
- **GET /api/health** - Health check endpoint

### Control Endpoints

- **POST /api/start** - Start log generation
- **POST /api/stop** - Stop log generation

## API Examples

### Check Application Status
```bash
curl http://localhost:8080/api/status
```

### Get Log Statistics
```bash
curl http://localhost:8080/api/stats
```

### Start Log Generation
```bash
curl -X POST http://localhost:8080/api/start
```

### Stop Log Generation
```bash
curl -X POST http://localhost:8080/api/stop
```

### Get System Information
```bash
curl http://localhost:8080/api/system
```

### Get Log Files Information
```bash
curl http://localhost:8080/api/logs/info
```

## Response Examples

### Status Response
```json
{
  "status": "running",
  "start_time": "2025-11-09T10:30:00.123456",
  "uptime_seconds": 300.5
}
```

### Statistics Response
```json
{
  "logs_generated": 625,
  "total_log_size_bytes": 640000,
  "total_log_size_mb": 0.61,
  "total_log_size_gb": 0.0006,
  "current_log_rate_bytes_per_sec": 174.76,
  "target_rate_gb_per_minute": 0.01,
  "status": "running"
}
```

### System Information Response
```json
{
  "cpu_percent": 15.2,
  "memory": {
    "total": 17179869184,
    "available": 8589934592,
    "percent": 50.0,
    "used": 8589934592
  },
  "disk": {
    "total": 1000000000000,
    "used": 500000000000,
    "free": 500000000000,
    "percent": 50.0
  }
}
```

## Log File Management

- Log files are stored in the `logs/` directory
- Each log file is limited to 100MB before rotation
- Up to 20 backup files are kept
- Log files follow the naming pattern: `app.log`, `app.log.1`, `app.log.2`, etc.

## Performance Notes

- The application generates approximately 10,240 log entries per minute (1KB each)
- Each log entry is timestamped and contains random data to reach the target size
- Log generation runs in a separate thread to avoid blocking the API
- File rotation prevents individual log files from becoming too large

## Monitoring and Alerting

You can use the monitoring endpoints to:
- Track log generation progress
- Monitor system resource usage
- Set up alerts based on disk space or memory usage
- Verify the application is healthy and responding

## Security Considerations

- The application binds to all interfaces (0.0.0.0) for accessibility
- Consider adding authentication for production deployments
- Monitor disk space to prevent system issues from large log files
- Consider rate limiting for production environments

## Troubleshooting

1. **Port already in use**: Change the PORT variable in the code or kill the process using port 8080
2. **Permission errors**: Ensure the application has write permissions in the working directory
3. **Disk usage**: Monitor the `logs/` directory and adjust retention settings if needed
4. **CPU/Memory usage**: Moderate resource usage for 10 MB/minute generation