@echo off
echo ==========================================
echo Starting Krishi Drishti Advanced Dashboard
echo ==========================================
echo.

cd /d "%~dp0"

echo Starting Streamlit dashboard...
echo Dashboard will open automatically in your browser
echo URL: http://localhost:8501
echo.

.venv\Scripts\python.exe -m streamlit run frontend\dashboard.py

pause
