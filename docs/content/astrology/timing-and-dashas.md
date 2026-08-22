---
title: Timing and Dashas
description: Separate natal promise from planetary periods, sign periods, transits, and event timing.
---

A birth chart is a map for one moment. Timing methods relate that map to a
later period. They do not all use the same clock: a transit follows current
motion, a planetary dasha assigns periods to grahas, and a rashi dasha assigns
periods to signs.

## Natal promise comes first

Before timing a topic, identify its natal foundation:

1. the relevant house or houses,
2. their lords,
3. planets occupying or influencing them,
4. the condition of those planets,
5. the declared divisional chart,
6. and supporting or constraining combinations.

Timing then asks when those factors become active. If the natal evidence is
missing or contradictory, a date should be presented with corresponding
caution.

## Vimshottari dasha

Vimshottari is a 120-year planetary-period framework. Its standard sequence is:

```text
Ketu → Venus → Sun → Moon → Mars → Rahu → Jupiter → Saturn → Mercury
```

The Moon's nakshatra at birth establishes the starting lord and remaining
balance. A Mahadasha is the major period; Antardasha subdivides it, with deeper
levels available in fuller practice.

Ascendant exposes:

```python
timeline = astro.get_dasha_timeline()
current = astro.get_current_dasha()
dated = astro.get_current_dasha(date="15-08-2025")
```

See the [Dasha API guide](/docs/library/dasha) for the result shape.

## How a dasha is interpreted

A period lord does not have one universal meaning. Its result is derived from
the natal chart, including:

- houses owned,
- house occupied,
- sign and dignity,
- conjunctions and aspects,
- relevant varga placement,
- and the relationship between major and sub-period lords.

The current Ascendant topic rubrics rank active Mahadasha and Antardasha lords
according to the houses that govern the selected topic. Dasha is an activation
layer below natal promise and the relevant varga, so it can time a pattern but
cannot invent one. This is an auditable developer-authored method, not a
summary of every classical dasha rule.

## Transits

Transits compare dated planetary positions with the natal chart. Slow planets
can describe a long background, while faster bodies describe shorter changes.
A reproducible transit statement needs:

- an exact timestamp and timezone,
- the natal calculation settings,
- the transit longitude or natal house reached,
- and the natal factor being activated.

The Ascendant skills report dated transit facts after natal and dasha evidence;
transits do not overwrite natal status.

## Other timing systems

Jyotisha contains many dashas. Parashari practice can use planetary dashas such
as Vimshottari under stated eligibility rules. Jaimini practice is especially
known for sign-based dashas such as Chara dasha. KP uses period lords together
with its star-lord, sub-lord, significator, cusp, and ruling-planet framework.

Do not combine their outputs as though the systems used identical predicates.
Record the system, variant, period calculation, and interpretation rules.

## Timing language

Prefer language proportional to the evidence:

- “The period activates the relevant lords” describes a rule match.
- “The transit reaches the natal tenth house” describes a calculated fact.
- “This guarantees a promotion” makes a certainty claim the calculation does
  not establish.

Astrology should not be used as proof of another person's feelings, consent,
medical diagnosis, legal outcome, or guaranteed financial result.
