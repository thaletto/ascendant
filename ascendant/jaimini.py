"""Deterministic calculations for Ascendant's named Jaimini core."""

from __future__ import annotations

from typing import Literal, TypedDict, cast

from ascendant.const import CLASSICAL_PLANETS, RASHI_LORD_MAP, RASHIS
from ascendant.types import PLANETS, ChartType
from ascendant.types import RASHIS as Rashi

JAIMINI_METHOD = "jaimini_srao_7_core_v1"

CharaKarakaRole = Literal[
    "Atmakaraka",
    "Amatyakaraka",
    "Bhratrikaraka",
    "Matrikaraka",
    "Putrakaraka",
    "Gnatikaraka",
    "Darakaraka",
]
KarakaBasis = Literal[
    "degree_order",
    "shared_degree",
    "rahu_tie_fallback",
    "unresolved_tie",
]

KARAKA_ROLES: tuple[CharaKarakaRole, ...] = (
    "Atmakaraka",
    "Amatyakaraka",
    "Bhratrikaraka",
    "Matrikaraka",
    "Putrakaraka",
    "Gnatikaraka",
    "Darakaraka",
)


class CharaKarakaAssignment(TypedDict):
    """One role in the seven-karaka degree order."""

    role: CharaKarakaRole
    planets: list[PLANETS]
    degrees_in_sign: list[float]
    basis: KarakaBasis


class KarakamshaResult(TypedDict):
    """Navamsa signs occupied by the Atmakaraka assignment."""

    planets: list[PLANETS]
    signs: list[Rashi]


class ArgalaRelation(TypedDict):
    """One sign contributing to an Argala relation."""

    position: int
    sign: Rashi
    planets: list[PLANETS]


class ArgalaResult(TypedDict):
    """Raw Argala contributors and their opposing signs."""

    reference_sign: Rashi
    supporting: list[ArgalaRelation]
    obstructing: list[ArgalaRelation]
    secondary_supporting: ArgalaRelation
    secondary_obstructing: ArgalaRelation


class ArgalaCollection(TypedDict):
    """Sign-based Argala plus Ketu's reversed calculation."""

    by_sign: dict[Rashi, ArgalaResult]
    ketu: ArgalaResult


class JaiminiResult(TypedDict):
    """Serializable result of the selected Jaimini calculation method."""

    method: Literal["jaimini_srao_7_core_v1"]
    chara_karakas: list[CharaKarakaAssignment]
    rashi_drishti: dict[Rashi, list[Rashi]]
    karakamsha: KarakamshaResult
    arudha_padas: dict[str, Rashi]
    upapada: Rashi
    argala: ArgalaCollection


def _planets_by_name(chart: ChartType) -> dict[PLANETS, dict[str, object]]:
    return {
        planet["name"]: cast(dict[str, object], cast(object, planet))
        for house in chart.values()
        for planet in house["planets"]
    }


def _planet_signs(chart: ChartType) -> dict[PLANETS, Rashi]:
    return {
        planet["name"]: planet["sign"]["name"]
        for house in chart.values()
        for planet in house["planets"]
    }


def _occupants(chart: ChartType) -> dict[Rashi, list[PLANETS]]:
    return {
        house["sign"]: [planet["name"] for planet in house["planets"]]
        for house in chart.values()
    }


def _degree_in_sign(longitude: float) -> float:
    return round(longitude % 30.0, 6)


def _arcseconds_in_sign(longitude: float) -> int:
    return int(round((longitude % 30.0) * 3600.0))


def _chara_karakas(d1: ChartType) -> list[CharaKarakaAssignment]:
    planets = _planets_by_name(d1)
    grouped: dict[int, list[PLANETS]] = {}
    for planet in CLASSICAL_PLANETS:
        longitude = cast(float, planets[planet]["longitude"])
        grouped.setdefault(_arcseconds_in_sign(longitude), []).append(planet)

    rahu_used = False
    assignments: list[CharaKarakaAssignment] = []
    role_index = 0
    for arcseconds in sorted(grouped, reverse=True):
        holders = grouped[arcseconds]
        longitudes = [
            cast(float, planets[planet]["longitude"])
            for planet in holders
        ]
        assignments.append(
            {
                "role": KARAKA_ROLES[role_index],
                "planets": holders,
                "degrees_in_sign": [
                    _degree_in_sign(longitude) for longitude in longitudes
                ],
                "basis": (
                    "shared_degree"
                    if len(holders) > 1
                    else "degree_order"
                ),
            }
        )
        role_index += 1

        for _ in range(len(holders) - 1):
            if not rahu_used and "Rahu" in planets:
                rahu_longitude = cast(float, planets["Rahu"]["longitude"])
                reverse_degree = 30.0 - (rahu_longitude % 30.0)
                assignments.append(
                    {
                        "role": KARAKA_ROLES[role_index],
                        "planets": ["Rahu"],
                        "degrees_in_sign": [round(reverse_degree, 6)],
                        "basis": "rahu_tie_fallback",
                    }
                )
                rahu_used = True
            else:
                assignments.append(
                    {
                        "role": KARAKA_ROLES[role_index],
                        "planets": [],
                        "degrees_in_sign": [],
                        "basis": "unresolved_tie",
                    }
                )
            role_index += 1

    return assignments


