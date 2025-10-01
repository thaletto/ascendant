"""
Pydantic models for Users
"""
from datetime import date, time
from typing import Optional
from pydantic import BaseModel, Field

class NewUser(BaseModel):
    """Model for creating a new user"""
    name: str = Field(..., min_length=3, max_length=100, description="User's full name")
    birth_date: date = Field(..., description="User's birth date")
    birth_time: Optional[time] = Field(None, description="Birth time (HH:MM)")
    birth_place: Optional[str] = Field(None, max_length=200, description="Birth place/city")

class UserUpdate(BaseModel):
    """Model for updating an existing user"""
    name: Optional[str] = None
    birth_date: Optional[date] = None
    birth_time: Optional[time] = None
    birth_place: Optional[str] = None



class UserResponse(BaseModel):
    """Model for user response."""
    id: int
    name: str
    birth_date: date
    birth_time: Optional[str]
    birth_place: Optional[str]
    created_at: date
    
    class Config:
        from_attributes = True