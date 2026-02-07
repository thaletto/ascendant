# Ascendant

Ascendant is a Python library for Vedic Astrology calculations, providing functionalities for charts, dashas, and yogas.

## Installation

```bash
pip install .
```

To install with test dependencies:

```bash
pip install ".[test]"
```

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