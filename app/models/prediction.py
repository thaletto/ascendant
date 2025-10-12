"""
Pydantic models for Prediction API endpoints
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Request model for astrology predictions."""

    session_id: str = Field(..., min_length=1, description="Unique session identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    birth_data: Optional[Dict[str, Any]] = Field(
        None, description="Birth data dictionary"
    )
    query: str = Field(
        ..., min_length=1, max_length=2000, description="Astrology question or query"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "user_id": "user_456",
                "query": "What does my birth chart say about my career prospects?",
                "birth_data": {
                    "name": "John Doe",
                    "birth_year": 2003,
                    "birth_month": 8,
                    "birth_day": 19,
                    "birth_hour": 11,
                    "birth_minute": 55,
                    "birth_second": 0,
                    "latitude": 13.0843,
                    "longitude": 80.2705,
                    "utc": "+05:30",
                },
            }
        }


class PredictionResponse(BaseModel):
    """Response model for astrology predictions."""

    session_id: str = Field(..., description="Session identifier")
    response: str = Field(..., description="Astrology prediction response")
    agent_used: str = Field(
        ..., description="Name of the agent that processed the request"
    )
    status: str = Field(default="success", description="Response status")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "response": "Based on your birth chart analysis...",
                "agent_used": "AscendantRootAgent",
                "status": "success",
                "metadata": {
                    "processing_time": 2.5,
                    "charts_analyzed": ["D1", "D9", "D10"],
                },
            }
        }


class SessionInfo(BaseModel):
    """Model for session information."""

    session_id: str = Field(..., description="Session identifier")
    has_birth_data: bool = Field(..., description="Whether birth data is available")
    message_count: int = Field(..., ge=0, description="Number of messages in session")
    last_updated: str = Field(..., description="Last update timestamp")
    birth_data_summary: Optional[Dict[str, Any]] = Field(
        default=None, description="Summary of stored birth data"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "has_birth_data": True,
                "message_count": 5,
                "last_updated": "2024-01-15T10:30:00Z",
                "birth_data_summary": {"name": "John Doe", "birth_date": "1990-05-15"},
            }
        }


class SessionCreate(BaseModel):
    """Model for creating a new session."""

    session_id: str = Field(..., min_length=1, description="Unique session identifier")
    user_id: Optional[str] = Field(None, description="Associated user ID")

    class Config:
        json_schema_extra = {
            "example": {"session_id": "session_123", "user_id": "user_456"}
        }


class SessionClearResponse(BaseModel):
    """Model for session clear response."""

    message: str = Field(..., description="Confirmation message")
    session_id: str = Field(..., description="Cleared session identifier")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Session session_123 cleared successfully",
                "session_id": "session_123",
            }
        }


class PredictionCategory(BaseModel):
    """Model for prediction category requests."""

    category: str = Field(..., description="Prediction category")
    query: str = Field(
        ..., min_length=1, max_length=2000, description="Category-specific query"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "category": "health",
                "query": "What does my chart say about my health?",
            }
        }
