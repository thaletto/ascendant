import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import ChartOut
from api.schemas import Chart
from ascendant.const import ALLOWED_DIVISIONS

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/chart", tags=["Chart"])


@router.get("/{user_id}", response_model=list[ChartOut])
async def get_all_charts_for_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received request to get all charts for user_id: {user_id}")

    charts = db.query(Chart).filter(Chart.user_id == user_id).all()

    if not charts:
        logger.warning(f"No charts found for user_id: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No charts found for user with ID: {user_id}",
        )

    logger.info(f"Successfully retrieved {len(charts)} charts for user_id: {user_id}")
    return charts


@router.get("/{user_id}/{division}", response_model=ChartOut)
async def get_single_chart(user_id: int, division: int, db: Session = Depends(get_db)):
    logger.info(
        f"Received request to get chart for user_id: {user_id}, division: {division}"
    )

    # Validate division
    if division not in ALLOWED_DIVISIONS:
        logger.warning(f"Invalid division requested: {division}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid division. Allowed divisions are: {ALLOWED_DIVISIONS}",
        )

    chart = (
        db.query(Chart)
        .filter(Chart.user_id == user_id, Chart.division == division)
        .first()
    )

    if chart is None:
        logger.warning(
            f"Chart not found for user_id: {user_id}, division: {division}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chart not found"
        )

    logger.info(
        f"Successfully retrieved chart for user_id: {user_id}, division: {division}"
    )
    return chart