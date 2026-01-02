from datetime import datetime, timezone
from typing import List, Union
from vedicastro.VedicAstro import VedicHoroscopeData
from ascendant.types import AntarDashaType, DashasType, MahaDashaType
from ascendant.utils import parseDate


class Dasha:
    """Utility class to compute and format Vimshottari Dasha timeline."""

    def __init__(self, horoscope: VedicHoroscopeData):
        """
        Initializes the Dasha utility with a VedicHoroscopeData object.

        Args:
            horoscope: An instance of VedicHoroscopeData containing the birth chart information.
        """
        self.__horoscope__ = horoscope
        self.__chart__ = horoscope.generate_chart()

        self.dasha = self.get_dasha_timeline()

    def get_dasha_timeline(self) -> DashasType:
        """
        Computes and returns the Vimshottari Dasha timeline.

        Returns:
            A list of MahaDashaType objects, each containing its AntarDashaType sub-periods.
        """
        vhd = self.__horoscope__.compute_vimshottari_dasa(self.__chart__)
        dashas: DashasType = []

        for maha_planet, details in vhd.items():
            bhuktis = details.get("bhuktis", {})

            antardashas: List[AntarDashaType] = []
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

    @staticmethod
    def _find_current_index_by_date(
        items, date: datetime, start_key="start", end_key="end"
    ):
        """Return index where date lies between start and end."""
        for idx, item in enumerate(items):
            start = parseDate(item.get(start_key))
            end = parseDate(item.get(end_key))
            if start and end and start <= date <= end:
                return idx
        return None

    def get_antardasha_by_index(
        self, n: int, date: Union[str, datetime] | None = None
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
        maha = self.get_mahadasha_by_index(0, date)
        if not maha:
            return None

        antardashas = maha.get("antardashas", [])
        if not antardashas:
            return None

        if date:
            target_date = parseDate(date)
        else:
            target_date = datetime.now(timezone.utc)

        current_index = self._find_current_index_by_date(antardashas, target_date)
        if current_index is None:
            return None

        target_index = current_index + n

        if 0 <= target_index < len(antardashas):
            return antardashas[target_index]

        return None

    def get_mahadasha_by_index(
        self, n: int, date: Union[str, datetime] | None = None
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

        current_index = self._find_current_index_by_date(self.dasha, target_date)

        if current_index is None:
            return None

        target = current_index + n

        if 0 <= target < len(self.dasha):
            return self.dasha[target]

        return None
