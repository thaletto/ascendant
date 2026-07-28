"""Public behavior tests for persisted person records."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest

from ascendant.person_record import (
    PersonRecordError,
    PersonRecordInput,
    PersonRecordStore,
)


def _write_record(root: Path, name: str = "Ada") -> Path:
    directory = root / name
    charts = directory / "charts"
    charts.mkdir(parents=True)
    _ = (directory / "CONTEXT.md").write_text(
        """---
name: Ada
dob: 1990-01-01 12:00
utc: +05:30
latitude: 28.6139
longitude: 77.2090
---
""",
        encoding="utf-8",
    )
    chart: dict[str, dict[str, object]] = {
        str(number): {
            "sign": sign,
            "planets": [],
            "lagna": None,
        }
        for number, sign in enumerate(
            (
                "Aries",
                "Taurus",
                "Gemini",
                "Cancer",
                "Leo",
                "Virgo",
                "Libra",
                "Scorpio",
                "Sagittarius",
                "Capricorn",
                "Aquarius",
                "Pisces",
            ),
            start=1,
        )
    }
    _ = (charts / "D1.json").write_text(
        json.dumps(chart),
        encoding="utf-8",
    )
    _ = (directory / "dasha.json").write_text(
        json.dumps(
            [
                {
                    "mahadasha": "Saturn",
                    "start": "01-01-2020",
                    "end": "01-01-2040",
                    "antardashas": [],
                }
            ]
        ),
        encoding="utf-8",
    )
    _ = (directory / "sav.json").write_text(
        json.dumps({"sarva": {"Aries": 28}}),
        encoding="utf-8",
    )
    return directory


@pytest.mark.parametrize("name", ("../Ada", ".", "group/Ada"))
def test_person_record_name_must_be_one_direct_child(
    tmp_path: Path,
    name: str,
) -> None:
    store = PersonRecordStore(tmp_path / "persons")

    with pytest.raises(
        PersonRecordError,
        match=r"one direct persons/<name> record",
    ):
        _ = store.open(name)


def test_person_record_exposes_typed_saved_data(tmp_path: Path) -> None:
    root = tmp_path / "persons"
    _ = _write_record(root)

    record = PersonRecordStore(root).open("Ada")

    assert record.coordinates == (28.6139, 77.209)
    assert record.chart(1)[1]["sign"] == "Aries"
    assert record.dasha[0]["mahadasha"] == "Saturn"
    assert record.sav["sarva"]["Aries"] == 28
    assert record.provenance is None


def test_person_record_rejects_malformed_dasha_entries(
    tmp_path: Path,
) -> None:
    root = tmp_path / "persons"
    directory = _write_record(root)
    _ = (directory / "dasha.json").write_text(
        json.dumps([{"mahadasha": "Saturn"}]),
        encoding="utf-8",
    )

    record = PersonRecordStore(root).open("Ada")

    with pytest.raises(PersonRecordError, match="Invalid dasha entry"):
        _ = record.dasha


def test_person_record_rejects_malformed_dasha_boundaries(
    tmp_path: Path,
) -> None:
    root = tmp_path / "persons"
    directory = _write_record(root)
    timeline = cast(
        list[dict[str, object]],
        cast(
            object,
            json.loads(
                (directory / "dasha.json").read_text(encoding="utf-8")
            ),
        ),
    )
    timeline[0]["end"] = "2040-01-01"
    _ = (directory / "dasha.json").write_text(
        json.dumps(timeline),
        encoding="utf-8",
    )

    record = PersonRecordStore(root).open("Ada")

    with pytest.raises(
        PersonRecordError,
        match="Invalid dasha timeline",
    ):
        _ = record.dasha


def test_person_record_reports_missing_and_malformed_saved_data(
    tmp_path: Path,
) -> None:
    root = tmp_path / "persons"
    directory = _write_record(root)
    record = PersonRecordStore(root).open("Ada")

    (directory / "sav.json").unlink()
    with pytest.raises(
        PersonRecordError,
        match=f"Missing required data: {directory / 'sav.json'}",
    ):
        _ = record.sav

    _ = (directory / "dasha.json").write_text("{", encoding="utf-8")
    with pytest.raises(
        PersonRecordError,
        match=f"Invalid JSON: {directory / 'dasha.json'}",
    ):
        _ = record.dasha

    chart = cast(
        dict[str, object],
        cast(
            object,
            json.loads(
                (directory / "charts/D1.json").read_text(encoding="utf-8")
            ),
        ),
    )
    del chart["12"]
    _ = (directory / "charts/D1.json").write_text(
        json.dumps(chart),
        encoding="utf-8",
    )
    with pytest.raises(PersonRecordError, match="no valid house 12"):
        _ = record.d1

    _ = (directory / "provenance.json").write_text(
        json.dumps({"schema_version": 1}),
        encoding="utf-8",
    )
    with pytest.raises(
        PersonRecordError,
        match="Expected provenance field rule_pack",
    ):
        _ = record.provenance


def test_matching_record_regenerates_complete_derived_set_without_context(
    tmp_path: Path,
) -> None:
    store = PersonRecordStore(tmp_path / "persons")
    person = PersonRecordInput(
        name="Ada",
        dob=datetime.fromisoformat("1990-01-01T12:00:00+05:30"),
        latitude=28.6139,
        longitude=77.2090,
    )
    record = store.initialize(person)
    context_before = (record.directory / "CONTEXT.md").read_bytes()
    d1 = record.directory / "charts/D1.json"
    d1.unlink()

    regenerated = store.initialize(person)

    assert regenerated.directory == record.directory
    assert d1.is_file()
    assert (record.directory / "CONTEXT.md").read_bytes() == context_before


def test_repeated_initialization_does_not_rewrite_complete_record(
    tmp_path: Path,
) -> None:
    store = PersonRecordStore(tmp_path / "persons")
    person = PersonRecordInput(
        name="Ada",
        dob=datetime.fromisoformat("1990-01-01T12:00:00+05:30"),
        latitude=28.6139,
        longitude=77.2090,
    )
    record = store.initialize(person)
    files = tuple(
        path for path in record.directory.rglob("*") if path.is_file()
    )
    for path in files:
        os.utime(path, (1_000_000_000, 1_000_000_000))
    mtimes_before = {path: path.stat().st_mtime_ns for path in files}

    repeated = store.initialize(person)

    assert repeated.directory == record.directory
    assert {path: path.stat().st_mtime_ns for path in files} == mtimes_before
