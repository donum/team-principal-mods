# Formula E cars, energy and boosts, 2014-15 to 2026-27

Part of the Formula E rules history (cars and energy, race format and
points). Seasons run from autumn to summer; "2014-15" is season 1. The
table image is made with
`python -I tools/history_table.py docs/history/fe-cars-energy.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Seasons | Car | Power | Boosts | Quirks |
|---|---|---|---|---|
| 2014-15 | Gen1: Spark chassis, 28 kWh battery, McLaren motor for all. | 150 kW in the race, 200 kW peak. | Fan Boost: fans vote, the top three get a 5-second power boost. | Two cars per driver, a car swap halfway. Michelin all-weather tyre. |
| 2015-16 to 2017-18 | Gen1, teams build their own motor, inverter and gearbox. | 170 kW (2015-16), 180 kW (2017-18). | Fan Boost. | Car swap until 2017-18. |
| 2018-19 to 2021-22 | Gen2: one car for the whole race, halo, 54 kWh battery. | 200 kW, 220 kW in 2021-22, 250 kW peak. | Attack Mode from 2018-19: drive through a zone off the racing line for extra power (+25 kW, +35 kW, 250 kW). Fan Boost to 2021-22, the top five from 2018-19, in the second half. | Teams may buy a motor from another maker. 2019-20: 1 kWh taken off per minute under the safety car. |
| 2022-23 to 2023-24 | Gen3: 38.5 kWh usable, up to 600 kW regeneration. | 300 kW race, 350 kW qualifying and Attack Mode. | Attack Mode: 4 minutes in two activations, 8 minutes from Jakarta 2023. No Fan Boost. | Hankook tyres. A Manufacturers' Trophy in 2023-24, a world title from 2024-25. |
| 2024-25 to 2025-26 | Gen3 Evo: all-wheel drive in Attack Mode, qualifying and starts. | 300 kW race, 350 kW peak (the front motor adds up to 50 kW). | Attack Mode, Pit Boost from Jeddah 2025: a 30-second stop at 600 kW for 3.85 kWh. | Lola, Yamaha join. 17 races in 2025-26. |
| 2026-27 | Gen4: 55 kWh, permanent all-wheel drive. | 450 kW race, 600 kW qualifying and Attack Mode. | Attack Mode, Pit Boost. | Bridgestone tyres with a wet tyre. Not raced yet. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| A fixed amount of energy per race | No | new lever (N8) |
| Electric power, regeneration | Partly | `ers_policy` for the hybrid part only |
| One chassis and battery, own powertrain | Yes | `engines.json` with level chassis ratings |
| Attack Mode (zone, minutes) | No | B13 |
| Fan Boost | No | B13 |
| Car swap halfway | No | B10 |
| Pit Boost (mandatory charging stop) | No | B5 |
| One all-weather tyre | Partly | `tyremodel.json`, allocation knows soft, medium and hard |

## Sources

- Wikipedia, "Formula E" (power by season, Attack Mode, Fan Boost, Pit
  Boost, powertrain rules), "Spark-Renault SRT_01E", "Spark SRT05e",
  "Formula E Gen3", "Formula E Gen4".
- Fan Boost reports 2015 to 2017 (top three by votes). Autosport and the
  Porsche 99X spec sheet (Gen3 Evo 350 kW, 50 kW to the front).
- FIA Formula E, March 2024 and later (Manufacturers' Trophy, world title
  from season 11). Racer, June 2026 (2026-27 calendar, Pit Boost races,
  opener on 18 December 2026).
- FIA, January 2025 (Pit Boost: 3.85 kWh, 30 seconds, 600 kW, from
  Jeddah). Motorsport.com, 2018 (Gen2 battery 54 kWh). Crash.net, 2018,
  and the Audi Formula E regulations page (Fan Boost for five drivers
  from 2018-19, from the 22nd minute). Racer and The Race, April 2024
  (Gen3 Evo 350 kW in qualifying and Attack Mode).
- Not used: 56 kWh for Gen2 (Wikipedia lead, no citation), 400 kW for
  Gen3 Evo (Wikipedia comparison table).

## Discord post

=== post | Formula E cars history | fe-cars-energy
## Formula E cars, energy and boosts, 2014-15 to 2026-27

Electric racing, very different from everything so far. The table is below. What stood out to me:

- **A fixed amount of energy per race** instead of fuel: managing it is the whole race. Gen3 has 38.5 kWh and gets a lot back under braking.
- **Car swaps halfway** in the first four seasons, because one battery didn't last a race.
- **Fan Boost (to 2021-22):** fans vote, the top three (later five) get a short burst of extra power.
- **Attack Mode (from 2018-19):** drive through a zone off the racing line for extra power, now with all-wheel drive.
- **Pit Boost (from 2025):** a mandatory 30-second charging stop.
- **One chassis and battery for all,** but teams build their own motor and powertrain.

For the game: an energy limit per race, a boost with a zone and a time budget, and a mandatory stop that only charges. The boost is the same request as push-to-pass in DTM and IndyCar.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
