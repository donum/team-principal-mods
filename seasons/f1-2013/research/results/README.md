# F1 2013: qualifying and race results

38 CSV files, one qualifying and one race file per round, in the column format of
`seasons/dtm-2013/research/results/` (`pos,number,driver,entrant,car,laps,time,gap,fastest_lap,status,notes`).
Driver names, numbers, entrant and car strings come from `../entries.csv`.

## How the files are built

Two sources were read for every round and compared row by row (script output, see "Conflicts" below):

1. **Jolpica F1 API** (the open successor of the Ergast database), `https://api.jolpi.ca/ergast/f1/<year>/...`. Structured data: qualifying Q1-Q3 times and positions, race classification with total times in milliseconds, grid, laps, status, points, each driver's fastest race lap, and pit stops per driver.
2. **English Wikipedia race article** for each round, pulled as wikitext through the MediaWiki API (`action=query&prop=revisions&rvprop=content`). Used for the qualifying and race tables, the footnotes on grid penalties and exclusions, and the infobox (length, laps, weather, pole, fastest lap).

**Qualifying (`NN-<venue>-qualifying.csv`)**
- `pos` is the final qualifying position, before grid penalties, as in the en.wiki table. A driver excluded from qualifying has an empty `pos` and status `excluded`.
- `time` is the driver's best lap of Q1, Q2 or Q3. The session is named in `notes`. In wet or drying sessions the best lap can be in Q1 or Q2, so `time` and `pos` do not always line up.
- `gap` is measured from the quickest lap of the whole qualifying by a driver who was not excluded.
- `notes` list every session time with the rank in that session, the grid slot from the en.wiki table, and the en.wiki footnote on any penalty.
- status `DNQ` = outside the 107% time and not allowed to start.

**Race (`NN-<venue>-race.csv`)**
- The winner's row has the race time. Every other car on the lead lap has `time` = its own total time from Jolpica (winner's time + gap). `gap` is the official gap.
- Lapped cars have `gap` "+N lap(s)" and an empty `time`.
- Retirements that still completed 90% of the winner's laps are classified (FIA rule) and keep their `pos`; the reason is in `notes`. Other retirements have an empty `pos` and status `DNF`. `DNS` = did not start, `DSQ` = disqualified, `DNQ` = did not qualify (no race).
- `notes` give the retirement reason (Jolpica status, with the en.wiki wording in brackets where it differs), the grid slot (en.wiki; "pit lane" for pit-lane starts), the number of pit stops (Jolpica pit-stop data; drive-through penalties may or may not be counted), points, and any en.wiki footnote.
- `fastest_lap` is each driver's best race lap (Jolpica).
- Tyre sequences per driver were not in either source and are not given.

## Sources per round

| Rd | en.wiki article | Jolpica endpoints |
|---|---|---|
| 1 | https://en.wikipedia.org/wiki/2013_Australian_Grand_Prix | /2013/1/qualifying, /2013/1/results, /2013/1/pitstops |
| 2 | https://en.wikipedia.org/wiki/2013_Malaysian_Grand_Prix | /2013/2/qualifying, /2013/2/results, /2013/2/pitstops |
| 3 | https://en.wikipedia.org/wiki/2013_Chinese_Grand_Prix | /2013/3/qualifying, /2013/3/results, /2013/3/pitstops |
| 4 | https://en.wikipedia.org/wiki/2013_Bahrain_Grand_Prix | /2013/4/qualifying, /2013/4/results, /2013/4/pitstops |
| 5 | https://en.wikipedia.org/wiki/2013_Spanish_Grand_Prix | /2013/5/qualifying, /2013/5/results, /2013/5/pitstops |
| 6 | https://en.wikipedia.org/wiki/2013_Monaco_Grand_Prix | /2013/6/qualifying, /2013/6/results, /2013/6/pitstops |
| 7 | https://en.wikipedia.org/wiki/2013_Canadian_Grand_Prix | /2013/7/qualifying, /2013/7/results, /2013/7/pitstops |
| 8 | https://en.wikipedia.org/wiki/2013_British_Grand_Prix | /2013/8/qualifying, /2013/8/results, /2013/8/pitstops |
| 9 | https://en.wikipedia.org/wiki/2013_German_Grand_Prix | /2013/9/qualifying, /2013/9/results, /2013/9/pitstops |
| 10 | https://en.wikipedia.org/wiki/2013_Hungarian_Grand_Prix | /2013/10/qualifying, /2013/10/results, /2013/10/pitstops |
| 11 | https://en.wikipedia.org/wiki/2013_Belgian_Grand_Prix | /2013/11/qualifying, /2013/11/results, /2013/11/pitstops |
| 12 | https://en.wikipedia.org/wiki/2013_Italian_Grand_Prix | /2013/12/qualifying, /2013/12/results, /2013/12/pitstops |
| 13 | https://en.wikipedia.org/wiki/2013_Singapore_Grand_Prix | /2013/13/qualifying, /2013/13/results, /2013/13/pitstops |
| 14 | https://en.wikipedia.org/wiki/2013_Korean_Grand_Prix | /2013/14/qualifying, /2013/14/results, /2013/14/pitstops |
| 15 | https://en.wikipedia.org/wiki/2013_Japanese_Grand_Prix | /2013/15/qualifying, /2013/15/results, /2013/15/pitstops |
| 16 | https://en.wikipedia.org/wiki/2013_Indian_Grand_Prix | /2013/16/qualifying, /2013/16/results, /2013/16/pitstops |
| 17 | https://en.wikipedia.org/wiki/2013_Abu_Dhabi_Grand_Prix | /2013/17/qualifying, /2013/17/results, /2013/17/pitstops |
| 18 | https://en.wikipedia.org/wiki/2013_United_States_Grand_Prix | /2013/18/qualifying, /2013/18/results, /2013/18/pitstops |
| 19 | https://en.wikipedia.org/wiki/2013_Brazilian_Grand_Prix | /2013/19/qualifying, /2013/19/results, /2013/19/pitstops |

