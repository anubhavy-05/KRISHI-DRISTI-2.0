"""
API Routes - REST endpoints for crop price prediction system
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.prediction_service import PredictionService
from services.weather_service import WeatherService

router = APIRouter()

# Initialize services
prediction_service = PredictionService()
weather_service = WeatherService()


# ==================== REQUEST MODELS ====================

class PredictionRequest(BaseModel):
    crop: str = Field(..., description="Crop name (e.g., Wheat, Paddy)")
    state: str = Field(..., description="State name (e.g., Punjab, Uttar Pradesh)")
    date: str = Field(..., description="Prediction date in YYYY-MM-DD format")
    rainfall: Optional[float] = Field(None, description="Rainfall in mm (auto-fetched if not provided)")
    demand: float = Field(..., ge=0, description="Market demand value")

class WeatherRequest(BaseModel):
    state: str = Field(..., description="State name")
    date: str = Field(..., description="Date in YYYY-MM-DD format")


# ==================== API ENDPOINTS ====================

@router.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🌾 Krishi Drishti API - Crop Price Prediction System",
        "version": "2.0",
        "endpoints": {
            "GET /crops": "Get list of supported crops",
            "GET /crops/{crop_name}/states": "Get states for a crop",
            "POST /predict": "Predict crop price",
            "POST /weather": "Get weather data",
            "GET /history/{crop}/{state}": "Get historical prices"
        }
    }


@router.get("/crops")
async def get_crops():
    """Get list of all supported crops"""
    try:
        crops = prediction_service.get_supported_crops()
        return {
            "success": True,
            "crops": sorted(crops),
            "total": len(crops)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crops/{crop_name}/states")
async def get_states_for_crop(crop_name: str):
    """Get list of states where a crop is available"""
    try:
        # Capitalize crop name for consistency
        crop_name = crop_name.title()
        states = prediction_service.get_states_for_crop(crop_name)
        
        if not states:
            raise HTTPException(
                status_code=404, 
                detail=f"Crop '{crop_name}' not found. Available crops: {', '.join(prediction_service.get_supported_crops())}"
            )
        
        return {
            "success": True,
            "crop": crop_name,
            "states": states,
            "total": len(states)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict")
async def predict_price(request: PredictionRequest):
    """
    Predict crop price based on input parameters
    
    - **crop**: Name of the crop
    - **state**: State name
    - **date**: Prediction date (YYYY-MM-DD)
    - **rainfall**: Rainfall in mm (optional, will be auto-fetched)
    - **demand**: Market demand value
    """
    try:
        # Validate date format
        try:
            datetime.strptime(request.date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use YYYY-MM-DD"
            )
        
        # Auto-fetch rainfall if not provided
        rainfall = request.rainfall
        weather_info = None
        
        if rainfall is None:
            weather_data = weather_service.fetch_weather_data(request.state, request.date)
            if weather_data.get("success"):
                rainfall = weather_data["rainfall"]
                weather_info = weather_data
            else:
                # Use default value if weather fetch fails
                rainfall = weather_data.get("default_rainfall", 25.0)
                weather_info = {"warning": weather_data.get("error")}
        
        # Make prediction
        result = prediction_service.predict_price(
            crop_name=request.crop,
            state_name=request.state,
            prediction_date=request.date,
            rainfall=rainfall,
            demand=request.demand
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        # Add weather info to response
        if weather_info:
            result["weather_data"] = weather_info
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.post("/weather")
async def get_weather(request: WeatherRequest):
    """
    Get weather data for a specific state and date
    
    - **state**: State name
    - **date**: Date in YYYY-MM-DD format
    """
    try:
        result = weather_service.fetch_weather_data(request.state, request.date)
        
        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error"),
                "default_rainfall": result.get("default_rainfall")
            }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{crop}/{state}")
async def get_historical_prices(
    crop: str, 
    state: str, 
    days: Optional[int] = 30
):
    """
    Get historical price data for a crop in a specific state
    
    - **crop**: Crop name
    - **state**: State name
    - **days**: Number of days of historical data (default: 30)
    """
    try:
        if days < 1 or days > 365:
            raise HTTPException(
                status_code=400,
                detail="Days must be between 1 and 365"
            )
        
        result = prediction_service.get_historical_prices(
            crop_name=crop.title(),
            state_name=state.title(),
            days=days
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("error"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Krishi Drishti API"
    }
