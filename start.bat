@echo off
cd /d "%~dp0"
echo.
echo =====================================
echo   KRISHI DRISHTI 2.0 - Quick Start
echo =====================================
echo.

REM Check if models exist
if not exist "all_crop_data.csv" (
    echo [1/3] Training models for first time...
    echo This will take 2-3 minutes...
    python more-advance-prediction.py
    timeout /t 5
    echo Models trained successfully!
) else (
    echo [✓] Models already trained
)

echo.
echo [2/3] Starting Backend API Server...
start "Krishi Drishti API" cmd /k "cd /d "%~dp0" && echo Starting FastAPI Backend... && python backend\app.py"

echo Waiting for backend to start...
timeout /t 5

echo.
echo [3/3] Starting Frontend Dashboard...
start "Krishi Drishti Dashboard" cmd /k "cd /d "%~dp0" && echo Starting Streamlit Dashboard... && python -m streamlit run frontend\dashboard.py"

echo.
echo =====================================
echo   SERVERS STARTED SUCCESSFULLY!
echo =====================================
echo.
echo Backend API:     http://localhost:8000
echo API Docs:        http://localhost:8000/docs
echo Dashboard:       http://localhost:8501
echo.
echo Press any key to close this window...
pause >nul
