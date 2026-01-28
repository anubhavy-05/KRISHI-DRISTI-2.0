# 🚀 Quick Start Guide - Ek Minute Mein!

## ✅ Super Easy Method (RECOMMENDED):

### **Option 1: Double Click RUN.bat**
1. File Explorer mein jaao
2. `RUN.bat` file pe **double click** karo
3. 2 windows khulenge automatically
4. Browser automatically khul jayega: http://localhost:8501

---

## 🔧 Manual Method (Agar RUN.bat nahi chala):

### **Terminal 1 - Backend:**
```powershell
cd "C:\Users\ay840\OneDrive\Desktop\APROJECT\krishidrshti\KRISHI-DRISTI-2.0"
python backend\app.py
```

### **Terminal 2 - Frontend:**
```powershell
cd "C:\Users\ay840\OneDrive\Desktop\APROJECT\krishidrshti\KRISHI-DRISTI-2.0"
python -m streamlit run frontend\dashboard.py
```

---

## ⚠️ Common Issues & Solutions:

### Problem: "Path not found"
**Solution:** Check your current folder. You should be in:
```
C:\Users\ay840\OneDrive\Desktop\APROJECT\krishidrshti\KRISHI-DRISTI-2.0
```
NOT in nested `KRISHI-DRISTI-2.0\KRISHI-DRISTI-2.0`

### Problem: "streamlit command not found"  
**Solution:** Use `python -m streamlit` instead of just `streamlit`

### Problem: "Module not found"
**Solution:** 
```powershell
cd backend
pip install -r requirements.txt

cd ..\frontend
pip install -r requirements.txt
```

---

## 🌐 URLs (After Starting):

- **Dashboard:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs
- **API Base:** http://localhost:8000

---

## 🎯 Testing Steps:

1. Open: http://localhost:8501
2. Select: **Wheat** → **Punjab** → **Today's Date**
3. Set Demand: **650**
4. Click: **"🔮 Predict Price"**
5. See magic! ✨

---

## 💡 Pro Tip:

**Path confusion ho raha hai?**

Simple command:
```powershell
cd C:\Users\ay840\OneDrive\Desktop\APROJECT\krishidrshti\KRISHI-DRISTI-2.0
```

Copy-paste this EXACT path!

---

## 🛑 Stop Servers:

Press **Ctrl + C** in both terminal windows

---

**Agar phir bhi problem ho, toh `RUN.bat` pe right-click → "Run as Administrator"**
