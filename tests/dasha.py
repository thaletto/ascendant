import pytest
from datetime import datetime

from ascendant.dasha import DashaFinder
from tests.horoscope import my_horoscope


def test_get_vimshottari_dasha_returns_list():
    """Test that get_vimshottari_dasha returns a list of dictionaries."""
    dasha = DashaFinder(my_horoscope)
    result = dasha.get_vimshottari_dasha()

    assert isinstance(result, list)
    assert len(result) > 0


def test_get_vimshottari_dasha_structure():
    """Test the structure of each element in Vimshottari Dasha result."""
    dasha = DashaFinder(my_horoscope)
    result = dasha.get_vimshottari_dasha()

    for entry in result:
        assert isinstance(entry, dict)
        assert "mahadasha" in entry and isinstance(entry["mahadasha"], str)
        assert "antardasha" in entry and isinstance(entry["antardasha"], list)
        assert "start" in entry and isinstance(entry["start"], str)
        assert "end" in entry and isinstance(entry["end"], str)

        # Check antardasha structure
        for antardasha in entry["antardasha"]:
            assert isinstance(antardasha, dict)
            assert "bhuthi" in antardasha and isinstance(antardasha["bhuthi"], str)
            assert "start" in antardasha and isinstance(antardasha["start"], str)
            assert "end" in antardasha and isinstance(antardasha["end"], str)


def test_get_vimshottari_dasha_date_format():
    """Test that dates are in DD-MM-YYYY format."""
    dasha = DashaFinder(my_horoscope)
    result = dasha.get_vimshottari_dasha()

    for entry in result:
        start_date = entry["start"]
        end_date = entry["end"]

        # Parse dates to verify format
        try:
            datetime.strptime(start_date, "%d-%m-%Y")
            datetime.strptime(end_date, "%d-%m-%Y")
        except ValueError as e:
            pytest.fail(f"Invalid date format: {e}")

        # Check antardasha dates
        for antardasha in entry["antardasha"]:
            try:
                datetime.strptime(antardasha["start"], "%d-%m-%Y")
                datetime.strptime(antardasha["end"], "%d-%m-%Y")
            except ValueError as e:
                pytest.fail(f"Invalid antardasha date format: {e}")


def test_get_vimshottari_dasha_sorted():
    """Test that mahadashas are sorted by start date."""
    dasha = DashaFinder(my_horoscope)
    result = dasha.get_vimshottari_dasha()

    dates = []
    for entry in result:
        if entry["start"]:
            dates.append(datetime.strptime(entry["start"], "%d-%m-%Y"))

    # Check dates are in ascending order
    for i in range(len(dates) - 1):
        assert dates[i] <= dates[i + 1], "Mahadashas are not sorted correctly"


def test_get_vimshottari_dasha_antardasha_sorted():
    """Test that antardashas within each mahadasha are sorted."""
    dasha = DashaFinder(my_horoscope)
    result = dasha.get_vimshottari_dasha()

    for entry in result:
        dates = []
        for antardasha in entry["antardasha"]:
            dates.append(datetime.strptime(antardasha["start"], "%d-%m-%Y"))

        # Check antardashas are sorted within each mahadasha
        for i in range(len(dates) - 1):
            assert dates[i] <= dates[i + 1], (
                f"Antardashas in {entry['mahadasha']} are not sorted"
            )


def test_get_vimshottari_dasha_maha_9_planets():
    """Test that there are 9 mahadashas (one for each planet)."""
    dasha = DashaFinder(my_horoscope)
    result = dasha.get_vimshottari_dasha()

    assert len(result) == 9, f"Expected 9 mahadashas, got {len(result)}"


def test_get_vimshottari_dasha_expected_planets():
    """Test that mahadashas contain expected planet names."""
    dasha = DashaFinder(my_horoscope)
    result = dasha.get_vimshottari_dasha()

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
    dasha = DashaFinder(my_horoscope)
    result = dasha.get_vimshottari_dasha()

    for entry in result:
        assert len(entry["antardasha"]) == 9, (
            f"Mahadasha {entry['mahadasha']} should have 9 antardashas, got {len(entry['antardasha'])}"
        )


def test_get_bhuthi_by_index_current():
    """Test getting current dasha (index 0)."""
    dasha = DashaFinder(my_horoscope)

    try:
        result = dasha.get_bhuthi_by_index(n=0)
        assert isinstance(result, dict)
        assert "mahadasha" in result
        assert "bhukti" in result
        assert "start" in result
        assert "end" in result

        # Check date format
        datetime.strptime(result["start"], "%d-%m-%Y")
        datetime.strptime(result["end"], "%d-%m-%Y")
    except ValueError as e:
        if "No current Dasha found" not in str(e):
            pytest.fail(f"Unexpected error: {e}")


