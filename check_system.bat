@echo off
echo ==========================================
echo Krishi Drishti - System Check
echo ==========================================
echo.
echo Checking dependencies...
echo.

cd /d "%~dp0"

echo [1/3] Checking Python environment...
.venv\Scripts\python.exe --version
if %errorlevel% neq 0 (
    echo ❌ Python environment not found!
    pause
    exit /b 1
)
echo ✅ Python environment OK
echo.

echo [2/3] Checking backend packages...
.venv\Scripts\python.exe -c "import fastapi, uvicorn, pandas, sklearn, joblib; print('✅ Backend packages OK')"
if %errorlevel% neq 0 (
    echo ❌ Backend packages missing! Run: .venv\Scripts\python.exe -m pip install -r backend\requirements.txt
    pause
    exit /b 1
)
echo.

echo [3/3] Checking frontend packages...
.venv\Scripts\python.exe -c "import streamlit, plotly; print('✅ Frontend packages OK')"
if %errorlevel% neq 0 (
    echo ❌ Frontend packages missing! Installing now...
    .venv\Scripts\python.exe -m pip install streamlit plotly
)
echo.

echo ==========================================
echo ✅ ALL CHECKS PASSED!
echo ==========================================
echo.
echo Your system is ready to run!
echo.
echo Quick Start:
echo   - Run complete system: run_complete_system.bat
echo   - Backend only: run_backend.bat
echo   - Dashboard only: run_dashboard.bat
echo.

pause
