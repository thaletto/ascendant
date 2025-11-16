from typing import Callable, Dict, List
from vedicastro.VedicAstro import VedicHoroscopeData
from ascendant.types import (
    HOUSES,
    PLANETS_LAGNA,
    RASHI_LORDS,
    RASHIS,
    PlanetsType,
    YogaType,
)
from ascendant.const import RASHI_LORD_MAP
from ascendant.utils import yogaNameToId

YogaFunction = Callable[["Yoga"], YogaType]

YOGA_REGISTRY: Dict[str, YogaFunction] = {}


def register_yoga(name: str):
    def decorator(func: YogaFunction) -> YogaFunction:
        def wrapper(yoga: "Yoga") -> YogaType:
            result = func(yoga)
            result["id"] = yogaNameToId(name)
            return result

        YOGA_REGISTRY[name] = wrapper
        return wrapper

    return decorator


class Yoga:
    def __init__(self, horoscope: VedicHoroscopeData):
        from ascendant.chart import Chart

        self.chart = Chart(horoscope).get_rasi_chart()

    def get_house_of_planet(self, planet: PLANETS_LAGNA) -> HOUSES:
        """Return house number where planet is located in the chart"""
        if planet == "Lagna":
            for house, data in self.chart.items():
                if data["lagna"]:
                    return house
        else:
            for house, data in self.chart.items():
                planets = data["planets"]
                for _planet in planets:
                    if _planet["name"] == planet:
                        return house
        return None

    def get_house_of_rashi(self, rashi: RASHIS) -> HOUSES:
        """Returns the house number of Rashi"""
        for house, data in self.chart.items():
            sign = data["sign"]
            if sign == rashi:
                return house
        return None

    def planet_in_kendra_from(self, base_house: HOUSES, target_planet: PLANETS_LAGNA):
        """Check if a planet is in Kendra (1, 4, 7, 10) from a reference house"""
        target_house = self.get_house_of_planet(target_planet)
        if not target_house:
            return False
        kendra_houses = [(base_house + i - 1) % 12 for i in [1, 4, 7, 10]]
        return target_house in kendra_houses

    def planets_in_relative_house(
        self, base_planet: PLANETS_LAGNA, relative_pos: HOUSES
    ) -> PlanetsType:
        """Return list of planets in the nth house from a base planet"""
        base_house = self.get_house_of_planet(base_planet)
        if not base_house:
            return []
        target_house = (base_house + relative_pos - 1) % 12
        target_house = 12 if target_house == 0 else target_house
        return list(self.chart[target_house]["planets"])

    def get_lord_of_house(self, house_number: HOUSES) -> RASHI_LORDS:
        """Return House Lord for give house number"""
        if house_number in self.chart:
            sign = self.chart[house_number]["sign"]
            return RASHI_LORD_MAP.get(sign)
        return None

    def get_rashi_of_house(self, house_number: HOUSES) -> RASHIS:
        """Return Sign of the house"""
        if house_number in self.chart:
            sign = self.chart[house_number]["sign"]
            return sign
        return None

    def relative_house(self, planet1: PLANETS_LAGNA, planet2: PLANETS_LAGNA) -> HOUSES:
        """Return the relative house number of planet2 from planet1"""
        house1 = self.get_house_of_planet(planet1)
        house2 = self.get_house_of_planet(planet2)
        if not house1 or not house2:
            return None
        relative_pos = (house2 - house1) % 12 + 1
        return relative_pos if relative_pos != 0 else 12

    def compute_all(self) -> List[Dict]:
        """Compute all registered yogas"""
        results = []
        for name, func in YOGA_REGISTRY.items():
            result = func(self)
            results.append(result)

        return results
