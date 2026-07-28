"""Behavior tests for the public Vimshottari Dasha API."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta, timezone

import pytest

from ascendant import Ascendant
from ascendant.dasha import DashaTimeline
from ascendant.types import DashasType


def _timeline() -> DashasType:
    return [
        {
            "mahadasha": "Saturn",
            "start": "01-01-2020",
            "end": "31-12-2029",
            "antardashas": [
                {
                    "mahadasha": "Saturn",
                    "antardasha": "Saturn",
                    "start": "01-01-2020",
                    "end": "31-12-2024",
                },
                {
                    "mahadasha": "Saturn",
                    "antardasha": "Mercury",
                    "start": "01-01-2025",
                    "end": "31-12-2029",
                },
            ],
        },
        {
            "mahadasha": "Mercury",
            "start": "01-01-2030",
            "end": "31-12-2039",
            "antardashas": [],
        },
    ]


def test_timeline_current_is_inclusive_and_empty_outside() -> None:
    timeline = DashaTimeline(_timeline())

    at_start = timeline.current("01-01-2020")
    at_end = timeline.current("31-12-2029")

    assert at_start["mahadasha"] == _timeline()[0]
    assert at_start["antardasha"] == _timeline()[0]["antardashas"][0]
    assert at_end["mahadasha"] == _timeline()[0]
    assert at_end["antardasha"] == _timeline()[0]["antardashas"][1]
    assert timeline.current("31-12-2019") == {
        "mahadasha": None,
        "antardasha": None,
    }


def test_timeline_selects_relative_periods_without_crossing_boundaries(
) -> None:
    periods = _timeline()
    timeline = DashaTimeline(periods)

    assert timeline.mahadasha(1, "01-01-2025") == periods[1]
    assert timeline.mahadasha(-1, "01-01-2025") is None
    assert (
        timeline.antardasha(1, "01-01-2020")
        == periods[0]["antardashas"][1]
    )
    assert timeline.antardasha(-1, "01-01-2020") is None
    assert timeline.antardasha(1, "01-01-2025") is None


def test_timeline_normalizes_supported_query_dates_to_utc() -> None:
    timeline = DashaTimeline(_timeline())

    assert timeline.current(date(2020, 1, 1))["mahadasha"] is not None
    naive = datetime(2020, 1, 1, tzinfo=UTC).replace(tzinfo=None)
    assert timeline.current(naive)["mahadasha"] is not None
    assert (
        timeline.current(datetime(2020, 1, 1, tzinfo=UTC))["mahadasha"]
        is not None
    )
    local_midnight = datetime(
        2020,
        1,
        1,
        0,
        30,
        tzinfo=timezone(timedelta(hours=5, minutes=30)),
    )
    assert timeline.current(local_midnight)["mahadasha"] is None
    assert timeline.current()["mahadasha"] is not None


def test_timeline_rejects_malformed_queries_and_boundaries() -> None:
    with pytest.raises(ValueError, match="DD-MM-YYYY"):
        _ = DashaTimeline(_timeline()).current("2020-01-01")

    periods = _timeline()
    periods[1]["end"] = "not-a-date"
    with pytest.raises(ValueError, match="timeline boundaries"):
        _ = DashaTimeline(periods)


def test_vimshottari_timeline_has_nine_ordered_mahadashas(
    astrology: Ascendant,
) -> None:
    timeline = astrology.get_dasha_timeline()

    assert len(timeline) == 9
    starts = [
        datetime.strptime(period["start"], "%d-%m-%Y").replace(tzinfo=UTC)
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
            datetime.strptime(period["start"], "%d-%m-%Y").replace(tzinfo=UTC)
            for period in antardashas
        ]
        assert starts == sorted(starts)


def test_current_dasha_uses_requested_date(astrology: Ascendant) -> None:
    first_mahadasha = astrology.get_dasha_timeline()[0]

    current = astrology.get_current_dasha(first_mahadasha["start"])

    assert current["mahadasha"] == first_mahadasha
    assert current["antardasha"] == first_mahadasha["antardashas"][0]
