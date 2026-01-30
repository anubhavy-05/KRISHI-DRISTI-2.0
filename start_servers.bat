@echo off
REM =================================================================
REM KRISHI DRISHTI 2.0 - Start Both Servers
REM =================================================================

echo.
echo ====================================================================
echo       KRISHI DRISHTI 2.0 - Servers Start Ho Rahi Hain
echo ====================================================================
echo.

REM Check if dependencies are installed
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Dependencies install nahi hain!
    echo.
    echo Pehle setup.bat run karein:
    echo   double-click setup.bat
    echo.
    pause
    exit /b 1
)

echo [INFO] Starting Backend Server (Port 8000)...
echo [INFO] Starting Frontend Dashboard (Port 8501)...
echo.
echo ====================================================================
echo.
echo   Backend API:    http://localhost:8000
echo   API Docs:       http://localhost:8000/docs
echo   Dashboard:      http://localhost:8501
echo.
echo ====================================================================
echo.
echo [TIP] Dashboard browser mein automatically khul jayega!
echo [TIP] Band karne ke liye: Ctrl+C dono windows mein
echo.
echo ====================================================================
echo.

REM Start Backend in new window
start "BACKEND - Port 8000" cmd /k "cd /d %~dp0backend && echo [BACKEND] Starting FastAPI... && python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000"

REM Wait 5 seconds for backend to start
echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

REM Start Frontend in new window
start "FRONTEND - Port 8501" cmd /k "cd /d %~dp0frontend && echo [FRONTEND] Starting Streamlit Dashboard... && streamlit run dashboard.py"

echo.
echo ====================================================================
echo           Dono servers start ho gayi hain!
echo ====================================================================
echo.
echo Backend window aur Frontend window alag se khul gayi hain
echo Dashboard browser mein automatically khul jayega
echo.
echo [SUCCESS] Setup complete! Happy farming! 
echo.

REM Keep this window open
pause
