"""Typed access to persisted ``persons/<name>`` records."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import NotRequired, TypedDict, cast, get_args

from ascendant.configuration import get_config
from ascendant.jaimini import JAIMINI_METHOD, JaiminiResult, calculate_jaimini
from ascendant.sav import AshtakavargaResult
from ascendant.types import (
    ALLOWED_DIVISIONS,
    HOUSES,
    RASHIS,
    ChartType,
    DashasType,
    HouseType,
)

_SIGNS = frozenset(get_args(RASHIS))
_CURRENT_SCHEMA_VERSION = 2
_CURRENT_RULE_PACK = "parashari_raman_jaimini_v3"
_LEGACY_RULE_PACKS = frozenset(
    ("parashari_raman_v1", "parashari_raman_v2")
)


class PersonRecordError(ValueError):
    """A persisted person record is missing or invalid."""


@dataclass(frozen=True)
class PersonRecordInput:
    """Birth input used to initialize one persisted person record."""

    name: str
    dob: datetime
    latitude: float
    longitude: float

    @property
    def input_hash(self) -> str:
        serialized = json.dumps(
            {
                "name": self.name,
                "dob": self.dob.isoformat(),
                "latitude": self.latitude,
                "longitude": self.longitude,
            },
            separators=(",", ":"),
        )
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


class Provenance(TypedDict):
    """Calculation metadata saved beside a person record."""

    schema_version: int
    rule_pack: str
    ayanamsa: str
    house_system: str
    input_hash: NotRequired[str]
    jaimini_method: NotRequired[str]


@dataclass(frozen=True)
class PersonRecord:
    """One validated direct child of a persons directory."""

    name: str
    directory: Path

    @property
    def context(self) -> dict[str, str]:
        path = self.directory / "CONTEXT.md"
        if not path.is_file():
            raise PersonRecordError(f"Missing required data: {path}")
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

    @property
    def coordinates(self) -> tuple[float, float]:
        fields = self.context
        try:
            return float(fields["latitude"]), float(fields["longitude"])
        except KeyError as error:
            raise PersonRecordError(
                f"CONTEXT.md is missing {error.args[0]}"
            ) from error
        except ValueError as error:
            raise PersonRecordError(
                "CONTEXT.md latitude and longitude must be decimal numbers"
            ) from error

    def chart(self, division: int) -> ChartType:
        path = self.directory / "charts" / f"D{division}.json"
        raw_chart = _mapping(_read_json(path), path)
        chart: ChartType = {}
        for number in range(1, 13):
            value = raw_chart.get(str(number))
            if not isinstance(value, dict):
                raise PersonRecordError(
                    f"Chart has no valid house {number} in {path}"
                )
            raw_house = _mapping(cast(object, value), path)
            sign = raw_house.get("sign")
            if not isinstance(sign, str) or sign not in _SIGNS:
                raise PersonRecordError(
                    f"Chart has no valid house {number} in {path}"
                )
            chart[cast(HOUSES, number)] = cast(
                HouseType,
                cast(object, raw_house),
            )
        return chart

    @property
    def d1(self) -> ChartType:
        return self.chart(1)

    @property
    def dasha(self) -> DashasType:
        from ascendant.dasha import DashaTimeline

        path = self.directory / "dasha.json"
        value = _read_json(path)
        if not isinstance(value, list):
            raise PersonRecordError(
                f"Expected a dasha timeline list in {path}"
            )
        items = cast(list[object], value)
        for item in items:
            if not isinstance(item, dict) or not all(
                field in item
                for field in (
                    "mahadasha",
                    "start",
                    "end",
                    "antardashas",
                )
            ):
                raise PersonRecordError(f"Invalid dasha entry in {path}")
            if not isinstance(item["antardashas"], list):
                raise PersonRecordError(f"Invalid dasha entry in {path}")
            antardashas = cast(list[object], item["antardashas"])
            for antardasha in antardashas:
                if not isinstance(antardasha, dict) or not all(
                    field in antardasha
                    for field in (
                        "mahadasha",
                        "antardasha",
                        "start",
                        "end",
                    )
                ):
                    raise PersonRecordError(
                        f"Invalid antardasha entry in {path}"
                    )
        timeline = cast(DashasType, cast(object, value))
        try:
            _ = DashaTimeline(timeline)
        except ValueError as error:
            raise PersonRecordError(
                f"Invalid dasha timeline in {path}: {error}"
            ) from error
        return timeline

    @property
    def sav(self) -> AshtakavargaResult:
        path = self.directory / "sav.json"
        value = _mapping(_read_json(path), path)
        if not isinstance(value.get("sarva"), dict):
            raise PersonRecordError(f"Expected SAV scores in {path}")
        return cast(AshtakavargaResult, cast(object, value))

    @property
    def jaimini(self) -> JaiminiResult:
        path = self.directory / "jaimini.json"
        value = _mapping(_read_json(path), path)
        if value.get("method") != JAIMINI_METHOD:
            raise PersonRecordError(f"Expected Jaimini method in {path}")
        if not isinstance(value.get("chara_karakas"), list):
            raise PersonRecordError(f"Expected Chara Karakas in {path}")
        return cast(JaiminiResult, cast(object, value))

    @property
    def provenance(self) -> Provenance | None:
        path = self.directory / "provenance.json"
        if not path.is_file():
            return None
        value = _mapping(_read_json(path), path)
        if not isinstance(value.get("schema_version"), int):
            raise PersonRecordError(
                f"Expected a provenance schema version in {path}"
            )
        for field in ("rule_pack", "ayanamsa", "house_system"):
            if not isinstance(value.get(field), str):
                raise PersonRecordError(
                    f"Expected provenance field {field} in {path}"
                )
        input_hash = value.get("input_hash")
        if input_hash is not None and not isinstance(input_hash, str):
            raise PersonRecordError(
                f"Expected provenance field input_hash in {path}"
            )
        jaimini_method = value.get("jaimini_method")
        if jaimini_method is not None and not isinstance(jaimini_method, str):
            raise PersonRecordError(
                f"Expected provenance field jaimini_method in {path}"
            )
        return cast(Provenance, cast(object, value))


def _read_json(path: Path) -> object:
    if not path.is_file():
        raise PersonRecordError(f"Missing required data: {path}")
    try:
        return cast(object, json.loads(path.read_text(encoding="utf-8")))
    except json.JSONDecodeError as error:
        raise PersonRecordError(f"Invalid JSON: {path}") from error


def _mapping(value: object, path: Path) -> dict[str, object]:
    if not isinstance(value, dict):
        raise PersonRecordError(f"Expected an object in {path}")
    mapping = cast(dict[object, object], value)
    if not all(isinstance(key, str) for key in mapping):
        raise PersonRecordError(f"Expected string keys in {path}")
    return cast(dict[str, object], mapping)


class PersonRecordStore:
    """Read and initialize persisted person records."""

    def __init__(self, root: Path | None = None) -> None:
        self.root: Path = Path("persons") if root is None else root

    def open(self, name: str) -> PersonRecord:
        self._validate_name(name)
        directory = self.root / name
        if not directory.is_dir():
            raise PersonRecordError(f"Missing person record: {directory}")
        return PersonRecord(name=name, directory=directory)

    def initialize(self, person: PersonRecordInput) -> PersonRecord:
        """Create or complete a deterministic persisted person record."""

        from ascendant import Ascendant

        self._validate_name(person.name)
        offset = person.dob.utcoffset()
        if offset is None:
            raise PersonRecordError("dob must be timezone-aware")

        person_hash = person.input_hash
        suffix = 1
        while True:
            record_name = (
                person.name if suffix == 1 else f"{person.name}_{suffix}"
            )
            directory = self.root / record_name
            hash_file = directory / "hash.txt"
            if not directory.exists():
                directory.mkdir(parents=True)
                _ = hash_file.write_text(person_hash, encoding="utf-8")
                break
            if (
                hash_file.is_file()
                and hash_file.read_text(encoding="utf-8").strip()
                == person_hash
            ):
                if self._has_saved_calculations(directory):
                    if self._has_known_rule_pack(directory):
                        self._backfill_jaimini(directory)
                        self._migrate_rule_pack(directory)
                    return PersonRecord(record_name, directory)
                break
            suffix += 1

        total_minutes = int(offset.total_seconds() // 60)
        hours, minutes = divmod(abs(total_minutes), 60)
        sign = "+" if total_minutes >= 0 else "-"
        utc = f"{sign}{hours:02}:{minutes:02}"

        charts_dir = directory / "charts"
        charts_dir.mkdir(exist_ok=True)
        context_file = directory / "CONTEXT.md"
        if not context_file.exists():
            context = "\n".join(
                (
                    "---",
                    f"name: {person.name}",
                    f"dob: {person.dob.strftime('%Y-%m-%d %H:%M')}",
                    f"utc: {utc}",
                    f"latitude: {person.latitude}",
                    f"longitude: {person.longitude}",
                    "---",
                )
            )
            _ = context_file.write_text(context, encoding="utf-8")

        ascendant = Ascendant(
            year=person.dob.year,
            month=person.dob.month,
            day=person.dob.day,
            hour=person.dob.hour,
            minute=person.dob.minute,
            second=person.dob.second,
            latitude=person.latitude,
            longitude=person.longitude,
            utc=utc,
        )
        divisions = cast(
            tuple[ALLOWED_DIVISIONS, ...],
            get_args(ALLOWED_DIVISIONS),
        )
        for division in divisions:
            chart = ascendant.get_chart(division)
            _write_json(charts_dir / f"D{division}.json", chart)

        dasha = ascendant.get_dasha_timeline()
        _write_json(directory / "dasha.json", dasha)

        yogas = ascendant.get_yogas()
        _write_json(directory / "yogas.json", yogas)
        _write_json(directory / "sav.json", ascendant.get_sav())
        _write_json(directory / "jaimini.json", ascendant.get_jaimini())

        config = get_config()
        _write_json(
            directory / "provenance.json",
            {
                "schema_version": _CURRENT_SCHEMA_VERSION,
                "rule_pack": _CURRENT_RULE_PACK,
                "jaimini_method": JAIMINI_METHOD,
                "ayanamsa": config.ayanamsa.value,
                "house_system": config.house_system.value,
                "input_hash": person_hash,
            },
        )
        return PersonRecord(record_name, directory)

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name or name in {".", ".."} or Path(name).name != name:
            raise PersonRecordError(
                "name must identify one direct persons/<name> record"
            )

    @staticmethod
    def _migrate_rule_pack(directory: Path) -> None:
        path = directory / "provenance.json"
        provenance = _mapping(_read_json(path), path)
        known_rule_packs = _LEGACY_RULE_PACKS | {_CURRENT_RULE_PACK}
        if provenance.get("rule_pack") not in known_rule_packs:
            return
        if (
            provenance.get("schema_version") == _CURRENT_SCHEMA_VERSION
            and provenance.get("rule_pack") == _CURRENT_RULE_PACK
            and provenance.get("jaimini_method") == JAIMINI_METHOD
        ):
            return
        provenance["schema_version"] = _CURRENT_SCHEMA_VERSION
        provenance["rule_pack"] = _CURRENT_RULE_PACK
        provenance["jaimini_method"] = JAIMINI_METHOD
        _write_json(path, provenance)

    @staticmethod
    def _backfill_jaimini(directory: Path) -> None:
        path = directory / "jaimini.json"
        if path.is_file():
            return
        record = PersonRecord(directory.name, directory)
        _write_json(path, calculate_jaimini(record.d1, record.chart(9)))

    @staticmethod
    def _has_known_rule_pack(directory: Path) -> bool:
        path = directory / "provenance.json"
        provenance = _mapping(_read_json(path), path)
        return provenance.get("rule_pack") in (
            _LEGACY_RULE_PACKS | {_CURRENT_RULE_PACK}
        )

    @staticmethod
    def _has_saved_calculations(directory: Path) -> bool:
        divisions = cast(
            tuple[ALLOWED_DIVISIONS, ...],
            get_args(ALLOWED_DIVISIONS),
        )
        required = (
            directory / "CONTEXT.md",
            directory / "dasha.json",
            directory / "yogas.json",
            directory / "sav.json",
            directory / "provenance.json",
            *(
                directory / "charts" / f"D{division}.json"
                for division in divisions
            ),
        )
        return all(path.is_file() for path in required)


def _write_json(path: Path, value: object) -> None:
    with path.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
