"""Public behavior tests for Ascendant's Jaimini core."""

from __future__ import annotations

from copy import deepcopy

from ascendant import Ascendant, calculate_jaimini
from ascendant.types import ChartType, PLANETS, PlanetType


def _planet(chart: ChartType, name: PLANETS) -> PlanetType:
    return next(
        planet
        for house in chart.values()
        for planet in house["planets"]
        if planet["name"] == name
    )


def test_public_facade_returns_classical_jaimini_core(
    astrology: Ascendant,
) -> None:
    result = astrology.get_jaimini()

    assert result["method"] == "jaimini_srao_7_core_v1"
    assert [
        (assignment["role"], assignment["planets"])
        for assignment in result["chara_karakas"]
    ] == [
        ("Atmakaraka", ["Saturn"]),
        ("Amatyakaraka", ["Sun"]),
        ("Bhratrikaraka", ["Mars"]),
        ("Matrikaraka", ["Venus"]),
        ("Putrakaraka", ["Jupiter"]),
        ("Gnatikaraka", ["Moon"]),
        ("Darakaraka", ["Mercury"]),
    ]
    assert result["karakamsha"] == {
        "planets": ["Saturn"],
        "signs": ["Libra"],
    }


def test_public_facade_returns_sign_aspects_and_projected_points(
    astrology: Ascendant,
) -> None:
    result = astrology.get_jaimini()

    assert result["rashi_drishti"]["Aries"] == [
        "Leo",
        "Scorpio",
        "Aquarius",
    ]
    assert result["rashi_drishti"]["Taurus"] == [
        "Cancer",
        "Libra",
        "Capricorn",
    ]
    assert result["rashi_drishti"]["Pisces"] == [
        "Gemini",
        "Virgo",
        "Sagittarius",
    ]
    assert result["arudha_padas"]["A1"] == "Virgo"
    assert result["arudha_padas"]["A12"] == "Libra"
    assert result["upapada"] == "Libra"


def test_public_facade_exposes_argala_without_a_numeric_score(
    astrology: Ascendant,
) -> None:
    result = astrology.get_jaimini()
    pisces = result["argala"]["by_sign"]["Pisces"]

    assert [relation["sign"] for relation in pisces["supporting"]] == [
        "Aries",
        "Gemini",
        "Capricorn",
    ]
    assert [relation["sign"] for relation in pisces["obstructing"]] == [
        "Aquarius",
        "Sagittarius",
        "Taurus",
    ]
    assert pisces["secondary_supporting"]["sign"] == "Cancer"
    assert pisces["secondary_obstructing"]["sign"] == "Scorpio"
    assert "score" not in pisces
    assert result["argala"]["ketu"]["reference_sign"] == "Cancer"
    assert [
        relation["sign"]
        for relation in result["argala"]["ketu"]["supporting"]
    ] == ["Gemini", "Aries", "Virgo"]
    assert result["argala"]["ketu"]["secondary_supporting"]["sign"] == (
        "Pisces"
    )
    assert result["argala"]["ketu"]["secondary_obstructing"]["sign"] == (
        "Scorpio"
    )


def test_exact_degree_tie_shares_role_and_uses_reverse_rahu_boundary(
    astrology: Ascendant,
) -> None:
    d1 = deepcopy(astrology.get_chart(1))
    d9 = astrology.get_chart(9)
    sun = _planet(d1, "Sun")
    saturn = _planet(d1, "Saturn")
    rahu = _planet(d1, "Rahu")
    sun["longitude"] = (sun["longitude"] // 30 * 30) + 29.25
    saturn["longitude"] = (saturn["longitude"] // 30 * 30) + 29.25
    rahu["longitude"] = rahu["longitude"] // 30 * 30

    assignments = calculate_jaimini(d1, d9)["chara_karakas"]

    assert assignments[0] == {
        "role": "Atmakaraka",
        "planets": ["Sun", "Saturn"],
        "degrees_in_sign": [29.25, 29.25],
        "basis": "shared_degree",
    }
    assert assignments[1] == {
        "role": "Amatyakaraka",
        "planets": ["Rahu"],
        "degrees_in_sign": [30.0],
        "basis": "rahu_tie_fallback",
    }


def test_third_planet_in_exact_tie_is_left_explicitly_unresolved(
    astrology: Ascendant,
) -> None:
    d1 = deepcopy(astrology.get_chart(1))
    d9 = astrology.get_chart(9)
    for name in ("Sun", "Moon", "Saturn"):
        planet = _planet(d1, name)
        planet["longitude"] = (planet["longitude"] // 30 * 30) + 29.25

    assignments = calculate_jaimini(d1, d9)["chara_karakas"]

    assert assignments[0]["planets"] == ["Sun", "Moon", "Saturn"]
    assert assignments[1]["basis"] == "rahu_tie_fallback"
    assert assignments[2] == {
        "role": "Bhratrikaraka",
        "planets": [],
        "degrees_in_sign": [],
        "basis": "unresolved_tie",
    }
