@echo off
echo ==========================================
echo Stopping All Krishi Drishti Servers
echo ==========================================
echo.

:: Kill processes on port 8000 (Backend)
echo Stopping Backend (Port 8000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Killing process %%a
    taskkill /F /PID %%a 2>nul
)

echo.

:: Kill processes on port 8501 (Dashboard)
echo Stopping Dashboard (Port 8501)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501') do (
    echo Killing process %%a
    taskkill /F /PID %%a 2>nul
)

echo.
echo ✅ All servers stopped!
echo.

pause
