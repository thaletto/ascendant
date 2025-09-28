"""
Horoscope prediction routes for Horoscope AI Backend.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime, timedelta

from db import get_db, User, Prediction
from models import PredictionRequest, PredictionResponse
from horoscope import generate_horoscope

router = APIRouter(prefix="/predict", tags=["predictions"])

@router.post("/", response_model=PredictionResponse, status_code=201)
async def create_prediction(
    prediction_data: PredictionRequest, 
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a horoscope prediction for a user.
    
    Args:
        prediction_data: Prediction request data
        db: Database session
    
    Returns:
        Generated horoscope prediction
    """
    try:
        # Get user information
        result = await db.execute(select(User).where(User.id == prediction_data.user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Use provided date or default to today
        prediction_date = prediction_data.date or datetime.now()
        
        # Prepare user info for horoscope generation
        user_info = {
            "name": user.name,
            "birth_date": user.birth_date.strftime("%Y-%m-%d"),
            "birth_time": user.birth_time,
            "birth_place": user.birth_place
        }
        
        # Generate horoscope
        horoscope_content = await generate_horoscope(
            user_info=user_info,
            prediction_type=prediction_data.prediction_type,
            date=prediction_date
        )
        
        # Save prediction to database
        db_prediction = Prediction(
            user_id=prediction_data.user_id,
            prediction_type=prediction_data.prediction_type,
            content=horoscope_content,
            date=prediction_date
        )
        
        db.add(db_prediction)
        await db.commit()
        await db.refresh(db_prediction)
        
        return PredictionResponse.model_validate(db_prediction)
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating prediction: {str(e)}")

@router.get("/user/{user_id}", response_model=List[PredictionResponse])
async def get_user_predictions(
    user_id: int, 
    prediction_type: str = None,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    Get predictions for a specific user.
    
    Args:
        user_id: ID of the user
        prediction_type: Filter by prediction type (optional)
        limit: Maximum number of predictions to return
        db: Database session
    
    Returns:
        List of user's predictions
    """
    # Check if user exists
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Build query
    query = select(Prediction).where(Prediction.user_id == user_id)
    
    if prediction_type:
        query = query.where(Prediction.prediction_type == prediction_type)
    
    query = query.order_by(Prediction.created_at.desc()).limit(limit)
    
    result = await db.execute(query)
    predictions = result.scalars().all()
    
    return [PredictionResponse.model_validate(prediction) for prediction in predictions]

@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(prediction_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific prediction by ID.
    
    Args:
        prediction_id: ID of the prediction
        db: Database session
    
    Returns:
        Prediction information
    """
    result = await db.execute(select(Prediction).where(Prediction.id == prediction_id))
    prediction = result.scalar_one_or_none()
    
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    return PredictionResponse.model_validate(prediction)

@router.delete("/{prediction_id}", status_code=204)
async def delete_prediction(prediction_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a prediction by ID.
    
    Args:
        prediction_id: ID of the prediction to delete
        db: Database session
    """
    result = await db.execute(select(Prediction).where(Prediction.id == prediction_id))
    prediction = result.scalar_one_or_none()
    
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    await db.delete(prediction)
    await db.commit()
    
    return None
