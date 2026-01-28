# 🌾 Krishi Drishti 2.0 - Web Dashboard + REST API

**AI-Powered Crop Price Prediction System with Real-time Weather Integration**

---

## 🚀 **Naye Features (Major Project Upgrade)**

### ✨ **Web Dashboard + REST API Implementation**

- ✅ **FastAPI Backend** - Production-ready REST API
- ✅ **Streamlit Dashboard** - Interactive web interface with real-time predictions
- ✅ **Real-time Weather Integration** - OpenWeatherMap API se live data
- ✅ **Historical Analytics** - 60-day price trends with interactive graphs
- ✅ **Multiple Endpoints** - `/predict`, `/weather`, `/crops`, `/history`
- ✅ **Auto-documentation** - Swagger UI (FastAPI docs)
- ✅ **CORS Enabled** - Frontend-backend communication
- ✅ **Responsive Design** - Mobile-friendly dashboard

---

## 📁 **Project Structure**

```
KRISHI-DRISTI-2.0/
│
├── backend/                          # FastAPI REST API
│   ├── api/
│   │   └── routes.py                # API endpoints
│   ├── services/
│   │   ├── prediction_service.py    # ML prediction logic
│   │   └── weather_service.py       # Weather API integration
│   ├── app.py                       # Main FastAPI app
│   └── requirements.txt             # Backend dependencies
│
├── frontend/                        # Streamlit Dashboard
│   ├── dashboard.py                 # Main dashboard app
│   └── requirements.txt             # Frontend dependencies
│
├── more-advance-prediction.py       # Original CLI script
├── all_crop_data.csv               # Training data
├── *.joblib                        # Trained ML models
├── .env.example                    # Environment variables template
└── README_WEB.md                   # This file
```

---

## 🛠️ **Installation & Setup (Step-by-Step)**

### **Step 1: Python Environment Setup**

```powershell
# Check Python version (3.8+ required)
python --version

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

### **Step 2: Install Backend Dependencies**

```powershell
# Navigate to backend folder
cd backend

# Install requirements
pip install -r requirements.txt

# Go back to main folder
cd ..
```

### **Step 3: Install Frontend Dependencies**

```powershell
# Navigate to frontend folder
cd frontend

# Install requirements
pip install -r requirements.txt

# Go back to main folder
cd ..
```

### **Step 4: Train Models (First Time Only)**

```powershell
# Run original script to generate models and data
python more-advance-prediction.py
# Press Ctrl+C after models are trained (don't wait for interactive loop)
```

---

## 🚀 **How to Run**

### **Method 1: Run Both Servers Separately (Recommended)**

#### **Terminal 1 - Start Backend API**

```powershell
# Navigate to backend folder
cd backend

# Start FastAPI server
python app.py
```

✅ Backend will run on: **http://localhost:8000**  
📖 API Documentation: **http://localhost:8000/docs**

#### **Terminal 2 - Start Frontend Dashboard**

```powershell
# Open new terminal
# Navigate to frontend folder
cd frontend

# Start Streamlit dashboard
streamlit run dashboard.py
```

✅ Dashboard will run on: **http://localhost:8501**

---

### **Method 2: Quick Start Script (Optional)**

Create a file `start.bat` in main folder:

```batch
@echo off
echo Starting Krishi Drishti 2.0...
start cmd /k "cd backend && python app.py"
timeout /t 3
start cmd /k "cd frontend && streamlit run dashboard.py"
echo Both servers started!
```

Run: `start.bat`

---

## 📡 **API Endpoints**

### **Base URL:** `http://localhost:8000/api/v1`

### **1. Get All Crops**
```http
GET /crops
```
**Response:**
```json
{
  "success": true,
  "crops": ["Arhar", "Cotton", "Maize", "Moong", "Mustard", "Paddy", "Sugarcane", "Wheat"],
  "total": 8
}
```

### **2. Get States for Crop**
```http
GET /crops/{crop_name}/states
```
**Example:** `GET /crops/Wheat/states`

**Response:**
```json
{
  "success": true,
  "crop": "Wheat",
  "states": ["Uttar Pradesh", "Punjab", "Madhya Pradesh"],
  "total": 3
}
```

### **3. Predict Crop Price** ⭐
```http
POST /predict
```
**Request Body:**
```json
{
  "crop": "Wheat",
  "state": "Punjab",
  "date": "2026-01-30",
  "demand": 650.0,
  "rainfall": 25.0  // Optional - auto-fetched if not provided
}
```

**Response:**
```json
{
  "success": true,
  "predicted_price": 2234.56,
  "crop": "Wheat",
  "state": "Punjab",
  "date": "2026-01-30",
  "rainfall": 12.5,
  "demand": 650.0,
  "statistics": {
    "historical_average": 2180.45,
    "historical_min": 1950.00,
    "historical_max": 2500.00,
    "vs_average_percent": 2.48
  },
  "weather_data": {
    "success": true,
    "rainfall": 12.5,
    "temperature": 18.2,
    "description": "light rain"
  }
}
```

### **4. Get Weather Data**
```http
POST /weather
```
**Request Body:**
```json
{
  "state": "Punjab",
  "date": "2026-01-30"
}
```

