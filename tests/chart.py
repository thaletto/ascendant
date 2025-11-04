from ascendant import ALLOWED_DIVISIONS
import pytest
from ascendant.chart import Chart
from tests.horoscope import my_horoscope


@pytest.mark.parametrize("division", ALLOWED_DIVISIONS)
def test_generate_varga_chart_runs_for_allowed_divisions(division: int):
    chart = Chart(my_horoscope)
    result = chart.generate_varga_chart(division=division)

    # Result should be a dictionary with house keys
    assert isinstance(result, dict)
    # Should have at least one house
    assert len(result) > 0

    # Check structure of each house
    for house_key, house_data in result.items():
        # House key should be house_1, house_2, etc.
        assert house_key.startswith("house_")
        assert isinstance(house_data, dict)
        assert "sign" in house_data and isinstance(house_data["sign"], str)
        assert "planets" in house_data and isinstance(house_data["planets"], dict)

        # Check each planet in the house
        for planet_name, planet_data in house_data["planets"].items():
            assert isinstance(planet_name, str) and planet_name
            assert isinstance(planet_data, dict)
            assert "longitude" in planet_data and isinstance(
                planet_data["longitude"], (int, float)
            )
            assert "retrograde" in planet_data and isinstance(
                planet_data["retrograde"], bool
            )

            # Check nakshatra-related fields
            assert "rashi_lord" in planet_data
            assert "nakshatra" in planet_data
            assert "nakshatra_lord" in planet_data
            assert "pada" in planet_data and isinstance(planet_data["pada"], int)

    # House 1 should always have lagna
    assert "house_1" in result
    assert "lagna" in result["house_1"]["planets"]


@pytest.mark.parametrize("division", ALLOWED_DIVISIONS)
def test_generate_varga_chart_longitude_ranges(division: int):
    chart = Chart(my_horoscope)
    result = chart.generate_varga_chart(division=division)

    for house_key, house_data in result.items():
        for planet_name, planet_data in house_data["planets"].items():
            longitude = planet_data["longitude"]
            assert 0 <= longitude < 360, (
                f"Longitude {longitude} out of range for {planet_name} in {house_key}"
            )

            if "degree" in planet_data:
                degree = planet_data["degree"]
                assert 0 <= degree < 30, (
                    f"Degree {degree} out of range for {planet_name} in {house_key}"
                )


def test_generate_varga_chart_returns_consistent_structure():
    chart = Chart(my_horoscope)
    # Test a few divisions to ensure consistent structure
    test_divisions = [1, 9, 10]
    for division in test_divisions:
        result = chart.generate_varga_chart(division=division)
        assert isinstance(result, dict)
        assert "house_1" in result


@pytest.mark.parametrize("division", ALLOWED_DIVISIONS)
def test_non_allowed_divisions_raise_error(division: int):
    # This will be empty when run for allowed divisions
    # The actual test for non-allowed is below
    pass


def test_non_allowed_divisions():
    chart = Chart(my_horoscope)
    non_allowed = [d for d in range(61) if d not in ALLOWED_DIVISIONS]

    for division in non_allowed:
        with pytest.raises(ValueError, match="Unsupported division"):
            chart.generate_varga_chart(division=division)


if __name__ == "__main__":
    chart = Chart(my_horoscope)

    # Compute results for allowed divisions
    allowed_results = {}
    for division in ALLOWED_DIVISIONS:
        try:
            allowed_results[division] = chart.generate_varga_chart(division=division)
        except Exception as err:
            allowed_results[division] = {"__error__": str(err)}

    # Build table rows (skip divisions that errored; those are printed as strings)
    rows = []
    error_lines = []
    for division, res in allowed_results.items():
        if isinstance(res, dict) and "__error__" in res:
            error_lines.append(f"Division {division}: {res['__error__']}")
            continue

        # Count houses and planets for this division
        num_houses = len(res)
        total_planets = sum(len(h.get("planets", {})) for h in res.values())

        # Get house 1 sign
        house_1_sign = res.get("house_1", {}).get("sign", "N/A")

        # Count planets in each house
        planet_distribution = {}
        for house_key, house_data in res.items():
            num_in_house = len(house_data.get("planets", {}))
            if num_in_house > 0:
                house_num = house_key.replace("house_", "")
                planet_distribution[house_num] = num_in_house

        dist_str = ", ".join(
            [f"{h}:{n}" for h, n in sorted(planet_distribution.items())]
        )

        rows.append(
            [str(division), str(num_houses), house_1_sign, str(total_planets), dist_str]
        )

    # Determine column widths
    headers = [
        "Division",
        "Houses",
        "Lagna Sign",
        "Total Planets",
        "Distribution (H:N)",
    ]
    col_widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            if len(cell) > col_widths[i]:
                col_widths[i] = len(cell)

    # Print table
    def format_row(vals):
        return " | ".join(val.ljust(col_widths[i]) for i, val in enumerate(vals))

    if rows:
        print(format_row(headers))
        print("-+-".join("-" * w for w in col_widths))
        for r in rows:
            print(format_row(r))

    # Print errors as plain strings
    if error_lines:
        print()
        print("Errors:")
        for line in error_lines:
            print(line)

    # Also test and print for non-allowed divisions (expect errors)
    non_allowed = [d for d in range(61) if d not in ALLOWED_DIVISIONS]
    non_allowed_errors = []
    for division in non_allowed:
        try:
            _ = chart.generate_varga_chart(division=division)
            non_allowed_errors.append(f"Division {division}: unexpectedly succeeded")
        except Exception:
            pass

    print("\nNon allowed divisions unexpectedly succeeded: ", len(non_allowed_errors))
    for line in non_allowed_errors:
        print(line)
