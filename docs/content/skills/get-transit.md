---
title: "Current planetary positions"
description: "Show where the planets are now, or at a requested date, compared with a person's birth chart."
---

> Generated from the canonical [`SKILL.md`](https://github.com/thaletto/ascendant/blob/main/plugins/agent/ascendant/skills/get-transit/SKILL.md). Edit the source specification, not this page.

Read [`../../../AGENTS.md`](https://github.com/thaletto/ascendant/blob/main/plugins/agent/AGENTS.md).

Use this skill when a user asks what is moving through their chart now or on a specific date.

## Inputs

- **Name:** a person already saved in `persons/<name>/`.
- **Date:** optional ISO date and time with a timezone; use the current moment when omitted.
- **Chart division:** optional; use the main birth chart by default.

From the user's project directory, run the bundled script using its installed skill path. If Ascendant is not installed, install the package first with `python3 -m pip install astro-ascendant`.

```bash
python3 <path-to-get-transit-skill>/scripts/get-transit.py --name "<name>" --date "<date>" --division 1
```

Leave out `--date` for the current moment. Use the requested chart division when one is provided.

## Result

Return the script's factual report with its saved-chart and computed-moment
citations. Interpret it only after reading the shared `parashari-judgement`
process and the selected topic hierarchy.

The report shows:

- each house and its sign;
- planets currently in each house;
- each planet's sign, degree, direction, birth-star, and quarter;
- the birth-chart house affected by each moving planet.

Use this report as dated evidence. The script calculates planetary positions;
it does not decide their meaning or weight.
