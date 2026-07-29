"""Behavior tests for public yoga evaluation."""

from __future__ import annotations

import pytest

from ascendant import Ascendant
from ascendant.const import BENEFIC_PLANETS, MALEFIC_PLANETS
from ascendant.horoscope import HoroscopeData
from ascendant.yoga import Yoga


def test_yoga_results_have_a_consistent_public_contract(
    astrology: Ascendant,
) -> None:
    yogas = astrology.get_yogas()

    assert yogas
    assert len({yoga["id"] for yoga in yogas}) == len(yogas)
    for yoga in yogas:
        assert set(yoga) == {
            "id", "name", "present", "strength", "details", "type"
        }
        assert isinstance(yoga["present"], bool)
        assert yoga["strength"] >= 0
        assert yoga["type"] in {"Positive", "Neutral", "Negative"}


def test_relative_house_judgements_wrap_from_house_twelve(
    horoscope: HoroscopeData,
) -> None:
    yoga = Yoga(horoscope)

    assert yoga.relative_house("Moon", "Moon") == 1
    assert yoga.planet_in_kendra_from(12, "Moon")
    assert yoga.planet_in_trikona_from(12, "Moon")
    assert "Moon" in {
        planet["name"] for planet in yoga.planets_in_relative_house("Moon", 1)
    }


def test_aspect_and_influence_judgements_are_distinct(
    horoscope: HoroscopeData,
) -> None:
    yoga = Yoga(horoscope)

    assert yoga.is_house_aspected_by(12, ("Jupiter",))
    assert yoga.is_house_aspected_by(12, MALEFIC_PLANETS)
    assert not yoga.is_house_aspected_by(11, BENEFIC_PLANETS)
    assert yoga.is_house_influenced_by(11, BENEFIC_PLANETS)
    assert not yoga.is_house_influenced_by(
        11,
        BENEFIC_PLANETS,
        excluding=("Mercury", "Venus"),
    )


@pytest.mark.parametrize(
    ("year", "month", "hour", "name", "expected_id", "expected_type"),
    [
        (1950, 3, 0, "Sakata", "sakata", "Negative"),
        (1950, 1, 6, "Sumukha", "sumukha", "Positive"),
        (1950, 3, 6, "Sodaranasa", "sodaranasa", "Neutral"),
        (1950, 1, 0, "Parakrama", "parakrama", "Positive"),
    ],
)
def test_representative_yoga_judgements_match_expected_outcomes(
    year: int,
    month: int,
    hour: int,
    name: str,
    expected_id: str,
    expected_type: str,
) -> None:
    astrology = Ascendant(
        year=year,
        month=month,
        day=15,
        hour=hour,
        minute=0,
        second=0,
        utc="+5:30",
        latitude=28.6139,
        longitude=77.2090,
        ayanamsa="Lahiri",
        house_system="Whole Sign",
    )

    result = next(
        yoga for yoga in astrology.get_yogas() if yoga["name"] == name
    )

    assert result["id"] == expected_id
    assert result["present"]
    assert result["strength"] == 1.0
    assert result["type"] == expected_type
