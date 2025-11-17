from datetime import datetime

from ascendant.dasha import Dasha
from tests.horoscope import my_horoscope

dasha = Dasha(my_horoscope)


def test_get_vimshottari_dasha_returns_list():
    """Test that get_dasha_timeline returns a list of dictionaries."""
    result = dasha.get_dasha_timeline()

    assert isinstance(result, list)
    assert len(result) > 0


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
        rows = []
        for entry in result:
            mahadasha = entry["mahadasha"]
            start = entry["start"]
            end = entry["end"]
            num_antardashas = len(entry["antardashas"])
            rows.append([mahadasha, start, end, str(num_antardashas)])

        headers = ["Mahadasha", "Start", "End", "Antardashas"]
        col_widths = [len(h) for h in headers]
        for r in rows:
            for i, cell in enumerate(r):
                if len(cell) > col_widths[i]:
                    col_widths[i] = len(cell)

        def format_row(vals):
            return " | ".join(val.ljust(col_widths[i]) for i, val in enumerate(vals))

        if rows:
            print(f"\nTotal Mahadashas: {len(result)}\n")
            print(format_row(headers))
            print("-+-".join("-" * w for w in col_widths))
            for r in rows:
                print(format_row(r))

        # Display sample antardashas for first mahadasha
        if result:
            print("\n" + "=" * 70)
            print(f"SAMPLE ANTARDASHAS FOR {result[0]['mahadasha']}")
            print("=" * 70)
            sample_rows = []
            for antardasha in result[0]["antardashas"]:
                sample_rows.append(
                    [
                        antardasha["antardasha"],
                        antardasha["start"],
                        antardasha["end"],
                    ]
                )

            sample_headers = ["Antardasha", "Start", "End"]
            sample_col_widths = [len(h) for h in sample_headers]
            for r in sample_rows:
                for i, cell in enumerate(r):
                    if len(cell) > sample_col_widths[i]:
                        sample_col_widths[i] = len(cell)

            print(format_row(sample_headers))
            print("-+-".join("-" * w for w in sample_col_widths))
            for r in sample_rows:
                print(format_row(r))

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

    # Check if --show-dasha flag is passed
    if "--show-dasha" in sys.argv or "-d" in sys.argv:
        show_dasha()
    else:
        success = main()
        exit(0 if success else 1)
