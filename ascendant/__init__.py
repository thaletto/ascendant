from typing import List

from ascendant.types import HouseNumber


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

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

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


def isSignOdd(n: HouseNumber) -> bool:
    """Return True if the rashi index is odd-numbered per this module's scheme."""
    return n % 2 == 0
