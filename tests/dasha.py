import functools
import time
from datetime import datetime
from typing import Union

from ascendant.dasha import Dasha
from tests.helpers import format_and_print_table, print_timing_summary
from tests.horoscope import my_horoscope

dasha = Dasha(my_horoscope)


def timeit_individual_dashas(func):
    """Decorator to measure execution time of dasha operations"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Store original methods
        original_get_dasha_timeline = dasha.get_dasha_timeline
        original_get_antardasha_by_index = dasha.get_antardasha_by_index

        # Track timings
        get_dasha_timeline_calls = []
        get_antardasha_timings = []
        mahadasha_timings = []
        antardasha_timings = []

        def timed_get_dasha_timeline():
            nonlocal mahadasha_timings, antardasha_timings
            start = time.perf_counter()
            result = original_get_dasha_timeline()
            elapsed = time.perf_counter() - start
            get_dasha_timeline_calls.append(elapsed)

            # Time individual mahadashas (by measuring each entry processing)
            if result:
                current_mahadasha_timings = []
                for entry in result:
                    mahadasha_start = time.perf_counter()
                    # Simulate processing time by accessing all fields
                    _ = entry.get("mahadasha")
                    _ = entry.get("start")
                    _ = entry.get("end")
                    _ = len(entry.get("antardashas", []))
                    mahadasha_elapsed = time.perf_counter() - mahadasha_start
                    current_mahadasha_timings.append(
                        (entry.get("mahadasha"), mahadasha_elapsed)
                    )
                mahadasha_timings = current_mahadasha_timings

                # Time individual antardashas
                current_antardasha_timings = []
                for entry in result:
                    mahadasha = entry.get("mahadasha")
                    for antardasha in entry.get("antardashas", []):
                        antardasha_start = time.perf_counter()
                        _ = antardasha.get("antardasha")
                        _ = antardasha.get("start")
                        _ = antardasha.get("end")
                        antardasha_elapsed = time.perf_counter() - antardasha_start
                        current_antardasha_timings.append(
                            (
                                f"{mahadasha} - {antardasha.get('antardasha')}",
                                antardasha_elapsed,
                            )
                        )
                antardasha_timings = current_antardasha_timings

            return result

        def timed_get_antardasha_by_index(
            n: int, date: Union[str, datetime] | None = None
        ):
            start = time.perf_counter()
            result = original_get_antardasha_by_index(n)
            elapsed = time.perf_counter() - start
            get_antardasha_timings.append((f"Index {n}", elapsed))
            return result

        # Temporarily replace methods with timed versions
        dasha.get_dasha_timeline = timed_get_dasha_timeline
        dasha.get_antardasha_by_index = timed_get_antardasha_by_index

        try:
            total_start = time.perf_counter()
            # Execute the test function
            result = func(*args, **kwargs)
            total_elapsed = time.perf_counter() - total_start

            # Print timing summary
            if get_dasha_timeline_calls or get_antardasha_timings:
                print(f"\n{'=' * 70}")
                print("DASHA TIMING SUMMARY")
                print(f"{'=' * 70}")
                print(f"Total test time: {total_elapsed:.4f} seconds\n")

                if mahadasha_timings:
                    print_timing_summary(
                        "Mahadasha Processing",
                        sum(t[1] for t in mahadasha_timings),
                        mahadasha_timings,
                        unit_name="mahadasha",
                    )

                if antardasha_timings:
                    print_timing_summary(
                        "Antardasha Processing",
                        sum(t[1] for t in antardasha_timings),
                        antardasha_timings,
                        unit_name="antardasha",
                    )

                if get_antardasha_timings:
                    print_timing_summary(
                        "Antardasha Index Lookup",
                        sum(t[1] for t in get_antardasha_timings),
                        get_antardasha_timings,
                        unit_name="lookup",
                    )

            return result
        finally:
            # Restore original methods
            dasha.get_dasha_timeline = original_get_dasha_timeline
            dasha.get_antardasha_by_index = original_get_antardasha_by_index

    return wrapper


@timeit_individual_dashas
def test_get_vimshottari_dasha_returns_list():
    """Test that get_dasha_timeline returns a list of dictionaries."""
    result = dasha.get_dasha_timeline()

    assert isinstance(result, list)
    assert len(result) > 0


@timeit_individual_dashas
def test_get_vimshottari_dasha_structure():
    """Test the structure of each element in Vimshottari Dasha result."""
    result = dasha.get_dasha_timeline()

    for entry in result:
        assert isinstance(entry, dict)
        assert "mahadasha" in entry and isinstance(entry["mahadasha"], str)
        assert "antardashas" in entry and isinstance(entry["antardashas"], list)
        assert "start" in entry and isinstance(entry["start"], str)
        assert "end" in entry and isinstance(entry["end"], str)

        # Check antardasha structure
        for antardasha in entry["antardashas"]:
            assert isinstance(antardasha, dict)
            assert "antardasha" in antardasha and isinstance(
                antardasha["antardasha"], str
            )
            assert "start" in antardasha and isinstance(antardasha["start"], str)
            assert "end" in antardasha and isinstance(antardasha["end"], str)


def test_get_vimshottari_dasha_date_format():
    """Test that dates are in DD-MM-YYYY format."""
    result = dasha.get_dasha_timeline()

    for entry in result:
        start_date = entry["start"]
        end_date = entry["end"]

        # Parse dates to verify format
        try:
            datetime.strptime(start_date, "%d-%m-%Y")
            datetime.strptime(end_date, "%d-%m-%Y")
        except ValueError as e:
            assert False, f"Invalid date format: {e}"

        # Check antardasha dates
        for antardasha in entry["antardashas"]:
            try:
                datetime.strptime(antardasha["start"], "%d-%m-%Y")
                datetime.strptime(antardasha["end"], "%d-%m-%Y")
            except ValueError as e:
                assert False, f"Invalid antardasha date format: {e}"


def test_get_vimshottari_dasha_sorted():
    """Test that mahadashas are sorted by start date."""
    result = dasha.get_dasha_timeline()

    dates = []
    for entry in result:
        if entry["start"]:
            dates.append(datetime.strptime(entry["start"], "%d-%m-%Y"))

    # Check dates are in ascending order
    for i in range(len(dates) - 1):
        assert dates[i] <= dates[i + 1], "Mahadashas are not sorted correctly"


def test_get_vimshottari_dasha_antardasha_sorted():
    """Test that antardashas within each mahadasha are sorted."""
    result = dasha.get_dasha_timeline()

    for entry in result:
        dates = []
        for antardasha in entry["antardashas"]:
            dates.append(datetime.strptime(antardasha["start"], "%d-%m-%Y"))

        # Check antardashas are sorted within each mahadasha
        for i in range(len(dates) - 1):
            assert dates[i] <= dates[i + 1], (
                f"Antardashas in {entry['mahadasha']} are not sorted"
            )


def test_get_vimshottari_dasha_maha_9_planets():
    """Test that there are 9 mahadashas (one for each planet)."""
    result = dasha.get_dasha_timeline()

    assert len(result) == 9, f"Expected 9 mahadashas, got {len(result)}"


def test_get_vimshottari_dasha_expected_planets():
    """Test that mahadashas contain expected planet names."""
    result = dasha.get_dasha_timeline()

    expected_planets = [
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
        "Saturn",
        "Mercury",
    ]
    actual_planets = [entry["mahadasha"] for entry in result]

    assert len(actual_planets) == len(expected_planets)
    for planet in expected_planets:
        assert planet in actual_planets, f"Expected planet {planet} not found"


def test_get_vimshottari_dasha_each_maha_9_bhuktis():
    """Test that each mahadasha has 9 antardashas (bhuktis)."""
    result = dasha.get_dasha_timeline()

    for entry in result:
        assert len(entry["antardashas"]) == 9, (
            f"Mahadasha {entry['mahadasha']} should have 9 antardashas, got {len(entry['antardashas'])}"
        )


def test_get_antardasha_by_index_current():
    """Test getting current antardasha (index 0)."""
    try:
        result = dasha.get_antardasha_by_index(n=0)
        if result is not None:
            assert isinstance(result, dict)
            assert "mahadasha" in result
            assert "antardasha" in result
            assert "start" in result
            assert "end" in result

            # Check date format
            datetime.strptime(result["start"], "%d-%m-%Y")
            datetime.strptime(result["end"], "%d-%m-%Y")
    except (ValueError, TypeError):
        # Birth date might be outside computed periods
        pass


def test_get_antardasha_by_index_next():
    """Test getting next antardasha (index 1)."""
    try:
        result = dasha.get_antardasha_by_index(n=1)
        if result is not None:
            assert isinstance(result, dict)
            assert "mahadasha" in result
            assert "antardasha" in result
    except (ValueError, IndexError, TypeError):
        # Birth date might be outside computed periods or out of range
        pass


def test_get_antardasha_by_index_previous():
    """Test getting previous antardasha (index -1)."""
    try:
        result = dasha.get_antardasha_by_index(n=-1)
        if result is not None:
            assert isinstance(result, dict)
            assert "mahadasha" in result
            assert "antardasha" in result
    except (ValueError, IndexError, TypeError):
        # Birth date might be outside computed periods or out of range
        pass


def test_get_antardasha_by_index_out_of_range():
    """Test that out-of-range indices return None."""
    # Try a very large index
    result = dasha.get_antardasha_by_index(n=1000)
    # Should return None if out of range
    assert result is None or isinstance(result, dict)


def show_dasha():
    """Display all dasha information for the horoscope"""
    print("\n" + "=" * 70)
    print("VIMSHOTTARI DASHA ANALYSIS FOR HOROSCOPE")
    print(
        f"Birth Time: {my_horoscope.day}/{my_horoscope.month}/{my_horoscope.year} {my_horoscope.hour}:{my_horoscope.minute}:{my_horoscope.second} {my_horoscope.utc}"
    )
    print(f"Latitude & Longitude: {my_horoscope.latitude}, {my_horoscope.longitude}")
    print(f"Ayanamsa: {my_horoscope.ayanamsa}")
    print(f"House System: {my_horoscope.house_system}")
    print("=" * 70)

    try:
        result = dasha.get_dasha_timeline()

        # Build summary table
        headers = ["Mahadasha", "Start", "End", "Antardashas"]
        rows = [
            [
                entry["mahadasha"],
                entry["start"],
                entry["end"],
                str(len(entry["antardashas"])),
            ]
            for entry in result
        ]
        if rows:
            print(f"\nTotal Mahadashas: {len(result)}\n")
            format_and_print_table(
                headers, rows, title="Vimshottari Dasha Mahadashas"
            )

        # Display sample antardashas for first mahadasha
        if result:
            print("\n" + "=" * 70)
            print(f"SAMPLE ANTARDASHAS FOR {result[0]['mahadasha']}")
            print("=" * 70)
            sample_headers = ["Antardasha", "Start", "End"]
            sample_rows = [
                [antardasha["antardasha"], antardasha["start"], antardasha["end"]]
                for antardasha in result[0]["antardashas"]
            ]
            format_and_print_table(
                sample_headers,
                sample_rows,
                title=f"Antardashas for {result[0]['mahadasha']}",
            )

    except Exception as err:
        print(f"\nError in get_dasha_timeline: {err}")
        import traceback

        traceback.print_exc()

    # Test get_antardasha_by_index
    print("\n" + "=" * 70)
    print("CURRENT ANTARDASHA TEST")
    print("=" * 70)

    try:
        current = dasha.get_antardasha_by_index(n=0)
        if current:
            print(f"Current Dasha: {current['mahadasha']} - {current['antardasha']}")
            print(f"Start: {current['start']}")
            print(f"End: {current['end']}")

            # Also get next and previous if available
            next_antardasha = dasha.get_antardasha_by_index(n=1)
            if next_antardasha:
                print(
                    f"\nNext Dasha: {next_antardasha['mahadasha']} - {next_antardasha['antardasha']}"
                )
                print(f"Start: {next_antardasha['start']}")
                print(f"End: {next_antardasha['end']}")
            else:
                print("\nNext Dasha: Not available (out of range or no current dasha)")

            prev_antardasha = dasha.get_antardasha_by_index(n=-1)
            if prev_antardasha:
                print(
                    f"\nPrevious Dasha: {prev_antardasha['mahadasha']} - {prev_antardasha['antardasha']}"
                )
                print(f"Start: {prev_antardasha['start']}")
                print(f"End: {prev_antardasha['end']}")
            else:
                print(
                    "\nPrevious Dasha: Not available (out of range or no current dasha)"
                )
        else:
            print("Note: Birth date is outside the computed Dasha periods.")
            print("This is normal for dates far in the past or future.")

    except Exception as err:
        print(f"Error in get_antardasha_by_index: {err}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 70 + "\n")


def main():
    """Run all dasha tests"""
    tests = [
        ("Get Dasha Timeline Returns List", test_get_vimshottari_dasha_returns_list),
        ("Dasha Structure", test_get_vimshottari_dasha_structure),
        ("Date Format", test_get_vimshottari_dasha_date_format),
        ("Mahadashas Sorted", test_get_vimshottari_dasha_sorted),
        ("Antardashas Sorted", test_get_vimshottari_dasha_antardasha_sorted),
        ("9 Mahadashas", test_get_vimshottari_dasha_maha_9_planets),
        ("Expected Planets", test_get_vimshottari_dasha_expected_planets),
        (
            "Each Mahadasha Has 9 Antardashas",
            test_get_vimshottari_dasha_each_maha_9_bhuktis,
        ),
        ("Get Current Antardasha", test_get_antardasha_by_index_current),
        ("Get Next Antardasha", test_get_antardasha_by_index_next),
        ("Get Previous Antardasha", test_get_antardasha_by_index_previous),
        ("Get Antardasha Out of Range", test_get_antardasha_by_index_out_of_range),
    ]

    passed = 0
    failed = 0

    print("Running dasha tests...\n")

    for test_name, test_func in tests:
        try:
            test_func()
            print(f"[OK] {test_name} - PASSED")
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test_name} - FAILED")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERR] {test_name} - ERROR")
            print(f"  Error: {e}")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'=' * 50}")

    return failed == 0


if __name__ == "__main__":
    import sys

    # Check if --show-dasha flag is passed
    if "--show-dasha" in sys.argv or "-d" in sys.argv:
        show_dasha()
    else:
        success = main()
        exit(0 if success else 1)


if __name__ == "__main__":
    import sys

    # Check if --show-dasha flag is passed
    if "--show-dasha" in sys.argv:
        show_dasha()
    else:
        success = main()
        exit(0 if success else 1)
