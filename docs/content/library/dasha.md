---
title: Dasha System
description: Work with Vimshottari Dasha timelines and current planetary periods.
---

Use Vimshottari Dasha when you want structured Mahadasha and Antardasha records instead of prose that your application has to parse.

## Understand the timeline

Vimshottari Dasha is based on the position of the Moon at the time of birth. It divides a 120-year cycle among the nine planets in a specific order:
Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, and Mercury.

## Read a Dasha period

### Get the full timeline

```python
timeline = astro.get_dasha_timeline()

for mahadasha in timeline:
    print(f"Mahadasha: {mahadasha['mahadasha']} ({mahadasha['start']} to {mahadasha['end']})")
    for antardasha in mahadasha['antardashas']:
        print(f"  - Antardasha: {antardasha['antardasha']} ({antardasha['start']} to {antardasha['end']})")
```

### Get the active period

Get the Mahadasha and Antardasha that are active now, or on a date you provide in `DD-MM-YYYY` format.

```python
# Get current dasha for now
current = astro.get_current_dasha()
print(f"Current MD: {current['mahadasha']['mahadasha']}")
print(f"Current AD: {current['antardasha']['antardasha']}")

# Get dasha for a specific date
specific_date = "15-08-2025"
dasha_then = astro.get_current_dasha(date=specific_date)
```

`mahadasha` or `antardasha` can be `None` when your date falls outside the computed timeline. Check the result before you present a period as active.
