@echo off
echo ==========================================
echo Starting Krishi Drishti Complete System
echo ==========================================
echo.
echo This will start:
echo 1. Backend API Server (Port 8000)
echo 2. Frontend Dashboard (Port 8501)
echo.
echo Please wait while both servers start...
echo.

cd /d "%~dp0"

:: Start backend in a new window
echo Starting Backend API...
start "Krishi Drishti Backend" cmd /k ".venv\Scripts\python.exe backend\app.py"

:: Wait 5 seconds for backend to start
timeout /t 5 /nobreak >nul

:: Start frontend in a new window
echo Starting Dashboard...
start "Krishi Drishti Dashboard" cmd /k ".venv\Scripts\python.exe -m streamlit run frontend\dashboard.py"

echo.
echo ==========================================
echo System Started Successfully!
echo ==========================================
echo Backend API: http://localhost:8000/docs
echo Dashboard: http://localhost:8501
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo ==========================================

pause
