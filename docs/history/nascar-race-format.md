# NASCAR Cup race format, qualifying and cautions, 1949 to 2026

Part of the NASCAR rules history (points and playoffs, race format and
cautions, cars and entries). The table image is made with
`python -I tools/history_table.py docs/history/nascar-race-format.md`.

`(?)` marks a detail that the sources we read did not confirm. The sources
had little on qualifying outside the Daytona 500.

## Table

| Years | Race | Qualifying and grid | Cautions and restarts | Quirks |
|---|---|---|---|---|
| 1949 to 1958 | Laps or miles, ovals of every size, some road and beach courses. | Timed laps, one car at a time (?). | Cars race back to the line when the yellow comes out (?). | 1954: first road course, Linden Airport. |
| 1959 to 2002 | Daytona 500 from 1959. Coca-Cola 600 the longest race. | Daytona: front row from timed laps, the rest from two Duel races (100 miles, 125 from 1969). | A race can finish under yellow. | 1974: Daytona 500 cut to 450 miles in the oil crisis. From 1963 at least one road course a year. |
| 2003 to 2008 | Same. | Daytona Duels 150 miles from 2005. Top 35 in owner points locked in (2005 to 2012). | Late 2003: no racing back to the line under yellow, the first lapped car gets a lap back (free pass, "lucky dog"). From 2004: green-white-checker, one attempt. | The free pass came after Mears nearly hit a stalled car while racing back to the line. |
| 2009 to 2016 | Same. | From 2013: 36 by speed, 6 by owner points, 1 for a past champion. 2016: 40 cars, 36 charters. | Double-file restarts from June 2009, free pass for the whole race, wave-around for lapped cars. From 2010 up to three green-white-checker tries. 2016: an overtime line. | |
| 2017 to 2023 | Three stages (four at the 600), each of the first two ends under caution. | Group and knockout qualifying in the 2010s, grids by formula in 2020 and 2021 (?). | Overtime with unlimited tries from August 2017. | Stage cautions became part of the race. |
| 2024 to 2026 | Same. 30 ovals and 6 road courses (2025). | Group qualifying with a final round (?). | Overtime: a one-lap restart if two laps remain after the time limit (2024). | Rain tyres on road courses since 2020. |

## Daytona 500 grid

| Places | How |
|---|---|
| 1 and 2 | timed laps on Wednesday (since 2021) |
| 3 to 39 | the two Duel races on Thursday, top 35 in owner points (later charters) safe |
| 40 to 43 | fastest times of those not yet in, one for a past champion |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta, as an oval pack. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Rolling start, double-file restarts | Yes | `oval_start_procedure` double_file_pace_lap, oval restarts |
| Stages ending under caution | Yes | `oval_stage_racing`, `caution_at_stage_end` |
| Free pass (lucky dog), wave-around | Yes | `oval_lucky_lapper`, wave-around built in |
| Green-white-checker, overtime | Partly | `oval_green_white_checkered`, number of tries and overtime line not set |
| Finish under yellow or race back | Yes | `oval_last_lap_caution` |
| Single-car qualifying | Partly | oval qualifying: 4 hot laps, several cars on track in live play |
| Duel races for the Daytona grid | No | A2 |
| Group and knockout qualifying, grid by formula | No | A6 |
| Grid places by owner points or charters | Yes | `oval_charter_system`, `oval_grid_limit` |

## Sources

- Wikipedia, "NASCAR Cup Series" (stages, owner points grid rules,
  charters, road courses, rain tyres, free pass history), "Daytona 500"
  (qualifying procedure, Duels, distances), "Green–white–checker finish"
  (attempts and overtime by year), "Free pass (NASCAR)" (free pass,
  wave-around, double-file restarts 2009).
- Game support from the 0.99.6 oval code (start procedure, stage racing,
  lucky lapper, green-white-checker, last-lap caution, oval qualifying,
  charters).
- Not confirmed, marked `(?)`: early qualifying and caution rules, group
  qualifying years, 2020 and 2021 grids, the current qualifying format.
- Conflict: the green-white-checker page also says unlimited tries began
  in 2016.

## Discord post

=== post | NASCAR race format history | nascar-race-format
## NASCAR Cup race format, qualifying and cautions, 1949 to 2026

Part two of the NASCAR rules history. The table is below. What stood out to me:

- **Racing back to the line under yellow** was allowed until late 2003. A near miss with a stalled car brought the free pass ("lucky dog").
- **Green-white-checker from 2004:** one try, then up to three (2010), an overtime line (2016), unlimited tries (2017).
- **Double-file restarts and the wave-around** from 2009.
- **Stages since 2017,** each of the first two ends under caution and pays points.
- **The Daytona 500 grid:** front row from timed laps, most of the field from two Duel races, the last places by speed and a past champion.
- **Who gets in:** top 35 in owner points (2005 to 2012), then charters (36 of 40 places from 2016).

The oval mode covers most of this already: rolling and double-file starts, stages, the lucky lapper, wave-arounds, green-white-checker and charters. The gaps are the Duel races and group or knockout qualifying.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
