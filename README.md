# 🌾 KRISHI - Crop Price Prediction System

A smart web-based application for predicting crop prices based on various agricultural and market factors.

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
├── styles.css          # CSS styling
├── script.js           # JavaScript logic
└── README.md           # Documentation
```

## 🌐 Live Demo

Visit: [Add your GitHub Pages URL here after deployment]

## 💻 Local Development

Simply open `index.html` in any modern web browser. No build process or dependencies required!

Or use a local server:

```bash
# Python
python -m http.server 8000

# Node.js
npx http-server -p 8000
```

Then visit: `http://localhost:8000`

## 📱 Screenshots

[Add screenshots here after deployment]

## 🎯 Price Prediction Algorithm

The system uses a sophisticated algorithm that considers:

- **Base Prices**: Historical average prices for each crop
- **Demand Factor**: Market demand in quintals (0-1M range)
- **Rainfall Impact**: Optimal rainfall ranges for each crop
- **State Variations**: Regional price differences
- **Seasonal Effects**: Harvest vs off-season pricing
- **Inflation Adjustment**: Year-over-year price changes

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- Agricultural data patterns based on Indian market research
- UI/UX inspired by modern web design principles
- Built for farmers and agricultural stakeholders

---

**Note**: This is a prediction tool based on statistical models. Actual market prices may vary due to numerous real-time factors.