def _rashi_drishti() -> dict[Rashi, list[Rashi]]:
    movable = frozenset(("Aries", "Cancer", "Libra", "Capricorn"))
    fixed = frozenset(("Taurus", "Leo", "Scorpio", "Aquarius"))
    dual = frozenset(("Gemini", "Virgo", "Sagittarius", "Pisces"))
    result: dict[Rashi, list[Rashi]] = {}
    for index, sign in enumerate(RASHIS):
        if sign in movable:
            adjacent = RASHIS[(index + 1) % 12]
            targets = fixed.difference((adjacent,))
        elif sign in fixed:
            adjacent = RASHIS[(index - 1) % 12]
            targets = movable.difference((adjacent,))
        else:
            targets = dual.difference((sign,))
        result[sign] = [target for target in RASHIS if target in targets]
    return result


def _arudha_padas(d1: ChartType) -> dict[str, Rashi]:
    planet_signs = _planet_signs(d1)
    padas: dict[str, Rashi] = {}
    for house_number, house in d1.items():
        source_index = RASHIS.index(house["sign"])
        lord = cast(PLANETS, RASHI_LORD_MAP[house["sign"]])
        lord_index = RASHIS.index(planet_signs[lord])
        distance = (lord_index - source_index) % 12
        padas[f"A{house_number}"] = RASHIS[(lord_index + distance) % 12]
    return padas


def _relation(
    reference_index: int,
    position: int,
    occupants: dict[Rashi, list[PLANETS]],
    *,
    reverse: bool,
) -> ArgalaRelation:
    offset = position - 1
    target_index = (
        reference_index - offset if reverse else reference_index + offset
    ) % 12
    sign = RASHIS[target_index]
    return {
        "position": position,
        "sign": sign,
        "planets": occupants[sign],
    }


def _argala_for_sign(
    sign: Rashi,
    occupants: dict[Rashi, list[PLANETS]],
    *,
    reverse: bool = False,
) -> ArgalaResult:
    reference_index = RASHIS.index(sign)
    return {
        "reference_sign": sign,
        "supporting": [
            _relation(reference_index, position, occupants, reverse=reverse)
            for position in (2, 4, 11)
        ],
        "obstructing": [
            _relation(reference_index, position, occupants, reverse=reverse)
            for position in (12, 10, 3)
        ],
        "secondary_supporting": _relation(
            reference_index,
            5,
            occupants,
            reverse=reverse,
        ),
        "secondary_obstructing": _relation(
            reference_index,
            9,
            occupants,
            reverse=reverse,
        ),
    }


def calculate_jaimini(d1: ChartType, d9: ChartType) -> JaiminiResult:
    """Return the selected seven-karaka Jaimini core from saved chart data."""

    chara_karakas = _chara_karakas(d1)
    atmakaraka = chara_karakas[0]
    d9_signs = _planet_signs(d9)
    karakamsha_planets = atmakaraka["planets"]
    arudha_padas = _arudha_padas(d1)
    occupants = _occupants(d1)
    ketu_sign = _planet_signs(d1)["Ketu"]
    return {
        "method": JAIMINI_METHOD,
        "chara_karakas": chara_karakas,
        "rashi_drishti": _rashi_drishti(),
        "karakamsha": {
            "planets": karakamsha_planets,
            "signs": [d9_signs[planet] for planet in karakamsha_planets],
        },
        "arudha_padas": arudha_padas,
        "upapada": arudha_padas["A12"],
        "argala": {
            "by_sign": {
                sign: _argala_for_sign(sign, occupants)
                for sign in RASHIS
            },
            "ketu": _argala_for_sign(ketu_sign, occupants, reverse=True),
        },
    }
