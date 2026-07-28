---
title: Houses and Divisional Charts
description: Learn what houses represent, how house systems differ, and why vargas are a separate layer.
---

Houses and signs both use twelvefold language, but they answer different
questions. A **sign** describes a zodiacal region. A **house** organizes the
chart around the local horizon, meridian, or a defined relationship to the
Ascendant.

## The twelve houses

The following themes paraphrase the Parashari house scheme recorded in
[BPHS chapters 11–20](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par1120.html).
They are a learning map, not a complete prediction:

| House | Core field |
| --- | --- |
| 1 | Body, identity, vitality, and approach |
| 2 | Resources, speech, family assets, and sustenance |
| 3 | Initiative, skills, communication, and siblings |
| 4 | Home, foundations, property, and inner security |
| 5 | Learning, creativity, children, and counsel |
| 6 | Work, service, illness, conflict, and obligations |
| 7 | Partners, contracts, and other people |
| 8 | Vulnerability, shared resources, discontinuity, and longevity |
| 9 | Teachers, principles, higher learning, and long journeys |
| 10 | Action, profession, responsibility, and public role |
| 11 | Gains, networks, fulfilment, and elder peers |
| 12 | Expenditure, retreat, loss, foreign settings, and release |

A judgment should combine the house, its sign, its lord, occupants, aspects,
relevant combinations, and timing. An empty house is not an absent life area;
its lord still carries the house.

## House systems

**Whole Sign** assigns the entire rising sign to house one, the next sign to
house two, and so on. **Equal** systems use equal 30-degree houses from a
defined starting point. **Placidus** and **Porphyry** divide arcs using
different geometrical constructions, so cusps and house placement can differ.

Swiss Ephemeris documents the geometry and codes for
[Whole Sign, Equal, Placidus, and Porphyry houses](https://www.astro.com/swisseph/swisseph.htm).
Ascendant's supported choices are listed on
[Configuration](/docs/configuration).

Ascendant currently calculates the selected Swiss cusp set internally, while
public `get_chart()` output remains one sign per numbered house. Consult the
[configuration boundary](/docs/configuration#current-public-chart-boundary)
before expecting a non-Whole-Sign choice to change planet-to-house membership.

## Bhava is not automatically rashi

In Whole Sign houses, sign and house boundaries coincide. In quadrant and
other cusp-based systems, a sign can span parts of multiple houses. Always
state whether a rule expects:

- the sign counted from the Ascendant,
- a bhava or house cusp,
- the house occupied by a planet,
- or the lord of a house.

## Divisional charts or vargas

Vargas subdivide a planet's position within a sign and map it into another
zodiacal chart according to a division-specific rule. They are not produced by
changing the birth time, and they are not the same as selecting another house
system.

Common examples include:

- D1 Rashi for the foundational natal chart,
- D2 Hora for resources,
- D4 Chaturthamsa for property and fixed assets,
- D9 Navamsa for strength, dharma, and partnership analysis,
- D10 Dasamsa for profession,
- D24 Chaturvimsamsa for education.

See [Divisional Charts](/docs/library/charts) for every division supported by
Ascendant.

## Use vargas after the natal chart

A stable workflow is:

1. Establish the D1 house and lord relevant to the topic.
2. Judge the planet's condition in D1.
3. Open only the varga declared for that topic.
4. Compare the repeated or changed pattern.
5. Apply a timing method.

The packaged Ascendant skills follow this D1-first order. A missing required
varga produces insufficient evidence rather than permission to improvise.
