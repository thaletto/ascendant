---
title: Planets, Stars, and Nakshatras
description: Distinguish astronomical bodies from astrological grahas, signs, fixed stars, and lunar mansions.
---

Astrology uses several overlapping maps of the sky. “Planet,” “graha,” “star,”
“sign,” and “nakshatra” are not interchangeable terms.

## Planets and grahas

In a modern astronomical description, the Sun is a star, the Moon is Earth's
satellite, and Rahu and Ketu are the lunar nodes. In Jyotisha, all four can be
treated as **grahas** because the category describes their astrological role,
not their modern astronomical classification.

The nine grahas commonly used in natal Jyotisha are:

| Graha | Astronomical referent |
| --- | --- |
| Surya | Sun |
| Chandra | Moon |
| Mangala | Mars |
| Budha | Mercury |
| Guru or Brihaspati | Jupiter |
| Shukra | Venus |
| Shani | Saturn |
| Rahu | Ascending lunar node |
| Ketu | Descending lunar node |

Ascendant calculates these nine factors. Its chart records include longitude,
retrograde state where applicable, sign, sign lord, nakshatra, nakshatra lord,
and pada.

## Signs describe position and condition

A sign gives a 30-degree zodiacal region. A tradition may then derive:

- the sign's ruler,
- a planet's dignity or relationship in that sign,
- aspects or sign aspects,
- and the houses ruled by that planet.

These are interpretive layers placed on the calculated longitude. The
longitude is the data; rulership and dignity belong to the selected rule
system.

## Fixed stars and constellations

Astronomical fixed stars have their own longitudes and latitudes and slowly
change apparent position over long periods. Swiss Ephemeris provides a
separate [fixed-star calculation interface](https://www.astro.com/swisseph-download/doc/swephprg.2.10.htm#_Toc112949027).
A fixed-star conjunction normally requires an explicitly chosen star, epoch,
coordinate convention, and orb.

Do not treat a whole 30-degree sign as though it were one physical
constellation or one fixed star.

Ascendant's current public chart builder does not call that fixed-star
interface. Fixed stars are included here for education, not as a documented
library output.

## The 27 nakshatras

The common 27-nakshatra scheme divides the zodiac into equal segments of
13°20′. Each nakshatra has four padas of 3°20′. Nakshatras therefore form a
regular zodiacal division even though their names are associated with stars or
stellar groups. BPHS connects the birth nakshatra to nakshatra-based dashas in
its [dasha chapters](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par4650.html).

Nakshatras matter structurally in several systems:

- the Moon's nakshatra determines the starting point and balance of
  Vimshottari dasha,
- KP subdivides nakshatras into unequal sub-lord portions,
- electional and interpretive traditions assign qualities to nakshatras and
  padas.

The mathematical division and the interpretive meaning should be documented
separately. Ascendant exposes the calculated nakshatra and pada in each planet's
chart data; the agent skills use that data only through their declared rules.

The current longitude helper uses decimal approximations for 13°20′ and 3°20′
intervals to preserve released output. Values extremely close to a boundary
should therefore be verified before they are treated as exact.

## A disciplined reading order

For each factor, keep four questions separate:

1. **Where is it?** Sign, degree, house, nakshatra, and pada.
2. **What does it own?** Houses or signs ruled in the chosen system.
3. **What modifies it?** Dignity, aspects, conjunctions, combustion,
   retrogradation, or other declared conditions.
4. **When is it active?** Dasha, transit, or another timing method.

This order prevents a generic planet keyword from replacing chart-specific
reasoning.
