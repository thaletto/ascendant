"""Behavior tests for public sidereal horoscope generation."""

from __future__ import annotations

import pytest

from ascendant.ephemeris import EphemerisChart
from ascendant.horoscope import HoroscopeData


def test_generates_complete_sidereal_chart(horoscope: HoroscopeData) -> None:
    chart = horoscope.generate_chart()

    assert isinstance(chart, EphemerisChart)
    assert {object_.id for object_ in chart.objects} == {
        "Sun",
        "Moon",
        "Mars",
        "Mercury",
        "Jupiter",
        "Venus",
        "Saturn",
        "North Node",
        "South Node",
    }
    assert len(chart.houses) == 12
    assert {angle.id for angle in chart.angles} == {"Asc", "MC", "Desc", "IC"}
    assert all(0 <= object_.lon < 360 for object_ in chart.objects)
    assert all(0 <= house.lon < 360 for house in chart.houses)


def test_lunar_nodes_are_opposite(horoscope: HoroscopeData) -> None:
    chart = horoscope.generate_chart()

    north_node = chart.get_object("North Node").lon
    south_node = chart.get_object("South Node").lon

    assert (south_node - north_node) % 360 == pytest.approx(180.0)


def test_invalid_utc_offset_is_rejected() -> None:
    horoscope = HoroscopeData(
        year=1990,
        month=1,
        day=1,
        hour=12,
        minute=0,
        second=0,
        utc="invalid",
        latitude=28.6139,
        longitude=77.2090,
    )

    with pytest.raises(ValueError, match="utc must be formatted"):
        _ = horoscope.generate_chart()
