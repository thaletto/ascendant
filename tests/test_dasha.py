"""Behavior tests for the public Vimshottari Dasha API."""

from __future__ import annotations

from datetime import datetime

from ascendant import Ascendant


def test_vimshottari_timeline_has_nine_ordered_mahadashas(
    astrology: Ascendant,
) -> None:
    timeline = astrology.get_dasha_timeline()

    assert len(timeline) == 9
    starts = [
        datetime.strptime(period["start"], "%d-%m-%Y")
        for period in timeline
    ]
    assert starts == sorted(starts)
    assert {period["mahadasha"] for period in timeline} == {
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
        "Rahu", "Ketu",
    }


def test_each_mahadasha_has_ordered_antardashas(astrology: Ascendant) -> None:
    timeline = astrology.get_dasha_timeline()

    for mahadasha in timeline:
        antardashas = mahadasha["antardashas"]
        assert len(antardashas) == 9
        assert {period["antardasha"] for period in antardashas} == {
            "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
            "Rahu", "Ketu",
        }
        starts = [
            datetime.strptime(period["start"], "%d-%m-%Y")
            for period in antardashas
        ]
        assert starts == sorted(starts)


def test_current_dasha_uses_requested_date(astrology: Ascendant) -> None:
    first_mahadasha = astrology.get_dasha_timeline()[0]

    current = astrology.get_current_dasha(first_mahadasha["start"])

    assert current["mahadasha"] == first_mahadasha
    assert current["antardasha"] == first_mahadasha["antardashas"][0]
