from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from datetime import date as Date
from typing import TypedDict

from dateutil.relativedelta import relativedelta

from ascendant.const import NAKSHATRAS, VIMSHOTTARI_PLANETS, VIMSHOTTARI_YEARS
from ascendant.ephemeris import EphemerisChart
from ascendant.horoscope import HoroscopeData
from ascendant.types import (
    PLANETS,
    AntarDashaType,
    CurrentDashaType,
    DashasType,
    MahaDashaType,
)


class _DashaPeriod(TypedDict):
    start: str
    end: str


class _VimshottariMahaDasha(_DashaPeriod):
    bhuktis: dict[PLANETS, _DashaPeriod]


_ChartDate = tuple[int, int, int, int, int]
_VimshottariData = dict[PLANETS, _VimshottariMahaDasha]


@dataclass(frozen=True, slots=True)
class _AntarPeriod:
    output: AntarDashaType
    start: Date
    end: Date


@dataclass(frozen=True, slots=True)
class _MahaPeriod:
    output: MahaDashaType
    start: Date
    end: Date
    antardashas: tuple[_AntarPeriod, ...]


_BoundedPeriod = _MahaPeriod | _AntarPeriod


class DashaTimeline:
    """Select periods from an existing Vimshottari Dasha timeline."""

    timeline: DashasType

    def __init__(self, timeline: DashasType) -> None:
        self.timeline = deepcopy(timeline)
        parsed: list[_MahaPeriod] = []
        for period in self.timeline:
            maha_start, maha_end = self._parse_bounds(period)
            antardashas: list[_AntarPeriod] = []
            for subperiod in period["antardashas"]:
                antar_start, antar_end = self._parse_bounds(subperiod)
                if antar_start < maha_start or antar_end > maha_end:
                    raise ValueError(
                        "antardasha boundaries must be within mahadasha"
                    )
                antardashas.append(
                    _AntarPeriod(subperiod, antar_start, antar_end)
                )
            parsed.append(
                _MahaPeriod(
                    period,
                    maha_start,
                    maha_end,
                    tuple(antardashas),
                )
            )
        self._periods = tuple(parsed)

    def current(
        self,
        when: str | Date | datetime | None = None,
    ) -> CurrentDashaType:
        """Return the period at a UTC-normalized moment.

        Strings use ``DD-MM-YYYY``. Dates are used directly, aware datetimes
        are converted to UTC, naive datetimes are treated as UTC, and an
        omitted value uses the current UTC date.
        """
        target = self._normalize(when)
        mahadasha: MahaDashaType | None = None
        antardasha: AntarDashaType | None = None
        for period in self._periods:
            if self._contains(period, target):
                mahadasha = period.output
                for subperiod in period.antardashas:
                    if self._contains(subperiod, target):
                        antardasha = subperiod.output
                        break
                break
        return {
            "mahadasha": mahadasha,
            "antardasha": antardasha,
        }

    def mahadasha(
        self,
        offset: int = 0,
        when: str | Date | datetime | None = None,
    ) -> MahaDashaType | None:
        target = self._normalize(when)
        current_index = self._index_containing(self._periods, target)
        if current_index is None:
            return None
        target_index = current_index + offset
        if 0 <= target_index < len(self._periods):
            return self._periods[target_index].output
        return None

    def antardasha(
        self,
        offset: int = 0,
        when: str | Date | datetime | None = None,
    ) -> AntarDashaType | None:
        target = self._normalize(when)
        maha_index = self._index_containing(self._periods, target)
        if maha_index is None:
            return None
        periods = self._periods[maha_index].antardashas
        current_index = self._index_containing(periods, target)
        if current_index is None:
            return None
        target_index = current_index + offset
        if 0 <= target_index < len(periods):
            return periods[target_index].output
        return None

    @staticmethod
    def _normalize(value: str | Date | datetime | None) -> Date:
        if value is None:
            return datetime.now(UTC).date()
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=UTC)
            return value.astimezone(UTC).date()
        if isinstance(value, Date):
            return value
        try:
            return (
                datetime.strptime(value, "%d-%m-%Y")
                .replace(tzinfo=UTC)
                .date()
            )
        except ValueError as error:
            raise ValueError("date must use DD-MM-YYYY") from error

    @staticmethod
    def _contains(
        period: _BoundedPeriod,
        target: Date,
    ) -> bool:
        return period.start <= target <= period.end

    @staticmethod
    def _parse_bounds(
        period: MahaDashaType | AntarDashaType,
    ) -> tuple[Date, Date]:
        try:
            start = (
                datetime.strptime(period["start"], "%d-%m-%Y")
                .replace(tzinfo=UTC)
                .date()
            )
            end = (
                datetime.strptime(period["end"], "%d-%m-%Y")
                .replace(tzinfo=UTC)
                .date()
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("timeline boundaries must use DD-MM-YYYY") from error
        if start > end:
            raise ValueError("timeline period start must not follow end")
        return start, end

    @classmethod
    def _index_containing(
        cls,
        periods: tuple[_MahaPeriod, ...] | tuple[_AntarPeriod, ...],
        target: Date,
    ) -> int | None:
        for index, period in enumerate(periods):
            if cls._contains(period, target):
                return index
        return None


class Dasha:
    """Utility class to compute and format Vimshottari Dasha timeline."""

    timeline: DashaTimeline

    def __init__(self, horoscope: HoroscopeData):
        """
        Initializes the Dasha utility with a HoroscopeData object.

        Args:
            horoscope: An instance of HoroscopeData containing the birth chart information.
        """
        self._initialize(horoscope, horoscope.generate_chart())

    @classmethod
    def from_ephemeris(
        cls,
        horoscope: HoroscopeData,
        ephemeris: EphemerisChart,
    ) -> "Dasha":
        dasha = cls.__new__(cls)
        dasha._initialize(horoscope, ephemeris)
        return dasha

    def _initialize(
        self,
        horoscope: HoroscopeData,
        ephemeris: EphemerisChart,
    ) -> None:
        self.__horoscope__: HoroscopeData = horoscope
        self.__chart__: EphemerisChart = ephemeris

        self.dasha: DashasType = self.get_dasha_timeline()
        self.timeline = DashaTimeline(self.dasha)

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
                bhukti_duration = length * bhukti_length / 120
                bhukti_end = self._compute_new_date(
                    self._date_tuple(bhukti_start),
                    bhukti_duration,
                    "forward",
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
        initial = datetime(year, month, day, hour, minute, tzinfo=UTC)
        if direction == "backward":
            return initial - delta
        if direction == "forward":
            return initial + delta
        raise ValueError("direction must be either 'backward' or 'forward'")

    def get_antardasha_by_index(
        self, n: int, date: str | Date | datetime | None = None
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
        return self.timeline.antardasha(n, date)

    def get_mahadasha_by_index(
        self, n: int, date: str | Date | datetime | None = None
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
        return self.timeline.mahadasha(n, date)
