"""
Streamlit Frontend Dashboard
Krishi Drishti - Interactive Crop Price Prediction Dashboard
"""
import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import os

# ==================== CONFIGURATION ====================

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

st.set_page_config(
    page_title="🌾 Krishi Drishti",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'About': "Krishi Drishti 2.0 - AI-Powered Crop Price Prediction"
    }
)

# ==================== CUSTOM CSS ====================

st.markdown("""
    <style>
    /* Base Responsive Styles */
    .main-header {
        font-size: clamp(1.5rem, 5vw, 3rem);
        color: #2E7D32;
        text-align: center;
        padding: clamp(0.5rem, 2vw, 1rem);
        background: linear-gradient(90deg, #81C784 0%, #66BB6A 100%);
        border-radius: 10px;
        margin-bottom: clamp(1rem, 3vw, 2rem);
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: clamp(1rem, 3vw, 1.5rem);
        border-radius: 10px;
        border-left: 5px solid #2E7D32;
    }
    .stButton>button {
        background-color: #2E7D32;
        color: white;
        font-size: clamp(1rem, 2.5vw, 1.1rem);
        padding: clamp(0.5rem, 2vw, 0.75rem) clamp(1rem, 3vw, 2rem);
        border-radius: 5px;
        border: none;
        width: 100%;
        min-height: 44px;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
    }
    
    /* Mobile Optimization */
    @media only screen and (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.5rem;
            max-width: 100%;
        }
        .stSelectbox, .stDateInput, .stNumberInput {
            font-size: 16px;
        }
        [data-testid="stSidebar"] {
            width: 280px !important;
        }
        [data-testid="column"] {
            width: 100% !important;
            flex: 100% !important;
            min-width: 100% !important;
        }
        .stButton>button {
            min-height: 48px;
            font-size: 1rem;
        }
    }
    
    /* Tablet Optimization */
    @media only screen and (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            padding: 1.5rem 1rem;
        }
        [data-testid="stSidebar"] {
            width: 300px !important;
        }
    }
    
    /* Desktop Optimization */
    @media only screen and (min-width: 1025px) {
        .main .block-container {
            padding: 2rem 1rem;
            max-width: 1400px;
        }
    }
    
    /* Large Desktop */
    @media only screen and (min-width: 1440px) {
        .main .block-container {
            max-width: 1600px;
        }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .metric-card {
            background-color: #1e1e1e;
        }
    }
    
    /* Improve plotly charts responsiveness */
    .js-plotly-plot {
        width: 100% !important;
    }
    
    /* Better input field sizing */
    input, select, textarea {
        max-width: 100%;
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==================== HELPER FUNCTIONS ====================

def fetch_crops():
    """Fetch available crops from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/crops", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("crops", [])
        return []
    except Exception as e:
        st.error(f"Error fetching crops: {e}")
        return []


def fetch_states(crop):
    """Fetch states for a given crop"""
    try:
        response = requests.get(f"{API_BASE_URL}/crops/{crop}/states", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("states", [])
        return []
    except Exception as e:
        st.error(f"Error fetching states: {e}")
        return []


def predict_price(crop, state, date, demand, rainfall=None):
    """Make price prediction via API"""
    try:
        payload = {
            "crop": crop,
            "state": state,
            "date": date,
            "demand": demand
        }
        if rainfall is not None:
            payload["rainfall"] = rainfall
        
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def fetch_historical_data(crop, state, days=30):
    """Fetch historical price data"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/history/{crop}/{state}",
            params={"days": days},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return {"success": False}
    except Exception as e:
        st.error(f"Error fetching history: {e}")
        return {"success": False}


# ==================== MAIN APP ====================

def main():
    st.title("🌾 Krishi Drishti 2.0 - Crop Price Prediction")
    st.markdown("---")
    
    # Fetch crops first
    crops = fetch_crops()
    
    if not crops:
        st.error("⚠️ Cannot connect to API. Please make sure the backend server is running on http://localhost:8000")
        st.info("Run: `cd backend && python app.py`")
        return
    
    # ========== TWO COLUMN LAYOUT ==========
    # Left: Enter Prediction Details | Right: Historical Data & Market Analysis
    col_left, col_right = st.columns([1, 2])
    
    # ========== LEFT COLUMN - ENTER PREDICTION DETAILS ==========
    with col_left:
        st.subheader("📝 Enter Prediction Details")
        st.markdown("---")
        
        # Crop selection
        selected_crop = st.selectbox(
            "🌾 Select Crop",
            options=crops,
            help="Choose the crop for price prediction"
        )
        
        # Fetch states for selected crop
        states = fetch_states(selected_crop)
        
        # State selection
        selected_state = st.selectbox(
            "📍 Select State",
            options=states,
            help="Choose the state"
        )
        
        # Date selection
        selected_date = st.date_input(
            "📅 Prediction Date",
            value=datetime.now(),
            min_value=datetime.now() - timedelta(days=5),
            max_value=datetime.now() + timedelta(days=30),
            help="Select date for prediction"
        )
        
        # Market demand
        demand_value = st.number_input(
            "📊 Market Demand",
            min_value=0.0,
            max_value=2000.0,
            value=650.0,
            step=10.0,
            help="Market demand value (typically 400-800)"
        )
        
        # Rainfall
        rainfall_value = st.number_input(
            "🌧️ Rainfall (mm)",
            min_value=0.0,
            max_value=200.0,
            value=25.0,
            step=5.0,
            help="Expected rainfall in millimeters"
        )
        
        # Predict button
        st.markdown("---")
        predict_button = st.button("🎯 Predict Price", type="primary", use_container_width=True)
    
    # ========== RIGHT COLUMN - HISTORICAL DATA & MARKET ANALYSIS ==========
    with col_right:
        st.subheader(f"📊 Historical Data & Market Analysis")
        st.markdown(f"**{selected_crop}** in **{selected_state}**")
        st.markdown("---")
        
        # Fetch historical data
        historical_data = fetch_historical_data(selected_crop, selected_state, days=60)
        
        if historical_data.get("success"):
            df = pd.DataFrame({
                'Date': pd.to_datetime(historical_data['dates']),
                'Price': historical_data['prices'],
                'Rainfall': historical_data['rainfall']
            })
            
            # Price trend chart
            st.markdown("**📈 Price Trend (Last 60 Days)**")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df['Price'],
                mode='lines+markers',
                name='Price',
                line=dict(color='#2E7D32', width=2),
                marker=dict(size=4)
            ))
            
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Price (₹/quintal)",
                hovermode='x unified',
                template='plotly_white',
                height=350,
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=30),
                font=dict(family="Inter, sans-serif", size=11),
                xaxis=dict(
                    tickformat='%b %d',
                    tickfont=dict(size=9)
                ),
                yaxis=dict(
                    tickfont=dict(size=9),
                    gridcolor='#f0f0f0'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # Statistics in compact grid
            st.markdown("**📊 Price Statistics**")
            stat_col1, stat_col2 = st.columns(2)
            
            # Calculate statistics
            prices = historical_data['prices']
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
            volatility = (max_price - min_price) / avg_price * 100
            
            with stat_col1:
                st.metric("Average Price", f"₹{avg_price:.2f}")
                st.metric("Minimum Price", f"₹{min_price:.2f}")
            
            with stat_col2:
                st.metric("Maximum Price", f"₹{max_price:.2f}")
                st.metric("Volatility", f"{volatility:.1f}%")
            
            # Rainfall chart
            st.markdown("---")
            st.markdown("**🌧️ Rainfall Pattern**")
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=df['Date'],
                y=df['Rainfall'],
                name='Rainfall',
                marker_color='#4FC3F7'
            ))
            
            fig2.update_layout(
                xaxis_title="",
                yaxis_title="Rainfall (mm)",
                template='plotly_white',
                height=200,
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=30),
                font=dict(family="Inter, sans-serif", size=11),
                xaxis=dict(
                    tickformat='%b %d',
                    tickfont=dict(size=9)
                ),
                yaxis=dict(
                    tickfont=dict(size=9),
                    gridcolor='#f0f0f0'
                )
            )
            
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("📊 Historical data will appear here once available")
    
    # ========== PREDICTION RESULTS (FULL WIDTH) ==========
    if predict_button:
        st.markdown("---")
        st.subheader("🔮 Prediction Results")
        
        with st.spinner("Analyzing data and generating prediction..."):
            result = predict_price(
                crop=selected_crop,
                state=selected_state,
                date=str(selected_date),
                demand=demand_value,
                rainfall=rainfall_value
            )
        
        if result.get("success"):
            col_a, col_b, col_c = st.columns([1, 2, 1])
            
            with col_b:
                # Main prediction card
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 100%);
                        padding: 2rem;
                        border-radius: 15px;
                        text-align: center;
                        color: white;
                        box-shadow: 0 8px 20px rgba(46, 125, 50, 0.3);
                    ">
                        <h3 style="margin: 0; font-size: 1.1rem; opacity: 0.9;">Predicted Price</h3>
                        <h1 style="margin: 15px 0; font-size: 3rem; font-weight: bold;">₹{result['predicted_price']}</h1>
                        <p style="margin: 0; font-size: 1rem; opacity: 0.9;">per quintal</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Additional info
                stats = result.get('statistics', {})
                if stats:
                    vs_avg = stats.get('vs_average_percent', 0)
                    
                    col_x, col_y = st.columns(2)
                    
                    with col_x:
                        st.metric("Historical Avg", f"₹{stats.get('historical_average', 0):.2f}")
                    
                    with col_y:
                        st.metric("vs Average", f"{abs(vs_avg):.1f}%", delta=f"{'↓' if vs_avg < 0 else '↑'}")
                
                # Recommendation
                if stats:
                    vs_avg = stats.get('vs_average_percent', 0)
                    if vs_avg > 10:
                        st.warning("⚠️ Price is significantly higher than average. Consider selling.")
                    elif vs_avg < -10:
                        st.info("💡 Price is below average. Consider holding stock.")
                    else:
                        st.success("✅ Price is stable and within normal range.")
        else:
            st.error(f"❌ Prediction failed: {result.get('error', 'Unknown error')}")


# ==================== RUN APP ====================

if __name__ == "__main__":
    main()
