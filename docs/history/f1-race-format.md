# F1 race format and starts, 1950 to 2026

Part of a series on how F1 rules changed (qualifying, points, tyres, pit
stops, race format). Each file has the table, the sources and a Discord
post. The table image is made with
`python -I tools/history_table.py docs/history/f1-race-format.md`.

`(?)` marks a detail that the sources we read did not confirm. Check it
before you rely on it.

## Table

| Years | Distance and time | Start | Stopped races | Quirks |
|---|---|---|---|---|
| 1950 to 1957 | More than 300 km or 3 hours. | Standing start, a flag is dropped (?). Grids of 4-3-4 or 3-2-3 cars per row, set per track. | Rare. | The Indianapolis 500 counts until 1960: 500 miles with a rolling start. Races of 3 hours mean drivers share cars. |
| 1958 to 1965 | 300 to 500 km or 2 hours. | Flag start. Wide rows of three or four. | | Races get shorter, so cars no longer need a driver change. |
| 1966 to 1980 | 300 to 400 km from 1966. At most 322 km from 1971. 322 km or 2 hours (1973 to 1980). | Start lights replace the flag in the 1970s (?). Grid two by two, staggered, from the mid 1970s (?). Formation lap from the 1970s (?). | Stopped race restarted, result on the total time of both parts (?). | Japan 1976: the title was decided in heavy rain, Lauda stopped on his own. |
| 1981 to 1988 | 250 to 320 km or 2 hours (1981 to 1984). At least 300 km from 1984. | Red light, then green. | Aggregate time of both parts. | Canada 1982: Paletti was killed hitting a stalled car at the start. South Africa 1985: the last race not on a Sunday, until Las Vegas 2023. |
| 1989 to 2010 | 305 km, or 2 hours at most. Monaco about 260 km. | Grid two by two. Five red lights that go out together (start year (?)). | Aggregate of both parts into the 1990s (last: Japan 1994 (?)). From 2005: restart behind the safety car, order when stopped. Under 75% of the distance: half points. | Australia 1991: 14 laps in rain, half points, the shortest race. 1997 on: some wet races start behind the safety car. Singapore 2008: first night race. |
| 2011 to 2020 | 305 km, 2 hours. Red flag time stops the clock, at most 4 hours in total (2012 to 2020). | Wet start behind the safety car, then a standing start once it is dry enough (from 2017). Aborted start: back to the 5-minute point, one lap less. | Restart behind the safety car. Standing restarts in the rules from mid 2018, first used at Monza 2020. | China 2014: the chequered flag came a lap early, the result was taken a lap earlier. |
| 2021 | Same. | Same. | Spa 2021: two laps behind the safety car, then red flag. Result after one lap, half points. | No racing lap, but a result. The 3-hour limit (from 2021) was stopped. |
| 2022 to 2026 | Same. | Same. Starting on wet or intermediate tyres means no mandatory stop. | Shortened races get a points scale in four steps, no points without two green laps. | São Paulo 2024: Norris mistook an aborted start for an extra formation lap. Austria 2025: Sainz's car caught fire, start delayed 15 minutes. |
| 2027 | The 3-hour clock is replaced by a hard stop for racing (announced). | | | |

## How a start works today

| Time | What happens |
|---|---|
| 40 min | Pit lane opens. Cars do laps to the grid through the pit lane. |
| 30 min | Pit lane closes. A car not on the grid starts from the pit lane. |
| 10 min | Only drivers, mechanics and marshals stay on the grid. |
| 5 min | Wheels must be on, otherwise a stop-go penalty. |
| 1 min | Engines on. At 15 seconds everyone leaves the grid. |
| 0 | Green lights: formation lap, no overtaking. |
| Start | Five pairs of red lights come on one by one, then all go out together after a random wait. |
| Problem | A driver who cannot go raises a hand: another formation lap, one lap less. |

## Rules across all years

- Today a driver must finish 90% of the winner's distance to be classified.
- Race distance: the fewest laps that are more than 305 km (Monaco 260 km).
  If the 2 hours are up, the leader finishes the lap and the race ends.

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Race length in laps | Yes | `laps` x `lap_modifier` per track |
| Time limit (2 hours) | No | A3 |
| Standing start, two by two | Yes | built in |
| Rolling start | No | oval packs only (A3) |
| Red flag and restart | Partly | `formula_red_flags`: up to 2, free tyre change, standing restart, no aggregate, not in simulated races (A3) |
| Half points or a scale for short races | No | B3 |
| Classification rules (90% distance) | Yes | built in: 90% of the winner's laps |
| Race distance per era (500 km, 305 km) | Partly | laps per track by hand |

## Sources

- Wikipedia, "Formula One race weekend" (race distance, time limit, start
  procedure, red flag clock, 2027 change, Saturday race 1985), "Formula One
  regulations" (start lights, aborted start, wet start, classification),
  "Rolling start" (wet starts behind the safety car since 1997), "Parade
  lap" (2024 and 2025 quirks), "Standing start" (Paletti 1982).
- Fact check: Wikipedia "List of Formula One Grands Prix" (distances 1950
  to 1989, 4 hours 2012 to 2020, 3 hours from 2021), "History of Formula
  One regulations" (4-hour cap from 2012), "2005 Formula One World
  Championship" (restart behind the safety car), "2021 Belgian Grand Prix",
  "Parade lap" (2024, 2025). racefans.net (standing restarts in the rules
  mid 2018, first used Monza 2020). Wet standing starts from 2017: racer.com,
  motorsport.com. Aggregate: 1981 and 1992 France, Japan 1994 (blog only).
- Not confirmed, marked `(?)`: flag starts, when two by two started, when
  the formation lap and five red lights came, the last aggregate race.
- Open conflict: "Formula One race weekend" says 4 hours "until 2011", the
  other two pages say from 2012.
- Open conflict: the random wait before lights out, 0.2 to 3 s or 4 to 7 s.

## Discord post

=== post | F1 race format history | f1-race-format
## F1 race format and starts, 1950 to 2026

Part five of the rules history (after qualifying, points, tyres and pit stops). The table is below. What stood out to me:

- **Races were long.** Over 300 km or 3 hours in the 1950s, so drivers shared cars. Since 1989 it's 305 km or 2 hours, Monaco 260 km.
- **The start changed a lot:** a dropped flag, rows of four cars, then lights and a grid of two by two. The Indianapolis 500 had a rolling start.
- **Stopped races** were once added up over both parts. Today the race restarts from the order when it was stopped, and the clock stops under red.
- **Wet races** can start behind the safety car, then switch to a standing start.
- **Short races:** Australia 1991 was 14 laps. Spa 2021 had no racing lap and still had a result.
- **The start procedure** is a fixed countdown: 40 minutes, 30, 10, 5, 1, formation lap, lights.

For the game this is: race length in km, laps or time, whatever comes first. Start type (standing, rolling, behind the safety car). What happens after a red flag (restart order, aggregate, clock). A minimum distance to be classified. The same settings cover DTM: rolling starts in 2000, 2001 and from 2021, races of minutes plus one lap, and the 1986 Zolder aggregate.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
