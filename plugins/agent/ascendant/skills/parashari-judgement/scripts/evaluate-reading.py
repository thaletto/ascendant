#!/usr/bin/env python3
"""Emit a deterministic, cited Parashari evidence ledger for saved charts."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any, Literal, cast

from ascendant import Ascendant


Topic = Literal[
    "career",
    "daily-transit",
    "education",
    "family",
    "finance",
    "health",
    "marriage",
    "property",
    "relationship-compatibility",
]

TOPICS: tuple[Topic, ...] = (
    "career",
    "daily-transit",
    "education",
    "family",
    "finance",
    "health",
    "marriage",
    "property",
    "relationship-compatibility",
)

SIGNS = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
    "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)
SIGN_LORDS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}
TOPIC_CONFIG: dict[Topic, tuple[tuple[int, ...], int | None, str]] = {
    "career": ((6, 10, 11), 10, "Career"),
    "education": ((4, 5, 9), 24, "Education"),
    "finance": ((2, 8, 11), 2, "Finance"),
    "health": ((1, 6, 8), None, "Wellbeing"),
    "marriage": ((5, 7, 8), 9, "Partnership"),
    "property": ((4, 11, 12), 4, "Property"),
}
FAMILY_CONFIG: dict[str, tuple[int, ...]] = {
    "mother": (4,), "father": (9,), "sibling": (3,), "child": (5,),
    "household": (4,),
}
SOURCE_IDS = (
    "BPHS-RS-1984",
    "BVR-HTJH",
    "PRV1",
)


@dataclass(frozen=True)
class Evidence:
    statement: str
    citations: tuple[str, ...]
    polarity: Literal["support", "constraint", "neutral", "missing"]


@dataclass(frozen=True)
class Reading:
    person: str
    topic: Topic
    as_of: str
    status: str
    evidence: tuple[Evidence, ...]
    practical_guidance: Evidence
    sources: dict[str, str]


class ReadingError(ValueError):
    """An input record cannot support the requested deterministic reading."""


def _safe_person_name(name: str) -> str:
    if not name or name in {".", ".."} or Path(name).name != name:
        raise ReadingError("name must identify one direct persons/<name> record")
    return name


def _read_json(path: Path) -> Any:
    if not path.is_file():
        raise ReadingError(f"Missing required data: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ReadingError(f"Invalid JSON: {path}") from error


def _optional_json(path: Path) -> Any | None:
    if not path.is_file():
        return None
    return _read_json(path)


def _load_record(name: str, required_varga: int | None) -> dict[str, Any]:
    safe_name = _safe_person_name(name)
    directory = Path("persons") / safe_name
    context = directory / "CONTEXT.md"
    if not context.is_file():
        raise ReadingError(f"Missing required data: {context}")
    charts = directory / "charts"
    record: dict[str, Any] = {
        "name": safe_name,
        "directory": directory,
        "d1": _read_json(charts / "D1.json"),
        "dasha": _read_json(directory / "dasha.json"),
        "sav": _read_json(directory / "sav.json"),
        "provenance": _optional_json(directory / "provenance.json"),
        "context": _context_fields(context),
    }
    if required_varga is not None:
        record["varga"] = _read_json(charts / f"D{required_varga}.json")
    return record


def _context_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    in_frontmatter = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() == "---":
            if in_frontmatter:
                break
            in_frontmatter = True
            continue
        if in_frontmatter and ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def _house(chart: dict[str, Any], number: int) -> dict[str, Any]:
    house = chart.get(str(number))
    if house is None:
        house = cast(Any, chart).get(number)
    if not isinstance(house, dict) or not isinstance(house.get("sign"), str):
        raise ReadingError(f"Chart has no valid house {number}")
    return house


def _planet(chart: dict[str, Any], name: str) -> tuple[int, dict[str, Any]] | None:
    for house_number in range(1, 13):
        for planet in _house(chart, house_number).get("planets", []):
            if isinstance(planet, dict) and planet.get("name") == name:
                return house_number, planet
    return None


def _citation(person: str, file_name: str, rule_id: str) -> tuple[str, ...]:
    return (
        f"persons/{person}/{file_name}", rule_id, *SOURCE_IDS,
    )


def _house_evidence(
    person: str,
    chart: dict[str, Any],
    chart_label: str,
    topic_prefix: str,
    house_number: int,
) -> Evidence:
    house = _house(chart, house_number)
    sign = cast(str, house["sign"])
    lord = SIGN_LORDS[sign]
    found = _planet(chart, lord)
    rule_id = f"PR-{topic_prefix}-H{house_number:02}"
    citations = _citation(person, chart_label, rule_id)
    if found is None:
        return Evidence(
            f"House {house_number} is {sign}; its lord {lord} is unavailable.",
            citations,
            "missing",
        )

    lord_house, planet = found
    dignity = planet.get("inSign", [])
    if not isinstance(dignity, list):
        dignity = []
    dignity_text = ", ".join(str(item) for item in dignity) or "no dignity label"
    if any(item in dignity for item in ("Exalted", "Moola Trikona", "Own", "Friend")):
        polarity: Literal["support", "constraint", "neutral", "missing"] = "support"
        phrase = "supports"
    elif any(item in dignity for item in ("Debilitated", "Enemy")) or lord_house in (6, 8, 12):
        polarity = "constraint"
        phrase = "constrains"
    else:
        polarity = "neutral"
        phrase = "gives mixed evidence for"
    return Evidence(
        f"House {house_number} is {sign}; {lord}, its lord, is in house "
        f"{lord_house} with {dignity_text}, which {phrase} this topic.",
        citations,
        polarity,
    )


def _provenance_evidence(record: dict[str, Any], topic_prefix: str) -> Evidence:
    citations = _citation(
        record["name"], "provenance.json", f"PR-{topic_prefix}-PROVENANCE",
    )
    provenance = record["provenance"]
    if not isinstance(provenance, dict):
        return Evidence(
            "This legacy record has no saved calculation provenance.",
            citations,
            "neutral",
        )
    ayanamsa = provenance.get("ayanamsa", "unspecified")
    house_system = provenance.get("house_system", "unspecified")
    rule_pack = provenance.get("rule_pack", "unspecified")
    return Evidence(
        f"Calculation provenance is {ayanamsa}, {house_system}, and {rule_pack}.",
        citations,
        "neutral",
    )


def _active_dasha(dasha: Any, as_of: date) -> tuple[str, str] | None:
    if not isinstance(dasha, list):
        raise ReadingError("dasha.json must contain a timeline list")
    for maha in dasha:
        if not isinstance(maha, dict):
            continue
        start = _dasha_date(maha.get("start"))
        end = _dasha_date(maha.get("end"))
        if start is None or end is None or not start <= as_of <= end:
            continue
        for antar in maha.get("antardashas", []):
            if not isinstance(antar, dict):
                continue
            antar_start = _dasha_date(antar.get("start"))
            antar_end = _dasha_date(antar.get("end"))
            if antar_start and antar_end and antar_start <= as_of <= antar_end:
                maha_name = maha.get("mahadasha")
                antar_name = antar.get("antardasha")
                if isinstance(maha_name, str) and isinstance(antar_name, str):
                    return maha_name, antar_name
    return None


def _dasha_date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.strptime(value, "%d-%m-%Y").date()
    except ValueError:
        return None


def _dasha_evidence(
    record: dict[str, Any],
    primary_houses: tuple[int, ...],
    topic_prefix: str,
    as_of: date,
) -> Evidence:
    active = _active_dasha(record["dasha"], as_of)
    citations = _citation(record["name"], "dasha.json", f"PR-{topic_prefix}-DASHA")
    if active is None:
        return Evidence(
            f"No active Vimshottari period is available for {as_of.isoformat()}.",
            citations,
            "missing",
        )
    d1 = cast(dict[str, Any], record["d1"])
    relevant_planets = {
        SIGN_LORDS[cast(str, _house(d1, house)["sign"])]
        for house in primary_houses
    }
    active_planets = set(active)
    activated = active[0] in relevant_planets and active[1] in relevant_planets
    result = "activates" if activated else "does not jointly activate"
    return Evidence(
        f"Vimshottari {active[0]}–{active[1]} is active on "
        f"{as_of.isoformat()} and {result} the selected house lords; "
        "timing requires both period lords to activate them.",
        citations,
        "support" if activated else "neutral",
    )


def _sav_evidence(
    record: dict[str, Any], primary_houses: tuple[int, ...], topic_prefix: str,
) -> Evidence:
    sav = record["sav"]
    sarva = sav.get("sarva") if isinstance(sav, dict) else None
    citations = _citation(record["name"], "sav.json", f"PR-{topic_prefix}-SAV")
    if not isinstance(sarva, dict):
        return Evidence("No SAV scores are available for this reading.", citations, "missing")
    d1 = cast(dict[str, Any], record["d1"])
    scores: list[str] = []
    for house_number in primary_houses:
        sign = cast(str, _house(d1, house_number)["sign"])
        score = sarva.get(sign)
        if isinstance(score, int | float):
            scores.append(f"house {house_number} ({sign}) = {score}")
    if not scores:
        return Evidence("No relevant SAV scores are available for this topic.", citations, "missing")
    return Evidence(
        "Supplementary SAV scores: " + "; ".join(scores) + ".",
        citations,
        "neutral",
    )


def _transit_chart(record: dict[str, Any], as_of: datetime) -> dict[str, Any]:
    fields = cast(dict[str, str], record["context"])
    try:
        latitude = float(fields["latitude"])
        longitude = float(fields["longitude"])
    except KeyError as error:
        raise ReadingError(f"CONTEXT.md is missing {error.args[0]}") from error
    offset = as_of.utcoffset()
    if offset is None:
        raise ReadingError("date must include a timezone")
    minutes = int(offset.total_seconds() // 60)
    sign = "+" if minutes >= 0 else "-"
    hours, remainder = divmod(abs(minutes), 60)
    return cast(
        dict[str, Any],
        Ascendant(
            year=as_of.year, month=as_of.month, day=as_of.day,
            hour=as_of.hour, minute=as_of.minute, second=as_of.second,
            latitude=latitude, longitude=longitude,
            utc=f"{sign}{hours:02}:{remainder:02}",
        ).get_chart(1),
    )


def _topic_transit_evidence(
    record: dict[str, Any],
    primary_houses: tuple[int, ...],
    topic_prefix: str,
    as_of: datetime,
) -> Evidence:
    transit = _transit_chart(record, as_of)
    natal_lagna = cast(str, _house(cast(dict[str, Any], record["d1"]), 1)["sign"])
    matches: list[str] = []
    for transit_house in range(1, 13):
        house = _house(transit, transit_house)
        natal_house = (SIGNS.index(cast(str, house["sign"])) - SIGNS.index(natal_lagna)) % 12 + 1
        if natal_house not in primary_houses:
            continue
        for planet in house.get("planets", []):
            if isinstance(planet, dict) and isinstance(planet.get("name"), str):
                matches.append(f"{planet['name']} in natal house {natal_house}")
    citations = (
        f"computed transit {as_of.isoformat()}",
        f"persons/{record['name']}/CONTEXT.md",
        f"persons/{record['name']}/charts/D1.json",
        f"PR-{topic_prefix}-TRANSIT",
        *SOURCE_IDS,
    )
    detail = "; ".join(matches) if matches else "no planets in the selected natal houses"
    return Evidence(
        f"Computed transit at {as_of.isoformat()} has {detail}.",
        citations,
        "neutral",
    )


def _status(evidence: tuple[Evidence, ...], requires_varga: bool) -> str:
    if any(item.polarity == "missing" for item in evidence):
        return "insufficient evidence"
    if any(item.polarity == "constraint" for item in evidence):
        return "constrained"
    support_count = sum(item.polarity == "support" for item in evidence)
    if support_count >= (3 if requires_varga else 2):
        return "supported"
    return "mixed"


def _topic_reading(
    name: str, topic: Topic, as_of: datetime, family_role: str | None,
) -> Reading:
    if topic == "family":
        if family_role not in FAMILY_CONFIG:
            raise ReadingError("family requires --family-role: mother, father, sibling, child, or household")
        primary_houses = FAMILY_CONFIG[family_role]
        required_varga = None
        title = f"Family ({family_role})"
    else:
        primary_houses, required_varga, title = TOPIC_CONFIG[topic]
    record = _load_record(name, required_varga)
    prefix = topic.replace("-", "").upper()[:3]
    evidence = [_provenance_evidence(record, prefix)] + [
        _house_evidence(record["name"], record["d1"], "charts/D1.json", prefix, house)
        for house in primary_houses
    ]
    if required_varga is not None:
        evidence.extend(
            _house_evidence(
                record["name"], record["varga"], f"charts/D{required_varga}.json",
                prefix, house,
            )
            for house in primary_houses
        )
    evidence.append(_dasha_evidence(record, primary_houses, prefix, as_of.date()))
    evidence.append(_topic_transit_evidence(record, primary_houses, prefix, as_of))
    evidence.append(_sav_evidence(record, primary_houses, prefix))
    frozen_evidence = tuple(evidence)
    status = _status(frozen_evidence, required_varga is not None)
    guidance = Evidence(
        f"Use the {title.lower()} evidence as planning context, not certainty.",
        ("PRV1-POLICY-001", "PRV1"),
        "neutral",
    )
    return Reading(
        person=record["name"], topic=topic, as_of=as_of.isoformat(), status=status,
        evidence=frozen_evidence, practical_guidance=guidance,
        sources=_source_bibliography(),
    )


def _daily_transit_reading(name: str, as_of: datetime) -> Reading:
    record = _load_record(name, None)
    transit = _transit_chart(record, as_of)
    natal_lagna = cast(str, _house(cast(dict[str, Any], record["d1"]), 1)["sign"])
    evidence: list[Evidence] = []
    for house_number in range(1, 13):
        house = _house(cast(dict[str, Any], transit), house_number)
        for planet in house.get("planets", []):
            if not isinstance(planet, dict) or not isinstance(planet.get("name"), str):
                continue
            sign_name = cast(str, house["sign"])
            natal_house = (SIGNS.index(sign_name) - SIGNS.index(natal_lagna)) % 12 + 1
            evidence.append(Evidence(
                f"{planet['name']} transits {sign_name}, the natal house {natal_house}.",
                (
                    f"computed transit {as_of.isoformat()}",
                    f"persons/{record['name']}/CONTEXT.md",
                    f"persons/{record['name']}/charts/D1.json",
                    "PR-DAI-TRANSIT", "BPHS-RS-1984", "PRV1",
                ),
                "neutral",
            ))
    guidance = Evidence(
        "Use the dated transit facts to plan the next few days, not to promise an event.",
        ("PRV1-POLICY-001", "PRV1"), "neutral",
    )
    return Reading(
        person=record["name"], topic="daily-transit", as_of=as_of.isoformat(),
        status="factual transit report", evidence=tuple(evidence),
        practical_guidance=guidance, sources=_source_bibliography(),
    )


def _compatibility_reading(name: str, other_name: str, as_of: datetime) -> Reading:
    first = _load_record(name, 9)
    second = _load_record(other_name, 9)
    evidence: list[Evidence] = []
    for record in (first, second):
        d1 = cast(dict[str, Any], record["d1"])
        moon = _planet(d1, "Moon")
        if moon is None:
            raise ReadingError(f"Missing Moon placement in {record['name']}'s D1 chart")
        moon_house, moon_data = moon
        moon_sign = cast(dict[str, Any], moon_data["sign"])["name"]
        evidence.append(Evidence(
            f"{record['name']}'s Moon is in {moon_sign}, house {moon_house}.",
            _citation(record["name"], "charts/D1.json", "PR-REL-MOON"),
            "neutral",
        ))
        d9 = cast(dict[str, Any], record["varga"])
        d9_moon = _planet(d9, "Moon")
        if d9_moon is None:
            raise ReadingError(f"Missing Moon placement in {record['name']}'s D9 chart")
        d9_house, d9_moon_data = d9_moon
        d9_moon_sign = cast(dict[str, Any], d9_moon_data["sign"])["name"]
        evidence.append(Evidence(
            f"{record['name']}'s D9 Moon is in {d9_moon_sign}, house {d9_house}.",
            _citation(record["name"], "charts/D9.json", "PR-REL-D9-MOON"),
            "neutral",
        ))
        evidence.append(_dasha_evidence(record, (5, 7, 8), "REL", as_of.date()))
        evidence.append(_topic_transit_evidence(record, (5, 7, 8), "REL", as_of))
        evidence.append(_sav_evidence(record, (5, 7, 8), "REL"))
    guidance = Evidence(
        "Treat the two cited chart patterns as communication themes; consent and mutual conduct establish a relationship.",
        ("PRV1-POLICY-RELATIONSHIP", "PRV1"), "neutral",
    )
    return Reading(
        person=f"{first['name']} and {second['name']}", topic="relationship-compatibility",
        as_of=as_of.isoformat(), status="qualitative comparison", evidence=tuple(evidence),
        practical_guidance=guidance, sources=_source_bibliography(),
    )


def _source_bibliography() -> dict[str, str]:
    return {
        "BPHS-RS-1984": "Brihat Parashara Hora Shastra, R. Santhanam translation (1984).",
        "BVR-HTJH": "B. V. Raman, How to Judge a Horoscope, Volumes I and II.",
        "PRV1": "Ascendant Parashari-Raman v1 curated rule catalogue.",
    }


def _render_markdown(reading: Reading) -> str:
    lines = [
        f"# {reading.topic.replace('-', ' ').title()} — {reading.person}",
        "",
        f"**As of:** {reading.as_of} [sources: PRV1]  ",
        "",
        "## Natal promise",
        "",
        f"- Status: {reading.status}. [sources: PRV1]",
        "",
        "## Evidence",
        "",
    ]
    for item in reading.evidence:
        lines.append(f"- {item.statement} [sources: {'; '.join(item.citations)}]")
    lines.extend([
        "", "## Practical guidance", "",
        f"- {reading.practical_guidance.statement} [sources: {'; '.join(reading.practical_guidance.citations)}]",
        "", "## Sources", "",
    ])
    for source_id, source in reading.sources.items():
        lines.append(f"- {source_id}: {source}")
    return "\n".join(lines)


def _parse_datetime(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise ReadingError("date must be ISO 8601 with a timezone") from error
    if parsed.tzinfo is None:
        raise ReadingError("date must include a timezone")
    return parsed


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a deterministic, cited Parashari evidence ledger.",
    )
    _ = parser.add_argument("--name", required=True, help="Saved persons/<name> record")
    _ = parser.add_argument("--topic", required=True, choices=TOPICS)
    _ = parser.add_argument("--date", help="ISO 8601 moment with timezone")
    _ = parser.add_argument("--other-name", help="Second saved record for compatibility")
    _ = parser.add_argument("--family-role", choices=tuple(FAMILY_CONFIG))
    _ = parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        name = _safe_person_name(cast(str, args.name))
        topic = cast(Topic, args.topic)
        as_of = _parse_datetime(cast(str | None, args.date))
        if topic == "daily-transit":
            reading = _daily_transit_reading(name, as_of)
        elif topic == "relationship-compatibility":
            if not isinstance(args.other_name, str):
                raise ReadingError("relationship-compatibility requires --other-name")
            reading = _compatibility_reading(name, args.other_name, as_of)
        else:
            reading = _topic_reading(name, topic, as_of, cast(str | None, args.family_role))
    except ReadingError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(asdict(reading), indent=2))
    else:
        print(_render_markdown(reading))
    return 0


if __name__ == "__main__":
    sys.exit(main())
