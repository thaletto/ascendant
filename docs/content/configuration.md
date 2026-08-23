---
title: Configuration
description: Choose Ascendant's ayanamsa and house system with explicit, typed, reproducible defaults.
---

`AscendantConfig` groups the calculation settings used by one `Ascendant`
instance. Configuration is explicit and immutable, so independent callers in
the same process can calculate with different settings without changing shared
module state.

## Configure an instance

```python
from ascendant import (
    AscendantConfig,
    Ayanamsa,
    HouseSystem,
    Ascendant,
)

astro = Ascendant(
    year=1990,
    month=1,
    day=1,
    hour=12,
    minute=0,
    second=0,
    latitude=28.6139,
    longitude=77.2090,
    utc="+5:30",
    config=AscendantConfig(
        ayanamsa=Ayanamsa.RAMAN,
        house_system=HouseSystem.PORPHYRY,
    ),
)
```

`AscendantConfig` is frozen and slotted. Its fields accept enum members, not
arbitrary strings. Passing a dictionary or another object as `config` raises
`TypeError`; passing strings into `AscendantConfig` also raises `TypeError`.

The built-in value is equivalent to:

```python
AscendantConfig(
    ayanamsa=Ayanamsa.LAHIRI,
    house_system=HouseSystem.WHOLE_SIGN,
)
```

## Built-in defaults and compatibility functions

```python
from ascendant import get_config, reset_config

current = get_config()
print(current.ayanamsa)
print(current.house_system)

reset_config()
```

`get_config()` always returns the immutable built-in defaults. `reset_config()`
remains as a compatibility no-op. The former process-wide `configure()` entry
point now raises an actionable `RuntimeError`; migrate callers by passing its
`AscendantConfig` value to `Ascendant(config=...)`.

## How an instance resolves its settings

When you construct a chart without explicit calculation settings, it uses the
immutable built-in configuration:

```python
from ascendant import Ascendant

astro = Ascendant(
    year=1990,
    month=1,
    day=1,
    hour=12,
    minute=0,
    second=0,
    latitude=28.6139,
    longitude=77.2090,
    utc="+5:30",
)
```

The effective precedence is:

1. Explicit `Ascendant(...)` arguments
2. The instance's explicit `config`
3. `AscendantConfig()` defaults

Each instance keeps the resolved values stored in its `horoscope_data`.

## Override one instance

The `Ascendant` constructor accepts enum members:

```python
from ascendant import Ascendant, Ayanamsa, HouseSystem

astro = Ascendant(
    year=1990,
    month=1,
    day=1,
    hour=12,
    minute=0,
    second=0,
    latitude=28.6139,
    longitude=77.2090,
    utc="+5:30",
    ayanamsa=Ayanamsa.KRISHNAMURTI,
    house_system=HouseSystem.PLACIDUS,
)
```

It also accepts supported strings at this constructor boundary:

```python
astro = Ascendant(
    year=1990,
    month=1,
    day=1,
    hour=12,
    minute=0,
    second=0,
    latitude=28.6139,
    longitude=77.2090,
    utc="+5:30",
    ayanamsa="raman",
    house_system="equal_2",
)
```

Ayanamsa strings are matched case-insensitively against their exact values.
House-system strings are stripped, underscores become spaces, and comparison
is case-insensitive. For example, `"equal_2"` resolves to
`HouseSystem.EQUAL_2`. Unsupported strings raise `ValueError` while the
instance is being constructed.

## `Ayanamsa`

| Member | Value |
| --- | --- |
| `Ayanamsa.LAHIRI` | `Lahiri` |
| `Ayanamsa.LAHIRI_1940` | `Lahiri_1940` |
| `Ayanamsa.LAHIRI_VP285` | `Lahiri_VP285` |
| `Ayanamsa.LAHIRI_ICRC` | `Lahiri_ICRC` |
| `Ayanamsa.RAMAN` | `Raman` |
| `Ayanamsa.KRISHNAMURTI` | `Krishnamurti` |
| `Ayanamsa.KRISHNAMURTI_SENTHILATHIBAN` | `Krishnamurti_Senthilathiban` |

## `HouseSystem`

| Member | Value | Swiss Ephemeris code |
| --- | --- | --- |
| `HouseSystem.WHOLE_SIGN` | `Whole Sign` | `W` |
| `HouseSystem.PLACIDUS` | `Placidus` | `P` |
| `HouseSystem.EQUAL` | `Equal` | `A` |
| `HouseSystem.EQUAL_2` | `Equal 2` | `E` |
| `HouseSystem.PORPHYRY` | `Porphyry` | `O` |

Ascendant maps these enums to Swiss Ephemeris in `horoscope.py`. Swiss
Ephemeris documents its
[sidereal modes](https://www.astro.com/swisseph-download/doc/swephprg.2.10.htm#_Toc112949044)
and [house methods](https://www.astro.com/swisseph-download/doc/swephprg.2.10.htm#_Toc112949056).

### Current chart-output boundary

The selected house-system code is used when Swiss Ephemeris calculates cusps
and angles. The current public `get_chart()` result still places one complete
sign in each numbered house from the rising sign and does not expose cusp
longitudes. In this release, a non-Whole-Sign setting changes the underlying
cusp calculation but not public `get_chart()` planet-to-house membership.

## Reproducibility

Store the resolved enum values with the birth timezone, coordinates, and
software version. When comparing two results, confirm those values before
investigating a difference in the calculated chart.
