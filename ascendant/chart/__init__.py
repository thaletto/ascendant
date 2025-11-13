from vedicastro.VedicAstro import VedicHoroscopeData
from ascendant.chart.utils import get_divisional_target
from ascendant.const import NODE_MAP, SELECTED_PLANETS
from ascendant.types import (
    Lagna,
    Planet,
    Planets,
)
from ascendant.utils import PlanetSignRelation, getSignName


class Chart:
    """Represents the birth chart and divisional charts.

    Args:
        horoscope: `VedicHoroscopeData`
    """

    def __init__(self, horoscope: VedicHoroscopeData):
        self.__horoscope__ = horoscope
        self.__chart__ = horoscope.generate_chart()

    def get_planets_in_D1(self) -> Planets:
        planets: Planets = []
        for _planet in self.__chart__.objects:
            name = _planet.id
            if name not in SELECTED_PLANETS:
                continue
            lon: float = _planet.lon
            data = self.__horoscope__.get_rl_nl_sl_data(lon)
            target_sign, _ = get_divisional_target(lon, 1)
            sign = getSignName(target_sign)

            planet: Planet = {
                "name": NODE_MAP.get(name, name),
                "longitude": lon,
                "is_retrograde": _planet.isRetrograde(),
                "inSign": PlanetSignRelation(name, sign),
                "sign": {
                    "name": sign,
                    "lord": data.get("RasiLord", ""),
                    "nakshatra": {
                        "name": data.get("Nakshatra", ""),
                        "lord": data.get("NakshatraLord", ""),
                        "pada": data.get("Pada", ""),
                    },
                },
            }
            planets.append(planet)
        return planets

    def get_lagna_in_D1(self) -> Lagna:
        asc = self.__chart__.getAngle("Asc")
        lon: float = asc.lon
        data = self.__horoscope__.get_rl_nl_sl_data(lon)
        target_sign, _ = get_divisional_target(lon, 1)
        sign = getSignName(target_sign)

        lagna: Lagna = {
            "name": "Lagna",
            "longitude": lon,
            "is_retrograde": False,
            "sign": {
                "name": sign,
                "lord": data.get("RasiLord", ""),
                "nakshatra": {
                    "name": data.get("Nakshatra", ""),
                    "lord": data.get("NakshatraLord", ""),
                    "pada": data.get("Pada", ""),
                },
            },
        }
        return lagna
