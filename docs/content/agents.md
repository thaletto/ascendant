---
title: Agent Workflows
description: Install Ascendant skills and give coding agents reliable astrology workflows backed by local calculations.
---

Ascendant pairs deterministic calculations with installable agent skills. The Python package produces the chart data; the skills tell an agent which evidence to inspect, which safety boundaries to keep, and how to structure a useful response.

## Install with the Skills CLI

Run this from the project where your agent works:

```bash
npx skills add thaletto/ascendant
```

The Skills CLI discovers the `plugins/agent/skills` pack in this repository and installs the available workflows for your agent environment.

Install the calculation package as well when a workflow needs to generate charts or transits:

```bash
python3 -m pip install astro-ascendant
```

## Available skills

| Skill | Use it for |
|---|---|
| `init-person` | Save birth details and prepare reusable chart and timing records |
| `get-transit` | Compare current or dated planetary positions with a saved birth chart |
| `daily-transit` | Explain short-term planetary movement in practical language |
| `career` | Work direction, recognition, professional changes, and timing |
| `finance` | Income, savings, risk, and money-related timing |
| `health` | Careful, non-diagnostic guidance about vitality and routines |
| `education` | Learning style, exams, higher education, and study timing |
| `family` | Parents, siblings, children, and family relationships |
| `marriage` | Partnership patterns, pressure points, and timing |
| `property` | Homes, land, vehicles, costs, and purchase timing |
| `relationship-compatibility` | Compare two complete charts without reducing them to one score |

## A reliable agent flow

1. Use `init-person` when the user provides a name, complete birth time with timezone, latitude, and longitude.
2. Let the skill save generated records under `persons/<name>/`.
3. Read the stored chart and Dasha data before interpreting it.
4. Use `get-transit` when the question depends on the current sky or a specific date.
5. Apply the matching domain skill, cite the chart factors used, and keep advice within that skill's safety boundaries.

This separation matters: calculations remain reproducible, while interpretation stays visible and reviewable instead of being hidden inside a model prompt.

## Example prompts

After installation, ask your agent in ordinary language:

```text
Save Priya's birth details and prepare her chart records.
```

```text
Using Priya's saved chart, explain the current career period and show the chart factors behind the answer.
```

```text
Compare today's transits with Priya's birth chart and give a practical three-day outlook.
```

The agent should locate the relevant installed skill automatically. You do not need to paste the skill instructions into every request.

## Codex plugin installation

In Codex, open **Plugins**, click **Add Marketplace**, and paste the Ascendant Git repository URL:

```text
https://github.com/thaletto/ascendant.git
```

That adds the Ascendant marketplace and its packaged Codex experience. Use the Skills CLI when you want a portable skill installation instead.

## Evidence and safety

- Treat astrology as interpretive guidance, not certainty.
- Do not invent chart values, Ashtakavarga scores, or dates that are absent from the calculated records.
- Use complete birth data for another person's chart; label indirect family readings clearly.
- Do not replace medical, legal, or financial professionals with an astrology response.
- Keep the calculation output available so a user or another agent can audit the reasoning.
