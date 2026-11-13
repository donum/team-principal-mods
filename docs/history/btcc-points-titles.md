# BTCC points and titles, 1958 to 2026

Part of the BTCC rules history (weekend format, points and titles, cars
classes and balancing). The table image is made with
`python -I tools/history_table.py docs/history/btcc-points-titles.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Race points | Bonus points | Titles | Quirks |
|---|---|---|---|---|
| 1958 to 1990 | By class: classes by engine size race together, the overall champion comes from class points (?). | | Drivers. | A small-class car could win the title without ever winning a race outright: Hodgetts (Toyota Corolla) 1986 and 1987, Cleland (Vauxhall Astra, small class) 1989. |
| 1991 | One class from 1991. Scale not stated (?). | | Drivers, manufacturers (start year (?)). | |
| 1992 to 1995 | 24-18-12-10-8-6-4-3-2-1, top 10 (1993 to 1994 (?)). | None found (?). | Independents' drivers' title from 1992. Teams' title from 1995 (?). | 1992: half points at double-header meetings. |
| 1996 to 1999 | 15-12-10-8-6-5-4-3-2-1, top 10. | Pole 1. 1998: also leading a lap in the feature race 1. | Teams' title. | |
| 2000 | 15-12-10-8-6-5-4-3-2-1, top 10. | Pole 1, fastest lap 1, leading a lap in the feature race 1. | Plus a Production (Class B) title, 2000 to 2003. | Best 20 of 24 results count. |
| 2001 to 2011 | 15-12-10-8-6-5-4-3-2-1, top 10. | Pole 1 (race 1 only from 2004), fastest lap 1, leading a lap 1, at most one per race. | Independent teams' title from 2005. | 2001: separate points per class, dropped for 2002 as too confusing. 2005: Team Dynamics won as an independent and was then counted as neither works nor independent until 2009. From 2007 BTC-T cars can't win the title outright. |
| 2012 to 2026 | 20-17-15-13-11-10-9-8-7-6-5-4-3-2-1, top 15, each of the three races. | Pole, fastest lap and leading a lap, 1 point each, at most one lead-lap point per race. | Five titles: drivers, independent drivers, teams, manufacturers, independent teams. Jack Sears Trophy from 2013. | Jack Sears Trophy: best S2000 driver (2013), most places gained (2014), best rookie (from 2015), anyone without a podium (2018). 2026: a Saturday qualifying race pays 10-9-8-7-6-5-5-4-4-3-3-2-2-1-1, drivers' title only. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Points down to 15th | Yes | `points_system`, any length |
| Pole and fastest lap points | Yes | `pole_point`, `fastest_lap_point` |
| Leading a lap point | No | B8 |
| Independents' titles | No | B4 |
| Teams' and manufacturers' titles | Partly | one constructors' title |
| Results per class | No | B4 |
| Drop results | No | B3 |

## Sources

- Wikipedia, "British Touring Car Championship" (current and previous
  points scale, bonuses, five titles, Jack Sears Trophy, class-title
  examples), "List of BTCC champions" (every champion by year, titles
  per year), 2000, 2001 and 2004 season articles (points, dropped
  results, class points 2001).
- Fact check: 1992, 1995, 1996, 1997 and 1998 season articles (24-point
  scale with half points at double-headers in 1992, the same scale in
  1995, the 15-point scale with a pole point from 1996, the lead-lap point
  in 1998), Touring Car Times and btcc.net
  2025 (2026 qualifying race points).
- Not confirmed, marked `(?)`: how class points worked before 1991, the
  1991, 1993 and 1994 scales, the start years of the manufacturers' and
  teams' titles.

## Discord post

=== post | BTCC points and titles history | btcc-points-titles
## BTCC points and titles, 1958 to 2026

Part two of the BTCC rules history. The table is below. What stood out to me:

- **Until 1990 classes by engine size raced together,** and a small-class car could win the title without ever winning a race outright (Hodgetts 1986 and 1987, Cleland 1989).
- **Bonus points for pole, fastest lap and leading a lap,** at most one lead-lap point per race.
- **The scale changed:** 24 points for a win in the early 1990s, 15 from 1996, 20 since 2012.
- **The top 15 score** in every one of the three races since 2012 (20 down to 1).
- **Five titles each year:** drivers, independent drivers (since 1992), teams, manufacturers, independent teams (since 2005).
- **The Jack Sears Trophy** changed its meaning: best S2000 driver, then most places gained, then best rookie.
- **2005:** an independent team won the title and was then counted as neither works nor independent for four years.

For the game this is: results per class that add up to one overall title, bonus points, extra titles for independents and rookies, and rules for who counts as independent. Most of it is in my DTM and IndyCar posts too, so it's the same handful of settings again.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
