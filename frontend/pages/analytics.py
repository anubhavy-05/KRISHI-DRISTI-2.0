"""
Advanced Analytics Dashboard
Krishi Drishti 2.0 - Market Intelligence & Analytics
"""
import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="📊 Advanced Analytics - Krishi Drishti",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000/api/v1"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .risk-low {
        background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
    }
    .risk-medium {
        background: linear-gradient(135deg, #FFC107 0%, #FF9800 100%);
    }
    .risk-high {
        background: linear-gradient(135deg, #F44336 0%, #E91E63 100%);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #F0F2F6;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================

def fetch_crops():
    """Fetch available crops from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/crops", timeout=5)
        if response.status_code == 200:
            return response.json().get("crops", [])
    except:
        pass
    return ["Wheat", "Paddy", "Sugarcane", "Maize", "Cotton", "Mustard", "Arhar", "Moong"]

def fetch_states(crop):
    """Fetch available states for a crop"""
    try:
        response = requests.get(f"{API_BASE_URL}/crops/{crop}/states", timeout=5)
        if response.status_code == 200:
            return response.json().get("states", [])
    except:
        pass
    return []

def fetch_analytics_data(endpoint, crop, state, **params):
    """Generic function to fetch analytics data"""
    try:
        url = f"{API_BASE_URL}/analytics/{endpoint}/{crop}/{state}"
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("data", {})
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timeout. Please try again.")
        return None
    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        return None

# ==================== VISUALIZATION FUNCTIONS ====================

def plot_volatility_gauge(volatility_data):
    """Create volatility risk gauge chart"""
    risk_score = volatility_data.get("risk_score", 2)
    volatility_pct = volatility_data.get("volatility_percentage", 0)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=volatility_pct,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Price Volatility %", 'font': {'size': 24}},
        delta={'reference': 5, 'increasing': {'color': "red"}},
        gauge={
            'axis': {'range': [None, 20], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 5], 'color': '#4CAF50'},
                {'range': [5, 10], 'color': '#FFC107'},
                {'range': [10, 20], 'color': '#F44336'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': volatility_pct
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def plot_seasonal_patterns(seasonal_data):
    """Create seasonal pattern bar chart"""
    monthly_data = seasonal_data.get("monthly_data", [])
    
    if not monthly_data:
        return None
    
    df = pd.DataFrame(monthly_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['month_name'],
        y=df['average_price'],
        marker=dict(
            color=df['average_price'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Price (₹)")
        ),
        text=df['average_price'].round(2),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Price: ₹%{y:.2f}<extra></extra>'
    ))
    
    # Highlight best and worst months
    best_month = seasonal_data.get("best_month", {}).get("name")
    worst_month = seasonal_data.get("worst_month", {}).get("name")
    
    fig.update_layout(
        title="📅 Month-wise Average Prices",
        xaxis_title="Month",
        yaxis_title="Average Price (₹/quintal)",
        height=400,
        hovermode='x',
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def plot_year_over_year_trends(trends_data):
    """Create year-over-year comparison line chart"""
    yearly_data = trends_data.get("yearly_data", [])
    
    if not yearly_data:
        return None
    
    df = pd.DataFrame(yearly_data)
    
    fig = go.Figure()
    
    # Add line for average price
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['average_price'],
        mode='lines+markers+text',
        name='Average Price',
        line=dict(color='#2E7D32', width=3),
        marker=dict(size=12, color='#4CAF50'),
        text=df['average_price'].round(2),
        textposition='top center',
        hovertemplate='<b>Year %{x}</b><br>Price: ₹%{y:.2f}<extra></extra>'
    ))
    
    # Add range area
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['max_price'],
        mode='lines',
        name='Max Price',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['min_price'],
        mode='lines',
        name='Price Range',
        line=dict(width=0),
        fillcolor='rgba(46, 125, 50, 0.2)',
        fill='tonexty',
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title="📈 Year-over-Year Price Trends",
        xaxis_title="Year",
        yaxis_title="Price (₹/quintal)",
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def plot_sentiment_indicator(sentiment_data):
    """Create market sentiment visualization"""
    sentiment = sentiment_data.get("sentiment", "Neutral")
    confidence = sentiment_data.get("confidence", 50)
    rsi = sentiment_data.get("rsi", 50)
    
    # Create subplot with two gauges
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}]],
        subplot_titles=("Confidence Score", "RSI (Relative Strength Index)")
    )
    
    # Confidence gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=confidence,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 33], 'color': '#F44336'},
                {'range': [33, 66], 'color': '#FFC107'},
                {'range': [66, 100], 'color': '#4CAF50'}
            ]
        }
    ), row=1, col=1)
    
    # RSI gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=rsi,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "purple"},
            'steps': [
                {'range': [0, 30], 'color': '#4CAF50'},  # Oversold
                {'range': [30, 70], 'color': '#9E9E9E'},  # Neutral
                {'range': [70, 100], 'color': '#F44336'}  # Overbought
            ]
        }
    ), row=1, col=2)
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

# ==================== MAIN APP ====================

def main():
    # Header
    st.markdown('<p class="main-header">📊 Advanced Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown("### 🎯 Market Intelligence & Price Analysis")
    
    # Sidebar - Selection Controls
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/analytics.png", width=80)
        st.title("🔧 Analytics Controls")
        
        # Crop selection
        crops = fetch_crops()
        selected_crop = st.selectbox("🌾 Select Crop", crops, key="crop_selector")
        
        # State selection
        if selected_crop:
            states = fetch_states(selected_crop)
            selected_state = st.selectbox("📍 Select State", states, key="state_selector")
        else:
            selected_state = None
        
        st.markdown("---")
        
        # Period selection
        period_days = st.slider("📅 Analysis Period (days)", 7, 90, 30, step=7)
        
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        st.info("💡 **Tip**: Use tabs above to explore different analytics")
    
    # Main content
    if not selected_crop or not selected_state:
        st.warning("⚠️ Please select both Crop and State from the sidebar to view analytics")
        return
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Volatility Analysis",
        "📅 Seasonal Patterns",
        "📈 Year-over-Year Trends",
        "🎯 Market Sentiment",
        "💰 Profit Opportunities"
    ])
    
    # ==================== TAB 1: VOLATILITY ANALYSIS ====================
    with tab1:
        st.header("📊 Price Volatility Analysis")
        
        with st.spinner("Loading volatility data..."):
            volatility_data = fetch_analytics_data(
                "volatility", selected_crop, selected_state, 
                period_days=period_days
            )
        
        if volatility_data:
            # Key metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                risk_level = volatility_data.get("risk_level", "Medium")
                risk_color = volatility_data.get("risk_color", "🟡")
                st.metric(
                    "Risk Level",
                    f"{risk_color} {risk_level}",
                    delta=None
                )
            
            with col2:
                volatility_pct = volatility_data.get("volatility_percentage", 0)
                st.metric(
                    "Volatility",
                    f"{volatility_pct:.2f}%",
                    delta=None
                )
            
            with col3:
                avg_price = volatility_data.get("average_price", 0)
                st.metric(
                    "Average Price",
                    f"₹{avg_price:.2f}",
                    delta=None
                )
            
            with col4:
                latest_price = volatility_data.get("latest_price", 0)
                st.metric(
                    "Latest Price",
                    f"₹{latest_price:.2f}",
                    delta=None
                )
            
            # Volatility gauge
            col1, col2 = st.columns([1, 1])
            
            with col1:
                gauge_fig = plot_volatility_gauge(volatility_data)
                st.plotly_chart(gauge_fig, use_container_width=True)
            
            with col2:
                st.markdown("### 📋 Volatility Details")
                
                price_range = volatility_data.get("price_range", {})
                std_dev = volatility_data.get("standard_deviation", 0)
                cv = volatility_data.get("coefficient_variation", 0)
                
                st.markdown(f"""
                **Price Range:**
                - 🔻 Minimum: ₹{price_range.get('min', 0):.2f}
                - 🔺 Maximum: ₹{price_range.get('max', 0):.2f}
                - 📏 Range: ₹{price_range.get('max', 0) - price_range.get('min', 0):.2f}
                
                **Statistical Measures:**
                - Standard Deviation: ₹{std_dev:.2f}
                - Coefficient of Variation: {cv:.2f}%
                - Data Points: {volatility_data.get('data_points', 0)}
                """)
                
                # Risk interpretation
                if risk_level == "Low":
                    st.success("✅ **Low Risk**: Prices are stable. Good for long-term planning.")
                elif risk_level == "Medium":
                    st.warning("⚠️ **Medium Risk**: Moderate price fluctuations. Monitor regularly.")
                else:
                    st.error("🚨 **High Risk**: Significant price volatility. Consider hedging strategies.")
    
    # ==================== TAB 2: SEASONAL PATTERNS ====================
    with tab2:
        st.header("📅 Seasonal Price Patterns")
        
        with st.spinner("Analyzing seasonal patterns..."):
            seasonal_data = fetch_analytics_data("seasonal", selected_crop, selected_state)
        
        if seasonal_data:
            # Best and worst months
            col1, col2 = st.columns(2)
            
            with col1:
                best_month = seasonal_data.get("best_month", {})
                st.markdown(f"""
                <div class="metric-card risk-low">
                    <h3>📈 Best Month to Sell</h3>
                    <h2>{best_month.get('name', 'N/A')}</h2>
                    <h1>₹{best_month.get('average_price', 0):.2f}</h1>
                    <p>Average price per quintal</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                worst_month = seasonal_data.get("worst_month", {})
                st.markdown(f"""
                <div class="metric-card risk-high">
                    <h3>📉 Worst Month to Sell</h3>
                    <h2>{worst_month.get('name', 'N/A')}</h2>
                    <h1>₹{worst_month.get('average_price', 0):.2f}</h1>
                    <p>Average price per quintal</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Price difference
            price_diff = seasonal_data.get("price_difference", {})
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Price Difference",
                    f"₹{price_diff.get('absolute', 0):.2f}",
                    delta=f"{price_diff.get('percentage', 0):.1f}%"
                )
            
            with col2:
                peak_season = seasonal_data.get("peak_season", "N/A")
                st.metric("Peak Season", peak_season)
            
            with col3:
                recommendation = seasonal_data.get("recommendation", "")
                st.info(f"💡 {recommendation}")
            
            # Seasonal pattern chart
            st.markdown("### 📊 Month-wise Price Analysis")
            seasonal_fig = plot_seasonal_patterns(seasonal_data)
            if seasonal_fig:
                st.plotly_chart(seasonal_fig, use_container_width=True)
            
            # Monthly data table
            with st.expander("📋 View Detailed Monthly Data"):
                monthly_data = seasonal_data.get("monthly_data", [])
                if monthly_data:
                    df = pd.DataFrame(monthly_data)
                    st.dataframe(
                        df.style.highlight_max(subset=['average_price'], color='lightgreen')
                              .highlight_min(subset=['average_price'], color='lightcoral'),
                        use_container_width=True
                    )
    
    # ==================== TAB 3: YEAR-OVER-YEAR TRENDS ====================
    with tab3:
        st.header("📈 Year-over-Year Price Trends")
        
        # Years selector
        years_to_analyze = st.slider("Select number of years", 2, 5, 3)
        
        with st.spinner("Analyzing trends..."):
            trends_data = fetch_analytics_data(
                "trends", selected_crop, selected_state,
                years=years_to_analyze
            )
        
        if trends_data:
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                cagr = trends_data.get("cagr", 0)
                st.metric(
                    "CAGR",
                    f"{cagr:.2f}%",
                    delta=None,
                    help="Compound Annual Growth Rate"
                )
            
            with col2:
                trend = trends_data.get("trend_direction", "Stable")
                st.metric("Trend", trend)
            
            with col3:
                avg_growth = trends_data.get("average_yearly_growth", 0)
                st.metric(
                    "Avg. Growth",
                    f"{avg_growth:.2f}%"
                )
            
            with col4:
                years_analyzed = trends_data.get("years_analyzed", 0)
                st.metric("Years Analyzed", years_analyzed)
            
            # Trend chart
            st.markdown("### 📊 Multi-Year Price Comparison")
            trends_fig = plot_year_over_year_trends(trends_data)
            if trends_fig:
                st.plotly_chart(trends_fig, use_container_width=True)
            
            # Growth rates
            st.markdown("### 📈 Year-over-Year Growth Rates")
            growth_rates = trends_data.get("growth_rates", [])
            if growth_rates:
                for growth in growth_rates:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**{growth['from_year']} → {growth['to_year']}**")
                    with col2:
                        pct = growth['growth_percentage']
                        color = "🟢" if pct > 0 else "🔴" if pct < 0 else "🟡"
                        st.write(f"{color} {pct:+.2f}%")
                    with col3:
                        st.write(f"₹{growth['absolute_change']:+.2f}")
            
            # Price range info
            price_range = trends_data.get("price_range", {})
            if price_range:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.success(f"""
                    **📈 Highest Price Year**
                    - Year: {price_range.get('highest_year')}
                    - Price: ₹{price_range.get('highest_price', 0):.2f}
                    """)
                
                with col2:
                    st.error(f"""
                    **📉 Lowest Price Year**
                    - Year: {price_range.get('lowest_year')}
                    - Price: ₹{price_range.get('lowest_price', 0):.2f}
                    """)
    
    # ==================== TAB 4: MARKET SENTIMENT ====================
    with tab4:
        st.header("🎯 Market Sentiment Analysis")
        
        with st.spinner("Analyzing market sentiment..."):
            sentiment_data = fetch_analytics_data("sentiment", selected_crop, selected_state)
        
        if sentiment_data:
            # Sentiment header
            sentiment = sentiment_data.get("sentiment", "Neutral")
            sentiment_emoji = sentiment_data.get("sentiment_emoji", "➡️")
            recommendation = sentiment_data.get("recommendation", "HOLD")
            confidence = sentiment_data.get("confidence", 50)
            
            # Main sentiment display
            if sentiment == "Bullish":
                sentiment_class = "risk-low"
            elif sentiment == "Bearish":
                sentiment_class = "risk-high"
            else:
                sentiment_class = "risk-medium"
            
            st.markdown(f"""
            <div class="metric-card {sentiment_class}">
                <h2>{sentiment_emoji} Market Sentiment: {sentiment}</h2>
                <h3>Recommendation: {recommendation}</h3>
                <p>Confidence: {confidence:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Metrics row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                current_price = sentiment_data.get("current_price", 0)
                st.metric("Current Price", f"₹{current_price:.2f}")
            
            with col2:
                rsi = sentiment_data.get("rsi", 50)
                rsi_status = sentiment_data.get("indicators", {}).get("rsi_status", "Normal")
                st.metric("RSI", f"{rsi:.1f}", delta=rsi_status)
            
            with col3:
                momentum = sentiment_data.get("momentum", 0)
                st.metric("Momentum", f"{momentum:+.2f}%")
            
            with col4:
                price_changes = sentiment_data.get("price_changes", {})
                change_1w = price_changes.get("1_week", 0)
                st.metric("1-Week Change", f"{change_1w:+.2f}%")
            
            # Sentiment indicators
            col1, col2 = st.columns([1, 1])
            
            with col1:
                sentiment_fig = plot_sentiment_indicator(sentiment_data)
                st.plotly_chart(sentiment_fig, use_container_width=True)
            
            with col2:
                st.markdown("### 📊 Sentiment Indicators")
                
                indicators = sentiment_data.get("indicators", {})
                
                st.markdown(f"""
                **RSI Analysis:**
                - Current RSI: {rsi:.1f}
                - Status: {indicators.get('rsi_status', 'Normal')}
                - Interpretation: {"Overbought - Sell signal" if rsi > 70 else "Oversold - Buy signal" if rsi < 30 else "Normal range"}
                
                **Momentum Analysis:**
                - 10-day Momentum: {momentum:.2f}%
                - Status: {indicators.get('momentum_status', 'Moderate')}
                """)
                
                # Price changes
                st.markdown("**Recent Price Changes:**")
                change_1m = price_changes.get("1_month", 0)
                
                if change_1w > 0:
                    st.success(f"↗️ 1-Week: +{change_1w:.2f}%")
                else:
                    st.error(f"↘️ 1-Week: {change_1w:.2f}%")
                
                if change_1m > 0:
                    st.success(f"↗️ 1-Month: +{change_1m:.2f}%")
                else:
                    st.error(f"↘️ 1-Month: {change_1m:.2f}%")
    
    # ==================== TAB 5: PROFIT OPPORTUNITIES ====================
    with tab5:
        st.header("💰 Profit Opportunity Analysis")
        
        # Get prediction first
        st.markdown("### 🔮 Enter Predicted Price")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            predicted_price = st.number_input(
                "Predicted Future Price (₹/quintal)",
                min_value=0.0,
                value=2500.0,
                step=50.0,
                help="Enter the predicted price from your model"
            )
        
        with col2:
            threshold = st.slider(
                "Profit Threshold %",
                min_value=5,
                max_value=30,
                value=15,
                step=5
            )
        
        if st.button("🔍 Analyze Profit Opportunity", use_container_width=True):
            with st.spinner("Analyzing profit opportunities..."):
                opportunity_data = fetch_analytics_data(
                    "opportunities", selected_crop, selected_state,
                    predicted_price=predicted_price,
                    threshold_percent=threshold
                )
            
            if opportunity_data:
                # Opportunity status
                opportunity_found = opportunity_data.get("opportunity_found", False)
                action = opportunity_data.get("action", "MONITOR")
                action_emoji = opportunity_data.get("action_emoji", "👁️")
                message = opportunity_data.get("message", "")
                
                if action == "HOLD":
                    alert_class = "risk-low"
                elif action == "SELL NOW":
                    alert_class = "risk-high"
                else:
                    alert_class = "risk-medium"
                
                st.markdown(f"""
                <div class="metric-card {alert_class}">
                    <h2>{action_emoji} Action: {action}</h2>
                    <p style="font-size: 1.2rem;">{message}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Price comparison
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    current_price = opportunity_data.get("current_price", 0)
                    st.metric("Current Price", f"₹{current_price:.2f}")
                
                with col2:
                    pred_price = opportunity_data.get("predicted_price", 0)
                    st.metric("Predicted Price", f"₹{pred_price:.2f}")
                
                with col3:
                    price_diff = opportunity_data.get("price_difference", {})
                    pct_change = price_diff.get("percentage", 0)
                    st.metric(
                        "Expected Change",
                        f"₹{price_diff.get('absolute', 0):.2f}",
                        delta=f"{pct_change:+.2f}%"
                    )
                
                # Confidence and risk
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    confidence = opportunity_data.get("confidence_level", "MEDIUM")
                    conf_color = opportunity_data.get("confidence_color", "🟡")
                    st.metric("Confidence", f"{conf_color} {confidence}")
                
                with col2:
                    risk = opportunity_data.get("risk_assessment", "Medium")
                    st.metric("Risk Level", risk)
                
                with col3:
                    rec_details = opportunity_data.get("recommendation_details", {})
                    stop_loss = rec_details.get("stop_loss_price", 0)
                    st.metric("Stop Loss", f"₹{stop_loss:.2f}")
                
                # Profit scenarios
                st.markdown("### 💵 Profit Scenarios")
                profit_scenarios = opportunity_data.get("profit_scenarios", [])
                
                if profit_scenarios:
                    scenario_df = pd.DataFrame(profit_scenarios)
                    scenario_df['profit'] = scenario_df['profit'].apply(lambda x: f"₹{x:,.2f}")
                    scenario_df.columns = ['Quantity (Quintal)', 'Expected Profit']
                    
                    st.table(scenario_df.set_index('Quantity (Quintal)'))
                
                # Recommendations
                with st.expander("📋 Detailed Recommendations"):
                    rec_details = opportunity_data.get("recommendation_details", {})
                    
                    st.markdown(f"""
                    **Investment Strategy:**
                    - Should Hold: {'✅ Yes' if rec_details.get('should_hold') else '❌ No'}
                    - Should Sell Now: {'✅ Yes' if rec_details.get('should_sell_now') else '❌ No'}
                    - Estimated Days to Target: {rec_details.get('estimated_days_to_target', 'N/A')}
                    - Stop Loss Price: ₹{rec_details.get('stop_loss_price', 0):.2f}
                    
                    **Risk Management:**
                    - Set stop loss at 10% below current price
                    - Monitor daily price movements
                    - Review prediction accuracy weekly
                    - Diversify across multiple crops if possible
                    """)

# ==================== RUN APP ====================

if __name__ == "__main__":
    main()
