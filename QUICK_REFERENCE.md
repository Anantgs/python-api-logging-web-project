# Quick Reference - Manual Linux Commands

## Essential Setup Commands

```bash
# 1. Clone and navigate
git clone https://github.com/Anantgs/python-api-logging-web-project.git
cd python-api-logging-web-project

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create log directory
sudo mkdir -p /var/log/python-api-logging
sudo chown $USER:$USER /var/log/python-api-logging
sudo chmod 755 /var/log/python-api-logging

# 5. Start application
python3 app.py
```

## Testing Commands

```bash
# Health check
curl http://localhost:8080/api/health

# Start logging
curl -X POST http://localhost:8080/api/start

# Check stats
curl http://localhost:8080/api/stats

# Stop logging  
curl -X POST http://localhost:8080/api/stop
```

## Monitoring Commands

```bash
# Watch logs
tail -f /var/log/python-api-logging/app.log

# Check log size
du -h /var/log/python-api-logging/

# Monitor process
ps aux | grep "python3 app.py"
```

## Stop/Cleanup Commands

```bash
# Stop application (Ctrl+C or)
pkill -f "python3 app.py"

# Deactivate virtual environment
deactivate
```