---
name: init-person
description: Save a person's birth details and prepare the charts and timing information used by the astrology skills.
license: MIT
---

# Save birth details

Use this skill when the user provides a name, birth date and time with timezone, latitude, and longitude.

From the user's project directory, run the bundled script using its installed skill path. If Ascendant is not installed, install the package first with `python3 -m pip install astro-ascendant`.

```bash
python3 <path-to-init-person-skill>/scripts/init-person.py \
  --name "<name>" \
  --dob "<YYYY-MM-DDTHH:MM:SS+HH:MM>" \
  --latitude <latitude> \
  --longitude <longitude>
```

The command creates `persons/<name>/`, saves the original details, and prepares the charts and planetary periods used by later readings. Running it again with the same details should reuse the existing record.

After it completes, read the generated files before answering the user's astrology question.
