from typing import TYPE_CHECKING, List
from vedicastro.VedicAstro import NAKSHATRAS, RASHIS

if TYPE_CHECKING:
    from ascendant.types import DeepExaltationPointsType


__all__ = [RASHIS, NAKSHATRAS]


SELECTED_PLANETS: List[str] = [
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

NODE_MAP = {"North Node": "Rahu", "South Node": "Ketu"}

BENEFIC_PLANETS: List[str] = ["Mercury", "Jupiter", "Venus"]

MALEFIC_PLANETS: List[str] = ["Mars", "Saturn", "Rahu", "Ketu"]

ALLOWED_DIVISIONS: List[int] = [
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

RASHI_LORD_MAP = {
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

