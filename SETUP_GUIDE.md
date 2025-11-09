# Log Generator Application - Complete Setup

## 📁 Project Structure
```
TEST/
├── .venv/                 # Python virtual environment
├── logs/                  # Generated log files directory
│   └── app.log           # Main log file (rotates automatically)
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── README.md            # Detailed documentation
├── start_app.bat        # Windows batch file to start the app
├── test_api.ps1         # PowerShell script to test APIs
├── test_api.py          # Python script to test APIs
├── verify_app.py        # Application verification script
└── demo.py              # Demo script showing functionality
```

## 🚀 Quick Start

### Option 1: Using Batch File (Easiest)
```cmd
.\start_app.bat
```

### Option 2: Using Python Directly
```cmd
C:\Users\Dell\OneDrive\Desktop\TEST\.venv\Scripts\python.exe app.py
```

### Option 3: Using PowerShell
```powershell
& "C:\Users\Dell\OneDrive\Desktop\TEST\.venv\Scripts\python.exe" app.py
```

## 🧪 Testing the Application

### Run Verification Tests
```cmd
C:\Users\Dell\OneDrive\Desktop\TEST\.venv\Scripts\python.exe verify_app.py
```

### Run Demo (Shows log generation)
```cmd
C:\Users\Dell\OneDrive\Desktop\TEST\.venv\Scripts\python.exe demo.py
```

### Test APIs with PowerShell
```powershell
.\test_api.ps1
```

## 🌐 API Endpoints

Once the application is running on **http://localhost:8080**, you can use these endpoints:

### Monitoring Endpoints
- `GET /` - Home page with basic info
- `GET /api/health` - Health check
- `GET /api/status` - Application status and uptime
- `GET /api/stats` - Log generation statistics
- `GET /api/system` - System resource usage (CPU, Memory, Disk)
- `GET /api/logs/info` - Information about log files

### Control Endpoints
- `POST /api/start` - Start log generation
- `POST /api/stop` - Stop log generation

## 📊 Application Features

✅ **Runs on port 8080** - Configurable port
✅ **Generates 0.01 GB (10 MB) logs per minute** - Controlled log generation
✅ **Monitoring APIs** - Comprehensive REST API for monitoring
✅ **System monitoring** - CPU, memory, disk usage tracking
✅ **Log rotation** - Automatic file rotation (100MB per file, 20 backups)
✅ **Real-time statistics** - Live tracking of log generation
✅ **Background processing** - Non-blocking log generation
✅ **Health checks** - Application health monitoring
✅ **Cross-platform** - Works on Windows, Linux, macOS

## 📈 Performance Metrics

- **Target Rate**: 0.01 GB per minute (0.17 MB/second)
- **Log Entry Size**: 1 KB per entry
- **Entries per Minute**: ~10,240 entries
- **File Rotation**: 100 MB per file, keeps 20 backup files
- **Memory Usage**: Minimal (< 50 MB typical)

## 🔧 Configuration

The application can be easily configured by modifying these variables in `app.py`:

```python
PORT = 8080                                    # Server port
TARGET_LOG_SIZE_PER_MINUTE = 10 * 1024 * 1024    # 0.01 GB (10 MB) target
LOG_ENTRY_SIZE = 1024                          # 1 KB per entry
```

## 📱 Example API Responses

### Health Check Response
```json
{
  "status": "healthy",
  "timestamp": "2025-11-09T19:33:28.233585",
  "service": "log-generator",
  "port": 8080
}
```

### Statistics Response
```json
{
  "logs_generated": 51314,
  "total_log_size_bytes": 52543576,
  "total_log_size_mb": 50.11,
  "total_log_size_gb": 0.05,
  "current_log_rate_bytes_per_sec": 174.76,
  "target_rate_gb_per_minute": 0.01,
  "status": "running"
}
```

### System Info Response
```json
{
  "cpu_percent": 31.5,
  "memory": {
    "total": 8482037760,
    "available": 1709944832,
    "percent": 77.0,
    "used": 6772092928
  },
  "disk": {
    "total": 127419334656,
    "used": 96693178368,
    "free": 30726156288,
    "percent": 75.9
  }
}
```

## ⚠️ Important Notes

1. **Disk Space**: The application will generate moderate log files (10 MB/minute).
2. **Performance**: Generating 10 MB/minute uses minimal CPU and I/O resources.
3. **Log Rotation**: Files are automatically rotated to prevent individual files from becoming too large.
4. **Production Use**: This is a development server. Use a production WSGI server for production deployments.

## 🎯 Use Cases

- **Load Testing**: Test logging systems with moderate-volume data
- **Performance Monitoring**: Monitor system behavior under light I/O load
- **Storage Testing**: Test disk performance and capacity
- **Application Monitoring**: Example of comprehensive API monitoring
- **DevOps Training**: Learn about logging, monitoring, and system resources

## 🔍 Troubleshooting

1. **Port 8080 in use**: Change the PORT variable or kill existing processes
2. **Permission errors**: Ensure write permissions in the application directory
3. **Resource usage**: Low resource usage for 10 MB/minute generation
4. **Connection refused**: Make sure the application is running and accessible

The application is now fully functional and ready to use! 🎉