"""Birth-chart construction and longitude metadata backed by sidereal flatlib."""

from typing import Any

from flatlib import const
from flatlib.chart import Chart as FlatlibChart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

from ascendant.const import NAKSHATRAS, SIGN_LORDS, VIMSHOTTARI_PLANETS, VIMSHOTTARI_YEARS

AYANAMSA_MAPPING = {
    "Lahiri": const.AY_LAHIRI,
    "Lahiri_1940": const.AY_LAHIRI_1940,
    "Lahiri_VP285": const.AY_LAHIRI_VP285,
    "Lahiri_ICRC": const.AY_LAHIRI_ICRC,
    "Raman": const.AY_RAMAN,
    "Krishnamurti": const.AY_KRISHNAMURTI,
    "Krishnamurti_Senthilathiban": const.AY_KRISHNAMURTI_SENTHILATHIBAN,
}

HOUSE_SYSTEM_MAPPING = {
    "Placidus": const.HOUSES_PLACIDUS,
    "Equal": const.HOUSES_EQUAL,
    "Equal 2": const.HOUSES_EQUAL_2,
    "Whole Sign": const.HOUSES_WHOLE_SIGN,
}


def _canonical_name(value: str, supported: dict[str, Any]) -> str:
    for name in supported:
        if value.casefold() == name.casefold():
            return name
    return value


def normalize_house_system(house_system: str) -> Any:
    key = house_system.replace("_", " ").strip().title()
    return HOUSE_SYSTEM_MAPPING.get(key, HOUSE_SYSTEM_MAPPING["Whole Sign"])


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
        ayanamsa: str = "Lahiri",
        house_system: str = "Equal",
    ):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.utc = utc
        self.latitude = latitude
        self.longitude = longitude
        self.ayanamsa = ayanamsa
        self.house_system = house_system

    def get_ayanamsa(self) -> Any:
        if not isinstance(self.ayanamsa, str):
            return None
        return AYANAMSA_MAPPING.get(_canonical_name(self.ayanamsa, AYANAMSA_MAPPING))

    def get_house_system(self) -> Any:
        if isinstance(self.house_system, str):
            return normalize_house_system(self.house_system)
        return self.house_system

    def generate_chart(self) -> FlatlibChart:
        date = Datetime(
            [self.year, self.month, self.day],
            ["+", self.hour, self.minute, self.second],
            self.utc,
        )
        position = GeoPos(self.latitude, self.longitude)
        return FlatlibChart(
            date,
            position,
            IDs=const.LIST_OBJECTS,
            hsys=self.get_house_system(),
            mode=self.get_ayanamsa(),
        )

    def get_rl_nl_sl_data(self, deg: float) -> dict[str, str | int] | None:
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
        pada = int((nakshatra_deg % 13.332) // 3.325) + 1

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
