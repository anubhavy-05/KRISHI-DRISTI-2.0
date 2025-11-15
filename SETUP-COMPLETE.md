# 🌾 KRISHI-DRISTI 2.0 - Complete Setup Guide

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation Guide](#installation-guide)
- [Deployment Guide](#deployment-guide)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [Browser Support](#browser-support)

---

## 🎯 Project Overview

**KRISHI-DRISTI 2.0** is a smart web-based crop price prediction system that helps farmers and agricultural stakeholders make informed decisions about crop pricing based on multiple factors including rainfall, market demand, seasonal variations, and regional differences.

### Key Capabilities
- Predicts prices for 8 major crops across multiple Indian states
- Provides confidence scores and market insights
- Visualizes price trends with interactive charts
- Fully responsive design for all devices

---

## ✨ Features

### 1. **Multi-Crop Support**
   - Wheat
   - Paddy (Rice)
   - Cotton
   - Maize
   - Arhar (Tur Dal)
   - Moong (Green Gram)
   - Mustard
   - Sugarcane

### 2. **State-Specific Predictions**
   - Madhya Pradesh
   - Maharashtra
   - Punjab
   - Uttar Pradesh
   - West Bengal
   - Gujarat
   - Rajasthan

### 3. **Smart Prediction Algorithm**
   - Rainfall impact analysis
   - Market demand integration (in quintals)
   - Seasonal variation factors
   - State-specific price adjustments
   - Year-based inflation modeling
   - Confidence scoring (65-95%)

### 4. **Interactive Visualization**
   - Real-time price prediction chart
   - 1000-day historical data simulation
   - Actual vs Predicted price comparison
   - Seasonal pattern visualization

### 5. **Responsive Design**
   - Mobile-optimized (iPhone, Samsung, Oppo, iQOO, etc.)
   - Tablet-compatible (iPad, Galaxy Tab)
   - Desktop-friendly
   - Portrait and landscape support

---

## 🛠️ Technology Stack

### Frontend Technologies
- **HTML5** - Semantic markup and structure
- **CSS3** - Advanced styling with:
  - CSS Grid and Flexbox
  - CSS Variables
  - Animations and transitions
  - Responsive media queries
- **JavaScript (ES6+)** - Core functionality:
  - Price prediction algorithm
  - Form validation
  - Dynamic UI updates
  - Data visualization

### External Libraries
- **Chart.js** - Interactive price trend charts
- **Google Fonts** - Poppins font family

### Version Control
- **Git** - Source control
- **GitHub** - Repository hosting and collaboration
- **GitHub Pages** - Free web hosting

---

## 📥 Installation Guide

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Text editor (VS Code, Sublime Text, etc.) - for development only
- Git (for version control) - optional

### Option 1: Direct Download
1. Download the repository as ZIP
2. Extract to your desired location
3. Open `index.html` in any web browser

### Option 2: Clone Repository
```bash
# Clone the repository
git clone https://github.com/anubhavy-05/KRISHI-DRISTI-2.0.git

# Navigate to project directory
cd KRISHI-DRISTI-2.0

# Open in browser
# Simply double-click index.html or use a local server
```

### Option 3: Local Development Server

#### Using Python:
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

#### Using Node.js:
```bash
# Install http-server globally
npm install -g http-server

# Run server
http-server -p 8000
```

#### Using VS Code Live Server:
1. Install "Live Server" extension
2. Right-click on `index.html`
3. Select "Open with Live Server"

### Access the Application
- Local file: `file:///path/to/index.html`
- Local server: `http://localhost:8000`
- Live site: `https://anubhavy-05.github.io/KRISHI-DRISTI-2.0/`

---

## 🚀 Deployment Guide

### GitHub Pages Deployment

#### Step 1: Create GitHub Repository
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit"

# Add remote repository
git remote add origin https://github.com/anubhavy-05/KRISHI-DRISTI-2.0.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### Step 2: Enable GitHub Pages
1. Go to repository settings
2. Navigate to "Pages" section
3. Under "Source", select `main` branch
4. Click "Save"
5. Wait 1-2 minutes for deployment
6. Access at: `https://anubhavy-05.github.io/KRISHI-DRISTI-2.0/`

### Alternative Deployment Options

#### Netlify
1. Drag and drop project folder to [Netlify Drop](https://app.netlify.com/drop)
2. Automatic deployment and SSL
3. Custom domain support

#### Vercel
1. Import repository from GitHub
2. Automatic deployment on push
3. Preview deployments for PRs

#### Firebase Hosting
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase
firebase init hosting

# Deploy
firebase deploy
```

---

## 📁 File Structure

```
KRISHI-DRISTI-2.0/
│
├── index.html              # Main HTML file
│   ├── Header section
│   ├── Prediction form
│   ├── Results display
│   └── Chart visualization
│
├── styles.css              # Complete styling
│   ├── Global variables
│   ├── Component styles
│   ├── Animations
│   └── Responsive media queries
│
├── script.js               # JavaScript logic
│   ├── Crop-state mapping
│   ├── Price calculation algorithm
│   ├── Form handlers
│   ├── Result display
│   └── Chart generation
│
├── README.md               # Project documentation
├── SETUP-COMPLETE.md       # This file
├── TESTING_GUIDE.md        # Testing procedures
├── requirements.txt        # Dependencies list
└── .gitignore             # Git ignore rules
```

---

## ⚙️ Configuration

### Customizing Base Prices
Edit `script.js` to modify crop base prices:

```javascript
const basePrices = {
    wheat: 2000,      // ₹ per quintal
    paddy: 1950,
    cotton: 5800,
    maize: 1850,
    arhar: 6300,
    moong: 7200,
    mustard: 5400,
    sugarcane: 3100
};
```

### Adjusting Rainfall Parameters
Modify optimal rainfall ranges:

```javascript
const rainfallImpact = {
    wheat: { optimal: 600, min: 400, max: 1000 },
    paddy: { optimal: 1200, min: 1000, max: 2500 },
    // ... add more crops
};
```

### State Price Factors
Adjust regional price variations:

```javascript
const stateFactors = {
    'Madhya Pradesh': 0.98,
    'Maharashtra': 1.05,
    'Punjab': 1.08,
    // ... modify as needed
};
```

### Chart Customization
Modify chart appearance in `script.js`:

```javascript
// Chart colors
borderColor: 'rgb(52, 152, 219)',      // Actual price line
backgroundColor: 'rgba(52, 152, 219, 0.1)', // Fill color

// Chart dimensions
height: 400px  // In styles.css
```

### Color Scheme
Edit CSS variables in `styles.css`:

```css
:root {
    --primary-color: #2ecc71;
    --primary-dark: #27ae60;
    --secondary-color: #3498db;
    --accent-color: #f39c12;
    /* ... customize colors */
}
```

---

## 🌐 Browser Support

### Fully Supported
- ✅ Chrome 90+ (Desktop & Mobile)
- ✅ Firefox 88+ (Desktop & Mobile)
- ✅ Safari 14+ (Desktop & Mobile)
- ✅ Edge 90+
- ✅ Opera 76+
- ✅ Samsung Internet 14+

### Mobile Browser Testing
- ✅ iOS Safari (iPhone, iPad)
- ✅ Chrome Mobile (Android)
- ✅ Samsung Internet
- ✅ UC Browser
- ✅ Firefox Mobile

### Features Used
- CSS Grid & Flexbox
- CSS Variables
- ES6+ JavaScript
- Canvas API (for charts)
- LocalStorage (optional)

---

## 🔧 Troubleshooting

### Chart Not Displaying
- Ensure Chart.js CDN is loading
- Check browser console for errors
- Verify internet connection (for CDN)

### Form Not Submitting
- Check JavaScript console for errors
- Ensure all required fields are filled
- Verify form validation

### Mobile Display Issues
- Clear browser cache
- Test in different browsers
- Check viewport meta tag

### Price Predictions Seem Off
- Verify input values are realistic
- Check algorithm parameters
- Review state-crop combinations

---

## 📞 Support & Contact

- **Repository**: [GitHub](https://github.com/anubhavy-05/KRISHI-DRISTI-2.0)
- **Issues**: [Report Bug](https://github.com/anubhavy-05/KRISHI-DRISTI-2.0/issues)
- **Live Demo**: [View Site](https://anubhavy-05.github.io/KRISHI-DRISTI-2.0/)

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- Chart.js for visualization library
- Google Fonts for Poppins font
- GitHub Pages for free hosting
- Agricultural market data references

---

**Last Updated**: November 16, 2025  
**Version**: 2.0  
**Author**: @anubhavy-05
