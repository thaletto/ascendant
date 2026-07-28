# Parashari-Raman v1 rule catalogue

Version: `parashari_raman_v1`

Each rule ID below selects a house only through its sign lord's house placement
and the calculator's saved dignity label. `Exalted`, `Moola Trikona`, `Own`, or
`Friend` is **support**; `Debilitated`, `Enemy`, or a lord in house 6, 8, or 12
is **constraint**; every other result is **neutral**. The cited classical
sources are `BPHS-RS-1984` and `BVR-HTJH`, defined in
[`sources.md`](sources.md).

| Topic | D1 rule IDs | Required varga rule IDs | Dasha / transit / SAV IDs |
| --- | --- | --- | --- |
| Career | `PR-CAR-H06`, `PR-CAR-H10`, `PR-CAR-H11` | D10, same house IDs | `PR-CAR-DASHA`, `PR-CAR-TRANSIT`, `PR-CAR-SAV` |
| Education | `PR-EDU-H04`, `PR-EDU-H05`, `PR-EDU-H09` | D24, same house IDs | `PR-EDU-DASHA`, `PR-EDU-TRANSIT`, `PR-EDU-SAV` |
| Finance | `PR-FIN-H02`, `PR-FIN-H08`, `PR-FIN-H11` | D2, same house IDs | `PR-FIN-DASHA`, `PR-FIN-TRANSIT`, `PR-FIN-SAV` |
| Health | `PR-HEA-H01`, `PR-HEA-H06`, `PR-HEA-H08` | None | `PR-HEA-DASHA`, `PR-HEA-TRANSIT`, `PR-HEA-SAV` |
| Marriage | `PR-MAR-H05`, `PR-MAR-H07`, `PR-MAR-H08` | D9, same house IDs | `PR-MAR-DASHA`, `PR-MAR-TRANSIT`, `PR-MAR-SAV` |
| Property | `PR-PRO-H04`, `PR-PRO-H11`, `PR-PRO-H12` | D4, same house IDs | `PR-PRO-DASHA`, `PR-PRO-TRANSIT`, `PR-PRO-SAV` |
| Family | `PR-FAM-H03`, `PR-FAM-H04`, `PR-FAM-H05`, `PR-FAM-H09` | None | `PR-FAM-DASHA`, `PR-FAM-TRANSIT`, `PR-FAM-SAV` |
| Compatibility | `PR-REL-MOON` | `PR-REL-D9-MOON` | `PR-REL-DASHA`, `PR-REL-TRANSIT`, `PR-REL-SAV` |
| Daily transit | `PR-DAI-TRANSIT` | None | Dated factual report only |

`PR-*-DASHA` is active only when both the Mahadasha and Antardasha lords are
selected house lords. `PR-*-TRANSIT` reports the dated planets in the selected
natal houses without changing natal status. `PR-*-SAV` reports saved scores as
supplementary context without a score threshold.
