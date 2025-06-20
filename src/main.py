from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import os
import sys

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import PassengerData, SurvivalPrediction, HealthCheck, ErrorResponse
from predictor import TitanicPredictor

# Initialize FastAPI app
app = FastAPI(
    title="Titanic Survival Prediction API",
    description="A REST API for predicting survival on the Titanic using machine learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor
predictor = TitanicPredictor()

@app.on_event("startup")
async def startup_event():
    """Load the model on startup"""
    success = predictor.load_model()
    if not success:
        print("Warning: Model could not be loaded")

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Titanic Survival Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "predict": "/predict"
    }

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy" if predictor.is_loaded else "unhealthy",
        model_loaded=predictor.is_loaded,
        timestamp=datetime.now().isoformat()
    )

@app.post("/predict", response_model=SurvivalPrediction)
async def predict_survival(passenger: PassengerData):
    """Predict survival probability for a passenger"""
    if not predictor.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    try:
        passenger_dict = passenger.dict()
        survived, probability, confidence = predictor.predict_survival(passenger_dict)
        
        return SurvivalPrediction(
            survived=survived,
            survival_probability=probability,
            confidence=confidence
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

@app.get("/model-info", response_model=dict)
async def get_model_info():
    """Get information about the loaded model"""
    return predictor.get_model_info()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom exception handler for HTTP errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=f"HTTP {exc.status_code}: {exc.detail}"
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).dict()
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 