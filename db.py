"""
Database configuration and models for Horoscope AI Backend.
"""
import asyncio
from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    """User model for storing birth information."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    birth_time = Column(String(10), nullable=True)  # Format: "HH:MM"
    birth_place = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationship to predictions
    predictions = relationship("Prediction", back_populates="user")

class Prediction(Base):
    """Prediction model for storing horoscope predictions."""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prediction_type = Column(String(20), nullable=False)  # daily, weekly, monthly
    content = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationship to user
    user = relationship("User", back_populates="predictions")

class ChatMessage(Base):
    """Chat message model for storing conversation history."""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    is_user_message = Column(String(10), nullable=False)  # "user" or "assistant"
    created_at = Column(DateTime, default=func.now())
    
    # Relationship to user
    user = relationship("User")

# Database configuration
DATABASE_URL = "sqlite+aiosqlite:///./horoscope_ai.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """Dependency to get database session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
