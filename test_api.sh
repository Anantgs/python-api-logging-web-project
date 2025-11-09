#!/bin/bash

# Bash script to test the Log Generator Application API

BASE_URL="http://localhost:8080"

echo -e "\033[32mTesting Log Generator Application API...\033[0m"
echo ""

# Check if curl is available
if ! command -v curl &> /dev/null; then
    echo -e "\033[31mError: curl is not installed. Please install curl to run this test.\033[0m"
    exit 1
fi

# Test health endpoint
echo -e "\033[33m1. Testing health endpoint...\033[0m"
response=$(curl -s "$BASE_URL/api/health")
if [ $? -eq 0 ]; then
    echo -e "\033[36mHealth check: $response\033[0m"
else
    echo -e "\033[31mFailed to connect to health endpoint\033[0m"
    exit 1
fi

echo ""

# Test status endpoint  
echo -e "\033[33m2. Testing status endpoint...\033[0m"
response=$(curl -s "$BASE_URL/api/status")
if [ $? -eq 0 ]; then
    echo -e "\033[36mStatus: $response\033[0m"
else
    echo -e "\033[31mFailed to connect to status endpoint\033[0m"
fi

echo ""

# Test system info
echo -e "\033[33m3. Testing system info endpoint...\033[0m"
response=$(curl -s "$BASE_URL/api/system")
if [ $? -eq 0 ]; then
    echo -e "\033[36mSystem info: $response\033[0m"
else
    echo -e "\033[31mFailed to connect to system endpoint\033[0m"
fi

echo ""

# Test log info
echo -e "\033[33m4. Testing log info endpoint...\033[0m"
response=$(curl -s "$BASE_URL/api/logs/info")
if [ $? -eq 0 ]; then
    echo -e "\033[36mLog info: $response\033[0m"
else
    echo -e "\033[31mFailed to connect to log info endpoint\033[0m"
fi

echo ""

# Test stats
echo -e "\033[33m5. Testing stats endpoint...\033[0m"
response=$(curl -s "$BASE_URL/api/stats")
if [ $? -eq 0 ]; then
    echo -e "\033[36mStats: $response\033[0m"
else
    echo -e "\033[31mFailed to connect to stats endpoint\033[0m"
fi

echo ""

# Test start log generation
echo -e "\033[33m6. Testing start log generation...\033[0m"
response=$(curl -s -X POST "$BASE_URL/api/start")
if [ $? -eq 0 ]; then
    echo -e "\033[36mStart response: $response\033[0m"
else
    echo -e "\033[31mFailed to start log generation\033[0m"
fi

# Wait a bit
echo ""
echo -e "\033[33mWaiting 5 seconds for logs to generate...\033[0m"
sleep 5

# Check stats again
echo -e "\033[33m7. Checking stats after starting...\033[0m"
response=$(curl -s "$BASE_URL/api/stats")
if [ $? -eq 0 ]; then
    echo -e "\033[36mStats after start: $response\033[0m"
else
    echo -e "\033[31mFailed to get stats\033[0m"
fi

echo ""

# Test stop log generation
echo -e "\033[33m8. Testing stop log generation...\033[0m"
response=$(curl -s -X POST "$BASE_URL/api/stop")
if [ $? -eq 0 ]; then
    echo -e "\033[36mStop response: $response\033[0m"
else
    echo -e "\033[31mFailed to stop log generation\033[0m"
fi

echo ""
echo -e "\033[32mAPI testing completed!\033[0m"