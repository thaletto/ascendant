from typing import Dict
from ascendant.chart import Chart, SELECTED_PLANETS
from ascendant.yoga import Yoga, YOGA_REGISTRY
from tests.horoscope import my_horoscope

chart = Chart(my_horoscope).get_rasi_chart()
yoga = Yoga(my_horoscope)


def test_chart_generation():
    assert isinstance(chart, Dict)
    assert len(chart) == 12
    assert all(i in chart for i in range(1, 13))


def test_get_house_of_planet():
    for planet in SELECTED_PLANETS:
        house = yoga.get_house_of_planet("Sun")
        assert house is not None, f"{planet} not found in chart"
        assert isinstance(house, int)
    lagna_house = yoga.get_house_of_planet("Lagna")
    assert lagna_house is not None, "Lagna not found in chart"


def test_planets_in_relative_house():
    rel_planets = yoga.planets_in_relative_house("Ketu", 2)
    assert isinstance(rel_planets, list)


def test_planet_in_kendra_from():
    kendra_result = yoga.planet_in_kendra_from(1, "Lagna")
    assert isinstance(kendra_result, bool)


def test_get_house_of_rashi():
    aries_house = yoga.get_house_of_rashi("Aries")
    assert aries_house is not None, "Aries not found in chart"
    assert isinstance(aries_house, int)


def test_get_lord_of_house():
    lord = yoga.get_lord_of_house(1)
    assert lord is not None, "Lord of house 1 not found"
    assert isinstance(lord, str)


def test_relative_house():
    relative_pos = yoga.relative_house("Moon", "Lagna")
    assert relative_pos is not None, (
        "Could not determine relative house of Moon and Lagna"
    )
    assert isinstance(relative_pos, int)


def test_yoga_computation():
    """Compute all registered yogas and ensure they are present"""
    results = yoga.compute_all()

    # Get names of all registered yogas
    registered_yoga_names = set(YOGA_REGISTRY.keys())

    # Get names of computed yogas
    computed_yoga_names = {r["name"] for r in results}

    # Assert that all registered yogas were computed
    assert registered_yoga_names.issubset(computed_yoga_names)

    # Optionally, check if any yoga is present
    assert any(r["present"] for r in results)


def show_yogas():
    """Display all yogas for the horoscope"""
    results = yoga.compute_all()

    # Separate present and absent yogas
    present_yogas = [r for r in results if r.get("present", False)]
    absent_yogas = [r for r in results if not r.get("present", False)]

    print("\n" + "=" * 70)
    print("YOGA ANALYSIS FOR HOROSCOPE")
    print(
        f"Birth Time: {my_horoscope.day}/{my_horoscope.month}/{my_horoscope.year} {my_horoscope.hour}:{my_horoscope.minute}:{my_horoscope.second} {my_horoscope.utc}"
    )
    print(f"Latitude & Longitude: {my_horoscope.latitude}, {my_horoscope.longitude}")
    print(f"Ayanamsa: {my_horoscope.ayanamsa}")
    print(f"House System: {my_horoscope.house_system}")
    print("=" * 70)
    print(f"Total Yogas Analyzed: {len(results)}\n")

    if present_yogas:
        print(f"✓ PRESENT YOGAS ({len(present_yogas)}):")
        print("-" * 70)
        for yoga_result in present_yogas:
            print(f"  • {yoga_result['name']}")
            print(f"    {yoga_result.get('details', 'No details available')}")
            print()
    else:
        print("✓ PRESENT YOGAS: None\n")

    if absent_yogas:
        print(f"✗ ABSENT YOGAS ({len(absent_yogas)}):")
        print("-" * 70)
        for yoga_result in absent_yogas:
            print(f"  • {yoga_result['name']}")
            print(f"    {yoga_result.get('details', 'No details available')}")
            print()

    print("=" * 70 + "\n")


def main():
    """Run all yoga tests"""
    tests = [
        ("Chart Generation", test_chart_generation),
        ("Get House of Planet", test_get_house_of_planet),
        ("Planets in relative house", test_planets_in_relative_house),
        ("Planet in Kendra from house", test_planet_in_kendra_from),
        ("Get House of Rashi", test_get_house_of_rashi),
        ("Get Lord of House", test_get_lord_of_house),
        ("Relative House", test_relative_house),
        ("Yoga Computation", test_yoga_computation),
    ]

    passed = 0
    failed = 0

    print("Running yoga tests...\n")

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

    # Check if --show-yogas flag is passed
    if "--show-yoga" in sys.argv or "-y" in sys.argv:
        show_yogas()
    else:
        success = main()
        exit(0 if success else 1)
