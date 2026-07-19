"""Classical Parashari Ashtakavarga constants."""

from __future__ import annotations

from typing import Final

from ascendant.sav.types import ASHTAKAVARGA_ENTITIES, ASHTAKAVARGA_PLANETS
from ascendant.types import RASHIS

ASHTAKAVARGA_PLANET_ORDER: Final[tuple[ASHTAKAVARGA_PLANETS, ...]] = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"
)
ASHTAKAVARGA_ENTITY_ORDER: Final[tuple[ASHTAKAVARGA_ENTITIES, ...]] = (
    *ASHTAKAVARGA_PLANET_ORDER, "Lagna"
)
RASHIS_ORDER: Final[tuple[RASHIS, ...]] = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)

# Each assessed entity lists the 1-based signs from every contributor that
# receive a benefic bindu. These are the standard Parashari tables.
CONTRIBUTION_OFFSETS: Final[
    dict[ASHTAKAVARGA_ENTITIES, dict[ASHTAKAVARGA_ENTITIES, frozenset[int]]]
] = {
    "Sun": {
        "Sun": frozenset({1, 2, 4, 7, 8, 9, 10, 11}),
        "Moon": frozenset({3, 6, 10, 11}),
        "Mars": frozenset({1, 2, 4, 7, 8, 9, 10, 11}),
        "Mercury": frozenset({3, 5, 6, 9, 10, 11, 12}),
        "Jupiter": frozenset({5, 6, 9, 11}),
        "Venus": frozenset({6, 7, 12}),
        "Saturn": frozenset({1, 2, 4, 7, 8, 9, 10, 11}),
        "Lagna": frozenset({3, 4, 6, 10, 11, 12}),
    },
    "Moon": {
        "Sun": frozenset({3, 6, 7, 8, 10, 11}),
        "Moon": frozenset({1, 3, 6, 7, 9, 10, 11}),
        "Mars": frozenset({2, 3, 5, 6, 10, 11}),
        "Mercury": frozenset({1, 3, 4, 5, 7, 8, 10, 11}),
        "Jupiter": frozenset({1, 2, 4, 7, 8, 10, 11}),
        "Venus": frozenset({3, 4, 5, 7, 9, 10, 11}),
        "Saturn": frozenset({3, 5, 6, 11}),
        "Lagna": frozenset({3, 6, 10, 11}),
    },
    "Mars": {
        "Sun": frozenset({3, 5, 6, 10, 11}),
        "Moon": frozenset({3, 6, 11}),
        "Mars": frozenset({1, 2, 4, 7, 8, 10, 11}),
        "Mercury": frozenset({3, 5, 6, 11}),
        "Jupiter": frozenset({6, 10, 11, 12}),
        "Venus": frozenset({6, 8, 11, 12}),
        "Saturn": frozenset({1, 4, 7, 8, 9, 10, 11}),
        "Lagna": frozenset({1, 3, 6, 10, 11}),
    },
    "Mercury": {
        "Sun": frozenset({5, 6, 9, 11, 12}),
        "Moon": frozenset({2, 4, 6, 8, 10, 11}),
        "Mars": frozenset({1, 2, 4, 7, 8, 9, 10, 11}),
        "Mercury": frozenset({1, 3, 5, 6, 9, 10, 11, 12}),
        "Jupiter": frozenset({6, 8, 11, 12}),
        "Venus": frozenset({1, 2, 3, 4, 5, 8, 9, 11}),
        "Saturn": frozenset({1, 2, 4, 7, 8, 9, 10, 11}),
        "Lagna": frozenset({1, 2, 4, 6, 8, 10, 11}),
    },
    "Jupiter": {
        "Sun": frozenset({1, 2, 3, 4, 7, 8, 9, 10, 11}),
        "Moon": frozenset({2, 5, 7, 9, 11}),
        "Mars": frozenset({1, 2, 4, 7, 8, 10, 11}),
        "Mercury": frozenset({1, 2, 4, 5, 6, 9, 10, 11}),
        "Jupiter": frozenset({1, 2, 3, 4, 7, 8, 10, 11}),
        "Venus": frozenset({2, 5, 6, 9, 10, 11}),
        "Saturn": frozenset({3, 5, 6, 12}),
        "Lagna": frozenset({1, 2, 4, 5, 6, 7, 9, 10, 11}),
    },
    "Venus": {
        "Sun": frozenset({8, 11, 12}),
        "Moon": frozenset({1, 2, 3, 4, 5, 8, 9, 11, 12}),
        "Mars": frozenset({3, 4, 6, 9, 11, 12}),
        "Mercury": frozenset({3, 5, 6, 9, 11}),
        "Jupiter": frozenset({5, 8, 9, 10, 11}),
        "Venus": frozenset({1, 2, 3, 4, 5, 8, 9, 10, 11}),
        "Saturn": frozenset({3, 4, 5, 8, 9, 10, 11}),
        "Lagna": frozenset({1, 2, 3, 4, 5, 8, 9, 11}),
    },
    "Saturn": {
        "Sun": frozenset({1, 2, 4, 7, 8, 10, 11}),
        "Moon": frozenset({3, 6, 11}),
        "Mars": frozenset({3, 5, 6, 10, 11, 12}),
        "Mercury": frozenset({6, 8, 9, 10, 11, 12}),
        "Jupiter": frozenset({5, 6, 11, 12}),
        "Venus": frozenset({6, 11, 12}),
        "Saturn": frozenset({3, 5, 6, 11}),
        "Lagna": frozenset({1, 3, 4, 6, 10, 11}),
    },
    "Lagna": {
        "Sun": frozenset({3, 4, 6, 10, 11, 12}),
        "Moon": frozenset({3, 6, 10, 11, 12}),
        "Mars": frozenset({1, 3, 6, 10, 11}),
        "Mercury": frozenset({1, 2, 4, 6, 8, 10, 11}),
        "Jupiter": frozenset({1, 2, 4, 5, 6, 7, 9, 10, 11}),
        "Venus": frozenset({1, 2, 3, 4, 5, 8, 9}),
        "Saturn": frozenset({1, 3, 4, 6, 10, 11}),
        "Lagna": frozenset({3, 6, 10, 11}),
    },
}

EXPECTED_BAV_TOTALS: Final[dict[ASHTAKAVARGA_ENTITIES, int]] = {
    "Sun": 48, "Moon": 49, "Mars": 39, "Mercury": 54,
    "Jupiter": 56, "Venus": 52, "Saturn": 39, "Lagna": 49,
}
EXPECTED_SAV_TOTAL: Final[int] = 337
TRIKONA_GROUPS: Final[tuple[tuple[int, int, int], ...]] = (
    (0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11)
)
DUAL_LORD_PAIRS: Final[tuple[tuple[int, int], ...]] = (
    (0, 7), (1, 6), (2, 5), (8, 11), (9, 10)
)
RASHI_GUNAKAR: Final[tuple[int, ...]] = (7, 10, 8, 4, 5, 2, 1, 8, 9, 5, 11, 12)
GRAHA_GUNAKAR: Final[dict[ASHTAKAVARGA_PLANETS, int]] = {
    "Sun": 5, "Moon": 5, "Mars": 8, "Mercury": 5,
    "Jupiter": 10, "Venus": 7, "Saturn": 5,
}
