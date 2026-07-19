from typing import Final

from ascendant.types import NAKSHATRAS as NAKSHATRAS_TYPE
from ascendant.types import PLANETS, RASHI_LORDS, DeepExaltationPointsType
from ascendant.types import RASHIS as RASHIS_TYPE

__all__ = ["RASHIS", "NAKSHATRAS"]

RASHIS: Final[list[RASHIS_TYPE]] = [
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

NAKSHATRAS: Final[list[NAKSHATRAS_TYPE]] = [
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

VIMSHOTTARI_PLANETS: Final[list[PLANETS]] = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",
]

VIMSHOTTARI_YEARS: Final[list[int]] = [7, 20, 6, 10, 7, 18, 16, 19, 17]


SELECTED_PLANETS: list[str] = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "North Node",
    "South Node",
]

CLASSICAL_PLANETS: Final[tuple[PLANETS, ...]] = (
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
)

PLANETS_LIST: list[PLANETS] = [
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

NODE_MAP: dict[str, PLANETS] = {"North Node": "Rahu", "South Node": "Ketu"}

BENEFIC_PLANETS: Final[tuple[PLANETS, ...]] = ("Mercury", "Jupiter", "Venus")

MALEFIC_PLANETS: Final[tuple[PLANETS, ...]] = (
    "Mars", "Saturn", "Rahu", "Ketu")

ALLOWED_DIVISIONS: list[int] = [
    1,
    2,
    3,
    4,
    7,
    9,
    10,
    12,
    16,
    20,
    24,
    27,
    30,
    40,
    45,
    60,
]

MOVABLE = [0, 3, 6, 9]  # Ar, Cn, Li, Cp
FIXED = [1, 4, 7, 10]  # Ta, Le, Sc, Aq
DUAL = [2, 5, 8, 11]  # Ge, Vi, Sg, Pi

RASHI_LORD_MAP: dict[RASHIS_TYPE, RASHI_LORDS] = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}

SIGN_LORDS: Final[list[RASHI_LORDS]] = list(RASHI_LORD_MAP.values())

HOUSES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

DEEP_EXALTATION_POINTS: DeepExaltationPointsType = {
    "Sun": {"sign": "Aries", "degree": 10},
    "Moon": {"sign": "Taurus", "degree": 3},
    "Mars": {"sign": "Capricorn", "degree": 28},
    "Mercury": {"sign": "Virgo", "degree": 15},
    "Jupiter": {"sign": "Cancer", "degree": 5},
    "Venus": {"sign": "Pisces", "degree": 27},
    "Saturn": {"sign": "Libra", "degree": 20},
}

MOVABLE_SIGNS = ["Aries", "Cancer", "Libra", "Capricorn"]

FIXED_SIGNS = ["Taurus", "Leo", "Scorpio", "Aquarius"]

BENEFIC_SIGNS = [
    "Taurus",
    "Gemini",
    "Cancer",
    "Virgo",
    "Libra",
    "Sagittarius",
    "Pisces",
]
