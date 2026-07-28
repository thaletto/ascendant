"""Public behavior tests for application-wide calculation defaults."""

from __future__ import annotations

from collections.abc import Iterator
from typing import cast

import pytest

from ascendant import (
    Ascendant,
    AscendantConfig,
    Ayanamsa,
    HouseSystem,
    configure,
    get_config,
    reset_config,
)


@pytest.fixture(autouse=True)
def isolated_configuration() -> Iterator[None]:
    reset_config()
    yield
    reset_config()


def test_application_configuration_can_be_replaced_and_reset() -> None:
    configured = AscendantConfig(
        ayanamsa=Ayanamsa.RAMAN,
        house_system=HouseSystem.PLACIDUS,
    )

    configure(configured)

    assert get_config() is configured

    reset_config()

    assert get_config() == AscendantConfig()


def test_ascendant_uses_configured_calculation_defaults() -> None:
    configure(
        AscendantConfig(
            ayanamsa=Ayanamsa.RAMAN,
            house_system=HouseSystem.PLACIDUS,
        )
    )

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
    )

    assert astrology.horoscope_data.ayanamsa == Ayanamsa.RAMAN
    assert astrology.horoscope_data.house_system == HouseSystem.PLACIDUS


def test_constructor_values_override_configured_defaults() -> None:
    configure(
        AscendantConfig(
            ayanamsa=Ayanamsa.RAMAN,
            house_system=HouseSystem.PLACIDUS,
        )
    )

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
        ayanamsa="Krishnamurti",
        house_system="Equal",
    )

    assert astrology.horoscope_data.ayanamsa == "Krishnamurti"
    assert astrology.horoscope_data.house_system == "Equal"


def test_existing_instance_keeps_its_configuration_snapshot() -> None:
    configure(
        AscendantConfig(
            ayanamsa=Ayanamsa.RAMAN,
            house_system=HouseSystem.PLACIDUS,
        )
    )
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
    )

    configure(
        AscendantConfig(
            ayanamsa=Ayanamsa.LAHIRI,
            house_system=HouseSystem.EQUAL,
        )
    )

    assert astrology.horoscope_data.ayanamsa == Ayanamsa.RAMAN
    assert astrology.horoscope_data.house_system == HouseSystem.PLACIDUS


def test_invalid_constructor_house_system_is_rejected() -> None:
    with pytest.raises(ValueError, match='Unsupported house system "Porphry"'):
        _ = Ascendant(
            year=1990,
            month=1,
            day=1,
            hour=12,
            minute=0,
            second=0,
            utc="+5:30",
            latitude=28.6139,
            longitude=77.2090,
            house_system="Porphry",
        )


def test_invalid_constructor_ayanamsa_is_rejected() -> None:
    with pytest.raises(ValueError, match='Unsupported ayanamsa "Lahri"'):
        _ = Ascendant(
            year=1990,
            month=1,
            day=1,
            hour=12,
            minute=0,
            second=0,
            utc="+5:30",
            latitude=28.6139,
            longitude=77.2090,
            ayanamsa="Lahri",
        )


def test_configuration_requires_the_typed_immutable_value() -> None:
    config = AscendantConfig()

    with pytest.raises(TypeError, match="AscendantConfig"):
        configure(
            cast(
                AscendantConfig,
                cast(object, {"house_system": "Whole Sign"}),
            )
        )

    with pytest.raises(AttributeError):
        config.__setattr__("house_system", HouseSystem.PORPHYRY)


def test_porphyry_configuration_calculates_porphyry_house_cusps() -> None:
    configure(
        AscendantConfig(house_system=HouseSystem.PORPHYRY)
    )
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
    )

    chart = astrology.horoscope_data.generate_chart()

    assert chart.get_house("House2").lon == pytest.approx(13.0156043582)
    assert chart.get_house("House3").lon == pytest.approx(42.1085686923)
