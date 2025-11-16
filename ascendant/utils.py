from datetime import datetime, timezone
from typing import Literal, Union
from ascendant.types import HOUSES, PLANETS, RASHIS
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


def parseDate(s: Union[str, datetime]) -> datetime:
    if not s:
        return None
    if isinstance(s, datetime):
        if s.tzinfo is None:
            return s.replace(tzinfo=timezone.utc)
        return s.astimezone(timezone.utc)
    dt = datetime.strptime(s, "%d-%m-%Y")
    return dt.replace(tzinfo=timezone.utc)


def PlanetSignRelation(
    planet: PLANETS, sign: RASHIS
) -> Literal[
    "Exalted", "Own", "Own Exalted", "Debilitated", "Friend", "Neutral", "Enemy"
]:
    match sign:
        case "Aries":
            match planet:
                case "Sun":
                    return "Exalted"
                case "Mars":
                    return "Own"
                case "Saturn":
                    return "Debilitated"
                case "Jupiter":
                    return "Friend"
                case "Mercury" | "Venus":
                    return "Neutral"
                case _:
                    return "Enemy"

        case "Taurus":
            match planet:
                case "Moon":
                    return "Exalted"
                case "Venus":
                    return "Own"
                case "Rahu" | "Ketu":
                    return "Debilitated"
                case "Mercury" | "Saturn":
                    return "Friend"
                case "Mars":
                    return "Neutral"
                case _:
                    return "Enemy"

        case "Gemini":
            match planet:
                case "Mercury":
                    return "Own"
                case "Sun":
                    return "Neutral"
                case "Mars" | "Jupiter":
                    return "Enemy"
                case _:
                    return "Friend"

        case "Cancer":
            match planet:
                case "Jupiter":
                    return "Exalted"
                case "Moon":
                    return "Own"
                case "Mars":
                    return "Debilitated"
                case "Sun":
                    return "Neutral"
                case _:
                    return "Enemy"

        case "Leo":
            match planet:
                case "Sun":
                    return "Own"
                case "Moon" | "Mars" | "Mercury" | "Jupiter":
                    return "Friend"
                case _:
                    return "Enemy"

        case "Virgo":
            match planet:
                case "Mercury":
                    return "Own Exalted"
                case "Venus":
                    return "Debilitated"
                case "Sun":
                    return "Neutral"
                case "Mars":
                    return "Enemy"
                case _:
                    return "Friend"

        case "Libra":
            match planet:
                case "Saturn":
                    return "Exalted"
                case "Venus":
                    return "Own"
                case "Sun":
                    return "Debilitated"
                case "Jupiter":
                    return "Enemy"
                case "Moon" | "Mars":
                    return "Neutral"
                case _:
                    return "Friend"

        case "Scorpio":
            match planet:
                case "Rahu" | "Ketu":
                    return "Exalted"
                case "Mars":
                    return "Own"
                case "Moon":
                    return "Debilitated"
                case "Saturn":
                    return "Enemy"
                case "Sun" | "Jupiter":
                    return "Friend"
                case _:
                    return "Neutral"

        case "Sagittarius":
            match planet:
                case "Jupiter":
                    return "Own"
                case "Moon" | "Mercury" | "Saturn":
                    return "Neutral"
                case _:
                    return "Friend"

        case "Capricorn":
            match planet:
                case "Mars":
                    return "Exalted"
                case "Saturn":
                    return "Own"
                case "Jupiter":
                    return "Debilitated"
                case "Sun":
                    return "Enemy"
                case "Mercury" | "Moon":
                    return "Neutral"
                case _:
                    return "Friend"

        case "Aquarius":
            match planet:
                case "Saturn":
                    return "Own"
                case "Venus":
                    return "Friend"
                case "Sun" | "Rahu" | "Ketu":
                    return "Enemy"
                case _:
                    return "Neutral"

        case "Pisces":
            match planet:
                case "Venus":
                    return "Exalted"
                case "Jupiter":
                    return "Own"
                case "Sun" | "Rahu" | "Ketu":
                    return "Friend"
                case "Moon" | "Saturn":
                    return "Neutral"
