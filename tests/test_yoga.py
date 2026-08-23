"""Behavior tests for public yoga evaluation."""

from __future__ import annotations

import json

import pytest

from ascendant import Ascendant
from ascendant.const import BENEFIC_PLANETS, MALEFIC_PLANETS
from ascendant.horoscope import HoroscopeData
from ascendant.yoga import YOGA_REGISTRY, YOGA_RULES, Yoga


def test_representative_yogas_are_backed_by_declarative_rules() -> None:
    migrated = {
        "GajaKesari",
        "Hamsa",
        "Malavya",
        "Sasa",
        "Ruchaka",
        "Bhadra",
    }

    assert migrated <= YOGA_RULES.keys()
    assert migrated <= YOGA_REGISTRY.keys()


def test_migrated_yoga_results_remain_byte_identical(
    astrology: Ascendant,
) -> None:
    migrated = {
        "GajaKesari",
        "Hamsa",
        "Malavya",
        "Sasa",
        "Ruchaka",
        "Bhadra",
    }
    results = [
        result
        for result in astrology.get_yogas()
        if result["name"] in migrated
    ]

    assert json.dumps(results, sort_keys=True, separators=(",", ":")) == (
        '[{"details":"Jupiter in house 4 and Moon is in 12",'
        '"id":"gajakesari","name":"GajaKesari","present":false,'
        '"strength":0,"type":"Positive"},{"details":"Jupiter is in '
        'Gemini (house 4).","id":"hamsa","name":"Hamsa",'
        '"present":false,"strength":0.0,"type":"Positive"},'
        '{"details":"Venus is in Capricorn (house 11).","id":"malavya",'
        '"name":"Malavya","present":false,"strength":0.0,'
        '"type":"Positive"},{"details":"Saturn is in Sagittarius '
        '(house 10).","id":"sasa","name":"Sasa","present":false,'
        '"strength":0.0,"type":"Neutral"},{"details":"Mars is in '
        'Scorpio (house 9).","id":"ruchaka","name":"Ruchaka",'
        '"present":false,"strength":0.0,"type":"Positive"},'
        '{"details":"Mercury is in Capricorn (house 11).","id":"bhadra",'
        '"name":"Bhadra","present":false,"strength":0.0,'
        '"type":"Positive"}]'
    )


@pytest.mark.parametrize(
    ("birth", "expected"),
    [
        (
            (1940, 1, 15, 6),
            (
                "GajaKesari",
                0,
                "Jupiter in house 4 and Moon is in 4",
                "Positive",
            ),
        ),
        (
            (1940, 1, 15, 0),
            ("Hamsa", 0.9, "Jupiter is in Pisces (house 7).", "Positive"),
        ),
        (
            (1945, 11, 15, 6),
            ("Malavya", 1.0, "Venus is in Libra (house 1).", "Positive"),
        ),
        (
            (1955, 1, 15, 12),
            ("Sasa", 1.0, "Saturn is in Libra (house 7).", "Neutral"),
        ),
        (
            (1940, 2, 15, 0),
            ("Ruchaka", 0.9, "Mars is in Aries (house 7).", "Positive"),
        ),
        (
            (1940, 6, 15, 6),
            ("Bhadra", 1.0, "Mercury is in Gemini (house 1).", "Positive"),
        ),
    ],
)
def test_migrated_present_yogas_keep_their_characterized_results(
    birth: tuple[int, int, int, int],
    expected: tuple[str, float, str, str],
) -> None:
    year, month, day, hour = birth
    name, strength, details, classification = expected
    astrology = Ascendant(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=0,
        second=0,
        utc="+5:30",
        latitude=28.6139,
        longitude=77.2090,
    )

    result = next(
        item for item in astrology.get_yogas() if item["name"] == name
    )

    assert result == {
        "id": name.casefold(),
        "name": name,
        "present": True,
        "strength": strength,
        "details": details,
        "type": classification,
    }


def test_yoga_results_have_a_consistent_public_contract(
    astrology: Ascendant,
) -> None:
    yogas = astrology.get_yogas()

    assert yogas
    assert len({yoga["id"] for yoga in yogas}) == len(yogas)
    for yoga in yogas:
        assert set(yoga) == {"id", "name", "present", "strength", "details", "type"}
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

    result = next(yoga for yoga in astrology.get_yogas() if yoga["name"] == name)

    assert result["id"] == expected_id
    assert result["present"]
    assert result["strength"] == 1.0
    assert result["type"] == expected_type
