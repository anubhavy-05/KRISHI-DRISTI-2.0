Rimport pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import os
import joblib
from datetime import timedelta
import requests
from datetime import datetime

# ==============================================================================
# PART 0: WEATHER API INTEGRATION
# ==============================================================================

# OpenWeatherMap API Configuration
# Get your free API key from: https://openweathermap.org/api
OPENWEATHER_API_KEY = "6b1edcf5240c69d1d1f63b17130896a7"  # Replace with your actual API key

# State to coordinates mapping (major cities in each state)
STATE_COORDINATES = {
    'Uttar Pradesh': {'lat': 26.8467, 'lon': 80.9462},  # Lucknow
    'Punjab': {'lat': 30.7333, 'lon': 76.7794},  # Chandigarh
    'Madhya Pradesh': {'lat': 23.2599, 'lon': 77.4126},  # Bhopal
    'West Bengal': {'lat': 22.5726, 'lon': 88.3639},  # Kolkata
    'Maharashtra': {'lat': 19.0760, 'lon': 72.8777},  # Mumbai
    'Rajasthan': {'lat': 26.9124, 'lon': 75.7873},  # Jaipur
    'Gujarat': {'lat': 23.0225, 'lon': 72.5714},  # Ahmedabad
}

def fetch_weather_data(state_name, date_str):
    """
    Fetches weather data from OpenWeatherMap API for given state and date.
    Returns rainfall in mm or None if data unavailable.
    """
    if OPENWEATHER_API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  OpenWeatherMap API key not configured.")
        print("   Get free API key from: https://openweathermap.org/api")
        return None
    
    if state_name not in STATE_COORDINATES:
        print(f"⚠️  Coordinates not available for {state_name}")
        return None
    
    coords = STATE_COORDINATES[state_name]
    lat, lon = coords['lat'], coords['lon']
    
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        current_date = datetime.now()
        
        # Check if date is in future or past
        days_diff = (target_date - current_date).days
        
        if abs(days_diff) <= 5:  # Within 5 days - use current/forecast API
            if days_diff < 0:
                print(f"📅 Date is in recent past. Using current weather data.")
                url = f"https://api.openweathermap.org/data/2.5/weather"
            else:
                print(f"📅 Date is {days_diff} days in future. Using forecast data.")
                url = f"https://api.openweathermap.org/data/2.5/forecast"
            
            params = {
                'lat': lat,
                'lon': lon,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract rainfall data
            if 'rain' in data:
                rainfall = data['rain'].get('1h', 0) + data['rain'].get('3h', 0)
            elif 'list' in data and len(data['list']) > 0:
                # Forecast data - average rainfall
                rainfall_sum = 0
                count = 0
                for item in data['list']:
                    if 'rain' in item:
                        rainfall_sum += item['rain'].get('3h', 0)
                        count += 1
                rainfall = rainfall_sum / count if count > 0 else 0
            else:
                rainfall = 0  # No rain data available
            
            print(f"🌧️  Weather API Response: {rainfall:.2f} mm rainfall")
            if 'weather' in data and len(data['weather']) > 0:
                weather_desc = data['weather'][0]['description']
                print(f"   Weather: {weather_desc}")
            
            return round(rainfall, 2)
        
        else:
            print(f"📅 Date is too far ({abs(days_diff)} days). API data not available.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error fetching weather data: {e}")
        return None

# ==============================================================================
# PART 1: SETUP & TRAINING LOGIC (Using a Single Data File)
# ==============================================================================

## NEW FUNCTION ##
def create_all_placeholder_data(file_path, crop_state_config):
    """Generates a single placeholder CSV file with dummy data for all crops and states."""
    print(f"Generating a single placeholder data file for all crops at '{file_path}'...")
    all_data_frames = []

    for crop_name, states in crop_state_config.items():
        for state_name in states:
            date_range = pd.date_range(start='2023-01-01', periods=1000, freq='D')
            
            base_prices = {
                'Arhar': 6300, 'Cotton': 7500, 'Moong': 6800, 'Mustard': 5500,
                'Wheat': 2125, 'Paddy': 2040, 'Maize': 1962, 'Sugarcane': 350
            }
            base_price = base_prices.get(crop_name, 2000)

            state_multiplier = {
                'Uttar Pradesh': 1.0, 'Punjab': 1.05, 'Madhya Pradesh': 0.98,
                'West Bengal': 0.95, 'Maharashtra': 1.02, 'Rajasthan': 0.97, 'Gujarat': 1.08
            }
            price_multiplier = state_multiplier.get(state_name, 1.0)
            final_base_price = base_price * price_multiplier

            df = pd.DataFrame({
                'Date': date_range,
                'Crop': crop_name,  # New 'Crop' column
                'State': state_name, # New 'State' column
                'Price': np.random.rand(1000) * (final_base_price * 0.1) + np.linspace(final_base_price, final_base_price * 1.1, 1000),
                'Rainfall': np.random.rand(1000) * 50,
                'Demand': np.random.rand(1000) * 200 + 500,
            })
            all_data_frames.append(df)
    
    # Combine all data into a single DataFrame and save
    final_df = pd.concat(all_data_frames, ignore_index=True)
    final_df.to_csv(file_path, index=False)
    print("Single data file generated successfully.")

## MODIFIED ##: Function now accepts a DataFrame and filters it, instead of reading a file.
def train_and_save_crop_model(full_df, crop_name, state_name):
    """Trains a model on a filtered slice of the main DataFrame."""
    print(f"--- Training Model for {crop_name} in {state_name} ---")
    
    # Filter the main DataFrame for the specific crop and state
    df = full_df[(full_df['Crop'] == crop_name) & (full_df['State'] == state_name)].copy()

    if df.empty:
        print(f"Warning: No data found for {crop_name} in {state_name}. Skipping.")
        return
        
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    df['month'] = df.index.month
    df['day_of_week'] = df.index.dayofweek
    df['moving_average_7_day'] = df['Price'].rolling(window=7).mean()
    df.dropna(inplace=True)

    features = ['Rainfall', 'Demand', 'month', 'day_of_week', 'moving_average_7_day']
    X = df[features]
    y = df['Price']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    model_filename = f"{crop_name.lower()}_{state_name.lower().replace(' ', '_')}_price_model.joblib"
    joblib.dump(model, model_filename)
    print(f"Model for {crop_name} in {state_name} saved as '{model_filename}'\n")

## MODIFIED ##: Main setup function now orchestrates using the single data file.
def run_initial_setup_and_training(crop_state_config):
    """Generates a single data file (if needed) and trains all models from it."""
    print("="*70)
    print("STARTING INITIAL SETUP AND MODEL TRAINING (FROM SINGLE DATA FILE)")
    print("="*70)
    
    data_file = "all_crop_data.csv"
    if not os.path.exists(data_file):
        create_all_placeholder_data(data_file, crop_state_config)
    else:
        print(f"Found existing data file: '{data_file}'.")
    
    # Load the entire dataset once
    full_dataset = pd.read_csv(data_file)
    
    for crop, states in crop_state_config.items():
        for state in states:
            model_file = f"{crop.lower()}_{state.lower().replace(' ', '_')}_price_model.joblib"
            if not os.path.exists(model_file):
                # Pass the full dataset to the training function
                train_and_save_crop_model(full_dataset, crop, state)
            else:
                print(f"Model for {crop} in {state} already exists. Skipping training.\n")
    
    print("\n" + "="*70)
    print("SETUP COMPLETE. ALL STATE-SPECIFIC MODELS ARE READY.")
    print("="*70 + "\n")

# ==============================================================================
# PART 2: PREDICTION LOGIC (MODIFIED TO USE SINGLE DATA FILE)
# ==============================================================================

## MODIFIED ##: Function now reads the single data file and filters it.
def predict_crop_price(crop_name, state_name, prediction_date, rainfall, demand):
    """Predicts the price by loading the single data file and filtering it."""
    model_filename = f"{crop_name.lower()}_{state_name.lower().replace(' ', '_')}_price_model.joblib"
    try:
        model = joblib.load(model_filename)
    except FileNotFoundError:
        print(f"Error: Model file '{model_filename}' not found.")
        return None

    data_filename = "all_crop_data.csv"
    try:
        df_hist_full = pd.read_csv(data_filename)
        df_hist_full['Date'] = pd.to_datetime(df_hist_full['Date'])
        
        # Filter for the relevant historical data
        df_hist = df_hist_full[(df_hist_full['Crop'] == crop_name) & (df_hist_full['State'] == state_name)]
        if df_hist.empty:
            print(f"Error: Could not find historical data for {crop_name} in {state_name} in {data_filename}")
            return None
    except FileNotFoundError:
        print(f"Error: Historical data file '{data_filename}' not found.")
        return None

    try:
        pred_date = pd.to_datetime(prediction_date)
        month = pred_date.month
        day_of_week = pred_date.dayofweek
        
        start_date = pred_date - timedelta(days=7)
        end_date = pred_date - timedelta(days=1)
        
        recent_data = df_hist[(df_hist['Date'] >= start_date) & (df_hist['Date'] <= end_date)]
        
        if recent_data.empty:
            moving_avg = df_hist['Price'].iloc[-1]
        else:
            moving_avg = recent_data['Price'].mean()

    except Exception as e:
        print(f"An error occurred during feature engineering: {e}")
        return None
        
    features = ['Rainfall', 'Demand', 'month', 'day_of_week', 'moving_average_7_day']
    input_data = pd.DataFrame([[rainfall, demand, month, day_of_week, moving_avg]], columns=features)
    
    predicted_price = model.predict(input_data)[0]
    return predicted_price

# ==============================================================================
# PART 3: MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    
    # This dictionary now just defines the structure of what to create and train
    supported_crops_and_states = {
        'Wheat': ['Uttar Pradesh', 'Punjab', 'Madhya Pradesh'],
        'Paddy': ['West Bengal', 'Punjab', 'Uttar Pradesh'],
        'Sugarcane': ['Uttar Pradesh', 'Maharashtra'],
        'Maize': ['Madhya Pradesh', 'Uttar Pradesh'],
        'Arhar': ['Maharashtra', 'Madhya Pradesh', 'Uttar Pradesh'],
        'Moong': ['Rajasthan', 'Madhya Pradesh'],
        'Cotton': ['Gujarat', 'Maharashtra', 'Punjab'],
        'Mustard': ['Rajasthan', 'Madhya Pradesh']
    }
    
    run_initial_setup_and_training(supported_crops_and_states)
    
    # The interactive loop remains the same as before
    while True:
        print("\n--- Crop Price Prediction ---")
        print("Available crops:", ", ".join(sorted(supported_crops_and_states.keys())))
        print("Type 'quit' to exit.")

        crop_input = input("Enter the crop name: ").strip().title()
        if crop_input.lower() in ['quit', 'exit', 'q']:
            break
        if crop_input not in supported_crops_and_states:
            print(f"Error: '{crop_input}' is not a supported crop. Please try again.")
            continue
        
        available_states = supported_crops_and_states[crop_input]
        print(f"Available states for {crop_input}: {', '.join(available_states)}")
        while True:
            state_input = input(f"Enter the state for {crop_input}: ").strip().title()
            if state_input in available_states:
                break
            else:
                print(f"Error: Invalid state. Please choose from: {', '.join(available_states)}")
        
        while True:
            date_input = input(f"Enter the prediction date (YYYY-MM-DD): ").strip()
            try:
                pd.to_datetime(date_input, format='%Y-%m-%d')
                break 
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        # Try to fetch rainfall data from API
        print("\n🌐 Fetching real-time weather data...")
        rainfall_val = fetch_weather_data(state_input, date_input)
        
        if rainfall_val is None:
            # Fallback to manual input
            print("\n⚠️  Could not fetch weather data automatically.")
            print("   Please enter rainfall manually:")
            while True:
                rainfall_input = input(f"Enter the rainfall in mm: ").strip()
                try:
                    rainfall_val = float(rainfall_input)
                    break
                except ValueError:
                    print("Invalid input. Please enter a number for rainfall.")
        else:
            print(f"✅ Using API rainfall data: {rainfall_val} mm")
            # Allow user to override if they want
            override = input("   Press Enter to use this value, or type new value to override: ").strip()
            if override:
                try:
                    rainfall_val = float(override)
                    print(f"   Using manual override: {rainfall_val} mm")
                except ValueError:
                    print("   Invalid input. Using API value.")
                
        while True:
            demand_input = input(f"Enter the market demand value: ").strip()
            try:
                demand_val = float(demand_input)
                break
            except ValueError:
                print("Invalid input. Please enter a number for demand.")

        predicted_price = predict_crop_price(
            crop_name=crop_input,
            state_name=state_input, 
            prediction_date=date_input,
            rainfall=rainfall_val,
            demand=demand_val
        )

        if predicted_price is not None:
            print("\n" + "*"*50)
            print(f"✅ PREDICTION RESULT:")
            print(f"The predicted price for {crop_input} in {state_input} on {date_input}")
            print(f"with rainfall of {rainfall_val} mm and demand of {demand_val} is:")
            print(f"---->   ₹ {predicted_price:.2f} per quintal   <----")
            print("*"*50)
        else:
            print("\nCould not generate a prediction due to an error.")

    # Clean up the generated files after the user quits
    print("\nExiting program and cleaning up generated files...")
    if os.path.exists("all_crop_data.csv"):
        os.remove("all_crop_data.csv")
    
    all_files_in_dir = os.listdir('.')
    for file in all_files_in_dir:
        if file.endswith('.joblib'):
            os.remove(file)
    print("Cleanup complete.")