from ascendant.chart import Chart
from ascendant.yoga import Yoga, register_yoga
from tests.horoscope import my_horoscope


def test_chart_generation():
    """Verify chart generation for D1 (Rasi) chart"""
    chart = Chart(my_horoscope).generate_varga_chart(1)
    assert isinstance(chart, dict)
    assert len(chart) == 12
    assert all(f"house_{i}" in chart for i in range(1, 13))


def test_yoga_basic_methods():
    """Test basic Yoga methods"""
    y = Yoga(my_horoscope)

    moon_house = y.get_house_of_planet("moon")
    assert isinstance(moon_house, int)
    assert 1 <= moon_house <= 12

    rel_planets = y.planets_in_relative_house("moon", 2)
    assert isinstance(rel_planets, list)

    kendra_result = y.planet_in_kendra_from(moon_house, "jupiter")
    assert isinstance(kendra_result, bool)


def test_yoga_computation():
    """Register and compute a simple dummy yoga"""
    y = Yoga(my_horoscope)

    @register_yoga("Dummy Yoga")
    def dummy_yoga(yoga_instance: Yoga):
        moon_house = yoga_instance.get_house_of_planet("moon")
        return {
            "name": "Dummy Yoga",
            "present": moon_house is not None,
            "details": f"Moon in house {moon_house}",
        }

    results = y.compute_all()
    assert any(r["name"] == "Dummy Yoga" for r in results)

    dummy_result = next(r for r in results if r["name"] == "Dummy Yoga")
    assert dummy_result["present"] is True


def show_yogas():
    """Display all yogas for the horoscope"""
    yoga = Yoga(my_horoscope)
    results = yoga.compute_all()

    # Separate present and absent yogas
    present_yogas = [r for r in results if r.get("present", False)]
    absent_yogas = [r for r in results if not r.get("present", False)]

    print("\n" + "=" * 70)
    print("YOGA ANALYSIS FOR HOROSCOPE")
    print(f"Birth Time: {my_horoscope.day}/{my_horoscope.month}/{my_horoscope.year} {my_horoscope.hour}:{my_horoscope.minute}:{my_horoscope.second} {my_horoscope.utc}")
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
        ("Yoga Basic Methods", test_yoga_basic_methods),
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
