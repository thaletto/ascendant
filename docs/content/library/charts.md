---
title: Divisional Charts (Vargas)
description: Calculate and inspect Ascendant's supported Vedic divisional charts.
---

Use a divisional chart when you need a specific Varga view of a birth chart. Ascendant supports sixteen divisions, and each call gives you a twelve-house dictionary with sign, planet, and Lagna data.

## Choose a division

Choose from these supported divisions:

| Division | Name | Description |
|---|---|---|
| 1 | Rasi | Basic natal chart |
| 2 | Hora | Wealth and prosperity |
| 3 | Drekkana | Siblings and initiatives |
| 4 | Chaturthamsa | Fixed assets and happiness |
| 7 | Saptamsa | Children and grandchildren |
| 9 | Navamsa | Spouse, strength, and fruits of life |
| 10 | Dasamsa | Career and profession |
| 12 | Dwadasamsa | Parents and ancestry |
| 16 | Shodasamsa | Vehicles and comforts |
| 20 | Vimsamsa | Spiritual progress |
| 24 | Chaturvimsamsa | Knowledge and education |
| 27 | Saptavimsamsa | Strengths and weaknesses |
| 30 | Trimsamsa | Evils and misfortunes |
| 40 | Khavedamsa | General auspiciousness |
| 45 | Akshavedamsa | Character and conduct |
| 60 | Shastyamsa | All aspects of life (very important) |

## Calculate a chart

For example, calculate the Navamsa (D9) chart:

```python
from ascendant import Ascendant

# Create `astro` as shown in Getting Started.
# Calculate the Navamsa (D9) chart.
d9_chart = astro.get_chart(division=9)

# Inspect the house numbers (1-12), signs, and planet data.
for house, data in d9_chart.items():
    print(f"House {house}: Sign {data['sign']}")
    for planet in data['planets']:
        print(f"  - {planet['name']} at {planet['longitude']:.2f}°")
```

Each planet includes its longitude, retrograde status, sign relationship, sign lord, Nakshatra, Nakshatra lord, and Pada. Use these values to ground an interpretation in the calculated placement rather than a rendered chart alone.

Passing a division outside the supported list raises `ValueError`.