Season level: https://en.wikipedia.org/wiki/2013_Formula_One_World_Championship and Jolpica /2013/driverStandings, /2013/constructorStandings.

## Checks

- Sum of race points per driver and per constructor (Jolpica race results) against the final standings (`../standings.csv`, `../standings_other.csv`): all equal, no mismatch.
- Pole sitter, winner and fastest lap in `../calendar.csv` come from the en.wiki infobox and were compared with Jolpica (grid 1, position 1, fastest-lap rank 1). No mismatches.

## Conflicts between the two sources

Every cell that differs between Jolpica and en.wiki is listed here. Where it matters the CSV note gives the other value ("en.wiki gives ..." or "Jolpica gives ...").

- Rd 3 (china):
  - Q #2 wiki EX (jolpica pos 14)
- Rd 5 (spain):
  - R #18 jolpica classified P20 with 52/66 laps (Accident); treated as DNF
  - R #21 jolpica classified P21 with 21/66 laps (Wheel); treated as DNF
  - R #8 jolpica classified P22 with 8/66 laps (Suspension); treated as DNF
- Rd 6 (monaco):
  - R time #9 wiki '2:17:52.506' vs jolpica 2:17:52.056
  - R time #1 wiki '+ 3.889' vs jolpica +3.888
  - R time #10 wiki '+ 13.895' vs jolpica +13.894
  - R time #15 wiki '+ 21.478' vs jolpica +21.477
  - R time #5 wiki '+ 23.104' vs jolpica +23.103
  - R time #18 wiki '+ 27.224' vs jolpica +27.223
  - R time #23 wiki '+ 49.886' vs jolpica +49.885
  - R time #21 wiki '+ 1:02.591' vs jolpica +1:02.590
- Rd 8 (britain):
  - Q #14 wiki EX (jolpica pos 5)
- Rd 13 (singapore):
  - R time #15 wiki '+1:24.688' vs jolpica +1:24.668
- Rd 15 (japan):
  - Q Q3 #11 wiki '1:31.664' vs jolpica '1:31.644'
- Rd 16 (india):
  - Q Q2 #12 wiki '1:26.336' vs jolpica '1:26.366'
- Rd 17 (abudhabi):
  - Q #7 wiki DSQ (jolpica pos 5)
  - Q pos #11 wiki 5 vs jolpica 6
  - Q pos #8 wiki 6 vs jolpica 7
  - Q pos #4 wiki 7 vs jolpica 8
  - Q pos #6 wiki 8 vs jolpica 9
  - Q pos #19 wiki 9 vs jolpica 10
  - Q pos #3 wiki 10 vs jolpica 11
  - Q pos #14 wiki 11 vs jolpica 12
  - Q pos #5 wiki 12 vs jolpica 13
  - Q pos #18 wiki 13 vs jolpica 14
  - Q pos #16 wiki 14 vs jolpica 15
  - Q pos #17 wiki 15 vs jolpica 16
  - Q pos #12 wiki 16 vs jolpica 17
  - Q pos #15 wiki 17 vs jolpica 18
  - Q pos #21 wiki 18 vs jolpica 19
  - Q pos #22 wiki 19 vs jolpica 20
  - Q pos #20 wiki 20 vs jolpica 21
  - Q pos #23 wiki 21 vs jolpica 22
- Rd 18 (usa):
  - R pos #18 wiki 16 vs jolpica 12
  - R time #18 wiki '+ 1:44.574' vs jolpica +1:24.574
  - R pos #4 wiki 12 vs jolpica 13
  - R pos #12 wiki 13 vs jolpica 14
  - R pos #7 wiki 14 vs jolpica 15
  - R pos #14 wiki 15 vs jolpica 16
- Rd 19 (brazil):
  - Q Q1 #12 wiki '1:27.445' vs jolpica '1:27.455'

## Notes and decisions

- Rd 3 China: Webber was excluded from qualifying (could not give the one-litre fuel sample) and started from the pit lane. Rd 8 Britain: di Resta was excluded from qualifying (en.wiki: he and his car were under the 640 kg minimum weight) and started 21st. Rd 17 Abu Dhabi: Räikkönen was disqualified from qualifying (floor deflection test). Jolpica keeps all three in their original qualifying places; the files follow en.wiki.
- Rd 5 Spain: Jolpica gives numeric positions 20-22 to three cars that retired well short of 90% distance (Vergne, van der Garde and Grosjean). The files show them as DNF, as en.wiki does.
- Rd 18 United States: Vergne got a 20-second post-race penalty and dropped from 12th to 16th. Jolpica does not apply it. The file follows en.wiki for positions 12-16; the time column keeps Jolpica's time without the penalty and the note gives the en.wiki gap. No points are affected.
- Rd 6 Monaco: en.wiki gives the winner's time as 2:17:52.506, Jolpica 2:17:52.056; several gaps differ by 0.001 s (rounding). Jolpica values are used.
