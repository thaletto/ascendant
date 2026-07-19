---
title: Ashtakavarga
description: Calculate Bhinna and Sarvashtakavarga scores, reductions, and Shodhya Pinda.
---

Ascendant implements typed Parashari Ashtakavarga calculations. The public result contains raw Bhinna scores, the Sarvashtakavarga total by sign, reduced scores, Shodhya Pinda components, and validation totals.

## Calculate scores

```python
result = astro.get_sav()

sarva = result["sarva"]
aries_score = sarva["Aries"]
```

## Result shape

```python
{
    "bhinna": {
        "Sun": {"Aries": 0, "Taurus": 0, ...},
        "Moon": {"Aries": 0, "Taurus": 0, ...},
        # Mars, Mercury, Jupiter, Venus, Saturn, and Lagna
    },
    "sarva": {"Aries": 0, "Taurus": 0, ...},
    "reduced": {
        "Sun": {"Aries": 0, "Taurus": 0, ...},
        # Moon through Saturn
    },
    "shodhya_pinda": {
        "Sun": {
            "rashi_pinda": 0,
            "graha_pinda": 0,
            "shodhya_pinda": 0,
        },
        # Moon through Saturn
    },
    "totals": {...},
}
```

The example uses zeroes only to illustrate the shape. Always calculate a real result before interpreting scores; do not infer missing values from a chart image or narrative description.

## Agent use

For agent workflows, preserve the calculated matrix with the person's chart records. A reading should distinguish the natal chart factors from Ashtakavarga evidence and should explicitly say when no matrix is available.
