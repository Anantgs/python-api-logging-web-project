# PowerShell script to test the Log Generator Application API

$baseUrl = "http://localhost:8080"

Write-Host "Testing Log Generator Application API..." -ForegroundColor Green
Write-Host ""

try {
    # Test health endpoint
    Write-Host "1. Testing health endpoint..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "$baseUrl/api/health" -Method Get
    Write-Host "Health check: $($response | ConvertTo-Json -Compress)" -ForegroundColor Cyan
    
    # Test status endpoint
    Write-Host ""
    Write-Host "2. Testing status endpoint..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "$baseUrl/api/status" -Method Get
    Write-Host "Status: $($response | ConvertTo-Json -Compress)" -ForegroundColor Cyan
    
    # Test system info
    Write-Host ""
    Write-Host "3. Testing system info endpoint..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "$baseUrl/api/system" -Method Get
    Write-Host "CPU: $($response.cpu_percent)%" -ForegroundColor Cyan
    Write-Host "Memory: $($response.memory.percent)%" -ForegroundColor Cyan
    Write-Host "Disk: $([math]::Round($response.disk.percent, 1))%" -ForegroundColor Cyan
    
    # Start log generation
    Write-Host ""
    Write-Host "4. Starting log generation..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "$baseUrl/api/start" -Method Post
    Write-Host "Start logging: $($response | ConvertTo-Json -Compress)" -ForegroundColor Cyan
    
    # Wait and check stats
    Write-Host ""
    Write-Host "5. Waiting 10 seconds to check statistics..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    $response = Invoke-RestMethod -Uri "$baseUrl/api/stats" -Method Get
    Write-Host "Logs generated: $($response.logs_generated)" -ForegroundColor Cyan
    Write-Host "Total size: $($response.total_log_size_mb) MB" -ForegroundColor Cyan
    Write-Host "Rate: $([math]::Round($response.current_log_rate_bytes_per_sec, 2)) bytes/sec" -ForegroundColor Cyan
    
    # Check log files
    Write-Host ""
    Write-Host "6. Checking log files..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "$baseUrl/api/logs/info" -Method Get
    Write-Host "Total files: $($response.total_files)" -ForegroundColor Cyan
    Write-Host "Total size: $($response.total_size_mb) MB" -ForegroundColor Cyan
    
    # Stop log generation
    Write-Host ""
    Write-Host "7. Stopping log generation..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "$baseUrl/api/stop" -Method Post
    Write-Host "Stop logging: $($response | ConvertTo-Json -Compress)" -ForegroundColor Cyan
    
    Write-Host ""
    Write-Host "✅ All tests completed successfully!" -ForegroundColor Green
    
} catch {
    Write-Host ""
    Write-Host "❌ Error: Could not connect to the application." -ForegroundColor Red
    Write-Host "Make sure the application is running on port 8080." -ForegroundColor Red
    Write-Host "Run: .\start_app.bat or python app.py" -ForegroundColor Red
}