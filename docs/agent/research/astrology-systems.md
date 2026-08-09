# Astrology systems research for public documentation

Research date: 2026-07-28

## Purpose and source discipline

This note separates three kinds of material that the public documentation
should not blur together:

1. Astronomical and computational facts, sourced to Swiss Ephemeris or the
   Ascendant implementation.
2. Teachings within an astrological tradition, attributed to a primary text or
   named school rather than stated as astronomical fact.
3. Ascendant product behavior, sourced to the current repository rather than
   inferred from the traditions.

Swiss Ephemeris documents coordinate frames, precession, planetary and
fixed-star positions, ayanamshas, and house calculations; it is not a source
for validating astrological interpretation. The classical and modern
astrological books below document what their traditions teach; they should not
be cited as scientific validation of those teachings.
([Swiss Ephemeris general documentation](https://www.astro.com/swisseph/swisseph.htm),
[BPHS chapters 1–10](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par0110.html),
[Jaimini Sutras, Rao edition](https://books.google.com/books/about/Sri_Jaiminisutras.html?id=z4v4gjJ_ay0C),
[Krishnamurti Padhdhati](https://books.google.com/books/about/Krishnamurti_Padhdhati_predictive_Stella.html?id=lJ5WAAAAMAAJ))

## Recommended documentation structure

The public documentation should use this hierarchy:

- **Introduction:** say plainly what Ascendant calculates and disclose the
  system used by its packaged reading skills.
- **Configuration:** a separate page for ayanamsha, house-system selection,
  precedence, supported values, and reproducibility.
- **Astrology foundations:** an overview page that introduces zodiac, planets
  or grahas, stars and nakshatras, houses, aspects, divisional charts, timing,
  and transits, then links to focused pages.
- **Tropical and sidereal zodiacs:** coordinate-frame choice, precession,
  ayanamsha, and why changing ayanamsha can change a sidereal longitude.
- **Planets, nodes, and fixed stars:** separate the calculated celestial object
  from the symbolic meaning assigned by a tradition.
- **Signs, stars, and nakshatras:** distinguish equal zodiac signs, individual
  fixed stars, and the 27 lunar-mansion intervals used by Ascendant.
- **Houses:** separate house topics from house-division geometry and explain
  Whole Sign, Equal, Placidus, and Porphyry.
- **Dashas and timing:** introduce dashas as a family of period systems, then
  document Ascendant's Vimshottari implementation specifically.
- **Schools of interpretation:** separate pages for Parāśari, Jaimini, and KP,
  with an explicit "supported by Ascendant" box on each page.

The introduction should not imply that Ascendant implements every system
covered educationally. The repository currently supports a sidereal
calculation layer with several ayanamshas and house-system codes, while the
packaged judgement skills use one curated `parashari_raman_v2` hierarchy.
([configuration defaults and supported values](../../../ascendant/configuration.py#L10-L29),
[Swiss Ephemeris mappings](../../../ascendant/horoscope.py#L18-L34),
[career skill](../../../plugins/agent/ascendant/skills/career/SKILL.md))

## Tropical and sidereal astrology

The tropical zodiac fixes 0° Aries to the vernal point, whereas a sidereal
zodiac fixes its origin relative to a stellar reference. Because Earth's
equinoctial point precesses relative to distant objects, the two frames drift
apart over time.
([Swiss Ephemeris, section 2.8.1](https://www.astro.com/swisseph-download/doc/swisseph.pdf#page=30),
[NASA Goddard on precession](https://earth.gsfc.nasa.gov/geo/multimedia/nutation-and-precession))

An ayanamsha is the angular offset used to convert a tropical longitude to a
chosen sidereal longitude; Swiss Ephemeris expresses the common computation as
`sidereal_position = tropical_position - ayanamsha(t)`. Sidereal schools do not
all choose the same zero point, so "sidereal" alone is incomplete calculation
provenance.
([Swiss Ephemeris, section 2.8.1](https://www.astro.com/swisseph-download/doc/swisseph.pdf#page=30),
[Swiss Ephemeris programming guide, sidereal modes](https://www.astro.com/swisseph/swephprg.pdf#page=53))

Ascendant is a sidereal calculator: its ephemeris adapter always applies the
Swiss Ephemeris sidereal flag and sets a selected sidereal mode before
calculating the chart. Its public defaults are Lahiri ayanamsha and Whole Sign
houses.
([sidereal calculation flags and chart builder](../../../ascendant/ephemeris.py#L13-L15),
[sidereal calculation call](../../../ascendant/ephemeris.py#L120-L150),
[public defaults](../../../ascendant/configuration.py#L53-L68))

Ascendant currently exposes Lahiri, Lahiri 1940, Lahiri VP285, Lahiri ICRC,
Raman, Krishnamurti, and Krishnamurti-Senthilathiban ayanamshas, all mapped to
Swiss Ephemeris modes. Supporting a Krishnamurti ayanamsha is a coordinate
option; it does not by itself mean that the reading engine implements
Krishnamurti Paddhati judgement.
([supported ayanamshas](../../../ascendant/configuration.py#L10-L19),
[Swiss Ephemeris mode mapping](../../../ascendant/horoscope.py#L18-L26),
[packaged hierarchy in each skill](../../../plugins/agent/ascendant/skills/career/references/hierarchy.md))

### Suggested public wording

> Ascendant calculates sidereal charts. It uses Lahiri ayanamsha and Whole Sign
> houses by default, and lets you choose another supported ayanamsha or house
> system. Ayanamsha chooses the reference for sidereal longitude; the house
> system chooses how the chart is divided into houses.

## Planets, nodes, fixed stars, and nakshatras

Classical Western astrology treats the Sun, Moon, Mercury, Venus, Mars,
Jupiter, and Saturn as the central wandering lights and also assigns
interpretive qualities to individual fixed stars. Ptolemy's *Tetrabiblos*
contains separate sections on the powers of the planets and the powers of the
fixed stars, so a foundations page should teach those as related but distinct
categories within that tradition.
([Ptolemy, *Tetrabiblos*, Book I](https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Ptolemy/Tetrabiblos/1B%2A.html),
[public-domain Robbins edition](https://commons.wikimedia.org/wiki/File:Loeb_435_-_Ptolemy_-_Tetrabiblos_by_Robbins_(1940).pdf))

The Parāśari source tradition describes nine grahas: Sun, Moon, Mars, Mercury,
Jupiter, Venus, Saturn, Rahu, and Ketu. Public prose should retain the word
**graha** or explain that this is an astrological category, because Rahu and
Ketu are lunar nodes rather than physical planets.
([BPHS chapters 1–10](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par0110.html),
[Ascendant's object and node construction](../../../ascendant/ephemeris.py#L20-L29),
[south-node derivation](../../../ascendant/ephemeris.py#L153-L182))

Fixed stars are individually identified stellar objects whose positions can be
computed with dedicated Swiss Ephemeris fixed-star functions. A nakshatra in
Ascendant is instead one of 27 named longitude intervals, divided into four
padas and assigned a planetary lord; the current chart builder derives this
metadata arithmetically from ecliptic longitude rather than calculating the
position of a named fixed star.
([Swiss Ephemeris programming guide, fixed-star functions](https://www.astro.com/swisseph/swephprg.pdf),
[Ascendant's 27-name list](../../../ascendant/const.py#L24-L52),
[longitude metadata calculation](../../../ascendant/horoscope.py#L117-L152))

Ascendant's standard chart object set is the Sun, Moon, Mercury, Venus, Mars,
Jupiter, Saturn, and the mean north node, with the south node derived 180°
opposite. The current chart builder does not call a Swiss Ephemeris fixed-star
function, so public docs may teach fixed stars but must mark fixed-star
calculation as unsupported.
([calculated object list](../../../ascendant/ephemeris.py#L20-L29),
[object calculation and south node](../../../ascendant/ephemeris.py#L153-L182))

Each returned planet and lagna record includes sign, sign lord, nakshatra,
nakshatra lord, and pada metadata. The internal longitude helper also computes
KP-style sub-lord and sub-sub-lord values, although those two fields are not
currently copied into the ordinary public `PlanetType` record.
([planet output construction](../../../ascendant/chart/__init__.py#L59-L91),
[lagna output construction](../../../ascendant/chart/__init__.py#L109-L132),
[KP metadata fields and calculation](../../../ascendant/horoscope.py#L37-L45),
[KP metadata result](../../../ascendant/horoscope.py#L133-L152))

## Houses

A zodiac frame and a house system answer different questions: the zodiac frame
sets celestial longitude, while a house system divides the local chart using
the ascendant, horizon, meridian, ecliptic, or time arcs according to that
system's geometry. Swiss Ephemeris documents those as separate calculation
surfaces.
([Swiss Ephemeris, sidereal zodiac](https://www.astro.com/swisseph-download/doc/swisseph.pdf#page=30),
[Swiss Ephemeris, house systems](https://www.astro.com/swisseph-download/doc/swisseph.pdf#page=56))

Whole Sign begins the first house at the start of the rising sign and gives
each house one complete sign. Equal House creates twelve 30° houses from the
ascendant. Porphyry trisects each ecliptic quadrant. Placidus defines
intermediate cusps through divisions of semidiurnal and seminocturnal arcs.
([Swiss Ephemeris, sections 6.2.1 and 6.2.5](https://www.astro.com/swisseph-download/doc/swisseph.pdf#page=56),
[Swiss Ephemeris, section 6.2.6](https://www.astro.com/swisseph-download/doc/swisseph.pdf#page=57))

Within the Parāśari text, the twelve bhavas are assigned different life
subjects, and later chapters elaborate results for individual houses. Public
documentation should attribute those meanings to the tradition, avoid
presenting one English gloss as exhaustive, and keep house meaning separate
from the geometry used to calculate a cusp.
([BPHS chapters 11–20](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par1120.html),
[Raman, *How to Judge a Horoscope*, Volume II](https://books.google.com/books/about/How_to_Judge_a_Horoscope.html?id=wqC1Ea88fTcC))

Ascendant exposes Whole Sign, Placidus, Equal, Equal 2, and Porphyry codes and
passes the selected code into `swe.houses_ex`. However,
`Chart.get_rasi_chart()` currently assigns one complete sign to each numbered
house starting from the lagna sign. Before public docs claim that every
configured house system changes planet-to-house membership in `get_chart()`,
that behavior should be verified with focused public-API tests and either
documented precisely or corrected.
([house-system values](../../../ascendant/configuration.py#L22-L29),
[Swiss Ephemeris code mapping](../../../ascendant/horoscope.py#L28-L34),
[house calculation call](../../../ascendant/ephemeris.py#L185-L205),
[D1 house construction](../../../ascendant/chart/__init__.py#L135-L155))

## Dashas

The Parāśari source describes multiple dasha systems rather than one universal
timing method. Its dasha section gives Vimshottari a 120-year framework tied to
the birth nakshatra and also discusses other systems and conditions of use.
([BPHS chapters 46–50](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par4650.html),
[Santhanam edition bibliographic record](https://books.google.com/books/about/Brihat_Parasara_hora_sastra_of_Maharshi.html?id=eb1-AAAAMAAJ))

Ascendant implements Vimshottari Mahadasha and Antardasha. Its sequence is
Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, and Mercury, with durations
7, 20, 6, 10, 7, 18, 16, 19, and 17 years; those values sum to 120.
([sequence and durations](../../../ascendant/const.py#L54-L66),
[timeline construction](../../../ascendant/dasha/__init__.py#L89-L138))

Ascendant chooses the starting period from the Moon's nakshatra lord and
computes the unelapsed balance from the Moon's progress through its nakshatra.
The public docs should therefore explain that exact implementation rather than
describing "dasha" as though all dasha systems work identically.
([Vimshottari starting lord and balance](../../../ascendant/dasha/__init__.py#L89-L110),
[BPHS chapters 46–50](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par4650.html))

## Parāśari system

The *Bṛhat Parāśara Horā Śāstra* source corpus covers grahas, signs, bhavas,
vargas, dashas, yogas, and Ashtakavarga. Manuscript history and translation
choices are complex, so public docs should say "the Parāśari tradition" or
"BPHS describes" and cite the edition used rather than imply one uncontested
modern rulebook.
([BPHS chapters 1–10](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par0110.html),
[BPHS chapters 11–20](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par1120.html),
[BPHS chapters 46–50](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par4650.html),
[Santhanam edition bibliographic record](https://books.google.com/books/about/Brihat_Parasara_hora_sastra_of_Maharshi.html?id=eb1-AAAAMAAJ))

Ascendant's packaged reading system is narrower than the full source corpus.
It calls itself `parashari_raman_v2` and combines exact BPHS locators with
Ascendant's developer-authored methodology. Every specialist skill carries its
own copy of the source register under
`references/sources.md`.
([packaged source register](../../../plugins/agent/ascendant/skills/career/references/sources.md),
[career skill](../../../plugins/agent/ascendant/skills/career/SKILL.md))

The hierarchy orders evidence as natal promise, relevant varga,
Vimshottari activation, transit trigger, and SAV corroboration. Within each
layer, topic factors are primary, corroborating, modifying, or background.
Higher factors control; lower factors do not win by accumulation; equal-rank
conflicts remain mixed without a developer-authored tie-breaker.
([hierarchy, copied into each skill](../../../plugins/agent/ascendant/skills/career/references/hierarchy.md))

The topic rules use D1 plus a selected varga where required: D10 for career,
D24 for education, D2 for finance, D9 for marriage and compatibility, and D4
for property. Health, family, and daily-transit rules do not require a varga.
([career rubric](../../../plugins/agent/ascendant/skills/career/references/topic.md))

The agent reads saved artifacts directly and applies those rubrics. Python
tools may create person records or dated transit data, but they do not evaluate
interpretive logic. Transits remain dated triggers and SAV remains the lightest
corroborating layer.
([saved evidence contract](../../../plugins/agent/ascendant/skills/career/references/artifacts.md),
[hierarchy, copied into each skill](../../../plugins/agent/ascendant/skills/career/references/hierarchy.md))

The specialist career, education, finance, health, marriage, property, family,
daily-transit, and relationship-compatibility skills are self-contained: each
carries its own `process.md`, `hierarchy.md`, `artifacts.md`, and `sources.md`
under `references/` plus its topic-specific `references/topic.md` rubric, so a
skills.sh install of one skill folder always includes its knowledge. No skill
depends on another skill. The process requires exact saved records,
claim-level evidence and method citations, qualitative confidence, partial
readings for partial data, and natural question-focused prose.
([process, copied into each skill](../../../plugins/agent/ascendant/skills/career/references/process.md),
[career skill](../../../plugins/agent/ascendant/skills/career/SKILL.md))

### Suggested introduction disclosure

> Ascendant's agent reading skills use a curated Parāśari–Raman hierarchy.
> They read saved sidereal charts directly, apply developer-owned topic
> weights, use Vimshottari for activation, and treat transits and
> Sarvashtakavarga as supporting context. The agent explains that evidence in
> natural prose with claim-level citations. The educational guides also
> introduce Western, Jaimini, and KP approaches, but those are not
> interchangeable with the reading rules used by the skills.

This wording is supported by the packaged workflow and its versioned hierarchy.
([skill declaration](../../../plugins/agent/ascendant/skills/career/SKILL.md),
[source register](../../../plugins/agent/ascendant/skills/career/references/sources.md),
[specialist rubric](../../../plugins/agent/ascendant/skills/career/references/topic.md))

## Jaimini

The *Jaimini Sutras* tradition uses a vocabulary and rule architecture that
should be taught separately from the packaged Parāśari rules. The
Suryanarain Rao edition contains concepts including Atmakaraka, Karakamsha,
Arudha or Pada Lagna, Argala, sign-based aspects, and multiple sign dashas.
([Jaimini, *Sri Jaiminisutras*, Rao edition](https://books.google.com/books/about/Sri_Jaiminisutras.html?id=z4v4gjJ_ay0C),
[B. V. Raman, *Studies in Jaimini Astrology*](https://books.google.com/books/about/Studies_in_Jaimini_Astrology.html?id=gW2DIFHrxfgC))

No Jaimini judgement path, Jaimini rule catalogue, or Jaimini-specific public
API appears in the inspected packaged skills. Jaimini should therefore be an
educational page marked **not implemented by Ascendant's reading skills**, not
described as part of `parashari_raman_v2`.
([packaged hierarchy in each skill](../../../plugins/agent/ascendant/skills/career/references/hierarchy.md),
[specialist rubric](../../../plugins/agent/ascendant/skills/career/references/topic.md))

## Krishnamurti Paddhati (KP)

K. S. Krishnamurti's own *Krishnamurti Padhdhati (Predictive Stellar
Astrology)* is the primary source for presenting KP as a modern stellar
predictive system using cusps, significators, ruling planets, constellation or
star lords, sub-lords, dashas, and bhuktis. Exact algorithms should be checked
against the relevant KP Reader and edition rather than copied from later
summary websites.
([K. S. Krishnamurti, *Krishnamurti Padhdhati*](https://books.google.com/books/about/Krishnamurti_Padhdhati_predictive_Stella.html?id=lJ5WAAAAMAAJ),
[K. S. Krishnamurti, *Horary Astrology: Krishnamurti Padhdhati*](https://books.google.com/books/about/Horary_Astrology.html?id=Wt9BAQAAIAAJ))

Ascendant exposes two Krishnamurti ayanamsha choices and calculates
nakshatra-lord, sub-lord, and sub-sub-lord longitude metadata. Those are KP
calculation ingredients, but the packaged hierarchy defines neither cuspal
sub-lord judgment nor a KP significator or ruling-planet procedure.
([Krishnamurti ayanamsha values](../../../ascendant/configuration.py#L10-L19),
[KP longitude metadata](../../../ascendant/horoscope.py#L37-L45),
[sub-lord calculation](../../../ascendant/horoscope.py#L117-L152),
[packaged topic scope](../../../plugins/agent/ascendant/skills/career/references/topic.md))

The KP page should consequently use three explicit labels:

- **Explained:** KP's historical vocabulary and conceptual workflow, sourced
  to K. S. Krishnamurti.
- **Calculated:** supported Krishnamurti ayanamshas and internal
  nakshatra/sub-lord metadata.
- **Not yet judged:** full KP cuspal significator, ruling-planet, horary, and
  event-prediction procedures.

Those labels match the current split between the coordinate and metadata code
and the Parāśari-only judgement hierarchy.
([calculation support](../../../ascendant/horoscope.py#L18-L45),
[career hierarchy](../../../plugins/agent/ascendant/skills/career/references/hierarchy.md))

## Implementation disclosure matrix

| Topic | Teach in public docs | Calculated by the Python library | Used by packaged judgement skills |
| --- | --- | --- | --- |
| Tropical zodiac | Yes, for comparison | No public tropical chart mode | No |
| Sidereal zodiac and ayanamsha | Yes | Yes | Yes, through saved provenance and sidereal charts |
| Seven classical planets | Yes | Yes | Yes |
| Rahu and Ketu | Yes, explicitly as nodes/grahas | Yes | Yes |
| Individual fixed stars | Yes | Not by the current chart builder | No |
| 27 nakshatras and four padas | Yes | Yes | Indirectly through charts and Vimshottari |
| House systems | Yes | Codes and Swiss house cusps exist; public chart membership needs verification | Rules consume saved numbered houses |
| Vimshottari Mahadasha/Antardasha | Yes | Yes | Yes |
| Other dasha systems | Yes, as context | No | No |
| Parāśari | Yes | Supporting chart data is calculated | Yes, curated `parashari_raman_v2` |
| Jaimini | Yes | No dedicated API found | No |
| KP | Yes | Krishnamurti ayanamshas and KP-style longitude metadata only | No full KP judgement |

Every implementation entry in this matrix is grounded in the current
configuration, ephemeris, chart, dasha, and packaged-rule sources.
([configuration](../../../ascendant/configuration.py#L10-L29),
[ephemeris objects](../../../ascendant/ephemeris.py#L20-L29),
[chart metadata](../../../ascendant/chart/__init__.py#L59-L91),
[Vimshottari implementation](../../../ascendant/dasha/__init__.py#L89-L138),
[packaged hierarchy in each skill](../../../plugins/agent/ascendant/skills/career/references/hierarchy.md))

## Primary and high-trust bibliography

- Astrodienst, [*Swiss Ephemeris General
  Documentation*](https://www.astro.com/swisseph/swisseph.htm).
- Astrodienst, [*Swiss Ephemeris Programming
  Interface*](https://www.astro.com/ftp/swisseph/doc/swephprg.htm).
- NASA Goddard Space Flight Center, [*Nutation and
  Precession*](https://earth.gsfc.nasa.gov/geo/multimedia/nutation-and-precession).
- Ptolemy, [*Tetrabiblos*, Book
  I](https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Ptolemy/Tetrabiblos/1B%2A.html),
  translated by F. E. Robbins.
- *Bṛhat Parāśara Horā Śāstra*, [chapters
  1–10](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par0110.html),
  [chapters
  11–20](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par1120.html),
  and [chapters
  46–50](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par4650.html),
  Sanskrit Documents.
- Parāśara, [*Brihat Parasara Hora Sastra*, R. Santhanam
  edition](https://books.google.com/books/about/Brihat_Parasara_hora_sastra_of_Maharshi.html?id=eb1-AAAAMAAJ),
  Ranjan Publications.
- Jaimini, [*Sri Jaiminisutras*, B. Suryanarain Rao
  edition](https://books.google.com/books/about/Sri_Jaiminisutras.html?id=z4v4gjJ_ay0C),
  Raman Publications, 1949.
- B. V. Raman, [*Studies in Jaimini
  Astrology*](https://books.google.com/books/about/Studies_in_Jaimini_Astrology.html?id=gW2DIFHrxfgC),
  Motilal Banarsidass.
- K. S. Krishnamurti, [*Krishnamurti Padhdhati (Predictive Stellar
  Astrology)*](https://books.google.com/books/about/Krishnamurti_Padhdhati_predictive_Stella.html?id=lJ5WAAAAMAAJ),
  1971.
- K. S. Krishnamurti, [*Horary Astrology: Krishnamurti
  Padhdhati*](https://books.google.com/books/about/Horary_Astrology.html?id=Wt9BAQAAIAAJ).
