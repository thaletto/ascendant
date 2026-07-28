#!/usr/bin/env python3
"""Emit a deterministic, cited Parashari evidence ledger for saved charts."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from html import escape
from pathlib import Path
from typing import Literal, TypedDict, cast

from ascendant import Ascendant
from ascendant.sav import AshtakavargaResult
from ascendant.types import (
    HOUSES,
    PLANETS,
    RASHI_LORDS,
    RASHIS,
    ChartType,
    DashasType,
    HouseType,
    PlanetType,
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
OutputFormat = Literal["markdown", "json"]

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


@dataclass
class Arguments:
    """Typed command-line values populated by argparse."""

    name: str = ""
    topic: Topic = "career"
    date: str | None = None
    other_name: str | None = None
    family_role: str | None = None
    output_format: OutputFormat = "markdown"
    html: bool = False


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
        return cast(object, json.loads(path.read_text(encoding="utf-8")))
    except json.JSONDecodeError as error:
        raise ReadingError(f"Invalid JSON: {path}") from error


def _optional_json(path: Path) -> object | None:
    if not path.is_file():
        return None
    return _read_json(path)


def _mapping(value: object, path: Path) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ReadingError(f"Expected an object in {path}")
    mapping = cast(dict[object, object], value)
    if not all(isinstance(key, str) for key in mapping):
        raise ReadingError(f"Expected string keys in {path}")
    return cast(dict[str, object], mapping)


def _chart_from_json(value: object, path: Path) -> ChartType:
    raw_chart = _mapping(value, path)
    chart: ChartType = {}
    for number in range(1, 13):
        raw_house = _mapping(raw_chart.get(str(number)), path)
        sign = raw_house.get("sign")
        if not isinstance(sign, str) or sign not in SIGNS:
            raise ReadingError(f"Chart has no valid house {number} in {path}")
        chart[cast(HOUSES, number)] = cast(
            HouseType, cast(object, raw_house)
        )
    return chart


def _dashas_from_json(value: object, path: Path) -> DashasType:
    if not isinstance(value, list):
        raise ReadingError(f"Expected a dasha timeline list in {path}")
    items = cast(list[object], value)
    if not all(isinstance(item, dict) for item in items):
        raise ReadingError(f"Expected dasha timeline entries in {path}")
    return cast(DashasType, cast(object, items))


def _sav_from_json(value: object, path: Path) -> AshtakavargaResult:
    raw_sav = _mapping(value, path)
    if not isinstance(raw_sav.get("sarva"), dict):
        raise ReadingError(f"Expected SAV scores in {path}")
    return cast(AshtakavargaResult, cast(object, raw_sav))


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
    return cast(Provenance, cast(object, provenance))


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
    dignity = planet["inSign"]
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
    statement = (
        f"House {house_number} is {sign}; {lord}, its lord, is in house "
        + f"{lord_house} with {dignity_text}, which {phrase} this topic."
    )
    return Evidence(
        statement,
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
    statement = (
        f"Calculation provenance is {ayanamsa}, {house_system}, "
        + f"and {rule_pack}."
    )
    return Evidence(
        statement,
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
        return datetime.strptime(value, "%d-%m-%Y").replace(
            tzinfo=UTC
        ).date()
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
        statement = (
            "No active Vimshottari period is available for "
            + f"{as_of.isoformat()}."
        )
        return Evidence(
            statement,
            citations,
            "missing",
        )
    relevant_planets = {
        SIGN_LORDS[_house(record.d1, house)["sign"]]
        for house in primary_houses
    }
    activated = active[0] in relevant_planets and active[1] in relevant_planets
    result = "activates" if activated else "does not jointly activate"
    statement = (
        f"Vimshottari {active[0]}–{active[1]} is active on "
        + f"{as_of.isoformat()} and {result} the selected house lords; "
        + "timing requires both period lords to activate them."
    )
    return Evidence(
        statement,
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
            message = (
                "family requires --family-role: mother, father, sibling, "
                + "child, or household"
            )
            raise ReadingError(message)
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
    guidance_statement = (
        f"Use the {title.lower()} evidence as planning context, "
        + "not certainty."
    )
    guidance = Evidence(
        guidance_statement,
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
            statement = (
                f"{planet['name']} transits {sign_name}, "
                + f"the natal house {natal_house}."
            )
            evidence.append(Evidence(
                statement,
                (
                    f"computed transit {as_of.isoformat()}",
                    f"persons/{record.name}/CONTEXT.md",
                    f"persons/{record.name}/charts/D1.json",
                    "PR-DAI-TRANSIT", "BPHS-RS-1984", "PRV1",
                ),
                "neutral",
            ))
    guidance_statement = (
        "Use the dated transit facts to plan the next few days, "
        + "not to promise an event."
    )
    guidance = Evidence(
        guidance_statement,
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
        statement = (
            f"{record.name}'s D9 Moon is in {d9_moon_sign}, "
            + f"house {d9_house}."
        )
        evidence.append(Evidence(
            statement,
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
    guidance_statement = (
        "Treat the two cited chart patterns as communication themes; "
        + "consent and mutual conduct establish a relationship."
    )
    guidance = Evidence(
        guidance_statement,
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
    guidance_line = (
        f"- {reading.practical_guidance.statement} "
        + f"[sources: {guidance_sources}]"
    )
    lines.extend([
        "", "## Practical guidance", "",
        guidance_line,
        "", "## Sources", "",
    ])
    for source_id, source in reading.sources.items():
        lines.append(f"- {source_id}: {source}")
    return "\n".join(lines)


def _render_html_citations(citations: tuple[str, ...]) -> str:
    source_list = "; ".join(escape(source) for source in citations)
    marker = f"[sources: {source_list}]"
    return f'<span class="citations" aria-label="Sources">{marker}</span>'


def _render_html(reading: Reading) -> str:
    title = escape(reading.topic.replace("-", " ").title())
    person = escape(reading.person)
    as_of = escape(reading.as_of)
    status = escape(reading.status)
    status_class = escape(reading.status.replace(" ", "-").lower())
    as_of_citations = _render_html_citations(("PRV1",))
    status_citations = _render_html_citations(("PRV1",))
    evidence_items = "\n".join(
        f"""
        <li class="evidence evidence--{escape(item.polarity)}">
          <span class="evidence__marker" aria-hidden="true"></span>
          <p>{escape(item.statement)}
            {_render_html_citations(item.citations)}
          </p>
        </li>""".strip()
        for item in reading.evidence
    )
    guidance = escape(reading.practical_guidance.statement)
    guidance_citations = _render_html_citations(
        reading.practical_guidance.citations
    )
    source_items = "\n".join(
        f"""
        <div class="source">
          <dt>{escape(source_id)}</dt>
          <dd>{escape(source)}</dd>
        </div>""".strip()
        for source_id, source in reading.sources.items()
    )
    styles = """
    :root {
      color-scheme: dark;
      font-family:
        Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
      background: #090b14;
      color: #f7f1e8;
    }
    * { box-sizing: border-box; }
    body {
      min-height: 100vh;
      margin: 0;
      background:
        radial-gradient(circle at 15% 0%, #34245f 0, transparent 34rem),
        radial-gradient(circle at 90% 18%, #164d52 0, transparent 28rem),
        #090b14;
    }
    body::before {
      position: fixed;
      inset: 0;
      z-index: -1;
      content: "";
      opacity: 0.3;
      background-image:
        linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
      background-size: 48px 48px;
      mask-image: linear-gradient(to bottom, black, transparent 80%);
    }
    main {
      width: min(880px, calc(100% - 2rem));
      margin: 0 auto;
      padding: 4rem 0;
    }
    header, section {
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 1.25rem;
      background: rgba(16, 18, 31, 0.84);
      box-shadow: 0 1.5rem 4rem rgba(0, 0, 0, 0.26);
      backdrop-filter: blur(18px);
    }
    header {
      position: relative;
      overflow: hidden;
      padding: clamp(1.5rem, 5vw, 3.5rem);
    }
    header::after {
      position: absolute;
      width: 12rem;
      height: 12rem;
      right: -4rem;
      bottom: -6rem;
      border: 1px solid rgba(234, 190, 116, 0.38);
      border-radius: 50%;
      content: "";
      box-shadow:
        0 0 0 2rem rgba(234, 190, 116, 0.05),
        0 0 0 4rem rgba(234, 190, 116, 0.03);
    }
    .eyebrow {
      margin: 0 0 0.85rem;
      color: #eabe74;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.18em;
      text-transform: uppercase;
    }
    h1 {
      max-width: 14ch;
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      font-size: clamp(2.4rem, 7vw, 5rem);
      font-weight: 500;
      letter-spacing: -0.045em;
      line-height: 0.96;
    }
    .meta {
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
      align-items: center;
      margin-top: 2rem;
    }
    .status-wrap {
      display: inline-flex;
      gap: 0.65rem;
      align-items: center;
    }
    .status-wrap .citations {
      display: inline;
      margin-top: 0;
    }
    .status {
      display: inline-flex;
      padding: 0.48rem 0.78rem;
      border: 1px solid rgba(119, 227, 191, 0.35);
      border-radius: 999px;
      background: rgba(45, 145, 117, 0.17);
      color: #aaf1d9;
      font-size: 0.82rem;
      font-weight: 750;
      text-transform: capitalize;
    }
    .as-of {
      color: #b5b8c9;
      font-size: 0.86rem;
    }
    section {
      margin-top: 1rem;
      padding: clamp(1.25rem, 4vw, 2.25rem);
    }
    h2 {
      margin: 0 0 1.25rem;
      color: #f5dcae;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 1.55rem;
      font-weight: 500;
    }
    p { margin: 0; line-height: 1.72; }
    .evidence-list {
      display: grid;
      gap: 0.75rem;
      margin: 0;
      padding: 0;
      list-style: none;
    }
    .evidence {
      display: grid;
      grid-template-columns: 0.65rem 1fr;
      gap: 0.85rem;
      padding: 1rem;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 0.9rem;
      background: rgba(255, 255, 255, 0.035);
    }
    .evidence__marker {
      width: 0.52rem;
      height: 0.52rem;
      margin-top: 0.55rem;
      border-radius: 50%;
      background: #8f96aa;
      box-shadow: 0 0 1rem currentColor;
    }
    .evidence--support .evidence__marker { background: #77e3bf; }
    .evidence--constraint .evidence__marker { background: #ff9c82; }
    .evidence--missing .evidence__marker { background: #eabe74; }
    .citations {
      display: block;
      margin-top: 0.45rem;
      color: #9499ad;
      font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
      font-size: 0.72rem;
      line-height: 1.55;
      overflow-wrap: anywhere;
    }
    .guidance {
      padding-left: 1rem;
      border-left: 3px solid #eabe74;
    }
    .sources {
      display: grid;
      gap: 0.75rem;
      margin: 0;
    }
    .source {
      display: grid;
      grid-template-columns: minmax(7rem, 0.25fr) 1fr;
      gap: 1rem;
      padding-top: 0.75rem;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    .source:first-child { padding-top: 0; border-top: 0; }
    dt { color: #eabe74; font-weight: 800; }
    dd { margin: 0; color: #c6c8d3; line-height: 1.55; }
    @media (max-width: 560px) {
      main { padding: 1rem 0 2rem; }
      .source { grid-template-columns: 1fr; gap: 0.25rem; }
    }
    @media print {
      :root { color-scheme: light; background: white; color: #171717; }
      body { background: white; }
      body::before { display: none; }
      main { width: 100%; padding: 0; }
      header, section {
        border-color: #d7d7d7;
        background: white;
        box-shadow: none;
        break-inside: avoid;
      }
      .citations, .as-of, dd { color: #454545; }
    }
    """
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — {person} | Ascendant</title>
  <style>{styles}</style>
</head>
<body>
  <main>
    <header>
      <p class="eyebrow">Ascendant · cited reading</p>
      <h1>{title} — {person}</h1>
      <div class="meta">
        <span class="status-wrap">
          <span class="status status--{status_class}">{status}</span>
          {status_citations}
        </span>
        <span class="as-of">As of {as_of}{as_of_citations}</span>
      </div>
    </header>
    <section aria-labelledby="promise-heading">
      <h2 id="promise-heading">Natal promise</h2>
      <p>Status: {status}.{status_citations}</p>
    </section>
    <section aria-labelledby="evidence-heading">
      <h2 id="evidence-heading">Evidence</h2>
      <ol class="evidence-list">
        {evidence_items}
      </ol>
    </section>
    <section aria-labelledby="guidance-heading">
      <h2 id="guidance-heading">Practical guidance</h2>
      <p class="guidance">{guidance}{guidance_citations}</p>
    </section>
    <section aria-labelledby="sources-heading">
      <h2 id="sources-heading">Sources</h2>
      <dl class="sources">
        {source_items}
      </dl>
    </section>
  </main>
</body>
</html>"""


def _parse_datetime(value: str | None) -> datetime:
    if value is None:
        return datetime.now(UTC)
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise ReadingError("date must be ISO 8601 with a timezone") from error
    if parsed.tzinfo is None:
        raise ReadingError("date must include a timezone")
    return parsed


def parse_args(argv: list[str] | None = None) -> Arguments:
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
    output_group = parser.add_mutually_exclusive_group()
    _ = output_group.add_argument(
        "--html",
        action="store_true",
        help="Render a styled, standalone HTML reading",
    )
    _ = output_group.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        dest="output_format",
    )
    return parser.parse_args(argv, namespace=Arguments())


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        name = _safe_person_name(args.name)
        topic = args.topic
        as_of = _parse_datetime(args.date)
        if topic == "daily-transit":
            reading = _daily_transit_reading(name, as_of)
        elif topic == "relationship-compatibility":
            if not isinstance(args.other_name, str):
                raise ReadingError(
                    "relationship-compatibility requires --other-name")
            reading = _compatibility_reading(name, args.other_name, as_of)
        else:
            reading = _topic_reading(
                name, topic, as_of, args.family_role)
    except ReadingError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if args.html:
        print(_render_html(reading))
    elif args.output_format == "json":
        print(json.dumps(asdict(reading), indent=2))
    else:
        print(_render_markdown(reading))
    return 0


if __name__ == "__main__":
    sys.exit(main())
