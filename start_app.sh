#!/bin/bash

echo "Starting Log Generator Application..."
echo ""
echo "The application will run on http://localhost:8080"
echo ""
echo "Available API endpoints:"
echo "  GET  /                    - Home page"
echo "  GET  /api/status          - Application status"  
echo "  GET  /api/stats           - Log generation statistics"
echo "  GET  /api/system          - System resource information"
echo "  GET  /api/logs/info       - Log files information"
echo "  GET  /api/health          - Health check"
echo "  POST /api/start           - Start log generation"
echo "  POST /api/stop            - Stop log generation"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Create log directory if it doesn't exist (requires sudo)
if [ ! -d "/var/log/python-api-logging" ]; then
    echo "Creating log directory at /var/log/python-api-logging..."
    sudo mkdir -p /var/log/python-api-logging
    sudo chown $USER:$USER /var/log/python-api-logging
    sudo chmod 755 /var/log/python-api-logging
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Start the application
python3 app.py