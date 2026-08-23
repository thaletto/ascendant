"""Typed application-wide defaults for Ascendant calculations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import cast


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
        ayanamsa = cast(object, self.ayanamsa)
        house_system = cast(object, self.house_system)
        if not isinstance(ayanamsa, Ayanamsa):
            raise TypeError("ayanamsa must be an Ayanamsa value")
        if not isinstance(house_system, HouseSystem):
            raise TypeError("house_system must be a HouseSystem value")


DEFAULT_CONFIG = AscendantConfig()


def configure(config: AscendantConfig) -> None:
    """Reject the retired process-wide configuration mechanism.

    Pass ``config=`` to each :class:`ascendant.Ascendant` instance instead.
    The function remains available so existing callers receive an actionable
    migration error instead of silently sharing mutable process state.
    """
    candidate = cast(object, config)
    if not isinstance(candidate, AscendantConfig):
        raise TypeError("config must be an AscendantConfig instance")
    raise RuntimeError(
        "Process-wide configuration is no longer supported. ",
        "Pass config= to each Ascendant instance."
    )


def get_config() -> AscendantConfig:
    """Return Ascendant's immutable built-in calculation defaults."""
    return DEFAULT_CONFIG


def reset_config() -> None:
    """Compatibility no-op; the built-in defaults cannot be mutated."""
