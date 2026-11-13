# GT World Challenge race format and points, 1997 to 2026

Part of the GT World Challenge rules history (classes and balancing, race
format and points). The table image is made with
`python -I tools/history_table.py docs/history/gtwc-race-format-points.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Races | Drivers and stops | Qualifying | Points and titles |
|---|---|---|---|---|
| 1997 to 2006 | At least 500 km or at most 3 hours, plus the Spa 24 Hours and a 2-hour race at Istanbul. | Two or three drivers, four at Spa. A driver may drive at most 55% of the distance (2002). | 2002: a 45-minute session, then a Superpole for the six fastest of each class. | Per class, top 6 score (top 8 from 2003). Spa: points also at 6 and 12 hours (2002 to 2008). |
| 2007 to 2009 | At most 2 hours, plus Spa 24 Hours. | Two or three drivers. Two stops, each with a driver change, at least 35 minutes per driver (2007). | 2007: one 15-minute session per class group. | Per class, top 8. |
| 2010 to 2012 | Two one-hour races per weekend: a qualifying race and a main race. | Each car must change tyres and drivers at least once. | Three-part knockout. | Top 3 of the qualifying race and top 10 of the main race score. |
| 2013 to 2019 | Endurance: 3 or 6 hours, Spa 24 Hours. Sprint: two one-hour races per weekend. | Endurance: three drivers, a fourth at Spa for non-Pro cars. Sprint: two drivers, a driver change in a set window. | From 2018: three parts, one per driver, the times added up. | From 2014 Sprint and Endurance points add up to the overall titles. Spa pays the most, with points during the race. |
| 2020 to 2026 | Same, five Endurance and five Sprint rounds (four each in 2020). | Same. Pro cars at most three drivers at Spa. | 2025: split qualifying groups for the Sprint Cup, 2026 for the Endurance Cup. | Overall, Sprint and Endurance titles, cups per class. Points at the 6 and 12-hour marks at Spa. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Races of 3, 6 and 24 hours | No | A3 |
| Two races per weekend | No | A1 |
| Two to four drivers per car, driver change window | No | C8, B5 |
| Qualifying with each driver's time added up | No | A6 |
| Points during a race (Spa) | No | B3 |
| Several titles from two cups | No | B4 |

## Sources

- Wikipedia, "GT World Challenge Europe" (formats, drivers, qualifying,
  titles), "FIA GT Championship" (race lengths 1997 to 2009), "FIA GT1
  World Championship" (2010 to 2012 format), "Sprint Cup" (driver change),
  "24 Hours of Spa", "List of FIA GT Champions" (top 6, top 8 from 2003,
  Spa 6 and 12-hour points 2002 to 2008), 2020 GTWC Europe season and 2025
  Spa reports (points at 6, 12 and 24 hours).
- FIA GT Championship Sporting Regulations 2002 (drivers, 55% limit,
  qualifying and Superpole) and 2007 (drivers, two-hour races with two
  driver changes, qualifying). Autosport, 2002 (a Superpole pole).
  Wikipedia "2007 FIA GT Championship" (two-hour races, two mandatory
  stops).
- Wikipedia "2020 GT World Challenge Europe" (four rounds per cup, Spa
  points at 6 and 12 hours), "2025 GT World Challenge Europe Endurance
  Cup" (rounds and lengths). Racingsportscars and Motorsport.com, 2002
  (Superpole for the top six of each class).
- Not found: GTWC points scales, minimum drive times, minimum pit stop
  times.
- The Mil Milhas was announced as a 2007 FIA GT round but moved to the Le
  Mans Series (Wikipedia "2007 FIA GT Championship" and "2007 Mil Milhas
  Brasil").

## Discord post

=== post | GT World Challenge race format history | gtwc-race-format-points
## GT World Challenge race format and points, 1997 to 2026

Part two and the last of the GT World Challenge rules history. The sources had no points scales, so this is mostly formats. What stood out to me:

- **Two cups in one season:** Endurance (3 and 6 hours, the Spa 24 Hours) and Sprint (two one-hour races per weekend). Points from both make the overall title.
- **Sprint: two drivers and a driver change** in a set window.
- **Qualifying with every driver:** three parts, one per driver, the times added up (from 2018).
- **Spa pays the most,** with points during the race.
- **FIA GT1 (2010 to 2012):** a qualifying race and a main race, a tyre and driver change in each.

For the game this combines what the other series asked for: two races per weekend, crews with driver changes, time-based races, and points during a race.

The last table in the picture shows what the game can do today: yes, partly or no.

That's the GT World Challenge series. Mistakes? Tell me!
