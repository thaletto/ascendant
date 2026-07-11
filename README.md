# Ascendant

Ascendant is a Python library for Vedic Astrology calculations, providing functionalities for charts, dashas, and yogas.

## Installation

Install via pip:

```bash
pip install astro-ascendant
```

> `PyPI` no longer supports specifying external packages (eg:git repo URLs) in `dependencies` in the `pyproject.toml` file. To install the required package `flatlib` from the sidereal branch, run the following command, after completion of above `pip install astro-ascendant` command:

```bash
pip install git+https://github.com/thaletto/flatlib.git@sidereal#egg=flatlib
```

## Documentation

The documentation is a Fumadocs app backed by the Markdown files in the [docs](docs/index.md) folder.

```bash
bun install
bun run dev
```

Open [http://localhost:3000/docs](http://localhost:3000/docs), or browse the source pages directly:

- [Divisional Charts (Vargas)](docs/charts.md)
- [Dasha Systems](docs/dasha.md)
- [Yoga Combinations](docs/yoga.md)

## Core Functionalities:

- **Chart Calculations**: Compute and analyze divisional astrological charts (Varga chakras).
- **Dasha System**: Implementation of the Vimshottari Dasha system for planetary periods.
- **Yoga Combinations**: Identification and interpretation of various Yoga (planetary combinations).

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
```

# Advanced Usage
```
astro = Ascendant(
    ...
    ayanamsa = "krishnamurti"
    house_system = "equal"
)
```

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
