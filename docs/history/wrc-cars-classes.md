# WRC cars, classes and tyres, 1973 to 2026

Part of the WRC rules history (cars and classes, event format and points).
The table image is made with
`python -I tools/history_table.py docs/history/wrc-cars-classes.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Top cars | Engine and weight | Tyres | Quirks |
|---|---|---|---|---|
| 1973 to 1981 | Groups 1 to 4: Alpine A110, Lancia Stratos, Fiat 131 Abarth, Ford Escort, Talbot Sunbeam Lotus. | Not stated (?). | Not stated (?). | Four-wheel drive allowed from 1979. Drivers' title from 1979. |
| 1982 to 1986 | Group B: 200 road cars needed, few limits. Audi Quattro, Lancia 037, Peugeot 205 T16, Lancia Delta S4. | Weight by engine size, from 580 kg (1,000 cc) to 1,300 kg, turbo engines count 1.4 times. No boost limit, over 500 hp by 1986. | Width by engine size. | 1986: spectators killed in Portugal, Toivonen and Cresto killed in Corsica. Group B banned from 1987. |
| 1987 to 1996 | Group A: Lancia Delta wins six makes' titles in a row, then Toyota, Subaru, Mitsubishi. | 2.0 L, about 300 hp (?). | Not stated (?). | Group N in a production car cup. |
| 1997 to 2010 | World Rally Car: 2.0 L turbo, four-wheel drive, built on a road car. | 34 mm restrictor, about 300 hp, 1,230 kg. 2006: active differentials and water injection banned, one engine for two rallies. | Pirelli alone 2008 to 2010. | |
| 2011 to 2016 | World Rally Car 1.6 L turbo. | 33 mm restrictor, 1,200 kg, 1,350 kg with crew (1,360 from 2013). | Michelin alone 2011 to 2020. | Volkswagen four titles in a row. |
| 2017 to 2021 | Wider World Rally Cars with more aero. | 36 mm restrictor, up to 380 hp. | Michelin, Pirelli from 2021. | One surface type per rally from 2021. |
| 2022 to 2024 | Rally1 hybrid: tube frame, the old 1.6 L engine, a 100 kW electric boost. | Hybrid adds 84 kg. Driver picks boost settings before each stage. | Pirelli, at most 28 tyres per rally (2023). | Electric only on road sections where the organiser says. |
| 2025 to 2026 | Rally1 without the hybrid. | Same engine. | Hankook alone. | Hybrid dropped because damaged units cost too much. 2027: new rules on a standard FIA chassis. |

## Classes in one rally

| Class | Cars |
|---|---|
| Manufacturers (P1) | Rally1, up to three crews nominated, the best two score |
| WRC2 (P2, from 2013) | Rally2, best 6 of 7 rallies count |
| WRC3 (P3) | Rally3, best 6 of 7 |
| Junior WRC | one-make Ford Fiesta Rally3, drivers under 29 |
| Masters Cup (from 2023) | drivers over 50 |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Rally stages on closed roads, one car at a time | No | the game races on circuits (N10) |
| Driver and co-driver crews | No | C8 |
| Classes in one event, nominated crews | No | B4 |
| Weight and restrictor by class | No | B2 |
| Hybrid boost chosen per stage | No | B13 |
| One tyre maker, tyres per event | Yes | `tyre_suppliers.json`, `weekend_tyre_allocation` |
| Engine for two events | Yes | `seasonal_component_allocation_rule` |

## Sources

- Wikipedia, "World Rally Championship" (eras, classes, nominations,
  tyres), "Group B" (weight and tyre table, 1986), "World Rally Car"
  (restrictors, weights, 2006 rules), "Rally1" (hybrid, 2025, 2027).
- Not confirmed, marked `(?)`: car rules before 1982, Group A limits.
- Conflict: World Rally Car power from 2017 (230 to 280 kW, or 300 to
  380 hp).

## Discord post

=== post | WRC cars history | wrc-cars-classes
## WRC cars, classes and tyres, 1973 to 2026

Rallying, as the series furthest from the game. The table is below. What stood out to me:

- **Group B (1982 to 1986):** weight by engine size, turbos counted 1.4 times, no boost limit. Over 500 hp, then banned after the 1986 deaths.
- **A restrictor sets the power:** 34 mm, 33 mm, 36 mm.
- **Rally1 hybrid (2022 to 2024):** a 100 kW boost, the driver picks the settings before each stage. Dropped for 2025 because repairs cost too much.
- **Several classes in one rally:** manufacturers, WRC2, WRC3, Junior WRC, each with its own priority and title.
- **Manufacturers nominate up to three crews,** the best two score.

For the game: a rally pack would need stages run one car at a time against the clock. The rest is familiar: classes in one event, a co-driver per car, weight and restrictor per class.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
