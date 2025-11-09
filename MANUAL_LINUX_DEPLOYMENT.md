# Manual Linux Deployment Guide

This guide provides step-by-step manual commands to deploy and run the Python API Logging Web Project on Linux systems without using the automated scripts.

## Prerequisites

Ensure your Linux system has the following installed:
- Python 3.7 or higher
- pip3
- git
- curl (for testing)
- sudo access

### Check Prerequisites

```bash
# Check Python version
python3 --version

# Check pip3
pip3 --version

# Check git
git --version

# Check curl
curl --version
```

## Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Anantgs/python-api-logging-web-project.git

# Navigate to the project directory
cd python-api-logging-web-project

# List the project files
ls -la
```

## Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Verify virtual environment creation
ls -la venv/

# Activate virtual environment
source venv/bin/activate

# Verify activation (you should see (venv) in your prompt)
which python
which pip
```

## Step 3: Install Dependencies

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Verify installations
pip list

# Check specific packages
pip show flask
pip show psutil
```

## Step 4: Create Log Directory

```bash
# Create the log directory with sudo
sudo mkdir -p /var/log/python-api-logging

# Set ownership to current user
sudo chown $USER:$USER /var/log/python-api-logging

# Set proper permissions
sudo chmod 755 /var/log/python-api-logging

# Verify directory creation and permissions
ls -la /var/log/ | grep python-api-logging
```

## Step 5: Start the Application

```bash
# Make sure you're in the project directory
cd /path/to/python-api-logging-web-project

# Activate virtual environment if not already active
source venv/bin/activate

# Start the application
python3 app.py
```

The application should start and display:
```
Starting Log Generator Application...

The application will run on http://localhost:8080

Available API endpoints:
  GET  /                    - Home page
  GET  /api/status          - Application status
  GET  /api/stats           - Log generation statistics
  GET  /api/system          - System resource information
  GET  /api/logs/info       - Log files information
  GET  /api/health          - Health check
  POST /api/start           - Start log generation
  POST /api/stop            - Stop log generation

Press Ctrl+C to stop the application

 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://[your-ip]:8080
```

## Step 6: Test the Application (New Terminal)

Open a new terminal window and run these commands:

```bash
# Test health endpoint
curl http://localhost:8080/api/health

# Expected output:
# {"message":"Application is running","status":"healthy","timestamp":"2025-11-09T..."}

# Test status endpoint
curl http://localhost:8080/api/status

# Test system information
curl http://localhost:8080/api/system

# Test log information
curl http://localhost:8080/api/logs/info

# Start log generation
curl -X POST http://localhost:8080/api/start

# Check stats after starting
curl http://localhost:8080/api/stats

# Wait a few seconds and check stats again
sleep 5
curl http://localhost:8080/api/stats

# Stop log generation
curl -X POST http://localhost:8080/api/stop

# Access the web interface
curl http://localhost:8080/
```

## Step 7: Monitor Logs

```bash
# Check if logs are being created
ls -la /var/log/python-api-logging/

# Monitor real-time logs
tail -f /var/log/python-api-logging/app.log

# Check log file sizes
du -h /var/log/python-api-logging/*

# Count log entries
wc -l /var/log/python-api-logging/app.log
```

## Step 8: Stop the Application

In the terminal where the application is running:
```bash
# Press Ctrl+C to stop the application
^C
```

Or from another terminal:
```bash
# Find the process
ps aux | grep "python3 app.py"

# Kill the process (replace PID with actual process ID)
kill <PID>

# Or kill all python processes (be careful!)
pkill -f "python3 app.py"
```

## Advanced Manual Operations

### Running in Background

```bash
# Start application in background
nohup python3 app.py > /dev/null 2>&1 &

# Check if running
ps aux | grep "python3 app.py"

# Get process ID
pgrep -f "python3 app.py"

# Stop background process
pkill -f "python3 app.py"
```

### Using Screen/Tmux

#### Using Screen:
```bash
# Install screen if not available
sudo apt-get install screen  # Ubuntu/Debian
sudo yum install screen       # CentOS/RHEL

# Start screen session
screen -S api-logger

# In screen session, start the app
source venv/bin/activate
python3 app.py

# Detach from screen (Ctrl+A, then D)
# Reattach to screen
screen -r api-logger

# List screen sessions
screen -ls
```

#### Using Tmux:
```bash
# Install tmux if not available
sudo apt-get install tmux     # Ubuntu/Debian
sudo yum install tmux         # CentOS/RHEL

# Start tmux session
tmux new-session -d -s api-logger

# Send commands to tmux session
tmux send-keys -t api-logger "cd $(pwd)" Enter
tmux send-keys -t api-logger "source venv/bin/activate" Enter
tmux send-keys -t api-logger "python3 app.py" Enter

# Attach to tmux session
tmux attach-session -t api-logger

# List tmux sessions
tmux list-sessions
```

### Setting Up as System Service

```bash
# Create service file
sudo tee /etc/systemd/system/python-api-logging.service > /dev/null <<EOF
[Unit]
Description=Python API Logging Web Application
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable python-api-logging

# Start service
sudo systemctl start python-api-logging

# Check service status
sudo systemctl status python-api-logging

# View service logs
sudo journalctl -u python-api-logging -f

# Stop service
sudo systemctl stop python-api-logging

# Disable service
sudo systemctl disable python-api-logging
```

## Troubleshooting Commands

### Check Dependencies
```bash
# Check if all packages are installed
pip check

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Check Permissions
```bash
# Check log directory permissions
ls -la /var/log/ | grep python-api-logging

# Fix permissions if needed
sudo chown -R $USER:$USER /var/log/python-api-logging
sudo chmod -R 755 /var/log/python-api-logging
```

### Check Network/Port
```bash
# Check if port 8080 is in use
sudo netstat -tlnp | grep :8080

# Check if application is listening
sudo ss -tlnp | grep :8080

# Test local connectivity
telnet localhost 8080
```

### Monitor Resources
```bash
# Monitor CPU and memory usage
top
htop

# Check disk space
df -h
du -h /var/log/python-api-logging/

# Monitor specific process
ps aux | grep python3
```

### Log Analysis
```bash
# Check application logs
tail -n 100 /var/log/python-api-logging/app.log

# Search for errors
grep -i error /var/log/python-api-logging/app.log

# Check log rotation
ls -la /var/log/python-api-logging/

# Monitor log growth
watch -n 1 'ls -lh /var/log/python-api-logging/'
```

## Environment Variables (Optional)

```bash
# Set custom port
export PORT=8080

# Set custom log directory (not recommended, use default)
export LOG_DIR="/var/log/python-api-logging"

# Run with environment variables
PORT=9000 python3 app.py
```

## Cleanup Commands

```bash
# Stop application
pkill -f "python3 app.py"

# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv/

# Remove logs (be careful!)
sudo rm -rf /var/log/python-api-logging/

# Remove service file
sudo rm /etc/systemd/system/python-api-logging.service
sudo systemctl daemon-reload
```

This manual guide provides all the commands needed to deploy and manage the Python API Logging Web Project on Linux systems without relying on automated scripts.