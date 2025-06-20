from pydantic import BaseModel, Field
from typing import Optional

class PassengerData(BaseModel):
    """Schema for passenger data input"""
    pclass: int = Field(..., ge=1, le=3, description="Passenger class (1=First, 2=Second, 3=Third)")
    sex: str = Field(..., description="Passenger sex (male/female)")
    age: float = Field(..., ge=0, le=100, description="Passenger age")
    sibsp: int = Field(..., ge=0, description="Number of siblings/spouses aboard")
    parch: int = Field(..., ge=0, description="Number of parents/children aboard")
    fare: float = Field(..., ge=0, description="Passenger fare")
    embarked: str = Field(..., description="Port of embarkation (C=Cherbourg, Q=Queenstown, S=Southampton)")
    cabin: Optional[str] = Field(None, description="Cabin number")
    name: Optional[str] = Field(None, description="Passenger name")

class SurvivalPrediction(BaseModel):
    """Schema for survival prediction response"""
    survived: bool = Field(..., description="Predicted survival (True=Survived, False=Did not survive)")
    survival_probability: float = Field(..., ge=0, le=1, description="Probability of survival")
    confidence: str = Field(..., description="Confidence level (High/Medium/Low)")

class HealthCheck(BaseModel):
    """Schema for health check response"""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether the model is loaded")
    timestamp: str = Field(..., description="Current timestamp")

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information") 