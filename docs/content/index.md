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

## What system the Ascendant skills use

Ascendant's interpretation skills use a versioned **Parashari–Jaimini** workflow
named `parashari_raman_jaimini_v3`. The calculator uses the **sidereal zodiac**, with
**Lahiri ayanamsa** and **Whole Sign houses** as its defaults. A reading begins
with separate Parashari and named seven-karaka Jaimini natal judgments. The two
are compared as co-primary evidence before the relevant divisional chart,
Vimshottari periods, dated transits, and Sarvashtakavarga are considered.

The workflow is deliberately narrower than either complete tradition. It uses
the declared `jaimini_srao_7_core_v1` method and does not silently switch
variants or add Chara Dasha or KP rules. The agent reads saved
artifacts directly, applies developer-owned evidence and factor hierarchies,
and cites each material conclusion with its artifact pointer and governing
source or Ascendant methodology rule. Choosing a Krishnamurti ayanamsa in the
Python configuration changes the sidereal reference point; it does not turn
the skills into a KP astrology engine.

Learn how these traditions differ in [Learn astrology](/docs/astrology), or
read the exact [agent workflow](/docs/agents).

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
jaimini = astro.get_jaimini()
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
| `get_jaimini()` | Seven Chara Karakas, Rashi Drishti, Karakamsha, Arudha Padas, Upapada, and raw Argala |

## Configure the calculation model

Charts use Lahiri ayanamsa and Whole Sign houses by default. You can override
either value for one instance or set immutable application defaults for future
instances. See [Configuration](/docs/configuration) for precedence, supported
values, validation, and reproducible examples.

Continue with [Agent workflows](/docs/agents), [Learn astrology](/docs/astrology),
or the Python library guides for [charts](/docs/library/charts),
[dashas](/docs/library/dasha), [yogas](/docs/library/yoga), and
[Ashtakavarga](/docs/library/ashtakavarga), or
[Jaimini core](/docs/library/jaimini).
