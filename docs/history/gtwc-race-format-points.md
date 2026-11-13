# GT World Challenge race format and points, 1997 to 2026

Part of the GT World Challenge rules history (classes and balancing, race
format and points). The table image is made with
`python -I tools/history_table.py docs/history/gtwc-race-format-points.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Races | Drivers and stops | Qualifying | Points and titles |
|---|---|---|---|---|
| 1997 to 2006 | At least 500 km or at most 3 hours, plus the Spa 24 Hours, Istanbul 2 hours, Mil Milhas. | Driver changes (?). | Not stated (?). | Per class (?). |
| 2007 to 2009 | At most 2 hours, plus Spa 24 Hours. | Same (?). | Not stated (?). | Per class (?). |
| 2010 to 2012 | Two one-hour races per weekend: a qualifying race and a main race. | Each car must change tyres and drivers at least once. | Three-part knockout. | Top 3 of the qualifying race and top 10 of the main race score. |
| 2013 to 2019 | Endurance: 3 or 6 hours, Spa 24 Hours. Sprint: two one-hour races per weekend. | Endurance: three drivers, a fourth at Spa for non-Pro cars. Sprint: two drivers, a driver change in a set window. | From 2018: three parts, one per driver, the times added up. | Sprint and Endurance points add up to the overall titles. Spa pays the most, with points during the race. |
| 2020 to 2026 | Same, five Endurance and five Sprint rounds. | Same. Pro cars at most three drivers at Spa. | 2025: split qualifying groups for the Sprint Cup, 2026 for the Endurance Cup. | Overall, Sprint and Endurance titles, cups per class. Points at the 6 and 12-hour marks at Spa (?). |

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
  "24 Hours of Spa".
- Not found: points scales, minimum drive times, minimum pit stop times.
- Not confirmed, marked `(?)`: FIA GT driver change rules and points, the
  Spa 6-hour points mark.

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
