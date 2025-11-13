from typing import List, Tuple
from vedicastro.VedicAstro import RASHIS, VedicHoroscopeData
from ascendant import (
    ALLOWED_DIVISIONS,
    FIXED,
    MOVABLE,
    NODE_MAP,
    SELECTED_PLANETS,
    isSignOdd,
)
from ascendant.types import AllowedDivision, ChartData, LagnaPlacement, PlanetData, PlanetPlacement


class Chart:
    """Represents the birth chart and divisional charts.

    Args:
        horoscope: `VedicHoroscopeData`
    """

    def __init__(self, horoscope: VedicHoroscopeData):
        self.horoscope = horoscope
        self.chart = horoscope.generate_chart()
        self.planets = self._extract_planet_data()

    def _extract_planet_data(self) -> List[PlanetData]:
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

    def _get_divisional_lagna(self, division: AllowedDivision) -> Tuple[int, float]:
        """Compute the lagna mapping for the specified division."""
        asc = self.chart.getAngle("Asc")
        lon: float = asc.lon
        return self._divisional_target(lon, division)

    def _divisional_target(self, longitude: float, division: AllowedDivision) -> Tuple[int, float]:
        """Map an absolute longitude into a target sign/degree for a varga."""
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
            target_sign = (
                (sign_index * 2 + part_index)
                if sign_index <= 5
                else ((sign_index - 6) * 2 + part_index)
            )

        # =====D3=====
        elif division == 3:
            target_sign = (sign_index + [0, 4, 8][part_index]) % 12

        # =====D4=====
        elif division == 4:
            target_sign = (sign_index + [0, 3, 6, 9][part_index]) % 12

        # =====D7=====
        elif division == 7:
            target_sign = (
                (sign_index + part_index) % 12
                if isSignOdd(sign_index)
                else (sign_index + 6 + part_index) % 12
            )

        # =====D9=====
        elif division == 9:
            if sign_index in MOVABLE:
                start = sign_index
            elif sign_index in FIXED:
                start = (sign_index + 8) % 12
            else:
                start = (sign_index + 4) % 12
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
            start = 0 if sign_index in MOVABLE else 4 if sign_index in FIXED else 8
            target_sign = (start + part_index) % 12

        # =====D20=====
        elif division == 20:
            start = 0 if sign_index in MOVABLE else 8 if sign_index in FIXED else 4
            target_sign = (start + part_index) % 12

        # =====D24=====
        elif division == 24:
            start = 4 if isSignOdd(sign_index) else 3
            target_sign = (start + part_index) % 12

        # =====D27=====
        elif division == 27:
            start = (
                0
                if sign_index in [0, 4, 8]
                else 3
                if sign_index in [1, 5, 9]
                else 6
                if sign_index in [2, 6, 10]
                else 9
            )
            target_sign = (start + part_index) % 12

        # =====D30=====
        elif division == 30:
            if isSignOdd(sign_index):
                targets, edges = [0, 10, 8, 2, 6], [5, 10, 18, 25]
            else:
                targets, edges = [1, 5, 11, 9, 7], [5, 12, 20, 25]
            for i, edge in enumerate(edges):
                if pos_in_sign < edge:
                    target_sign = targets[i]
                    break
            else:
                target_sign = targets[-1]

        # =====D40=====
        elif division == 40:
            target_sign = ((0 if isSignOdd(sign_index) else 6) + part_index) % 12

        # =====D45=====
        elif division == 45:
            start = 0 if sign_index in MOVABLE else 4 if sign_index in FIXED else 8
            target_sign = (start + part_index) % 12

        # =====D60=====
        elif division == 60:
            target_sign = (sign_index + part_index) % 12

        return target_sign, degree_in_target

    def generate_varga_chart(self, division: AllowedDivision) -> ChartData:
        """Generate a simple divisional chart representation for the given varga."""
        if division not in ALLOWED_DIVISIONS:
            raise ValueError(
                f"Unsupported division '{division}'. Allowed divisions: {ALLOWED_DIVISIONS}"
            )

        # Get Lagna details
        asc_target_sign, asc_degree_in_target = self._get_divisional_lagna(division)
        asc_div_lon = (asc_target_sign * 30) + asc_degree_in_target
        asc_rl_nl_data = self.horoscope.get_rl_nl_sl_data(asc_div_lon)

        chart_data: ChartData = {}

        # Initialize 12 houses
        for house_num in range(1, 13):
            sign_index = (asc_target_sign + house_num - 1) % 12
            chart_data[f"house_{house_num}"] = {
                "sign": RASHIS[sign_index],
                "planets": {},
            }

        # Lagna in House 1
        chart_data["house_1"]["planets"]["lagna"] = LagnaPlacement(
            longitude=asc_div_lon,
            retrograde=False,
            rashi_lord=asc_rl_nl_data["RasiLord"],
            nakshatra=asc_rl_nl_data["Nakshatra"],
            nakshatra_lord=asc_rl_nl_data["NakshatraLord"],
            pada=asc_rl_nl_data["Pada"],
        )

        # Loop through planets
        for planet in self.planets:
            name = planet["name"]
            if name not in SELECTED_PLANETS:
                continue

            lon = planet["longitude"]
            target_sign, degree_in_target = self._divisional_target(lon, division)
            house_number = ((target_sign - asc_target_sign) % 12) + 1
            display_name = NODE_MAP.get(name, name)

            div_lon = target_sign * 30 + degree_in_target
            rl_nl_data = self.horoscope.get_rl_nl_sl_data(div_lon)

            planet_placement: PlanetPlacement = {
                "longitude": div_lon,
                "degree": degree_in_target,
                "retrograde": planet["is_retrograde"],
                "rashi_lord": rl_nl_data["RasiLord"],
                "nakshatra": rl_nl_data["Nakshatra"],
                "nakshatra_lord": rl_nl_data["NakshatraLord"],
                "pada": rl_nl_data["Pada"],
            }

            chart_data[f"house_{house_number}"]["planets"][display_name] = (
                planet_placement
            )

        return chart_data
