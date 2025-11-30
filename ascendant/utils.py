from datetime import datetime, timezone
import re
from typing import List, Union

from vedicastro.VedicAstro import HOUSE_SYSTEM_MAPPING
from ascendant.types import HOUSES, PLANET_SIGN_RELATION, PLANETS, RASHIS
from ascendant.const import RASHIS as RASHI_MAP


def isSignOdd(n: HOUSES) -> bool:
    """Return True if the rashi index is odd-numbered per this module's scheme."""
    if not n:
        return None
    return n % 2 == 0


def getSignName(n: HOUSES) -> RASHIS:
    if not n and n != 0:
        return None
    return RASHI_MAP[n]


def getHouseSystem(house_system: str):
    # Normalize
    key = house_system.replace("_", " ").strip().title()

    # If exists in mapping, return it
    if key in HOUSE_SYSTEM_MAPPING:
        return HOUSE_SYSTEM_MAPPING[key]

    # Default fallback
    return HOUSE_SYSTEM_MAPPING["Whole Sign"]


def parseDate(s: Union[str, datetime]) -> datetime:
    if not s:
        return None
    if isinstance(s, datetime):
        if s.tzinfo is None:
            return s.replace(tzinfo=timezone.utc)
        return s.astimezone(timezone.utc)
    dt = datetime.strptime(s, "%d-%m-%Y")
    return dt.replace(tzinfo=timezone.utc)


def planetSignRelation(
    planet: PLANETS, sign: RASHIS, lon: float
) -> List[PLANET_SIGN_RELATION]:
    # -------------------------
    # Moola Trikona degree map
    # -------------------------
    moolatrikona_ranges = {
        "Sun": ("Leo", (0, 20)),
        "Moon": ("Taurus", (4, 30)),
        "Mars": ("Aries", (0, 12)),
        "Mercury": ("Virgo", (16, 20)),
        "Jupiter": ("Sagittarius", (0, 10)),
        "Venus": ("Libra", (0, 15)),
        "Saturn": ("Aquarius", (0, 20)),
    }

    results: List[PLANET_SIGN_RELATION] = []

    # -------------------------
    # Helper: check MT
    # -------------------------
    if planet in moolatrikona_ranges:
        mt_sign, (start, end) = moolatrikona_ranges[planet]
        if sign == mt_sign and start <= lon % 30 <= end:
            results.append("Moola Trikona")

    # -------------------------
    # Basic classification per sign
    # -------------------------
    match sign:
        case "Aries":
            match planet:
                case "Sun":
                    results.append("Exalted")
                case "Mars":
                    results.append("Own")
                case "Saturn":
                    results.append("Debilitated")
                case "Jupiter":
                    results.append("Friend")
                case "Mercury" | "Venus":
                    results.append("Neutral")
                case _:
                    results.append("Enemy")

        case "Taurus":
            match planet:
                case "Moon":
                    results.append("Exalted")
                case "Venus":
                    results.append("Own")
                case "Rahu" | "Ketu":
                    results.append("Debilitated")
                case "Mercury" | "Saturn":
                    results.append("Friend")
                case "Mars":
                    results.append("Neutral")
                case _:
                    results.append("Enemy")

        case "Gemini":
            match planet:
                case "Mercury":
                    results.append("Own")
                case "Sun":
                    results.append("Neutral")
                case "Mars" | "Jupiter":
                    results.append("Enemy")
                case _:
                    results.append("Friend")

        case "Cancer":
            match planet:
                case "Jupiter":
                    results.append("Exalted")
                case "Moon":
                    results.append("Own")
                case "Mars":
                    results.append("Debilitated")
                case "Sun":
                    results.append("Neutral")
                case _:
                    results.append("Enemy")

        case "Leo":
            match planet:
                case "Sun":
                    results.append("Own")
                case "Moon" | "Mars" | "Mercury" | "Jupiter":
                    results.append("Friend")
                case _:
                    results.append("Enemy")

        case "Virgo":
            match planet:
                case "Mercury":
                    results.extend(["Own", "Exalted"])  # Your requirement
                case "Venus":
                    results.append("Debilitated")
                case "Sun":
                    results.append("Neutral")
                case "Mars":
                    results.append("Enemy")
                case _:
                    results.append("Friend")

        case "Libra":
            match planet:
                case "Saturn":
                    results.append("Exalted")
                case "Venus":
                    results.append("Own")
                case "Sun":
                    results.append("Debilitated")
                case "Jupiter":
                    results.append("Enemy")
                case "Moon" | "Mars":
                    results.append("Neutral")
                case _:
                    results.append("Friend")

        case "Scorpio":
            match planet:
                case "Rahu" | "Ketu":
                    results.append("Exalted")
                case "Mars":
                    results.append("Own")
                case "Moon":
                    results.append("Debilitated")
                case "Saturn":
                    results.append("Enemy")
                case "Sun" | "Jupiter":
                    results.append("Friend")
                case _:
                    results.append("Neutral")

        case "Sagittarius":
            match planet:
                case "Jupiter":
                    results.append("Own")
                case "Moon" | "Mercury" | "Saturn":
                    results.append("Neutral")
                case _:
                    results.append("Friend")

        case "Capricorn":
            match planet:
                case "Mars":
                    results.append("Exalted")
                case "Saturn":
                    results.append("Own")
                case "Jupiter":
                    results.append("Debilitated")
                case "Sun":
                    results.append("Enemy")
                case "Mercury" | "Moon":
                    results.append("Neutral")
                case _:
                    results.append("Friend")

        case "Aquarius":
            match planet:
                case "Saturn":
                    results.append("Own")
                case "Venus":
                    results.append("Friend")
                case "Sun" | "Rahu" | "Ketu":
                    results.append("Enemy")
                case _:
                    results.append("Neutral")

        case "Pisces":
            match planet:
                case "Venus":
                    results.append("Exalted")
                case "Jupiter":
                    results.append("Own")
                case "Sun" | "Rahu" | "Ketu":
                    results.append("Friend")
                case "Moon" | "Saturn":
                    results.append("Neutral")

    return results


def yogaNameToId(name: str) -> str:
    name = name.lower()  # Lowercase
    name = re.sub(
        r"[^a-z0-9]+", "_", name
    )  # Replace any non-alphanumeric group with underscore
    name = name.strip("_")  # Remove leading/trailing underscores
    return name
