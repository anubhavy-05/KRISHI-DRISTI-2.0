# Quick Setup Guide - Hinglish
# Krishi Drishti 2.0 Web Dashboard

## 🚀 5-Minute Setup (Ekdum Easy!)

### Step 1️⃣: Install Backend
```powershell
cd backend
pip install -r requirements.txt
```

### Step 2️⃣: Install Frontend
```powershell
cd ../frontend
pip install -r requirements.txt
```

### Step 3️⃣: Train Models (Agar pehli baar run kar rahe ho)
```powershell
cd ..
python more-advance-prediction.py
# Jab "SETUP COMPLETE" dikhe, Ctrl+C press karo
```

### Step 4️⃣: Start Everything
```powershell
start.bat
# Ya manually:
# Terminal 1: cd backend && python app.py
# Terminal 2: cd frontend && streamlit run dashboard.py
```

### Step 5️⃣: Open Dashboard
Browser mein jaao: **http://localhost:8501**

---

## 📱 What You'll See:

1. **Left Sidebar** - Crop, State, Date select karo
2. **Main Area** - Historical price graphs dikhengi
3. **Predict Button** - Click karke price prediction dekho
4. **Purple Card** - Predicted price with recommendations

---

## 🎯 Testing Checklist:

- [ ] Backend running on port 8000 ✅
- [ ] Frontend running on port 8501 ✅
- [ ] Can select crops and states ✅
- [ ] Weather data auto-fetch ho raha hai ✅
- [ ] Historical graphs dikh rahe hain ✅
- [ ] Prediction working perfectly ✅

---

## 🐛 Common Issues:

**"Module not found"**
```powershell
pip install fastapi uvicorn streamlit plotly
```

**"Port already in use"**
```powershell
# Kill existing process
netstat -ano | findstr :8000
taskkill /PID <number> /F
```

**"Cannot connect to API"**
- Backend chal raha hai? Check terminal 1
- URL sahi hai? `http://localhost:8000`

---

## 🎓 For Presentation:

### Screenshots lena:
1. Dashboard homepage with graphs
2. Prediction result (purple card)
3. API documentation (http://localhost:8000/docs)
4. Historical trends chart

### Demo flow:
1. Select "Wheat" + "Punjab"
2. Choose today's date
3. Click "Predict Price"
4. Show predicted price with weather data
5. Explain the recommendation
6. Open API docs to show endpoints

---

## 📊 Key Features to Highlight:

✨ **Real-time Weather Integration** - Live API se data
✨ **Interactive Dashboard** - Graphs, filters, responsive
✨ **REST API** - Multiple endpoints for scalability
✨ **Historical Analytics** - 60-day price trends
✨ **Smart Recommendations** - Buy/sell alerts
✨ **Auto Documentation** - Swagger UI built-in

---

## 🚀 Next Level (Optional):

### Add Database:
```powershell
pip install sqlalchemy
# Store predictions history
```

### Add Authentication:
```powershell
pip install python-jose
# JWT tokens for secure access
```

### Deploy Online:
- Backend → Railway.app (free)
- Frontend → Streamlit Cloud (free)

---

## 💡 Pro Tips:

1. **Live Demo** - Run locally during presentation
2. **API Testing** - Show Swagger UI at /docs
3. **Mobile Demo** - Open dashboard on phone (same WiFi)
4. **Code Walkthrough** - Explain architecture briefly

---

**Total Setup Time:** 5-10 minutes  
**Total Code:** 1000+ lines  
**Complexity Level:** Professional ⭐⭐⭐⭐⭐

**Shabash! Major project ready hai! 🎉**
