"""Public behavior tests for application-wide calculation defaults."""

from __future__ import annotations

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


def test_process_default_is_immutable() -> None:
    configured = AscendantConfig(
        ayanamsa=Ayanamsa.RAMAN,
        house_system=HouseSystem.PLACIDUS,
    )

    with pytest.raises(RuntimeError, match="Pass config=.+Ascendant"):
        configure(configured)

    reset_config()

    assert get_config() == AscendantConfig()


def test_two_instances_can_use_different_configs_concurrently() -> None:
    raman = Ascendant(
        year=1990,
        month=1,
        day=1,
        hour=12,
        minute=0,
        second=0,
        utc="+5:30",
        latitude=28.6139,
        longitude=77.2090,
        config=AscendantConfig(
            ayanamsa=Ayanamsa.RAMAN,
            house_system=HouseSystem.PLACIDUS,
        ),
    )
    lahiri = Ascendant(
        year=1990,
        month=1,
        day=1,
        hour=12,
        minute=0,
        second=0,
        utc="+5:30",
        latitude=28.6139,
        longitude=77.2090,
        config=AscendantConfig(
            ayanamsa=Ayanamsa.LAHIRI,
            house_system=HouseSystem.EQUAL,
        ),
    )

    assert raman.horoscope_data.ayanamsa == Ayanamsa.RAMAN
    assert raman.horoscope_data.house_system == HouseSystem.PLACIDUS
    assert lahiri.horoscope_data.ayanamsa == Ayanamsa.LAHIRI
    assert lahiri.horoscope_data.house_system == HouseSystem.EQUAL


def test_constructor_values_override_configured_defaults() -> None:
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
        config=AscendantConfig(
            ayanamsa=Ayanamsa.RAMAN,
            house_system=HouseSystem.PLACIDUS,
        ),
        ayanamsa="Krishnamurti",
        house_system="Equal",
    )

    assert astrology.horoscope_data.ayanamsa == "Krishnamurti"
    assert astrology.horoscope_data.house_system == "Equal"


def test_instance_keeps_its_configuration_snapshot() -> None:
    config = AscendantConfig(
        ayanamsa=Ayanamsa.RAMAN,
        house_system=HouseSystem.PLACIDUS,
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
        config=config,
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
        config=AscendantConfig(house_system=HouseSystem.PORPHYRY),
    )

    chart = astrology.horoscope_data.generate_chart()

    assert chart.get_house("House2").lon == pytest.approx(13.0156043582)
    assert chart.get_house("House3").lon == pytest.approx(42.1085686923)
