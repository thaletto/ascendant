import os
from datetime import datetime
from vedicastro.VedicAstro import VedicHoroscopeData

from ascendant.utils import getHouseSystem

# Default test values
DEFAULT_BIRTH_DATE = "1990-01-01"
DEFAULT_BIRTH_TIME = "12:00"
DEFAULT_LATITUDE = "28.6139"  # New Delhi
DEFAULT_LONGITUDE = "77.2090"
DEFAULT_UTC = "+5:30"

birth_date_str = os.getenv("NATIVE_BIRTH_DATE", DEFAULT_BIRTH_DATE)
birth_time_str = os.getenv("NATIVE_BIRTH_TIME", DEFAULT_BIRTH_TIME)

birth_date = datetime.strptime(f"{birth_date_str} {birth_time_str}", "%Y-%m-%d %H:%M")

lat = float(os.getenv("NATIVE_LATITUDE", DEFAULT_LATITUDE))
lng = float(os.getenv("NATIVE_LONGITUDE", DEFAULT_LONGITUDE))

utc = os.getenv("NATIVE_UTC", DEFAULT_UTC)

ayanamsa = os.getenv("AYANAMSA", default="Lahiri")
house_system = os.getenv("HOUSE_SYSTEM", default="whole_sign")

house_system_mapped = getHouseSystem(house_system)


my_horoscope = VedicHoroscopeData(
    year=birth_date.year,
    month=birth_date.month,
    day=birth_date.day,
    hour=birth_date.hour,
    minute=birth_date.minute,
    second=birth_date.second,
    utc=utc,
    latitude=lat,
    longitude=lng,
    ayanamsa=ayanamsa,
    house_system=house_system_mapped,
)
