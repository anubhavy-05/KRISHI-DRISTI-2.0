@echo off
echo ==========================================
echo Checking Krishi Drishti Server Status
echo ==========================================
echo.

:: Check Backend (Port 8000)
netstat -ano | findstr :8000 >nul
if %errorlevel% equ 0 (
    echo ✅ Backend API: RUNNING on http://localhost:8000
) else (
    echo ❌ Backend API: NOT RUNNING
)

echo.

:: Check Dashboard (Port 8501)
netstat -ano | findstr :8501 >nul
if %errorlevel% equ 0 (
    echo ✅ Dashboard: RUNNING on http://localhost:8501
) else (
    echo ❌ Dashboard: NOT RUNNING
)

echo.
echo ==========================================
echo.

pause
