# 🌾 KRISHI-DRISTI 2.0 - Crop Price Prediction System

A smart web-based application for predicting crop prices and exploring market analytics based on various agricultural and market factors.

[![Live Preview](https://img.shields.io/badge/Live%20Preview-Click%20Here-brightgreen?style=for-the-badge&logo=github)](https://anubhavy-05.github.io/KRISHI-DRISTI-2.0/)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/anubhavy-05/KRISHI-DRISTI-2.0)

## 🚀 Features

- **8 Major Crops Supported**: Wheat, Paddy (Rice), Cotton, Maize, Arhar, Moong, Mustard, and Sugarcane
- **Multi-State Coverage**: Predictions for major agricultural states in India
- **Smart Price Prediction**: ML-based algorithm considering multiple factors:
  - Rainfall patterns
  - Market demand
  - Seasonal variations
  - State-specific factors
  - Year-based trends
- **Interactive UI**: Beautiful, responsive design that works on all devices
- **Real-time Insights**: Get market insights and confidence scores with predictions
- **Static Analytics Dashboard**: Vercel-ready advanced analytics page with volatility, seasonal, trend, and sentiment views
- **Browser-Based Market Analysis**: Dashboard reads directly from `all_crop_data.csv` and works without Streamlit on Vercel
- **Direct Navigation**: Homepage buttons jump to prediction and analytics pages

## 📊 How It Works

1. Select your crop
2. Choose the state
3. Enter rainfall data (in mm)
4. Input market demand (in quintals)
5. Select year and month
6. Get instant price prediction with confidence score and market insights

## 🛠️ Technologies Used

- **HTML5** - Structure
- **CSS3** - Styling with modern gradients and animations
- **JavaScript** - Price prediction algorithm and interactivity

## 📁 Project Structure

```
NEW-KRISHI/
│
├── index.html          # Main HTML file
├── analytics.html      # Static advanced analytics dashboard
├── analytics-static.js  # Analytics dashboard logic
├── styles.css          # CSS styling
├── script.js           # JavaScript logic
├── all_crop_data.csv   # Source data for analytics charts
└── README.md           # Documentation
```

## 🌐 Live Demo

**🔗 [View Live Website](https://anubhavy-05.github.io/KRISHI-DRISTI-2.0/)**

**📊 [Open Analytics Dashboard](analytics.html)**

Click the button above or visit: `https://anubhavy-05.github.io/KRISHI-DRISTI-2.0/`

### 📸 Website Preview
The website is live and fully functional! Visit the link above to:
- ✅ Predict crop prices for 8 different crops
- ✅ Get market insights based on rainfall and demand
- ✅ View interactive price prediction charts
- ✅ Open a Vercel-friendly advanced analytics dashboard
- ✅ View price volatility, seasonal patterns, year-over-year trends, and market sentiment
- ✅ Access from any device (mobile, tablet, desktop)

> **Note**: Upload a screenshot as `screenshot.png` in the repository root to display it here.

## 💻 Local Development

Simply open `index.html` in any modern web browser. No build process or dependencies required!

For the analytics page, open `analytics.html` in the browser after serving the folder locally.

Or use a local server:

```bash
# Python
python -m http.server 8000

# Node.js
npx http-server -p 8000
```

Then visit: `http://localhost:8000`

To open the analytics dashboard locally, visit: `http://localhost:8000/analytics.html`

If you are running the Streamlit version locally, the advanced dashboard is available at `http://localhost:8501/analytics`.

## 📱 Screenshots

![alt text](Screenshot.png)

## 🎯 Price Prediction Algorithm

The system uses a sophisticated algorithm that considers:

- **Base Prices**: Historical average prices for each crop
- **Demand Factor**: Market demand in quintals (0-1M range)
- **Rainfall Impact**: Optimal rainfall ranges for each crop
- **State Variations**: Regional price differences
- **Seasonal Effects**: Harvest vs off-season pricing
- **Inflation Adjustment**: Year-over-year price changes

## 📊 Analytics Dashboard

The static analytics dashboard includes:

- **Volatility Analysis** with meaning-based risk colors
- **Seasonal Patterns** showing best and worst months to sell
- **Year-over-Year Trends** with yearly comparison charts
- **Market Sentiment** based on volatility, momentum, and confidence
- **Predictive Inputs** for date, demand, and rainfall

Open it from the homepage using the **Analytics Dashboard** button or directly at `analytics.html`.

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Copyright (c) 2025 anubhavy-05. All Rights Reserved.

This project is proprietary software. No copying, distribution, or modification is permitted without explicit permission from the author. See the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**@anubhavy-05**
- GitHub: [@anubhavy-05](https://github.com/anubhavy-05)
- Repository: [KRISHI-DRISTI-2.0](https://github.com/anubhavy-05/KRISHI-DRISTI-2.0)

## 🙏 Acknowledgments

- Agricultural data patterns based on Indian market research
- UI/UX inspired by modern web design principles
- Built for farmers and agricultural stakeholders

---

**Note**: This is a prediction tool based on statistical models. Actual market prices may vary due to numerous real-time factors.
