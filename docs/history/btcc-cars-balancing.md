# BTCC cars, classes and balancing, 1958 to 2026

Part of the BTCC rules history (weekend format, points and titles, cars
classes and balancing). The table image is made with
`python -I tools/history_table.py docs/history/btcc-cars-balancing.md`.

`(?)` marks a detail that the sources we read did not confirm. The
sources had almost nothing on ballast and tyres.

## Table

| Years | Car rules | Classes | Balancing | Tyres and fuel |
|---|---|---|---|---|
| 1958 to 1960 | Own BTCC rules (1958), FIA Appendix J (1959), special saloons (1960). | By engine size, racing together. | Classes only. | |
| 1961 to 1983 | FIA Group 2 (1961 to 1965, 1970 to 1973), Group 5 (1966 to 1969), Group 1 (1974 to 1983). | By engine size. | Classes only. | |
| 1983 to 1990 | FIA Group A: at least 2,500 (earlier 5,000) road cars built. | Classes by engine size (Class B, Class C). 1990: a new 2.0 L class next to the big cars. | Classes only. | |
| 1991 to 2000 | 2.0 L "Super Touring": up to 6 cylinders, no turbo, two driven wheels, at least 4.20 m, four doors from 1993. | One class. | Wings allowed from 1995. 1996: Audi wins with a 4WD car (weight penalty (?)). | 2000: Michelin only, 28 dry sets per team per season. |
| 2000 to 2003 | Super Touring (to 2000), BTC Touring (from 2001). | Plus a Production class. | 2000: success ballast 40, 30 and 20 kg for the top three of each race, at most 40 kg. | |
| 2004 to 2010 | BTC Touring and Super 2000 together. | One class, two car types. TOCA rules to equalise them. | BTC-T cars can't win the title from 2007. | |
| 2010 to 2013 | NGTC phased in: 2.0 L turbo, about 300 hp, common gearbox, brakes, electronics. A leased TOCA engine. | NGTC, plus older cars with NGTC engines. | 2011: old BTC-T cars allowed one more year with 50 kg extra. NGTC cars kept level with S2000 until 2013. Success ballast by results (?). | |
| 2014 to 2021 | NGTC only. FIA name TCN-1 from 2014. | One class. | Success ballast by championship position (?). Engines with a short over-boost. | Goodyear sole supplier (start year (?)). Hard, medium, soft and wet. A softer tyre must be used once per meeting (?). |
| 2022 to 2026 | NGTC with a hybrid unit (?). | One class. | Hybrid deployment used for balancing instead of ballast (?). | 2025: sustainable fuel for all. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Success ballast | No | B1 |
| Two car types in one class | No | C9 |
| Common parts, leased engine | Partly | level ratings by hand |
| Hybrid limited for the leaders | No | B1, B13 |
| One tyre maker | Yes | `tyre_suppliers.json` |
| Softer tyre once per meeting | No | B12 |

## Sources

- Wikipedia, "British Touring Car Championship" (regulations by era,
  NGTC, cost control, Goodyear, fuels), "Super Touring" (rules, 1995
  aero), "Group A" (homologation), "BTC Touring" (2001 to 2011, S2000
  from 2004), "Next Generation Touring Car" (spec, over-boost), 2000
  season article (ballast, tyres).
- Not confirmed, marked `(?)`: the 1996 Audi penalty, ballast after 2000,
  the hybrid and its use for balancing, the option tyre rule, Goodyear's
  start year.
- Conflict: Super Touring allowed only two driven wheels, yet Audi raced
  a 4WD car in 1996. No source explains it.

## Discord post

=== post | BTCC cars and balancing history | btcc-cars-balancing
## BTCC cars, classes and balancing, 1958 to 2026

Part three and the last of the BTCC rules history. The sources were thin on ballast and tyres, so those rows are marked (?). The table is below. What stood out to me:

- **FIA groups until 1990:** Group 2, Group 5, Group 1, Group A, always with classes by engine size.
- **The BTCC invented the 2.0 L class (1990),** which became the FIA's Super Touring. One class from 1991.
- **Two car types in one class** (BTC Touring and Super 2000, 2004 to 2010), kept level by TOCA rules. Old cars allowed one more year with 50 kg extra (2011).
- **NGTC since 2011:** a common gearbox, brakes and electronics, a leased engine, front or rear drive. Built to keep costs down.
- **Success ballast:** 40, 30 and 20 kg for the top three of each race (2000). Later ballast by points, and the hybrid is used for balancing today (both not confirmed).

For the game: car types or generations in one class with their own weights, common parts, success ballast per race or per championship position, and a hybrid boost that is limited for the leaders. It's the same balancing rule as DTM and GT3: "if X, add Y to Z".

The last table in the picture shows what the game can do today: yes, partly or no.

That's the BTCC series. Mistakes? Tell me!
