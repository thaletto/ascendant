from typing import Dict, Literal, TypedDict, Union

PlanetName = Literal[
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Rahu",
    "Ketu",
]

RashiName = Literal[
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

LagnaName = Literal["Lagna"]

HouseNumber = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

LordName = Literal["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

NakshatraName = Literal[
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashīrsha",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Āshleshā",
    "Maghā",
    "PūrvaPhalgunī",
    "UttaraPhalgunī",
    "Hasta",
    "Chitra",
    "Svati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "PurvaAshadha",
    "UttaraAshadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "PurvaBhādrapadā",
    "UttaraBhādrapadā",
    "Revati",
]

PadaNumber = Literal[1, 2, 3, 4]

AllowedDivision = Literal[1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60]


class PlanetData(TypedDict):
    name: PlanetName
    longitude: float
    is_retrograde: bool


class PlanetPlacement(TypedDict):
    longitude: float
    degree: float
    retrograde: bool
    rashi_lord: LordName
    nakshatra: NakshatraName
    nakshatra_lord: PlanetName
    pada: PadaNumber


class LagnaPlacement(TypedDict):
    longitude: float
    retrograde: Literal[False]
    rashi_lord: LordName
    nakshatra: NakshatraName
    nakshatra_lord: PlanetName
    pada: PadaNumber


class HouseData(TypedDict):
    sign: RashiName
    planets: Dict[Union[PlanetName, LagnaName], Union[PlanetPlacement, LagnaPlacement]]


ChartData = Dict[str, HouseData]

class Yoga(TypedDict):
    name: str
    present: bool
    details: str