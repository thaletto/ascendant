from typing import Dict, List
from vedicastro.VedicAstro import VedicHoroscopeData

from ascendant import ALLOWED_DIVISIONS

from .chart import Chart


class Planets:
    def __init__(self, horoscope: VedicHoroscopeData):
        self.horoscope = horoscope
        self.chart = Chart(horoscope)

    def _get_varga_chart(self, division: int) -> dict:
        """Return the generated varga chart for the given division."""
        return self.chart.generate_varga_chart(division)

    def _planet_house_map(self, division: int) -> Dict[str, int]:
        """Return mapping of planet display name -> house number (1..12).

        Planet names follow display in Chart (e.g., Rahu, Ketu).
        """
        varga = self._get_varga_chart(division)
        planet_to_house: Dict[str, int] = {}
        for house_idx in range(1, 13):
            house_key = f"house_{house_idx}"
            if house_key not in varga:
                continue
            for pname in varga[house_key].get("planets", {}).keys():
                if pname.lower() in ("lagna", "ketu"):
                    continue
                planet_to_house[pname] = house_idx
        return planet_to_house

    def _house_sign_map(self, division: int = 1) -> Dict[int, str]:
        """Return mapping of house number -> sign label for a given division.

        Defaults to D1 when no division is provided.
        """
        varga = self._get_varga_chart(division)
        return {
            i: varga[f"house_{i}"]["sign"]
            for i in range(1, 13)
            if f"house_{i}" in varga
        }

    def _aspect_offsets_for_planet(self, planet_name: str) -> List[int]:
        # Everyone aspects 7th
        offsets: List[int] = [7]
        p = planet_name.lower()
        if p == "mars":
            offsets += [4, 8]
        elif p == "jupiter" or p == "rahu":
            offsets += [5, 9]
        elif p == "saturn":
            offsets += [3, 10]
        return offsets

    def graha_drishthi(self, division: int = 1) -> Dict[str, Dict[str, object]]:
        """Compute graha drishti (planetary aspects) for the given division.

        Returns:
            Mapping of planet -> { from_house, aspects: [houses], aspect_planets: {house: [planets]} }
        """
        if division not in ALLOWED_DIVISIONS:
            raise ValueError(
                f"Unsupported division '{division}'. Allowed divisions: {ALLOWED_DIVISIONS}"
            )

        varga = self._get_varga_chart(division)
        planet_to_house = self._planet_house_map(division)

        results: Dict[str, Dict[str, object]] = {}
        for planet_name, from_house in planet_to_house.items():
            aspect_houses: List[int] = []
            for offset in self._aspect_offsets_for_planet(planet_name):
                target_house = (from_house - 1 + offset) % 12
                aspect_houses.append(target_house)

            aspect_planets: Dict[int, List[str]] = {}
            for h in aspect_houses:
                hk = f"house_{h}"
                plist = list(varga.get(hk, {}).get("planets", {}).keys())
                aspect_planets[h] = plist

            results[planet_name] = {
                "from_house": from_house,
                "aspects": aspect_houses,
                "aspect_planets": aspect_planets,
            }

        return results

    # Convenience alias for clarity
    def aspects_for(self, division: int = 1) -> Dict[str, Dict[str, object]]:
        """Alias for graha_drishthi to fetch aspects for a division."""
        return self.graha_drishthi(division=division)
