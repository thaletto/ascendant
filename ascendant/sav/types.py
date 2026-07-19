"""Public type definitions for Ashtakavarga calculations."""

from __future__ import annotations

from typing import Literal, TypedDict

from ascendant.types import RASHIS

ASHTAKAVARGA_PLANETS = Literal[
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"
]
ASHTAKAVARGA_ENTITIES = ASHTAKAVARGA_PLANETS | Literal["Lagna"]
SignScores = dict[RASHIS, int]


class PindaType(TypedDict):
    """The three Shodhya Pinda components for one planet."""

    rashi_pinda: int
    graha_pinda: int
    shodhya_pinda: int


class AshtakavargaResult(TypedDict):
    """Complete raw and reduced Ashtakavarga result."""

    bhinna: dict[ASHTAKAVARGA_ENTITIES, SignScores]
    sarva: SignScores
    reduced: dict[ASHTAKAVARGA_PLANETS, SignScores]
    shodhya_pinda: dict[ASHTAKAVARGA_PLANETS, PindaType]
    totals: dict[str, int]
