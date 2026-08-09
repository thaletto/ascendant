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
8. Apply the developer-owned factor rank within each evidence layer.
9. State missing evidence and keep every material claim traceable.

This sequence keeps natal structure separate from timing and prevents a single
transit from becoming the whole reading.

## What `parashari_raman_v2` means

The agent workflow is a **curated interpretive hierarchy**, not a complete
digital edition of BPHS. It separates two kinds of precedence:

- Evidence layers run from natal promise through the relevant varga,
  Vimshottari activation, transit triggers, and SAV corroboration.
- Within a layer, factors are primary, corroborating, modifying, or
  background.

Higher factors control. Repeated lower factors cannot outvote them, and
equally ranked contradictions remain mixed unless a topic rubric supplies an
explicit tie-breaker. The agent inspects saved artifacts directly, applies the
hierarchy, and explains the result in natural prose. Calculation scripts
create chart or transit data; they do not decide meaning.

Each material conclusion cites its saved artifact and its exact external source
locator. Developer-authored rules without an external locator are labeled
`Ascendant methodology`. Each specialist skill carries the `parashari_raman_v2`
hierarchy and process under its own `references/hierarchy.md` and
`references/process.md`, so a skills.sh install of that skill always includes
its knowledge; the topic-specific rubric lives at `references/topic.md`.

## What it does not yet encode

The current hierarchy does not claim to define every:

- planetary aspect and special aspect,
- yoga and cancellation rule,
- avastha or strength system,
- varga dignity synthesis,
- dasha eligibility exception,
- or remedial tradition.

That boundary is intentional. Developer-owned, cited rules can be audited and
expanded one topic at a time while the agent retains natural synthesis.

## Primary reading

The catalogue cites R. Santhanam's translation of *Brihat Parashara Hora
Shastra* for bhava, lord, varga, Vimshottari, and Ashtakavarga material, and
B. V. Raman's *How to Judge a Horoscope*, Volumes I and II, for a disciplined
house-by-house organization. See [Sources](/docs/astrology/sources) for the
full bibliography and scope notes.
