@echo off
echo ==========================================
echo Starting Krishi Drishti Backend API
echo ==========================================
echo.

cd /d "%~dp0"

echo Starting FastAPI backend server...
echo API will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.

.venv\Scripts\python.exe backend\app.py

pause
