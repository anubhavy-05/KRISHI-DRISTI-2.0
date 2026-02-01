@echo off
REM ==============================================================
REM   KRISHI DRISHTI 2.0 - Quick Start (Simple Version)
REM ==============================================================

echo.
echo ==============================================================
echo          KRISHI DRISHTI 2.0 - Starting Servers
echo ==============================================================
echo.

REM Start Backend
echo [1/2] Starting Backend API (Port 8000)...
start "Backend API - Port 8000" cmd /c "cd /d %~dp0backend && python app.py"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend
echo [2/2] Starting Frontend Dashboard (Port 8501)...
start "Frontend Dashboard - Port 8501" cmd /c "cd /d %~dp0frontend && python -m streamlit run dashboard.py"

REM Wait for frontend to start  
timeout /t 5 /nobreak >nul

echo.
echo ==============================================================
echo                   SERVERS STARTED!
echo ==============================================================
echo.
echo   Backend API:      http://localhost:8000
echo   API Docs:         http://localhost:8000/docs
echo   Dashboard:        http://localhost:8501
echo.
echo   Terminal windows opened separately.
echo   Browser will open automatically in 5-10 seconds!
echo.
echo   To stop: Close both terminal windows or press Ctrl+C
echo ==============================================================
echo.

REM Open browser after 8 seconds
timeout /t 8 /nobreak >nul
start http://localhost:8501

echo.
echo [SUCCESS] Dashboard opened in browser!
echo.
pause
