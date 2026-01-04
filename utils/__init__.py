from api.schemas import BirthDetails
from ascendant import Ascendant


def get_ascendant(data: BirthDetails) -> Ascendant:
    return Ascendant(
        year=data.year,
        month=data.month,
        day=data.day,
        hour=data.hour,
        minute=data.minute,
        second=data.second,
        latitude=data.latitude,
        longitude=data.longitude,
        utc=data.utc,
        ayanamsa=data.ayanamsa,
        house_system=data.house_system,
    )
