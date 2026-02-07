# Yoga Combinations

Yogas are specific planetary combinations in a chart that produce unique results. Ascendant includes a comprehensive registry of hundreds of classical Yogas.

## Types of Yogas

The library categorizes yogas into:
- **Positive**: Beneficial combinations (e.g., Dhana Yogas, Raja Yogas)
- **Negative**: Challenging combinations (e.g., Aristha Yogas)
- **Neutral**: Combinations that have mixed or specific structural effects

## Key Yogas Supported

A few examples of supported yogas include:

| Yoga | Description |
|---|---|
| **GajaKesari** | Jupiter in a Kendra from the Moon. Brings fame and intelligence. |
| **Pancha Mahapurusha** | Five great person yogas (Hamsa, Malavya, Bhadra, Ruchaka, Sasa). |
| **Buddha Aditya** | Conjunction of Sun and Mercury. |
| **Chandra Mangala** | Conjunction of Moon and Mars. |
| **Adhi Yoga** | Benefics in 6th, 7th, and 8th from Moon or Lagna. |
| **Malika Yogas** | Continuous occupation of houses by planets. |

## Usage

To compute all yogas present in a chart:

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

## Yoga Object Structure

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
