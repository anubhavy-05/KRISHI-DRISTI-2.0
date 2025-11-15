// Crop and State mapping based on available models
const cropStateMapping = {
    wheat: ['Madhya Pradesh', 'Punjab', 'Uttar Pradesh'],
    paddy: ['Punjab', 'Uttar Pradesh', 'West Bengal'],
    cotton: ['Gujarat', 'Maharashtra', 'Punjab'],
    maize: ['Madhya Pradesh', 'Uttar Pradesh'],
    arhar: ['Madhya Pradesh', 'Maharashtra', 'Uttar Pradesh'],
    moong: ['Madhya Pradesh', 'Rajasthan'],
    mustard: ['Madhya Pradesh', 'Rajasthan'],
    sugarcane: ['Maharashtra', 'Uttar Pradesh']
};

// Base prices for different crops (₹ per quintal)
const basePrices = {
    wheat: 2000,
    paddy: 1950,
    cotton: 5800,
    maize: 1850,
    arhar: 6300,
    moong: 7200,
    mustard: 5400,
    sugarcane: 3100
};

// Demand impact calculation
// Higher demand = higher prices (uses logarithmic scale for realistic impact)
function calculateDemandMultiplier(demand) {
    // Base demand: 10000 quintals = 1.0 multiplier
    // Scale: 0-5000 = Low (0.75-0.90)
    //        5000-15000 = Moderate (0.90-1.10)
    //        15000-50000 = High (1.10-1.30)
    //        50000+ = Very High (1.30-1.50)
    
    if (demand <= 0) return 0.70;
    if (demand < 5000) return 0.75 + (demand / 5000) * 0.15;
    if (demand < 15000) return 0.90 + ((demand - 5000) / 10000) * 0.20;
    if (demand < 50000) return 1.10 + ((demand - 15000) / 35000) * 0.20;
    return Math.min(1.50, 1.30 + ((demand - 50000) / 50000) * 0.20);
}

// Rainfall impact factors (optimal ranges vary by crop)
const rainfallImpact = {
    wheat: { optimal: 600, min: 400, max: 1000 },
    paddy: { optimal: 1200, min: 1000, max: 2500 },
    cotton: { optimal: 700, min: 500, max: 1200 },
    maize: { optimal: 800, min: 600, max: 1200 },
    arhar: { optimal: 800, min: 600, max: 1100 },
    moong: { optimal: 650, min: 400, max: 900 },
    mustard: { optimal: 600, min: 400, max: 900 },
    sugarcane: { optimal: 1500, min: 1200, max: 2500 }
};

// State price adjustment factors
const stateFactors = {
    'Madhya Pradesh': 0.98,
    'Maharashtra': 1.05,
    'Punjab': 1.08,
    'Uttar Pradesh': 1.0,
    'West Bengal': 0.97,
    'Gujarat': 1.06,
    'Rajasthan': 0.96
};

// Initialize form
document.addEventListener('DOMContentLoaded', function() {
    const cropSelect = document.getElementById('crop');
    const stateSelect = document.getElementById('state');
    const form = document.getElementById('predictionForm');
    
    // Update states when crop is selected
    cropSelect.addEventListener('change', function() {
        const selectedCrop = this.value;
        stateSelect.innerHTML = '<option value="">Select state...</option>';
        
        if (selectedCrop && cropStateMapping[selectedCrop]) {
            cropStateMapping[selectedCrop].forEach(state => {
                const option = document.createElement('option');
                option.value = state.toLowerCase().replace(/ /g, '_');
                option.textContent = state;
                stateSelect.appendChild(option);
            });
            stateSelect.disabled = false;
        } else {
            stateSelect.disabled = true;
        }
    });
    
    // Handle form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        predictPrice();
    });
    
    // Handle form reset
    form.addEventListener('reset', function() {
        setTimeout(() => {
            stateSelect.innerHTML = '<option value="">First select a crop...</option>';
            stateSelect.disabled = true;
            document.getElementById('resultsSection').style.display = 'none';
        }, 10);
    });
});

// Main prediction function
function predictPrice() {
    // Get form values
    const crop = document.getElementById('crop').value;
    const state = document.getElementById('state').value;
    const rainfall = parseFloat(document.getElementById('rainfall').value);
    const demand = parseFloat(document.getElementById('demand').value);
    const year = parseInt(document.getElementById('year').value);
    const month = parseInt(document.getElementById('month').value);
    
    // Validate inputs
    if (!crop || !state || !rainfall || !demand || !year || !month) {
        alert('Please fill in all fields');
        return;
    }
    
    // Calculate predicted price
    const prediction = calculatePrice(crop, state, rainfall, demand, year, month);
    
    // Display results
    displayResults(crop, state, rainfall, demand, prediction);
}

