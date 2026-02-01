# 🌾 KRISHI DRISHTI 2.0 - Complete Setup Guide (Hinglish)

## ✅ Setup Complete! Sab Kuch Ready Hai

### 🎉 **Congratulations!**
Aapka project successfully setup ho gaya hai aur servers chal rahi hain!

---

## 🌐 **Kaha Jaana Hai? (URLs)**

### **1. Frontend Dashboard (User Interface)**
```
http://localhost:8501
```
**Ye hai main interface** jaha aap:
- Crop select karoge
- State select karoge  
- Date aur demand enter karoge
- **Price prediction** dekhoge

**Ye automatically browser mein khul gaya hoga!** 🚀

---

### **2. Backend API (Developer View)**
```
http://localhost:8000
```
**Ye API server hai** jo background mein kaam karta hai

---

### **3. API Documentation (Interactive)**
```
http://localhost:8000/docs
```
**Ye FastAPI ka automatic documentation hai** - Yaha aap:
- Saare API endpoints dekh sakte ho
- Directly browser se test kar sakte ho
- Request/Response format samajh sakte ho

**Try karna chahiye!** Bahut useful hai! 📖

---

## 🖥️ **Kya Chal Raha Hai?**

### **Terminal Windows:**
Aapko **2 alag terminal windows** dikhengi:

#### **Window 1: BACKEND - Port 8000**
```
[BACKEND] Starting FastAPI...
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete
```

#### **Window 2: FRONTEND - Port 8501**
```
[FRONTEND] Starting Streamlit Dashboard...

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**Dono windows ko chalti rehne do!** ❌ Band mat karo!

---

## 📊 **Project Architecture (Simple Explanation)**

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR BROWSER                             │
│                   (Jo aap dekhte ho)                        │
│                                                             │
│  ┌────────────────────────────────────────────────┐        │
│  │  DASHBOARD (Streamlit)                         │        │
│  │  http://localhost:8501                         │        │
│  │                                                 │        │
│  │  📋 Form: Crop, State, Date, Demand           │        │
│  │  💰 Result: Predicted Price                    │        │
│  └──────────────┬─────────────────────────────────┘        │
│                 │                                           │
│                 │ HTTP Request                              │
│                 ▼                                           │
└─────────────────────────────────────────────────────────────┘
                  │
                  │
┌─────────────────▼─────────────────────────────────────────┐
│            BACKEND API (FastAPI)                          │
│            http://localhost:8000                          │
│                                                           │
│  ┌─────────────┐      ┌──────────────┐                  │
│  │   Routes    │──────│   Services    │                  │
│  │  (API       │      │  (Business    │                  │
│  │  Endpoints) │      │   Logic)      │                  │
│  └─────────────┘      └───────┬───────┘                  │
│                               │                           │
│                               ▼                           │
│                    ┌──────────────────┐                   │
│                    │ Prediction       │                   │
│                    │ Service          │                   │
│                    └────────┬─────────┘                   │
│                             │                             │
│                             ▼                             │
└─────────────────────────────────────────────────────────┘
                              │
                              │
┌─────────────────────────────▼─────────────────────────────┐
│              FILE SYSTEM (Your Computer)                  │
│                                                           │
│  📁 KRISHI-DRISTI-2.0/                                   │
│     ├── 📊 all_crop_data.csv (Historical Data)          │
│     ├── 🤖 wheat_punjab_price_model.joblib (ML Model)   │
│     ├── 🤖 paddy_uttar_pradesh_price_model.joblib       │
│     └── ... (More models for different crops)           │
└───────────────────────────────────────────────────────────┘
```

---

## 🔄 **Complete Flow (Request to Response)**

### **User ki taraf se:**
1. Browser mein `localhost:8501` kholo
2. Form fill karo:
   - Crop: **Wheat**
   - State: **Punjab**
   - Date: **2026-01-30**
   - Demand: **500**
3. "Predict Price" button click karo

### **System ki taraf se:**

```
Step 1: Frontend (Streamlit Dashboard)
│
├─► Form data collect karo
│   {crop: "Wheat", state: "Punjab", date: "2026-01-30", demand: 500}
│
Step 2: HTTP Request bhejo Backend ko
│
├─► POST http://localhost:8000/api/v1/predict
│   Body: {crop, state, date, demand}
│
Step 3: Backend (FastAPI) receives request
│
├─► Route handler process karta hai
│   └─► Prediction Service call karta hai
│
Step 4: Prediction Service
│
├─► 1. Weather Service se rainfall data fetch karo
│   └─► OpenWeatherMap API call
│       └─► Returns: rainfall = 15mm
│
├─► 2. Model file load karo
│   └─► wheat_punjab_price_model.joblib
│
├─► 3. Historical data padhna
│   └─► all_crop_data.csv se last 7 days ka data
│       └─► Moving average calculate karo
│
├─► 4. Features prepare karo
│   └─► [rainfall=15, demand=500, month=1, day=3, moving_avg=2200]
│
├─► 5. ML Model run karo
│   └─► model.predict(features)
│       └─► Returns: ₹2,315.75
│
Step 5: Response bhejo Frontend ko
│
├─► JSON: {success: true, predicted_price: 2315.75}
│
Step 6: Dashboard update ho jata hai
│
└─► Screen pe dikhta hai: "₹2,315.75 per quintal"
```

**Total time: ~2-3 seconds** ⚡

