from vedicastro.VedicAstro import VedicHoroscopeData
from app.utils.chart import ChartGenerator


class AstrologyAgentTools:
    """
    Tools for HoroscopeAgent.
    LLM infers latitude, longitude, and UTC offset based on city name.
    """

    def __init__(self):
        self.horoscope = None
        self.chart_gen = None
        self.ayanamsa = "Lahiri"
        self.house_system = "Whole Sign"

    def _create_horoscope(
        self,
        name: str,
        birth_year: int,
        birth_month: int,
        birth_day: int,
        birth_hour: int,
        birth_minute: int,
        birth_second: int,
        lat: float,
        lng: float,
        utc: float,
    ):
        """Initialize horoscope and chart generator using all parameters."""
        self.horoscope = VedicHoroscopeData(
            year=birth_year,
            month=birth_month,
            day=birth_day,
            hour=birth_hour,
            minute=birth_minute,
            second=birth_second,
            latitude=lat,
            longitude=lng,
            utc=utc,
            ayanamsa=self.ayanamsa,
            house_system=self.house_system,
        )
        self.chart_gen = ChartGenerator(self.horoscope)

    # ====== TOOL METHODS ======

    def get_chart(
        self,
        name: str,
        birth_year: int,
        birth_month: int,
        birth_day: int,
        birth_hour: int,
        birth_minute: int,
        birth_second: int,
        lat: float,
        lng: float,
        utc: float,
        division: str,
    ):
        """
        Generic chart generator.
        The LLM provides city-derived (lat, lng, utc) automatically.
        Example:
            get_chart("Laxman", 2003, 8, 19, 11, 55, 0, 13.08, 80.27, 5.5, "D9")
        """
        self._create_horoscope(
            name,
            birth_year,
            birth_month,
            birth_day,
            birth_hour,
            birth_minute,
            birth_second,
            lat,
            lng,
            utc,
        )
        return self.chart_gen.get_chart(division)

    def get_d1(self, name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, lat, lng, utc):
        self._create_horoscope(name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, lat, lng, utc)
        return self.chart_gen.get_d1()

    def get_d7(self, name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, lat, lng, utc):
        self._create_horoscope(name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, lat, lng, utc)
        return self.chart_gen.get_d7()

    def get_d9(self, name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, lat, lng, utc):
        self._create_horoscope(name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, lat, lng, utc)
        return self.chart_gen.get_d9()

    def get_d10(self, name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, lat, lng, utc):
        self._create_horoscope(name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, lat, lng, utc)
        return self.chart_gen.get_d10()
