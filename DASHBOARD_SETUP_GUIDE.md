# 🌾 Krishi Drishti Advanced Dashboard - Quick Start Guide

## ✅ Fixed Issues:
1. ✓ Fixed syntax error in `more-advance-prediction.py` (Line 1: "Rimport" → "import")
2. ✓ Installed all required dependencies (Python packages)
3. ✓ Created easy-to-use launch scripts

## 📝 How to Run the Advanced Dashboard System:

### Option 1: Run Complete System (Recommended)
Double-click: **`run_complete_system.bat`**
- This starts both Backend API AND Frontend Dashboard automatically
- Backend API: http://localhost:8000/docs
- Dashboard: http://localhost:8501

### Option 2: Run Components Separately

**Step 1: Start Backend API**
- Double-click: `run_backend.bat`
- API will be available at: http://localhost:8000
- API Documentation: http://localhost:8000/docs

**Step 2: Start Frontend Dashboard**  
- Double-click: `run_dashboard.bat`
- Dashboard will open at: http://localhost:8501

### Option 3: Command Line
```bash
# Terminal 1 - Backend
.venv\Scripts\python.exe backend\app.py

# Terminal 2 - Dashboard (in another terminal)
.venv\Scripts\python.exe -m streamlit run frontend\dashboard.py
```

## 📊 Accessing the Dashboard:

Once both servers are running:
1. **Backend API**: http://localhost:8000/docs (for API testing)
2. **Main Dashboard**: http://localhost:8501
3. **Analytics Page**: http://localhost:8501/analytics (Advanced analytics & charts)

## 🔧 Troubleshooting:

### Problem: "Port already in use"
**Solution**: Close any existing Python/Streamlit processes:
```bash
taskkill /F /IM python.exe
# Then restart the system
```

### Problem: "Module not found"
**Solution**: Reinstall dependencies:
```bash
.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.venv\Scripts\python.exe -m pip install -r frontend\requirements.txt
```

### Problem: Dashboard not loading
**Solution**: Make sure backend is running FIRST, then start frontend

## 📂 Important Files:
- `backend/app.py` - FastAPI backend server
- `frontend/dashboard.py` - Main Streamlit dashboard
- `frontend/pages/analytics.py` - Advanced analytics page
- `more-advance-prediction.py` - ML prediction model (✅ FIXED)

## 🎯 Features:
- ✅ Real-time crop price predictions
- ✅ Interactive charts and visualizations
- ✅ Weather API integration
- ✅ Advanced analytics dashboard
- ✅ Multi-crop support with regional data

## 📞 Need Help?
Check the logs in the terminal windows for any error messages.

---
**Status**: ✅ All issues resolved - System ready to run!
