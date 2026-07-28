---
title: Tropical and Sidereal Zodiacs
description: Understand signs, constellations, precession, ayanamsa, and why two valid calculations can disagree.
---

The zodiac is a longitude system along the ecliptic, the apparent annual path
of the Sun. Astrological signs divide that circle into twelve equal sections of
30 degrees. The named astronomical constellations are unequal regions of the
sky, so a zodiac sign is not the same thing as the modern constellation that
shares its name.

## Tropical zodiac

The tropical zodiac anchors zero degrees Aries to the March equinox. Its signs
remain tied to the seasonal equinox-and-solstice framework rather than to a
selected stellar zero point. This is the dominant zodiac in modern Western
astrology, but it is not the only zodiac used by Western astrologers.

## Sidereal zodiac

A sidereal zodiac defines its zero point relative to a stellar reference.
Because Earth's equinox moves relative to the stars through precession, a
sidereal longitude is commonly calculated by subtracting an **ayanamsa** from a
tropical longitude:

```text
sidereal longitude = tropical longitude - ayanamsa for the date
```

This is the traditional relation documented by
[Swiss Ephemeris](https://www.astro.com/swisseph/swisseph.htm). Different
ayanamsas define the reference point differently, so they can place a body at
slightly different sidereal longitudes and can change a sign or nakshatra near
a boundary.

## Ayanamsa is part of the chart identity

Lahiri, Raman, and Krishnamurti are not interpretive systems by themselves in
Ascendant; they are supported sidereal reference choices. A reproducible chart
should record:

- the ayanamsa name,
- the date and time standard,
- the geographic coordinates,
- the house system,
- and the software or ephemeris version.

Ascendant defaults to Lahiri. Its other supported modes are listed on
[Configuration](/docs/configuration). Swiss Ephemeris documents its
[sidereal mode API and named ayanamsas](https://www.astro.com/swisseph-download/doc/swephprg.2.10.htm#_Toc112949044).

## Zodiac and house system are separate choices

A zodiac determines planetary and sign longitudes. A house system determines
house boundaries. A chart can therefore be:

- tropical with Placidus houses,
- sidereal with Whole Sign houses,
- sidereal with Placidus houses,
- or another supported combination.

Do not infer one setting from the other.

## How to compare two charts

Before interpreting a disagreement:

1. Confirm that both charts use the same birth moment and timezone.
2. Confirm tropical or sidereal.
3. If sidereal, confirm the ayanamsa.
4. Confirm geocentric or topocentric positions where relevant.
5. Confirm the house system.
6. Compare exact longitudes before comparing sign and house labels.

Only after the calculation model matches should you investigate a possible
software or interpretation error.

