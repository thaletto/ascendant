from ascendant.chart import Chart
from ascendant.configuration import (
    AscendantConfig,
    Ayanamsa,
    HouseSystem,
    configure,
    get_config,
    reset_config,
)
from ascendant.configuration import (
    parse_ayanamsa as _parse_ayanamsa,
)
from ascendant.configuration import (
    parse_house_system as _parse_house_system,
)
from ascendant.dasha import Dasha
from ascendant.horoscope import HoroscopeData
from ascendant.sav import Ashtakavarga, AshtakavargaResult
from ascendant.types import ALLOWED_DIVISIONS, ChartType
from ascendant.yoga.base import Yoga

__all__ = [
    "Ascendant",
    "AscendantConfig",
    "Ayanamsa",
    "HouseSystem",
    "configure",
    "get_config",
    "reset_config",
]


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

        ephemeris = self.horoscope_data.generate_chart()
        self.chart_module: Chart = Chart.from_ephemeris(
            self.horoscope_data,
            ephemeris,
        )
        self.yoga_module: Yoga = Yoga.from_chart(self.chart_module)
        self.dasha_module: Dasha = Dasha.from_ephemeris(
            self.horoscope_data,
            ephemeris,
        )
        self.ashtakavarga_module: Ashtakavarga = (
            Ashtakavarga.from_ephemeris(ephemeris)
        )

    def get_chart(self, division: ALLOWED_DIVISIONS) -> ChartType:
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
        return self.dasha_module.timeline.current(date)

    def get_sav(self) -> AshtakavargaResult:
        """Return the complete Ashtakavarga result."""
        return self.ashtakavarga_module.calculate()
