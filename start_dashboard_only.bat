@echo off
title Krishi Drishti - Dashboard  
color 0B
echo ======================================================================
echo   KRISHI DRISHTI - DASHBOARD
echo ======================================================================
echo.
echo   ⚠️  DO NOT CLOSE THIS WINDOW!
echo   This window must stay open for the dashboard to work.
echo.
echo   Starting dashboard...
echo ======================================================================
echo.

cd /d "%~dp0"
.venv\Scripts\python.exe -m streamlit run frontend\dashboard.py --server.headless true

echo.
echo ❌ Dashboard stopped!
echo.
pause
