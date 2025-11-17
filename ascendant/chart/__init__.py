from vedicastro.VedicAstro import VedicHoroscopeData
from ascendant.chart.utils import aspect_offsets_for_planet, get_divisional_target
from ascendant.const import (
    NODE_MAP,
    SELECTED_PLANETS,
    RASHIS,
    ALLOWED_DIVISIONS as DIVISIONS,
)
from typing import List
from ascendant.types import (
    ALLOWED_DIVISIONS,
    HOUSES,
    PLANETS,
    AspectType,
    ChartType,
    LagnaType,
    PlanetType,
    PlanetsType,
)
from ascendant.utils import planetSignRelation, getSignName


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
        """
        Retrieves the list of planets for a specified divisional chart (varga).

        Args:
            n: The divisional chart number (e.g., 1 for Rasi, 9 for Navamsa). Defaults to 1.

        Returns:
            A list of PlanetType objects, or None if the division is not allowed.
        """
        if n not in DIVISIONS:
            return None

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
                "inSign": planetSignRelation(name, sign, lon),
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
        """
        Retrieves the Lagna (Ascendant) for a specified divisional chart (varga).

        Args:
            n: The divisional chart number. Defaults to 1.

        Returns:
            A LagnaType object, or None if the division is not allowed.
        """
        if n not in DIVISIONS:
            return None

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
        """
        Generates the Rasi (D1) chart based on the Lagna and planet positions.

        Returns:
            A ChartType object representing the Rasi chart.
        """
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
        """
        Generates a specific divisional chart (varga chakra) based on the given division number.

        Args:
            n: The divisional chart number.

        Returns:
            A ChartType object representing the specified divisional chart, or None if the division is not allowed.
        """
        if n not in DIVISIONS:
            return None

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

    def graha_drishti(
        self, n: ALLOWED_DIVISIONS, planet: PLANETS | None = None
    ) -> List[AspectType]:
        """
        Calculates and returns the planetary aspects (graha drishti) for a given divisional chart.

        Args:
            n: The divisional chart number.
            planet: Optional. If provided, returns aspects only for this specific planet.

        Returns:
            A list of AspectType objects, each detailing a planet's aspects and the planets in aspected houses.
            Returns None if the division is not allowed.
        """
        if n not in DIVISIONS:
            return None

        chart = self.get_varga_chakra_chart(n)

        # Pre-process chart to create mappings for quick lookups
        planet_to_house = {}
        house_to_planets = {h: [] for h in range(1, 13)}

        for house_num in range(1, 13):
            house = chart.get(house_num)
            if not house:
                continue
            for p in house.get("planets", []):
                planet_name = p["name"]
                house_to_planets[house_num].append(planet_name)
                if planet_name != "Ketu":
                    planet_to_house[planet_name] = house_num

        # Determine which planets to process
        planets_to_process = {}
        if planet:
            if planet in planet_to_house:
                planets_to_process = {planet: planet_to_house[planet]}
        else:
            planets_to_process = planet_to_house

        # Build results using the pre-processed mappings
        results: List[AspectType] = []
        for planet_name, from_house in planets_to_process.items():
            aspected_houses = [
                (from_house - 1 + offset) % 12 + 1
                for offset in aspect_offsets_for_planet(planet_name)
            ]

            aspected_houses_info = [
                {house: house_to_planets.get(house, [])} for house in aspected_houses
            ]

            aspect_data: AspectType = {
                "planet": planet_name,
                "from_house": from_house,
                "aspect_houses": aspected_houses_info,
            }
            results.append(aspect_data)

        return results
