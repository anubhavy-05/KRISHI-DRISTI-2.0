"""
Weather Service - Fetches real-time weather data from OpenWeatherMap API
"""
import requests
from datetime import datetime


class WeatherService:
    """Service class for weather data operations"""
    
    STATE_COORDINATES = {
        'Uttar Pradesh': {'lat': 26.8467, 'lon': 80.9462},  # Lucknow
        'Punjab': {'lat': 30.7333, 'lon': 76.7794},  # Chandigarh
        'Madhya Pradesh': {'lat': 23.2599, 'lon': 77.4126},  # Bhopal
        'West Bengal': {'lat': 22.5726, 'lon': 88.3639},  # Kolkata
        'Maharashtra': {'lat': 19.0760, 'lon': 72.8777},  # Mumbai
        'Rajasthan': {'lat': 26.9124, 'lon': 75.7873},  # Jaipur
        'Gujarat': {'lat': 23.0225, 'lon': 72.5714},  # Ahmedabad
    }
    
    def __init__(self, api_key="6b1edcf5240c69d1d1f63b17130896a7"):
        self.api_key = api_key
    
    def fetch_weather_data(self, state_name, date_str):
        """
        Fetches weather data from OpenWeatherMap API
        
        Args:
            state_name: Name of the state
            date_str: Date in YYYY-MM-DD format
            
        Returns:
            dict: Weather data with rainfall and temperature
        """
        if state_name not in self.STATE_COORDINATES:
            return {
                "success": False,
                "error": f"Coordinates not available for {state_name}"
            }
        
        coords = self.STATE_COORDINATES[state_name]
        lat, lon = coords['lat'], coords['lon']
        
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d')
            current_date = datetime.now()
            days_diff = (target_date - current_date).days
            
            if abs(days_diff) <= 5:  # Within 5 days - use current/forecast API
                if days_diff < 0:
                    url = "https://api.openweathermap.org/data/2.5/weather"
                else:
                    url = "https://api.openweathermap.org/data/2.5/forecast"
                
                params = {
                    'lat': lat,
                    'lon': lon,
                    'appid': self.api_key,
                    'units': 'metric'
                }
                
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                # Extract rainfall data
                rainfall = 0
                if 'rain' in data:
                    rainfall = data['rain'].get('1h', 0) or data['rain'].get('3h', 0)
                elif 'list' in data and len(data['list']) > 0:
                    for item in data['list']:
                        if 'rain' in item:
                            rainfall += item['rain'].get('3h', 0)
                    rainfall = rainfall / len(data['list']) if data['list'] else 0
                
                # Get temperature and weather description
                temperature = None
                description = None
                
                if 'main' in data:
                    temperature = data['main'].get('temp')
                elif 'list' in data and len(data['list']) > 0:
                    temperature = data['list'][0]['main'].get('temp')
                
                if 'weather' in data and len(data['weather']) > 0:
                    description = data['weather'][0].get('description', 'N/A')
                elif 'list' in data and len(data['list']) > 0:
                    description = data['list'][0]['weather'][0].get('description', 'N/A')
                
                return {
                    "success": True,
                    "rainfall": round(rainfall, 2),
                    "temperature": round(temperature, 1) if temperature else None,
                    "description": description,
                    "state": state_name,
                    "date": date_str,
                    "source": "OpenWeatherMap API"
                }
            else:
                return {
                    "success": False,
                    "error": f"Date is too far ({abs(days_diff)} days). API data not available.",
                    "default_rainfall": 25.0  # Fallback value
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API Error: {str(e)}",
                "default_rainfall": 25.0
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error fetching weather data: {str(e)}",
                "default_rainfall": 25.0
            }
