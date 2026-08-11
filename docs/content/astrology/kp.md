---
title: Krishnamurti Paddhati (KP)
description: Learn how KP combines sidereal cusps, star lords, sub-lords, significators, and ruling planets.
---

Krishnamurti Paddhati, usually called KP, is a modern Indian astrological system
developed by K. S. Krishnamurti. It combines sidereal planetary positions with
a cusp-centered and stellar subdivision method. KP is more than selecting an
ayanamsa named “Krishnamurti.” Krishnamurti's own
[*Predictive Stellar Astrology*](https://books.google.com/books/about/Krishnamurti_Padhdhati_predictive_Stella.html?id=lJ5WAAAAMAAJ)
is the primary system reference used here.

## Calculation framework

A reproducible KP chart normally declares:

- Krishnamurti ayanamsa,
- Placidus house cusps,
- planetary and cuspal longitudes,
- nakshatra or star lords,
- sub-lords derived from the Vimshottari proportions,
- and the node and significator rules used by the practitioner.

Swiss Ephemeris exposes Krishnamurti sidereal modes and Placidus houses as
separate calculation choices. Ascendant exposes those choices through
[Configuration](/docs/configuration).

## Star lord and sub-lord

Each zodiacal position falls in one of the 27 nakshatras and therefore has a
star lord. KP subdivides that nakshatra in the Vimshottari dasha proportions,
producing a sub-lord. The sub-lord is used for fine judgment, especially at a
house cusp.

This is not the same as the four equal nakshatra padas. A pada is 3°20′; KP
subdivisions are unequal because their lengths follow planetary period
proportions.

## Cusps and significators

KP emphasizes the exact cusps of houses. Its judgment derives significators
through a ranked relationship among occupation, ownership, star-lord
connections, nodes, and other declared rules. A query is framed through houses
that promise the event, oppose it, or describe its context.

Because ranking and node treatment matter, software should expose the
significator chain rather than return only “yes” or “no.”

## Ruling planets and timing

Ruling planets are selected from factors tied to the moment of judgment, such
as the Ascendant and Moon at that time, under the chosen KP rules. They are used
with significators and period lords to narrow timing or validate a selection.
They are not a substitute for calculating natal cusps and sub-lords.

## KP is not just an ayanamsa

This distinction is essential:

```text
Krishnamurti ayanamsa
    = a sidereal coordinate choice

KP astrology
    = ayanamsa + cusps + star lords + sub-lords
      + significators + ruling planets + timing rules
```

Setting `ayanamsa="Krishnamurti"` in Ascendant changes the sidereal longitude
reference. Setting `house_system="Placidus"` changes house calculation. The
current agent skills still apply `parashari_raman_jaimini_v3`; they do not become a KP
interpreter.

## Ascendant support boundary

Ascendant currently supplies several ingredients—sidereal positions,
Krishnamurti ayanamsa options, internal Placidus cusp calculations,
nakshatra metadata, internal sub-lord metadata, and Vimshottari periods. Public
planet records do not expose all of that metadata, and public `get_chart()`
membership remains sign-based. The public skill hierarchy does not define
cuspal sub-lord judgments, KP significator rankings, ruling planets, or KP
event predicates.

See [Sources](/docs/astrology/sources) for the KP Readers and Swiss Ephemeris
calculation references.
