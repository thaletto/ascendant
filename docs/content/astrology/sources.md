---
title: Sources and Scope
description: Primary texts, calculation references, and implementation sources for the astrology learning guide.
---

The learning pages separate three kinds of evidence:

1. **Calculation references** define coordinate and house algorithms.
2. **Primary astrological texts** document a tradition's rules.
3. **Ascendant source files** define what this software actually implements.

Astrological texts are sources for the traditions described; citing them does
not establish scientific validation of astrological prediction.

## Calculation references

- Astrodienst, [Swiss Ephemeris documentation](https://www.astro.com/swisseph/swisseph.htm).
  Used for tropical and sidereal coordinates, ayanamsa, precession, fixed-star
  calculations, and house-system geometry.
- Astrodienst, [Swiss Ephemeris programming interface](https://www.astro.com/swisseph-download/doc/swephprg.2.10.htm).
  Used for named sidereal modes, house codes, and API-level calculation
  behavior.

## Parashari and house judgment

- Maharishi Parashara, *Brihat Parashara Hora Shastra*, translated by
  R. Santhanam, Ranjan Publications, 1984, Volumes I and II. The packaged
  catalogue uses its bhava, lord, varga, Vimshottari, and Ashtakavarga
  material as its classical basis.
- *Brihat Parashara Hora Shastra* Sanskrit source sections:
  [grahas and foundations](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par0110.html),
  [houses](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par1120.html),
  and [dashas](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par4650.html).
- B. V. Raman, *How to Judge a Horoscope*, Volumes I and II, Motilal
  Banarsidass. Used for the disciplined house-by-house judgment structure.

The public docs paraphrase concepts and do not reproduce book passages.

## Western astrology

- Claudius Ptolemy, *Tetrabiblos*, translated by F. E. Robbins in the Loeb
  Classical Library. A
  [public transcription](https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Ptolemy/Tetrabiblos/home.html)
  is used as a primary historical reference for classical planets, signs,
  aspects, and judgments.
- Swiss Ephemeris documentation is used for current astronomical coordinates,
  fixed stars, and house calculations. The historical source documents a
  tradition; the ephemeris documents computation.

## Jaimini

- Jaimini, [*Sri Jaiminisutras*, translated and edited by B. Suryanarain
  Rao](https://books.google.com/books/about/Sri_Jaiminisutras.html?id=z4v4gjJ_ay0C),
  Raman Publications, 3rd edition, 1949.
- B. V. Raman, [*Studies in Jaimini Astrology*](https://books.google.com/books/about/Studies_in_Jaimini_Astrology.html?id=gW2DIFHrxfgC),
  Motilal Banarsidass. Used as a modern methodological study.

The Jaimini page flags variant-sensitive calculations instead of presenting one
lineage's choice as universal.

## Krishnamurti Paddhati

- K. S. Krishnamurti,
  [*Krishnamurti Padhdhati (Predictive Stellar Astrology)*](https://books.google.com/books/about/Krishnamurti_Padhdhati_predictive_Stella.html?id=lJ5WAAAAMAAJ),
  1971. Primary-author reference for cusps, significators, ruling planets,
  star lords, sub-lords, and timing.
- K. S. Krishnamurti,
  [*Horary Astrology: Krishnamurti Padhdhati*](https://books.google.com/books/about/Horary_Astrology.html?id=Wt9BAQAAIAAJ),
  primary-author reference for the horary workflow.
- Swiss Ephemeris documentation for the Krishnamurti ayanamsa modes and
  Placidus house calculation.

The KP page distinguishes these system rules from the mere selection of a
Krishnamurti ayanamsa.

## Ascendant implementation references

- [`ascendant/configuration.py`](https://github.com/thaletto/ascendant/blob/main/ascendant/configuration.py)
  defines supported ayanamsas, house systems, and immutable defaults.
- [`ascendant/types.py`](https://github.com/thaletto/ascendant/blob/main/ascendant/types.py)
  defines chart, planet, nakshatra, dasha, and division types.
- Each specialist skill directory (for example `skills/career/`) ships the
  whole reading contract under its own `references/`: a judgement
  `process.md`, the `hierarchy.md` evidence layers and factor ranks,
  `artifacts.md` saved-evidence contract, `sources.md` citation locators, and
  the topic-specific `topic.md` rubric. Skills carry these copies so a
  skills.sh install of one skill folder always includes its knowledge.

When a learning page and the current source code differ about supported output,
the checked-out source and released package version are authoritative for that
software version.
