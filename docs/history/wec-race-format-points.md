# Endurance race format and points, 1953 to 2026

Part of the endurance rules history (classes and BoP, drivers and pit
stops, race format and points). Covers the World Sportscar Championship
(1953 to 1992), Le Mans, and the FIA WEC (2012 to 2026). The table image
is made with
`python -I tools/history_table.py docs/history/wec-race-format-points.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Races | Start and qualifying | Finish and classification | Titles and points |
|---|---|---|---|---|
| 1953 to 1962 | Le Mans 24 h, Sebring 12 h, 1000 km races, Mille Miglia, Targa Florio, Carrera Panamericana. | Le Mans start: drivers run across the track to their cars. Cars lined up by engine size. | Le Mans: the most distance from the starting spot wins. | Manufacturers' title only. Points per place (?). |
| 1963 to 1969 | Same kinds of races. | Le Mans start, grid by qualifying times from 1963. | Same. | Titles per GT class and for prototypes. |
| 1969 to 1970 | | 1969: Ickx walked to his car in protest, strapped in, and still won. 1970: drivers already strapped in, engines started at the flag. | | |
| 1971 to 1981 | Le Mans not in the championship 1975 to 1979. | Rolling start behind the safety car. | From 1971: most distance at the end of the last lap, measured from the line. | Makes titles. Drivers' title from 1981. |
| 1982 to 1992 | Mostly 500 or 1000 km, about 3 or 6 hours. Le Mans out in 1989 and 1990. | Rolling start. | | Manufacturers to 1984, then teams from 1985. Drivers' title. |
| 1993 to 2011 | No world championship. Le Mans on its own, ILMC from 2010. | Pre-qualifying test day to 2000. Practice and qualifying Wednesday and Thursday. | | |
| 2012 to 2019 | WEC: 6-hour races, Le Mans 24 h, some 4 and 8 hours, Sebring 1000 miles (2019). All timed. | Qualifying with the times of two drivers averaged (?). | Classified: the car must finish the last lap within a set lap time, and cover 70% of the overall winner's distance. | Top 10 score on a scale (25 for a win (?)), 11th and lower half a point. Le Mans about double, 8 and 10 hours about 1.5 times. |
| 2014 to 2026 | | | Slow zones at Le Mans from 2014 (?). Safety cars, full-course yellow (?). | GTE drivers' and makes' titles from 2017. |
| 2020 to 2026 | Le Mans moved to September (2020) and August (2021). 2026: 8 rounds, Le Mans plus 6-hour races and Qatar 1812 km (2024, 2025). | Hyperpole: a top-class shootout for pole (from 2020 (?)). Pole is worth 1 point. | Points need 70% of the winner's distance and two laps under green (2021). | World titles for Hypercar drivers and makes, cups for the other classes. |

## Sources

- Wikipedia, "24 Hours of Le Mans" (Le Mans start, 1969, rolling start
  1971, classification before and after 1971, the 70% rule, schedule,
  dates), "World Sportscar Championship" (races, names, Le Mans in or out,
  titles by era, race lengths 1982 to 1992), "FIA World Endurance
  Championship" (races, points multipliers, half points, 2026 calendar),
  2012 and 2021 WEC season articles (timed races, 2021 pole point and
  green laps).
- Not confirmed, marked `(?)`: points per place before 2012 and the WEC
  scale, averaged qualifying times, Hyperpole year, slow zones, full-course
  yellow, safety car rules.

## Discord post

=== post | Endurance race format and points history | wec-race-format-points
## Endurance race format and points, 1953 to 2026

Part three and the last of the endurance rules history. The table is below. What stood out to me:

- **The Le Mans start** until 1969: drivers ran across the track to their cars. Ickx walked in protest in 1969 and still won. Rolling start since 1971.
- **Who wins:** until 1971 the most distance from your starting spot, since then from the line. To be classified you must finish the last lap inside a set lap time and cover 70% of the winner's distance.
- **Le Mans wasn't always in the championship:** out in 1956, 1975 to 1979 and 1989 to 1990.
- **Titles for makes first,** teams from 1985, drivers from 1981.
- **WEC points by race length:** about 1.5 times for 8 and 10 hours, double for Le Mans, half a point for 11th and lower.

For the game: races by time (6, 8, 10, 24 hours) or by distance (1000 km, 1812 km), a classification rule (last lap, distance share), points multiplied by race length, and results per class. The time-based race length is already in my weekend builder post, so endurance would fit the same system.

That's the endurance series. Mistakes? Tell me!
