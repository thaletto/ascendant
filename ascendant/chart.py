from typing import Dict, List, Tuple
from vedicastro.VedicAstro import RASHIS, VedicHoroscopeData


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

MOVABLE = [0, 3, 6, 9] # Ar, Cn, Li, Cp
FIXED = [1, 4, 7, 10] # Ta, Le, Sc, Aq
DUAL = [2, 5, 8, 11] # Ge, Vi, Sg, Pi

def isSignOdd(n: int) -> bool:
    return n % 2 == 0

class Chart:
    def __init__(self, horoscope: VedicHoroscopeData):
        self.horoscope = horoscope
        self.chart = horoscope.generate_chart()
        self.planets = self.extract_planet_data()
    
    def extract_planet_data(self) -> List[Dict]:
        return [
            {
                "name": planet.id,
                "longitude": planet.lon,
                "is_retrograde": planet.isRetrograde()
            }
            for planet in self.chart.objects
        ]
    
    def _get_divisional_lagna_index(self, division: int) -> int:
        asc = self.chart.getAngle("Asc")
        lon = asc.lon
        target_sign, degree_in_target = self._divisional_target(lon, division)
        return target_sign, degree_in_target

    def _sign_type_start(self, sign_index: int) -> int:
        if sign_index in self.MOVABLE:
            return sign_index
        if sign_index in self.FIXED:
            return (sign_index + 8) % 12  # 9th from itself
        if sign_index in self.DUAL:
            return (sign_index + 4) % 12  # 5th from itself
        return sign_index

    def _divisional_target(self, longitude: float, division: int) -> Tuple[int, float]:
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
            target_sign = (sign_index + part_index) % 12
        
        # =====D3=====
        elif division == 3:
            if part_index == 0:
                target_sign = sign_index
            elif part_index == 1:
                target_sign = (sign_index + 4) % 12
            else:
                target_sign = (sign_index + 8) % 12
        
        # =====D4=====
        elif division == 4:
            offsets = [0, 3, 6, 9]
            target_sign = (sign_index + offsets[part_index]) % 12
        
        elif division == 7:
            if isSignOdd(sign_index):
                target_sign = (sign_index + part_index) % 12
            else:
                target_sign = (sign_index + 6 + part_index) % 12
        
        elif division == 9:
            if sign_index in MOVABLE:
                start = sign_index
            elif sign_index in FIXED:
                start = (sign_index + 8) % 12 # 9th from it.
            else:
                start = (sign_index + 4) % 12 # 5th from it.
            target_sign = (start + part_index) % 12
        
        elif division == 10:
            if isSignOdd(sign_index):
                start = sign_index
            else:
                start = (sign_index + 8) % 12
            target_sign = (start + part_index) % 12
        
        elif division == 12:
            target_sign = (sign_index + part_index) % 12
        
        elif division == 16:
            if sign_index in MOVABLE:
                start = 0
            elif sign_index in FIXED:
                start = 4
            else:
                start = 8
            target_sign = (start + part_index) % 12
        
        elif division == 20:
            if sign_index in MOVABLE:
                start = 0  # Ar
            elif sign_index in FIXED:
                start = 8  # Sg
            else:
                start = 4  # Le
            target_sign = (start + part_index) % 12

        # ---- D24 ChaturVimsamsa ----
        elif division == 24:
            if sign_index % 2 == 0:  # odd signs
                start = 4  # Leo
            else:
                start = 3  # Cancer
            target_sign = (start + part_index) % 12

        # ---- D27 SaptaVimsamsa ----
        elif division == 27:
            if sign_index in [0, 4, 8]:  # fiery
                start = 0
            elif sign_index in [1, 5, 9]:  # earthy
                start = 3
            elif sign_index in [2, 6, 10]:  # airy
                start = 6
            else:  # watery
                start = 9
            target_sign = (start + part_index) % 12

        # ---- D30 Trimsamsa ----
        elif division == 30:
            if sign_index % 2 == 0:  # odd sign index (0-based = odd zodiac)
                # Odd signs: Mars–Sat–Jup–Merc–Ven
                if pos_in_sign < 5:
                    target_sign = 0  # Aries
                elif pos_in_sign < 10:
                    target_sign = 10  # Aquarius
                elif pos_in_sign < 18:
                    target_sign = 8  # Sagittarius
                elif pos_in_sign < 25:
                    target_sign = 2  # Gemini
                else:
                    target_sign = 6  # Libra
            else:
                # Even signs: Ven–Merc–Jup–Sat–Mars
                if pos_in_sign < 5:
                    target_sign = 1  # Taurus
                elif pos_in_sign < 12:
                    target_sign = 5  # Virgo
                elif pos_in_sign < 20:
                    target_sign = 11  # Pisces
                elif pos_in_sign < 25:
                    target_sign = 9  # Capricorn
                else:
                    target_sign = 7  # Scorpio

        # ---- D40 KhaVedamsa ----
        elif division == 40:
            start = 0 if sign_index % 2 == 0 else 6  # odd→Ar, even→Li
            target_sign = (start + part_index) % 12

        # ---- D45 AkshaVedamsa ----
        elif division == 45:
            if sign_index in MOVABLE:
                start = 0  # Aries
            elif sign_index in FIXED:
                start = 4  # Leo
            else:
                start = 8  # Sagittarius
            target_sign = (start + part_index) % 12

        # ---- D60 Shastiamsa ----
        elif division == 60:
            target_sign = (sign_index + part_index) % 12

        return target_sign, degree_in_target
    
    def generate_varga_chart(self, division: int) -> dict:
        chart_data = {}

        # Get Lagna details
        asc_target_sign, asc_degree_in_target = self._get_divisional_lagna_index(division)
        asc_deg = int(asc_degree_in_target)
        asc_minutes = (asc_degree_in_target % 1) * 60
        asc_deg_float = round(asc_deg + asc_minutes / 60, 2)
        asc_div_lon = (asc_target_sign * 30) + asc_deg_float
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
            if name not in self.SELECTED_PLANETS:
                continue

            lon = planet["longitude"]
            target_sign, degree_in_target = self._divisional_target(lon, division)

            house_number = ((target_sign - asc_target_sign) % 12) + 1
            display_name = self.NODE_MAP.get(name, name)

            deg = int(degree_in_target)
            minutes = (degree_in_target % 1) * 60
            deg_float = round(deg + minutes / 60, 2)
            div_lon = round((target_sign * 30) + deg_float, 2)
            rl_nl_data = self.horoscope.get_rl_nl_sl_data(div_lon)

            house_key = f"house_{house_number}"
            if house_key not in chart_data:
                chart_data[house_key] = {
                    "sign": RASHIS[target_sign],
                    "planets": {},
                }

            chart_data[house_key]["planets"][display_name] = {
                "longitude": div_lon,
                "retrograde": planet["is_retrograde"],
                "rashi_lord": rl_nl_data["RasiLord"],
                "nakshatra": rl_nl_data["Nakshatra"],
                "nakshatra_lord": rl_nl_data["NakshatraLord"],
                "pada": rl_nl_data["Pada"],
            }

        return chart_data
