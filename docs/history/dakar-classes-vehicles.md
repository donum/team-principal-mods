# Dakar classes and vehicles, 1979 to 2026

Part of the Dakar rules history (classes and vehicles, format and routes).
A rally raid: bikes, cars and trucks in one event, over two weeks of long
stages. The table image is made with
`python -I tools/history_table.py docs/history/dakar-classes-vehicles.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Bikes and quads | Cars | Trucks and others | Quirks |
|---|---|---|---|---|
| 1979 to 1988 | Motorbikes from 1979 (Yamaha XT500 wins the first). | Cars from 1979 (a Range Rover is the best car, all vehicles in one ranking that year), Porsche 1984, then Peugeot and Mitsubishi. | Trucks a separate category from 1980. | Open to almost anything with wheels. 1988: Vatanen's Peugeot stolen from the service area, he is disqualified. |
| 1989 to 2004 | Bikes. | FIA Group T from 1990: T1 series production, T2 improved production, T3 prototypes. From 2004 (?) T1 is the improved class and T2 production. | No trucks in 1989 after a DAF crew member died in 1988. Fast support trucks (T5, later T4.3) from 1998 (?). | 2001: Kleinschmidt is the first woman to win (cars). |
| 2005 to 2016 | 2005: twin-cylinder bikes limited to 450cc. From 2011 all bikes 450cc. Quads their own class from 2009 (2WD up to 750cc, 4WD up to 900cc). | T1 by fuel and drive (2WD buggies, 4WD), T2 production. | Trucks T4.1 (production) and T4.2 (modified), support trucks T5, later T4.3. | Kamaz dominates the trucks. 2WD buggies may change tyre pressure while driving, 4WD cars may not. |
| 2017 to 2021 | Bikes (RallyGP, Rally2), quads. | Same. | UTVs from 2017, split into T3 light prototypes and T4 side-by-sides in 2021. Dakar Classic from 2021 for older cars and trucks, scored on regularity. | Unassisted bikes (Malle Moto, now "Original by Motul"): no outside help, the riders service their own bikes. |
| 2022 to 2026 | Bikes. Quads dropped for 2025. | T1 "Ultimate" (T1.1 4WD including the larger T1+, T1.2 2WD, T1.U electric or hybrid), T2 "Stock" (these names from 2024). Audi RS Q e-tron (electric drive) wins 2024. | T3 "Challenger", T4 SSV, T5 trucks. Mission 1000 for alternative energy from 2024. | Classic cut-off moved to 2005 cars for 2025. FIA "Equivalence of Technology" sets weight and power for the Audi (2023: minimum weight up 100 kg, then 8 kW more from stage 5). 2022: bigger wheels and more suspension travel for 4WD T1+ cars. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Bikes, quads, cars and trucks in one event | No | B4, N9 |
| Classes by drive, fuel and weight | No | B2, B4 |
| Crews of two or three | No | C8 |
| Unassisted riders | No | B10 |
| Regularity scoring (Classic) | No | B3 |

## Sources

- Wikipedia, "Dakar Rally" (categories, classes, quads, UTVs, Classic,
  Mission 1000, unassisted class, winners), "World Rally-Raid
  Championship" (T1 to T5 names), "Group T1", "Group T3", "Group T4".
- "1979 Paris-Dakar Rally" (one ranking for all vehicles in 1979).
- Wikipedia, "Group T1" and "Group T2" (Group T split in 1990, T1
  series production and T3 prototypes until 2003, T1 improved and T2
  production from 2004). French Wikipedia "Rallye Dakar" (T1 series,
  T2 modified series at first, T2 and T3 merged in 2002) dates the T1
  and T2 swap to 2006. The FIA pages are used for the table.
- Wikipedia, "2017 Dakar Rally" (new UTV category) and "2021 Dakar
  Rally" (new T3 Light Proto, T4 SSV and T5 truck classes, Dakar
  Classic new). French Wikipedia "Rallye Dakar" (SSV since 2017).
- Commercial Motor, 21 December 2006 (race trucks T4, fast assistance
  trucks T5). Only "Dakar Rally" gives 1998 for the support trucks, so
  that year stays `(?)`.
- Balancing: Motorsport.com, "Car race at Dakar: a collision of worlds"
  (2013, tyre inflation on the move for buggies only); Autosport and
  Motorsport.com on the 2022 rules (T1+ with 37 inch wheels and 350 mm
  travel, inflation kept for 2WD and electric cars); Motorsport.com,
  "Sainz hits out at 100kg weight increase" and DirtFish, "Audi to
  receive more power from Dakar stage five" (2023). The Drive, January
  2021 (speed limits of 180 km/h for T1 and T2 cars from 2021).
- Confirmation round: FIA, "New terminology of FIA cross-country
  rallying disciplines to be used from 2024" (Ultimate, Stock,
  Challenger, SSV, Truck); The Checkered Flag, October 2023 (same).
  The T1 and T2 swap year stays `(?)`: English Wikipedia says 2004,
  French Wikipedia says 2006, no FIA text found. Motorsport.com and
  Autosport, 2018, "Toyota drivers slam unfair Dakar rules" (on-board
  inflation for buggies only).
- Not found: tyre size rules before 2022, air restrictor tables (a
  Motorsport.com report gives 39 mm for the Mini buggy and 37 mm for
  the Toyota 4WD in 2019).

## Discord post

=== post | Dakar classes history | dakar-classes-vehicles
## Dakar classes and vehicles, 1979 to 2026

A different type of rally: the rally raid. The table is below. What stood out to me:

- **Everything in one event:** bikes, quads (to 2024), cars, trucks, light prototypes and side-by-sides, each with its own results.
- **Car classes by drive and fuel:** 2WD buggies against 4WD, production cars, and since 2022 electric and hybrid cars (the Audi won in 2024).
- **Unassisted riders:** no outside help, they fix their own bikes at night.
- **Dakar Classic** (from 2021) is scored on regularity, not speed.
- **Mission 1000** (from 2024) for alternative energy, with points per stage.

For the game this is far from circuit racing: many vehicle types in one event, crews of two or three, and classes with their own scoring. The classes part is the same lever as in endurance racing.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
