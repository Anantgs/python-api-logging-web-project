# Linux Deployment Guide

This guide covers deploying the Python API Logging Web Project on Linux systems.

## System Requirements

- Linux distribution (Ubuntu, CentOS, RHEL, Debian, etc.)
- Python 3.7 or higher
- pip3
- sudo access (for initial setup)
- curl (for testing)

## Quick Deployment

1. Clone the repository:
```bash
git clone https://github.com/Anantgs/python-api-logging-web-project.git
cd python-api-logging-web-project
```

2. Run the setup script:
```bash
chmod +x setup_linux.sh
./setup_linux.sh
```

3. Start the application:
```bash
./start_app.sh
```

4. Test the application (in another terminal):
```bash
./test_api.sh
```

## Log Storage

The application stores logs in `/var/log/python-api-logging/` following Linux standards:

- **Main log file**: `/var/log/python-api-logging/app.log`
- **Rotated logs**: `/var/log/python-api-logging/app.log.1`, `app.log.2`, etc.
- **Maximum size**: 100MB per file
- **Retention**: 20 backup files (total ~2GB of logs)

## Permissions

The setup script automatically configures the necessary permissions:

```bash
sudo mkdir -p /var/log/python-api-logging
sudo chown $USER:$USER /var/log/python-api-logging
sudo chmod 755 /var/log/python-api-logging
```

## Service Management (Optional)

To run as a system service, create a systemd service file:

```bash
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
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable python-api-logging
sudo systemctl start python-api-logging
```

Check service status:
```bash
sudo systemctl status python-api-logging
```

## Monitoring

- **Application logs**: Check `/var/log/python-api-logging/app.log`
- **Service logs**: `sudo journalctl -u python-api-logging -f`
- **API health**: `curl http://localhost:8080/api/health`

## Firewall Configuration

If using a firewall, allow port 8080:

```bash
# UFW (Ubuntu)
sudo ufw allow 8080

# firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
```

## Troubleshooting

1. **Permission denied for log directory**:
   ```bash
   sudo chown $USER:$USER /var/log/python-api-logging
   ```

2. **Port already in use**:
   ```bash
   sudo netstat -tlnp | grep :8080
   sudo pkill -f "python.*app.py"
   ```

3. **Python module not found**:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Security Notes

- The application runs on port 8080 by default
- Log files are stored with user ownership in `/var/log/`
- Consider using a reverse proxy (nginx/apache) for production
- Implement SSL/TLS for production deployments