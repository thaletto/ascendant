# Remove the VedicAstro Dependency

## Summary

Replace the small portion of VedicAstro and flatlib used by Ascendant with an internal typed horoscope layer backed directly by `pyswisseph`. Preserve public chart, yoga, and dasha schemas while keeping longitudes, angles, and house cusps within 0.1° of the previous sidereal flatlib baseline.

## Implementation Changes

- Add `HoroscopeData` for birth inputs, direct sidereal Swiss Ephemeris chart construction, and longitude metadata.
- Move Vimshottari calculation into Ascendant's dasha module while preserving the existing periods and `DD-MM-YYYY` output.
- Keep the `Ascendant` API and return schemas unchanged; export `HoroscopeData` for advanced callers.
- Remove VedicAstro from package and test imports; explicitly depend on `pyswisseph` and `python-dateutil`.
- Remove flatlib imports, installation documentation, and CI setup; use local Swiss Ephemeris type stubs and align release CI to Python 3.11+.

## Test Plan

- Capture sidereal flatlib reference positions for all supported ayanamsas and house systems from 1900–2100, enforcing a 0.1° maximum circular error.
- Run all chart, planet, dasha, and yoga checks, then build and install the wheel in a fresh environment without VedicAstro or flatlib.

## Assumptions

- The direct adapter is the source of runtime chart positions; the reference fixtures define the numerical compatibility contract.
- A VedicAstro compatibility alias remains out of scope.
