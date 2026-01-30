@echo off
REM Quick Health Check - Backend & Frontend

echo.
echo ========================================
echo   Testing Backend API...
echo ========================================
echo.

curl -s http://localhost:8000/ 2>nul
if errorlevel 1 (
    echo [X] Backend NOT running on port 8000
    echo.
    echo Start backend first:
    echo   cd backend
    echo   python -m uvicorn app:app --reload
    echo.
) else (
    echo [✓] Backend is RUNNING on port 8000
    echo.
)

echo ========================================
echo   Testing Frontend Dashboard...
echo ========================================
echo.

curl -s http://localhost:8501/ 2>nul
if errorlevel 1 (
    echo [X] Frontend NOT running on port 8501
    echo.
    echo Start frontend:
    echo   cd frontend
    echo   streamlit run dashboard.py
    echo.
) else (
    echo [✓] Frontend is RUNNING on port 8501
    echo.
)

echo ========================================
echo   Summary
echo ========================================
echo.
echo If both are running:
echo   - Backend:  http://localhost:8000/docs
echo   - Frontend: http://localhost:8501
echo.

pause
