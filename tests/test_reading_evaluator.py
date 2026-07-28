"""Public CLI tests for deterministic personal-chart reading evidence."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
EVALUATOR = (
    REPOSITORY
    / "plugins/agent/ascendant/skills/parashari-judgement/scripts"
    / "evaluate-reading.py"
)
GET_TRANSIT = (
    REPOSITORY
    / "plugins/agent/ascendant/skills/get-transit/scripts/get-transit.py"
)
INIT_PERSON = (
    REPOSITORY
    / "plugins/agent/ascendant/skills/init-person/scripts/init-person.py"
)


def _chart() -> dict[str, dict[str, object]]:
    chart: dict[str, dict[str, object]] = {}
    signs = (
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
    )
    for house, sign in enumerate(signs, start=1):
        chart[str(house)] = {"sign": sign, "planets": [], "lagna": None}

    chart["1"] = {
        "sign": "Aries",
        "planets": [],
        "lagna": {
            "name": "Lagna",
            "longitude": 5.0,
            "is_retrograde": False,
            "sign": {
                "name": "Aries",
                "lord": "Mars",
                "nakshatra": {"name": "Ashwini", "lord": "Ketu", "pada": 1},
            },
        },
    }
    chart["6"]["planets"] = [
        {
            "name": "Mercury",
            "longitude": 155.0,
            "is_retrograde": False,
            "inSign": ["Own"],
            "sign": {
                "name": "Virgo",
                "lord": "Mercury",
                "nakshatra": {"name": "Hasta", "lord": "Moon", "pada": 1},
            },
        }
    ]
    chart["4"]["planets"] = [
        {
            "name": "Moon",
            "longitude": 95.0,
            "is_retrograde": False,
            "inSign": ["Own"],
            "sign": {
                "name": "Cancer",
                "lord": "Moon",
                "nakshatra": {"name": "Pushya", "lord": "Saturn", "pada": 1},
            },
        }
    ]
    chart["10"]["planets"] = [
        {
            "name": "Saturn",
            "longitude": 275.0,
            "is_retrograde": False,
            "inSign": ["Own"],
            "sign": {
                "name": "Capricorn",
                "lord": "Saturn",
                "nakshatra": {"name": "Shravana", "lord": "Moon", "pada": 1},
            },
        }
    ]
    return chart


def _write_person(workspace: Path, name: str = "Ada") -> None:
    person = workspace / "persons" / name
    charts = person / "charts"
    charts.mkdir(parents=True)
    (person / "CONTEXT.md").write_text(
        "---\nname: Ada\ndob: 1990-01-01 12:00\nutc: +05:30\n"
        "latitude: 28.6139\nlongitude: 77.2090\n---\n",
        encoding="utf-8",
    )
    for division in (1, 9, 10):
        (charts / f"D{division}.json").write_text(
            json.dumps(_chart()), encoding="utf-8"
        )
    (person / "dasha.json").write_text(
        json.dumps(
            [
                {
                    "mahadasha": "Saturn",
                    "start": "01-01-2020",
                    "end": "01-01-2040",
                    "antardashas": [
                        {
                            "mahadasha": "Saturn",
                            "antardasha": "Saturn",
                            "start": "01-01-2025",
                            "end": "01-01-2027",
                        }
                    ],
                }
            ]
        ),
        encoding="utf-8",
    )
    (person / "provenance.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "rule_pack": "parashari_raman_v1",
                "ayanamsa": "Lahiri",
                "house_system": "Whole Sign",
            }
        ),
        encoding="utf-8",
    )
    (person / "sav.json").write_text(
        json.dumps(
            {
                "sarva": {
                    sign: 28
                    for sign in (
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
                    )
                }
            }
        ),
        encoding="utf-8",
    )


def test_career_evaluator_emits_cited_deterministic_ledger(
    tmp_path: Path,
) -> None:
    _write_person(tmp_path)
    environment = os.environ | {"PYTHONPATH": str(REPOSITORY)}

    result = subprocess.run(
        [
            sys.executable,
            str(EVALUATOR),
            "--name",
            "Ada",
            "--topic",
            "career",
            "--date",
            "2026-07-28T12:00:00+05:30",
        ],
        cwd=tmp_path,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "## Natal promise" in result.stdout
    assert "supported" in result.stdout
    assert "[sources:" in result.stdout
    assert "PR-CAR-" in result.stdout
    assert "D1.json" in result.stdout
    assert "Computed transit" in result.stdout


def test_init_person_backfills_provenance_without_rewriting_context(
    tmp_path: Path,
) -> None:
    environment = os.environ | {"PYTHONPATH": str(REPOSITORY)}
    command = [
        sys.executable,
        str(INIT_PERSON),
        "--name",
        "Ada",
        "--dob",
        "1990-01-01T12:00:00+05:30",
        "--latitude",
        "28.6139",
        "--longitude",
        "77.2090",
    ]

    first = subprocess.run(
        command,
        cwd=tmp_path,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    assert first.returncode == 0, first.stderr
    context = tmp_path / "persons/Ada/CONTEXT.md"
    original_context = context.read_text(encoding="utf-8")
    provenance = tmp_path / "persons/Ada/provenance.json"
    assert (
        json.loads(provenance.read_text(encoding="utf-8"))["rule_pack"]
        == "parashari_raman_v1"
    )

    provenance.unlink()
    second = subprocess.run(
        command,
        cwd=tmp_path,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )

    assert second.returncode == 0, second.stderr
    assert context.read_text(encoding="utf-8") == original_context
    assert provenance.is_file()


def test_evaluator_rejects_a_person_path_outside_the_named_record(
    tmp_path: Path,
) -> None:
    _write_person(tmp_path)
    environment = os.environ | {"PYTHONPATH": str(REPOSITORY)}

    result = subprocess.run(
        [
            sys.executable, str(EVALUATOR), "--name", "../Ada", "--topic",
            "career", "--date", "2026-07-28T12:00:00+05:30",
        ],
        cwd=tmp_path,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "one direct persons/<name> record" in result.stderr


def test_compatibility_and_daily_transit_keep_personal_data_citations(
    tmp_path: Path,
) -> None:
    _write_person(tmp_path, "Ada")
    _write_person(tmp_path, "Bea")
    environment = os.environ | {"PYTHONPATH": str(REPOSITORY)}

    compatibility = subprocess.run(
        [
            sys.executable, str(EVALUATOR), "--name", "Ada", "--other-name",
            "Bea", "--topic", "relationship-compatibility", "--date",
            "2026-07-28T12:00:00+05:30",
        ],
        cwd=tmp_path,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    daily = subprocess.run(
        [
            sys.executable, str(EVALUATOR), "--name", "Ada", "--topic",
            "daily-transit", "--date", "2026-07-28T12:00:00+05:30",
        ],
        cwd=tmp_path,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )

    assert compatibility.returncode == 0, compatibility.stderr
    assert "Vimshottari" in compatibility.stdout
    assert "Computed transit" in compatibility.stdout
    assert "Supplementary SAV" in compatibility.stdout
    assert daily.returncode == 0, daily.stderr
    assert "persons/Ada/CONTEXT.md" in daily.stdout
    assert "persons/Ada/charts/D1.json" in daily.stdout


def test_person_tools_reject_paths_outside_persons_directory(
    tmp_path: Path,
) -> None:
    environment = os.environ | {"PYTHONPATH": str(REPOSITORY)}
    commands = (
        [
            sys.executable, str(INIT_PERSON), "--name", "../Ada",
            "--dob", "1990-01-01T12:00:00+05:30", "--latitude", "28.6139",
            "--longitude", "77.2090",
        ],
        [
            sys.executable, str(GET_TRANSIT), "--name", "../Ada",
            "--date", "2026-07-28T12:00:00+05:30",
        ],
    )

    for command in commands:
        result = subprocess.run(
            command, cwd=tmp_path, env=environment, check=False,
            capture_output=True, text=True,
        )
        assert result.returncode == 2
        assert "one direct persons/<name> record" in result.stderr
