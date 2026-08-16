from typing import Literal, TypedDict

PLANETS = Literal[
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

RASHIS = Literal[
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

LAGNA = Literal["Lagna"]

PLANETS_LAGNA = PLANETS | LAGNA

HOUSES = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

RASHI_LORDS = Literal["Sun", "Moon", "Mars",
                      "Mercury", "Jupiter", "Venus", "Saturn"]

NAKSHATRAS = Literal[
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

PADA = Literal[1, 2, 3, 4]

ALLOWED_DIVISIONS = Literal[1, 2, 3, 4, 7, 9,
                            10, 12, 16, 20, 24, 27, 30, 40, 45, 60]

PLANET_SIGN_RELATION = Literal[
    "Exalted",
    "Moola Trikona",
    "Own",
    "Friend",
    "Neutral",
    "Enemy",
    "Debilitated",
]


class NakshatraType(TypedDict):
    name: NAKSHATRAS
    lord: PLANETS
    pada: PADA


class PlanetOrLagnaSignType(TypedDict):
    name: RASHIS
    lord: RASHI_LORDS
    nakshatra: NakshatraType


class PlanetType(TypedDict):
    name: PLANETS
    longitude: float
    is_retrograde: bool
    inSign: list[PLANET_SIGN_RELATION]
    sign: PlanetOrLagnaSignType


class LagnaType(TypedDict):
    name: LAGNA
    longitude: float
    is_retrograde: Literal[False]
    sign: PlanetOrLagnaSignType


PlanetsType = list[PlanetType]


class HouseType(TypedDict):
    sign: RASHIS
    planets: PlanetsType
    lagna: LagnaType | None


ChartType = dict[HOUSES, HouseType]


class AntarDashaType(TypedDict):
    mahadasha: PLANETS
    antardasha: PLANETS
    start: str
    end: str


class MahaDashaType(TypedDict):
    mahadasha: PLANETS
    start: str
    end: str
    antardashas: list[AntarDashaType]


DashasType = list[MahaDashaType]


class CurrentDashaType(TypedDict):
    mahadasha: MahaDashaType | None
    antardasha: AntarDashaType | None


class AspectType(TypedDict):
    planet: PLANETS
    from_house: HOUSES
    aspect_houses: list[dict[HOUSES, list[PLANETS]]]


class YogaType(TypedDict):
    id: str
    name: str
    present: bool
    strength: float
    details: str
    type: Literal["Positive", "Neutral", "Negative"]


class DeepExaltationInfo(TypedDict):
    sign: RASHIS
    degree: int


DeepExaltationPointsType = dict[RASHI_LORDS, DeepExaltationInfo]
