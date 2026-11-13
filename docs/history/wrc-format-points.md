# WRC event format and points, 1973 to 2026

Part of the WRC rules history (cars and classes, event format and points).
The table image is made with
`python -I tools/history_table.py docs/history/wrc-format-points.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Event | Retirements | Points | Titles |
|---|---|---|---|---|
| 1973 to 1978 | Special stages against the clock, joined by road sections. 8 to 13 rallies a year. | Out is out. | Makes only: 20-15-12-10-8-6-4-3-2-1, best car of each make (1973). Later by overall and group place (?). | Manufacturers from 1973, an FIA Cup for drivers in 1977 and 1978. |
| 1979 to 2003 | Same. 8 to 14 rallies (8 in 1995). | Out is out. | Drivers: 20-15-12-10-8-6-4-3-2-1 to 1996, 10-6-4-3-2-1 from 1997, 10-8-6-5-4-3-2-1 from 2003. Makes: own scales. | Drivers' title from 1979, co-drivers recorded from 1982 (?). |
| 2004 to 2010 | Same. 12 to 16 rallies. | Restart the next day after retiring ("SuperRally", later "Rally 2"), with a time penalty, first tried in 2004. | 10-8-6-5-4-3-2-1 to 2009. Top 10: 25-18-15-12-10-8-6-4-2-1 from 2010. | |
| 2011 to 2016 | Same. 13 rallies. Shakedown Thursday. | Same. | Plus the Power Stage at the end: 3-2-1. | Makes score from their best two nominated crews. |
| 2017 to 2023 | Same. Since 2021 one surface per rally. 7 rallies in 2020. | Same, "restart after retirement" from 2019. Only crews that restarted can score. | Power Stage 5-4-3-2-1. Makes score Power Stage points from 2021. | |
| 2024 | 15 to 30 stages, at most 350 km of stages, 13 rallies. | Same. | Saturday night standings: 18-15-13-10-8-6-4-3-2-1 (if the crew finishes). Sunday stages: 7 down to 1. Power Stage 5 down to 1. Most per rally: 30. | Drivers' and makes' champions differ in 2018, 2019, 2020 and 2024. |
| 2025 to 2026 | Same. | Same. | Final result again: 25-17-15-12-10-8-6-4-2-1. Sunday stages 5 down to 1. Power Stage 5 down to 1. Most per rally: 35. | |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Stages against the clock, overall time | No | N10 |
| Restart after retiring with a penalty | No | N10 |
| Bonus points for the Power Stage | No | B8 |
| Points for Saturday standings and Sunday stages | No | B3 |
| Makes score from the best two nominated crews | No | B4 |
| Co-drivers' title | No | C8 |
| Best 6 of 7 in the support classes | No | B3 |

## Sources

- Wikipedia, "World Rally Championship" (format, restart rule, 2024
  points), "Power Stage" (bonus points by year), "Rally2" (restart rule
  name), lists of seasons and champions.
- Wikipedia season articles 1973, 1979, 2010, 2025 and 2026 (points
  scales, rally counts), DirtFish (SuperRally first tried at the 2004
  Acropolis Rally, before that a retirement ended the rally).
- Not confirmed, marked `(?)`: makes' points 1974 to 1978, co-drivers'
  records, running order rules.
- Crash.net and GrandPrix.com, 2002 (10-6-4-3-2-1 replaced by
  10-8-6-5-4-3-2-1 for 2003).
- Scales: 25-18-15 from 2010 to 2023, 25-17-15 from 2025.

## Discord post

=== post | WRC format history | wrc-format-points
## WRC event format and points, 1973 to 2026

Part two and the last of the WRC rules history. The table is below. What stood out to me:

- **Stages against the clock,** one car at a time, joined by road sections. Today 15 to 30 stages and at most 350 km of them.
- **Restart after retiring** the next day, with a time penalty per missed stage ("SuperRally", later "Rally 2").
- **The Power Stage:** bonus points for the fastest on the last stage, 3-2-1 from 2011, 5 down to 1 from 2017.
- **2024: points split over the weekend:** 18 down to 1 for the Saturday night standings, 7 down to 1 for Sunday, plus the Power Stage. From 2025 back to points for the final result, plus 5 down to 1 for Sunday.
- **Manufacturers score from their best two crews.**

For the game: rallying is the furthest from what the game does. But the points ideas carry over: bonus points with conditions and points at set moments of an event, like IMSA's points during a race.

The last table in the picture shows what the game can do today: yes, partly or no.

That's the WRC series. Mistakes? Tell me!
