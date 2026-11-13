# American open-wheel qualifying and race format, 1979 to 2026

Part of the IndyCar rules history (points, qualifying and race, pit stops
fuel and tyres, cars and engines). Covers CART (1979 to 2003), Champ Car
World Series (2004 to 2007) and IRL / IndyCar (1996 to 2026). The table
image is made with
`python -I tools/history_table.py docs/history/indycar-qualifying-race.md`.

`(?)` marks a detail that the sources we read did not confirm. The
sources were thin for the early years.

## Table

| Years | Road and street qualifying | Oval qualifying | Race | Quirks |
|---|---|---|---|---|
| 1979 to 1995 | Timed sessions, at some events in two groups (Miami 1985). Rules per year not found (?). | One car at a time. Michigan 1991: two timed laps. | Rolling start behind the pace car. Laps or miles. | 1979: CART splits from USAC. The Indy 500 stays with USAC. It pays CART points in 1979 and 1980, not in 1981 and 1982, and again from 1983. |
| 1996 to 2001 | CART: a provisional session on Friday, the final session on Saturday. | IRL: one car at a time, two timed laps, the faster one counts. | Rolling start. | 1996: the IRL starts, the Indy 500 reserves 25 of 33 places for IRL points leaders. |
| 2002 to 2003 | CART: qualifying in groups, a bonus point for the fastest in the slowest group. | | Rolling start. | |
| 2004 to 2007 | Champ Car: qualifying in groups. | Few ovals left. | Timed races (all races in 2007), standing starts where safe (2007). | Champ Car became almost all road and street races. |
| 2008 to 2021 | IndyCar: two groups, the top 6 of each go on, then a "Fast Six" for pole (from St. Petersburg 2008). | One car at a time, four laps averaged (2008), two laps averaged from Chicagoland 2010. | Rolling start. Double-file restarts from 2011 (at all tracks in 2011). | Texas 2011: two short races in one night. 2020: double-headers at Road America, Iowa, Gateway, Mid-Ohio and the Indianapolis road course. |
| 2022 to 2026 | Same. | Same. | Rolling start. No green-white-checker: a race can finish under yellow. | Indianapolis can call a late red flag to get a green finish (used 2014, 2019, 2022, 2023, 2026). |

## Indianapolis 500 qualifying

| Years | Format |
|---|---|
| Since 1939 | Four timed laps (10 miles) per run, 33 starters in 11 rows of three |
| 1979 to 2009 | Several days of qualifying, slower cars could be bumped from the 33 (bumping also in later formats) |
| 2010 to 2021 | Fast Nine shootout for pole (points for it from 2010) |
| 2022 on | Fast Twelve, then Fast Six for pole |
| 2019 on | Cars outside the top 30 run a last chance session for the last row |
| Rain | A race is official after more than half the distance (101 laps) |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| One car at a time on ovals | Partly | oval packs: 4 hot laps, but several cars on track in live play |
| Groups, then Fast Six on road courses | No | A6 |
| Indy 500 shootouts and bumping | No | A5, A6 |
| Rolling start | Partly | oval packs only (A3) |
| Double-file restarts, wave-around | Partly | oval packs only |
| Green-white-checker or late red flag | Partly | oval packs have green-white-checker |
| Two races in one weekend | No | A1 |

## Sources

- Wikipedia, "Indianapolis 500" (four laps, 33 cars, late red flags, no
  green-white-checker, rain rule), "Rolling start" (Indy triple-file, 2011
  double-file restarts), "Champ Car World Series" (timed races and standing
  starts, no years), "IndyCar Series" (2020 double-headers, via summary),
  "List of American Championship car racing points scoring systems"
  (CART groups 2002 to 2003, Indy Fast Nine and top 12 years, Texas 2011).
- Fact check: Racecar.com and Eurosport 2008 (knockout format from St.
  Petersburg 2008; a single-car Fast Six existed from 2005 or 2006),
  motorsport.com and AP 2011 to 2012 (double-file restarts at all venues
  in 2011, dropped at Indianapolis, Texas and Fontana for 2012), 2007 Champ
  Car season article (all races timed, standing starts where safe), 1979
  SCCA/CART season article (Indy 500 paid CART points in 1979 and 1983),
  2026 Indy 500 reports (late red flag), Champ Car points bonus for the
  slowest qualifying group (groups 2004 to 2007).
- Open items check: 1980 and 1981 Indianapolis 500 articles (CART points
  in 1980, an invitational race without CART points in 1981 and 1982),
  The Auto Channel 1999 (Mid-Ohio provisional pole on Friday, final
  qualifying on Saturday), 1985 Beatrice Indy Challenge article (two
  qualifying groups), 1991 Michigan 500 article (two qualifying laps),
  motorsport.com, ESPN and Crash.net 1999 to 2002 (IRL pole on one lap,
  "the first of two allowed laps"), 2006 Kansas Lottery Indy 300 article
  (faster of two laps), Autosport 2010 (four laps averaged since 2008, two
  from Chicagoland 2010), IndyCar rulebook 2026 (two laps, the total
  counts), PlanetF1 and Sportskeeda (two-lap average).
- Confirmation round: 1981, 1982 and 1983 CART season articles (Indy 500
  non-championship in 1981 and 1982, CART points again in 1983), Autosport
  2010 Chicagoland (two-lap average), IndyCar.com, RACER and The Checkered
  Flag 2019 (Last Row Shootout), NBC Sports and the 1996 Indianapolis 500
  article (25/8 rule), "Indianapolis 500" (four laps since 1939, late red
  flags, 101 laps).
- Not confirmed, marked `(?)`: CART road course qualifying rules before
  1999.

## Discord post

=== post | IndyCar qualifying and race history | indycar-qualifying-race
## IndyCar qualifying and race format, 1979 to 2026

Part two of the IndyCar rules history. The sources were thin for the early years. What stood out to me:

- **Road courses:** qualifying in groups, then the top 6 of each group go on, then a "Fast Six" for pole.
- **Ovals:** one car at a time on track, over two laps (four laps averaged 2008 to 2010). At Indianapolis four laps, and the 33 fastest start.
- **Indy 500 qualifying** changed a lot: bumping slower cars out over several days, a Fast Nine (2010 to 2021), now a Fast Twelve and Fast Six, with points for it.
- **Rolling starts,** three abreast at Indianapolis. Champ Car tried standing starts and timed races.
- **No green-white-checker:** a race can end under yellow, so Indianapolis sometimes uses a late red flag to get a green finish.
- **Two races in one weekend or night:** Texas 2011, double-headers in 2020.

For the game: single-car qualifying on ovals (the oval mode has this), groups plus knockout on road courses, a shootout at one special event, and race control rules like "red flag near the end instead of finishing under yellow". All of this fits the weekend builder idea.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
