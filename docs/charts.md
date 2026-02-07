# Divisional Charts (Vargas)

Ascendant supports various divisional charts (Varga chakras) used in Vedic Astrology.

## Supported Divisions

The following divisions are supported:

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

## Usage

To get a specific divisional chart:

```python
# Get the Navamsa (D9) chart
d9_chart = astro.get_chart(division=9)

# The output is a dictionary mapping house numbers (1-12) to sign and planet data
for house, data in d9_chart.items():
    print(f"House {house}: Sign {data['sign']}")
    for planet in data['planets']:
        print(f"  - {planet['name']} at {planet['longitude']:.2f}°")
```
