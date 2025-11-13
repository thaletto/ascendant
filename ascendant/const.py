from typing import List
from vedicastro.VedicAstro import RASHIS, NAKSHATRAS

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

HOUSES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
