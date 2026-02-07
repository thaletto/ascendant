# Ascendant Documentation

Welcome to the Ascendant documentation. Ascendant is a comprehensive Python library for Vedic Astrology (Jyotish) calculations.

## Contents

- [Getting Started](index.md)
- [Divisional Charts (Vargas)](charts.md)
- [Dasha Systems](dasha.md)
- [Yoga Combinations](yoga.md)

## Installation

```bash
pip install astro-ascendant
```

## Basic Usage

```python
from ascendant import Ascendant

# Initialize the main class
astro = Ascendant(
    year=1990, month=1, day=1,
    hour=12, minute=0, second=0,
    latitude=28.6139, longitude=77.2090,
    utc="+5:30"
)
```
