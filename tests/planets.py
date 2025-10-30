from ascendant import ALLOWED_DIVISIONS
import pytest

from ascendant.planets import Planets
from tests.horoscope import my_horoscope


@pytest.mark.parametrize("division", ALLOWED_DIVISIONS)
def test_graha_drishthi_runs_for_allowed_divisions(division: int):
    planets = Planets(my_horoscope)
    result = planets.graha_drishthi(division=division)

    # Result should be a mapping of planet name -> detail dict
    assert isinstance(result, dict)
    # If there are no planets (unlikely), it's still valid to be empty
    for name, data in result.items():
        assert isinstance(name, str) and name
        assert isinstance(data, dict)
        assert "from_house" in data and isinstance(data["from_house"], int)
        assert 1 <= data["from_house"] <= 12
        assert "aspects" in data and isinstance(data["aspects"], list)
        assert all(isinstance(h, int) and 1 <= h <= 12 for h in data["aspects"])
        assert "aspect_planets" in data and isinstance(data["aspect_planets"], dict)
        for h, plist in data["aspect_planets"].items():
            assert isinstance(h, int) and 1 <= h <= 12
            assert isinstance(plist, list)


def test_graha_drishthi_default_is_d1():
    planets = Planets(my_horoscope)
    d1 = planets.graha_drishthi()
    d1_explicit = planets.graha_drishthi(division=1)
    assert isinstance(d1, dict) and isinstance(d1_explicit, dict)
    # Keys should match for implicit vs explicit D1
    assert set(d1.keys()) == set(d1_explicit.keys())


def test_aspects_for_alias_matches_graha_drishthi():
    planets = Planets(my_horoscope)
    for division in ALLOWED_DIVISIONS:
        a = planets.aspects_for(division=division)
        b = planets.graha_drishthi(division=division)
        assert set(a.keys()) == set(b.keys())


if __name__ == "__main__":
    planets = Planets(my_horoscope)

    # Compute results for allowed divisions
    allowed_results = {}
    for division in ALLOWED_DIVISIONS:
        try:
            allowed_results[division] = planets.graha_drishthi(division=division)
        except Exception as err:
            allowed_results[division] = {"__error__": str(err)}

    # Build table rows (skip divisions that errored; those are printed as strings)
    rows = []
    error_lines = []
    for division, res in allowed_results.items():
        if isinstance(res, dict) and "__error__" in res:
            error_lines.append(f"Division {division}: {res['__error__']}")
            continue
        for planet_name, data in res.items():
            from_house = data.get("from_house", "")
            aspects = data.get("aspects", [])
            aspects_str = ",".join(str(h) for h in aspects)
            aspect_planets = data.get("aspect_planets", {})
            ap_str_parts = []
            for h, plist in aspect_planets.items():
                ap_str_parts.append(f"{h}:{','.join(plist)}")
            ap_str = " | ".join(ap_str_parts)
            rows.append(
                [str(division), planet_name, str(from_house), aspects_str, ap_str]
            )

    # Determine column widths
    headers = ["Division", "Planet", "From", "Aspects", "AspectPlanets"]
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
        for line in error_lines:
            print(line)

    # Also test and print for non-allowed divisions (expect errors)
    non_allowed = [d for d in range(61) if d not in ALLOWED_DIVISIONS]
    non_allowed_errors = []
    for division in non_allowed:
        try:
            _ = planets.graha_drishthi(division=division)
            non_allowed_errors.append(f"Division {division}: unexpectedly succeeded")
        except Exception:
            pass
    
    print('\nNon allowed divisions unexpectedly succeeded: ', len(non_allowed_errors))
    for line in non_allowed_errors:
        print(line)