### **5. Get Historical Prices**
```http
GET /history/{crop}/{state}?days=30
```
**Example:** `GET /history/Wheat/Punjab?days=60`

---

## 🎨 **Dashboard Features**

### **1. Interactive Prediction Form**
- Dropdown selection for crops and states
- Date picker with validation
- Market demand slider
- Optional custom rainfall input

### **2. Real-time Weather Integration**
- Auto-fetches weather data from OpenWeatherMap
- Shows temperature, rainfall, and conditions
- Fallback values if API fails

### **3. Historical Price Trends**
- 60-day price trend chart (interactive)
- Rainfall pattern visualization
- Price statistics (min, max, average, volatility)

### **4. Smart Recommendations**
- Market alerts for high/low prices
- Comparison with historical averages
- Visual indicators for price movements

### **5. Responsive Design**
- Clean, modern UI with gradient cards
- Mobile-friendly layout
- Real-time updates

---

## 🔧 **Configuration**

### **Environment Variables (Optional)**

Create `.env` file from `.env.example`:

```bash
# OpenWeatherMap API
OPENWEATHER_API_KEY=your_api_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend Configuration
FRONTEND_PORT=8501
```

---

## 🧪 **Testing the API**

### **Method 1: Using FastAPI Docs (Easiest)**

1. Start backend: `python backend/app.py`
2. Open browser: **http://localhost:8000/docs**
3. Click on any endpoint → "Try it out" → Execute

### **Method 2: Using PowerShell**

```powershell
# Test GET request
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/crops" -Method GET

# Test POST request (price prediction)
$body = @{
    crop = "Wheat"
    state = "Punjab"
    date = "2026-01-30"
    demand = 650.0
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/predict" -Method POST -Body $body -ContentType "application/json"
```

### **Method 3: Using Python**

```python
import requests

# Predict price
response = requests.post(
    "http://localhost:8000/api/v1/predict",
    json={
        "crop": "Wheat",
        "state": "Punjab",
        "date": "2026-01-30",
        "demand": 650.0
    }
)

print(response.json())
```

---

## 📊 **Dashboard Screenshots Guide**

### **What to Show in Your Presentation:**

1. **Main Dashboard** - Full view with sidebar and charts
2. **Prediction Result** - Purple gradient card with predicted price
3. **Historical Trends** - Interactive line chart showing 60-day trends
4. **API Documentation** - Swagger UI at `/docs`
5. **Mobile View** - Responsive design demo

---

## 🎓 **For Your Major Project Report**

### **Technical Stack:**

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend Framework | FastAPI | REST API server |
| Frontend Framework | Streamlit | Interactive dashboard |
| ML Model | RandomForestRegressor | Price prediction |
| Data Processing | Pandas, NumPy | Feature engineering |
| Visualization | Plotly | Interactive charts |
| Weather API | OpenWeatherMap | Real-time weather data |
| Model Persistence | Joblib | Save/load trained models |

### **Key Improvements from Minor Project:**

✅ **Scalability** - REST API can serve multiple clients  
✅ **User Experience** - Web interface vs CLI  
✅ **Real-time Data** - Live weather integration  
✅ **Analytics** - Historical trends and statistics  
✅ **Documentation** - Auto-generated API docs  
✅ **Deployment Ready** - Can be hosted on cloud  

---

## 🚀 **Next Steps (Optional Enhancements)**

### **For Extra Marks:**

1. **Database Integration**
   ```powershell
   pip install sqlalchemy databases
   # Store predictions in SQLite/PostgreSQL
   ```

2. **User Authentication**
   ```powershell
   pip install python-jose passlib
   # Add JWT-based auth
   ```

3. **Deployment**
   - Deploy backend on **Railway.app** (free)
   - Deploy frontend on **Streamlit Cloud** (free)

4. **Mobile App**
   - Convert Streamlit to **Flutter/React Native**
   - Or create **Android APK** using Kivy

---

## 🐛 **Troubleshooting**

### **Problem: "Cannot connect to API"**
✅ **Solution:** Make sure backend is running on port 8000
```powershell
cd backend
python app.py
```

### **Problem: "Model file not found"**
✅ **Solution:** Train models first
```powershell
python more-advance-prediction.py
# Wait for "SETUP COMPLETE" message, then Ctrl+C
```

### **Problem: "Module not found"**
✅ **Solution:** Install requirements
```powershell
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### **Problem: "Port already in use"**
✅ **Solution:** Kill existing process or change port
```powershell
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

---

## 📞 **Support**

- 📖 **API Docs**: http://localhost:8000/docs
- 🌐 **Dashboard**: http://localhost:8501
- 📧 **OpenWeatherMap Support**: https://openweathermap.org/api

---

## 📝 **License**

MIT License - Free for educational and commercial use

---

## 🎯 **Summary**

Aapne successfully implement kar liya:
- ✅ FastAPI REST API with 5+ endpoints
- ✅ Interactive Streamlit dashboard
- ✅ Real-time weather integration
- ✅ Historical price analytics
- ✅ Auto-documentation with Swagger UI
- ✅ Production-ready architecture

**Total time to setup:** ~10 minutes  
**Lines of code added:** ~1000+  
**New features:** 8+ major features

---

**🌾 Krishi Drishti 2.0 - Empowering Farmers with AI**

*Made with ❤️ for Major Project*
