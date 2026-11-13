# NASCAR Cup points and playoffs, 1949 to 2026

Part of the NASCAR rules history (points and playoffs, race format and
cautions, cars and entries). Strictly Stock 1949, Grand National 1950 to
1970, Winston Cup 1971 to 2003, then Nextel, Sprint and Monster Energy Cup,
NASCAR Cup Series from 2020. The table image is made with
`python -I tools/history_table.py docs/history/nascar-points-playoffs.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Race points | Bonus points | Title format | Quirks |
|---|---|---|---|---|
| 1949 to 1951 | By prize money: 50 points per 1,000 USD of purse, down to 14th. | | Season total. | 1949: Jim Roper was declared winner of the first race after the leader was disqualified. |
| 1952 to 1967 | By prize money, top 25. | | Season total. | A rich race is worth many times a small one. |
| 1968 to 1971 | By race length: 50, 100 or 150 for a win, every place down to 50th scores. | | Season total. | |
| 1972 to 1974 | Points per place plus points per lap (1972, 1973). 1974: purse times races started. | | Season total. | 1974 is the strangest: money decides. |
| 1975 to 2003 | Same for every race: 175 for a win, 170 for 2nd, 5, 4 and 3 points steps, last points at 54th. | Leading a lap +5, most laps led +5. | Season total. | 1992: Kulwicki led one lap more than Elliott in the final race, took the 5 bonus points and the title. 2003: Kenseth champion with one win, Newman had eight. |
| 2004 to 2010 | Win 180 (2004), 185 (2007). | Same. | Chase: top 10 (and close ones) from 2004, top 12 from 2007, reset for the last 10 races. From 2007 +10 per win in the reset. | |
| 2011 to 2013 | 43 for a win down to 1 for 43rd, +3 for the win. | Leading a lap +1, most laps led +1, the winner +1 for leading. | Chase: top 10 plus two wild cards with the most wins, reset to 2,000, +3 per win. | 2011: Stewart and Edwards tied on points, Stewart champion on wins (5 to 1). 2013: 13 drivers, one added after the Richmond affair. |
| 2014 to 2016 | 43 (2016: 40) down to 1. | Same. | Elimination: 16 drivers, a win in a round means the next round, rounds of 12, 8 and the Championship 4. Best of the four in the final race is champion. | 2016: field of 40 cars. |
| 2017 to 2024 | 40 for 1st, more for the win. | Stage points: top 10 after stages 1 and 2 score 10 down to 1. Playoff points for stage and race wins. | Playoffs: 16 drivers, playoff points carried into each round. | 2023: first champion who did not win the final race. Eliminated drivers race for fifth place. |
| 2025 | Same. | Plus 1 for the fastest lap. | Same playoffs. | Last year of the elimination rounds. |
| 2026 | Win 55, 2nd 35. | Stage and fastest lap points. No playoff points. | "The Chase" returns: 16 drivers, no eliminations (?). | Win-and-in dropped (?). |

## Other titles

| Title | Rule |
|---|---|
| Owners' championship | per car, scored like the drivers, owner points also for drivers who can't score |
| Manufacturers' championship | to 2013: 9-6-4-3-2-1 for the top six makes; from 2014 each make's best car |
| Rookie of the Year | official from 1958; from 2026 at most 12 earlier Cup starts, own points |
| Regular season champion | from 2017, top of the points after race 26 |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta, as an oval pack. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Same points per place for every race, win bonus | Yes | `points_system`, any length |
| Points by prize money or race length | No | B3 |
| Leading a lap, most laps led bonus | No | laps led are counted, but score nothing (B8) |
| Stage points | Yes | `oval_stage_racing` with `stage_points` |
| Pole and fastest lap points | Yes | `oval_pole_point`, `oval_fastest_lap_point` |
| Chase with a reset | Partly | `oval_championship_format` chase: one seeded reset, no wins in the seeding |
| Elimination rounds, playoff points | No | new lever (N7) |
| Owners' and manufacturers' titles | Yes | oval owner, manufacturer and best-car championships |
| Rookie of the Year | No | B4 |

## Sources

- Wikipedia, "List of NASCAR points scoring systems" (every scale, read in
  full), "The Chase (NASCAR)" (Chase and playoff formats), "NASCAR Cup
  Series" (owners' and manufacturers' titles, tie-break, 2011), "NASCAR
  Rookie of the Year", "1992 NASCAR Winston Cup Series".
- Game support from the 0.99.6 oval code (stage racing, chase, oval
  championships, bonus points).
- Not confirmed, marked `(?)`: the 2026 Chase details. Conflict: who made
  the 2004 Chase besides the top 10 (within 400 points, or ties).

## Discord post

=== post | NASCAR points history | nascar-points-playoffs
## NASCAR Cup points and playoffs, 1949 to 2026

After F1, DTM, IndyCar, endurance and BTCC, here's NASCAR, as a test of the oval mode. The table is below. What stood out to me:

- **Points by prize money (1949 to 1967), by race length (1968 to 1971), even purse times races started (1974).** Then the same table for every race from 1975 on.
- **Bonus points for leading a lap and leading the most laps** from 1975 to 2016. Kulwicki won the 1992 title by leading one lap more than Elliott.
- **The Chase from 2004,** then elimination rounds from 2014: 16 drivers, a win means the next round, the best of the final four is champion.
- **Stage points since 2017,** playoff points for stage and race wins, and a fastest lap point from 2025.
- **2026: "The Chase" is back** without eliminations.

The oval mode already has stage points, a chase with one reset, charters and owners' and manufacturers' titles. What's missing: bonus points for laps led, points by race length, and elimination rounds with playoff points.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
