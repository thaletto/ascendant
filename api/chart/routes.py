import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Chart, User
from api.schemas import BirthDetails, ChartOut, UserOut
from ascendant.types import ALLOWED_DIVISIONS
from utils import get_ascendant

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/chart", tags=["Chart"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_charts(data: BirthDetails, db: Session = Depends(get_db)):
    logger.info(f"Received request to create charts for birth details: {data}")

    # Create new user
    db_user = User(**data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"Created new user with ID: {db_user.id}")

    ascendant = get_ascendant(data)
    
    charts_to_create = []
    for division_enum_value in ALLOWED_DIVISIONS.__args__:
        chart_data = ascendant.get_chart(division_enum_value)
        db_chart = Chart(
            user_id=db_user.id,
            division=division_enum_value,
            chart_data=chart_data
        )
        charts_to_create.append(db_chart)
        logger.debug(f"Generated chart for division {division_enum_value} for user {db_user.id}")

    db.add_all(charts_to_create)
    db.commit()
    for chart in charts_to_create:
        db.refresh(chart)
    logger.info(f"Created {len(charts_to_create)} charts for user {db_user.id}")

    # Refresh user to load charts relationship
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=list[ChartOut])
async def get_all_charts_for_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received request to get all charts for user_id: {user_id}")

    charts = db.query(Chart).filter(Chart.user_id == user_id).all()

    if not charts:
        logger.warning(f"No charts found for user_id: {user_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No charts found for user with ID: {user_id}")
    
    logger.info(f"Successfully retrieved {len(charts)} charts for user_id: {user_id}")
    return charts

@router.get("/{user_id}/{division}", response_model=ChartOut)
async def get_single_chart(user_id: int, division: int, db: Session = Depends(get_db)):
    logger.info(f"Received request to get chart for user_id: {user_id}, division: {division}")

    # Validate division
    if division not in ALLOWED_DIVISIONS.__args__:
        logger.warning(f"Invalid division requested: {division}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid division. Allowed divisions are: {list(ALLOWED_DIVISIONS.__args__)}"
        )

    chart = db.query(Chart).filter(
        Chart.user_id == user_id,
        Chart.division == division
    ).first()

    if chart is None:
        logger.warning(f"Chart not found for user_id: {user_id}, division: {division}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chart not found")
    
    logger.info(f"Successfully retrieved chart for user_id: {user_id}, division: {division}")
    return chart