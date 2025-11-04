from typing import List


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

NODE_MAP = {"North Node": "Rahu", "South Node": "Ketu"}

MOVABLE = [0, 3, 6, 9]  # Ar, Cn, Li, Cp
FIXED = [1, 4, 7, 10]  # Ta, Le, Sc, Aq
DUAL = [2, 5, 8, 11]  # Ge, Vi, Sg, Pi


def isSignOdd(n: int) -> bool:
    """Return True if the rashi index is odd-numbered per this module's scheme.

    Note: In this context, a return value of True corresponds to signs the
    code treats as "odd" for certain divisional rules.
    """
    return n % 2 == 0
