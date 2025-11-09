#!/bin/bash

echo "Setting up Python API Logging Web Project for Linux..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt

# Create log directory with proper permissions
echo "Setting up log directory at /var/log/python-api-logging..."
sudo mkdir -p /var/log/python-api-logging
sudo chown $USER:$USER /var/log/python-api-logging
sudo chmod 755 /var/log/python-api-logging

# Make scripts executable
echo "Making scripts executable..."
chmod +x start_app.sh
chmod +x test_api.sh

echo ""
echo "Setup completed successfully!"
echo ""
echo "To run the application:"
echo "  ./start_app.sh"
echo ""
echo "To test the API:"
echo "  ./test_api.sh"
echo ""
echo "Note: The application will store logs in /var/log/python-api-logging/"