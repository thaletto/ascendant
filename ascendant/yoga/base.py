from typing import Callable, Dict, List, Tuple
from vedicastro.VedicAstro import VedicHoroscopeData
from ascendant.types import (
    HOUSES,
    PLANET_SIGN_RELATION,
    PLANETS_LAGNA,
    RASHI_LORDS,
    RASHIS,
    LagnaType,
    PlanetType,
    PlanetsType,
    YogaType,
)
from ascendant.const import RASHI_LORD_MAP, MALEFIC_PLANETS
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


def register_yogas(*names: str):
    def decorator(
        func: Callable[["Yoga"], Dict[str, YogaType]],
    ) -> Callable[["Yoga"], Dict[str, YogaType]]:
        # Register each yoga name
        for name in names:
            # Create a closure to capture the name properly
            def make_wrapper(yoga_name: str):
                def wrapper(yoga: "Yoga") -> YogaType:
                    results = func(yoga)
                    if yoga_name not in results:
                        # Return default if yoga name not found
                        return {
                            "id": yogaNameToId(yoga_name),
                            "name": yoga_name,
                            "present": False,
                            "strength": 0.0,
                            "details": f"Yoga {yoga_name} not found in results",
                            "type": "Positive",
                        }
                    result = results[yoga_name]
                    result["id"] = yogaNameToId(yoga_name)
                    return result

                return wrapper

            YOGA_REGISTRY[name] = make_wrapper(name)
        return func

    return decorator


class Yoga:
    def __init__(self, horoscope: VedicHoroscopeData):
        from ascendant.chart import Chart

        self.__chart__ = Chart(horoscope)
        self.chart = self.__chart__.get_rasi_chart()

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

    def planet_in_trikona_from(self, base_house: HOUSES, target_planet: PLANETS_LAGNA):
        """Check if a planet is in Trikona (1, 5, 9) from a reference house"""
        target_house = self.get_house_of_planet(target_planet)
        if not target_house:
            return False
        kendra_houses = [(base_house + i - 1) % 12 for i in [1, 5, 9]]
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

    def get_lord_of_planet(self, planet: PLANETS_LAGNA) -> RASHI_LORDS:
        """Return House Lord of the Planet"""
        planet_house = self.get_house_of_planet(planet)
        house_lord = self.get_lord_of_house(planet_house)
        return house_lord

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

    def get_planet_by_name(
        self, planet: PLANETS_LAGNA
    ) -> PlanetType | LagnaType | None:
        if planet == "Lagna":
            for house, data in self.chart.items():
                Lagna = data["lagna"]
                return Lagna
        else:
            for house, data in self.chart.items():
                planets = data["planets"]
                for _planet in planets:
                    if _planet["name"] == planet:
                        return _planet
        return None

    def isPlanetPowerful(self, planet: PlanetType) -> Tuple[bool, float]:
        """Checks if a planet in the chart is powerful"""
        relation = planet.get("inSign")
        name = planet.get("name")
        if not relation or not name:
            return False, 0.0

        strength_map: Dict[PLANET_SIGN_RELATION, float] = {
            "Exalted": 1.0,
            "Moola Trikona": 0.85,
            "Own": 0.7,
            "Friend": 0.5,
        }

        is_powerful = False
        strength = 0.0

        relations: List[PLANET_SIGN_RELATION]
        if isinstance(relation, str):
            relations = [relation]
        else:
            relations = list(relation)

        for relation_status in relations:
            if relation_status not in strength_map:
                continue

            if relation_status == "Friend":
                # Only powerful if Friend and also in kendra from Lagna (house 1)
                in_kendra = self.planet_in_kendra_from(1, name)
                if not in_kendra:
                    continue

            is_powerful = True
            strength = max(strength, strength_map[relation_status])

        return is_powerful, strength

    def is_planet_unafflicted(self, planet: PlanetType, planet_house: HOUSES) -> bool:
        """
        Check if a benefic planet is unafflicted.
        A planet is unafflicted if:
        - It's not debilitated
        - It's not in enemy sign
        - It's not aspected by malefics
        """

        if any(status in planet["inSign"] for status in ["Debilitated", "Enemy"]):
            return False

        # Check if aspected by malefics
        chart = self.__chart__
        for malefic in MALEFIC_PLANETS:
            try:
                malefic_aspects = chart.graha_drishti(n=1, planet=malefic)
                if malefic_aspects:
                    aspect_data = malefic_aspects[0]
                    aspect_houses = aspect_data.get("aspect_houses", [])

                    for house_dict in aspect_houses:
                        if planet_house in house_dict:
                            return False
            except (KeyError, IndexError, TypeError):
                continue

        return True

    def compute_all(self) -> List[Dict]:
        """Compute all registered yogas"""
        results = []
        for name, func in YOGA_REGISTRY.items():
            result = func(self)
            results.append(result)

        return results
