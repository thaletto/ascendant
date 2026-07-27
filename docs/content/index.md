---
title: Getting Started
description: Install Ascendant for Python or an AI coding agent, then calculate your first chart.
---

Use Ascendant when you want to calculate Vedic astrology data locally from Python or an AI coding agent. You get structured charts, Vimshottari Dasha periods, yoga results, and Ashtakavarga scores without relying on a hosted API.

## Choose how you want to use Ascendant

### Python package

Choose the package when you want to call Ascendant directly from your application:

```bash
pip install astro-ascendant
```

### Agent skills

Choose the Skills CLI when you want your coding agent to handle saved birth records, transits, and guided reading workflows:

```bash
npx skills add thaletto/ascendant
```

The skill pack includes executable setup and transit flows plus guidance for career, finance, health, education, family, marriage, property, daily transit, and relationship compatibility.

## Calculate your first chart

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

rasi = astro.get_chart(division=1)
navamsa = astro.get_chart(division=9)
current_dasha = astro.get_current_dasha()
yogas = astro.get_yogas()
ashtakavarga = astro.get_sav()
```

Provide the complete birth details explicitly. The results are ordinary Python dictionaries and typed structures that you can inspect, validate, store, or cite in a response.

## Choose the result you need

| Method | Result |
|---|---|
| `get_chart(division)` | A twelve-house divisional chart |
| `get_dasha_timeline()` | The full Vimshottari Mahadasha and Antardasha sequence |
| `get_current_dasha(date=None)` | The Mahadasha and Antardasha active on a date |
| `get_yogas()` | Structured yoga presence, strength, type, and details |
| `get_sav()` | Bhinna, Sarva, reduced scores, and Shodhya Pinda |

## Calculation options

Your charts use `Lahiri` and `Whole Sign` by default. Override either setting
for one chart when you create the instance:

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
    ayanamsa="Krishnamurti",
    house_system="Equal",
)
```

If your application uses the same calculation settings for most charts,
configure typed defaults once:

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
    latitude=28.6139,
    longitude=77.2090,
    utc="+5:30",
)
```

Values you pass to `Ascendant` take precedence over configured defaults. Each
instance keeps the settings it had at creation time. Use `get_config()` to
inspect the current immutable defaults and `reset_config()` to restore Lahiri
and Whole Sign. Unsupported ayanamsa or house-system values raise `ValueError`.

Supported house systems are `Whole Sign`, `Placidus`, `Equal`, `Equal 2`, and
`Porphyry`. Supported ayanamsas are `Lahiri`, `Lahiri_1940`,
`Lahiri_VP285`, `Lahiri_ICRC`, `Raman`, `Krishnamurti`, and
`Krishnamurti_Senthilathiban`.

Continue with [Agent workflows](/docs/agents), or use the Python library guides for [charts](/docs/library/charts), [dashas](/docs/library/dasha), [yogas](/docs/library/yoga), and [Ashtakavarga](/docs/library/ashtakavarga).