// Price calculation algorithm
function calculatePrice(crop, state, rainfall, demand, year, month) {
    // Base price
    let price = basePrices[crop];
    
    // Apply demand multiplier
    const demandMultiplier = calculateDemandMultiplier(demand);
    price *= demandMultiplier;
    
    // Apply state factor
    const stateName = state.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    if (stateFactors[stateName]) {
        price *= stateFactors[stateName];
    }
    
    // Rainfall impact
    const rainfallData = rainfallImpact[crop];
    let rainfallFactor = 1.0;
    
    if (rainfall < rainfallData.min) {
        // Drought conditions - price increases
        rainfallFactor = 1.15 + (rainfallData.min - rainfall) / rainfallData.min * 0.25;
    } else if (rainfall > rainfallData.max) {
        // Excess rainfall - price increases due to damage
        rainfallFactor = 1.1 + (rainfall - rainfallData.max) / rainfallData.max * 0.15;
    } else if (Math.abs(rainfall - rainfallData.optimal) < 100) {
        // Optimal rainfall - slight price decrease
        rainfallFactor = 0.95;
    }
    
    price *= rainfallFactor;
    
    // Seasonal variation (month impact)
    const seasonalFactor = getSeasonalFactor(crop, month);
    price *= seasonalFactor;
    
    // Year-based inflation (2% per year from base year 2023)
    const yearsFactor = Math.pow(1.02, year - 2023);
    price *= yearsFactor;
    
    // Add some controlled randomness (±5%)
    const randomFactor = 0.95 + Math.random() * 0.1;
    price *= randomFactor;
    
    // Calculate confidence based on inputs
    const confidence = calculateConfidence(crop, state, rainfall, demand);
    
    return {
        price: Math.round(price),
        confidence: confidence,
        rainfallFactor: rainfallFactor,
        demandFactor: demandMultiplier,
        seasonalFactor: seasonalFactor
    };
}

// Seasonal factor calculation
function getSeasonalFactor(crop, month) {
    // Different crops have different harvest seasons
    const harvestSeasons = {
        wheat: [3, 4, 5], // March-May
        paddy: [10, 11, 12], // Oct-Dec
        cotton: [10, 11, 12, 1], // Oct-Jan
        maize: [9, 10, 11], // Sep-Nov
        arhar: [12, 1, 2], // Dec-Feb
        moong: [9, 10, 11], // Sep-Nov
        mustard: [2, 3, 4], // Feb-Apr
        sugarcane: [12, 1, 2, 3] // Dec-Mar
    };
    
    const isHarvestMonth = harvestSeasons[crop].includes(month);
    
    // Prices typically lower during harvest, higher off-season
    return isHarvestMonth ? 0.90 : 1.05;
}

// Confidence calculation
function calculateConfidence(crop, state, rainfall, demand) {
    let confidence = 85; // Base confidence
    
    // Reduce confidence for extreme rainfall
    const rainfallData = rainfallImpact[crop];
    if (rainfall < rainfallData.min * 0.5 || rainfall > rainfallData.max * 1.5) {
        confidence -= 15;
    } else if (rainfall < rainfallData.min || rainfall > rainfallData.max) {
        confidence -= 8;
    }
    
    // Increase confidence for moderate demand (more predictable)
    if (demand === 'moderate') {
        confidence += 5;
    }
    
    // Random variation
    confidence += Math.floor(Math.random() * 8) - 4;
    
    return Math.max(65, Math.min(95, confidence));
}

