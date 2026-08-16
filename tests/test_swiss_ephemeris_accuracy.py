"""Acceptance tests for sidereal positions from independent references."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from ascendant.horoscope import HoroscopeData


@dataclass(frozen=True)
class ReferenceCase:
    """A birth chart with reference positions captured before the migration."""

    year: int
    month: int
    day: int
    hour: int
    minute: int
    utc: str
    latitude: float
    longitude: float
    ayanamsa: str
    house_system: str
    sun: float
    moon: float
    ascendant: float
    first_house: float
    second_house: float | None = None


REFERENCE_CASES = (
    ReferenceCase(
        1900,
        1,
        1,
        6,
        0,
        "+5:30",
        22.5726,
        88.3639,
        "Lahiri",
        "Whole Sign",
        257.70923343208085,
        250.24941804644592,
        252.79969077342392,
        240.0,
    ),
    ReferenceCase(
        1925,
        6,
        15,
        13,
        45,
        "-5:00",
        40.7128,
        -74.006,
        "Lahiri_1940",
        "Placidus",
        61.31247665819556,
        358.92341990788145,
        173.66477676069843,
        173.66477676069843,
    ),
    ReferenceCase(
        2100,
        12,
        31,
        23,
        55,
        "+5:30",
        28.6139,
        77.209,
        "Krishnamurti_Senthilathiban",
        "Equal",
        254.93298567103764,
        265.3912544618971,
        158.09447090230287,
        158.09447090230287,
    ),
    ReferenceCase(
        1990,
        1,
        1,
        12,
        0,
        "+5:30",
        28.6139,
        77.209,
        "Lahiri",
        "Porphyry",
        256.8599180914489,
        306.4652948972497,
        343.9226400242266,
        343.9226400242266,
        13.015604358247334,
    ),
)


def angular_error(actual: float, expected: float) -> float:
    """Return the shortest angular distance in degrees."""
    return abs((actual - expected + 180) % 360 - 180)


@pytest.mark.parametrize("reference", REFERENCE_CASES)
def test_sidereal_positions_match_reference_within_tenth_of_degree(
    reference: ReferenceCase,
) -> None:
    horoscope = HoroscopeData(
        year=reference.year,
        month=reference.month,
        day=reference.day,
        hour=reference.hour,
        minute=reference.minute,
        second=0,
        utc=reference.utc,
        latitude=reference.latitude,
        longitude=reference.longitude,
        ayanamsa=reference.ayanamsa,
        house_system=reference.house_system,
    )
    chart = horoscope.generate_chart()

    assert angular_error(chart.get_object("Sun").lon, reference.sun) <= 0.1
    assert angular_error(chart.get_object("Moon").lon, reference.moon) <= 0.1
    assert angular_error(chart.get_angle("Asc").lon, reference.ascendant) <= 0.1
    assert angular_error(chart.get_house("House1").lon, reference.first_house) <= 0.1
    if reference.second_house is not None:
        assert (
            angular_error(chart.get_house("House2").lon, reference.second_house) <= 0.1
        )
