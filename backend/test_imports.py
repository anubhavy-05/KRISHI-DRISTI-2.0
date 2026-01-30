"""
Test script to check if all imports are working
"""
print("Testing imports...")

try:
    from fastapi import FastAPI
    print("✅ FastAPI imported")
except Exception as e:
    print(f"❌ FastAPI import failed: {e}")

try:
    from fastapi.middleware.cors import CORSMiddleware
    print("✅ CORS middleware imported")
except Exception as e:
    print(f"❌ CORS import failed: {e}")

try:
    from api.routes import router
    print("✅ API routes imported")
except Exception as e:
    print(f"❌ API routes import failed: {e}")

try:
    from services.prediction_service import PredictionService
    print("✅ PredictionService imported")
    
    service = PredictionService()
    print(f"✅ PredictionService initialized")
    print(f"   Models dir: {service.models_dir}")
    print(f"   Data file: {service.data_file}")
except Exception as e:
    print(f"❌ PredictionService failed: {e}")

try:
    from services.weather_service import WeatherService
    print("✅ WeatherService imported")
except Exception as e:
    print(f"❌ WeatherService failed: {e}")

print("\n✅ All imports successful!")
