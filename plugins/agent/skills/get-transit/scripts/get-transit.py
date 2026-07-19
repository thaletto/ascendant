#!/usr/bin/env python3
import argparse
import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TypeAlias, cast, get_args

from ascendant import Ascendant
from ascendant.types import RASHIS as RASHIS_LITERAL, ALLOWED_DIVISIONS

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s %(message)s"
)

RASHI: TypeAlias = RASHIS_LITERAL
RASHIS = cast(tuple[RASHI, ...], get_args(RASHIS_LITERAL))

@dataclass(frozen=True)
class TransitQuery:
    name: str
    date: datetime
    division: ALLOWED_DIVISIONS


def load_native(name: str) -> tuple[Path, dict[str, str]]:
    directory = Path("persons") / name
    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(
            f"Native '{name}' has no data directory at {directory}. ",
            "Run init-person first."
        )

    context_file = directory / "CONTEXT.md"
    if not context_file.exists():
        raise FileNotFoundError(
            f"Missing CONTEXT.md for native '{name}' at {context_file}."
        )

    text = context_file.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    in_frontmatter = False
    for line in text.splitlines():
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
                continue
            break
        if in_frontmatter and ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()

    for required in ("latitude", "longitude", "utc"):
        if required not in fields:
            raise ValueError(
                f"CONTEXT.md for '{name}' is missing required field '{required}'."
            )

    return directory, fields


def natal_lagna_sign(chart_dir: Path) -> RASHI:
    d1 = chart_dir / "charts" / "D1.json"
    if not d1.exists():
        raise FileNotFoundError(f"Missing natal chart at {d1}.")
    with d1.open("r", encoding="utf-8") as f:
        chart = json.load(f)
    house1 = chart.get("1")
    if not house1:
        raise ValueError("Natal D1.json has no house 1 entry.")
    return cast(RASHI, house1["sign"])


def natal_house_for_sign(transit_sign: RASHI, lagna_sign: RASHI) -> int:
    if transit_sign not in RASHIS or lagna_sign not in RASHIS:
        raise ValueError(f"Unknown sign: {transit_sign} or {lagna_sign}")
    return (RASHIS.index(transit_sign) - RASHIS.index(lagna_sign)) % 12 + 1


def format_degree(longitude: float) -> str:
    deg_in_sign = longitude % 30
    return f"{deg_in_sign:.2f}°"


def render_houses(chart) -> str:
    """Render the transit houses as a concise, readable list."""
    lines = ["## Transit houses", ""]
    for h in range(1, 13):
        house = chart.get(h)
        if not house:
            lines.append(f"{h}. No house data available.")
            continue
        sign = house["sign"]
        lord = (
            house["planets"][0]["sign"]["lord"]
            if house.get("planets")
            else (house["lagna"]["sign"]["lord"] if house.get("lagna") else "—")
        )
        planet_cells: list[str] = []
        for p in house.get("planets", []):
            tag = f" ({format_degree(p['longitude'])})"
            if p.get("is_retrograde"):
                tag = f" (R){tag}"
            planet_cells.append(f"{p['name']}{tag}")
        planets_str = ", ".join(planet_cells) if planet_cells else "—"
        lines.append(f"{h}. {sign} — ruled by {lord}; planets: {planets_str}.")
    return "\n".join(lines)


def render_planets(chart, lagna_sign: RASHI) -> str:
    """Render transit planet details as one item per planet."""
    rows = []
    for h in range(1, 13):
        house = chart.get(h)
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
            f"transit house {r['house']}, natal house {r['natal_house']}; "
            f"{r['retrograde'].lower()} retrograde; {r['nakshatra']}, "
            f"pada {r['pada']}; in sign with {r['in_sign']}."
        )
    return "\n".join(lines)


def get_transit(query: TransitQuery) -> str:
    directory, fields = load_native(query.name)
    lagna_sign = natal_lagna_sign(directory)

    target = query.date
    if target.tzinfo is None:
        target = target.replace(tzinfo=timezone.utc)

    offset = target.utcoffset()
    if offset is None:
        raise ValueError("date must be timezone-aware")
    total_minutes = int(offset.total_seconds() // 60)
    hours, minutes = divmod(abs(total_minutes), 60)
    sign_char = "+" if total_minutes >= 0 else "-"
    utc = f"{sign_char}{hours:02}:{minutes:02}"

    latitude = float(fields["latitude"])
    longitude = float(fields["longitude"])

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

    logging.info(f"Computed transit chart for {query.name} at {target.isoformat()}")
    chart = ascendant.get_chart(query.division)

    timestamp = target.strftime("%Y-%m-%d %H:%M %Z").strip()
    header = (
        f"# Transit Chart — {query.name}\n\n"
        f"**Moment:** {timestamp}  \n"
        f"**Division:** D{query.division}  \n"
        f"**Location:** {latitude}, {longitude} (natal location)  \n"
        f"**Natal Lagna:** {lagna_sign}\n"
    )

    return "\n".join(
        [header, render_houses(chart), render_planets(chart, lagna_sign)]
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
        help="Target moment in ISO 8601 with timezone offset. Defaults to now (UTC).",
    )
    _ = parser.add_argument(
        "--division",
        required=False,
        type=int,
        default=1,
        help=f"Divisional chart number. Allowed: {divisions}",
    )
    args = parser.parse_args(argv)

    name: object = args.name
    date_text: object = args.date
    division: object = args.division
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    if not isinstance(division, int) or division not in divisions:
        raise ValueError(f"division must be one of {divisions}, got {division}")

    if date_text is None:
        date = datetime.now(timezone.utc)
    else:
        if not isinstance(date_text, str):
            raise ValueError("date must be an ISO 8601 string")
        date = datetime.fromisoformat(date_text)
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)

    return TransitQuery(name=name, date=date, division=division)


def main(argv: list[str] | None = None) -> int:
    try:
        query = parse_args(argv)
    except (ValueError, SystemExit) as e:
        if isinstance(e, SystemExit) and e.code == 0:
            return 0
        print(f"error: {e}", file=sys.stderr)
        return 2

    try:
        markdown = get_transit(query)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        logging.exception("Failed to render transit")
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
