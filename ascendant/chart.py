from typing import Dict, List, Tuple
from vedicastro.VedicAstro import RASHIS, VedicHoroscopeData

from ascendant import ALLOWED_DIVISIONS, FIXED, MOVABLE, NODE_MAP, SELECTED_PLANETS, isSignOdd


class Chart:
    """Represents the birth chart and divisional charts.

    Args:
        horoscope: `VedicHoroscopeData`
    """

    def __init__(self, horoscope: VedicHoroscopeData):
        self.horoscope = horoscope
        self.chart = horoscope.generate_chart()
        self.planets = self._extract_planet_data()

    def _extract_planet_data(self) -> List[Dict]:
        """Extract planet identification, longitude, and retrograde state.

        Returns:
            A list of dictionaries, one per planet in the base chart, with
            keys `name`, `longitude`, and `is_retrograde`.
        """
        return [
            {
                "name": planet.id,
                "longitude": planet.lon,
                "is_retrograde": planet.isRetrograde(),
            }
            for planet in self.chart.objects
        ]

    def _get_divisional_lagna(self, division: int) -> int:
        """Compute the lagna mapping for the specified division.

        Args:
            division: The varga division (e.g., 1 for D1, 9 for D9).

        Returns:
            A tuple ``(target_sign_index, degree_in_target_sign)`` where
            ``target_sign_index`` is 0..11 and ``degree_in_target_sign`` is 0..30.
        """
        asc = self.chart.getAngle("Asc")
        lon = asc.lon
        target_sign, degree_in_target = self._divisional_target(lon, division)
        return target_sign, degree_in_target

    def _divisional_target(self, longitude: float, division: int) -> Tuple[int, float]:
        """Map an absolute longitude into a target sign/degree for a varga.

        This routine contains specific mapping rules for commonly used vargas
        (D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60).
        For D1, a fast path returns the natal sign and intra-sign degree.

        Args:
            longitude: Absolute ecliptic longitude in degrees (0..360).
            division: The varga division number (e.g., 1, 9, 10, ...).

        Returns:
            A tuple ``(target_sign_index, degree_in_target_sign)`` where
            ``target_sign_index`` is 0..11 and ``degree_in_target_sign`` is 0..30.
        """
        # Fast path for D1: target sign is the natal sign and degree is within that sign
        if division == 1:
            sign_index = int(longitude // 30)
            degree_in_target = longitude % 30
            return sign_index, degree_in_target

        sign_index = int(longitude // 30)  # 0..11
        pos_in_sign = longitude % 30  # 0..30
        part_size = 30.0 / division  # size of each part
        part_index = int(pos_in_sign // part_size)  # which part (0..division-1)
        offset_in_part = pos_in_sign - (part_index * part_size)
        degree_in_target = (offset_in_part / part_size) * 30.0

        # Default target sign, same as D1
        target_sign = sign_index

        # =====D2=====
        if division == 2:
            if sign_index <= 5:
                target_sign = sign_index * 2 + part_index
            else:
                target_sign = (sign_index - 6) * 2 + part_index

        # =====D3=====
        elif division == 3:
            offsets = [0, 4, 8]
            target_sign = (sign_index + offsets[part_index]) % 12

        # =====D4=====
        elif division == 4:
            offsets = [0, 3, 6, 9]
            target_sign = (sign_index + offsets[part_index]) % 12

        # =====D7=====
        elif division == 7:
            if isSignOdd(sign_index):
                target_sign = (sign_index + part_index) % 12
            else:
                target_sign = (
                    sign_index + 6 + part_index
                ) % 12  # Starts from 7th sign from it

        # =====D9=====
        elif division == 9:
            division_start = {
                "movable": lambda idx: idx,
                "fixed": lambda idx: (idx + 8) % 12,
                "dual": lambda idx: (idx + 4) % 12,
            }
            if sign_index in MOVABLE:
                sign_type = "movable"
            elif sign_index in FIXED:
                sign_type = "fixed"
            else:
                sign_type = "dual"
            start = division_start[sign_type](sign_index)
            target_sign = (start + part_index) % 12

        # =====D10=====
        elif division == 10:
            start = sign_index if isSignOdd(sign_index) else (sign_index + 8) % 12
            target_sign = (start + part_index) % 12

        # =====D12=====
        elif division == 12:
            target_sign = (sign_index + part_index) % 12

        # =====D16=====
        elif division == 16:
            start_sign_map = {
                "movable": 0,  # Ar
                "fixed": 4,  # Le
                "dual": 8,  # Sg
            }
            if sign_index in MOVABLE:
                sign_type = "movable"
            elif sign_index in FIXED:
                sign_type = "fixed"
            else:
                sign_type = "dual"
            start = start_sign_map[sign_type]
            target_sign = (start + part_index) % 12

        # =====D20=====
        elif division == 20:
            start_sign_map = {
                "movable": 0,  # Ar
                "fixed": 8,  # Sg
                "dual": 4,  # Le
            }
            if sign_index in MOVABLE:
                sign_type = "movable"
            elif sign_index in FIXED:
                sign_type = "fixed"
            else:
                sign_type = "dual"
            start = start_sign_map[sign_type]
            target_sign = (start + part_index) % 12

        # =====D24=====
        elif division == 24:
            if isSignOdd(sign_index):  # odd signs
                start = 4  # Le
            else:
                start = 3  # Cn
            target_sign = (start + part_index) % 12

        # =====D27=====
        elif division == 27:
            if sign_index in [0, 4, 8]:  # fiery
                start = 0  # Ar
            elif sign_index in [1, 5, 9]:  # earthy
                start = 3  # Cn
            elif sign_index in [2, 6, 10]:  # airy
                start = 6  # Li
            else:  # watery
                start = 9  # Cp
            target_sign = (start + part_index) % 12

        # =====D30=====
        elif division == 30:
            # Trimsamsa: map pos_in_sign to target_sign via table for odd/even signs
            if isSignOdd(sign_index):  # odd sign index
                # Ma–Sa–Ju–Me–Ve -> [Ar, Aq, Sg, Ge, Li]
                targets = [0, 10, 8, 2, 6]
                edges = [5, 10, 18, 25]
            else:
                # Ve–Me–Ju–Sa–Ma -> [Ta, Vi, Pi, Cp, Sc]
                targets = [1, 5, 11, 9, 7]
                edges = [5, 12, 20, 25]
            for i, edge in enumerate(edges):
                if pos_in_sign < edge:
                    target_sign = targets[i]
                    break
            else:
                target_sign = targets[-1]

        # =====D40=====
        elif division == 40:
            start = 0 if isSignOdd(sign_index) else 6  # odd -> Ar, even -> Li
            target_sign = (start + part_index) % 12

        # =====D45=====
        elif division == 45:
            start_sign_map = {
                "movable": 0,  # Ar
                "fixed": 4,  # Le
                "dual": 8,  # Sg
            }
            if sign_index in MOVABLE:
                sign_type = "movable"
            elif sign_index in FIXED:
                sign_type = "fixed"
            else:
                sign_type = "dual"
            start = start_sign_map[sign_type]
            target_sign = (start + part_index) % 12

        # =====D60=====
        elif division == 60:
            target_sign = (sign_index + part_index) % 12

        return target_sign, degree_in_target

    def generate_varga_chart(self, division: int) -> dict:
        """Generate a simple divisional chart representation for the given varga.

        The result is a dictionary keyed by ``house_1``..``house_12``. Each
        entry includes the sign label and a nested mapping of placed bodies
        (Lagna and selected planets), with additional contextual data pulled
        from ``get_rl_nl_sl_data`` at the computed divisional longitudes.

        Args:
            division: The varga division number to generate (e.g., 1, 9, 10).

        Returns:
            A dictionary with house keys containing sign and planet placements.
        """
        if division not in ALLOWED_DIVISIONS:
            raise ValueError(
                f"Unsupported division '{division}'. Allowed divisions: {ALLOWED_DIVISIONS}"
            )

        chart_data = {}

        # Get Lagna details
        asc_target_sign, asc_degree_in_target = self._get_divisional_lagna(division)
        asc_div_lon = (asc_target_sign * 30) + asc_degree_in_target
        asc_rl_nl_data = self.horoscope.get_rl_nl_sl_data(asc_div_lon)

        # Insert Lagna into House 1
        chart_data["house_1"] = {
            "sign": RASHIS[asc_target_sign],
            "planets": {
                "lagna": {
                    "longitude": asc_div_lon,
                    "retrograde": False,
                    "rashi_lord": asc_rl_nl_data["RasiLord"],
                    "nakshatra": asc_rl_nl_data["Nakshatra"],
                    "nakshatra_lord": asc_rl_nl_data["NakshatraLord"],
                    "pada": asc_rl_nl_data["Pada"],
                }
            },
        }

        # Loop through planets
        for planet in self.planets:
            name = planet["name"]
            if name not in SELECTED_PLANETS:
                continue

            lon = planet["longitude"]
            target_sign, degree_in_target = self._divisional_target(lon, division)

            house_number = ((target_sign - asc_target_sign) % 12) + 1
            display_name = NODE_MAP.get(name, name)

            div_lon = (target_sign * 30) + degree_in_target
            rl_nl_data = self.horoscope.get_rl_nl_sl_data(div_lon)

            house_key = f"house_{house_number}"
            if house_key not in chart_data:
                chart_data[house_key] = {
                    "sign": RASHIS[target_sign],
                    "planets": {},
                }

            chart_data[house_key]["planets"][display_name] = {
                "longitude": div_lon,
                "degree": degree_in_target,
                "retrograde": planet["is_retrograde"],
                "rashi_lord": rl_nl_data["RasiLord"],
                "nakshatra": rl_nl_data["Nakshatra"],
                "nakshatra_lord": rl_nl_data["NakshatraLord"],
                "pada": rl_nl_data["Pada"],
            }

        return chart_data
