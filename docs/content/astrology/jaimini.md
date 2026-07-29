---
title: Jaimini Astrology
description: Understand sign aspects, variable significators, arudhas, and sign dashas without mixing them into Parashari rules.
---

Jaimini astrology is a distinct rule tradition associated with the *Jaimini
Upadesa Sutras*. It shares the same chart data with other Jyotisha systems but
often selects significators, aspects, and timing through different rules.
Terminology and calculation variants must be named because modern lineages do
not resolve every sutra identically. B. Suryanarain Rao's
[*Sri Jaiminisutras*](https://books.google.com/books/about/Sri_Jaiminisutras.html?id=z4v4gjJ_ay0C)
provides Sanskrit, transliteration, translation, and commentary; its commentary
should be distinguished from the sutra text.

## Chara karakas

Chara karakas are variable significators assigned by comparing planetary
degrees within signs. A common scheme includes:

- Atmakaraka,
- Amatyakaraka,
- Bhratrikaraka,
- Matrikaraka,
- Putrakaraka,
- Gnatikaraka,
- and Darakaraka.

Some lineages use seven and others eight, affecting the inclusion and treatment
of Rahu. A program must declare the scheme and tie-breaking behavior before
producing a result.

## Rashi drishti

Jaimini's sign aspects are not ordinary planet-to-planet aspects:

- movable signs aspect fixed signs except the adjacent fixed sign,
- fixed signs aspect movable signs except the adjacent movable sign,
- dual signs aspect the other dual signs.

Planets influence through the signs they occupy under this framework. Do not
silently substitute Parashari graha drishti.

## Arudha padas

An arudha represents a projected or manifest image of a house. Its calculation
counts from a house to its lord and projects an equal distance from the lord,
with special handling in defined same-sign or opposite-sign cases. The Arudha
Lagna is the best-known example, but each house can have an arudha.

Because exception rules materially change the result, a chart output should
identify the exact arudha algorithm rather than expose only a label.

## Karakamsha and sign-based synthesis

The navamsa sign occupied by the Atmakaraka is central to Karakamsha analysis.
Jaimini judgment can combine chara karakas, sign aspects, arudhas, argala, and
other sutra-based rules. These factors should be evaluated as a coherent
Jaimini system rather than scattered into a Parashari house-lord checklist.

## Chara dasha

Chara dasha assigns periods to signs rather than planets. The starting sign,
direction, period lengths, and exceptions depend on the selected method.
Implementations must name their lineage or algorithm; “Jaimini dasha” alone is
not enough to reproduce the sequence.

## Ascendant support boundary

Ascendant can calculate D1 and D9 chart data that a Jaimini implementation
would need. The current public skill hierarchy does **not** define chara
karakas, rashi drishti, arudhas, argala, Karakamsha, or Chara dasha. Its
educational description here must not be mistaken for implemented output.

See [Sources](/docs/astrology/sources) for editions of the *Jaimini Sutras* and
B. V. Raman's modern methodological study.
