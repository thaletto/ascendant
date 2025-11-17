import functools
import time
from ascendant.const import ALLOWED_DIVISIONS
from ascendant.chart import Chart
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
                print(f"\n{'=' * 70}")
                print("CHART DIVISION TIMING SUMMARY")
                print(f"{'=' * 70}")
                print(f"Total time: {total_elapsed:.4f} seconds")
                print(f"Number of divisions: {len(division_timings)}\n")

                # Sort by time (slowest first)
                division_timings.sort(key=lambda x: x[1], reverse=True)
                print("Top 10 slowest divisions:")
                print("-" * 70)
                for division, elapsed in division_timings[:10]:
                    percentage = (elapsed / total_elapsed) * 100
                    print(
                        f"  Division {division:2d}: {elapsed:8.6f} seconds ({percentage:5.2f}%)"
                    )

                if len(division_timings) > 10:
                    print(f"\n... and {len(division_timings) - 10} more divisions\n")
                else:
                    print()

                # Print statistics
                times = [t[1] for t in division_timings]
                avg_time = sum(times) / len(times) if times else 0
                min_time = min(times) if times else 0
                max_time = max(times) if times else 0

                print("Statistics:")
                print(f"\nAverage time per division: {avg_time:.6f} seconds")
                print(f"\nFastest division: {min_time:.6f} seconds")
                print(f"\nSlowest division: {max_time:.6f} seconds")
                print(f"{'=' * 70}\n")

            return result
        finally:
            # Restore original get_varga_chakra_chart method
            chart.get_varga_chakra_chart = original_get_varga_chakra_chart

    return wrapper


@timeit_individual_divisions
def test_generate_varga_chart_runs_for_allowed_divisions():
    """Test that varga charts can be generated for all allowed divisions"""
    for division in ALLOWED_DIVISIONS:
        result = chart.get_varga_chakra_chart(n=division)

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
        result = chart.get_varga_chakra_chart(n=division)

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
        result = chart.get_varga_chakra_chart(n=division)
        assert isinstance(result, dict)
        assert len(result) == 12
        assert 1 in result
        assert result[1]["lagna"] is not None


def test_non_allowed_divisions():
    """Test that non-allowed divisions return None"""
    non_allowed = [d for d in range(61) if d not in ALLOWED_DIVISIONS]

    for division in non_allowed:
        result = chart.get_varga_chakra_chart(n=division)
        assert result is None, (
            f"Division {division} should return None, got {type(result)}"
        )


def show_chart():
    """Display all varga charts for the horoscope"""
    print("\n" + "=" * 70)
    print("VARGA CHART ANALYSIS FOR HOROSCOPE")
    print(
        f"Birth Time: {my_horoscope.day}/{my_horoscope.month}/{my_horoscope.year} {my_horoscope.hour}:{my_horoscope.minute}:{my_horoscope.second} {my_horoscope.utc}"
    )
    print(f"Latitude & Longitude: {my_horoscope.latitude}, {my_horoscope.longitude}")
    print(f"Ayanamsa: {my_horoscope.ayanamsa}")
    print(f"House System: {my_horoscope.house_system}")
    print("=" * 70)

    # Compute results for allowed divisions
    allowed_results = {}
    for division in ALLOWED_DIVISIONS:
        try:
            allowed_results[division] = chart.get_varga_chakra_chart(n=division)
        except Exception as err:
            allowed_results[division] = {"__error__": str(err)}

    # Build table rows (skip divisions that errored; those are printed as strings)
    rows = []
    error_lines = []
    for division, res in allowed_results.items():
        if isinstance(res, dict) and "__error__" in res:
            error_lines.append(f"Division {division}: {res['__error__']}")
            continue

        if res is None:
            error_lines.append(f"Division {division}: returned None")
            continue

        # Count houses and planets for this division
        num_houses = len(res)
        total_planets = sum(len(h.get("planets", [])) for h in res.values())

        # Get house 1 sign
        house_1_sign = res.get(1, {}).get("sign", "N/A")

        # Count planets in each house
        planet_distribution = {}
        for house_num, house_data in res.items():
            num_in_house = len(house_data.get("planets", []))
            if num_in_house > 0:
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
        print(f"\nTotal Divisions Analyzed: {len(ALLOWED_DIVISIONS)}\n")
        print(format_row(headers))
        print("-+-".join("-" * w for w in col_widths))
        for r in rows:
            print(format_row(r))

    # Print errors as plain strings
    if error_lines:
        print("\nErrors:")
        print("-" * 70)
        for line in error_lines:
            print(f"  • {line}")

    # Also test and print for non-allowed divisions (expect None)
    non_allowed = [d for d in range(61) if d not in ALLOWED_DIVISIONS]
    non_allowed_errors = []
    for division in non_allowed:
        result = chart.get_varga_chakra_chart(n=division)
        if result is not None:
            non_allowed_errors.append(
                f"Division {division}: unexpectedly returned {type(result)} instead of None"
            )

    if non_allowed_errors:
        print(
            f"\nNon-allowed divisions unexpectedly returned values: {len(non_allowed_errors)}"
        )
        print("-" * 70)
        for line in non_allowed_errors:
            print(f"  • {line}")

    print("\n" + "=" * 70 + "\n")


def main():
    """Run all chart tests"""
    tests = [
        (
            "Generate Varga Chart for Allowed Divisions",
            test_generate_varga_chart_runs_for_allowed_divisions,
        ),
        ("Longitude Ranges", test_generate_varga_chart_longitude_ranges),
        (
            "Consistent Structure",
            test_generate_varga_chart_returns_consistent_structure,
        ),
        ("Non-Allowed Divisions", test_non_allowed_divisions),
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

    print(f"\n{'=' * 50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'=' * 50}")

    return failed == 0


if __name__ == "__main__":
    import sys

    # Check if --show-chart flag is passed
    if "--show-chart" in sys.argv or "-c" in sys.argv:
        show_chart()
    else:
        success = main()
        exit(0 if success else 1)
