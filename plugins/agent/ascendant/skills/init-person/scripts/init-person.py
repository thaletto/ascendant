#!/usr/bin/env python3
import argparse
import sys
from dataclasses import dataclass
from datetime import datetime

from ascendant.person_record import (
    PersonRecordError,
    PersonRecordInput,
    PersonRecordStore,
)

Person = PersonRecordInput


@dataclass
class Arguments:
    name: object = ""
    dob: object = ""
    latitude: object = 0.0
    longitude: object = 0.0


def init_person(person: Person) -> str:
    """Initialize or complete a person record and return its absolute path."""

    record = PersonRecordStore().initialize(person)
    return str(record.directory.resolve())


def parse_args(argv: list[str] | None = None) -> PersonRecordInput:
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
    args = parser.parse_args(argv, namespace=Arguments())

    name = args.name
    dob = args.dob
    latitude = args.latitude
    longitude = args.longitude
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    if not isinstance(dob, str):
        raise TypeError("dob must be an ISO 8601 string")
    if not isinstance(latitude, float) or not isinstance(longitude, float):
        raise TypeError("latitude and longitude must be decimal numbers")

    return PersonRecordInput(
        name=name,
        dob=datetime.fromisoformat(dob),
        latitude=latitude,
        longitude=longitude,
    )


def main(argv: list[str] | None = None) -> int:
    try:
        person = parse_args(argv)
    except (PersonRecordError, TypeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    try:
        directory = init_person(person)
    except PersonRecordError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    except Exception as error:  # noqa: BLE001
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(directory)
    return 0


if __name__ == "__main__":
    sys.exit(main())
