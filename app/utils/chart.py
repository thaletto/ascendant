from typing import Dict, List, Tuple
from vedicastro.VedicAstro import VedicHoroscopeData, RASHIS
from tabulate import tabulate


class ChartGenerator:
    """
    ChartGenerator handles generation of divisional charts (D1-D24)
    using an existing VedicHoroscopeData object.

    It uses the planetary longitudes from D1 and applies the standard
    Varga division rules to calculate new sign placements for each division.
    """

    DIVISION_RANGES = {
        "D1": 1,
        "D2": 2,  # Hora
        "D3": 3,  # Drekkana
        "D4": 4,  # Chaturthamsha
        "D7": 7,  # Saptamsha
        "D9": 9,  # Navamsha
        "D10": 10,  # Dasamsha
        "D12": 12,  # Dwadashamsha
        "D16": 16,  # Shodashamsha
        "D20": 20,  # Vimsamsha
        "D24": 24,  # Chaturvimshamsha
    }

    SELECTED_PLANETS = [
        "Sun",
        "Moon",
        "Mars",
        "Mercury",
        "Jupiter",
        "Venus",
        "Saturn",
        "North Node",
        "South Node",
    ]

    NODE_MAP = {"North Node": "Rahu", "South Node": "Ketu"}

    MOVABLE = {0, 3, 6, 9}  # Aries, Cancer, Libra, Capricorn
    FIXED = {1, 4, 7, 10}  # Taurus, Leo, Scorpio, Aquarius
    DUAL = {2, 5, 8, 11}  # Gemini, Virgo, Sagittarius, Pisces

    def __init__(self, horoscope: VedicHoroscopeData):
        self.horoscope = horoscope
        self.chart = horoscope.generate_chart()
        self.planets = self._extract_planet_data()

    # ----------------------------------------------------------
    # INTERNAL HELPERS
    # ----------------------------------------------------------
    def _extract_planet_data(self) -> List[Dict]:
        """Extract planet data."""
        return [
            {
                "name": planet.id,
                "longitude": planet.lon,
                "is_retrograde": planet.isRetrograde(),
            }
            for planet in self.chart.objects
        ]

    def _get_divisional_lagna_index(self, division: int) -> int:
        asc = self.chart.getAngle("Asc")
        lon = asc.lon
        target_sign, degree_in_target = self._divisional_target(lon, division)
        return target_sign, degree_in_target

    def _sign_type_start(self, sign_index: int) -> int:
        """
        Return the sign-index that is the *first* part's mapped sign for a Rashi
        when dividing it into 'division' parts (the base for part_index=0).
        """
        if sign_index in self.MOVABLE:
            return sign_index
        if sign_index in self.FIXED:
            return (sign_index + 8) % 12  # 9th from itself
        if sign_index in self.DUAL:
            return (sign_index + 4) % 12  # 5th from itself
        # fallback
        return sign_index

    def _divisional_target(self, longitude: float, division: int) -> Tuple[int, float]:
        """
        Given absolute longitude (0..360) and division (e.g., 9 for Navamsa),
        returns (target_sign_index, degree_in_target_sign)
        degree_in_target_sign is 0..30 (float)
        """
        sign_index = int(longitude // 30)  # 0..11
        pos_in_sign = longitude % 30  # 0..30
        part_size = 30.0 / division  # size of each part
        part_index = int(pos_in_sign // part_size)  # which part (0..division-1)
        offset_in_part = pos_in_sign - (part_index * part_size)
        fraction_within_part = offset_in_part / part_size  # 0..1

        # find the starting sign for the 1st part
        if division != 1:
            start_sign = self._sign_type_start(sign_index)
        else:
            start_sign = sign_index

        # target sign mapped by adding part_index (always forward order)
        target_sign = (start_sign + part_index) % 12

        # degree inside the target sign:
        # fraction within the part scaled to full 30° of the target rashi
        degree_in_target = fraction_within_part * 30.0

        return target_sign, degree_in_target

    # ----------------------------------------------------------
    # CORE FUNCTION
    # ----------------------------------------------------------
    def _generate_divisional_chart(self, division: int) -> str:
        table_data = []
        asc_target_sign, asc_degree_in_target = self._get_divisional_lagna_index(
            division
        )

        for planet in self.planets:
            name = planet["name"]
            if name not in self.SELECTED_PLANETS:
                continue

            lon = planet["longitude"]
            target_sign, degree_in_target = self._divisional_target(lon, division)

            house_number = ((target_sign - asc_target_sign) % 12) + 1
            display_name = self.NODE_MAP.get(name, name)

            deg = int(degree_in_target)
            minutes = (degree_in_target % 1) * 60
            deg_float = round(deg + minutes / 60, 2)  # e.g., 123.45
            div_lon = (target_sign * 30) + deg_float
            rl_nl_data = self.horoscope.get_rl_nl_sl_data(div_lon)

            table_data.append(
                [
                    display_name,
                    RASHIS[target_sign],
                    f"House {house_number}",
                    "Yes" if planet["is_retrograde"] else "",
                    rl_nl_data["RasiLord"],
                    rl_nl_data["Nakshatra"],
                    rl_nl_data["NakshatraLord"],
                    rl_nl_data["Pada"],
                ]
            )

        # Add Lagna row on top — show asc degree inside its Dn sign as well
        asc_deg = int(asc_degree_in_target)
        asc_minutes = (asc_degree_in_target % 1) * 60
        asc_deg_float = round(asc_deg + asc_minutes / 60, 2)  # e.g., 123.45
        asc_div_lon = (asc_target_sign * 30) + asc_deg_float
        asc_rl_nl_data = self.horoscope.get_rl_nl_sl_data(asc_div_lon)

        table_data.insert(
            0,
            [
                "Lagna",
                RASHIS[asc_target_sign],
                "House 1",
                "",
                asc_rl_nl_data["RasiLord"],
                asc_rl_nl_data["Nakshatra"],
                asc_rl_nl_data["NakshatraLord"],
                asc_rl_nl_data["Pada"],
            ],
        )

        return tabulate(
            table_data,
            headers=[
                "Body",
                f"D{division} Sign",
                "House",
                "Retrograde",
                "Rashi Lord",
                "Nakshatra",
                "Nakshatra Lord",
                "Nakshatra Pada",
            ],
            tablefmt="simple",
        )

    # ----------------------------------------------------------
    # PUBLIC INTERFACE
    # ----------------------------------------------------------
    def get_chart(self, division_name: str) -> Dict[str, Dict]:
        """
        Generalized access method.
        Example: get_chart("D7") or get_chart("D9")
        """
        if division_name.upper() not in self.DIVISION_RANGES:
            raise ValueError(f"Unsupported chart name: {division_name}")
        division = self.DIVISION_RANGES[division_name]
        return self._generate_divisional_chart(division)

    # Convenience aliases
    def get_d1(self):
        return self.get_chart("D1")

    def get_d7(self):
        return self.get_chart("D7")

    def get_d9(self):
        return self.get_chart("D9")

    def get_d10(self):
        return self.get_chart("D10")
