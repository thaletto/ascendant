---
title: Astrology as a System
description: Build a clear mental model of zodiacs, planets, stars, houses, charts, and timing before comparing traditions.
---

Astrology is not one universal technique. It is a family of traditions that
map astronomical positions into symbolic frameworks. A useful chart reading
therefore starts by naming its coordinate system, house system, interpretive
rules, and timing method. Mixing those layers without saying so makes a reading
difficult to reproduce.

This guide teaches the layers in that order. It describes astrology as a
historical and interpretive practice; it does not present astrological
prediction as scientifically established fact.

## The six layers of a reading

1. **Astronomical data** — a time, location, planetary longitude, and reference
   frame.
2. **Zodiac** — tropical or sidereal longitudes divided into twelve signs.
3. **Houses** — twelve areas anchored to the local horizon and meridian, or to
   the rising sign in Whole Sign houses.
4. **Symbolic factors** — planets or grahas, signs, nakshatras, aspects,
   dignities, house lordships, and combinations.
5. **Derived charts and points** — vargas, lots, arudhas, cuspal sub-lords, or
   other constructs defined by a tradition.
6. **Timing** — transits, planetary periods, sign periods, directions, or other
   time-lord methods.

The same sky can produce different chart structures when two practitioners use
different zodiacs or house systems. The calculation choice must be settled
before interpretation begins. Swiss Ephemeris describes the underlying
[sidereal conversion and ayanamsa model](https://www.astro.com/swisseph/swisseph.htm)
and its independent [house calculation methods](https://www.astro.com/swisseph-download/doc/swephprg.2.10.htm#_Toc112949056).

## Western, Indian, tropical, and sidereal

“Western” and “tropical” are not synonyms. Modern Western astrology commonly
uses a tropical zodiac, but Western sidereal schools also exist. Indian
astrology commonly uses a sidereal zodiac, while its texts and practices
contain several distinct interpretive systems. **Tradition** describes a body
of methods; **zodiac** describes a coordinate convention.

Start with [Tropical and sidereal zodiacs](/docs/astrology/zodiacs), then learn
the structure of [Western astrology](/docs/astrology/western) and how
[planets, stars, and nakshatras](/docs/astrology/planets-and-stars) occupy
[houses and divisional charts](/docs/astrology/houses-and-vargas).

## Natal promise and timing

In the workflow documented here, the natal chart describes the underlying
pattern and a timing method describes when parts of that pattern become
relevant. A transit or dasha should not silently invent a result that has no
foundation in the natal analysis. See
[Timing and dashas](/docs/astrology/timing-and-dashas).

## Compare the major systems

| System | Main emphasis | Typical timing tools |
| --- | --- | --- |
| [Parashari](/docs/astrology/parashari) | Planets, house lords, dignities, aspects, yogas, and vargas | Vimshottari and other dashas, transits |
| [Jaimini](/docs/astrology/jaimini) | Sign aspects, variable karakas, arudhas, and sign-based rules | Chara and other rashi dashas |
| [KP](/docs/astrology/kp) | Cusps, star lords, sub-lords, significators, and ruling planets | Periods plus cuspal and ruling-planet judgment |

These systems share vocabulary but do not make every decision in the same way.
For example, selecting Krishnamurti ayanamsa changes a coordinate setting; a KP
judgment additionally requires KP's cuspal, star-lord, sub-lord, and
significator rules.

## What Ascendant implements

The Python library calculates sidereal charts, divisional charts, Vimshottari
periods, yogas, Ashtakavarga, and Swiss Ephemeris cusps for its supported
house-system codes. The current public chart result remains sign-based and does
not expose cusp membership. The packaged agent skills use the
`parashari_raman_v1` catalogue: D1 first, then the topic-specific varga when
required, Vimshottari Mahadasha and Antardasha, dated transits, and
Sarvashtakavarga corroboration.

The skills do **not** currently implement a general Jaimini or KP interpreter.
Those pages are educational comparisons, not promises of library output. The
exact skill workflow is described on [Getting Started](/docs) and
[Agent Workflows](/docs/agents).
