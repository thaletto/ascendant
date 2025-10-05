"""
User management API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.client import get_db
from app.db.schema import User
from app.models.users import NewUser, UserResponse, UserUpdate

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user_data: NewUser, db: AsyncSession = Depends(get_db)):
    f"""
    Create a new user with birth information.
    
    Args:
        user_data: {NewUser}
        db: Database session
    
    Returns:
        {UserResponse}
    """
    try:
        # Create new user
        db_user = User(
            name=user_data.name,
            birth_date=user_data.birth_date,
            birth_time=user_data.birth_time,
            birth_place=user_data.birth_place
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return UserResponse.model_validate(db_user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update an existing user's details.

    Args:
        user_id: ID of the user to update
        user_data: Updated user info
        db: Database session

    Returns:
        Updated user as UserResponse
    """
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalar_one_or_none()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update fields if provided
        if user_data.name is not None:
            db_user.name = user_data.name
        if user_data.birth_date is not None:
            db_user.birth_date = user_data.birth_date
        if user_data.birth_time is not None:
            db_user.birth_time = user_data.birth_time
        if user_data.birth_place is not None:
            db_user.birth_place = user_data.birth_place

        await db.commit()
        await db.refresh(db_user)

        return UserResponse.model_validate(db_user)

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(e)}")

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get user information by ID.
    
    Args:
        user_id: ID of the user to retrieve
        db: Database session
    
    Returns:
        User information
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse.model_validate(user)

@router.get("/", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    List all users with pagination.
    
    Args:
        skip: Number of users to skip
        limit: Maximum number of users to return
        db: Database session
    
    Returns:
        List of users
    """
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    
    return [UserResponse.model_validate(user) for user in users]

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a user by ID.
    
    Args:
        user_id: ID of the user to delete
        db: Database session
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(user)
    await db.commit()
    
    return None