---
title: Yoga Combinations
description: Identify and inspect classical planetary combinations in a chart.
---

Use Yogas when you want to evaluate named planetary combinations in a calculated chart. Ascendant returns a structured record for every registered yoga, so you can distinguish a detected combination from one that is absent.

## Understand yoga types

Your result categorizes yogas as:
- **Positive**: Beneficial combinations (e.g., Dhana Yogas, Raja Yogas)
- **Negative**: Challenging combinations (e.g., Aristha Yogas)
- **Neutral**: Combinations that have mixed or specific structural effects

## Explore supported yogas

For example, you can inspect:

| Yoga | Description |
|---|---|
| **GajaKesari** | Jupiter in a Kendra from the Moon. Brings fame and intelligence. |
| **Pancha Mahapurusha** | Five great person yogas (Hamsa, Malavya, Bhadra, Ruchaka, Sasa). |
| **Buddha Aditya** | Conjunction of Sun and Mercury. |
| **Chandra Mangala** | Conjunction of Moon and Mars. |
| **Adhi Yoga** | Benefics in 6th, 7th, and 8th from Moon or Lagna. |
| **Malika Yogas** | Continuous occupation of houses by planets. |

## Calculate yogas

Calculate all yogas, then keep only the ones present in your chart:

```python
yogas = astro.get_yogas()

# Filter for present yogas
present_yogas = [y for y in yogas if y['present']]

for yoga in present_yogas:
    print(f"Yoga: {yoga['name']} (Strength: {yoga['strength']:.2f})")
    print(f"Type: {yoga['type']}")
    print(f"Details: {yoga['details']}")
    print("-" * 20)
```

## Inspect a yoga result

Each yoga result is a dictionary:

```python
{
    "id": "gajakesari",
    "name": "GajaKesari",
    "present": True,
    "strength": 0.9,
    "details": "Jupiter in house 4 and Moon is in 1",
    "type": "Positive"
}
```

When you discuss a detected yoga, cite `details` and the relevant chart placements. Treat `strength` as calculation output, not as a standalone prediction or certainty.
