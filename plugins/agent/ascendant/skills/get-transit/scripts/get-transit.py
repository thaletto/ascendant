#!/usr/bin/env python3
import argparse
import logging
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TypeAlias, TypedDict, cast, get_args

from ascendant import Ascendant
from ascendant.person_record import PersonRecordError, PersonRecordStore
from ascendant.types import ALLOWED_DIVISIONS, HOUSES, ChartType
from ascendant.types import RASHIS as RASHIS_LITERAL

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s %(message)s"
)
LOGGER = logging.getLogger(__name__)

RASHI: TypeAlias = RASHIS_LITERAL
RASHIS = cast(tuple[RASHI, ...], get_args(RASHIS_LITERAL))


@dataclass(frozen=True)
class TransitQuery:
    name: str
    date: datetime
    division: ALLOWED_DIVISIONS


@dataclass
class Arguments:
    name: object = ""
    date: object = None
    division: object = 1


class TransitRow(TypedDict):
    planet: str
    house: int
    sign: str
    degree: str
    in_sign: str
    retrograde: str
    nakshatra: str
    pada: int
    natal_house: int


def natal_house_for_sign(transit_sign: RASHI, lagna_sign: RASHI) -> int:
    if transit_sign not in RASHIS or lagna_sign not in RASHIS:
        raise ValueError(f"Unknown sign: {transit_sign} or {lagna_sign}")
    return (RASHIS.index(transit_sign) - RASHIS.index(lagna_sign)) % 12 + 1


def format_degree(longitude: float) -> str:
    deg_in_sign = longitude % 30
    return f"{deg_in_sign:.2f}°"


def render_houses(chart: ChartType, citation: str) -> str:
    """Render the transit houses as a concise, readable list."""
    lines = ["## Transit houses", ""]
    for h in range(1, 13):
        house = chart.get(cast(HOUSES, h))
        if not house:
            lines.append(f"{h}. No house data available. [sources: {citation}]")
            continue
        sign = house["sign"]
        if house.get("planets"):
            lord = house["planets"][0]["sign"]["lord"]
        elif (lagna := house.get("lagna")) is not None:
            lord = lagna["sign"]["lord"]
        else:
            lord = "—"
        planet_cells: list[str] = []
        for p in house.get("planets", []):
            tag = f" ({format_degree(p['longitude'])})"
            if p.get("is_retrograde"):
                tag = f" (R){tag}"
            planet_cells.append(f"{p['name']}{tag}")
        planets_str = ", ".join(planet_cells) if planet_cells else "—"
        lines.append(
            f"{h}. {sign} — ruled by {lord}; planets: {planets_str}. "
            + f"[sources: {citation}]"
        )
    return "\n".join(lines)


def render_planets(chart: ChartType, lagna_sign: RASHI, citation: str) -> str:
    """Render transit planet details as one item per planet."""
    rows: list[TransitRow] = []
    for h in range(1, 13):
        house = chart.get(cast(HOUSES, h))
        if not house:
            continue
        for p in house.get("planets", []):
            rows.append(
                {
                    "planet": p["name"],
                    "house": h,
                    "sign": p["sign"]["name"],
                    "degree": format_degree(p["longitude"]),
                    "in_sign": ", ".join(p.get("inSign", [])) or "—",
                    "retrograde": "Yes" if p.get("is_retrograde") else "No",
                    "nakshatra": p["sign"]["nakshatra"]["name"],
                    "pada": p["sign"]["nakshatra"]["pada"],
                    "natal_house": natal_house_for_sign(p["sign"]["name"], lagna_sign),
                }
            )
    rows.sort(key=lambda r: (r["house"], r["planet"]))

    lines = ["", "## Transit planets", ""]
    for r in rows:
        lines.append(
            f"- {r['planet']}: {r['degree']} in {r['sign']}; "
            + f"transit house {r['house']}, natal house {r['natal_house']}; "
            + f"{r['retrograde'].lower()} retrograde; {r['nakshatra']}, "
            + f"pada {r['pada']}; in sign with {r['in_sign']}. "
            + f"[sources: {citation}]"
        )
    return "\n".join(lines)


def get_transit(query: TransitQuery) -> str:
    record = PersonRecordStore().open(query.name)
    lagna_sign = record.d1[1]["sign"]

    target = query.date
    if target.tzinfo is None:
        target = target.replace(tzinfo=UTC)

    offset = target.utcoffset()
    if offset is None:
        raise ValueError("date must be timezone-aware")
    total_minutes = int(offset.total_seconds() // 60)
    hours, minutes = divmod(abs(total_minutes), 60)
    sign_char = "+" if total_minutes >= 0 else "-"
    utc = f"{sign_char}{hours:02}:{minutes:02}"

    latitude, longitude = record.coordinates

    ascendant = Ascendant(
        year=target.year,
        month=target.month,
        day=target.day,
        hour=target.hour,
        minute=target.minute,
        second=target.second,
        latitude=latitude,
        longitude=longitude,
        utc=utc,
    )

    LOGGER.info("Computed transit chart for %s at %s", query.name, target.isoformat())
    chart = ascendant.get_chart(query.division)

    timestamp = target.strftime("%Y-%m-%d %H:%M %Z").strip()
    header = (
        f"# Transit Chart — {query.name}\n\n"
        f"**Moment:** {timestamp}  \n"
        f"**Division:** D{query.division}  \n"
        f"**Location:** {latitude}, {longitude} (natal location)  \n"
        f"**Natal Lagna:** {lagna_sign}  \n"
        f"[sources: persons/{query.name}/CONTEXT.md; "
        f"persons/{query.name}/charts/D1.json]\n"
    )
    citation = (
        f"computed transit {target.isoformat()}; persons/{query.name}/charts/D1.json"
    )

    return "\n".join(
        [
            header,
            render_houses(chart, citation),
            render_planets(chart, lagna_sign, citation),
        ]
    )


def parse_args(argv: list[str] | None = None) -> TransitQuery:
    divisions = cast(tuple[ALLOWED_DIVISIONS, ...], get_args(ALLOWED_DIVISIONS))
    parser = argparse.ArgumentParser(
        description="Render a native's transit chart as a readable report."
    )
    _ = parser.add_argument("--name", required=True, help="Native's display name")
    _ = parser.add_argument(
        "--date",
        required=False,
        default=None,
        help=("Target moment in ISO 8601 with timezone offset. Defaults to now (UTC)."),
    )
    _ = parser.add_argument(
        "--division",
        required=False,
        type=int,
        default=1,
        help=f"Divisional chart number. Allowed: {divisions}",
    )
    args = parser.parse_args(argv, namespace=Arguments())

    name = args.name
    date_text = args.date
    division = args.division
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    if not isinstance(division, int) or division not in divisions:
        raise ValueError(f"division must be one of {divisions}, got {division}")

    if date_text is None:
        date = datetime.now(UTC)
    else:
        if not isinstance(date_text, str):
            raise TypeError("date must be an ISO 8601 string")
        date = datetime.fromisoformat(date_text)
        if date.tzinfo is None:
            date = date.replace(tzinfo=UTC)

    return TransitQuery(name=name, date=date, division=division)


def main(argv: list[str] | None = None) -> int:
    try:
        query = parse_args(argv)
    except (TypeError, ValueError, SystemExit) as e:
        if isinstance(e, SystemExit) and e.code == 0:
            return 0
        print(f"error: {e}", file=sys.stderr)
        return 2

    try:
        markdown = get_transit(query)
    except PersonRecordError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        LOGGER.exception("Failed to render transit")
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
