---
title: Getting Started
description: Install Ascendant for Python or an AI coding agent, then calculate your first chart.
---

Ascendant is a local Vedic astrology calculation engine for Python and AI agents. It returns structured charts, Vimshottari Dasha periods, yoga results, and Ashtakavarga scores without requiring a hosted API.

## Choose an installation

### Python package

Use the package when you want to call Ascendant directly from application code:

```bash
pip install astro-ascendant
```

### Agent skills

Use the Skills CLI when you want a coding agent to handle saved birth records, transits, and guided reading workflows:

```bash
npx skills add thaletto/ascendant
```

The skill pack includes executable setup and transit flows plus guidance for career, finance, health, education, family, marriage, property, daily transit, and relationship compatibility.

## Calculate a chart

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

All inputs remain explicit. Results are ordinary Python dictionaries and typed structures that an application or agent can inspect, validate, store, and cite in a response.

## Public methods

| Method | Result |
|---|---|
| `get_chart(division)` | A twelve-house divisional chart |
| `get_dasha_timeline()` | The full Vimshottari Mahadasha and Antardasha sequence |
| `get_current_dasha(date=None)` | The Mahadasha and Antardasha active on a date |
| `get_yogas()` | Structured yoga presence, strength, type, and details |
| `get_sav()` | Bhinna, Sarva, reduced scores, and Shodhya Pinda |

## Calculation options

`Lahiri` and `Whole Sign` are the defaults. You can select another supported ayanamsa or house system when creating the instance:

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

Continue with [Agent workflows](/docs/agents) or inspect the calculation APIs for [charts](/docs/charts), [dashas](/docs/dasha), [yogas](/docs/yoga), and [Ashtakavarga](/docs/ashtakavarga).
