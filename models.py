"""
Pydantic models for API request/response validation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    """Model for creating a new user."""
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    birth_date: datetime = Field(..., description="User's birth date")
    birth_time: Optional[str] = Field(None, pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$", description="Birth time in HH:MM format")
    birth_place: Optional[str] = Field(None, max_length=200, description="Birth place/city")

class UserResponse(BaseModel):
    """Model for user response."""
    id: int
    name: str
    birth_date: datetime
    birth_time: Optional[str]
    birth_place: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class PredictionRequest(BaseModel):
    """Model for horoscope prediction request."""
    user_id: int = Field(..., description="ID of the user")
    prediction_type: str = Field(..., pattern="^(daily|weekly|monthly)$", description="Type of prediction: daily, weekly, or monthly")
    date: Optional[datetime] = Field(None, description="Specific date for prediction (defaults to today)")

class PredictionResponse(BaseModel):
    """Model for horoscope prediction response."""
    id: int
    user_id: int
    prediction_type: str
    content: str
    date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    """Model for chat message request."""
    user_id: int = Field(..., description="ID of the user")
    message: str = Field(..., min_length=1, description="User's message")

class ChatResponse(BaseModel):
    """Model for chat message response."""
    id: int
    user_id: int
    message: str
    response: str
    is_user_message: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class StatusResponse(BaseModel):
    """Model for status endpoint response."""
    status: str
