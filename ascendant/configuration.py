"""Typed application-wide defaults for Ascendant calculations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from threading import RLock


class Ayanamsa(StrEnum):
    """Sidereal reference systems supported by Ascendant."""

    LAHIRI = "Lahiri"
    LAHIRI_1940 = "Lahiri_1940"
    LAHIRI_VP285 = "Lahiri_VP285"
    LAHIRI_ICRC = "Lahiri_ICRC"
    RAMAN = "Raman"
    KRISHNAMURTI = "Krishnamurti"
    KRISHNAMURTI_SENTHILATHIBAN = "Krishnamurti_Senthilathiban"


class HouseSystem(StrEnum):
    """House division systems supported by Ascendant."""

    WHOLE_SIGN = "Whole Sign"
    PLACIDUS = "Placidus"
    EQUAL = "Equal"
    EQUAL_2 = "Equal 2"
    PORPHYRY = "Porphyry"


def parse_ayanamsa(value: Ayanamsa | str) -> Ayanamsa:
    """Return a supported ayanamsa or reject the supplied value."""
    if isinstance(value, Ayanamsa):
        return value
    for ayanamsa in Ayanamsa:
        if value.casefold() == ayanamsa.value.casefold():
            return ayanamsa
    raise ValueError(f'Unsupported ayanamsa "{value}"')


def parse_house_system(value: HouseSystem | str) -> HouseSystem:
    """Return a supported house system or reject the supplied value."""
    if isinstance(value, HouseSystem):
        return value
    normalized = value.replace("_", " ").strip()
    for house_system in HouseSystem:
        if normalized.casefold() == house_system.value.casefold():
            return house_system
    raise ValueError(f'Unsupported house system "{value}"')


@dataclass(frozen=True, slots=True)
class AscendantConfig:
    """Calculation defaults for newly created Ascendant instances."""

    ayanamsa: Ayanamsa = Ayanamsa.LAHIRI
    house_system: HouseSystem = HouseSystem.WHOLE_SIGN

    def __post_init__(self) -> None:
        if not isinstance(self.ayanamsa, Ayanamsa):
            raise TypeError("ayanamsa must be an Ayanamsa value")
        if not isinstance(self.house_system, HouseSystem):
            raise TypeError("house_system must be a HouseSystem value")


_CONFIG_LOCK = RLock()
_config = AscendantConfig()


def configure(config: AscendantConfig) -> None:
    """Replace the defaults used by newly created Ascendant instances."""
    if not isinstance(config, AscendantConfig):
        raise TypeError("config must be an AscendantConfig instance")
    global _config
    with _CONFIG_LOCK:
        _config = config


def get_config() -> AscendantConfig:
    """Return the current immutable application defaults."""
    with _CONFIG_LOCK:
        return _config


def reset_config() -> None:
    """Restore Ascendant's built-in calculation defaults."""
    configure(AscendantConfig())
