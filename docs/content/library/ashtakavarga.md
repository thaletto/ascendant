---
title: Ashtakavarga
description: Calculate Bhinna and Sarvashtakavarga scores, reductions, and Shodhya Pinda.
---

Use Ashtakavarga when you want to inspect Bhinna scores, the Sarvashtakavarga total for each sign, reductions, Shodhya Pinda components, and validation totals from one structured result.

## Calculate your scores

```python
result = astro.get_sav()

sarva = result["sarva"]
aries_score = sarva["Aries"]
```

## Inspect the result

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

The zeroes only show the result shape. Calculate a real result before you interpret scores; do not infer missing values from a chart image or narrative description.

## Agent use

When you use agent workflows, keep the calculated matrix with the person's chart records. Make the reading distinguish natal-chart factors from Ashtakavarga evidence, and say clearly when no matrix is available.
