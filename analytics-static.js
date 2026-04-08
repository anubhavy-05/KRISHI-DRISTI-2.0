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

let analyticsRows = [];
let charts = {
  volatility: null,
  seasonal: null,
  trend: null,
  sentiment: null,
  momentum: null
};

const monthNames = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];

function formatCurrency(value) {
  return `₹${Math.round(value).toLocaleString('en-IN')}`;
}

function calculateDemandMultiplier(demand) {
  if (demand <= 0) return 0.7;
  if (demand < 5000) return 0.75 + (demand / 5000) * 0.15;
  if (demand < 15000) return 0.9 + ((demand - 5000) / 10000) * 0.2;
  if (demand < 50000) return 1.1 + ((demand - 15000) / 35000) * 0.2;
  return Math.min(1.5, 1.3 + ((demand - 50000) / 50000) * 0.2);
}

function getSeasonalFactor(crop, month) {
  const harvestSeasons = {
    wheat: [3, 4, 5],
    paddy: [10, 11, 12],
    cotton: [10, 11, 12, 1],
    maize: [9, 10, 11],
    arhar: [12, 1, 2],
    moong: [9, 10, 11],
    mustard: [2, 3, 4],
    sugarcane: [12, 1, 2, 3]
  };

  return harvestSeasons[crop].includes(month) ? 0.9 : 1.05;
}

function calculateProjectedPrice(crop, state, rainfall, demand, year, month) {
  let price = basePrices[crop] || 2000;
  price *= calculateDemandMultiplier(demand);

  const stateFactors = {
    'Madhya Pradesh': 0.98,
    'Maharashtra': 1.05,
    'Punjab': 1.08,
    'Uttar Pradesh': 1.0,
    'West Bengal': 0.97,
    'Gujarat': 1.06,
    'Rajasthan': 0.96
  };

  if (stateFactors[state]) {
    price *= stateFactors[state];
  }

  const rainfallData = rainfallImpact[crop] || rainfallImpact.wheat;
  let rainfallFactor = 1;
  if (rainfall < rainfallData.min) {
    rainfallFactor = 1.15 + (rainfallData.min - rainfall) / rainfallData.min * 0.25;
  } else if (rainfall > rainfallData.max) {
    rainfallFactor = 1.1 + (rainfall - rainfallData.max) / rainfallData.max * 0.15;
  } else if (Math.abs(rainfall - rainfallData.optimal) < 100) {
    rainfallFactor = 0.95;
  }
  price *= rainfallFactor;
  price *= getSeasonalFactor(crop, month);
  price *= Math.pow(1.02, year - 2023);
  return Math.round(price);
}

function parseCsvRows(csvText) {
  const lines = csvText.trim().split(/\r?\n/);
  return lines.slice(1).map(line => line.split(',')).filter(parts => parts.length >= 6).map(parts => ({
    date: parts[0],
    crop: parts[1],
    state: parts[2],
    price: Number(parts[3]),
    rainfall: Number(parts[4]),
    demand: Number(parts[5])
  })).filter(row => row.date && row.crop && row.state && Number.isFinite(row.price));
}

