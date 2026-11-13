# Endurance drivers, crews and pit stops, 1953 to 2026

Part of the endurance rules history (classes and BoP, drivers and pit
stops, race format and points). Covers the World Sportscar Championship
(1953 to 1992), Le Mans, and the FIA WEC (2012 to 2026). The table image
is made with
`python -I tools/history_table.py docs/history/wec-drivers-pit-stops.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Drivers per car | Drive time limits | Driver ratings | Pit stop rules |
|---|---|---|---|---|
| 1953 to 1970s | At first no rule. Almost every team uses two drivers. | None at first. | None. | Engine off while refuelling (since when (?)). Oil and water may only be topped up after at least an hour of racing (old rule, end year (?)). |
| 1950s to 1960s | Some tried to drive alone (Levegh, Hall). Solo drives were banned later (year (?)). | | | |
| 1980s | Two-driver crews until the 1980s, then at least three per car at Le Mans by the end of the decade (?). | | | |
| 1990s to 2016 | Three drivers per car at Le Mans. | At most 4 hours in any 6 hours, at most 14 hours in total (from the 1990s). | GTE Pro for professional crews, GTE Am for amateurs (2012). | Engine off while refuelling. Mechanics may not work on the car during refuelling. The driver may change during refuelling. |
| 2017 to 2022 | Three. A crew of two can still finish (two drivers did all 24 hours in 2014). | Same. From 2017: if it is 32 °C or hotter, at most 80 minutes in a row and 30 minutes rest. | FIA ratings since 2015: Platinum, Gold, Silver, Bronze. Bronze for drivers who got their first licence at 30 or older. | Same. |
| 2023 to 2026 | Three. | Same. | 2023: many Silver drivers moved up to Gold. Bronze drivers may not race in Hypercar. LMGT3 (2024): at least one Bronze, plus a Bronze or Silver, at most one Gold or Platinum. | Same. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Two or three drivers per car | No | C8 |
| Drive time limits | No | C8 |
| Driver ratings (Platinum to Bronze) | No | C8 |
| Driver change at a stop | No | C8 |
| Refuelling | Yes | `formula_refueling` |
| Le Mans pit rules (engine off, no work while refuelling) | No | B10 |

## Sources

- Wikipedia, "24 Hours of Le Mans" (crews, solo attempts, drive time
  limits, the 2017 heat rule, pit stop rules unique to Le Mans), "FIA Driver
  Categorisation" (2015 start, the four ratings, 2023 change, Bronze ban in
  Hypercar), "FIA World Endurance Championship" (GTE Pro and Am).
- FIA WEC regulations page and Autosport, Sportscar365 (LMGT3 crew rule).
- Not confirmed, marked `(?)`: when solo drives were banned, the exact
  year of the three-driver rule (Wikipedia says three were required by
  the end of the 1980s, but also that two drivers finished in 2014), when
  the fluid top-up rule ended. Not covered: minimum drive time, rookie tests, crew sizes in the
  pits.

## Discord post

=== post | Endurance drivers and pit stops history | wec-drivers-pit-stops
## Endurance drivers, crews and pit stops, 1953 to 2026

Part two of the endurance rules history. The table is below. What stood out to me:

- **No rule on drivers at first.** Two per car was normal, some tried to drive the whole 24 hours alone. Today three drivers per car at Le Mans.
- **Drive time limits:** at most 4 hours in any 6, at most 14 hours in total. Since 2017, in heat over 32 °C, at most 80 minutes in a row.
- **Driver ratings since 2015:** Platinum, Gold, Silver, Bronze. Bronze is for drivers who got their first licence at 30 or older. Bronze drivers can't race in Hypercar, and the amateur classes need them.
- **Le Mans pit rules:** engine off while refuelling, nobody works on the car during refuelling, but the driver may change. Oil and water could only be topped up after at least an hour (an old rule).

This is the entry model from my earlier post at its hardest: one car, three drivers, each with a rating, a minimum and maximum drive time, and a class that needs a certain mix of ratings. Plus pit rules that say what can happen at the same time (fuel, tyres, driver). The game would need that for the endurance mode anyway.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
