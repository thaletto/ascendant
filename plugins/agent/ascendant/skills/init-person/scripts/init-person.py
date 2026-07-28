#!/usr/bin/env python3
import argparse
import hashlib
import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import cast, get_args

from ascendant import Ascendant
from ascendant.configuration import get_config
from ascendant.types import ALLOWED_DIVISIONS

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s %(message)s"
)


@dataclass(frozen=True)
class Person:
    name: str
    dob: datetime
    latitude: float
    longitude: float

    @property
    def hash(self) -> str:
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


def validate_name(name: str) -> str:
    if not name or name in {".", ".."} or Path(name).name != name:
        raise ValueError("name must identify one direct persons/<name> record")
    return name


def init_person(person: Person) -> str:
    """
    Creates a directory under persons/ containing the person's
    astrological data.
    Returns the absolute path of the created directory.
    Skips generation if a directory with the same hash already exists.
    If the name exists but the hash differs, a new directory with a numeric
    suffix is created.
    """
    person_hash = person.hash
    base = Path("persons")
    suffix = 1

    while True:
        directory = base / person.name
        if suffix != 1:
            directory = base / f"{person.name}_{suffix}"
        hash_file = directory / "hash.txt"

        if not directory.exists():
            directory.mkdir(parents=True)
            _ = hash_file.write_text(person_hash, encoding="utf-8")
            break

        if hash_file.exists():
            existing_hash = hash_file.read_text(encoding="utf-8").strip()
            if existing_hash == person_hash:
                sav_file = directory / "sav.json"
                provenance_file = directory / "provenance.json"
                if sav_file.exists() and provenance_file.exists():
                    logging.info(f"{directory} already exists. Skipping.")
                    return str(directory.resolve())
                logging.info(
                    "%s already exists. Generating missing derived data.",
                    directory,
                )
                break

        suffix += 1

    offset = person.dob.utcoffset()
    if offset is None:
        raise ValueError("dob must be timezone-aware")

    total_minutes = int(offset.total_seconds() // 60)
    hours, minutes = divmod(abs(total_minutes), 60)
    sign = "+" if total_minutes >= 0 else "-"
    utc = f"{sign}{hours:02}:{minutes:02}"

    charts_dir = directory / "charts"
    charts_dir.mkdir(exist_ok=True)

    context_file = directory / "CONTEXT.md"
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
    if not context_file.exists():
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

    logging.info(f"Initialized ascendant for {person.name}")

    divisions = cast(
        tuple[ALLOWED_DIVISIONS, ...], get_args(ALLOWED_DIVISIONS)
    )
    for division in divisions:
        chart = ascendant.get_chart(division)
        if chart is None:
            logging.warning(f"Failed to get chart for D{division}")
            continue
        chart_file = charts_dir / f"D{division}.json"
        with chart_file.open("w", encoding="utf-8") as f:
            json.dump(chart, f, indent=2, ensure_ascii=False)

    dasha = ascendant.get_dasha_timeline()
    if dasha is not None:
        with (directory / "dasha.json").open("w", encoding="utf-8") as f:
            json.dump(dasha, f, indent=2, ensure_ascii=False)
    else:
        logging.warning("Failed to get dasha timeline")

    yogas = ascendant.get_yogas()
    if yogas is not None:
        with (directory / "yogas.json").open("w", encoding="utf-8") as f:
            json.dump(yogas, f, indent=2, ensure_ascii=False)
    else:
        logging.warning("Failed to get yogas")

    sav = ascendant.get_sav()
    with (directory / "sav.json").open("w", encoding="utf-8") as f:
        json.dump(sav, f, indent=2, ensure_ascii=False)

    config = get_config()
    provenance = {
        "schema_version": 1,
        "rule_pack": "parashari_raman_v1",
        "ayanamsa": config.ayanamsa.value,
        "house_system": config.house_system.value,
        "input_hash": person_hash,
    }
    with (directory / "provenance.json").open("w", encoding="utf-8") as f:
        json.dump(provenance, f, indent=2, ensure_ascii=False)

    logging.info(f"Saved data for {person.name} to {directory}")
    return str(directory.resolve())


def parse_args(argv: list[str] | None = None) -> Person:
    parser = argparse.ArgumentParser(
        description="Initialize a native's astrological data directory."
    )
    _ = parser.add_argument(
        "--name", required=True, help="Native's display name"
    )
    _ = parser.add_argument(
        "--dob",
        required=True,
        help=(
            "Date and time of birth in ISO 8601 with timezone offset, "
            "e.g. 2003-08-19T11:55:00+05:30"
        ),
    )
    _ = parser.add_argument(
        "--latitude",
        required=True,
        type=float,
        help="Latitude in decimal degrees",
    )
    _ = parser.add_argument(
        "--longitude",
        required=True,
        type=float,
        help="Longitude in decimal degrees",
    )
    args = parser.parse_args(argv)

    name: object = args.name
    dob: object = args.dob
    latitude: object = args.latitude
    longitude: object = args.longitude
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    if not isinstance(dob, str):
        raise ValueError("dob must be an ISO 8601 string")
    if not isinstance(latitude, float) or not isinstance(longitude, float):
        raise ValueError("latitude and longitude must be decimal numbers")

    return Person(
        name=validate_name(name),
        dob=datetime.fromisoformat(dob),
        latitude=latitude,
        longitude=longitude,
    )


def main(argv: list[str] | None = None) -> int:
    try:
        person = parse_args(argv)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    directory = init_person(person)
    print(directory)
    return 0


if __name__ == "__main__":
    sys.exit(main())
