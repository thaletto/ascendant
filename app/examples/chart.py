from datetime import datetime
from typing import Tuple
from vedicastro.VedicAstro import VedicHoroscopeData

from app.utils.chart import ChartGenerator

# Major cities in specified states with lat/lng
CITY_COORDINATES = {
    # Tamil Nadu
    "Chennai": (13.0827, 80.2707, "+5:30"),
    "Coimbatore": (11.0168, 76.9558, "+5:30"),
    "Madurai": (9.9252, 78.1198, "+5:30"),
    "Tiruchirappalli": (10.7905, 78.7047, "+5:30"),
    "Salem": (11.6643, 78.1460, "+5:30"),
    "Erode": (11.3263, 77.7060, "+5:30"),

    # Kerala
    "Thiruvananthapuram": (8.5241, 76.9366, "+5:30"),
    "Kochi": (9.9312, 76.2673, "+5:30"),
    "Kozhikode": (11.2588, 75.7804, "+5:30"),
    "Thrissur": (10.5276, 76.2144, "+5:30"),
    "Alappuzha": (9.4981, 76.3388, "+5:30"),

    # Andhra Pradesh
    "Visakhapatnam": (17.6868, 83.2185, "+5:30"),
    "Vijayawada": (16.5062, 80.6480, "+5:30"),
    "Guntur": (16.3067, 80.4365, "+5:30"),
    "Tirupati": (13.6288, 79.4192, "+5:30"),
    "Kurnool": (15.8281, 78.0373, "+5:30"),

    # Karnataka
    "Bengaluru": (12.9716, 77.5946, "+5:30"),
    "Mysuru": (12.2958, 76.6394, "+5:30"),
    "Mangalore": (12.9141, 74.8560, "+5:30"),
    "Hubli": (15.3647, 75.1236, "+5:30"),
    "Belgaum": (15.8497, 74.4977, "+5:30"),

    # Telangana
    "Hyderabad": (17.3850, 78.4867, "+5:30"),
    "Warangal": (17.9787, 79.5941, "+5:30"),
    "Nizamabad": (18.6720, 78.0940, "+5:30"),
    "Karimnagar": (18.4386, 79.1288, "+5:30"),
    "Khammam": (17.2473, 80.1434, "+5:30"),

    # Maharashtra
    "Mumbai": (19.0760, 72.8777, "+5:30"),
    "Pune": (18.5204, 73.8567, "+5:30"),
    "Nagpur": (21.1458, 79.0882, "+5:30"),
    "Nashik": (19.9975, 73.7898, "+5:30"),
    "Aurangabad": (19.8762, 75.3433, "+5:30"),

    # Delhi
    "Delhi": (28.6139, 77.2090, "+5:30"),
    "New Delhi": (28.6139, 77., "+5:30"),

    # West Bengal
    "Kolkata": (22.5726, 88.3639, "+5:30"),
    "Durgapur": (23.5204, 87.3119, "+5:30"),
    "Siliguri": (26.7271, 88.3953, "+5:30"),
    "Howrah": (22.5958, 88.2636, "+5:30"),
    "Asansol": (23.6850, 86.9514, "+5:30"),
}

def get_lat_lng_utc(city: str) -> Tuple[float, float, str]:
    """
    Returns latitude and longitude for the given city.
    Raises ValueError if city not found.
    """
    if city in CITY_COORDINATES:
        return CITY_COORDINATES[city]
    else:
        raise ValueError(f"Coordinates for city '{city}' not found. Please add it to CITY_COORDINATES.")

birth_date = datetime.strptime("2003-08-19 11:55", "%Y-%m-%d %H:%M")
city = "Chennai"
lat, lng, utc = get_lat_lng_utc(city)
ayanamsa = "Lahiri"
house_system = "Whole Sign"

if __name__ == "__main__":
    horoscope = VedicHoroscopeData(
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
        house_system=house_system
    )
    chart = ChartGenerator(horoscope)

    print("=== D1 Chart ===")
    print(chart.get_d1())

    print("\n=== D9 Chart ===")
    print(chart.get_d9())

    print("\n=== D10 Chart ===")
    print(chart.get_d10())