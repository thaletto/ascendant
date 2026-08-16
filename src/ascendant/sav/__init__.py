"""Typed Parashari Ashtakavarga calculations."""

from __future__ import annotations

from ascendant.ephemeris import EphemerisChart
from ascendant.horoscope import HoroscopeData
from ascendant.sav.constants import (
    ASHTAKAVARGA_ENTITY_ORDER,
    ASHTAKAVARGA_PLANET_ORDER,
    CONTRIBUTION_OFFSETS,
    DUAL_LORD_PAIRS,
    EXPECTED_BAV_TOTALS,
    EXPECTED_SAV_TOTAL,
    GRAHA_GUNAKAR,
    RASHI_GUNAKAR,
    RASHIS_ORDER,
    TRIKONA_GROUPS,
)
from ascendant.sav.types import (
    ASHTAKAVARGA_ENTITIES,
    ASHTAKAVARGA_PLANETS,
    AshtakavargaResult,
    PindaType,
    SignScores,
)

__all__ = [
    "ASHTAKAVARGA_ENTITIES",
    "ASHTAKAVARGA_PLANETS",
    "Ashtakavarga",
    "AshtakavargaResult",
    "PindaType",
    "SignScores",
]


class Ashtakavarga:
    """Calculate classical Bhinnashtakavarga, SAV, and Shodhya Pinda."""

    _chart: EphemerisChart
    _positions: dict[ASHTAKAVARGA_ENTITIES, int]
    _result: AshtakavargaResult | None

    def __init__(self, horoscope: HoroscopeData):
        self._initialize(horoscope.generate_chart())

    @classmethod
    def from_ephemeris(
        cls,
        ephemeris: EphemerisChart,
    ) -> Ashtakavarga:
        ashtakavarga = cls.__new__(cls)
        ashtakavarga._initialize(ephemeris)
        return ashtakavarga

    def _initialize(self, ephemeris: EphemerisChart) -> None:
        self._chart = ephemeris
        self._positions = self._get_positions()
        self._result = None

    def _get_positions(self) -> dict[ASHTAKAVARGA_ENTITIES, int]:
        positions: dict[ASHTAKAVARGA_ENTITIES, int] = {}
        for planet in ASHTAKAVARGA_PLANET_ORDER:
            positions[planet] = (
                int(self._chart.get_object(planet).lon // 30) % 12
            )
        positions["Lagna"] = (
            int(self._chart.get_angle("Asc").lon // 30) % 12
        )
        return positions

    def _calculate_bhinna(self) -> dict[ASHTAKAVARGA_ENTITIES, SignScores]:
        result: dict[ASHTAKAVARGA_ENTITIES, SignScores] = {}
        for target in ASHTAKAVARGA_ENTITY_ORDER:
            scores: SignScores = {sign: 0 for sign in RASHIS_ORDER}
            for sign_index, sign in enumerate(RASHIS_ORDER):
                for contributor in ASHTAKAVARGA_ENTITY_ORDER:
                    distance = (
                        (sign_index - self._positions[contributor]) % 12 + 1
                    )
                    if distance in CONTRIBUTION_OFFSETS[target][contributor]:
                        scores[sign] += 1
            result[target] = scores
        return result

    @staticmethod
    def _validate_bhinna(
        bhinna: dict[ASHTAKAVARGA_ENTITIES, SignScores],
    ) -> None:
        for entity, expected_total in EXPECTED_BAV_TOTALS.items():
            actual_total = sum(bhinna[entity].values())
            if actual_total != expected_total:
                raise ValueError(
                    f"Invalid {entity} BAV total: {actual_total}; ",
                    f"expected {expected_total}."
                )

    @staticmethod
    def _calculate_sarva(
        bhinna: dict[ASHTAKAVARGA_ENTITIES, SignScores],
    ) -> SignScores:
        sarva: SignScores = {
            sign: sum(
                bhinna[planet][sign] for planet in ASHTAKAVARGA_PLANET_ORDER
            )
            for sign in RASHIS_ORDER
        }
        total = sum(sarva.values())
        if total != EXPECTED_SAV_TOTAL:
            raise ValueError(
                f"Invalid SAV total: {total}; expected {EXPECTED_SAV_TOTAL}."
            )
        return sarva

    @staticmethod
    def _copy_tables(
        tables: dict[ASHTAKAVARGA_PLANETS, SignScores],
    ) -> dict[ASHTAKAVARGA_PLANETS, SignScores]:
        return {planet: dict(scores) for planet, scores in tables.items()}

    def _calculate_reduced(
        self,
        bhinna: dict[ASHTAKAVARGA_ENTITIES, SignScores],
    ) -> dict[ASHTAKAVARGA_PLANETS, SignScores]:
        reduced = self._copy_tables(
            {planet: bhinna[planet] for planet in ASHTAKAVARGA_PLANET_ORDER}
        )
        for scores in reduced.values():
            for group in TRIKONA_GROUPS:
                minimum = min(scores[RASHIS_ORDER[index]] for index in group)
                for index in group:
                    scores[RASHIS_ORDER[index]] -= minimum
            for first, second in DUAL_LORD_PAIRS:
                first_sign = RASHIS_ORDER[first]
                second_sign = RASHIS_ORDER[second]
                first_value = scores[first_sign]
                second_value = scores[second_sign]
                if first_value >= second_value:
                    scores[first_sign] = first_value - second_value
                    scores[second_sign] = 0
                else:
                    scores[first_sign] = 0
                    scores[second_sign] = second_value - first_value
        return reduced

    def _calculate_pinda(
        self,
        reduced: dict[ASHTAKAVARGA_PLANETS, SignScores],
    ) -> dict[ASHTAKAVARGA_PLANETS, PindaType]:
        result: dict[ASHTAKAVARGA_PLANETS, PindaType] = {}
        for target in ASHTAKAVARGA_PLANET_ORDER:
            scores = reduced[target]
            rashi_pinda = sum(
                scores[sign] * RASHI_GUNAKAR[index]
                for index, sign in enumerate(RASHIS_ORDER)
            )
            graha_pinda = sum(
                scores[RASHIS_ORDER[self._positions[planet]]]
                * GRAHA_GUNAKAR[planet]
                for planet in ASHTAKAVARGA_PLANET_ORDER
            )
            result[target] = {
                "rashi_pinda": rashi_pinda,
                "graha_pinda": graha_pinda,
                "shodhya_pinda": rashi_pinda + graha_pinda,
            }
        return result

    def calculate(self) -> AshtakavargaResult:
        """Return the complete raw, reduced, and Pinda result."""
        if self._result is not None:
            return self._result
        bhinna = self._calculate_bhinna()
        self._validate_bhinna(bhinna)
        sarva = self._calculate_sarva(bhinna)
        reduced = self._calculate_reduced(bhinna)
        shodhya_pinda = self._calculate_pinda(reduced)
        result: AshtakavargaResult = {
            "bhinna": bhinna,
            "sarva": sarva,
            "reduced": reduced,
            "shodhya_pinda": shodhya_pinda,
            "totals": {
                **{
                    entity: sum(scores.values())
                    for entity, scores in bhinna.items()
                },
                "sarva": sum(sarva.values()),
            },
        }
        self._result = result
        return result

    def get_bhinna_ashtakavarga(
        self,
    ) -> dict[ASHTAKAVARGA_ENTITIES, SignScores]:
        """Return the seven planetary and Lagna BAV tables."""
        return self.calculate()["bhinna"]

    def get_sarvashtakavarga(self) -> SignScores:
        """Return the combined SAV table, excluding Lagna."""
        return self.calculate()["sarva"]

    def get_reduced_ashtakavarga(
        self,
    ) -> dict[ASHTAKAVARGA_PLANETS, SignScores]:
        """Return the Trikona- and Ekadhipatya-reduced BAV tables."""
        return self.calculate()["reduced"]

    def get_shodhya_pinda(self) -> dict[ASHTAKAVARGA_PLANETS, PindaType]:
        """Return Rashi, Graha, and total Shodhya Pinda values."""
        return self.calculate()["shodhya_pinda"]
