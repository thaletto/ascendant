"""Shared public fixtures for Ascendant's behavior tests."""

from __future__ import annotations

import pytest

from ascendant import Ascendant
from ascendant.horoscope import HoroscopeData


@pytest.fixture(scope="module")
def horoscope() -> HoroscopeData:
    """Return a stable New Delhi birth chart fixture."""
    return HoroscopeData(
        year=1990,
        month=1,
        day=1,
        hour=12,
        minute=0,
        second=0,
        utc="+5:30",
        latitude=28.6139,
        longitude=77.2090,
        ayanamsa="Lahiri",
        house_system="Whole Sign",
    )


@pytest.fixture(scope="module")
def astrology() -> Ascendant:
    """Return the public facade for the shared birth chart."""
    return Ascendant(
        year=1990,
        month=1,
        day=1,
        hour=12,
        minute=0,
        second=0,
        utc="+5:30",
        latitude=28.6139,
        longitude=77.2090,
        ayanamsa="Lahiri",
        house_system="Whole Sign",
    )
