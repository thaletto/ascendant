import functools
import time
from typing import Dict
from ascendant.chart import Chart, SELECTED_PLANETS
from ascendant.yoga import Yoga, YOGA_REGISTRY
from tests.helpers import print_timing_summary
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


def timeit_individual_yogas(func):
    """Decorator to measure execution time of individual yoga computations"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Store original compute_all method
        original_compute_all = yoga.compute_all

        # Create a timed version of compute_all
        def timed_compute_all():
            total_start = time.perf_counter()

            # Time individual yoga computations
            yoga_timings = []
            results = []

            for name, func in YOGA_REGISTRY.items():
                start = time.perf_counter()
                result = func(yoga)
                elapsed = time.perf_counter() - start
                yoga_timings.append((name, elapsed))
                results.append(result)

            total_elapsed = time.perf_counter() - total_start

            print_timing_summary("YOGA", total_elapsed, yoga_timings, unit_name="yoga")

            return results

        # Temporarily replace compute_all with timed version
        yoga.compute_all = timed_compute_all

        try:
            # Execute the test function
            result = func(*args, **kwargs)
            return result
        finally:
            # Restore original compute_all method
            yoga.compute_all = original_compute_all

    return wrapper


@timeit_individual_yogas
def test_yoga_computation():
    """Compute all registered yogas and ensure they are present"""
    yoga.compute_all()


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
        print(f"[+] PRESENT YOGAS ({len(present_yogas)}):")
        print("-" * 70)
        for yoga_result in present_yogas:
            print(f"  * {yoga_result['name']}")
            print(f"    {yoga_result.get('details', 'No details available')}")
            print()
    else:
        print("[+] PRESENT YOGAS: None\n")

    if absent_yogas:
        print(f"[-] ABSENT YOGAS ({len(absent_yogas)}):")
        print("-" * 70)
        for yoga_result in absent_yogas:
            print(f"  * {yoga_result['name']}")
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
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Test yogas.")
    parser.add_argument("--yoga", type=str, help="Test a single yoga by name.")
    parser.add_argument(
        "--show-yoga", "-y", action="store_true", help="Show all yogas for the horoscope."
    )

    args = parser.parse_args()

    if args.yoga:
        yoga_name = args.yoga
        if yoga_name in YOGA_REGISTRY:
            print(f"Testing yoga: {yoga_name}")
            start_time = time.perf_counter()
            result = YOGA_REGISTRY[yoga_name](yoga)
            end_time = time.perf_counter()
            print(json.dumps(result, indent=2))
            print(f"\nExecution time: {end_time - start_time:.6f} seconds")
        else:
            print("Available yogas:")
            for y_name in sorted(YOGA_REGISTRY.keys()):
                print(f"  - {y_name}")
            exit(1)
    elif args.show_yoga:
        show_yogas()
    else:
        success = main()
        exit(0 if success else 1)
