---
title: Jaimini Astrology
description: Understand Ascendant's named seven-karaka Jaimini core and how the skills keep it distinct inside a combined reading.
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
of Rahu. Ascendant declares `jaimini_srao_7_core_v1`: Sun through Saturn are
ranked by degree within sign. An exact degree-minute-second tie is recorded as
a shared role, with Rao's reverse-Rahu fallback identified rather than hidden.

## Rashi drishti

Jaimini's sign aspects are not ordinary planet-to-planet aspects:

- movable signs aspect fixed signs except the adjacent fixed sign,
- fixed signs aspect movable signs except the adjacent movable sign,
- dual signs aspect the other dual signs.

Planets influence through the signs they occupy under this framework. Do not
silently substitute Parashari graha drishti.

## Arudha padas

An arudha represents a projected or manifest image of a house. Ascendant uses
Rao's literal projection: count from a house to its lord, then project the same
distance from the lord. It preserves the same and opposite results described
in that source rather than adding an unnamed modern correction. The Arudha
Lagna is the best-known example; Upapada is the projection of the twelfth.

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

`Ascendant.get_jaimini()` calculates the named seven-karaka core: Chara
Karakas, Rashi Drishti, Karakamsha, all twelve Arudha Padas, Upapada, and raw
Argala contributors and blockers. The raw Argala result keeps primary support
from the second, fourth, and eleventh distinct from obstruction through the
twelfth, tenth, and third; it also records secondary support from the fifth and
its ninth-place obstruction. Ketu's calculation is stored separately in reverse
order. The skill hierarchy applies only the factor named by each topic rubric
and compares it with the Parashari natal result.

Chara Dasha remains outside the implemented core because its starting sign,
direction, duration, and exception rules require a separately named method.

See [Sources](/docs/astrology/sources) for editions of the *Jaimini Sutras* and
B. V. Raman's modern methodological study.
