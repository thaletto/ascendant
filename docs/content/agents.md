---
title: Agent workflows
description: Install Ascendant skills and give coding agents reliable astrology workflows backed by local calculations.
---

Use these workflows when you want your coding agent to calculate astrology data locally and explain it responsibly. The Python package produces the chart data; each skill tells your agent what evidence to inspect, which safety boundaries to keep, and how to structure a useful response.

## Install with the Skills CLI

Run this in the project where your agent works:

```bash
npx skills add thaletto/ascendant
```

The Skills CLI discovers the `plugins/agent/skills` pack in this repository and installs the workflows available to your agent environment.

Also install the calculation package when you need a workflow to generate charts or transits:

```bash
python3 -m pip install astro-ascendant
```

## Browse the skill specifications

The skill specifications are available under **Skill specifications** in the
left sidebar. They are published directly from the plugin's canonical
`SKILL.md` files. The website regenerates those pages during development and
production builds, so the documentation cannot drift into a second maintained
copy.

## Give your agent a reliable flow

1. Use `init-person` when the user provides a name, complete birth time with timezone, latitude, and longitude.
2. Let the skill save generated records under `persons/<name>/`.
3. Re-running matching v1 records upgrades their provenance to v2 while preserving `CONTEXT.md` and chart artifacts.
4. Read the stored chart and Dasha data before interpreting it.
5. Use `get-transit` when the question depends on the current sky or a specific date.
6. Apply the matching domain skill, cite the chart factors used, and keep advice within that skill's safety boundaries.

This keeps your calculations reproducible and your interpretation visible for review instead of hiding it inside a model prompt.

## Example prompts

After installation, you can ask your agent in ordinary language:

```text
Save Priya's birth details and prepare her chart records.
```

```text
Using Priya's saved chart, explain the current career period and show the chart factors behind the answer.
```

```text
Compare today's transits with Priya's birth chart and give a practical three-day outlook.
```

Your agent should locate the relevant installed skill automatically; you do not need to paste skill instructions into every request.

## Codex plugin installation

In Codex, open **Plugins**, click **Add Marketplace**, and paste the Ascendant Git repository URL:

```text
https://github.com/thaletto/ascendant.git
```

This adds the Ascendant marketplace and its packaged Codex experience. Use the Skills CLI instead when you want a portable skill installation.

## Evidence and safety

- Treat astrology as interpretive guidance, not certainty.
- Do not invent chart values, Ashtakavarga scores, or dates that are absent from the calculated records.
- Use complete birth data for another person's chart; label indirect family readings clearly.
- Do not replace medical, legal, or financial professionals with an astrology response.
- Keep the calculation output available so a user or another agent can audit the reasoning.
