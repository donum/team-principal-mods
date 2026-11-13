# MotoGP race format, qualifying and points, 1949 to 2026

Part of the MotoGP rules history (bikes and tyres, race format and
points). The table image is made with
`python -I tools/history_table.py docs/history/motogp-race-format-points.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Race | Qualifying and grid | Points | Quirks |
|---|---|---|---|---|
| 1949 to 1968 | One race per Grand Prix. | Not stated (?). | 1949: 10-8-7-6-5 and 1 for the fastest lap, best 3 count. 1950: 8-6-4-3-2-1, best 4. Then best results by number of rounds (?). | 1954 Ulster GP not counted after rain shortened it. |
| 1969 to 1987 | Same. Push starts until 1987. | Not stated (?). | 15-12-10-8-6-5-4-3-2-1. Best results only, in 1976 split by season half. All results count 1977 to 1987. | |
| 1988 to 1992 | Same. Grid of 4 per row from 1990. | Not stated (?). | 20-17-15-13-11-10-9-8-7-6-5-4-3-2-1 (1988 to 1991). 1992: 20-15-12-10-8-6-4-3-2-1. | |
| 1993 to 2004 | About 45 minutes, no stops. Rain: red flag, restart on wet tyres. | Not stated (?). Grid of 3 per row from 2004. | 25-20-16-13-11-10-9-8-7-6-5-4-3-2-1, top 15. | |
| 2005 to 2012 | Flag-to-flag from 2005: riders swap to a second bike with wet tyres. | Qualifying tyres until 2008. | Same. | |
| 2013 to 2022 | Same. Long lap penalty from 2019 for track limits. | Q1 and Q2: the top 10 from practice go straight to Q2, the best two of Q1 join them. | Same. Riders', constructors' and teams' titles. | Rookie rule dropped for 2013. |
| 2023 to 2026 | Sprint race on Saturday, about half the distance. Main race Sunday. | Q1 and Q2, direct Q2 places from Friday practice. | Sprint: 12-9-7-6-5-4-3-2-1. Race as before. A race needs half its distance for full points. | 2023 Japan: red flag on lap 13 of 24, full points. 2027: separate sprint qualifying on Friday. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Race length in laps | Yes | per track |
| Points table to 15th | Yes | `points_system`, any length |
| Best N results, split season | No | B3 |
| Sprint race with its own points | No | A1, B3 |
| Q1 and Q2 with the top 10 from practice | No | A6 |
| Flag-to-flag bike swap | No | B10 |
| Long lap penalty | No | B11 |
| Grid of three per row | No | grid two by two (A6) |

## Sources

- Wikipedia, "List of FIM World Championship points scoring systems" (every
  scale and best-result rule, read in full), "Grand Prix motorcycle racing"
  (event format, flag-to-flag, red flags, chronology), 2013 and 2023 season
  articles (Q1 and Q2, sprints, Japan 2023).
- Not confirmed, marked `(?)`: points scales 1951 to 1968 and 1970 to
  1975, qualifying before 2013.

## Discord post

=== post | MotoGP race format history | motogp-race-format-points
## MotoGP race format, qualifying and points, 1949 to 2026

Part two and the last of the MotoGP rules history. The table is below. What stood out to me:

- **Best results only** until 1976, once even split by season half (like F1 and DTM).
- **25-20-16 down to 1 for the top 15** since 1993.
- **Flag-to-flag since 2005:** when it starts to rain, riders come in and jump on a second bike with wet tyres.
- **Q1 and Q2 since 2013:** the top 10 from practice go straight to Q2, the two fastest from Q1 join them.
- **Sprint races since 2023,** half the distance, half the points.
- **Long lap penalty** for track limits since 2019.

For the game: sprints are the "several races per weekend" request again, Q1 and Q2 fits qualifying as stages, and the bike swap is a pit-stop procedure rule.

The last table in the picture shows what the game can do today: yes, partly or no.

That's the MotoGP series. Mistakes? Tell me!
