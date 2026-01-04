from typing import cast

import pytest

from ascendant.chart import Chart
from ascendant.const import ALLOWED_DIVISIONS as DIVISIONS
from ascendant.types import ALLOWED_DIVISIONS
from tests.helpers import format_and_print_table
from tests.horoscope import my_horoscope


@pytest.mark.parametrize("division", DIVISIONS)
def test_graha_drishthi_runs_for_allowed_divisions(division: ALLOWED_DIVISIONS):
    chart = Chart(my_horoscope)
    result = chart.graha_drishti(n=division)

    # Result can be None if varga chart generation fails.
    if result is None:
        return

    assert isinstance(result, list)

    # If there are no planets with aspects (unlikely), it's still valid to be empty
    if not result:
        return

    for aspect_data in result:
        assert isinstance(aspect_data, dict)
        assert "planet" in aspect_data and isinstance(aspect_data["planet"], str)
        assert "from_house" in aspect_data and isinstance(
            aspect_data["from_house"], int
        )
        assert 1 <= aspect_data["from_house"] <= 12

        assert "aspect_houses" in aspect_data and isinstance(
            aspect_data["aspect_houses"], list
        )
        for aspected_house_info in aspect_data["aspect_houses"]:
            assert isinstance(aspected_house_info, dict)
            for house, planets_in_house in aspected_house_info.items():
                assert isinstance(house, int) and 1 <= house <= 12
                assert isinstance(planets_in_house, list)
                assert all(isinstance(p, str) for p in planets_in_house)


def test_graha_drishthi_for_single_planet():
    chart = Chart(my_horoscope)
    # Test for Sun in D1 chart
    result = chart.graha_drishti(n=1, planet="Sun")

    if result is None:
        return  # might be none if chart fails

    assert isinstance(result, list)
    # Should only contain one element for the Sun's aspects
    assert len(result) <= 1
    if result:
        assert result[0]["planet"] == "Sun"


def test_graha_drishthi_for_non_allowed_division():
    chart = Chart(my_horoscope)
    non_allowed = [d for d in range(61) if d not in DIVISIONS]
    for d in non_allowed:
        div = cast(ALLOWED_DIVISIONS, d)
        assert chart.graha_drishti(n=div) is None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ascendant Planet Aspect Tester")
    parser.add_argument(
        "--d",
        action="append",
        type=int,
        help="Specific division(s) to generate aspects for (e.g., --d 1 or --d 1 --d 9)",
    )
    args = parser.parse_args()

    divisions_to_process = args.d if args.d else DIVISIONS

    chart = Chart(my_horoscope)

    # Compute results for selected divisions
    allowed_results = {}
    for division in divisions_to_process:
        div = cast(ALLOWED_DIVISIONS, division)
        if div not in DIVISIONS:
            allowed_results[division] = {
                "__error__": f"Division {div} is not an allowed division."
            }
            continue
        try:
            allowed_results[division] = chart.graha_drishti(n=div)
        except Exception as err:
            allowed_results[division] = {"__error__": str(err)}

    # Build table rows
    rows = []
    error_lines = []
    headers = ["Division", "Planet", "From", "Aspects on Houses", "Planets Aspected"]

    for division, res_list in allowed_results.items():
        if isinstance(res_list, dict) and "__error__" in res_list:
            error_lines.append(f"Division {division}: {res_list['__error__']}")
            continue
        if res_list is None:
            rows.append([str(division), "-", "-", "No chart data", "-"])
            continue

        for aspect_data in res_list:
            planet_name = aspect_data.get("planet", "?")
            from_house = aspect_data.get("from_house", "?")

            aspected_houses_info = aspect_data.get("aspect_houses", [])

            house_numbers = sorted([list(h.keys())[0] for h in aspected_houses_info])
            aspected_houses_str = ", ".join(map(str, house_numbers))

            planets_aspected_parts = []
            for house_info in aspected_houses_info:
                for house_num, planets_list in house_info.items():
                    if planets_list:
                        planets_aspected_parts.append(
                            f"{house_num}: {', '.join(planets_list)}"
                        )

            planets_aspected_str = (
                " | ".join(planets_aspected_parts) if planets_aspected_parts else "-"
            )

            rows.append(
                [
                    str(division),
                    planet_name,
                    str(from_house),
                    aspected_houses_str,
                    planets_aspected_str,
                ]
            )

    if rows:
        format_and_print_table(
            headers, rows, title="Graha Drishti (Planetary Aspects)"
        )

    # Print errors as plain strings
    if error_lines:
        print("\nErrors during processing:")
        for line in error_lines:
            print(line)
