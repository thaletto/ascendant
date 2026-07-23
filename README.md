# Ascendant

Ascendant is a Python library for Vedic Astrology calculations, providing functionalities for charts, dashas, and yogas.

## Installation

Install via pip:

```bash
pip install astro-ascendant
```

Ascendant calculates sidereal positions directly with the bundled
`pyswisseph` dependency; no `flatlib` installation is required.

## Documentation

The documentation is a separate Fumadocs app in [`docs/`](docs), backed by Markdown files in [`docs/content/`](docs/content/index.md).

```bash
cd docs
bun install
bun run dev
```

Open [http://localhost:3000/docs](http://localhost:3000/docs), or browse the source pages directly:

- [Divisional Charts (Vargas)](docs/content/charts.md)
- [Dasha Systems](docs/content/dasha.md)
- [Yoga Combinations](docs/content/yoga.md)

The docs app is independent: create or configure its Vercel project with `docs/` as the project root.

## Codex and Agent Skills

This repository is also the canonical source for the Ascendant agent skills. The plugin bundle lives
under [`plugins/agent/`](plugins/agent/), and the same `plugins/{scope}/skills` layout is discoverable
by the `skills` CLI.

Install the skills with:

```bash
npx skills add thaletto/ascendant
```

Add the Codex marketplace from Git and install the plugin with:

```bash
codex plugin marketplace add https://github.com/thaletto/ascendant.git --ref main
codex plugin add agent@ascendant
```

## Core Functionalities:

- **Chart Calculations**: Compute and analyze divisional astrological charts (Varga chakras).
- **Dasha System**: Implementation of the Vimshottari Dasha system for planetary periods.
- **Yoga Combinations**: Identification and interpretation of various Yoga (planetary combinations).
- **Ashtakavarga**: Classical Bhinnashtakavarga, Sarvashtakavarga, Shodhana, and Shodhya Pinda calculations.

## Usage

```python
from ascendant import Ascendant

# Initialize with birth details
astro = Ascendant(
    year=1990, month=1, day=1,
    hour=12, minute=0, second=0,
    latitude=28.6139, longitude=77.2090,
    utc="+5:30"
)

# Get Rasi Chart (D1)
chart = astro.get_chart(division=1)

# Get Yogas
yogas = astro.get_yogas()

# Get Dasha Timeline
dasha = astro.get_dasha_timeline()

# Get Ashtakavarga / Sarvashtakavarga
ashtakavarga = astro.get_sav()
sarva = ashtakavarga["sarva"]
```

# Advanced Usage

Override the built-in Lahiri and Whole Sign defaults for one chart:

```python
astro = Ascendant(
    ...,
    ayanamsa="Krishnamurti",
    house_system="Equal",
)
```

Configure typed application-wide defaults once when most charts use the same
calculation settings:

```python
from ascendant import (
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

astro = Ascendant(...)  # Uses Lahiri and Porphyry.
```

Explicit `Ascendant` arguments take precedence over the configured defaults.
Configuration is immutable and is captured when each instance is created.
Use `get_config()` to inspect the current defaults and `reset_config()` to
restore Lahiri and Whole Sign. Unsupported constructor values raise
`ValueError`.

## Available Ayanamsa

- Lahiri (default)
- Lahiri_1940
- Lahiri_VP285
- Lahiri_ICRC
- Raman
- Krishnamurti
- Krishnamurti_Senthilathiban

## Available House System

- Whole Sign (default)
- Placidus
- Equal
- Equal 2
- Porphyry

## Accuracy Verification

Run the Swiss Ephemeris reference cases independently:

```bash
.venv/bin/python -m pytest tests/test_swiss_ephemeris_accuracy.py -vv
```

The cases compare sidereal Sun, Moon, ascendant, and house cusp positions
against fixed reference values with a maximum angular error of `0.1°`. They
cover Whole Sign, Placidus, Equal, and Porphyry house systems across multiple
ayanamsas and dates. The Porphyry case also checks House 2 so the test
distinguishes its cusps from systems that share the same ascendant and first
house cusp.
