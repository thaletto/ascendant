# Remove the VedicAstro Dependency

## Summary

Replace the small portion of VedicAstro used by Ascendant with an internal typed horoscope layer while retaining the sidereal flatlib fork. Preserve current public outputs and calculation behavior.

## Implementation Changes

- Add `HoroscopeData` for birth inputs, sidereal flatlib chart construction, and longitude metadata.
- Move Vimshottari calculation into Ascendant's dasha module while preserving the existing periods and `DD-MM-YYYY` output.
- Keep the `Ascendant` API and return schemas unchanged; export `HoroscopeData` for advanced callers.
- Remove VedicAstro from package and test imports; explicitly depend on `pyswisseph` and `python-dateutil`.
- Pin the documented sidereal flatlib revision and align release CI to Python 3.11+.

## Test Plan

- Capture VedicAstro 0.2.1 baseline output and compare D1, D9, D10, and complete dasha results via deterministic regression digests.
- Run all chart, planet, dasha, and yoga checks, then build and install the wheel in a fresh environment without VedicAstro.

## Assumptions

- Current numerical and period-boundary behavior takes priority over correcting existing approximation quirks.
- Direct Swiss Ephemeris integration and a VedicAstro compatibility alias are out of scope.
