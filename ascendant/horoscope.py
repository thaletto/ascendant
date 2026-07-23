"""Birth-chart construction and longitude metadata backed by Swiss Ephemeris."""

from typing import Final, TypedDict, cast

import swisseph as swe

from ascendant.configuration import (
    Ayanamsa,
    HouseSystem,
    parse_ayanamsa,
    parse_house_system,
)
from ascendant.const import NAKSHATRAS, SIGN_LORDS, VIMSHOTTARI_PLANETS, VIMSHOTTARI_YEARS
from ascendant.ephemeris import ChartInput, EphemerisChart, build_sidereal_chart
from ascendant.types import NAKSHATRAS as NAKSHATRA_NAMES
from ascendant.types import PADA, PLANETS, RASHI_LORDS

AYANAMSA_MAPPING: Final[dict[Ayanamsa, int]] = {
    Ayanamsa.LAHIRI: swe.SIDM_LAHIRI,
    Ayanamsa.LAHIRI_1940: swe.SIDM_LAHIRI_1940,
    Ayanamsa.LAHIRI_VP285: swe.SIDM_LAHIRI_VP285,
    Ayanamsa.LAHIRI_ICRC: swe.SIDM_LAHIRI_ICRC,
    Ayanamsa.RAMAN: swe.SIDM_RAMAN,
    Ayanamsa.KRISHNAMURTI: swe.SIDM_KRISHNAMURTI,
    Ayanamsa.KRISHNAMURTI_SENTHILATHIBAN: swe.SIDM_KRISHNAMURTI_VP291,
}

HOUSE_SYSTEM_MAPPING: Final[dict[HouseSystem, bytes]] = {
    HouseSystem.PLACIDUS: b"P",
    HouseSystem.EQUAL: b"A",
    HouseSystem.EQUAL_2: b"E",
    HouseSystem.WHOLE_SIGN: b"W",
    HouseSystem.PORPHYRY: b"O",
}


class LongitudeMetadata(TypedDict):
    """KP sign and nakshatra data derived from an ecliptic longitude."""

    Nakshatra: NAKSHATRA_NAMES
    Pada: PADA
    NakshatraLord: PLANETS
    RasiLord: RASHI_LORDS
    SubLord: PLANETS
    SubSubLord: PLANETS


def normalize_house_system(house_system: str | bytes) -> bytes:
    if isinstance(house_system, bytes):
        if house_system in HOUSE_SYSTEM_MAPPING.values():
            return house_system
        raise ValueError(f"Unsupported house system code {house_system!r}")
    return HOUSE_SYSTEM_MAPPING[parse_house_system(house_system)]


class HoroscopeData:
    """Input data and sidereal chart helpers used by Ascendant's modules."""

    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        utc: str,
        latitude: float,
        longitude: float,
        ayanamsa: Ayanamsa | str = Ayanamsa.LAHIRI,
        house_system: HouseSystem | str | bytes = HouseSystem.EQUAL,
    ):
        self.year: int = year
        self.month: int = month
        self.day: int = day
        self.hour: int = hour
        self.minute: int = minute
        self.second: int = second
        self.utc: str = utc
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.ayanamsa = parse_ayanamsa(ayanamsa)
        if isinstance(house_system, bytes):
            normalize_house_system(house_system)
            self.house_system: HouseSystem | bytes = house_system
        else:
            self.house_system = parse_house_system(house_system)

    def chart_input(self) -> ChartInput:
        """Return the immutable data consumed by the Swiss Ephemeris adapter."""
        return ChartInput(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=self.hour,
            minute=self.minute,
            second=self.second,
            utc=self.utc,
            latitude=self.latitude,
            longitude=self.longitude,
        )

    def get_ayanamsa(self) -> int:
        """Return the requested Swiss Ephemeris sidereal mode."""
        return AYANAMSA_MAPPING[self.ayanamsa]

    def get_house_system(self) -> bytes:
        return normalize_house_system(self.house_system)

    def generate_chart(self) -> EphemerisChart:
        return build_sidereal_chart(
            birth=self.chart_input(),
            ayanamsa=self.get_ayanamsa(),
            house_system=self.get_house_system(),
        )

    def get_rl_nl_sl_data(self, deg: float) -> LongitudeMetadata | None:
        """Return the KP longitude metadata used by Ascendant's public charts.

        The interval arithmetic deliberately matches VedicAstro 0.2.1 so existing
        chart and dasha results remain stable.
        """
        durations = VIMSHOTTARI_YEARS
        lords = VIMSHOTTARI_PLANETS
        star_lords = lords * 3

        sign_deg = deg % 360
        sign_index = int(sign_deg // 30)
        nakshatra_deg = sign_deg % 13.332
        nakshatra_index = int(sign_deg // 13.332) % len(NAKSHATRAS)
        pada = cast(PADA, int((nakshatra_deg % 13.332) // 3.325) + 1)

        deg = deg - 120 * int(deg / 120)
        degcum = 0.0
        for i in range(9):
            deg_nl = 360 / 27
            j = i
            while True:
                deg_sl = deg_nl * durations[j] / 120
                k = j
                while True:
                    deg_ss = deg_sl * durations[k] / 120
                    degcum += deg_ss
                    if degcum >= deg:
                        return {
                            "Nakshatra": NAKSHATRAS[nakshatra_index],
                            "Pada": pada,
                            "NakshatraLord": star_lords[nakshatra_index],
                            "RasiLord": SIGN_LORDS[sign_index],
                            "SubLord": lords[j],
                            "SubSubLord": lords[k],
                        }
                    k = (k + 1) % 9
                    if k == j:
                        break
                j = (j + 1) % 9
                if j == i:
                    break
        return None
