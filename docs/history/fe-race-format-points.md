# Formula E race format, qualifying and points, 2014-15 to 2025-26

Part of the Formula E rules history (cars and energy, race format and
points). The table image is made with
`python -I tools/history_table.py docs/history/fe-race-format-points.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Seasons | Race | Qualifying | Safety car | Points and titles |
|---|---|---|---|---|
| 2014-15 to 2017-18 | Set number of laps, a car swap halfway. Practice, qualifying and race on one day. | Four groups of five, Super Pole for the top five from 2015-16. Groups by lottery, by championship order from 2017-18. | | 25-18-15-12-10-8-6-4-2-1, pole 3, fastest lap 2 (first two seasons), then 1, top 10 only from 2017-18. 2014-15: the worst round is dropped. Drivers' and teams' titles. |
| 2018-19 to 2020-21 | 45 minutes plus one lap. | Groups by championship order, then Super Pole for the top six. | 2019-20 and 2020-21: 1 kWh taken off per minute under safety car or full-course yellow. | Pole 3, fastest lap 1 (top 10 only). 2019-20 and 2020-21: 1 point for the fastest in the group stage. World Championship from 2020-21. |
| 2021-22 | 45 minutes plus time added: 45 seconds per minute of safety car in the first 40 minutes, at most 10 minutes. | Two groups by championship place (odd and even), the top four of each into duels: quarter-finals, semi-finals, final. | Time added instead of energy taken off. | Same. |
| 2022-23 to 2025-26 | Laps again, more laps after the safety car. Double-headers at many venues. | Groups and duels. 2025-26: group sessions of 10 minutes. If the duels can't run (rain, time), the grid comes from the groups. | Laps added. | Same. Manufacturers' Trophy from 2023-24, a world title from 2024-25, from each make's best two cars. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Race length in laps | Yes | per track |
| Races by time, time or laps added after the safety car | No | A3 |
| Qualifying in groups and head-to-head duels | No | A6 |
| Pole 3 points, fastest lap only in the top 10 | Partly | +1 for pole and fastest lap (B8) |
| Points table | Yes | `points_system` |
| Worst round dropped (2014-15) | No | B3 |
| Two races on one weekend | No | A1 |
| Manufacturers' title from the best two cars | No | B4 |

## Sources

- Wikipedia, "Formula E" (race formats by generation, qualifying with
  duels, points, safety car rules), season articles 2014-15, 2018-19,
  2021-22, 2022-23, 2024-25 and 2025-26 (partly via summaries).
- Autosport and Racer, September 2015 (Super Pole from 2015-16, groups by
  lottery), Autosport 2017 (groups by championship order).
- FIA Formula E, March 2024 (Manufacturers' Trophy, best two cars) and
  2024 (world title from season 11). Reports from Shanghai and Berlin
  2025 (no duels, grid from the groups).
- Autosport, Motorsport.com and FIA, 2018 (Super Pole six drivers from
  2018-19, groups by championship order). Speedcafe and The Checkered
  Flag, November 2017 (lottery ended in 2017-18). The Checkered Flag,
  September 2017 (fastest lap point only in the top 10 from 2017-18).
  FIA Formula E, October 2021 (added time rules). Racer and FIA, October
  2025 (10-minute group sessions).
- The source
  for "one lap added per four minutes of safety car" is marked as needing
  a citation, so it is left out.

## Discord post

=== post | Formula E race format history | fe-race-format-points
## Formula E race format, qualifying and points, 2014-15 to 2025-26

Part two and the last of the Formula E rules history. The table is below. What stood out to me:

- **Laps, then time, then laps again:** a set number of laps (to 2017-18), 45 minutes plus one lap (2018-19 to 2021-22), laps again with more laps after the safety car (from 2022-23).
- **The safety car costs energy or adds time:** 1 kWh per minute taken off (2019-20, 2020-21), then 45 seconds added per minute (2021-22).
- **Qualifying as head-to-head duels** since 2021-22: two groups, then quarter-finals, semi-finals and a final.
- **Points:** 25 down to 1, plus 3 for pole and 1 for the fastest lap in the top 10. For two seasons also 1 point for the fastest in the group stage.
- **A manufacturers' trophy** from 2023-24 (a world title from 2024-25), from each make's best two cars.

For the game: races by time with time or laps added after the safety car, qualifying duels, and bonus points with conditions. All three are in my earlier posts, so Formula E is another case for the same settings.

The last table in the picture shows what the game can do today: yes, partly or no.

That's the Formula E series. Mistakes? Tell me!
