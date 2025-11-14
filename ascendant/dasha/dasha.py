from datetime import datetime
from typing import List, Dict
from vedicastro.VedicAstro import VedicHoroscopeData


class DashaFinder:
    """Utility class to compute and format Vimshottari Dasha timeline."""

    def __init__(self, horoscope: VedicHoroscopeData):
        self.horoscope = horoscope
        self.chart = horoscope.generate_chart()

    # ----------------------------------------------------------
    # INTERNAL HELPERS
    # ----------------------------------------------------------
    def _parse_date(self, date_str: str) -> datetime:
        """Parse DD-MM-YYYY string into datetime."""
        return datetime.strptime(date_str, "%d-%m-%Y")

    def _format_date(self, date_obj: datetime) -> str:
        """Convert datetime back to DD-MM-YYYY string."""
        return date_obj.strftime("%d-%m-%Y")

    # ----------------------------------------------------------
    # CORE METHODS
    # ----------------------------------------------------------
    def _get_vimshottari_timeline(self) -> List[Dict]:
        """Compute flattened Vimshottari Dasha timeline (Maha + Bhukti)."""
        vhd = self.horoscope
        vimshottari_dasa = vhd.compute_vimshottari_dasa(self.chart)

        timeline = []
        for maha, details in vimshottari_dasa.items():
            for bhukti, period in details["bhuktis"].items():
                timeline.append(
                    {
                        "mahadasha": maha,
                        "bhukti": bhukti,
                        "start": self._parse_date(period["start"]),
                        "end": self._parse_date(period["end"]),
                    }
                )

        # Sort by start date
        timeline.sort(key=lambda x: x["start"])

        # Convert datetime back to strings
        for t in timeline:
            t["start"] = self._format_date(t["start"])
            t["end"] = self._format_date(t["end"])

        return timeline

    def get_vimshottari_dasha(self) -> List[Dict]:
        """
        Return Vimshottari Dasha as List[Dict] in nested Mahadasha-Antardasha format.
        Shape:
        [
          {
            "mahadasha": str,
            "antardasha": [ { "bhuthi": str, "start": str, "end": str } ],
            "start": str,
            "end": str,
          },
          ...
        ]
        """
        vhd = self.horoscope
        vimshottari_dasa = vhd.compute_vimshottari_dasa(self.chart)

        nested: List[Dict] = []
        for maha, details in vimshottari_dasa.items():
            bhuktis = details.get("bhuktis", {})
            antardasha_list: List[Dict] = []

            for bhukti, period in bhuktis.items():
                antardasha_list.append(
                    {
                        "bhuthi": bhukti,
                        "start": period["start"],
                        "end": period["end"],
                    }
                )

            # Sort antardashas by start
            antardasha_list.sort(key=lambda x: self._parse_date(x["start"]))

            # Derive maha start/end from first/last bhukti
            if antardasha_list:
                maha_start = antardasha_list[0]["start"]
                maha_end = antardasha_list[-1]["end"]
            else:
                maha_start = ""
                maha_end = ""

            nested.append(
                {
                    "mahadasha": maha,
                    "antardasha": antardasha_list,
                    "start": maha_start,
                    "end": maha_end,
                }
            )

        nested.sort(
            key=lambda x: self._parse_date(x["start"]) if x["start"] else datetime.max
        )

        return nested

    # ----------------------------------------------------------
    # ADVANCED METHODS
    # ----------------------------------------------------------
    def get_bhuthi_by_index(self, n: int = 0) -> Dict:
        """
        Return the current (+n or -n) Dasha period.
        n = 0 → current dasha
        n = 1 → next dasha
        n = -1 → previous dasha
        """
        timeline = self._get_vimshottari_timeline()
        now = datetime.now()

        # Convert string dates back to datetime for comparison
        parsed = [
            {
                **t,
                "start": self._parse_date(t["start"]),
                "end": self._parse_date(t["end"]),
            }
            for t in timeline
        ]

        # Find current index
        current_index = next(
            (i for i, t in enumerate(parsed) if t["start"] <= now <= t["end"]), None
        )

        if current_index is None:
            raise ValueError("No current Dasha found for this date.")

        target_index = current_index + n
        if target_index < 0 or target_index >= len(parsed):
            raise IndexError("Requested Dasha index out of range.")

        result = parsed[target_index]
        result["start"] = self._format_date(result["start"])
        result["end"] = self._format_date(result["end"])
        return result
