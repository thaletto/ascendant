from ascendant.chart import Chart
from ascendant.configuration import (
    AscendantConfig,
    Ayanamsa,
    HouseSystem,
    configure,
    get_config,
    parse_ayanamsa as _parse_ayanamsa,
    parse_house_system as _parse_house_system,
    reset_config,
)
from ascendant.dasha import Dasha
from ascendant.horoscope import HoroscopeData
from ascendant.sav import Ashtakavarga, AshtakavargaResult
from ascendant.types import ALLOWED_DIVISIONS
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
        ayanamsa: Ayanamsa | str | None = None,
        house_system: HouseSystem | str | None = None,
    ):
        config = get_config()
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
            ayanamsa=_parse_ayanamsa(
                config.ayanamsa if ayanamsa is None else ayanamsa
            ),
            house_system=_parse_house_system(
                config.house_system
                if house_system is None
                else house_system
            ),
        )

        self.chart_module: Chart = Chart(self.horoscope_data)
        self.yoga_module: Yoga = Yoga(self.horoscope_data)
        self.dasha_module: Dasha = Dasha(self.horoscope_data)
        self.ashtakavarga_module: Ashtakavarga = Ashtakavarga(
            self.horoscope_data
        )

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
        # Reuse the first indexed period as the current-period helper.
        mahadasha = self.dasha_module.get_mahadasha_by_index(0, date)
        antardasha = self.dasha_module.get_antardasha_by_index(0, date)

        return {"mahadasha": mahadasha, "antardasha": antardasha}

    def get_sav(self) -> AshtakavargaResult:
        """Return the complete Ashtakavarga result."""
        return self.ashtakavarga_module.calculate()
