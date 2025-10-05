from datetime import datetime
from typing import List, Dict
from tabulate import tabulate
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
    def get_vimshottari_timeline(self) -> List[Dict]:
        """Compute flattened Vimshottari Dasha timeline (Maha + Bhukti)."""
        vhd = self.horoscope
        vimshottari_dasa = vhd.compute_vimshottari_dasa(self.chart)

        timeline = []
        for maha, details in vimshottari_dasa.items():
            for bhukti, period in details["bhuktis"].items():
                timeline.append({
                    "mahadasha": maha,
                    "bhukti": bhukti,
                    "start": self._parse_date(period["start"]),
                    "end": self._parse_date(period["end"])
                })

        # Sort by start date
        timeline.sort(key=lambda x: x["start"])

        # Convert datetime back to strings
        for t in timeline:
            t["start"] = self._format_date(t["start"])
            t["end"] = self._format_date(t["end"])

        return timeline

    def pretty_table(self) -> str:
        """Return formatted Vimshottari Dasha table."""
        timeline = self.get_vimshottari_timeline()
        return tabulate(timeline, headers="keys", tablefmt="simple_grid")

    # ----------------------------------------------------------
    # ADVANCED METHODS
    # ----------------------------------------------------------
    def get_dasha_by_index(self, n: int = 0) -> Dict:
        """
        Return the current (+n or -n) Dasha period.
        n = 0 → current dasha
        n = 1 → next dasha
        n = -1 → previous dasha
        """
        timeline = self.get_vimshottari_timeline()
        now = datetime.now()

        # Convert string dates back to datetime for comparison
        parsed = [
            {**t, "start": self._parse_date(t["start"]), "end": self._parse_date(t["end"])}
            for t in timeline
        ]

        # Find current index
        current_index = next(
            (i for i, t in enumerate(parsed) if t["start"] <= now <= t["end"]),
            None
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
