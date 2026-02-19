@echo off
title Krishi Drishti - Backend API Server
color 0A
echo ======================================================================
echo   KRISHI DRISHTI - BACKEND API SERVER
echo ======================================================================
echo.
echo   ⚠️  DO NOT CLOSE THIS WINDOW!
echo   This window must stay open for the system to work.
echo.
echo   Starting server...
echo ======================================================================
echo.

cd /d "%~dp0"
.venv\Scripts\python.exe backend\app.py

echo.
echo ❌ Server stopped!
echo.
pause