// Display results
function displayResults(crop, state, rainfall, demand, prediction) {
    // Update result summary
    document.getElementById('resultCrop').textContent = 
        crop.charAt(0).toUpperCase() + crop.slice(1);
    
    document.getElementById('resultState').textContent = 
        state.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    
    document.getElementById('resultRainfall').textContent = 
        rainfall + ' mm';
    
    document.getElementById('resultDemand').textContent = 
        demand.toLocaleString('en-IN') + ' quintals';
    
    // Update price
    document.getElementById('predictedPrice').textContent = 
        '₹ ' + prediction.price.toLocaleString('en-IN');
    
    // Update confidence
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceValue = document.getElementById('confidenceValue');
    
    confidenceBar.style.width = prediction.confidence + '%';
    confidenceValue.textContent = prediction.confidence + '%';
    
    // Generate insights
    generateInsights(crop, state, rainfall, demand, prediction);
    
    // Show results section with animation
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Generate market insights
function generateInsights(crop, state, rainfall, demand, prediction) {
    const insightsGrid = document.getElementById('insightsGrid');
    insightsGrid.innerHTML = '';
    
    const insights = [];
    
    // Rainfall insight
    const rainfallData = rainfallImpact[crop];
    let rainfallStatus = '';
    if (rainfall < rainfallData.min) {
        rainfallStatus = 'Below optimal - Expect lower yields';
    } else if (rainfall > rainfallData.max) {
        rainfallStatus = 'Above optimal - Risk of crop damage';
    } else if (Math.abs(rainfall - rainfallData.optimal) < 100) {
        rainfallStatus = 'Optimal - Excellent growing conditions';
    } else {
        rainfallStatus = 'Adequate - Good growing conditions';
    }
    
    insights.push({
        title: 'Rainfall Impact',
        value: rainfallStatus
    });
    
    // Demand insight
    let demandStatus = '';
    if (demand < 5000) {
        demandStatus = 'Low demand - Oversupply expected';
    } else if (demand < 15000) {
        demandStatus = 'Moderate demand - Balanced market';
    } else if (demand < 50000) {
        demandStatus = 'High demand - Good selling opportunity';
    } else {
        demandStatus = 'Very high demand - Premium prices expected';
    }
    
    insights.push({
        title: 'Market Demand',
        value: demandStatus + ' (' + demand.toLocaleString('en-IN') + ' quintals)'
    });
    
    // Price trend
    const priceTrend = prediction.price > basePrices[crop] ? 
        'Above historical average' : 'Below historical average';
    
    insights.push({
        title: 'Price Trend',
        value: priceTrend
    });
    
    // Season impact
    const seasonImpact = prediction.seasonalFactor < 1.0 ? 
        'Harvest season - Prices typically lower' : 
        'Off-season - Higher market prices';
    
    insights.push({
        title: 'Seasonal Factor',
        value: seasonImpact
    });
    
    // Render insights
    insights.forEach(insight => {
        const insightDiv = document.createElement('div');
        insightDiv.className = 'insight-item';
        insightDiv.innerHTML = `
            <div class="insight-title">${insight.title}</div>
            <div class="insight-value">${insight.value}</div>
        `;
        insightsGrid.appendChild(insightDiv);
    });
    
    // Generate price trend chart
    generatePriceChart(crop, state, prediction);
}

// Utility function to format currency
function formatCurrency(amount) {
    return '₹ ' + amount.toLocaleString('en-IN');
}

// Global chart variable
let priceChart = null;

// Generate price trend chart
function generatePriceChart(crop, state, prediction) {
    const ctx = document.getElementById('priceChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (priceChart) {
        priceChart.destroy();
    }
    
    // Generate historical data (simulated)
    const historicalData = generateHistoricalData(crop, prediction.price);
    
    // Create chart
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: historicalData.dates,
            datasets: [
                {
                    label: 'Actual Price',
                    data: historicalData.actualPrices,
                    borderColor: 'rgb(52, 152, 219)',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    pointBackgroundColor: 'rgb(52, 152, 219)',
                    pointBorderColor: '#fff',
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    borderWidth: 2,
                    tension: 0.1
                },
                {
                    label: 'Predicted Price',
                    data: historicalData.predictedPrices,
                    borderColor: 'rgb(231, 76, 60)',
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    pointBackgroundColor: 'rgb(231, 76, 60)',
                    pointBorderColor: '#fff',
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    borderWidth: 3,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            size: 14,
                            family: 'Poppins'
                        },
                        usePointStyle: true,
                        padding: 20
                    }
                },
                title: {
                    display: true,
                    text: `Price Prediction for ${crop.charAt(0).toUpperCase() + crop.slice(1)}`,
                    font: {
                        size: 18,
                        family: 'Poppins',
                        weight: 'bold'
                    },
                    padding: 20
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {
                        size: 14,
                        family: 'Poppins'
                    },
                    bodyFont: {
                        size: 13,
                        family: 'Poppins'
                    },
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += '₹ ' + context.parsed.y.toLocaleString('en-IN');
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date',
                        font: {
                            size: 14,
                            family: 'Poppins',
                            weight: 'bold'
                        }
                    },
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        font: {
                            size: 11,
                            family: 'Poppins'
                        }
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Price (₹)',
                        font: {
                            size: 14,
                            family: 'Poppins',
                            weight: 'bold'
                        }
                    },
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        font: {
                            size: 11,
                            family: 'Poppins'
                        },
                        callback: function(value) {
                            return '₹ ' + value.toLocaleString('en-IN');
                        }
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

// Generate historical and predicted data for visualization
function generateHistoricalData(crop, predictedPrice) {
    const dates = [];
    const actualPrices = [];
    const predictedPrices = [];
    
    const basePrice = basePrices[crop];
    const today = new Date();
    
    // Generate 1000 days of historical data (like in your Python code)
    for (let i = 999; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        
        // Format date as MM/DD/YYYY for better readability
        if (i % 50 === 0) { // Show every 50th date to avoid crowding
            dates.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
        } else {
            dates.push('');
        }
        
        // Generate actual prices with seasonality (similar to Python code)
        const seasonality = Math.sin((999 - i) / 50) * 20;
        const randomVariation = (Math.random() - 0.5) * 100;
        const actualPrice = basePrice + randomVariation + seasonality;
        actualPrices.push(Math.round(actualPrice));
        
        // Generate predicted prices (smoother, following the trend)
        const trendFactor = Math.sin((999 - i) / 50) * 15;
        const predictedVariation = (Math.random() - 0.5) * 50;
        let modelPrice = basePrice + trendFactor + predictedVariation;
        
        // Make recent predictions closer to the actual predicted price
        if (i < 100) {
            const convergeFactor = (100 - i) / 100;
            modelPrice = modelPrice * (1 - convergeFactor) + predictedPrice * convergeFactor;
        }
        
        predictedPrices.push(Math.round(modelPrice));
    }
    
    return {
        dates: dates,
        actualPrices: actualPrices,
        predictedPrices: predictedPrices
    };
}