function groupBy(list, keyFn) {
  return list.reduce((acc, item) => {
    const key = keyFn(item);
    if (!acc[key]) acc[key] = [];
    acc[key].push(item);
    return acc;
  }, {});
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function stdDev(values) {
  const avg = mean(values);
  const variance = mean(values.map(value => Math.pow(value - avg, 2)));
  return Math.sqrt(variance);
}

function linearTrend(values) {
  if (values.length < 2) return 0;
  return values[values.length - 1] - values[0];
}

function calculateRsi(values, period = 14) {
  if (values.length < period + 1) return 50;
  let gains = 0;
  let losses = 0;
  for (let i = values.length - period; i < values.length; i++) {
    const change = values[i] - values[i - 1];
    if (change >= 0) gains += change;
    else losses -= change;
  }
  const avgGain = gains / period;
  const avgLoss = losses / period || 0.0001;
  const rs = avgGain / avgLoss;
  return Math.max(0, Math.min(100, 100 - (100 / (1 + rs))));
}

function updateAnalysisHeader(crop, state) {
  document.getElementById('analyticsTitle').textContent = `Price Analysis: ${crop} in ${state}`;
  document.getElementById('analyticsSubtitle').textContent = `Advanced market intelligence for ${crop} in ${state}.`;
  const topTitle = document.getElementById('analyticsTopTitle');
  if (topTitle) {
    topTitle.textContent = `📈 Price Analysis: ${crop} in ${state}`;
  }
}

function setActiveTab(tabName) {
  document.querySelectorAll('.analytics-tab').forEach(button => {
    button.classList.toggle('active', button.dataset.tab === tabName);
  });
  document.querySelectorAll('.analytics-panel').forEach(panel => {
    panel.classList.toggle('active', panel.dataset.panel === tabName);
  });
}

function clearChart(chartKey) {
  if (charts[chartKey]) {
    charts[chartKey].destroy();
    charts[chartKey] = null;
  }
}

function centerTextPlugin() {
  return {
    id: 'centerText',
    afterDraw(chart, args, options) {
      const { ctx, chartArea } = chart;
      if (!chartArea || !options || !options.text) return;
      const x = (chartArea.left + chartArea.right) / 2;
      const y = (chartArea.top + chartArea.bottom) / 2;
      ctx.save();
      ctx.fillStyle = options.color || '#2c3e50';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.font = `${options.fontWeight || 700} ${options.fontSize || 28}px Poppins, sans-serif`;
      ctx.fillText(options.text, x, y - 6);
      if (options.subtext) {
        ctx.font = `500 ${options.subFontSize || 14}px Poppins, sans-serif`;
        ctx.fillStyle = options.subColor || '#7f8c8d';
        ctx.fillText(options.subtext, x, y + 20);
      }
      ctx.restore();
    }
  };
}

function drawVolatilityChart(volatility, riskColor, riskLevel) {
  const ctx = document.getElementById('volatilityChart').getContext('2d');
  clearChart('volatility');
  charts.volatility = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Low Risk', 'Moderate Risk', 'High Risk'],
      datasets: [
        {
          data: [5, 5, 10],
          backgroundColor: ['#4caf50', '#ffc107', '#f44336'],
          borderWidth: 0,
          hoverOffset: 0,
          cutout: '68%',
          weight: 1
        },
        {
          data: [Math.min(volatility, 20), Math.max(0, 20 - Math.min(volatility, 20))],
          backgroundColor: [riskColor, 'rgba(229, 231, 235, 0.35)'],
          borderWidth: 0,
          hoverOffset: 0,
          cutout: '82%',
          weight: 1.4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      rotation: -90,
      circumference: 180,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false },
        centerText: {
          text: `${volatility.toFixed(1)}%`,
          subtext: riskLevel ? `${riskLevel} risk` : 'volatility'
        }
      }
    },
    plugins: [centerTextPlugin()]
  });
}

function drawSeasonalChart(monthlySummary) {
  const ctx = document.getElementById('seasonalChart').getContext('2d');
  clearChart('seasonal');
  charts.seasonal = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: monthlySummary.map(entry => entry.name),
      datasets: [{
        label: 'Average Price',
        data: monthlySummary.map(entry => entry.avg),
        backgroundColor: monthlySummary.map(entry => entry.avgColor || '#4caf50'),
        borderRadius: 10,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { callback: value => `₹ ${Math.round(value).toLocaleString('en-IN')}` }
        }
      }
    }
  });
}

function drawTrendChart(yearSummary) {
  const ctx = document.getElementById('trendChart').getContext('2d');
  clearChart('trend');
  charts.trend = new Chart(ctx, {
    type: 'line',
    data: {
      labels: yearSummary.map(entry => entry.year),
      datasets: [{
        label: 'Average Price',
        data: yearSummary.map(entry => entry.avg),
        borderColor: '#2e7d32',
        backgroundColor: 'rgba(46,125,50,0.12)',
        tension: 0.3,
        fill: true,
        pointRadius: 5,
        pointBackgroundColor: '#2e7d32'
      }, {
        label: 'Minimum Price',
        data: yearSummary.map(entry => entry.min),
        borderColor: '#42a5f5',
        borderDash: [6, 4],
        tension: 0.3,
        fill: false,
        pointRadius: 3
      }, {
        label: 'Maximum Price',
        data: yearSummary.map(entry => entry.max),
        borderColor: '#ef5350',
        borderDash: [6, 4],
        tension: 0.3,
        fill: false,
        pointRadius: 3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom' } },
      scales: {
        y: { ticks: { callback: value => `₹ ${Math.round(value).toLocaleString('en-IN')}` } }
      }
    }
  });
}

function drawSentimentChart(confidence) {
  const ctx = document.getElementById('sentimentChart').getContext('2d');
  clearChart('sentiment');
  charts.sentiment = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Confidence', 'Remaining'],
      datasets: [{
        data: [confidence, 100 - confidence],
        backgroundColor: ['#4caf50', '#e5e7eb'],
        borderWidth: 0,
        cutout: '75%'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      rotation: -90,
      circumference: 180,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false },
        centerText: {
          text: `${confidence.toFixed(0)}%`,
          subtext: 'confidence'
        }
      }
    },
    plugins: [centerTextPlugin()]
  });
}

