from collections.abc import Callable
from typing import TYPE_CHECKING, cast

from ascendant.const import BENEFIC_PLANETS, MALEFIC_PLANETS, RASHI_LORD_MAP
from ascendant.horoscope import HoroscopeData
from ascendant.types import (
    HOUSES,
    PLANET_SIGN_RELATION,
    PLANETS_LAGNA,
    RASHI_LORDS,
    RASHIS,
    ChartType,
    LagnaType,
    PlanetsType,
    PlanetType,
    YogaType,
)
from ascendant.utils import yoga_name_to_id

if TYPE_CHECKING:
    from ascendant.chart import Chart

YogaFunction = Callable[["Yoga"], YogaType]

YOGA_REGISTRY: dict[str, YogaFunction] = {}


def register_yoga(name: str) -> Callable[[YogaFunction], YogaFunction]:
    def decorator(func: YogaFunction) -> YogaFunction:
        def wrapper(yoga: "Yoga") -> YogaType:
            result = func(yoga)
            result["id"] = yoga_name_to_id(name)
            return result

        YOGA_REGISTRY[name] = wrapper
        return wrapper

    return decorator


def register_yogas(
    *names: str,
) -> Callable[
    [Callable[["Yoga"], dict[str, YogaType]]],
    Callable[["Yoga"], dict[str, YogaType]],
]:
    def decorator(
        func: Callable[["Yoga"], dict[str, YogaType]],
    ) -> Callable[["Yoga"], dict[str, YogaType]]:
        # Register each yoga name
        for name in names:
            # Create a closure to capture the name properly
            def make_wrapper(yoga_name: str):
                def wrapper(yoga: "Yoga") -> YogaType:
                    results = func(yoga)
                    if yoga_name not in results:
                        # Return default if yoga name not found
                        return {
                            "id": yoga_name_to_id(yoga_name),
                            "name": yoga_name,
                            "present": False,
                            "strength": 0.0,
                            "details": f"Yoga {yoga_name} not found in results",
                            "type": "Positive",
                        }
                    result = results[yoga_name]
                    result["id"] = yoga_name_to_id(yoga_name)
                    return result

                return wrapper

            YOGA_REGISTRY[name] = make_wrapper(name)
        return func

    return decorator


class Yoga:
    def __init__(self, horoscope: HoroscopeData):
        from ascendant.chart import Chart

        self._initialize(Chart(horoscope))

    @classmethod
    def from_chart(cls, chart: "Chart") -> "Yoga":
        yoga = cls.__new__(cls)
        yoga._initialize(chart)
        return yoga

    def _initialize(self, chart: "Chart") -> None:
        self.__chart__: Chart = chart
        self.chart: ChartType = self.__chart__.get_rasi_chart()

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
        raise ValueError(f"Planet {planet} not found.")

    def get_house_of_rashi(self, rashi: RASHIS) -> HOUSES:
        """Returns the house number of Rashi"""
        for house, data in self.chart.items():
            sign = data["sign"]
            if sign == rashi:
                return house
        raise ValueError(f"Rashi {rashi} not found.")

    def planet_in_kendra_from(
        self, base_house: HOUSES, target_planet: PLANETS_LAGNA
    ) -> bool:
        """Check if a planet is in Kendra (1, 4, 7, 10) from a reference house"""
        target_house = self.get_house_of_planet(target_planet)
        kendra_houses = [(base_house + i - 1) % 12 for i in [1, 4, 7, 10]]
        return target_house in kendra_houses

    def planet_in_trikona_from(
        self, base_house: HOUSES, target_planet: PLANETS_LAGNA
    ) -> bool:
        """Check if a planet is in Trikona (1, 5, 9) from a reference house"""
        target_house = self.get_house_of_planet(target_planet)
        kendra_houses = [(base_house + i - 1) % 12 for i in [1, 5, 9]]
        return target_house in kendra_houses

    def planets_in_relative_house(
        self, base_planet: PLANETS_LAGNA, relative_pos: HOUSES
    ) -> PlanetsType:
        """Return list of planets in the nth house from a base planet"""
        base_house = self.get_house_of_planet(base_planet)
        target_house = (base_house + relative_pos - 1) % 12
        target_house = cast(HOUSES, 12 if target_house == 0 else target_house)
        return list(self.chart[target_house]["planets"])

    def get_lord_of_house(self, house_number: HOUSES) -> RASHI_LORDS:
        """Return House Lord for give house number"""
        if house_number in self.chart:
            sign = self.chart[house_number]["sign"]
            return RASHI_LORD_MAP[sign]
        raise ValueError(f"House {house_number} not found.")

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
        raise ValueError(f"House {house_number} not found.")

    def relative_house(
        self, planet1: PLANETS_LAGNA, planet2: PLANETS_LAGNA
    ) -> HOUSES:
        """Return the relative house number of planet2 from planet1"""
        house1 = self.get_house_of_planet(planet1)
        house2 = self.get_house_of_planet(planet2)
        relative_pos = (house2 - house1) % 12 + 1
        pos = cast(HOUSES, relative_pos if relative_pos != 0 else 12)
        return pos

    def get_planet_by_name(
        self, planet: PLANETS_LAGNA
    ) -> PlanetType | LagnaType:
        if planet == "Lagna":
            for data in self.chart.values():
                lagna = data["lagna"]
                if lagna is not None:
                    return lagna
        else:
            for data in self.chart.values():
                planets = data["planets"]
                for _planet in planets:
                    if _planet["name"] == planet:
                        return _planet
        raise ValueError(f"Planet {planet} not found.")

    def is_planet_powerful(self, planet: PlanetType) -> tuple[bool, float]:
        """Checks if a planet in the chart is powerful"""
        relations = planet.get("inSign")
        name = planet.get("name")
        if not relations or not name:
            return False, 0.0

        strength_map: dict[PLANET_SIGN_RELATION, float] = {
            "Exalted": 1.0,
            "Moola Trikona": 0.85,
            "Own": 0.7,
            "Friend": 0.5,
        }

        is_powerful = False
        strength = 0.0

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

    def is_house_benefic_aspected(self, house: HOUSES) -> bool:
        """
        Check if a house is has benefic or aspected by benefic
        """
        for house_, data in self.chart.items():
            if house_ == house:
                planets = data["planets"]
                for planet in planets:
                    if planet["name"] in BENEFIC_PLANETS:
                        if planet["name"] == "Mercury":
                            Me_is_unafflicted = self.is_planet_unafflicted(
                                planet, house_
                            )
                            if Me_is_unafflicted:
                                return True
                            else:
                                continue
                        else:
                            return True

        aspects = self.__chart__.graha_drishti(n=1)
        for aspect in aspects:
            if aspect["planet"] in BENEFIC_PLANETS:
                for aspect_house in aspect["aspect_houses"]:
                    for house_, data in aspect_house.items():
                        if house_ == house:
                            return True

        return False

    def compute_all(self) -> list[YogaType]:
        """Compute all registered yogas"""
        results: list[YogaType] = []
        for func in YOGA_REGISTRY.values():
            result = func(self)
            results.append(result)

        return results
