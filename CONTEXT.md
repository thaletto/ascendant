# Ascendant Jyotisha

This context defines the language for Ascendant's sidereal Jyotisha
calculations and saved birth records.

## Repository boundary

This repository contains the core Python library. The documentation website
lives in `thaletto/ascendant-docs`; agent workflows, the Codex plugin, and the
hosted MCP service live in `thaletto/ascendant-agents`. Their integration
vocabulary and runtime contracts do not belong to this core model.

## Chart language

**Natal chart (D1/Rashi)**:
The foundational chart calculated for a person's birth data. It establishes the
natal pattern that later timing and derived-chart analysis must relate back to.
_Avoid_: bare “chart” when the chart type is relevant.

**Divisional chart (Varga)**:
A chart derived from the natal chart for a specific division, such as D9. It is
not a second birth chart and does not change the person's birth data.
_Avoid_: treating a Varga as an independent natal chart.

**Lagna**:
The rising point that anchors the house sequence in a chart.
_Avoid_: using “Ascendant” for the library and the chart point in the same
sentence when the distinction matters.

**Sign (Rashi)**:
One of the twelve zodiacal regions occupied by the Lagna or a planet.
_Avoid_: using “sign” and “house” interchangeably.

**House (Bhava)**:
One of the twelve life-area positions organized around the Lagna or a selected
house system. A house is not automatically the same thing as the sign occupying
it.
_Avoid_: treating a Bhava as a synonym for Rashi outside Whole Sign houses.

## Jaimini core

**Chara Karakas**:
The seven planet roles derived under the saved Jaimini method. A Karaka selects
the planet that carries a topic role in this chart; it does not establish a
literal event or another person's private state. Atmakaraka is the self and
core-direction role; Darakaraka is the partnership role; other roles are read
only when the topic rubric selects them.
_Avoid_: treating a Karaka as a guarantee or substituting one role for another.

**Rashi Drishti**:
Jaimini's sign-to-sign influence. Use the saved sign-aspect map for it.
_Avoid_: importing Parashari planetary aspects or degree orbs.

**Karakamsha**:
The D9 sign occupied by the Atmakaraka. Topic rubrics may derive signs from it.
_Avoid_: treating Karakamsha as a replacement natal chart.

**Arudha Pada**:
The projected or visible expression of a house, calculated by the saved method.
**Upapada** is the twelfth-house Pada used for partnership themes.
_Avoid_: reading either Pada as a literal fact about status, ownership, or
another person's intent.

**Argala**:
The saved support and obstruction around a selected sign or Pada. Read its
contributors and blockers as evidence; the artifact is not a score.
_Avoid_: turning a count of contributors into a deterministic result.

**Parashari-Jaimini comparison**:
When a topic rubric declares both systems co-primary, judge each system by its
own rules before comparing them. Agreement strengthens natal confidence;
equally ranked disagreement remains mixed.
_Avoid_: letting one system silently borrow the other's aspects, significators,
or counting rules.

## Timing

**Vimshottari Dasha**:
The planetary timing framework used to describe when natal factors may become
active. Its periods can activate a natal pattern but cannot create one absent
from the natal chart.
_Avoid_: using “Dasha” without naming the timing system when other systems are
under discussion.

## Saved people

**Person**:
The human subject whose birth data is being examined.
_Avoid_: using “person” to mean the saved directory or calculation bundle.

**Person record**:
A reusable saved bundle representing one person's birth data and the chart,
timing, combination, and supporting results derived from it. Different records
may share a name while representing different birth inputs.
_Avoid_: “profile” when referring to this calculation record.