function drawMomentumChart(prices) {
  const ctx = document.getElementById('momentumChart').getContext('2d');
  clearChart('momentum');
  charts.momentum = new Chart(ctx, {
    type: 'line',
    data: {
      labels: prices.map((_, index) => index + 1),
      datasets: [{
        label: 'Price Momentum',
        data: prices,
        borderColor: '#7c4dff',
        backgroundColor: 'rgba(124,77,255,0.12)',
        tension: 0.35,
        fill: true,
        pointRadius: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { ticks: { callback: value => `₹ ${Math.round(value).toLocaleString('en-IN')}` } },
        x: { display: false }
      }
    }
  });
}

function renderAnalytics() {
  const crop = document.getElementById('analyticsCrop').value;
  const state = document.getElementById('analyticsState').value;
  const dateValue = document.getElementById('analyticsDate').value;
  const periodDays = Number(document.getElementById('analyticsPeriod').value);
  const demandInput = document.getElementById('analyticsDemand').value;
  const rainfallInput = document.getElementById('analyticsRainfall').value;

  if (!crop || !state) return;

  const filtered = analyticsRows
    .filter(row => row.crop === crop && row.state === state)
    .sort((a, b) => new Date(a.date) - new Date(b.date));

  if (!filtered.length) return;

  updateAnalysisHeader(crop, state);

  const lastRows = filtered.slice(-periodDays);
  const prices = lastRows.map(row => row.price);
  const avg = mean(prices);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const latest = prices[prices.length - 1];
  const std = stdDev(prices);
  const volatility = (std / avg) * 100;
  const riskLevel = volatility < 5 ? 'Low' : volatility < 10 ? 'Medium' : 'High';
  const riskColor = riskLevel === 'Low' ? '#4caf50' : riskLevel === 'Medium' ? '#ffc107' : '#f44336';

  const avgRainfall = mean(lastRows.map(row => row.rainfall || 0));
  const avgDemand = mean(lastRows.map(row => row.demand || 0));
  const rainfall = rainfallInput ? Number(rainfallInput) : avgRainfall;
  const demand = demandInput ? Number(demandInput) : avgDemand;

  let projectedPrice = null;
  if (dateValue) {
    const predDate = new Date(dateValue);
    projectedPrice = calculateProjectedPrice(crop.toLowerCase(), state, rainfall, demand, predDate.getFullYear(), predDate.getMonth() + 1);
  }

  document.getElementById('analyticsPeriodValue').textContent = periodDays;
  document.getElementById('volRiskLevel').textContent = riskLevel;
  document.getElementById('volatilityPct').textContent = `${volatility.toFixed(1)}%`;
  document.getElementById('volAverage').textContent = formatCurrency(avg);
  document.getElementById('volLatest').textContent = formatCurrency(latest);
  document.getElementById('volMin').textContent = formatCurrency(min);
  document.getElementById('volMax').textContent = formatCurrency(max);
  document.getElementById('volRange').textContent = formatCurrency(max - min);
  document.getElementById('volStdDev').textContent = formatCurrency(std);
  document.getElementById('volProjected').textContent = projectedPrice ? formatCurrency(projectedPrice) : '—';
  document.getElementById('volPoints').textContent = String(lastRows.length);
  document.getElementById('volInsight').textContent = riskLevel === 'Low'
    ? 'Prices are relatively stable. This market is suitable for long-term planning.'
    : riskLevel === 'Medium'
      ? 'Moderate fluctuations detected. Watch the trend closely before selling.'
      : 'High volatility detected. Consider timing and risk management carefully.';

  drawVolatilityChart(Math.min(volatility, 20), riskColor, riskLevel);

  const monthlyGroups = groupBy(filtered, row => new Date(row.date).getMonth());
  const monthlySummary = monthNames.map((name, index) => {
    const rows = monthlyGroups[index] || [];
    if (!rows.length) {
      return { name, avg: 0, min: 0, max: 0, avgColor: '#dfe6e9' };
    }
    const values = rows.map(row => row.price);
    return {
      name,
      avg: mean(values),
      min: Math.min(...values),
      max: Math.max(...values),
      avgColor: index % 2 === 0 ? '#64b5f6' : '#4caf50'
    };
  }).filter(entry => entry.avg > 0);

  if (monthlySummary.length) {
    const best = [...monthlySummary].sort((a, b) => b.avg - a.avg)[0];
    const worst = [...monthlySummary].sort((a, b) => a.avg - b.avg)[0];
    document.getElementById('bestMonthName').textContent = best.name;
    document.getElementById('bestMonthPrice').textContent = formatCurrency(best.avg);
    document.getElementById('worstMonthName').textContent = worst.name;
    document.getElementById('worstMonthPrice').textContent = formatCurrency(worst.avg);
    document.getElementById('seasonPriceDiff').textContent = formatCurrency(best.avg - worst.avg);
    document.getElementById('seasonPricePct').textContent = `${(((best.avg - worst.avg) / worst.avg) * 100).toFixed(1)}% difference`;
    drawSeasonalChart(monthlySummary);

    const seasonalTableBody = document.getElementById('seasonalTableBody');
    seasonalTableBody.innerHTML = monthlySummary.map(entry => `
      <tr>
        <td>${entry.name}</td>
        <td>${formatCurrency(entry.avg)}</td>
        <td>${formatCurrency(entry.min)}</td>
        <td>${formatCurrency(entry.max)}</td>
      </tr>
    `).join('');
  }

  const yearGroups = groupBy(filtered, row => new Date(row.date).getFullYear());
  const yearSummary = Object.entries(yearGroups).map(([year, rows]) => {
    const values = rows.map(row => row.price);
    return {
      year: Number(year),
      avg: mean(values),
      min: Math.min(...values),
      max: Math.max(...values)
    };
  }).sort((a, b) => a.year - b.year);

  const yearGrowthList = document.getElementById('trendGrowthList');
  if (yearSummary.length) {
    drawTrendChart(yearSummary);
    const first = yearSummary[0].avg;
    const last = yearSummary[yearSummary.length - 1].avg;
    const cagr = yearSummary.length > 1
      ? ((Math.pow(last / first, 1 / (yearSummary.length - 1)) - 1) * 100)
      : 0;
    const avgGrowth = yearSummary.length > 1
      ? yearSummary.slice(1).map((entry, index) => ((entry.avg - yearSummary[index].avg) / yearSummary[index].avg) * 100)
      : [0];
    document.getElementById('trendCagr').textContent = `${cagr.toFixed(1)}%`;
    document.getElementById('trendDirection').textContent = last > first ? 'Upward' : last < first ? 'Downward' : 'Stable';
    document.getElementById('trendGrowth').textContent = `${mean(avgGrowth).toFixed(1)}%`;
    document.getElementById('trendYears').textContent = String(yearSummary.length);

    if (yearSummary.length > 1) {
      const items = [];
      for (let i = 1; i < yearSummary.length; i++) {
        const prev = yearSummary[i - 1];
        const curr = yearSummary[i];
        const pct = ((curr.avg - prev.avg) / prev.avg) * 100;
        items.push(`<div class="analytics-growth-item"><strong>${prev.year} → ${curr.year}</strong><span>${pct >= 0 ? '+' : ''}${pct.toFixed(1)}%</span><span>${formatCurrency(curr.avg - prev.avg)}</span></div>`);
      }
      yearGrowthList.innerHTML = items.join('');
    } else {
      yearGrowthList.innerHTML = '<div class="analytics-empty-note">Not enough annual data in the CSV to compute year-over-year growth yet.</div>';
    }
  } else {
    document.getElementById('trendCagr').textContent = '0.0%';
    document.getElementById('trendDirection').textContent = 'Stable';
    document.getElementById('trendGrowth').textContent = '0.0%';
    document.getElementById('trendYears').textContent = '0';
    yearGrowthList.innerHTML = '<div class="analytics-empty-note">No yearly trend data found.</div>';
  }

  const recentPrices = lastRows.slice(-30).map(row => row.price);
  const trendChange = recentPrices.length > 1 ? ((recentPrices[recentPrices.length - 1] - recentPrices[0]) / recentPrices[0]) * 100 : 0;
  const confidence = Math.max(45, Math.min(95, 85 - volatility * 3 + Math.max(0, trendChange)));
  const rsi = calculateRsi(prices);
  const momentum = trendChange;
  const sentiment = confidence >= 70 ? 'Positive' : confidence >= 55 ? 'Neutral' : 'Cautious';

  document.getElementById('sentimentLabel').textContent = sentiment;
  document.getElementById('sentimentConfidence').textContent = `${confidence.toFixed(0)}%`;
  document.getElementById('sentimentRsi').textContent = rsi.toFixed(0);
  document.getElementById('sentimentMomentum').textContent = `${momentum >= 0 ? '+' : ''}${momentum.toFixed(1)}%`;
  document.getElementById('sentimentInsight').textContent = sentiment === 'Positive'
    ? 'The market is displaying constructive momentum and price stability is acceptable.'
    : sentiment === 'Neutral'
      ? 'The market is mixed. Track trend movement and seasonal pressure before deciding.'
      : 'Market conditions look cautious. Watch volatility and avoid rushed selling.';

  drawSentimentChart(confidence);
  drawMomentumChart(recentPrices.length ? recentPrices : prices.slice(-14));
}

async function initializeAnalytics() {
  const cropSelect = document.getElementById('analyticsCrop');
  const stateSelect = document.getElementById('analyticsState');
  const periodInput = document.getElementById('analyticsPeriod');
  const periodValue = document.getElementById('analyticsPeriodValue');
  const dateInput = document.getElementById('analyticsDate');
  const rainfallInput = document.getElementById('analyticsRainfall');
  const demandInput = document.getElementById('analyticsDemand');
  const refreshButton = document.getElementById('analyticsRefresh');

  try {
    const response = await fetch('all_crop_data.csv');
    const csv = await response.text();
    analyticsRows = parseCsvRows(csv);

    const crops = [...new Set(analyticsRows.map(row => row.crop))].sort((a, b) => a.localeCompare(b));
    cropSelect.innerHTML = crops.map(crop => `<option value="${crop}">${crop}</option>`).join('');
    cropSelect.value = crops[0] || '';

    if (dateInput && !dateInput.value) {
      dateInput.value = new Date().toISOString().split('T')[0];
    }

    function populateStates() {
      const crop = cropSelect.value;
      const states = [...new Set(analyticsRows.filter(row => row.crop === crop).map(row => row.state))].sort((a, b) => a.localeCompare(b));
      stateSelect.innerHTML = states.map(state => `<option value="${state}">${state}</option>`).join('');
      stateSelect.value = states[0] || '';
    }

    function syncDefaults() {
      const crop = cropSelect.value;
      const state = stateSelect.value;
      const subset = analyticsRows.filter(row => row.crop === crop && row.state === state);
      const avgRainfall = subset.length ? mean(subset.slice(-60).map(row => row.rainfall || 0)) : 0;
      const avgDemand = subset.length ? mean(subset.slice(-60).map(row => row.demand || 0)) : 0;
      if (rainfallInput && !rainfallInput.value && avgRainfall) rainfallInput.value = avgRainfall.toFixed(1);
      if (demandInput && !demandInput.value && avgDemand) demandInput.value = Math.round(avgDemand);
    }

    cropSelect.addEventListener('change', () => {
      populateStates();
      syncDefaults();
      renderAnalytics();
    });
    stateSelect.addEventListener('change', () => {
      syncDefaults();
      renderAnalytics();
    });
    periodInput.addEventListener('input', () => {
      periodValue.textContent = periodInput.value;
      renderAnalytics();
    });
    [dateInput, rainfallInput, demandInput].forEach(input => input.addEventListener('input', renderAnalytics));
    refreshButton.addEventListener('click', () => {
      populateStates();
      syncDefaults();
      renderAnalytics();
    });

    document.querySelectorAll('.analytics-tab').forEach(button => {
      button.addEventListener('click', () => setActiveTab(button.dataset.tab));
    });

    populateStates();
    syncDefaults();
    periodValue.textContent = periodInput.value;
    setActiveTab('volatility');
    renderAnalytics();
  } catch (error) {
    document.getElementById('analyticsSubtitle').textContent = 'Unable to load analytics data from all_crop_data.csv.';
  }
}

document.addEventListener('DOMContentLoaded', initializeAnalytics);
