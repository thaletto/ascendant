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
    ) -> dict:
        """Generic chart generator returning dict for ADK."""
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
        result = self.chart_gen.get_chart(division)
        return {f"{division}_chart": result}  # wrap in dict


    def get_d1(
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
    ) -> dict:
        self._create_horoscope(name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, lat, lng, utc)
        result = self.chart_gen.get_d1()
        return {"d1_chart": result}


    def get_d7(
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
    ) -> dict:
        self._create_horoscope(name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, lat, lng, utc)
        result = self.chart_gen.get_d7()
        return {"d7_chart": result}


    def get_d9(
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
    ) -> dict:
        self._create_horoscope(name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, lat, lng, utc)
        result = self.chart_gen.get_d9()
        return {"d9_chart": result}


    def get_d10(
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
    ) -> dict:
        self._create_horoscope(name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, lat, lng, utc)
        result = self.chart_gen.get_d10()
        return {"d10_chart": result}

