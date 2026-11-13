# F1 safety car and red flags, 1950 to 2026

Part of a series on how F1 rules changed (qualifying, points, tyres, pit
stops, race format, safety car). Each file has the table, the sources and
a Discord post. The table image is made with
`python -I tools/history_table.py docs/history/f1-safety-car.md`.

`(?)` marks a detail that the sources we read did not confirm. Check it
before you rely on it.

## Table

| Years | Safety car | Lapped cars and restarts | VSC and red flag | Quirks |
|---|---|---|---|---|
| 1950 to 1972 | None. Yellow flags only: slow down, no overtaking at that spot. | | Red flag stops the race (?). | A crash is cleared while the race goes on. |
| 1973 to 1991 | Canada 1973: first safety car, a Porsche 914. Then only now and then, e.g. a Lamborghini Countach at Monaco 1981 to 1983. | | Red flag, restart, result on both parts added up (?). | Canada 1973: the safety car picked up the wrong car as leader. Part of the field lost a lap, and it took hours to find the winner. |
| 1992 to 1995 | Trials in France and Britain 1992. Official from 1993. A different car per season and track. | | | Imola 1994: the Opel Vectra was too slow to keep tyres warm and its brakes faded. Hungary 1995: the safety car hit Inoue, who was helping marshals (?). |
| 1996 to 2006 | Mercedes from 1996. Bernd Mayländer drives it from 2000. | Lapped cars stay where they are (?). | | The safety car bunches the field, a free gap for anyone who stops. |
| 2007 to 2008 | Pit lane closed as soon as the safety car comes out. Entering early: 10 s stop-go. Yellow light in the cockpit. | Lapped cars may move up a lap before the restart (?). | | Singapore 2008: Piquet crashed on purpose just after Alonso's early stop, to make a safety car help him. |
| 2009 | Pit lane open again. Software sets a minimum lap time to the pits, so nobody races in. | Same. | | Red light at pit exit while the safety car passes. Passing it once meant disqualification (Montoya 2005, Fisichella and Massa 2007). |
| 2010 to 2011 | Same. | Lapped cars may not unlap. | | Canada 2011: a red flag for rain made it the longest race, about 4 hours (?). |
| 2012 to 2014 | Same. | Lapped cars may unlap again. The safety car waits until they have caught up. | | Restarts take several laps. |
| 2015 to 2020 | Same. Mercedes AMG GT. | The safety car no longer waits for the lapped cars to catch up. | Virtual safety car from 2015, after Bianchi's crash at Suzuka 2014: everyone slows by about 35% and keeps a positive delta. First use: Monaco 2015. Standing restart after a red flag (from 2020 (?)). | Mugello 2020: the leader went slow until late at a restart, cars behind crashed (?). |
| 2021 | Aston Martin and Mercedes share the job. | Abu Dhabi: only the five lapped cars between Hamilton and Verstappen were let through, and the safety car came in a lap early. Verstappen passed on the last lap and won the title. | Spa: two laps behind the safety car, red flag on lap 3. Result after lap 1, half points. | The rule said "any" lapped cars. Was that all of them or only some? The FIA said later it was open to both readings. |
| 2022 to 2026 | Same. | All lapped cars must unlap, a list on screen tells them. The safety car comes in one lap after the message. | Free tyre change and repairs under a red flag. | Japan 2022: a recovery crane was on track under the safety car in the rain (?). Australia 2023: three red flags, the race ended behind the safety car with the order from before the last restart (?). Monza 2024: the safety car crashed on Thursday. |

## Safety car or red flag?

| | Safety car | Virtual safety car | Red flag |
|---|---|---|---|
| Cars | In a line behind the safety car | Spread out, each slows down | Into the pit lane, stop |
| Race clock | Runs, laps count | Runs, laps count | Stops, no racing |
| Pit stop | Cheap: the field is slow | Cheap, but less | Free tyre change |
| Gaps | Gone | Kept | Gone |
| Restart | Behind the safety car, rolling | Green flag, everyone at once | Standing start from the grid (?) |

## Rules across all years

- Double waved yellow: be ready to stop, no overtaking.
- Under the safety car nobody may overtake, until the first safety car line.
- The leader's lap decides when a lapped car is "lapped".

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| No safety car (early eras) | Yes | `safety_car_policy` none |
| Safety car | Yes | `safety_car_policy` physical_only |
| Virtual safety car | Yes | `safety_car_policy` all_types |
| Red flag | Partly | `formula_red_flags`, up to 2 per race |
| Pit lane closed under the safety car | No | B11 |
| Lapped cars unlap, wave-around | Partly | oval mode only |
| Full-course yellow, slow zones | Partly | VSC stands in (B11) |

## Sources

- Wikipedia, "Safety car" (F1 history, procedure, VSC, cars, incidents),
  "Racing flags" (yellow, double yellow, red flag, VSC end), "2021 Abu
  Dhabi Grand Prix" (lapped cars, rule text, FIA report).
- Not confirmed, marked `(?)`: red flags before the 1990s, lapped car rules
  before 2010, Hungary 1995, Canada 2011, Mugello 2020, Japan 2022,
  Australia 2023, when standing restarts after a red flag came in.

## Discord post

=== post | F1 safety car history | f1-safety-car
## F1 safety car and red flags, 1950 to 2026

Part six of the rules history. The table is below. What stood out to me:

- **No safety car for over 40 years.** The first one in 1973 picked up the wrong leader. It took hours to find the winner. Official only from 1993.
- **Pit lane closed under the safety car (2007 to 2008).** A car low on fuel got a penalty for stopping. Singapore 2008 showed how a safety car can be used on purpose.
- **Lapped cars:** stay, may not unlap (2010 to 2011), may unlap, then all must unlap after Abu Dhabi 2021.
- **Virtual safety car from 2015:** everyone slows down, the gaps stay.
- **Red flag:** the clock stops, tyres can be changed for free, standing restart.

A small table in the picture compares safety car, VSC and red flag. That's really what the game would need. For each one: does the clock run, do the gaps stay, how cheap is a pit stop, how does the restart work, what happens to lapped cars, and whether the pit lane is open. With those settings, every F1 era and the DTM rules (full course yellow, safety car laps added to the race in 2019 and 2025) fit.

The last table in the picture shows what the game can do today: yes, partly or no.

Next up: DRS. Mistakes? Tell me!
