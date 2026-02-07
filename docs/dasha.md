# Dasha System

The library implements the **Vimshottari Dasha** system, which is the most widely used planetary period system in Vedic Astrology.

## Concepts

Vimshottari Dasha is based on the position of the Moon at the time of birth. It divides a 120-year cycle among the nine planets in a specific order:
Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, and Mercury.

## Usage

### Get Full Dasha Timeline

```python
timeline = astro.get_dasha_timeline()

for mahadasha in timeline:
    print(f"Mahadasha: {mahadasha['mahadasha']} ({mahadasha['start']} to {mahadasha['end']})")
    for antardasha in mahadasha['antardashas']:
        print(f"  - Antardasha: {antardasha['antardasha']} ({antardasha['start']} to {antardasha['end']})")
```

### Get Current Dasha

You can get the current Mahadasha and Antardasha for the current time or a specific date.

```python
# Get current dasha for now
current = astro.get_current_dasha()
print(f"Current MD: {current['mahadasha']['mahadasha']}")
print(f"Current AD: {current['antardasha']['antardasha']}")

# Get dasha for a specific date
specific_date = "15-08-2025"
dasha_then = astro.get_current_dasha(date=specific_date)
```
