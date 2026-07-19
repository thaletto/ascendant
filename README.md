# Ascendant

Ascendant is a Python library for Vedic Astrology calculations, providing functionalities for charts, dashas, and yogas.

## Installation

Install via pip:

```bash
pip install astro-ascendant
```

> `flatlib`'s sidereal support is provided by a Git dependency, which PyPI cannot declare in package metadata. Install the tested revision after installing Ascendant:

```bash
pip install "flatlib @ git+https://github.com/thaletto/flatlib.git@2618c348ce1ab2588548f935ff65f031630b4872"
```

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
    ayanamsa = "Krishnamurti"
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
