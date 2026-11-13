# World Rallycross format and cars, 2014 to 2025

The FIA World Rallycross Championship (World RX), with the European
championship from 1973 as background. Short races on mixed tarmac and
gravel tracks. The table image is made with
`python -I tools/history_table.py docs/history/wrx-format-cars.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Event | Cars | Points | Quirks |
|---|---|---|---|---|
| 1973 to 2013 | European championship: from 1976 under FIA rules, Group 5, then Group A and Group B cars. | Classes split by drive and car group (Division 1 and 2). | Not stated (?). | Group B cars moved to rallycross from 1987. |
| 2014 to 2021 | Two-day events. Four qualifying heats of 4 laps, 3 to 5 cars each, one joker lap per race. The top 12 go to two semi-finals of 6 laps, the top 3 of each to the final. | Supercar (RX1 from 2021): 2.0 L turbo, four-wheel drive, about 600 hp, 1,300 kg, 45 mm restrictor. RX Lites, then RX2. | Heats: 16 down to 1. Semi-final: 6 down to 1. Final: 8-5-4-3-2-1. The final's winner does not always score the most. | Solberg champion 2014, 2015. Kristoffersson from 2017, eight titles in all. |
| 2022 to 2023 | Same idea. | RX1e: electric, two motors, 680 hp (from August 2022). RX2e. | 20-16-13 down to 1 for 15 places (?). | All-electric series. |
| 2024 to 2025 | Same. | RX1e and RX1 (petrol on sustainable fuel) race together. | 2025: 25-20-17 down to 1 for 18 places, plus 3-2-1 per heat (?). | World RX cancelled after 2025, replaced by the European championship for 2026. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Heats, semi-finals and a final in one event | No | A1, A6 |
| Points per heat, semi-final and final | No | B3 |
| Joker lap, tarmac and gravel in one lap | No | N12 |
| Electric and petrol cars together | No | C9 |
| Short races of 4 to 6 laps | Yes | laps per track |

## Sources

- Wikipedia, "FIA World Rallycross Championship" (format, points tables,
  classes, electric switch, champions), "FIA European Rallycross
  Championship" (history), "Rallycross" (joker lap, surfaces).
- Not confirmed, marked `(?)`: European points, what the 2022 to 2025
  points rows apply to.
- Conflict: RX1e from 2021 or from August 2022.

## Discord post

=== post | Rallycross history | wrx-format-cars
## World Rallycross format and cars, 2014 to 2025

Rallycross: short races on tracks of tarmac and gravel. The table is below. What stood out to me:

- **An event is a tournament:** four qualifying heats, two semi-finals, a final, all in one weekend.
- **The joker lap:** every driver must take a longer route once per race, so strategy matters even in a 4-lap race.
- **Points for every round of the event,** so the final's winner doesn't always score the most.
- **Electric from 2022,** then petrol and electric cars together (2024, 2025).
- **Kristoffersson: eight titles.**

For the game: an event as several races with points each is the weekend builder again, and the joker lap is a track feature the game doesn't know.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
