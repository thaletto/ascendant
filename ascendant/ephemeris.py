"""Small typed sidereal chart adapter backed directly by Swiss Ephemeris."""

from __future__ import annotations

from dataclasses import dataclass
import re
from threading import RLock
from typing import Final

import swisseph as swe


SIDEREAL_FLAGS: Final[int] = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL
DEFAULT_SIDEREAL_MODE: Final[int] = swe.SIDM_FAGAN_BRADLEY
_SIDEREAL_LOCK: Final[RLock] = RLock()
_UTC_OFFSET_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^(?P<sign>[+-])?(?P<hours>\d{1,2}):(?P<minutes>\d{1,2})(?::(?P<seconds>\d{1,2}))?$"
)

PLANET_IDS: Final[tuple[tuple[str, int], ...]] = (
    ("Sun", swe.SUN),
    ("Moon", swe.MOON),
    ("Mercury", swe.MERCURY),
    ("Venus", swe.VENUS),
    ("Mars", swe.MARS),
    ("Jupiter", swe.JUPITER),
    ("Saturn", swe.SATURN),
    ("North Node", swe.MEAN_NODE),
)


def _normalize_degrees(value: float) -> float:
    return value % 360.0


def _utc_offset_hours(value: str) -> float:
    match = _UTC_OFFSET_PATTERN.fullmatch(value.strip())
    if match is None:
        raise ValueError("utc must be formatted as ±HH:MM or ±HH:MM:SS")

    hours = int(match["hours"])
    minutes = int(match["minutes"])
    seconds = int(match["seconds"] or 0)
    if hours > 23 or minutes > 59 or seconds > 59:
        raise ValueError("utc must be a valid UTC offset")
    sign = -1.0 if match["sign"] == "-" else 1.0
    return sign * (hours + minutes / 60 + seconds / 3600)


def julian_day(
    year: int, month: int, day: int, hour: int, minute: int, second: int, utc: str
) -> float:
    """Return the UTC Julian day for a local Gregorian birth time."""
    local_hour = hour + minute / 60 + second / 3600
    return swe.julday(year, month, day, local_hour - _utc_offset_hours(utc), swe.GREG_CAL)


@dataclass(frozen=True)
class ChartInput:
    """The birth details and calculation settings needed for one chart."""

    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    utc: str
    latitude: float
    longitude: float


@dataclass(frozen=True)
class EphemerisObject:
    """A planet, lunar node, house cusp, or chart angle."""

    id: str
    lon: float
    lat: float = 0.0
    lonspeed: float = 0.0
    latspeed: float = 0.0
    size: float = 0.0

    def is_retrograde(self) -> bool:
        return self.lonspeed < 0


@dataclass(frozen=True)
class EphemerisChart:
    """The limited typed chart surface consumed by Ascendant and advanced callers."""

    objects: tuple[EphemerisObject, ...]
    houses: tuple[EphemerisObject, ...]
    angles: tuple[EphemerisObject, ...]

    def get_object(self, identifier: str) -> EphemerisObject:
        return self._find(self.objects, identifier)

    def get_house(self, identifier: str) -> EphemerisObject:
        return self._find(self.houses, identifier)

    def get_angle(self, identifier: str) -> EphemerisObject:
        return self._find(self.angles, identifier)

    def get(self, identifier: str) -> EphemerisObject:
        if identifier.startswith("House"):
            return self.get_house(identifier)
        if identifier in {"Asc", "MC", "Desc", "IC"}:
            return self.get_angle(identifier)
        return self.get_object(identifier)

    @staticmethod
    def _find(values: tuple[EphemerisObject, ...], identifier: str) -> EphemerisObject:
        for value in values:
            if value.id == identifier:
                return value
        raise KeyError(identifier)


def build_sidereal_chart(
    *,
    birth: ChartInput,
    ayanamsa: int,
    house_system: bytes,
) -> EphemerisChart:
    """Calculate a sidereal chart without relying on flatlib.

    Swiss Ephemeris keeps the selected ayanamsa in process-global state. The
    lock keeps that state stable from setting the mode through every position
    and house calculation for a chart.
    """
    jd = julian_day(
        birth.year,
        birth.month,
        birth.day,
        birth.hour,
        birth.minute,
        birth.second,
        birth.utc,
    )
    with _SIDEREAL_LOCK:
        try:
            swe.set_sid_mode(ayanamsa, 0.0, 0.0)
            objects = _calculate_objects(jd)
            houses, angles = _calculate_houses(
                jd, birth.latitude, birth.longitude, house_system
            )
        finally:
            swe.set_sid_mode(DEFAULT_SIDEREAL_MODE, 0.0, 0.0)
    return EphemerisChart(objects=objects, houses=houses, angles=angles)


def _calculate_objects(jd: float) -> tuple[EphemerisObject, ...]:
    objects: list[EphemerisObject] = []
    north_node: EphemerisObject | None = None
    for identifier, body in PLANET_IDS:
        values, _ = swe.calc_ut(jd, body, SIDEREAL_FLAGS)
        obj = EphemerisObject(
            id=identifier,
            lon=_normalize_degrees(values[0]),
            lat=values[1],
            lonspeed=values[3],
            latspeed=values[4],
        )
        objects.append(obj)
        if identifier == "North Node":
            north_node = obj

    if north_node is None:
        raise RuntimeError("Swiss Ephemeris did not return the north node")
    return tuple(
        [
            *objects,
            EphemerisObject(
                id="South Node",
                lon=_normalize_degrees(north_node.lon + 180.0),
                lat=north_node.lat,
                lonspeed=north_node.lonspeed,
                latspeed=north_node.latspeed,
            ),
        ]
    )


def _calculate_houses(
    jd: float, latitude: float, longitude: float, house_system: bytes
) -> tuple[tuple[EphemerisObject, ...], tuple[EphemerisObject, ...]]:
    cusps, ascmc = swe.houses_ex(jd, latitude, longitude, house_system, swe.FLG_SIDEREAL)
    houses = tuple(
        EphemerisObject(
            id=f"House{index + 1}",
            lon=_normalize_degrees(cusp),
            size=_normalize_degrees(cusps[(index + 1) % len(cusps)] - cusp),
        )
        for index, cusp in enumerate(cusps)
    )
    asc = _normalize_degrees(ascmc[0])
    mc = _normalize_degrees(ascmc[1])
    angles = (
        EphemerisObject(id="Asc", lon=asc),
        EphemerisObject(id="MC", lon=mc),
        EphemerisObject(id="Desc", lon=_normalize_degrees(asc + 180.0)),
        EphemerisObject(id="IC", lon=_normalize_degrees(mc + 180.0)),
    )
    return houses, angles
