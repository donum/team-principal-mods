# BTCC cars, classes and balancing, 1958 to 2026

Part of the BTCC rules history (weekend format, points and titles, cars
classes and balancing). The table image is made with
`python -I tools/history_table.py docs/history/btcc-cars-balancing.md`.

`(?)` marks a detail that the sources we read did not confirm. The
sources had little on ballast between 2003 and 2013.

## Table

| Years | Car rules | Classes | Balancing | Tyres and fuel |
|---|---|---|---|---|
| 1958 to 1960 | Own BTCC rules (1958), FIA Appendix J (1959), special saloons (1960). | By engine size, racing together. | Classes only. | |
| 1961 to 1983 | FIA Group 2 (1961 to 1965, 1970 to 1973), Group 5 (1966 to 1969), Group 1 (1974 to 1983). | By engine size. | Classes only. | |
| 1983 to 1990 | FIA Group A: at least 5,000 road cars built in a year. | Classes by engine size (Class B, Class C). 1990: a new 2.0 L class next to the big cars. | Classes only. | |
| 1991 to 2000 | 2.0 L "Super Touring": up to 6 cylinders, no turbo, at least 4.20 m, four doors from 1993. 4WD banned from 1998. | One class. | Wings allowed from 1995. 1996: Audi wins with a 4WD car. Its minimum weight is 65 kg above front-drive cars, 95 kg from May 1996. | 2000: Michelin only, 28 dry sets per team per season. |
| 2000 to 2003 | Super Touring (to 2000), BTC Touring (from 2001). | Plus a Production class. | Success ballast from 2000: 40, 30 and 20 kg for the top three of each race, at most 40 kg. 2001: at most 60 kg. 2002: 42 kg for a win down to 9 kg for 4th, cars from 6th down lose weight. | |
| 2004 to 2010 | BTC Touring and Super 2000 together. | One class, two car types. TOCA rules to equalise them. | Success ballast as before. From 2005 for the top five, by championship position (race 1) and race results (races 2 and 3). BTC-T cars can't win the title from 2007. | |
| 2011 to 2013 | NGTC phased in: 2.0 L turbo, about 300 hp, common gearbox, brakes, electronics. A leased TOCA engine. | NGTC, plus older cars with NGTC engines. | 2011: old BTC-T cars allowed one more year with 50 kg extra. NGTC cars kept level with S2000 until 2013. Success ballast as before. | 2013: a soft option tyre, used in one race per meeting. |
| 2014 to 2021 | NGTC only. FIA name TCN-1 (endorsed December 2014). | One class. | Success ballast by championship position and results: at most 45 kg in 2014, 75 kg for the top ten from 2015 (54 kg in 2019, 60 kg in 2020, 75 kg again in 2021). Boost set race by race to 2014, then once per season. Engines with a short over-boost. | Dunlop to 2019, Goodyear from 2020. Hard, medium, soft and wet. The option tyre is used in one race per meeting. |
| 2022 to 2024 | NGTC with a Cosworth hybrid unit. | One class. | Success ballast dropped. Hybrid boost limited by championship position. | Goodyear. |
| 2025 to 2026 | NGTC, hybrid removed, 55 kg lighter. | One class. | The same boost from the turbo, limited by championship position ("TOCA Turbo Boost"). | 2025: 100% sustainable fuel for all. |

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
- Fact check: Motorsport Magazine 1996 and 1990sbtcc.com (Audi penalty,
  4WD banned 1998), Autosport and Motorsport Magazine (ballast up to 75
  kg dropped for the 2022 hybrid), Autocar, Autosport and RACER (hybrid
  ended after 2024, turbo boost since 2025), Autosport 2013 and 2016
  (option tyre), Autosport and Tyrepress 2019 (Dunlop 2003 to 2019,
  Goodyear from 2020), main article (NGTC from 2011).
- Open items check: 1990sbtcc.com regulations page (minimum weights:
  front drive 975 kg, 4WD 1,040 kg, raised to 1,070 kg in May 1996) and the
  1996 season article (penalty added during the season); so both 65 kg and
  95 kg are right, at different times. Motorsport Magazine and The
  Checkered Flag 2017 (ballast since 2004, 75 kg scale in 2017), Crash.net
  2005 (championship and race ballast, top five), 2006 season article
  (ballast for late entries), Autosport and motorsport.com 2019 (54 kg
  maximum), Autosport 2021 (maximum raised from 60 to 75 kg for 2021),
  btcc.net and TouringCars.net December 2014 and "Next Generation Touring
  Car" (FIA TCN-1).
- Confirmation round: 2000 season article, 1990sbtcc.com 2000 season page
  and Autosport 2000 ("Thompson's rivals weighed down": ballast new for
  2000), Autosport and totalmotorsport 2001 (60 kg maximum, podium only
  from May 2001), Autosport 30 March 2002 ("Ballast system overhauled":
  42 kg down to minus 24 kg), Touring Car Times October 2014 (45 kg
  maximum before 2015, race-by-race boost dropped), Touring Car Times 2015
  (75 kg scale for the top ten), motorsport.com and Autosport 2018 (54 kg
  for 2019), btcc.net and Autosport 2020 (75 kg again for 2021), Autosport
  and Touring Car Times 2010 (BTC-T 50 kg for 2011), Autosport and
  Touring Car Times 2012 (option tyre for 2013), Goodwood and btcc.net
  2024 (hybrid dropped, 55 kg, sustainable fuel).
- Not found: the kg values from 2003 to 2013. The Super Touring article
  says only two driven wheels; that describes the rule after the 1998 ban.

## Discord post

=== post | BTCC cars and balancing history | btcc-cars-balancing
## BTCC cars, classes and balancing, 1958 to 2026

Part three and the last of the BTCC rules history. The table is below. What stood out to me:

- **FIA groups until 1990:** Group 2, Group 5, Group 1, Group A, always with classes by engine size.
- **The BTCC invented the 2.0 L class (1990),** which became the FIA's Super Touring. One class from 1991.
- **Two car types in one class** (BTC Touring and Super 2000, 2004 to 2010), kept level by TOCA rules. Old cars allowed one more year with 50 kg extra (2011).
- **NGTC since 2011:** a common gearbox, brakes and electronics, a leased engine, front or rear drive. Built to keep costs down.
- **Success ballast since 2000:** 40, 30 and 20 kg for the top three of each race at first, later up to 75 kg by championship position. From 2022 a hybrid boost limited for the leaders replaced it, and since 2025 a turbo boost does the same.

For the game: car types or generations in one class with their own weights, common parts, success ballast per race or per championship position, and a boost that is limited for the leaders. It's the same balancing rule as DTM and GT3: "if X, add Y to Z".

The last table in the picture shows what the game can do today: yes, partly or no.

That's the BTCC series. Mistakes? Tell me!