---

## 📁 **File Structure (Kaha Kya Hai?)**

```
KRISHI-DRISTI-2.0/
│
├── 📂 backend/                    (API Server - Port 8000)
│   ├── app.py                     ← Main FastAPI application
│   ├── requirements.txt           ← Backend dependencies
│   │
│   ├── 📂 api/
│   │   └── routes.py             ← API endpoints (/predict, /crops, etc.)
│   │
│   └── 📂 services/
│       ├── prediction_service.py  ← ML prediction logic
│       └── weather_service.py     ← Weather API integration
│
├── 📂 frontend/                   (Dashboard - Port 8501)
│   ├── dashboard.py              ← Streamlit UI
│   └── requirements.txt          ← Frontend dependencies
│
├── 📊 all_crop_data.csv          ← Historical crop price data (1000 days)
│
├── 🤖 *.joblib files             ← Trained ML models (one per crop-state combo)
│   ├── wheat_punjab_price_model.joblib
│   ├── wheat_uttar_pradesh_price_model.joblib
│   ├── paddy_punjab_price_model.joblib
│   └── ... (22 models total)
│
├── 🔧 more-advance-prediction.py ← Original ML training script
│
├── ⚙️ setup.bat                  ← One-time setup (dependencies install)
├── ▶️ start_servers.bat          ← Start both servers
└── 📖 README.md                  ← Documentation
```

---

## 🎮 **How to Use (Step-by-Step)**

### **First Time Setup:**
```bash
1. Double-click: setup.bat
   └─► Installs all dependencies
   └─► Takes ~2-3 minutes

2. Double-click: start_servers.bat
   └─► Starts backend (Port 8000)
   └─► Starts frontend (Port 8501)
   └─► Opens browser automatically
```

### **Daily Use:**
```bash
1. Double-click: start_servers.bat
   
2. Browser automatically khulega: http://localhost:8501

3. Dashboard use karo:
   - Crop select karo
   - State select karo
   - Date pick karo
   - Demand enter karo
   - Click "Predict Price"
   
4. Result dekho! ₹2,315.75 per quintal
```

### **Stop Servers:**
```
Dono terminal windows mein: Ctrl+C
Ya windows band kar do
```

---

## ❓ **Common Questions & Answers**

### **Q1: localhost:8501 kyu nahi khul raha?**
**A:** 
- Check karo ki `start_servers.bat` properly run hua
- Frontend window mein error hai kya?
- Browser manually open karo: `http://localhost:8501`

---

### **Q2: "Connection refused" error aa raha hai**
**A:**
- Backend server chal rahi hai kya? Check karo terminal
- Port 8000 kisi aur app ne use kar rakha hai kya?
- `setup.bat` dobara run karo

---

### **Q3: Prediction galat aa rahi hai**
**A:**
- Models trained hain kya? Check karo `.joblib` files exist karti hain
- `all_crop_data.csv` file hai kya?
- Agar nahi hai toh `more-advance-prediction.py` run karo

---

### **Q4: Weather data fetch nahi ho raha**
**A:**
- Internet connection check karo
- API key valid hai kya? (already valid hai aapki)
- Manual rainfall enter kar sakte ho as fallback

---

### **Q5: Dono servers ek saath start nahi ho rahi**
**A:**
```bash
Manual start karo:

Terminal 1:
cd backend
python -m uvicorn app:app --reload --port 8000

Terminal 2:
cd frontend
streamlit run dashboard.py
```

---

## 🔧 **Advanced Tips**

### **1. API Directly Test Karna:**
```bash
# PowerShell mein:
Invoke-RestMethod -Method POST -Uri "http://localhost:8000/api/v1/predict" -ContentType "application/json" -Body '{"crop":"Wheat","state":"Punjab","date":"2026-01-30","demand":500}'
```

### **2. New Model Train Karna:**
```bash
python more-advance-prediction.py
```

### **3. Production Deployment:**
```bash
# Backend:
gunicorn -k uvicorn.workers.UvicornWorker backend.app:app

# Frontend:
streamlit run frontend/dashboard.py --server.port 80
```

---

## 📞 **Troubleshooting Commands**

### Check Python version:
```bash
python --version
# Expected: Python 3.10.x or higher
```

### Check if ports are free:
```bash
netstat -ano | findstr :8000
netstat -ano | findstr :8501
```

### Reinstall dependencies:
```bash
pip install -r backend/requirements.txt --force-reinstall
pip install -r frontend/requirements.txt --force-reinstall
```

---

## 🎯 **Summary (Ek Line Mein)**

1. **Setup:** `setup.bat` (one time)
2. **Start:** `start_servers.bat` (har baar)
3. **Use:** Browser → `localhost:8501` → Form fill → Predict
4. **Stop:** Ctrl+C in both windows

---

## ✅ **Final Checklist**

- [x] Python installed (3.10.11) ✅
- [x] Dependencies installed ✅
- [x] Backend running (Port 8000) ✅
- [x] Frontend running (Port 8501) ✅
- [x] API key configured ✅
- [x] Models trained ✅
- [x] Data file exists ✅

---

## 🎊 **Congratulations!**

**Aapka KRISHI DRISHTI 2.0 fully functional hai!** 

Farmers ab apni crops ki predicted prices dekh sakte hain aur better decisions le sakte hain! 🌾💰

**Happy Farming! 🚜**
