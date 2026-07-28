---
title: Parashari Astrology
description: Learn the planet-and-house-led framework used as the foundation of Ascendant's agent skills.
---

Parashari astrology is the principal interpretive foundation used by
Ascendant's packaged skills. The name refers to a broad textual and teaching
tradition associated with *Brihat Parashara Hora Shastra* (BPHS), not to one
small modern checklist.

## Core building blocks

A Parashari judgment commonly relates:

- grahas and their natural roles,
- signs, sign lords, and planetary dignity,
- houses and house lords,
- planetary aspects,
- yogas or defined combinations,
- divisional charts,
- dashas, especially Vimshottari,
- and corroborating transit or Ashtakavarga evidence.

These factors are relational. For example, “Saturn” is not a complete result:
its houses owned, house occupied, sign condition, associations, aspects,
varga condition, and current period all change the judgment.

## A practical judgment sequence

Ascendant documents a reproducible sequence influenced by the
house-by-house discipline of B. V. Raman:

1. Select the life topic and its relevant D1 houses.
2. Identify each house's sign and lord.
3. Locate the lord and inspect its saved dignity.
4. Repeat the declared checks in the topic-specific varga.
5. Check the active Vimshottari Mahadasha and Antardasha.
6. Add dated transits.
7. Add saved Sarvashtakavarga scores as supporting context.
8. State missing evidence and keep every claim traceable to its rule.

This sequence keeps natal structure separate from timing and prevents a single
transit from becoming the whole reading.

## What `parashari_raman_v1` means

The agent evaluator is a **curated software rule catalogue**, not a complete
digital edition of BPHS. For each selected house it:

- identifies the sign lord,
- locates that lord by house,
- treats `Exalted`, `Moola Trikona`, `Own`, and `Friend` as support,
- treats `Debilitated`, `Enemy`, or lord placement in 6, 8, or 12 as a
  constraint,
- and treats other available results as neutral.

Topic rules declare the D1 houses and required varga. Timing is marked as
jointly active only when both current period lords are selected house lords.
Transits and SAV remain supplementary.

Every emitted sentence cites the saved artifact, a `PR-*` rule identifier, and
the catalogue's source identifiers. The exact operational rules live in the
packaged
[`rule-catalogue.md`](https://github.com/thaletto/ascendant/blob/main/plugins/agent/ascendant/skills/parashari-judgement/references/rule-catalogue.md).

## What it does not yet encode

The current catalogue does not claim to implement every:

- planetary aspect and special aspect,
- yoga and cancellation rule,
- avastha or strength system,
- varga dignity synthesis,
- dasha eligibility exception,
- Ashtakavarga threshold,
- or remedial tradition.

That boundary is intentional. A deterministic, cited subset can be audited and
expanded rule by rule; an unnamed mixture of remembered rules cannot.

## Primary reading

The catalogue cites R. Santhanam's translation of *Brihat Parashara Hora
Shastra* for bhava, lord, varga, Vimshottari, and Ashtakavarga material, and
B. V. Raman's *How to Judge a Horoscope*, Volumes I and II, for a disciplined
house-by-house organization. See [Sources](/docs/astrology/sources) for the
full bibliography and scope notes.

