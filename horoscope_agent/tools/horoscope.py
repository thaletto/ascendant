from vedicastro.VedicAstro import VedicHoroscopeData
from app.utils.chart import ChartGenerator


class AstrologyAgentTools:
    """Utility tools used by the HoroscopeAgent.

    This helper encapsulates creation of a `VedicHoroscopeData` instance and
    exposes convenience methods to compute common divisional charts.

    Available Tools
    ---------------
    - get_chart: Generate a full Vedic horoscope chart using provided birth details (including latitude, longitude, and UTC offset).
    - get_d1: Generate the D1 (Rasi) chart for basic predictions about health, wealth, career, family, partner, and longevity.
    - get_d7: Generate the D7 (Saptamsa) chart for insights related to children and creativity.
    - get_d9: Generate the D9 (Navamsa) chart for deeper analysis of marriage, partnerships, and spiritual growth.
    - get_d10: Generate the D10 (Dasamsa) chart for career and professional life analysis.

    Notes:
    - The caller must provide birth details including geographic coordinates and UTC offset. If only a city name is available, the agent layer should resolve it to latitude, longitude, and UTC offset before calling these methods.
    - Default `ayanamsa` is "Lahiri" and `house_system` is "Whole Sign".
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
        """Initialize horoscope and chart generator using all parameters"""
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
        """Generate any supported divisional chart.

        Parameters
        ----------
        name : str
            Person's name (for context only).
        birth_year : int
            Four-digit year of birth.
        birth_month : int
            Month of birth (1-12).
        birth_day : int
            Day of month.
        birth_hour : int
            Hour of birth (0-23).
        birth_minute : int
            Minute of birth (0-59).
        birth_second : int
            Second of birth (0-59).
        lat : float
            Latitude in decimal degrees.
        lng : float
            Longitude in decimal degrees.
        utc : float
            Timezone offset from UTC in hours.
        division : "D1" | "D2" | "D3" | "D4" | "D7" | "D9" | "D10" | "D12" | "D16" | "D20" | "D24"
            Divisional chart identifier understood by `ChartGenerator`

        Returns
        -------
        dict
            A dictionary with a single key of the form "{division}_chart"
            mapping to the computed chart data structure.
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
        """Compute the D1 (Rasi) chart.

        Returns
        -------
        dict
            Dictionary with key "d1_chart" containing the computed chart data.
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
        """Compute the D7 (Saptamsha) chart.

        Returns
        -------
        dict
            Dictionary with key "d7_chart" containing the computed chart data.
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
        """Compute the D9 (Navamsha) chart.

        Returns
        -------
        dict
            Dictionary with key "d9_chart" containing the computed chart data.
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
        """Compute the D10 (Dasamsha) chart.

        Returns
        -------
        dict
            Dictionary with key "d10_chart" containing the computed chart data.
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
        result = self.chart_gen.get_d10()
        return {"d10_chart": result}
