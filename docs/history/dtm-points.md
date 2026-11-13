# DTM points systems, 1984 to 2026

Part of the DTM rules history (qualifying, race format, pit stops and
tyres, points, weight balancing). Made from the season research in
`seasons/<id>/research/` and the rulebook page `docs/dtm_rules.html`.
The table image is made with
`python -I tools/history_table.py docs/history/dtm-points.md`.

`(?)` marks a detail the research files flag as unverified or
conflicting. No DTM ran from 1997 to 1999.

## Table

| Years | Race points | Extra points | Results that count | Other titles and quirks |
|---|---|---|---|---|
| 1984 | 20-18-16-15 down to 1, top 18. Half points per heat at two-heat rounds. | | Two drop results. | Guest starters don't score, drivers behind move up. Some sources say only German licence holders scored (?). |
| 1985 | 20 down to 1, top 18. Half points per heat at Erding and Diepholz. | | One drop result. | Foreign drivers now score. |
| 1986 to 1987 | 20 down to 1, top 18. | | One drop result (best 8 of 9 in 1986). | 1987: guest Ludwig won round 7 and scored nothing. |
| 1988 to 1989 | 20 down to 1, top 18, per race. | | Four drop results. | |
| 1990 to 1996 | 20-15-12-10-8-6-4-3-2-1 per heat. | | All results count. | 1991: teams', manufacturers' (best car per make) and privateer titles. 1993: a Class 2 cup. 1995: DTM and ITC were separate titles with the same cars. |
| 2000 | 20-15-12-10-8-6-4-3-2-1 per race. | | All. | |
| 2001 | Main race 20-15-12-10-8-6-4-3-2-1. | Qualifying race 3-2-1. | All. | |
| 2002 | Main race 10-6-4-3-2-1. | Qualifying race 3-2-1. | All. | |
| 2003 to 2011 | 10-8-6-5-4-3-2-1, top 8. | | All. | 2003: manufacturers' title from all cars. Lausitz 2007: half points. 2008: team orders banned. |
| 2012 to 2016 | 25-18-15-12-10-8-6-4-2-1. | | All. | From 2015 both races pay full points. |
| 2017 to 2018 | 25 down to 1. | Top 3 in qualifying 3-2-1. | All. | 2018: guest entries don't score, drivers behind move up. |
| 2019 | 25 down to 1. | Qualifying 3-2-1. | All. | Manufacturers score from their best 4 cars per race. |
| 2020 | 25 down to 1. | Qualifying 3-2-1. | All. | Teams with three cars score from their best two. |
| 2021 | 25 down to 1. | Qualifying 3-2-1. | All. | Guest drivers score nothing. Manufacturers count their best 3 cars. |
| 2022 | 25 down to 1. | Qualifying 3-2-1. Fastest lap +1, only for a top-10 finisher. | All. | |
| 2023 to 2026 | 25-20-16-13-11-10-9-8-7-6-5-4-3-2-1, top 15. | Qualifying 3-2-1. | All. | Half points for a race stopped before 75% (2023). Rookie of the Year with its own points (2025). |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Points table per race | Yes | `points_system` |
| Points down to 15th or 18th | Yes | `points_system`, any length |
| Drop results | No | B3 |
| Half points | No | B3 |
| Qualifying points 3-2-1 | Partly | pole point only (B8) |
| Fastest lap point only inside the top 10 | No | B8 |
| Guests score nothing | No | B9 |
| Teams, makes from best N cars, privateers, rookies | No | B4 |

## Sources

- `seasons/dtm-<year>/research/season.md` for every season, summed up in
  `docs/dtm_rules.html`.
- Gaps: drop result counts per year are in the season files, the exact
  table for 1985 to 1989 (20 down to 1) is listed only as a range. It is
  the 1984 scale: 20-18-16-15 down to 1.
- Fact check: de.wikipedia DTM-Saison 1984 to 1991, 2000 to 2003, 2007
  (Lausitz half points), 2020 to 2024. en.wikipedia 2018 (wildcards don't
  score). 1984: de.wikipedia says guests could not score, but Swiss driver
  Walter Brun has points, so the "German drivers only" rule is unclear.

## Discord post

=== post | DTM points history | dtm-points
## DTM points systems, 1984 to 2026

Part four of the DTM rules history. The table is below. What stood out to me:

- **Guest starters scored nothing in 1984.** They dropped out of the points order. In 1987 a guest won a race and scored nothing.
- **Drop results until 1989:** two, then one, then four.
- **Half points per heat** at some 1984 and 1985 rounds, half points at Lausitz 2007, and half points for a race stopped before 75% since 2023.
- **Points for qualifying:** 3-2-1 in the qualifying race (2001, 2002), and 3-2-1 for the top 3 in qualifying since 2017.
- **Fastest lap point** only for a top-10 finisher (2022).
- **Other titles:** teams, manufacturers from the best car, best 3 or best 4 cars, privateers, a Class 2 cup, rookies. 2020: a three-car team scores from its best two.
- **Top 15 score** since 2023 (25-20-16 down to 1).

For the game this means points tables per session (race, qualifying, qualifying race), drop results, rules for half points, non-scoring guests, and extra titles with a "best N cars" rule. Most of this is in my earlier points post for F1 too.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
