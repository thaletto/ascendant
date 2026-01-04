import functools
import time
from typing import cast

from ascendant.chart import Chart
from ascendant.const import ALLOWED_DIVISIONS
from ascendant.types import ALLOWED_DIVISIONS as ALLOWED_DIVISIONS_LITERAL
from tests.helpers import format_and_print_table, print_timing_summary
from tests.horoscope import my_horoscope

chart = Chart(my_horoscope)


def timeit_individual_divisions(func):
    """Decorator to measure execution time of individual division chart generations"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Store original get_varga_chakra_chart method
        original_get_varga_chakra_chart = chart.get_varga_chakra_chart

        # Create a timed version that tracks division timings
        division_timings = []
        original_results = {}

        def timed_get_varga_chakra_chart(n):
            start = time.perf_counter()
            result = original_get_varga_chakra_chart(n)
            elapsed = time.perf_counter() - start
            division_timings.append((n, elapsed))
            original_results[n] = result
            return result

        # Temporarily replace get_varga_chakra_chart with timed version
        chart.get_varga_chakra_chart = timed_get_varga_chakra_chart

        try:
            total_start = time.perf_counter()
            # Execute the test function
            result = func(*args, **kwargs)
            total_elapsed = time.perf_counter() - total_start

            # Print timing summary
            if division_timings:
                print_timing_summary(
                    "CHART DIVISION",
                    total_elapsed,
                    division_timings,
                    unit_name="division",
                )

            return result
        finally:
            # Restore original get_varga_chakra_chart method
            chart.get_varga_chakra_chart = original_get_varga_chakra_chart

    return wrapper


@timeit_individual_divisions
def test_generate_varga_chart_runs_for_allowed_divisions():
    """Test that varga charts can be generated for all allowed divisions"""
    for division in ALLOWED_DIVISIONS:
        div = cast(ALLOWED_DIVISIONS_LITERAL, division)
        result = chart.get_varga_chakra_chart(n=div)

        # Result should be a dictionary (ChartType)
        assert isinstance(result, dict)
        # Should have 12 houses
        assert len(result) == 12

        # Check structure of each house
        for house_num, house_data in result.items():
            # House key should be integer 1-12
            assert isinstance(house_num, int)
            assert 1 <= house_num <= 12
            assert isinstance(house_data, dict)
            assert "sign" in house_data and isinstance(house_data["sign"], str)
            assert "planets" in house_data and isinstance(house_data["planets"], list)
            assert "lagna" in house_data

            # Check each planet in the house
            for planet_data in house_data["planets"]:
                assert isinstance(planet_data, dict)
                assert "name" in planet_data and isinstance(planet_data["name"], str)
                assert "longitude" in planet_data and isinstance(
                    planet_data["longitude"], (int, float)
                )
                assert "is_retrograde" in planet_data and isinstance(
                    planet_data["is_retrograde"], bool
                )
                assert "sign" in planet_data and isinstance(planet_data["sign"], dict)

                # Check sign structure
                sign_data = planet_data["sign"]
                assert "name" in sign_data and isinstance(sign_data["name"], str)
                assert "lord" in sign_data and isinstance(sign_data["lord"], str)
                assert "nakshatra" in sign_data and isinstance(
                    sign_data["nakshatra"], dict
                )

                # Check nakshatra structure
                nakshatra_data = sign_data["nakshatra"]
                assert "name" in nakshatra_data and isinstance(
                    nakshatra_data["name"], str
                )
                assert "lord" in nakshatra_data and isinstance(
                    nakshatra_data["lord"], str
                )
                assert "pada" in nakshatra_data and isinstance(
                    nakshatra_data["pada"], int
                )

        # House 1 should always have lagna
        assert 1 in result
        assert result[1]["lagna"] is not None
        assert isinstance(result[1]["lagna"], dict)
        assert result[1]["lagna"]["name"] == "Lagna"


def test_generate_varga_chart_longitude_ranges():
    """Test that longitudes are within valid ranges"""
    for division in ALLOWED_DIVISIONS:
        div = cast(ALLOWED_DIVISIONS_LITERAL, division)
        if (result := chart.get_varga_chakra_chart(n=div)) is None:
            raise ValueError(f"Division {division} should return None")

        for house_num, house_data in result.items():
            for planet_data in house_data["planets"]:
                planet_name = planet_data["name"]
                longitude = planet_data["longitude"]
                assert 0 <= longitude < 360, (
                    f"Longitude {longitude} out of range for {planet_name} in house {house_num}"
                )


def test_generate_varga_chart_returns_consistent_structure():
    """Test that varga charts return consistent structure"""
    # Test a few divisions to ensure consistent structure
    test_divisions = [1, 9, 10]
    for division in test_divisions:
        div = cast(ALLOWED_DIVISIONS_LITERAL, division)
        result = chart.get_varga_chakra_chart(n=div)
        assert isinstance(result, dict)
        assert len(result) == 12
        assert 1 in result
        assert result[1]["lagna"] is not None


def test_non_allowed_divisions():
    """Test that non-allowed divisions return None"""
    non_allowed = [d for d in range(61) if d not in ALLOWED_DIVISIONS]

    for division in non_allowed:
        div = cast(ALLOWED_DIVISIONS_LITERAL, division)
        result = chart.get_varga_chakra_chart(n=div)
        assert result is None, (
            f"Division {division} should return None, got {type(result)}"
        )


def format_chart_markdown(division, chart_data):
    """Format a single chart's data into a Markdown table string."""
    if not chart_data:
        return f"# Division {division}\n\nNo data available or error occurred.\n"

    lines = []
    lines.append(f"# Division {division} Chart Analysis")
    lines.append(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Basic Info Table
    lines.append("## Chart Details")
    lines.append("| House | Sign | Lord | Planets |")
    lines.append("|-------|------|------|---------|")

    for house_num in range(1, 13):
        house = chart_data.get(house_num, {})
        sign_data = house.get("sign", "N/A")

        # Handle sign data which might be a string or dict
        if isinstance(sign_data, dict):
            sign_name = sign_data.get("name", "Unknown")
            sign_lord = sign_data.get("lord", "Unknown")
        else:
            sign_name = str(sign_data)
            sign_lord = "-"  # Can't get lord easily if just string

        planets = house.get("planets", [])
        planet_strs = []
        for p in planets:
            p_name = p.get("name", "?")
            p_long = p.get("longitude", 0)
            p_retro = "(R)" if p.get("is_retrograde") else ""
            planet_strs.append(f"{p_name}{p_retro} ({p_long:.2f}°)")

        planets_display = ", ".join(planet_strs) if planet_strs else "-"

        lines.append(f"| {house_num} | {sign_name} | {sign_lord} | {planets_display} |")

    lines.append("\n")
    return "\n".join(lines)


def save_chart(division, content):
    """Save chart content to sample/chart/ directory."""
    from pathlib import Path

    output_dir = Path("sample/chart")
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = output_dir / f"chart_D{division}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved Division {division} chart to: {filename}")


