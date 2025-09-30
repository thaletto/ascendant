"""
Pydantic models for Users
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class NewUser(BaseModel):
    """Model for creating a new user"""
    name: str = Field(..., min_length=3, max_length=100, description="User's full name")
    birth_date: datetime = Field(..., description="User's birth date")
    birth_time: str = Field(None, pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$", description="Birth time in HH:MM format")
    birth_place: str = Field(None, max_length=200, description="Birth place/city")

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