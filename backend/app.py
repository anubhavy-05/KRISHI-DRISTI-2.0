"""
FastAPI Backend Application - Main entry point
Krishi Drishti Crop Price Prediction API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="🌾 Krishi Drishti API",
    description="AI-powered Crop Price Prediction System for Indian Farmers",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS (allow frontend to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["Crop Prediction"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🌾 Welcome to Krishi Drishti API",
        "version": "2.0.0",
        "documentation": "/docs",
        "api_base": "/api/v1"
    }


if __name__ == "__main__":
    print("="*70)
    print("🌾 KRISHI DRISHTI API SERVER")
    print("="*70)
    print("📡 Starting FastAPI server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔄 Interactive API: http://localhost:8000/redoc")
    print("="*70)
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
