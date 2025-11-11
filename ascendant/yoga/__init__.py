from typing import Dict, Callable, List
from vedicastro.VedicAstro import VedicHoroscopeData
from ascendant.chart import Chart

YOGA_REGISTRY: Dict[str, Callable] = {}


def register_yoga(name: str):
    def decorator(func: Callable):
        YOGA_REGISTRY[name] = func
        return func

    return decorator


class Yoga:
    def __init__(self, horoscope: VedicHoroscopeData):
        self.chart = Chart(horoscope).generate_varga_chart(1)

    def get_house_of_planet(self, planet_name: str) -> int | None:
        """Return house number where planet is located in the chart"""
        planet_name_lower = planet_name.lower()
        for house, data in self.chart.items():
            planets = data.get("planets", {})
            # Case-insensitive comparison
            for planet_key in planets.keys():
                if planet_key.lower() == planet_name_lower:
                    return int(house.split("_")[1])
        return None

    def planet_in_kendra_from(self, base_house: int, target_planet: str) -> bool:
        """Check if a planet is in Kendra (1, 4, 7, 10) from a reference house"""
        target_house = self.get_house_of_planet(target_planet)
        if not target_house:
            return False
        kendra_houses = [(base_house + i - 1) % 12 + 1 for i in [1, 4, 7, 10]]
        return target_house in kendra_houses

    def planets_in_relative_house(self, base_planet: str, relative_pos: int):
        """Return list of planets in the nth house from a base planet"""
        base_house = self.get_house_of_planet(base_planet)
        if not base_house:
            return []
        target_house = (base_house + relative_pos - 1) % 12
        return list(
            self.chart.get(f"house_{target_house}", {}).get("planets", {}).keys()
        )

    def get_lord_of_house(self, house_number: int) -> str:
        """Return House Lord for give house number"""
        for house, data in self.chart.items():
            if house == f'house_{house_number}':
                planets = data.get("planets", {})
                for planet in planets.keys():
                    return planet['rashi_lord']
                    break


    def compute_all(self) -> List[Dict]:
        """Compute all registered yogas"""
        results = []
        for name, func in YOGA_REGISTRY.items():
            result = func(self)
            results.append(result)
        return results
