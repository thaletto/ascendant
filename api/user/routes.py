import logging
from typing import cast

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from vedicastro.VedicAstro import VedicHoroscopeData

from api.database import get_db
from api.models import BirthDetails, UserCreationOut
from api.schemas import Chart, Dasha, User
from ascendant.chart import Chart as AscendantChart
from ascendant.const import ALLOWED_DIVISIONS as DIVISIONS
from ascendant.dasha import Dasha as AscendantDasha
from ascendant.types import ALLOWED_DIVISIONS
from ascendant.utils import getHouseSystem

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post("/", response_model=UserCreationOut, status_code=status.HTTP_201_CREATED)
async def create_user_and_astrological_data(
    data: BirthDetails, db: Session = Depends(get_db)
):
    """
    Creates a new user and generates all associated astrological data,
    including all divisional charts and the dasha timeline.
    """
    logger.info(f"Received request to create user and data for: {data.model_dump()}")

    # 1. Create a new user record
    db_user = User(**data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"Created new user with ID: {db_user.id}")

    # 2. Generate horoscope object from birth data
    horoscope = VedicHoroscopeData(
        year=data.year,
        month=data.month,
        day=data.day,
        hour=data.hour,
        minute=data.minute,
        second=data.second,
        utc=data.utc,
        latitude=data.latitude,
        longitude=data.longitude,
        ayanamsa=data.ayanamsa,
        house_system=getHouseSystem(data.house_system),
    )

    # 3. Calculate and store all divisional charts
    ascendant_chart = AscendantChart(horoscope)
    charts_to_create = []
    for division in DIVISIONS:
        div = cast(ALLOWED_DIVISIONS, division)
        chart_data = ascendant_chart.get_varga_chakra_chart(div)
        if chart_data:
            db_chart = Chart(user_id=db_user.id, division=div, chart_data=chart_data)
            charts_to_create.append(db_chart)
    db.add_all(charts_to_create)
    logger.info(f"Generated {len(charts_to_create)} charts for user {db_user.id}")

    # 4. Calculate and store dasha timeline
    ascendant_dasha = AscendantDasha(horoscope)
    dasha_data = ascendant_dasha.get_dasha_timeline()
    if dasha_data:
        db_dasha = Dasha(user_id=db_user.id, dasha_data=dasha_data)
        db.add(db_dasha)
        logger.info(f"Generated dasha for user {db_user.id}")

    db.commit()

    # 5. Refresh user object to load relationships and return
    db.refresh(db_user)
    return db_user
