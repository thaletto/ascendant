"""Behavior tests for public chart and aspect APIs."""

from __future__ import annotations

from typing import cast

import pytest

from ascendant import Ascendant
from ascendant.chart import Chart
from ascendant.horoscope import HoroscopeData
from ascendant.types import ALLOWED_DIVISIONS


@pytest.mark.parametrize("division", (1, 9, 10))
def test_supported_divisional_chart_has_complete_house_layout(
    astrology: Ascendant,
    division: int,
) -> None:
    chart = astrology.get_chart(cast(ALLOWED_DIVISIONS, division))

    assert list(chart) == list(range(1, 13))
    assert chart[1]["lagna"] is not None
    assert chart[1]["lagna"]["name"] == "Lagna"
    assert {house["sign"] for house in chart.values()} == {
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
    }

    planets = [planet for house in chart.values() for planet in house["planets"]]
    assert {planet["name"] for planet in planets} == {
        "Sun",
        "Moon",
        "Mars",
        "Mercury",
        "Jupiter",
        "Venus",
        "Saturn",
        "Rahu",
        "Ketu",
    }
    assert all(0 <= planet["longitude"] < 360 for planet in planets)


def test_invalid_division_is_rejected(astrology: Ascendant) -> None:
    with pytest.raises(ValueError, match="Division 8 not allowed"):
        _ = astrology.get_chart(cast(ALLOWED_DIVISIONS, cast(object, 8)))


def test_graha_drishti_reports_requested_planet_only(
    horoscope: HoroscopeData,
) -> None:
    aspects = Chart(horoscope).graha_drishti(n=1, planet="Sun")

    assert len(aspects) == 1
    assert aspects[0]["planet"] == "Sun"
    assert aspects[0]["from_house"] in range(1, 13)
    assert len(aspects[0]["aspect_houses"]) == 1
