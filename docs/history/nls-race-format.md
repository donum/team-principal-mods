# NLS race format, drivers and safety, 1977 to 2026

Part of the NLS rules history (classes and points, race format). The table
image is made with `python -I tools/history_table.py docs/history/nls-race-format.md`.

`(?)` marks a detail that the sources we read did not confirm. The sources
had no pit stop or qualifying rules.

## Table

| Years | Races | Start and drivers | Safety | Quirks |
|---|---|---|---|---|
| 1977 to 1992 | Races of 3.5 to 6 hours, a 250-mile race. One day, on Saturday. | One to three drivers per car (?). | | A marshal died in 1977. |
| 1993 to 2014 | Mostly 4 hours, one 6-hour race from 1993. Ten races until 2016. Nordschleife plus the GP track's short loop, 24.358 km. | Three start groups a few minutes apart after a warm-up lap behind safety cars. 4-hour races: one driver alone or up to three. 6-hour race: two to four. | Double yellow: 60 km/h. No safety car in the race. Code 60 flag added in 2014. | 1998: Jack Brabham raced aged 72. |
| 2015 to 2019 | Ten races to 2016, then nine, eight of 4 hours. | Same. From 2015 drivers need the DMSB Permit Nordschleife, grade A or B by class. | Code 60: 60 km/h in a zone. Double yellow 120 km/h from 2016. 2015: after a GT3 car flew over the fence and killed a spectator, speed limits at three places, lifted in 2016. | |
| 2020 to 2026 | Renamed NLS. 2024: eight races, 2025: ten, including the 24-hour qualifiers and NLS Light. Qualifying 08:30, race at 12:00. | Same. | Code 60 and double yellow. | 2026: a driver died after an oil trail caused a multi-car crash. Special races with red wigs (NLS-6) and ham prizes (NLS-9). |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| 4 and 6-hour races | No | A3 |
| Start in three groups | No | A3 |
| One to four drivers per car | No | C8 |
| Code 60 zones, double yellow at 120 km/h | Partly | local yellows and VSC (B11) |
| Licence by class | Partly | `driverslicense.json` for race seats only |
| Long tracks with a GP loop | Yes | track files |

## Sources

- Wikipedia (English and German), "Nürburgring Langstrecken-Serie"
  (lengths, start groups, drivers per car, Code 60, safety history,
  quirks), "24 Hours of Nürburgring" (2015 speed limits, the permit).
- Not found: pit stop rules, qualifying format, BoP rules. The NLS website
  is the next place to check.
- VLN/NLS website (2014, 2015) and DMSB (December 2015): the permit is
  needed in VLN from 2015, in grades A and B.
- German Wikipedia: ten races until 2016, then nine.
- VLN website, March 2016 (double yellow 120 km/h instead of 60 km/h,
  Code 60 flag since 2014) and March 2015 (permit grades A and B from
  2015). Motorsport.com and Autoblog (2015 speed limits, lifted March 2016).
- Not confirmed, marked `(?)`: drivers per car before 1993.

## Discord post

=== post | NLS race format history | nls-race-format
## NLS race format, drivers and safety, 1977 to 2026

Part two and the last of the NLS rules history. The table is below. What stood out to me:

- **One-day races on Saturdays,** mostly 4 hours, one 6-hour race, on the Nordschleife plus the GP track's short loop.
- **Three start groups** a few minutes apart, so 100+ cars fit on the road.
- **One driver can race alone for 4 hours,** or two to four share a car.
- **Code 60 and slow zones instead of a safety car:** 60 km/h in the zone, 120 km/h under double yellow.
- **A licence for the track:** the DMSB Permit Nordschleife, level A or B by class.

For the game: time-based races, staggered starts, crews and local slow zones. All of these are in the earlier endurance posts, so the NLS adds no new kind of rule, only more of them at once.

The last table in the picture shows what the game can do today: yes, partly or no.

That's the NLS series. Mistakes? Tell me!
