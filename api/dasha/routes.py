import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import DashaResponse
from api.schemas import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/dasha", tags=["Dasha"])


@router.get("/{user_id}", response_model=DashaResponse)
async def get_dasha_for_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the stored dasha timeline for a specific user and determines
    the current running mahadasha from it.
    """
    logger.info(f"Received request to get dasha for user_id: {user_id}")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUnd, detail="User not found"
        )

    dasha = user.dasha
    user_utc = user.utc

    if not dasha or not dasha.dasha_data:
        logger.warning(f"No dasha found for user_id: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No dasha data found for user with ID: {user_id}",
        )

    timeline = dasha.dasha_data
    current_mahadasha = None
    
    tz = ZoneInfo(user_utc) if user_utc else ZoneInfo("UTC")
    now = datetime.now(tz)

    for mahadasha in timeline:
        try:
            start_date = datetime.strptime(mahadasha["start"], "%d-%m-%Y")
            end_date = datetime.strptime(mahadasha["end"], "%d-%m-%Y")
            if start_date <= now <= end_date:
                current_mahadasha = mahadasha
                break  # Found it
        except (ValueError, KeyError):
            # Log error if date format is wrong or keys are missing
            logger.error(f"Could not parse dates for mahadasha for user {user_id}")
            continue

    logger.info(f"Successfully retrieved dasha for user_id: {user_id}")
    return {"current": current_mahadasha}
