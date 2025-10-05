# utils/planets.py

from vedicastro.VedicAstro import VedicHoroscopeData
from typing import List, Dict
from tabulate import tabulate

class PlanetaryAspects:
    """
    Class to fetch and process planetary aspects from a Vedic horoscope,
    returning results in a tabular format using tabulate.
    """

    def __init__(self, horoscope: VedicHoroscopeData):
        self.horoscope = horoscope
        self.chart = horoscope.generate_chart()
        self._aspects: List[Dict] = []

    def fetch_aspects(self) -> List[Dict]:
        """Fetch planetary aspects from the horoscope."""
        self._aspects = self.horoscope.get_planetary_aspects(self.chart)
        return self._aspects

    def _format_table_data(self, aspects: List[Dict]) -> List[List]:
        """Convert aspects list to a 2D list suitable for tabulate."""
        return [[a["P1"], a["P2"], a["AspectType"]] for a in aspects]

    def get_aspects_table(self) -> str:
        """Return all aspects as a formatted table string."""
        if not self._aspects:
            self.fetch_aspects()
        table_data = self._format_table_data(self._aspects)
        return tabulate(table_data, headers=["Planet 1", "Planet 2", "AspectType"], tablefmt="simple_grid")

    def filter_by_planets(self, planets: List[str]) -> str:
        """Return aspects where either planet matches the provided list, formatted as table."""
        if not self._aspects:
            self.fetch_aspects()
        filtered = [
            a for a in self._aspects if a["P1"] in planets or a["P2"] in planets
        ]
        table_data = self._format_table_data(filtered)
        return tabulate(table_data, headers=["Planet 1", "Planet 2", "AspectType"], tablefmt="simple_grid")

    def filter_by_aspect_type(self, aspect_types: List[str]) -> str:
        """Return aspects that match the specified aspect types, formatted as table."""
        if not self._aspects:
            self.fetch_aspects()
        filtered = [a for a in self._aspects if a["AspectType"] in aspect_types]
        table_data = self._format_table_data(filtered)
        return tabulate(table_data, headers=["Planet 1", "Planet 2", "AspectType"], tablefmt="simple_grid")
