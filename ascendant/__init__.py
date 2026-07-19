from ascendant.chart import Chart
from ascendant.dasha import Dasha
from ascendant.horoscope import HoroscopeData
from ascendant.types import ALLOWED_DIVISIONS
from ascendant.utils import get_house_system
from ascendant.yoga.base import Yoga


class Ascendant:
    """
    Super class to manage Chart, Yoga, and Dasha calculations.
    """

    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        latitude: float,
        longitude: float,
        utc: str,
        ayanamsa: str = "Lahiri",
        house_system: str = "Whole Sign",
    ):
        self.horoscope_data: HoroscopeData = HoroscopeData(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            utc=utc,
            latitude=latitude,
            longitude=longitude,
            ayanamsa=ayanamsa,
            house_system=get_house_system(house_system),
        )

        self.chart_module: Chart = Chart(self.horoscope_data)
        self.yoga_module: Yoga = Yoga(self.horoscope_data)
        self.dasha_module: Dasha = Dasha(self.horoscope_data)

    def get_chart(self, division: ALLOWED_DIVISIONS):
        """Get the divisional chart."""
        return self.chart_module.get_varga_chakra_chart(division)

    def get_yogas(self):
        """Compute all yogas."""
        return self.yoga_module.compute_all()

    def get_dasha_timeline(self):
        """Get Dasha timeline."""
        return self.dasha_module.get_dasha_timeline()

    def get_current_dasha(self, date: str | None = None):
        """Get current Mahadasha and Antardasha."""
        # This is a helper accessing the internal dasha logic if needed
        # Since logic is in get_antardasha_by_index(0), we can expose similar functionality
        mahadasha = self.dasha_module.get_mahadasha_by_index(0, date)
        antardasha = self.dasha_module.get_antardasha_by_index(0, date)

        return {"mahadasha": mahadasha, "antardasha": antardasha}
