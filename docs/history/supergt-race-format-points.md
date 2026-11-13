# Super GT race format, drivers and points, 1993 to 2026

Part of the Super GT rules history (classes and balancing, race format and
points). JGTC 1993 to 2004, Super GT from 2005. The table image is made
with `python -I tools/history_table.py docs/history/supergt-race-format-points.md`.

`(?)` marks a detail that the sources we read did not confirm. The sources
had little on race rules before 2005.

## Table

| Years | Races | Drivers and stops | Qualifying | Points |
|---|---|---|---|---|
| 1993 to 2005 | 300 km races, Fuji 500 km, Suzuka 1000 km (not for points until 2006). Sepang from 2000. | Two drivers per car (all races from 1996). One stop with a driver change, in a set pit window (2004). | 2005: new Super Lap, the top 12 of each class run alone on track. Format before 2005 not found (?). | Per class, top 10. 2000: 20-15-12-10-8-6-4-3-2-1. By 2005 also points for the top 3 in qualifying and for fastest laps. |
| 2006 to 2012 | Plus Suzuka 1000 km for points. Distances cut in 2009 and 2011, back in 2012. | Same. A third driver may join at the long races (Fuji 500 km, Suzuka 1000 km). | Super Lap for the top 10. Knockout tried in 2007, used at some races from 2010. | 2008: 20-15-11-8-6-5-4-3-2-1, qualifying 3-2-1. 2012: Suzuka 25-18-13-10-8-6-5-4-3-2. |
| 2013 to 2021 | 250 to 300 km, Suzuka 1000 km to 2017, Fuji 500 miles (805 km) in 2018 and 2019. Buriram from 2014. | One stop at 300 km races. No driver may drive more than two thirds of the distance. | Knockout from 2013, Q1 and Q2 with a different driver each. | 20-15-11-8-6-5-4-3-2-1, Suzuka 1000 km 25-18-13 (2014). |
| 2022 to 2023 | Some races 450 km. | Two compulsory stops at 450 km races. | Knockout. | |
| 2024 to 2026 | 300 and 350 km (250 km at Motegi in 2026), and races of three hours. | One stop at 300 km. Tyre sets: 4 for 300 km, 5 for 350 km, 6 for three hours. | Both drivers' times added up. One set for Q1 and Q2, the race starts on it. Missing 107% means the pit lane. | Qualifying: top 3 per class 3-2-1. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Two drivers per car, driver change at the stop | No | C8 |
| Mandatory stops | No | B5 |
| Three-hour races | No | A3 |
| Races by distance | Yes | laps per track |
| Both drivers' qualifying times added up | No | A6 |
| Start on the qualifying tyres | No | B12 |
| Tyre sets per race | Yes | `weekend_tyre_allocation` |
| 107% rule | Yes | `config.json` `quali_107_rule` |
| Qualifying points 3-2-1 | Partly | pole point only (B8) |
| Different points for the long race | No | B3 |
| Titles per class | No | B4 |

## Sources

- Wikipedia, "Super GT" (race lengths, stops, the two-thirds rule),
  "All Japan Grand Touring Car Championship", 2014, 2024 and 2026 Super GT
  season articles (calendars, 2024 qualifying rules and points, tyre sets).
- Wikipedia, "2013 Fuji GT 300km" (separate Q1 and Q2 drivers), 2026
  Super GT season (250 km Motegi rounds).
- Wikipedia, "1996 All Japan Grand Touring Car Championship" (two drivers
  at all races from 1996), "Super GT" (two-thirds rule, pit windows in
  2004, Super Lap replaced in 2013), 2000, 2005, 2008 and 2012 season
  articles (points scales, third drivers in 2012). Japanese Wikipedia
  "SUPER GT" (two-thirds rule, Super Lap to 2012, knockout tried in 2007
  and used from 2010, top 10 score, third drivers need 120 km for points).
- WebCG and Honda race report, 2005 Okayama (Super Lap new in 2005, 12
  cars per class). Motorsport.com qualifying reports 2008 and 2010 (Super
  Lap for the top 10).
- Honda, SUPER GT 2005 round 1 report (Super Lap new, top 10 plus 2 per
  class). Wikipedia "2006 Super GT Series" and "Suzuka 1000km" (1000 km
  race in the championship from 2006). Wikipedia "2011 Super GT Series"
  (shorter races after the earthquake), "Suzuka 1000km" (700 km in 2009
  and 2010, 1000 km again in 2012), "2018 Super GT Series" (Fuji 500 miles
  2018 and 2019).
- Not found, marked `(?)`: qualifying before 2005. The start year of the
  two-thirds rule.
- Not found: rolling start, safety car and full-course yellow rules.

## Discord post

=== post | Super GT race format history | supergt-race-format-points
## Super GT race format, drivers and points, 1993 to 2026

Part two and the last of the Super GT rules history. The sources were thin on race rules before 2005. What stood out to me:

- **Two drivers per car,** a driver change at the compulsory stop, and nobody may drive more than two thirds.
- **Long races:** Suzuka 1000 km, Fuji 500 miles (2018, 2019), 450 km with two stops (2022), and three-hour races since 2024.
- **Qualifying since 2024:** both drivers run, their times are added up, and the car starts the race on the tyres it qualified on.
- **Tyre sets by race length:** 4 for 300 km, 5 for 350 km, 6 for three hours.
- **Points per class,** with more for the 1000 km race, and 3-2-1 for qualifying.

For the game this is the entry model again: two drivers on one car, drive-time rules, a driver change at the stop. Plus qualifying where both drivers count.

The last table in the picture shows what the game can do today: yes, partly or no.

That's the Super GT series. Mistakes? Tell me!