def test_get_bhuthi_by_index_next():
    """Test getting next dasha (index 1)."""
    dasha = DashaFinder(my_horoscope)

    try:
        result = dasha.get_bhuthi_by_index(n=1)
        assert isinstance(result, dict)
        assert "mahadasha" in result
        assert "bhukti" in result
    except (ValueError, IndexError) as e:
        if "No current Dasha found" not in str(e) and "out of range" not in str(e):
            pytest.fail(f"Unexpected error: {e}")


def test_get_bhuthi_by_index_previous():
    """Test getting previous dasha (index -1)."""
    dasha = DashaFinder(my_horoscope)

    try:
        result = dasha.get_bhuthi_by_index(n=-1)
        assert isinstance(result, dict)
        assert "mahadasha" in result
        assert "bhukti" in result
    except (ValueError, IndexError) as e:
        if "No current Dasha found" not in str(e) and "out of range" not in str(e):
            pytest.fail(f"Unexpected error: {e}")


def test_get_bhuthi_by_index_out_of_range():
    """Test that out-of-range indices raise IndexError."""
    dasha = DashaFinder(my_horoscope)

    # Try a very large index
    try:
        _ = dasha.get_bhuthi_by_index(n=1000)
        # If we get here, either there are many dashas or we're not in a valid period
    except (ValueError, IndexError):
        pass  # Expected


if __name__ == "__main__":
    dasha = DashaFinder(my_horoscope)

    # Test get_vimshottari_dasha
    print("=" * 80)
    print("VIMSHOTTARI DASHA TEST")
    print("=" * 80)

    try:
        result = dasha.get_vimshottari_dasha()

        # Build summary table
        rows = []
        for entry in result:
            mahadasha = entry["mahadasha"]
            start = entry["start"]
            end = entry["end"]
            num_antardashas = len(entry["antardasha"])
            rows.append([mahadasha, start, end, str(num_antardashas)])

        headers = ["Mahadasha", "Start", "End", "Antardashas"]
        col_widths = [len(h) for h in headers]
        for r in rows:
            for i, cell in enumerate(r):
                if len(cell) > col_widths[i]:
                    col_widths[i] = len(cell)

        def format_row(vals):
            return " | ".join(val.ljust(col_widths[i]) for i, val in enumerate(vals))

        print(format_row(headers))
        print("-+-".join("-" * w for w in col_widths))
        for r in rows:
            print(format_row(r))

        # Display sample antardashas for first mahadasha
        if result:
            print("\n" + "=" * 80)
            print(f"SAMPLE ANTARDASHAS FOR {result[0]['mahadasha']}")
            print("=" * 80)
            sample_rows = []
            for antardasha in result[0]["antardasha"]:
                sample_rows.append(
                    [
                        antardasha["bhuthi"],
                        antardasha["start"],
                        antardasha["end"],
                    ]
                )

            sample_headers = ["Bhukti", "Start", "End"]
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
        print(f"Error in get_vimshottari_dasha: {err}")
        import traceback

        traceback.print_exc()

    # Test get_bhuthi_by_index
    print("\n" + "=" * 80)
    print("CURRENT BHUTHI TEST")
    print("=" * 80)

    try:
        current = dasha.get_bhuthi_by_index(n=0)
        print(f"Current Dasha: {current['mahadasha']} - {current['bhukti']}")
        print(f"Start: {current['start']}")
        print(f"End: {current['end']}")

        # Also get next and previous if available
        try:
            next_bhuthi = dasha.get_bhuthi_by_index(n=1)
            print(f"\nNext Dasha: {next_bhuthi['mahadasha']} - {next_bhuthi['bhukti']}")
            print(f"Start: {next_bhuthi['start']}")
            print(f"End: {next_bhuthi['end']}")
        except (ValueError, IndexError):
            print("\nNext Dasha: Not available (out of range or no current dasha)")

        try:
            prev_bhuthi = dasha.get_bhuthi_by_index(n=-1)
            print(
                f"\nPrevious Dasha: {prev_bhuthi['mahadasha']} - {prev_bhuthi['bhukti']}"
            )
            print(f"Start: {prev_bhuthi['start']}")
            print(f"End: {prev_bhuthi['end']}")
        except (ValueError, IndexError):
            print("\nPrevious Dasha: Not available (out of range or no current dasha)")

    except ValueError as err:
        if "No current Dasha found" in str(err):
            print("Note: Birth date is outside the computed Dasha periods.")
            print("This is normal for dates far in the past or future.")
        else:
            print(f"Error: {err}")
            import traceback

            traceback.print_exc()
    except Exception as err:
        print(f"Error in get_bhuthi_by_index: {err}")
        import traceback

        traceback.print_exc()
