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

:: Kill any existing processes on these ports
echo Checking for existing processes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501') do taskkill /F /PID %%a 2>nul
timeout /t 2 /nobreak >nul

:: Start backend in a new window - KEEP WINDOW OPEN
echo Starting Backend API...
start "Krishi Drishti Backend - DO NOT CLOSE" cmd /k "cd /d "%~dp0" && .venv\Scripts\python.exe backend\app.py"

:: Wait 5 seconds for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

:: Start frontend in a new window - KEEP WINDOW OPEN
echo Starting Dashboard...
start "Krishi Drishti Dashboard - DO NOT CLOSE" cmd /k "cd /d "%~dp0" && .venv\Scripts\python.exe -m streamlit run frontend\dashboard.py --server.headless true"

:: Wait a bit for dashboard to start
timeout /t 3 /nobreak >nul

echo.
echo ==========================================
echo System Started Successfully!
echo ==========================================
echo Backend API: http://localhost:8000/docs
echo Dashboard: http://localhost:8501
echo.
echo ⚠️  IMPORTANT: DO NOT CLOSE THE TWO NEW WINDOWS!
echo    - "Krishi Drishti Backend" window
echo    - "Krishi Drishti Dashboard" window
echo.
echo To stop the servers: Close those two windows
echo or press Ctrl+C in each window
echo ==========================================
echo.
echo Opening dashboard in your browser...
timeout /t 2 /nobreak >nul
start http://localhost:8501

pause
