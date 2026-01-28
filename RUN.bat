@echo off
REM Simple run script - Just double click this file!
cd /d "%~dp0"

echo Starting Backend...
start "Backend" cmd /k "python backend\app.py"

timeout /t 3

echo Starting Frontend...
start "Frontend" cmd /k "python -m streamlit run frontend\dashboard.py"

echo.
echo Both servers starting...
echo Backend: http://localhost:8000/docs
echo Dashboard: http://localhost:8501
timeout /t 5
