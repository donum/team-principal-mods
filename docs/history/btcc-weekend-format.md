# BTCC race weekend format, 1958 to 2026

Part of the BTCC rules history (weekend format, points and titles, cars
classes and balancing). The table image is made with
`python -I tools/history_table.py docs/history/btcc-weekend-format.md`.

`(?)` marks a detail that the sources we read did not confirm. The
sources had little on the years before 2000.

## Table

| Years | Races per meeting | Qualifying | Grids for later races | Pit stops and quirks |
|---|---|---|---|---|
| 1958 to 1989 | One race (?). | Timed qualifying (?). | | Many classes in one race, by engine size. |
| 1990 to 1999 | Mostly one, some double-headers (three in 1992). Two at every meeting from 1995. 1998: a sprint and a feature race. | 1998: a one-lap shootout for the sprint race grid, dropped for 2001. | | 1998 to 2001: one mandatory stop for two tyres in the feature race, between 15% and 75% of the distance. |
| 2000 | Two: a sprint and a feature race. 24 races at 12 meetings. | Two qualifying sessions. | | Tyre warmers banned, so cars start and leave the pits on cold tyres. An engine change after qualifying means the back of the grid. |
| 2001 | Planned: two class sprints plus one feature. After round 1 the sprints were merged, too few BTC-T cars. | Normal timed sessions again. | | The feature race: BTC-T cars start first, the Production cars a set time later with one lap less. First race outside the UK, Mondello Park. |
| 2002 to 2003 | Two. | Timed. | | |
| 2004 to 2005 | Three, 30 races a year. | Timed, sets the race 1 grid. | 2004: race 2 is race 1 order with the top 10 reversed, race 3 is race 2 order. 2005: the reversal moves to race 3, so 10th in race 2 takes race 3 pole. | Drivers could slow down to finish 10th. |
| 2006 to 2013 | Three. | 30 minutes, sets the race 1 grid. | Race 2: race 1 order. Race 3: race 2 order with the top 6 to 10 reversed, the number drawn by the race 2 winner (2006). Later 6 to 12 (year (?)). | |
| 2014 to 2025 | Three, 16 to 25 laps each. | Two practice sessions, then 30 minutes of qualifying. | Same, top 6 to 12 reversed, the draw is made by the 10th-place finisher of race 2. | Three laps added if three or more laps run behind the safety car. |
| 2026 | Three on Sunday, plus a qualifying race on Saturday. | Two groups of 15 minutes. They set the qualifying race grid, the faster group on the odd places. | Qualifying race result sets the race 1 grid. Races 2 and 3 as before. | The qualifying race pays half points, no bonus points. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Three races per meeting | Partly | each race as its own week (A1) |
| Race 2 grid from race 1 | No | A1 |
| Reversed grid by a draw | No | A6 |
| Race length in laps | Yes | per track |
| Laps added after the safety car | No | A3 |
| Classes with a staggered start | No | A3, B4 |
| Mandatory stop | No | B5 |

## Sources

- Wikipedia, "British Touring Car Championship" (race and grid rules,
  draw, lengths, safety car laps; partly via summary), season articles
  2000, 2001 and 2004 (regulation sections read in full).
- Fact check: 1992, 1995 and 1998 season articles (double-headers,
  sprint and feature, shootout, feature race stop), 2005 and 2006 season
  articles and Crash.net 2006 (reversal in race 2 in 2004, in race 3 in
  2005; the 2006 draw of 6 to 10 by the race 2 winner), btcc.net, BARC,
  RACER and Touring Car Times 2025 (2026 qualifying race).
- Not confirmed, marked `(?)`: race counts before 1990, qualifying before
  1998, the year the draw range grew to 6 to 12.
- Resolved conflict: the 2004 article (reversal in race 2) and the main
  article (10th in race 2 took race 3 pole) describe 2004 and 2005.

## Discord post

=== post | BTCC weekend format history | btcc-weekend-format
## BTCC race weekend format, 1958 to 2026

After F1, DTM, IndyCar and endurance racing, here's the BTCC. The table is below. What stood out to me:

- **Three races per meeting since 2004,** about 30 per season. Before that two, and in the early years one.
- **The race 3 grid is drawn:** a ball draw decides how many of the top finishers of race 2 are reversed (6 to 12 today). Since 2014 the driver who finished 10th draws the ball.
- **2026: a Saturday qualifying race** with half points sets the race 1 grid.
- **In 2005 the 10th place in race 2 got race 3 pole,** so drivers slowed down to finish 10th. That's why the draw came.
- **2001: a "tortoise and hare" feature race.** The faster class started first, the slower class later with one lap less.
- **Mandatory stops** for two tyres (1998 to 2001), and no tyre warmers in 2000, so cars left the pits on cold tyres.
- **Races are lap-based** (16 to 25 laps) with three laps added after a long safety car.

For the game: three races per meeting, a grid rule per race (finishing order, partial reverse, a random draw), classes with staggered starts, and laps added after the safety car. The weekend builder from my first post would need "random draw" as a grid option.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
