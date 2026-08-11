---
title: Jaimini core
description: Calculate Ascendant's named seven-karaka Jaimini structures from D1 and D9.
---

## Calculate the named core

```python
from ascendant import Ascendant

astro = Ascendant(
    year=1990,
    month=1,
    day=1,
    hour=12,
    minute=0,
    second=0,
    latitude=28.6139,
    longitude=77.2090,
    utc="+5:30",
)

jaimini = astro.get_jaimini()
```

The result identifies its method as `jaimini_srao_7_core_v1` and contains:

- seven degree-ordered Chara Karaka assignments,
- the Rashi Drishti map,
- the Atmakaraka's Karakamsha sign,
- all twelve Arudha Padas and Upapada,
- and raw Argala support and obstruction for every sign, with the secondary
  fifth/ninth pair kept distinct and Ketu calculated separately in reverse.

The calculation reuses D1 and D9 data from the existing birth ephemeris. It
does not make another Swiss Ephemeris call and does not interpret the result.

## Declared boundaries

The method ranks Sun through Saturn. Rahu is outside the normal seven roles and
appears only as Rao's recorded fallback for an exact shared-degree vacancy.
Rashi Drishti is sign-to-sign; no Western aspect orb is applied. Arudha uses
Rao's literal equal-distance projection. Chara Dasha is not part of this result.

Saved person records persist the same structure in `jaimini.json`, with the
method name repeated in schema-2 provenance.
