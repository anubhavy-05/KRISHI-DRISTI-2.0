@echo off
REM =================================================================
REM KRISHI DRISHTI 2.0 - Complete Setup Script
REM =================================================================

echo.
echo ====================================================================
echo          KRISHI DRISHTI 2.0 - Setup Kar Rahe Hain
echo ====================================================================
echo.

REM Check Python installed hai ya nahi
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python installed nahi hai!
    echo Python download karein: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Python version check...
python --version
echo.

REM Backend dependencies install
echo [2/4] Backend dependencies install kar rahe hain...
echo.
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Backend dependencies install nahi hui!
    pause
    exit /b 1
)
cd ..
echo.
echo [SUCCESS] Backend dependencies installed!
echo.

REM Frontend dependencies install
echo [3/4] Frontend dependencies install kar rahe hain...
echo.
cd frontend
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Frontend dependencies install nahi hui!
    pause
    exit /b 1
)
cd ..
echo.
echo [SUCCESS] Frontend dependencies installed!
echo.

REM Check if models exist
echo [4/4] ML Models check kar rahe hain...
echo.
if not exist "all_crop_data.csv" (
    echo [INFO] all_crop_data.csv nahi mili, pehli baar training hogi...
    echo [INFO] Ye kuch time le sakta hai...
    echo.
)

if not exist "wheat_uttar_pradesh_price_model.joblib" (
    echo [INFO] Models nahi mile, training karni padegi...
    echo [INFO] Jab aap server start karenge, models automatically train honge
    echo.
) else (
    echo [SUCCESS] ML Models already trained hain!
    echo.
)

echo ====================================================================
echo                    SETUP COMPLETE!
echo ====================================================================
echo.
echo Ab aap project start kar sakte ho:
echo.
echo   Option 1: Automated Start (Recommended)
echo   -----------------------------------------
echo   Double-click:  start_servers.bat
echo.
echo   Option 2: Manual Start
echo   -----------------------------------------
echo   Terminal 1:  cd backend && python -m uvicorn app:app --reload
echo   Terminal 2:  cd frontend && streamlit run dashboard.py
echo.
echo ====================================================================
echo.

pause
