"""
Prediction Service - Core ML prediction logic extracted from main script
"""
import pandas as pd
import numpy as np
import joblib
import os
from datetime import timedelta, datetime


class PredictionService:
    """Service class for crop price predictions"""
    
    SUPPORTED_CROPS_AND_STATES = {
        'Wheat': ['Uttar Pradesh', 'Punjab', 'Madhya Pradesh'],
        'Paddy': ['West Bengal', 'Punjab', 'Uttar Pradesh'],
        'Sugarcane': ['Uttar Pradesh', 'Maharashtra'],
        'Maize': ['Madhya Pradesh', 'Uttar Pradesh'],
        'Arhar': ['Maharashtra', 'Madhya Pradesh', 'Uttar Pradesh'],
        'Moong': ['Rajasthan', 'Madhya Pradesh'],
        'Cotton': ['Gujarat', 'Maharashtra', 'Punjab'],
        'Mustard': ['Rajasthan', 'Madhya Pradesh']
    }
    
    def __init__(self, models_dir="../", data_file="../all_crop_data.csv"):
        self.models_dir = models_dir
        self.data_file = data_file
        
    def get_supported_crops(self):
        """Returns list of supported crops"""
        return list(self.SUPPORTED_CROPS_AND_STATES.keys())
    
    def get_states_for_crop(self, crop_name):
        """Returns list of states for a given crop"""
        return self.SUPPORTED_CROPS_AND_STATES.get(crop_name, [])
    
    def predict_price(self, crop_name, state_name, prediction_date, rainfall, demand):
        """
        Predicts crop price using trained model
        
        Args:
            crop_name: Name of the crop
            state_name: State name
            prediction_date: Date for prediction (YYYY-MM-DD)
            rainfall: Rainfall in mm
            demand: Market demand value
            
        Returns:
            dict: Prediction result with price and metadata
        """
        try:
            # Load model
            model_filename = os.path.join(
                self.models_dir,
                f"{crop_name.lower()}_{state_name.lower().replace(' ', '_')}_price_model.joblib"
            )
            
            if not os.path.exists(model_filename):
                return {
                    "success": False,
                    "error": f"Model not found for {crop_name} in {state_name}"
                }
            
            model = joblib.load(model_filename)
            
            # Load historical data
            if not os.path.exists(self.data_file):
                return {
                    "success": False,
                    "error": "Historical data file not found"
                }
            
            df_hist_full = pd.read_csv(self.data_file)
            df_hist_full['Date'] = pd.to_datetime(df_hist_full['Date'])
            
            # Filter for specific crop and state
            df_hist = df_hist_full[
                (df_hist_full['Crop'] == crop_name) & 
                (df_hist_full['State'] == state_name)
            ]
            
            if df_hist.empty:
                return {
                    "success": False,
                    "error": f"No historical data for {crop_name} in {state_name}"
                }
            
            # Feature engineering
            pred_date = pd.to_datetime(prediction_date)
            month = pred_date.month
            day_of_week = pred_date.dayofweek
            
            # Calculate moving average
            start_date = pred_date - timedelta(days=7)
            end_date = pred_date - timedelta(days=1)
            
            recent_data = df_hist[
                (df_hist['Date'] >= start_date) & 
                (df_hist['Date'] <= end_date)
            ]
            
            if recent_data.empty:
                moving_avg = df_hist['Price'].iloc[-1]
            else:
                moving_avg = recent_data['Price'].mean()
            
            # Prepare input features
            features = ['Rainfall', 'Demand', 'month', 'day_of_week', 'moving_average_7_day']
            input_data = pd.DataFrame(
                [[rainfall, demand, month, day_of_week, moving_avg]], 
                columns=features
            )
            
            # Make prediction
            predicted_price = model.predict(input_data)[0]
            
            # Calculate statistics for context
            historical_avg = df_hist['Price'].mean()
            historical_min = df_hist['Price'].min()
            historical_max = df_hist['Price'].max()
            
            return {
                "success": True,
                "predicted_price": round(predicted_price, 2),
                "crop": crop_name,
                "state": state_name,
                "date": prediction_date,
                "rainfall": rainfall,
                "demand": demand,
                "statistics": {
                    "historical_average": round(historical_avg, 2),
                    "historical_min": round(historical_min, 2),
                    "historical_max": round(historical_max, 2),
                    "vs_average_percent": round(((predicted_price - historical_avg) / historical_avg) * 100, 2)
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Prediction error: {str(e)}"
            }
    
    def get_historical_prices(self, crop_name, state_name, days=30):
        """
        Get historical price data for visualization
        
        Args:
            crop_name: Name of the crop
            state_name: State name
            days: Number of days of historical data
            
        Returns:
            dict: Historical price data
        """
        try:
            if not os.path.exists(self.data_file):
                return {"success": False, "error": "Data file not found"}
            
            df = pd.read_csv(self.data_file)
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Filter for specific crop and state
            df_filtered = df[
                (df['Crop'] == crop_name) & 
                (df['State'] == state_name)
            ].sort_values('Date')
            
            # Get last N days
            df_recent = df_filtered.tail(days)
            
            return {
                "success": True,
                "dates": df_recent['Date'].dt.strftime('%Y-%m-%d').tolist(),
                "prices": df_recent['Price'].round(2).tolist(),
                "rainfall": df_recent['Rainfall'].round(2).tolist(),
                "demand": df_recent['Demand'].round(2).tolist()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error fetching historical data: {str(e)}"
            }
