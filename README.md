# Ascendant

Ascendant is a Python package for calculating Vedic astrology charts,
Vimshottari Dashas, Yoga combinations, Ashtakavarga values, and a named
seven-karaka Jaimini core.

It uses Swiss Ephemeris through `pyswisseph` and supports typed configuration
for ayanamsa and house-system defaults.

## Installation

Ascendant requires Python 3.11 or later.

```bash
python -m pip install astro-ascendant
```

`pyswisseph` is installed as a package dependency. No separate `flatlib`
installation is required.

## Quick start

Create an `Ascendant` instance with the local birth time, UTC offset, and
geographic coordinates:

```python
from ascendant import Ascendant

astro = Ascendant(
    year=1990,
    month=1,
    day=1,
    hour=12,
    minute=0,
    second=0,
    utc="+5:30",
    latitude=28.6139,
    longitude=77.2090,
)

# Rasi chart (D1)
chart = astro.get_chart(division=1)

# Detected Yoga combinations
present_yogas = [
    yoga for yoga in astro.get_yogas() if yoga["present"]
]

# Vimshottari Dasha
dasha_timeline = astro.get_dasha_timeline()
current_dasha = astro.get_current_dasha()

# Ashtakavarga and Sarvashtakavarga
ashtakavarga = astro.get_sav()
sarvashtakavarga = ashtakavarga["sarva"]

# Seven Chara Karakas, Rashi Drishti, Karakamsha, Arudhas, and Argala
jaimini = astro.get_jaimini()
```

By default, Ascendant uses the Lahiri ayanamsa and Whole Sign houses.

## Features

- Sidereal planetary and house calculations using Swiss Ephemeris
- Divisional charts, including D1, D9, D10, and other supported Vargas
- Vimshottari Mahadasha and Antardasha timelines
- Current Dasha lookup for a supplied date
- Registered Vedic Yoga evaluation with structured results
- Bhinnashtakavarga, Sarvashtakavarga, Shodhana, and Shodhya Pinda
- Named seven-karaka Jaimini core derived from D1 and D9
- Typed, immutable calculation configuration

## Configuration

Override the defaults for an individual chart:

```python
astro = Ascendant(
    year=1990,
    month=1,
    day=1,
    hour=12,
    minute=0,
    second=0,
    utc="+5:30",
    latitude=28.6139,
    longitude=77.2090,
    ayanamsa="Krishnamurti",
    house_system="Porphyry",
)
```

Or configure application-wide defaults:

```python
from ascendant import (
    Ascendant,
    AscendantConfig,
    Ayanamsa,
    HouseSystem,
    configure,
)

configure(
    AscendantConfig(
        ayanamsa=Ayanamsa.LAHIRI,
        house_system=HouseSystem.PORPHYRY,
    )
)

astro = Ascendant(
    year=1990,
    month=1,
    day=1,
    hour=12,
    minute=0,
    second=0,
    utc="+5:30",
    latitude=28.6139,
    longitude=77.2090,
)
```

Explicit `Ascendant` arguments take precedence over configured defaults, which
take precedence over the package defaults. Each instance captures an immutable
configuration snapshot when it is created.

Use `get_config()` to inspect the configured defaults and `reset_config()` to
restore Lahiri and Whole Sign. Unsupported constructor values raise
`ValueError`.

### Supported ayanamsas

- `Lahiri`
- `Lahiri_1940`
- `Lahiri_VP285`
- `Lahiri_ICRC`
- `Raman`
- `Krishnamurti`
- `Krishnamurti_Senthilathiban`

### Supported house systems

- `Whole Sign`
- `Placidus`
- `Equal`
- `Equal 2`
- `Porphyry`

## Result shape

Ascendant returns regular Python dictionaries and lists. For example, every
Yoga result contains:

```python
{
    "id": "gajakesari",
    "name": "GajaKesari",
    "present": True,
    "strength": 0.9,
    "details": "Jupiter in house 4 and Moon is in 1",
    "type": "Positive",
}
```

Use `present` to select detected combinations and retain `details` when
presenting or interpreting a result.

## Documentation

The repository includes guides for:

- [Divisional charts](https://github.com/thaletto/ascendant/blob/main/docs/content/library/charts.md)
- [Dasha systems](https://github.com/thaletto/ascendant/blob/main/docs/content/library/dasha.md)
- [Jaimini core](https://github.com/thaletto/ascendant/blob/main/docs/content/library/jaimini.md)
- [Yoga combinations](https://github.com/thaletto/ascendant/blob/main/docs/content/library/yoga.md)
- [Configuration](https://github.com/thaletto/ascendant/blob/main/docs/content/configuration.md)

## Development

Clone the repository, create the local environment, and use the documented
Make targets:

```bash
make help
make test
make typecheck
make lint
```

Swiss Ephemeris accuracy cases live in
[`tests/test_swiss_ephemeris_accuracy.py`](https://github.com/thaletto/ascendant/blob/main/tests/test_swiss_ephemeris_accuracy.py).

## Agent skills

The repository also contains an optional Ascendant agent plugin. It is not
required to use the Python package.

```bash
npx skills add thaletto/ascendant
```

Codex users can install the bundled plugin from the repository marketplace:

```bash
codex plugin marketplace add https://github.com/thaletto/ascendant.git --ref main
codex plugin add agent@ascendant
```
