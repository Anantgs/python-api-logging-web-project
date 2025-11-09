@echo off
echo Starting Log Generator Application...
echo.
echo The application will run on http://localhost:8080
echo.
echo Available API endpoints:
echo   GET  /                    - Home page
echo   GET  /api/status          - Application status
echo   GET  /api/stats           - Log generation statistics
echo   GET  /api/system          - System resource information
echo   GET  /api/logs/info       - Log files information
echo   GET  /api/health          - Health check
echo   POST /api/start           - Start log generation
echo   POST /api/stop            - Stop log generation
echo.
echo Press Ctrl+C to stop the application
echo.

C:\Users\Dell\OneDrive\Desktop\TEST\.venv\Scripts\python.exe app.py