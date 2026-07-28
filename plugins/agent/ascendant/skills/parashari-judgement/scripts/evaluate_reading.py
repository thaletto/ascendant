#!/usr/bin/env python3
"""Emit a deterministic, cited Parashari evidence ledger for saved charts."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
import json
from pathlib import Path
import sys
from typing import Literal, TypedDict, cast

from ascendant import Ascendant
from ascendant.sav import AshtakavargaResult
from ascendant.types import (
    ChartType,
    DashasType,
    HOUSES,
    HouseType,
    PLANETS,
    PlanetType,
    RASHI_LORDS,
    RASHIS,
)


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

SIGNS: tuple[RASHIS, ...] = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
    "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)
SIGN_LORDS: dict[RASHIS, RASHI_LORDS] = {
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


class Provenance(TypedDict):
    """Saved calculation metadata for a personal chart record."""

    schema_version: int
    rule_pack: str
    ayanamsa: str
    house_system: str


@dataclass(frozen=True)
class PersonRecord:
    """Typed persisted inputs for one named personal-chart reading."""

    name: str
    directory: Path
    d1: ChartType
    dasha: DashasType
    sav: AshtakavargaResult
    provenance: Provenance | None
    context: dict[str, str]
    varga: ChartType | None = None


class ReadingError(ValueError):
    """An input record cannot support the requested deterministic reading."""


def _safe_person_name(name: str) -> str:
    if not name or name in {".", ".."} or Path(name).name != name:
        raise ReadingError(
            "name must identify one direct persons/<name> record")
    return name


def _read_json(path: Path) -> object:
    if not path.is_file():
        raise ReadingError(f"Missing required data: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ReadingError(f"Invalid JSON: {path}") from error


def _optional_json(path: Path) -> object | None:
    if not path.is_file():
        return None
    return _read_json(path)


def _mapping(value: object, path: Path) -> dict[str, object]:
    if not isinstance(value, dict) or not all(
        isinstance(key, str) for key in value
    ):
        raise ReadingError(f"Expected an object in {path}")
    return cast(dict[str, object], value)


def _chart_from_json(value: object, path: Path) -> ChartType:
    raw_chart = _mapping(value, path)
    chart: ChartType = {}
    for number in range(1, 13):
        raw_house = _mapping(raw_chart.get(str(number)), path)
        sign = raw_house.get("sign")
        if not isinstance(sign, str) or sign not in SIGNS:
            raise ReadingError(f"Chart has no valid house {number} in {path}")
        chart[cast(HOUSES, number)] = cast(HouseType, raw_house)
    return chart


def _dashas_from_json(value: object, path: Path) -> DashasType:
    if not isinstance(value, list) or not all(
        isinstance(item, dict) for item in value
    ):
        raise ReadingError(f"Expected a dasha timeline list in {path}")
    return cast(DashasType, value)


def _sav_from_json(value: object, path: Path) -> AshtakavargaResult:
    raw_sav = _mapping(value, path)
    if not isinstance(raw_sav.get("sarva"), dict):
        raise ReadingError(f"Expected SAV scores in {path}")
    return cast(AshtakavargaResult, raw_sav)


def _provenance_from_json(
    value: object | None, path: Path
) -> Provenance | None:
    if value is None:
        return None
    provenance = _mapping(value, path)
    if not isinstance(provenance.get("schema_version"), int):
        raise ReadingError(f"Expected a provenance schema version in {path}")
    for field in ("rule_pack", "ayanamsa", "house_system"):
        if not isinstance(provenance.get(field), str):
            raise ReadingError(f"Expected provenance field {field} in {path}")
    return cast(Provenance, provenance)


def _load_record(name: str, required_varga: int | None) -> PersonRecord:
    safe_name = _safe_person_name(name)
    directory = Path("persons") / safe_name
    context = directory / "CONTEXT.md"
    if not context.is_file():
        raise ReadingError(f"Missing required data: {context}")
    charts = directory / "charts"
    d1_path = charts / "D1.json"
    dasha_path = directory / "dasha.json"
    sav_path = directory / "sav.json"
    provenance_path = directory / "provenance.json"
    varga = None
    if required_varga is not None:
        varga_path = charts / f"D{required_varga}.json"
        varga = _chart_from_json(_read_json(varga_path), varga_path)
    return PersonRecord(
        name=safe_name,
        directory=directory,
        d1=_chart_from_json(_read_json(d1_path), d1_path),
        dasha=_dashas_from_json(_read_json(dasha_path), dasha_path),
        sav=_sav_from_json(_read_json(sav_path), sav_path),
        provenance=_provenance_from_json(
            _optional_json(provenance_path), provenance_path
        ),
        context=_context_fields(context),
        varga=varga,
    )


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


def _house(chart: ChartType, number: int) -> HouseType:
    if number not in range(1, 13):
        raise ReadingError(f"Chart has no valid house {number}")
    return chart[cast(HOUSES, number)]


def _planet(
    chart: ChartType, name: PLANETS
) -> tuple[HOUSES, PlanetType] | None:
    for house_number in range(1, 13):
        for planet in _house(chart, house_number).get("planets", []):
            if planet["name"] == name:
                return cast(HOUSES, house_number), planet
    return None


def _citation(person: str, file_name: str, rule_id: str) -> tuple[str, ...]:
    return (
        f"persons/{person}/{file_name}", rule_id, *SOURCE_IDS,
    )


def _house_evidence(
    person: str,
    chart: ChartType,
    chart_label: str,
    topic_prefix: str,
    house_number: int,
) -> Evidence:
    house = _house(chart, house_number)
    sign = house["sign"]
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
    dignity_text = (
        ", ".join(str(item) for item in dignity) or "no dignity label"
    )
    if any(
        item in dignity
        for item in ("Exalted", "Moola Trikona", "Own", "Friend")
    ):
        polarity: Literal["support", "constraint", "neutral", "missing"] = (
            "support"
        )
        phrase = "supports"
    elif (
        any(item in dignity for item in ("Debilitated", "Enemy"))
        or lord_house in (6, 8, 12)
    ):
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


def _provenance_evidence(
    record: PersonRecord, topic_prefix: str
) -> Evidence:
    citations = _citation(
        record.name, "provenance.json", f"PR-{topic_prefix}-PROVENANCE",
    )
    provenance = record.provenance
    if provenance is None:
        return Evidence(
            "This legacy record has no saved calculation provenance.",
            citations,
            "neutral",
        )
    ayanamsa = provenance["ayanamsa"]
    house_system = provenance["house_system"]
    rule_pack = provenance["rule_pack"]
    return Evidence(
        f"Calculation provenance is {ayanamsa}, {house_system}, "
        f"and {rule_pack}.",
        citations,
        "neutral",
    )


def _active_dasha(
    dasha: DashasType, as_of: date
) -> tuple[PLANETS, PLANETS] | None:
    for maha in dasha:
        start = _dasha_date(maha["start"])
        end = _dasha_date(maha["end"])
        if start is None or end is None or not start <= as_of <= end:
            continue
        for antar in maha["antardashas"]:
            antar_start = _dasha_date(antar["start"])
            antar_end = _dasha_date(antar["end"])
            if antar_start and antar_end and antar_start <= as_of <= antar_end:
                return maha["mahadasha"], antar["antardasha"]
    return None


def _dasha_date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%d-%m-%Y").date()
    except ValueError:
        return None


def _dasha_evidence(
    record: PersonRecord,
    primary_houses: tuple[int, ...],
    topic_prefix: str,
    as_of: date,
) -> Evidence:
    active = _active_dasha(record.dasha, as_of)
    citations = _citation(
        record.name, "dasha.json", f"PR-{topic_prefix}-DASHA")
    if active is None:
        return Evidence(
            "No active Vimshottari period is available for "
            f"{as_of.isoformat()}.",
            citations,
            "missing",
        )
    relevant_planets = {
        SIGN_LORDS[_house(record.d1, house)["sign"]]
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
    record: PersonRecord,
    primary_houses: tuple[int, ...],
    topic_prefix: str,
) -> Evidence:
    sarva = record.sav["sarva"]
    citations = _citation(record.name, "sav.json", f"PR-{topic_prefix}-SAV")
    scores: list[str] = []
    for house_number in primary_houses:
        sign = _house(record.d1, house_number)["sign"]
        scores.append(f"house {house_number} ({sign}) = {sarva[sign]}")
    if not scores:
        return Evidence(
            "No relevant SAV scores are available for this topic.",
            citations,
            "missing")
    return Evidence(
        "Supplementary SAV scores: " + "; ".join(scores) + ".",
        citations,
        "neutral",
    )


def _transit_chart(record: PersonRecord, as_of: datetime) -> ChartType:
    fields = record.context
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
    return Ascendant(
        year=as_of.year, month=as_of.month, day=as_of.day,
        hour=as_of.hour, minute=as_of.minute, second=as_of.second,
        latitude=latitude, longitude=longitude,
        utc=f"{sign}{hours:02}:{remainder:02}",
    ).get_chart(1)


def _topic_transit_evidence(
    record: PersonRecord,
    primary_houses: tuple[int, ...],
    topic_prefix: str,
    as_of: datetime,
) -> Evidence:
    transit = _transit_chart(record, as_of)
    natal_lagna = _house(record.d1, 1)["sign"]
    matches: list[str] = []
    for transit_house in range(1, 13):
        house = _house(transit, transit_house)
        natal_house = (
            SIGNS.index(house["sign"]) - SIGNS.index(natal_lagna)
        ) % 12 + 1
        if natal_house not in primary_houses:
            continue
        for planet in house.get("planets", []):
            matches.append(f"{planet['name']} in natal house {natal_house}")
    citations = (
        f"computed transit {as_of.isoformat()}",
        f"persons/{record.name}/CONTEXT.md",
        f"persons/{record.name}/charts/D1.json",
        f"PR-{topic_prefix}-TRANSIT",
        *SOURCE_IDS,
    )
    detail = "; ".join(matches)
    if not detail:
        detail = "no planets in the selected natal houses"
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
            raise ReadingError(
                "family requires --family-role: mother, father, sibling, "
                "child, or household"
            )
        primary_houses = FAMILY_CONFIG[family_role]
        required_varga = None
        title = f"Family ({family_role})"
    else:
        primary_houses, required_varga, title = TOPIC_CONFIG[topic]
    record = _load_record(name, required_varga)
    prefix = topic.replace("-", "").upper()[:3]
    evidence = [_provenance_evidence(record, prefix)] + [
        _house_evidence(
            record.name, record.d1, "charts/D1.json", prefix, house
        )
        for house in primary_houses
    ]
    if required_varga is not None and record.varga is not None:
        evidence.extend(
            _house_evidence(
                record.name,
                record.varga,
                f"charts/D{required_varga}.json",
                prefix, house,
            )
            for house in primary_houses
        )
    evidence.append(
        _dasha_evidence(record, primary_houses, prefix, as_of.date())
    )
    evidence.append(
        _topic_transit_evidence(record, primary_houses, prefix, as_of)
    )
    evidence.append(_sav_evidence(record, primary_houses, prefix))
    frozen_evidence = tuple(evidence)
    status = _status(frozen_evidence, required_varga is not None)
    guidance = Evidence(
        f"Use the {title.lower()} evidence as planning context, "
        "not certainty.",
        ("PRV1-POLICY-001", "PRV1"),
        "neutral",
    )
    return Reading(
        person=record.name,
        topic=topic,
        as_of=as_of.isoformat(),
        status=status,
        evidence=frozen_evidence,
        practical_guidance=guidance,
        sources=_source_bibliography(),
    )


def _daily_transit_reading(name: str, as_of: datetime) -> Reading:
    record = _load_record(name, None)
    transit = _transit_chart(record, as_of)
    natal_lagna = _house(record.d1, 1)["sign"]
    evidence: list[Evidence] = []
    for house_number in range(1, 13):
        house = _house(transit, house_number)
        for planet in house.get("planets", []):
            sign_name = house["sign"]
            natal_house = (
                SIGNS.index(sign_name) - SIGNS.index(natal_lagna)
            ) % 12 + 1
            evidence.append(Evidence(
                f"{planet['name']} transits {sign_name}, "
                f"the natal house {natal_house}.",
                (
                    f"computed transit {as_of.isoformat()}",
                    f"persons/{record.name}/CONTEXT.md",
                    f"persons/{record.name}/charts/D1.json",
                    "PR-DAI-TRANSIT", "BPHS-RS-1984", "PRV1",
                ),
                "neutral",
            ))
    guidance = Evidence(
        "Use the dated transit facts to plan the next few days, "
        "not to promise an event.",
        ("PRV1-POLICY-001", "PRV1"), "neutral",
    )
    return Reading(
        person=record.name, topic="daily-transit", as_of=as_of.isoformat(),
        status="factual transit report", evidence=tuple(evidence),
        practical_guidance=guidance, sources=_source_bibliography(),
    )


def _compatibility_reading(
    name: str, other_name: str, as_of: datetime
) -> Reading:
    first = _load_record(name, 9)
    second = _load_record(other_name, 9)
    evidence: list[Evidence] = []
    for record in (first, second):
        moon = _planet(record.d1, "Moon")
        if moon is None:
            raise ReadingError(
                f"Missing Moon placement in {record.name}'s D1 chart")
        moon_house, moon_data = moon
        moon_sign = moon_data["sign"]["name"]
        evidence.append(Evidence(
            f"{record.name}'s Moon is in {moon_sign}, house {moon_house}.",
            _citation(record.name, "charts/D1.json", "PR-REL-MOON"),
            "neutral",
        ))
        if record.varga is None:
            raise ReadingError(f"Missing D9 chart for {record.name}")
        d9_moon = _planet(record.varga, "Moon")
        if d9_moon is None:
            raise ReadingError(
                f"Missing Moon placement in {record.name}'s D9 chart")
        d9_house, d9_moon_data = d9_moon
        d9_moon_sign = d9_moon_data["sign"]["name"]
        evidence.append(Evidence(
            f"{record.name}'s D9 Moon is in {d9_moon_sign}, "
            f"house {d9_house}.",
            _citation(record.name, "charts/D9.json", "PR-REL-D9-MOON"),
            "neutral",
        ))
        evidence.append(
            _dasha_evidence(record, (5, 7, 8), "REL", as_of.date())
        )
        evidence.append(
            _topic_transit_evidence(record, (5, 7, 8), "REL", as_of)
        )
        evidence.append(_sav_evidence(record, (5, 7, 8), "REL"))
    guidance = Evidence(
        "Treat the two cited chart patterns as communication themes; "
        "consent and mutual conduct establish a relationship.",
        ("PRV1-POLICY-RELATIONSHIP", "PRV1"), "neutral",
    )
    return Reading(
        person=f"{first.name} and {second.name}",
        topic="relationship-compatibility",
        as_of=as_of.isoformat(),
        status="qualitative comparison",
        evidence=tuple(evidence),
        practical_guidance=guidance,
        sources=_source_bibliography(),
    )


def _source_bibliography() -> dict[str, str]:
    return {
        "BPHS-RS-1984": (
            "Brihat Parashara Hora Shastra, R. Santhanam translation (1984)."
        ),
        "BVR-HTJH": (
            "B. V. Raman, How to Judge a Horoscope, Volumes I and II."
        ),
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
        lines.append(
            f"- {item.statement} [sources: {'; '.join(item.citations)}]")
    guidance_sources = "; ".join(reading.practical_guidance.citations)
    lines.extend([
        "", "## Practical guidance", "",
        "- "
        f"{reading.practical_guidance.statement} "
        f"[sources: {guidance_sources}]",
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
    _ = parser.add_argument("--name", required=True,
                            help="Saved persons/<name> record")
    _ = parser.add_argument("--topic", required=True, choices=TOPICS)
    _ = parser.add_argument("--date", help="ISO 8601 moment with timezone")
    _ = parser.add_argument(
        "--other-name", help="Second saved record for compatibility")
    _ = parser.add_argument("--family-role", choices=tuple(FAMILY_CONFIG))
    _ = parser.add_argument(
        "--format", choices=("markdown", "json"), default="markdown")
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
                raise ReadingError(
                    "relationship-compatibility requires --other-name")
            reading = _compatibility_reading(name, args.other_name, as_of)
        else:
            reading = _topic_reading(
                name, topic, as_of, cast(str | None, args.family_role))
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
