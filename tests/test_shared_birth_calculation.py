"""Public behavior tests for shared birth-chart calculation."""

from __future__ import annotations

import pytest
import swisseph as swe

from ascendant import Ascendant


def test_ascendant_calculates_one_birth_chart(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calculations = {"planets": 0, "houses": 0}
    original_calc_ut = swe.calc_ut
    original_houses_ex = swe.houses_ex

    def counting_calc_ut(
        tjdut: float,
        planet: int,
        flags: int,
    ) -> tuple[tuple[float, float, float, float, float, float], int]:
        calculations["planets"] += 1
        return original_calc_ut(tjdut, planet, flags)

    def counting_houses_ex(
        tjdut: float,
        lat: float,
        lon: float,
        hsys: bytes,
        flags: int,
    ) -> tuple[tuple[float, ...], tuple[float, ...]]:
        calculations["houses"] += 1
        return original_houses_ex(tjdut, lat, lon, hsys, flags)

    monkeypatch.setattr(swe, "calc_ut", counting_calc_ut)
    monkeypatch.setattr(swe, "houses_ex", counting_houses_ex)

    astrology = Ascendant(
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
    _ = astrology.get_jaimini()

    assert calculations == {"planets": 8, "houses": 1}