def print_chart_table(division, chart_data):
    """Format and print a single chart's data into a table."""
    if not chart_data:
        print(f"Division {division}: No data available.")
        return

    headers = ["House", "Sign", "Lord", "Planets"]
    rows = []
    for house_num in range(1, 13):
        house = chart_data.get(house_num, {})
        sign_data = house.get("sign", "N/A")

        if isinstance(sign_data, dict):
            sign_name = sign_data.get("name", "?")
            sign_lord = sign_data.get("lord", "?")
        else:
            sign_name = str(sign_data)
            sign_lord = "-"

        planets = house.get("planets", [])
        planet_strs = []
        for p in planets:
            p_name = p.get("name", "?")
            p_long = p.get("longitude", 0)
            p_retro = "(R)" if p.get("is_retrograde") else ""
            planet_strs.append(f"{p_name}{p_retro} ({p_long:.2f}°)")

        planets_display = ", ".join(planet_strs) if planet_strs else "-"

        rows.append([str(house_num), sign_name, sign_lord, planets_display])

    format_and_print_table(headers, rows, title=f"DIVISION {division} CHART")


def process_charts(divisions_to_process, save_mode=False):
    """Process specific divisions: display and optionally save."""

    print(f"\nProcessing Divisions: {divisions_to_process}\n")

    for div in divisions_to_process:
        try:
            div = cast(ALLOWED_DIVISIONS_LITERAL, div)
            result = chart.get_varga_chakra_chart(n=div)

            # console output (table)
            print_chart_table(div, result)

            # file output (Markdown)
            if save_mode:
                markdown_output = format_chart_markdown(div, result)
                save_chart(div, markdown_output)

        except Exception as e:
            print(f"Error processing Division {div}: {e}")


def show_chart():
    """Display all allowed division charts"""
    process_charts(ALLOWED_DIVISIONS, save_mode=False)


def handle_cli():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Ascendant Chart Generator & Tester")
    parser.add_argument(
        "--d",
        action="append",
        type=int,
        help="Specific division(s) to generate (e.g., --d 1 or --d 1 --d 9)",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the generated charts to sample/chart/ folder",
    )
    parser.add_argument(
        "--show-chart",
        "-c",
        action="store_true",
        help="Show summary table of all charts (legacy mode)",
    )

    args, _ = parser.parse_known_args()

    if args.d or args.save:
        divisions = args.d or ALLOWED_DIVISIONS
        process_charts(divisions, save_mode=args.save)
        return

    if args.show_chart:
        show_chart()
        return

    success = main()
    sys.exit(0 if success else 1)


def main():
    """Run all chart tests"""
    tests = [
        (
            "Generate varga chart for allowed divisions",
            test_generate_varga_chart_runs_for_allowed_divisions,
        ),
        ("Longitude ranges", test_generate_varga_chart_longitude_ranges),
        (
            "Consistent structure",
            test_generate_varga_chart_returns_consistent_structure,
        ),
        ("Non-allowed divisions", test_non_allowed_divisions),
    ]

    passed = 0
    failed = 0

    print("Running chart tests...\n")

    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✓ {test_name} - PASSED")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_name} - FAILED")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_name} - ERROR")
            print(f"  Error: {e}")
            failed += 1

    print(f"\n{'=' * 70}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'=' * 70}")

    return failed == 0


if __name__ == "__main__":
    handle_cli()
