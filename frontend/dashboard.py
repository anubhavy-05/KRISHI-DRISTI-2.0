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

# ==================== CONFIGURATION ====================

API_BASE_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="🌾 Krishi Drishti",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================

st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #81C784 0%, #66BB6A 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2E7D32;
    }
    .stButton>button {
        background-color: #2E7D32;
        color: white;
        font-size: 1.1rem;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
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
    # Header
    st.markdown('<h1 class="main-header">🌾 Krishi Drishti 2.0</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Crop Price Prediction System</p>',
        unsafe_allow_html=True
    )
    
    # Sidebar
    st.sidebar.image("https://img.icons8.com/color/96/000000/plant.png", width=80)
    st.sidebar.title("🎯 Prediction Settings")
    st.sidebar.markdown("---")
    
    # Fetch crops
    crops = fetch_crops()
    
    if not crops:
        st.error("⚠️ Cannot connect to API. Please make sure the backend server is running on http://localhost:8000")
        st.info("Run: `cd backend && python app.py`")
        return
    
    # Input Form
    selected_crop = st.sidebar.selectbox(
        "🌾 Select Crop",
        options=crops,
        help="Choose the crop for price prediction"
    )
    
    # Fetch states for selected crop
    states = fetch_states(selected_crop)
    selected_state = st.sidebar.selectbox(
        "📍 Select State",
        options=states,
        help="Choose the state"
    )
    
    # Date selection
    selected_date = st.sidebar.date_input(
        "📅 Prediction Date",
        value=datetime.now(),
        min_value=datetime.now() - timedelta(days=5),
        max_value=datetime.now() + timedelta(days=30),
        help="Select date for prediction (within ±5 days for live weather data)"
    )
    
    # Demand input
    demand_value = st.sidebar.number_input(
        "📊 Market Demand",
        min_value=0.0,
        max_value=2000.0,
        value=650.0,
        step=10.0,
        help="Market demand value (typically 400-800)"
    )
    
    # Optional rainfall override
    use_custom_rainfall = st.sidebar.checkbox("⚙️ Use Custom Rainfall")
    rainfall_value = None
    if use_custom_rainfall:
        rainfall_value = st.sidebar.number_input(
            "🌧️ Rainfall (mm)",
            min_value=0.0,
            max_value=200.0,
            value=25.0,
            step=5.0
        )
    
    st.sidebar.markdown("---")
    predict_button = st.sidebar.button("🔮 Predict Price", use_container_width=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📈 Price Analysis: {selected_crop} in {selected_state}")
        
        # Fetch and display historical data
        historical_data = fetch_historical_data(selected_crop, selected_state, days=60)
        
        if historical_data.get("success"):
            df = pd.DataFrame({
                'Date': pd.to_datetime(historical_data['dates']),
                'Price': historical_data['prices'],
                'Rainfall': historical_data['rainfall']
            })
            
            # Create price trend chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df['Price'],
                mode='lines+markers',
                name='Historical Price',
                line=dict(color='#2E7D32', width=3),
                marker=dict(size=6)
            ))
            
            fig.update_layout(
                title=f"{selected_crop} Price Trend (Last 60 Days)",
                xaxis_title="Date",
                yaxis_title="Price (₹/quintal)",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Rainfall chart
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=df['Date'],
                y=df['Rainfall'],
                name='Rainfall',
                marker_color='lightblue'
            ))
            
            fig2.update_layout(
                title="Rainfall Pattern",
                xaxis_title="Date",
                yaxis_title="Rainfall (mm)",
                template='plotly_white',
                height=250
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("📊 Historical data will appear here once available")
    
    with col2:
        st.subheader("📊 Statistics")
        
        if historical_data.get("success"):
            prices = historical_data['prices']
            
            # Display metrics
            st.metric(
                label="Average Price",
                value=f"₹{sum(prices)/len(prices):.2f}",
                delta=None
            )
            
            st.metric(
                label="Minimum Price",
                value=f"₹{min(prices):.2f}",
                delta=None
            )
            
            st.metric(
                label="Maximum Price",
                value=f"₹{max(prices):.2f}",
                delta=None
            )
            
            # Price volatility
            volatility = (max(prices) - min(prices)) / (sum(prices)/len(prices)) * 100
            st.metric(
                label="Price Volatility",
                value=f"{volatility:.1f}%",
                delta=None
            )
    
    # Prediction results
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
            # Display prediction with emphasis
            col_a, col_b, col_c = st.columns([1, 2, 1])
            
            with col_b:
                st.success("✅ Prediction Successful!")
                
                # Main prediction card
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 2rem;
                        border-radius: 15px;
                        text-align: center;
                        color: white;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    ">
                        <h2 style="margin: 0; font-size: 1.2rem;">Predicted Price</h2>
                        <h1 style="margin: 10px 0; font-size: 3rem;">₹{result['predicted_price']}</h1>
                        <p style="margin: 0; font-size: 1rem;">per quintal</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Statistics comparison
                stats = result.get('statistics', {})
                vs_avg = stats.get('vs_average_percent', 0)
                
                col_x, col_y = st.columns(2)
                
                with col_x:
                    st.metric(
                        "Historical Average",
                        f"₹{stats.get('historical_average', 0):.2f}",
                        delta=None
                    )
                
                with col_y:
                    delta_color = "inverse" if vs_avg < 0 else "normal"
                    st.metric(
                        "vs Average",
                        f"{abs(vs_avg):.1f}%",
                        delta=f"{'↓' if vs_avg < 0 else '↑'}",
                        delta_color=delta_color
                    )
                
                # Weather info
                if "weather_data" in result:
                    weather = result["weather_data"]
                    if weather.get("success"):
                        st.info(f"""
                        🌤️ **Weather Info**: {weather.get('description', 'N/A').title()}  
                        🌡️ **Temperature**: {weather.get('temperature', 'N/A')}°C  
                        🌧️ **Rainfall**: {weather.get('rainfall', 0)} mm
                        """)
                
                # Recommendation
                if vs_avg > 10:
                    st.warning("⚠️ **Market Alert**: Price is significantly higher than average. Consider selling.")
                elif vs_avg < -10:
                    st.info("💡 **Market Insight**: Price is below average. Consider holding stock.")
                else:
                    st.success("✅ **Market Status**: Price is stable and within normal range.")
        
        else:
            st.error(f"❌ Prediction failed: {result.get('error', 'Unknown error')}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #888;">🌾 Krishi Drishti 2.0 | Powered by AI & Machine Learning</p>',
        unsafe_allow_html=True
    )


# ==================== RUN APP ====================

if __name__ == "__main__":
    main()
