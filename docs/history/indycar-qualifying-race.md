# American open-wheel qualifying and race format, 1979 to 2026

Part of the IndyCar rules history (points, qualifying and race, pit stops
fuel and tyres, cars and engines). Covers CART (1979 to 2003), Champ Car
World Series (2004 to 2007) and IRL / IndyCar (1996 to 2026). The table
image is made with
`python -I tools/history_table.py docs/history/indycar-qualifying-race.md`.

`(?)` marks a detail that the sources we read did not confirm. The
sources were thin for this topic, so many rows are marked.

## Table

| Years | Road and street qualifying | Oval qualifying | Race | Quirks |
|---|---|---|---|---|
| 1979 to 1995 | Timed sessions on Friday and Saturday (?). | One car at a time, a few timed laps (?). | Rolling start behind the pace car. Laps or miles. | 1979: CART splits from USAC. The Indy 500 stays with USAC but pays CART points (1983 on). |
| 1996 to 2001 | Same (?). | One car at a time (?). | Rolling start. | 1996: the IRL starts, the Indy 500 reserves 25 of 33 places for IRL points leaders. |
| 2002 to 2003 | CART: qualifying in groups, a bonus point for the fastest in the slowest group. | | Rolling start. | |
| 2004 to 2007 | Champ Car: qualifying in groups (?). | Few ovals left. | Some timed races (?), standing starts tried (2007 ?). | Champ Car became almost all road and street races. |
| 2008 to 2021 | IndyCar: two groups, the top 6 of each go on, then a "Fast Six" for pole (?). | One car at a time, two laps averaged (?). | Rolling start. Double-file restarts on short ovals (2011). | Texas 2011: two short races in one night. 2020: double-headers at Road America, Iowa, Mid-Ohio and Gateway. |
| 2022 to 2026 | Same. | Same. | Rolling start. No green-white-checker: a race can finish under yellow. | Indianapolis can call a late red flag to get a green finish (used 2014, 2019, 2022, 2023, 2026). |

## Indianapolis 500 qualifying

| Years | Format |
|---|---|
| Since 1939 (?) | Four timed laps (10 miles) per run, 33 starters in 11 rows of three |
| 1979 to 2009 | Several days of qualifying, slower cars could be bumped from the 33 (?) |
| 2010 to 2021 | Fast Nine shootout for pole (points for it from 2010) |
| 2022 on | Fast Twelve, then Fast Six for pole |
| 2019 on | Cars outside the 33 run a last chance session (?) |
| Rain | A race is official after more than half the distance (101 laps) |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| One car at a time on ovals | Partly | oval mode qualifying |
| Groups, then Fast Six on road courses | No | A6 |
| Indy 500 shootouts and bumping | No | A5, A6 |
| Rolling start | Partly | oval mode only (A3) |
| Double-file restarts, wave-around | Partly | oval mode only |
| Green-white-checker or late red flag | Partly | oval mode has green-white-checker |
| Two races in one weekend | No | A1 |

## Sources

- Wikipedia, "Indianapolis 500" (four laps, 33 cars, late red flags, no
  green-white-checker, rain rule), "Rolling start" (Indy triple-file, 2011
  double-file restarts), "Champ Car World Series" (timed races and standing
  starts, no years), "IndyCar Series" (2020 double-headers, via summary),
  "List of American Championship car racing points scoring systems"
  (CART groups 2002 to 2003, Indy Fast Nine and top 12 years, Texas 2011).
- Not confirmed, marked `(?)`: road course qualifying before 2002 and the
  start year of the Fast Six, oval run lengths, Champ Car timed races and
  standing start years, bumping years, last chance qualifying.

## Discord post

=== post | IndyCar qualifying and race history | indycar-qualifying-race
## IndyCar qualifying and race format, 1979 to 2026

Part two of the IndyCar rules history. The sources were thin here, so more is marked (?) than usual. What stood out to me:

- **Road courses:** qualifying in groups, then the top 6 of each group go on, then a "Fast Six" for pole.
- **Ovals:** one car at a time on track, averaged over a few laps. At Indianapolis four laps, and the 33 fastest start.
- **Indy 500 qualifying** changed a lot: bumping slower cars out over several days, a Fast Nine (2010 to 2021), now a Fast Twelve and Fast Six, with points for it.
- **Rolling starts,** three abreast at Indianapolis. Champ Car tried standing starts and timed races.
- **No green-white-checker:** a race can end under yellow, so Indianapolis sometimes uses a late red flag to get a green finish.
- **Two races in one weekend or night:** Texas 2011, double-headers in 2020.

For the game: single-car qualifying on ovals (the oval mode has this), groups plus knockout on road courses, a shootout at one special event, and race control rules like "red flag near the end instead of finishing under yellow". All of this fits the weekend builder idea.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
