from vedicastro.VedicAstro import VedicHoroscopeData
from ascendant.chart.utils import get_divisional_target
from ascendant.const import NODE_MAP, SELECTED_PLANETS, RASHIS
from ascendant.types import (
    ALLOWED_DIVISIONS,
    HOUSES,
    ChartType,
    LagnaType,
    PlanetType,
    PlanetsType,
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

        self.planets = self.get_planets()
        self.lagna = self.get_lagna()
        self.chart = self.get_rasi_chart()

    def get_planets(self, n: ALLOWED_DIVISIONS = 1) -> PlanetsType:
        planets: PlanetsType = []
        for _planet in self.__chart__.objects:
            name = _planet.id
            if name not in SELECTED_PLANETS:
                continue
            lon: float = _planet.lon
            data = self.__horoscope__.get_rl_nl_sl_data(lon)
            target_sign, _ = get_divisional_target(lon, n)
            sign = getSignName(target_sign)

            planet: PlanetType = {
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

    def get_lagna(self, n: ALLOWED_DIVISIONS = 1) -> LagnaType:
        asc = self.__chart__.getAngle("Asc")
        lon: float = asc.lon
        data = self.__horoscope__.get_rl_nl_sl_data(lon)
        target_sign, _ = get_divisional_target(lon, n)
        sign = getSignName(target_sign)

        lagna: LagnaType = {
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

    def get_rasi_chart(self) -> ChartType:
        chart: ChartType = {}

        lagna_sign = self.lagna["sign"]["name"]
        lagna_index = RASHIS.index(lagna_sign)

        for i in range(12):
            house_num: HOUSES = i + 1
            sign_index = (lagna_index + i) % 12
            sign = RASHIS[sign_index]

            planets_in_house = [p for p in self.planets if p["sign"]["name"] == sign]

            chart[house_num] = {
                "sign": sign,
                "planets": planets_in_house,
                "lagna": self.lagna if house_num == 1 else None,
            }

        return chart

    def get_varga_chakra_chart(self, n: ALLOWED_DIVISIONS) -> ChartType:
        chart: ChartType = {}

        lagna = self.get_lagna(n)
        planets = self.get_planets(n)

        lagna_sign = lagna["sign"]["name"]
        lagna_index = RASHIS.index(lagna_sign)

        for i in range(12):
            house_num: HOUSES = i + 1
            sign_index = (lagna_index + i) % 12
            sign = RASHIS[sign_index]

            planets_in_house = [p for p in planets if p["sign"]["name"] == sign]

            chart[house_num] = {
                "sign": sign,
                "planets": planets_in_house,
                "lagna": lagna if house_num == 1 else None,
            }

        return chart
