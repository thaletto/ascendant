---
title: "Save birth details"
description: "Save a person's birth details and prepare reusable charts, timing, yoga, and SAV information used by the astrology skills."
---

> Generated from the canonical [`SKILL.md`](https://github.com/thaletto/ascendant/blob/main/plugins/agent/ascendant/skills/init-person/SKILL.md). Edit the source specification, not this page.

Use this skill when the user provides a name, birth date and time with timezone, latitude, and longitude.

From the user's project directory, run the bundled script using its installed skill path. If Ascendant is not installed, install the package first with `python3 -m pip install astro-ascendant`.

```bash
python3 <path-to-init-person-skill>/scripts/init-person.py \
  --name "<name>" \
  --dob "<YYYY-MM-DDTHH:MM:SS+HH:MM>" \
  --latitude <latitude> \
  --longitude <longitude>
```

The command creates `persons/<name>/`, saves the original details, and prepares:

- divisional charts under `charts/`
- planetary periods in `dasha.json`
- yoga results in `yogas.json`
- the complete Ashtakavarga/Sarvashtakavarga result in `sav.json`

Running it again with the same details reuses the existing record. If an older record is missing `sav.json`, the command backfills it in place. If the same name is used with different birth details, a numeric suffix is appended to the directory name.
Matching records with `parashari_raman_v1` provenance are upgraded to v2
without rewriting `CONTEXT.md` or chart artifacts.

After it completes, read `provenance.json` and the generated files before
answering the user's astrology question. Cite the resulting record and
provenance for every factual statement about the saved chart; use the shared
[`../../shared/process.md`](https://github.com/thaletto/ascendant/blob/main/plugins/agent/ascendant/shared/process.md) and the matching skill's
topic rubric for interpretation.
