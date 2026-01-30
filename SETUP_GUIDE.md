# 🌾 KRISHI DRISHTI 2.0 - Complete Setup Guide (Hinglish)

## 📋 Project Structure Samjhiye

```
KRISHI-DRISTI-2.0/
├── backend/              ← REST API (FastAPI)
│   ├── app.py           ← Server start hoti hai yaha se
│   ├── api/routes.py    ← API endpoints (predict, crops, etc.)
│   └── services/        ← Business logic
│
├── frontend/            ← Dashboard (Streamlit)
│   └── dashboard.py     ← User interface
│
├── more-advance-prediction.py  ← Original ML logic
├── all_crop_data.csv           ← Historical data
└── *.joblib files              ← Trained ML models
```

---

## 🚀 Quick Start (3 Steps Mein)

### **Step 1: Dependencies Install Karein**

```powershell
# Backend dependencies
cd backend
pip install -r requirements.txt

# Frontend dependencies  
cd ../frontend
pip install -r requirements.txt

# Go back to root
cd ..
```

---

### **Step 2: Backend Start Karein**

**Terminal 1 mein:**
```powershell
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

✅ **Output dikhega:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

🌐 **Browser mein test karein:**
- API Docs: http://localhost:8000/docs
- Main API: http://localhost:8000/api/v1

---

### **Step 3: Frontend Dashboard Start Karein**

**Terminal 2 mein (naya terminal kholen):**
```powershell
cd frontend
streamlit run dashboard.py
```

✅ **Output dikhega:**
```
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

📊 **Browser automatically khul jayega ya manually open karein:**
http://localhost:8501

---

## 🎯 Kaise Use Karein?

### **Method 1: Streamlit Dashboard (Recommended)**

1. Browser mein `http://localhost:8501` kholen
2. Sidebar se crop aur state select karein
3. Date aur demand enter karein
4. "🔮 Predict Price" button pe click karein
5. Result dikhe ga with beautiful graphs!

### **Method 2: API Documentation (Developer View)**

1. `http://localhost:8000/docs` kholen
2. Interactive API testing kar sakte ho
3. Try out different endpoints

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/crops` | GET | Sabhi crops ki list |
| `/api/v1/crops/{crop}/states` | GET | Crop ke liye states |
| `/api/v1/predict` | POST | Price prediction |
| `/api/v1/weather` | POST | Weather data fetch |

---

## 🔧 Troubleshooting

### **Problem 1: Port already in use**

**Backend ke liye:**
```powershell
# Different port use karein
uvicorn app:app --port 8001
```

**Frontend ke liye:**
```powershell
# Different port use karein
streamlit run dashboard.py --server.port 8502
```

---

### **Problem 2: Module not found**

```powershell
# Phir se install karein
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

---

### **Problem 3: API connection failed**

✅ Check karein:
1. Backend chal raha hai? (Terminal 1 check karein)
2. Port 8000 correct hai?
3. `http://localhost:8000/` browser mein test karein

---

## 🌟 Features

✨ **Real-time Weather Integration** - OpenWeatherMap API  
✨ **8 Major Crops** - Wheat, Paddy, Cotton, etc.  
✨ **7 States Coverage** - Punjab, UP, Maharashtra, etc.  
✨ **ML-Powered** - RandomForest algorithm  
✨ **Beautiful Dashboard** - Streamlit with Plotly charts  
✨ **REST API** - FastAPI for integration  

---

## 📞 Ports Summary

| Service | Port | URL |
|---------|------|-----|
| Backend API | 8000 | http://localhost:8000 |
| API Docs | 8000 | http://localhost:8000/docs |
| Frontend Dashboard | 8501 | http://localhost:8501 |

---

## 🎓 Architecture Flow

```
User Browser (Port 8501)
    ↓
Streamlit Dashboard (frontend/dashboard.py)
    ↓ HTTP Request
FastAPI Backend (backend/app.py - Port 8000)
    ↓
ML Service (services/prediction_service.py)
    ↓ Loads
Trained Models (*.joblib files)
    ↓ Predicts
Price Result → Back to User
```

---

## 💡 Pro Tips

1. **Always start Backend first**, then Frontend
2. **Keep both terminals running** during use
3. Use **Ctrl+C** to stop servers
4. Check **logs** in terminal for debugging
5. API docs at `/docs` for testing endpoints

---

**Happy Farming! 🌾 Jai Jawan Jai Kisan! 🚜**
