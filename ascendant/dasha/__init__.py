from collections.abc import Sequence
from datetime import datetime, timezone
from typing import Literal, TypedDict

from dateutil.relativedelta import relativedelta
from ascendant.const import NAKSHATRAS, VIMSHOTTARI_PLANETS, VIMSHOTTARI_YEARS
from ascendant.ephemeris import EphemerisChart
from ascendant.horoscope import HoroscopeData
from ascendant.types import AntarDashaType, DashasType, MahaDashaType, PLANETS
from ascendant.utils import parseDate


class _DashaPeriod(TypedDict):
    start: str
    end: str


class _VimshottariMahaDasha(_DashaPeriod):
    bhuktis: dict[PLANETS, _DashaPeriod]


_ChartDate = tuple[int, int, int, int, int]
_DashaTimelineItem = MahaDashaType | AntarDashaType
_VimshottariData = dict[PLANETS, _VimshottariMahaDasha]


class Dasha:
    """Utility class to compute and format Vimshottari Dasha timeline."""

    def __init__(self, horoscope: HoroscopeData):
        """
        Initializes the Dasha utility with a HoroscopeData object.

        Args:
            horoscope: An instance of HoroscopeData containing the birth chart information.
        """
        self.__horoscope__: HoroscopeData = horoscope
        self.__chart__: EphemerisChart = horoscope.generate_chart()

        self.dasha: DashasType = self.get_dasha_timeline()

    def get_dasha_timeline(self) -> DashasType:
        """
        Computes and returns the Vimshottari Dasha timeline.

        Returns:
            A list of MahaDashaType objects, each containing its AntarDashaType sub-periods.
        """
        vhd: _VimshottariData = self._compute_vimshottari_dasa()
        dashas: DashasType = []

        for maha_planet, details in vhd.items():
            bhuktis = details.get("bhuktis", {})

            antardashas: list[AntarDashaType] = []
            maha_start = None
            maha_end = None

            for bhukti_planet, period in bhuktis.items():
                start = period["start"]
                end = period["end"]

                # Set Mahadasha start & end (first bhukti start, last bhukti end)
                if maha_start is None:
                    maha_start = start
                maha_end = end

                antardashas.append(
                    {
                        "mahadasha": maha_planet,
                        "antardasha": bhukti_planet,
                        "start": start,
                        "end": end,
                    }
                )

            # Add Mahadasha entry
            if maha_start and maha_end:
                dashas.append(
                    {
                        "mahadasha": maha_planet,
                        "start": maha_start,
                        "end": maha_end,
                        "antardashas": antardashas,
                    }
                )
        return dashas

    def _compute_vimshottari_dasa(self) -> _VimshottariData:
        moon = self.__chart__.get("Moon")
        moon_data = self.__horoscope__.get_rl_nl_sl_data(moon.lon)
        if moon_data is None:
            return {}

        sequence = VIMSHOTTARI_PLANETS.copy()
        lengths = VIMSHOTTARI_YEARS.copy()
        nakshatra_lord = moon_data["NakshatraLord"]
        start_index = sequence.index(nakshatra_lord)
        sequence = sequence[start_index:] + sequence[:start_index]
        lengths = lengths[start_index:] + lengths[:start_index]
        dasa_order: dict[PLANETS, int] = dict(zip(sequence, lengths))

        nakshatra_start = NAKSHATRAS.index(moon_data["Nakshatra"]) * 800
        elapsed_moon_mins = round(moon.lon * 60, 2) - nakshatra_start
        remaining_arc_mins = 800 - elapsed_moon_mins
        duration = dasa_order[nakshatra_lord]
        elapsed_duration = duration - (duration / 800) * remaining_arc_mins

        start = self._compute_new_date(self._chart_date(), elapsed_duration, "backward")
        dashas: _VimshottariData = {}
        for dasa, length in zip(sequence, lengths):
            end = self._compute_new_date(self._date_tuple(start), length, "forward")
            bhuktis: dict[PLANETS, _DashaPeriod] = {}
            dashas[dasa] = {
                "start": start.strftime("%d-%m-%Y"),
                "end": end.strftime("%d-%m-%Y"),
                "bhuktis": bhuktis,
            }
            bhukti_start = start
            index = sequence.index(dasa)
            bhukti_sequence = sequence[index:] + sequence[:index]
            bhukti_lengths = lengths[index:] + lengths[:index]
            for bhukti, bhukti_length in zip(bhukti_sequence, bhukti_lengths):
                bhukti_end = self._compute_new_date(
                    self._date_tuple(bhukti_start), length * bhukti_length / 120, "forward"
                )
                bhuktis[bhukti] = {
                    "start": bhukti_start.strftime("%d-%m-%Y"),
                    "end": bhukti_end.strftime("%d-%m-%Y"),
                }
                bhukti_start = bhukti_end
            start = end
        return dashas

    def _chart_date(self) -> _ChartDate:
        return (
            self.__horoscope__.year,
            self.__horoscope__.month,
            self.__horoscope__.day,
            self.__horoscope__.hour,
            self.__horoscope__.minute,
        )

    @staticmethod
    def _date_tuple(value: datetime) -> _ChartDate:
        return (value.year, value.month, value.day, value.hour, value.minute)

    @staticmethod
    def _compute_new_date(
        start_date: _ChartDate, diff_value: float, direction: str
    ) -> datetime:
        year, month, day, hour, minute = start_date
        whole_years = int(diff_value)
        months = (diff_value - whole_years) * 12
        whole_months = int(months)
        days = (months - whole_months) * 30
        whole_days = int(days)
        hours = (days - whole_days) * 24
        whole_hours = int(hours)
        minutes = (hours - whole_hours) * 60
        delta = relativedelta(
            years=whole_years,
            months=whole_months,
            days=whole_days,
            hours=whole_hours,
            minutes=int(minutes),
        )
        initial = datetime(year, month, day, hour, minute)
        if direction == "backward":
            return initial - delta
        if direction == "forward":
            return initial + delta
        raise ValueError("direction must be either 'backward' or 'forward'")

    @staticmethod
    def _find_current_index_by_date(
        items: Sequence[_DashaTimelineItem],
        date: datetime,
        start_key: Literal["start"] = "start",
        end_key: Literal["end"] = "end",
    ) -> int | None:
        """Return index where date lies between start and end."""
        for idx, item in enumerate(items):
            start = parseDate(item.get(start_key))
            end = parseDate(item.get(end_key))
            if start and end and start <= date <= end:
                return idx
        return None

    def get_antardasha_by_index(
        self, n: int, date: str | datetime | None = None
    ) -> AntarDashaType | None:
        """
        Returns an Antardasha period relative to the current Antardasha for a given date.

        Args:
            n: The relative index from the current Antardasha (0 for current, -1 for previous, 1 for next).
            date: Optional. A string "DD-MM-YYYY" or a datetime object to determine the current Antardasha.
                  If None, the current UTC time is used.

        Returns:
            An AntarDashaType object if found, otherwise None.
        """
        if (maha := self.get_mahadasha_by_index(0, date)) is None:
            return None

        if (antardashas := maha.get("antardashas", [])) is None:
            return None

        if date:
            target_date = parseDate(date)
        else:
            target_date = datetime.now(timezone.utc)
        if target_date is None:
            return None

        current_index = self._find_current_index_by_date(antardashas, target_date)
        if current_index is None:
            return None

        target_index = current_index + n

        if 0 <= target_index < len(antardashas):
            return antardashas[target_index]

        return None

    def get_mahadasha_by_index(
        self, n: int, date: str | datetime | None = None
    ) -> MahaDashaType | None:
        """
        Returns a Mahadasha period relative to the current Mahadasha for a given date.

        Args:
            n: The relative index from the current Mahadasha (0 for current, -1 for previous, 1 for next).
            date: Optional. A string "DD-MM-YYYY" or a datetime object to determine the current Mahadasha.
                  If None, the current UTC time is used.

        Returns:
            A MahaDashaType object if found, otherwise None.
        """
        if not self.dasha:
            return None

        if date:
            target_date = parseDate(date)
        else:
            target_date = datetime.now(timezone.utc)
        if target_date is None:
            return None

        if (
            current_index := self._find_current_index_by_date(self.dasha, target_date)
        ) is None:
            return None

        target = current_index + n

        if 0 <= target < len(self.dasha):
            return self.dasha[target]

        return None
