# F1 engines and grid penalties, 1950 to 2026

Part of a series on how F1 rules changed (qualifying, points, tyres, pit
stops, race format, safety car, overtaking aids, engines). Each file has
the table, the sources and a Discord post. The table image is made with
`python -I tools/history_table.py docs/history/f1-engines.md`.

`(?)` marks a detail that the sources we read did not confirm. Check it
before you rely on it.

## Table

| Years | Engine | Fuel | Engines per season and penalties | Quirks |
|---|---|---|---|---|
| 1950 to 1953 | 4.5 L, or 1.5 L with supercharger. | Free. | No limits. | 1952 and 1953 run to Formula 2 rules (2 L) because too few F1 cars exist. Indianapolis has its own rules. |
| 1954 to 1960 | 2.5 L, or 0.75 L with supercharger (to 1957). Superchargers banned from 1958. | Aviation fuel from 1958. | No limits. | |
| 1961 to 1965 | 1.5 L, no supercharger. | Pump fuel. | No limits. | Small engines, British teams with Coventry Climax win most races. |
| 1966 to 1976 | 3.0 L, or 1.5 L with supercharger. Up to 12 cylinders from 1972. Even gas turbines and rotary engines allowed. | Commercial fuel. | No limits. | Cosworth DFV from 1967: a cheap customer V8 for everyone. Ford (Cosworth) wins 176 races in total. |
| 1977 to 1985 | 3.0 L or 1.5 L turbo. Turbine, rotary, diesel and two-stroke banned in 1982. | | No limits. Turbo qualifying engines last a few laps (?). | Renault brings the turbo in 1977. By the end of 1985 everyone has one. |
| 1986 to 1988 | Turbo only in 1986. 1987: 3.5 L without turbo allowed again, turbo boost 4 bar. 1988: 2.5 bar. | Fuel tank for turbo cars cut, down to 150 L by 1988. | No limits. | Qualifying engines with about 1,400 hp (BMW 1986). McLaren-Honda 1988: 15 wins in 16 races. |
| 1989 to 1994 | 3.5 L, no turbo. | Unleaded from 1992. | No limits. | V8, V10 and V12 side by side. |
| 1995 to 1999 | 3.0 L. | | No limits. | |
| 2000 to 2005 | 3.0 L V10 only. | | 2004: one engine per race weekend. 2005: one engine for two weekends. A new engine: 10 places back. | Engines reach 19,000 rpm and more. |
| 2006 to 2013 | 2.4 L V8. Engines frozen from 2007. Rev limit 19,000 (2007), 18,000 (2009). KERS from 2009. | 5.75% bio fuel from 2008. | Two races per engine (to 2008). 8 engines per season from 2009. Extra engine: 10 places back. | 2006: Toro Rosso still allowed a slowed V10. Same engines for seven years, the cars get the difference. |
| 2014 to 2021 | 1.6 L V6 turbo hybrid. MGU-K 120 kW, MGU-H. Fuel flow at most 100 kg/h. | 100 kg per race, 110 kg from 2019. | Six parts counted separately. 5 power units in 2014, then fewer: 3 by 2018. Penalties per part, more than 15 places means the back of the grid. Development "tokens" 2015 to 2016. | Mercedes wins 8 constructors' titles in a row. McLaren-Honda 2015: grid penalties of 50 and 55 places at Spa. |
| 2022 to 2025 | Same engines, frozen from 2022. Price for a customer team capped at 15 million euro a season. | At least 10% ethanol. | 3 engines, turbos, MGU-H and MGU-K (4 from 2024), 2 batteries and electronics per driver. 2025: gearbox penalties removed. | Grid penalties make some races a back-of-grid charge. Teams take penalties at tracks where passing is easy. |
| 2026 | 1.6 L V6 turbo, no MGU-H. MGU-K 350 kW, engine 400 kW: about half electric. | 100% sustainable fuel. | Per driver: 4 engines, turbos and exhausts, 3 MGU-K, batteries and electronics. 2027 and 2028: the same (?). New makes get more. | Audi, Ford (with Red Bull), Honda and Cadillac (Ferrari engines for now). Renault leaves. |

## Gearboxes and other penalties

| Rule | Setting |
|---|---|
| Gearbox | must last several events in a row (6 from 2014), from 2022 a pool of 4 per season. Otherwise 5 places back. Removed in 2025. |
| Car can't start from its grid spot | 10 places back, or start from the pit lane |
| Work in parc fermé (chassis, suspension, bodywork) | start from the pit lane |
| Extra engine part | grid places at the first race it is used |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Engine makers, works and customers | Yes | `engines.json`, engine contracts |
| Engine formula per era | Partly | ratings and `car_profile`, no engine size rules |
| Two engine types side by side, own rules | No | B2 |
| Parts per season, grid penalties | Yes | `seasonal_component_allocation_rule`: engines and gearboxes, fixed 20 and 10 places |
| Fuel limit per race | Partly | `formula_fuel_tank` |
| Engine freeze | No | D7 |
| Hybrid power | Yes | `ers_policy` |

## Sources

- Wikipedia, "Formula One engines" (formula per era, rev limits, freezes,
  KERS, 2014 to 2026 specs, suppliers and wins), "Formula One
  regulations" (2026 and 2027 allocations, gearbox rule, 2025 change,
  parc fermé, 10-place rule), "Formula One race weekend" (part).
- Wikipedia regulation table (supercharger ban 1958, unleaded 1992 to 1994,
  150 L tank 1988). Formula1.com and formulaonehistory.com penalty guides
  (15-place rule, 2024 allocation raised from 3 to 4). Crash.net, 2025
  rule changes (gearbox limits removed). Autosport (gearbox: 6 events to
  2021, pool of 4 from 2022). RacingNews365, July 2026 (extra part kept
  for 2027 and 2028).
- Not confirmed, marked `(?)`: qualifying engines, the 2027 and 2028
  allocation.
- Open conflicts: rev limits per year. 2027 allocation: Wikipedia and an
  older F1.com guide say 3 and 2, a later FIA decision (RacingNews365)
  keeps 4 and 3.

## Discord post

=== post | F1 engines history | f1-engines
## F1 engines and grid penalties, 1950 to 2026

Part eight of the rules history. The table is below. What stood out to me:

- **The engine formula changed about every 5 to 10 years:** 4.5 L, 2.5 L, 1.5 L, 3.0 L, turbo, 3.5 L, V10, V8, V6 hybrid, and now about half electric.
- **Two engine kinds side by side** for long stretches: with or without supercharger or turbo, each with its own size. In 1952 and 1953 the races even ran to Formula 2 rules.
- **No limit on engines until the 2000s.** Then one engine per weekend, then for two weekends, 8 per season, and since 2014 each part counted on its own.
- **Grid penalties** for every extra part, the gearbox (until 2024) and work in parc fermé.
- **Freezes and price caps:** 2007 and 2022 engine freezes, 15 million euro a season for a customer team.

For the game this is: engine rules per era (size, turbo yes or no, two classes side by side), a fuel limit per race, how many of each part a driver gets per season, and the grid penalty for an extra one. The same settings cover DTM: the 1990s engines per make with their own weight, and the engine freeze and homologation in 2012 and 2013.

The last table in the picture shows what the game can do today: yes, partly or no.

Next up: anything you'd like to see? Mistakes? Tell me!
