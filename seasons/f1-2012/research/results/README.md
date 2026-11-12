# F1 2012: qualifying and race results

40 CSV files, one qualifying and one race file per round, in the column format of
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
| 1 | https://en.wikipedia.org/wiki/2012_Australian_Grand_Prix | /2012/1/qualifying, /2012/1/results, /2012/1/pitstops |
| 2 | https://en.wikipedia.org/wiki/2012_Malaysian_Grand_Prix | /2012/2/qualifying, /2012/2/results, /2012/2/pitstops |
| 3 | https://en.wikipedia.org/wiki/2012_Chinese_Grand_Prix | /2012/3/qualifying, /2012/3/results, /2012/3/pitstops |
| 4 | https://en.wikipedia.org/wiki/2012_Bahrain_Grand_Prix | /2012/4/qualifying, /2012/4/results, /2012/4/pitstops |
| 5 | https://en.wikipedia.org/wiki/2012_Spanish_Grand_Prix | /2012/5/qualifying, /2012/5/results, /2012/5/pitstops |
| 6 | https://en.wikipedia.org/wiki/2012_Monaco_Grand_Prix | /2012/6/qualifying, /2012/6/results, /2012/6/pitstops |
| 7 | https://en.wikipedia.org/wiki/2012_Canadian_Grand_Prix | /2012/7/qualifying, /2012/7/results, /2012/7/pitstops |
| 8 | https://en.wikipedia.org/wiki/2012_European_Grand_Prix | /2012/8/qualifying, /2012/8/results, /2012/8/pitstops |
| 9 | https://en.wikipedia.org/wiki/2012_British_Grand_Prix | /2012/9/qualifying, /2012/9/results, /2012/9/pitstops |
| 10 | https://en.wikipedia.org/wiki/2012_German_Grand_Prix | /2012/10/qualifying, /2012/10/results, /2012/10/pitstops |
| 11 | https://en.wikipedia.org/wiki/2012_Hungarian_Grand_Prix | /2012/11/qualifying, /2012/11/results, /2012/11/pitstops |
| 12 | https://en.wikipedia.org/wiki/2012_Belgian_Grand_Prix | /2012/12/qualifying, /2012/12/results, /2012/12/pitstops |
| 13 | https://en.wikipedia.org/wiki/2012_Italian_Grand_Prix | /2012/13/qualifying, /2012/13/results, /2012/13/pitstops |
| 14 | https://en.wikipedia.org/wiki/2012_Singapore_Grand_Prix | /2012/14/qualifying, /2012/14/results, /2012/14/pitstops |
| 15 | https://en.wikipedia.org/wiki/2012_Japanese_Grand_Prix | /2012/15/qualifying, /2012/15/results, /2012/15/pitstops |
| 16 | https://en.wikipedia.org/wiki/2012_Korean_Grand_Prix | /2012/16/qualifying, /2012/16/results, /2012/16/pitstops |
| 17 | https://en.wikipedia.org/wiki/2012_Indian_Grand_Prix | /2012/17/qualifying, /2012/17/results, /2012/17/pitstops |
| 18 | https://en.wikipedia.org/wiki/2012_Abu_Dhabi_Grand_Prix | /2012/18/qualifying, /2012/18/results, /2012/18/pitstops |
| 19 | https://en.wikipedia.org/wiki/2012_United_States_Grand_Prix | /2012/19/qualifying, /2012/19/results, /2012/19/pitstops |
| 20 | https://en.wikipedia.org/wiki/2012_Brazilian_Grand_Prix | /2012/20/qualifying, /2012/20/results, /2012/20/pitstops |

Season level: https://en.wikipedia.org/wiki/2012_Formula_One_World_Championship and Jolpica /2012/driverStandings, /2012/constructorStandings.

## Checks

- Sum of race points per driver and per constructor (Jolpica race results) against the final standings (`../standings.csv`, `../standings_other.csv`): all equal, no mismatch.
- Pole sitter, winner and fastest lap in `../calendar.csv` come from the en.wiki infobox and were compared with Jolpica (grid 1, position 1, fastest-lap rank 1). No mismatches.

## Conflicts between the two sources

Every cell that differs between Jolpica and en.wiki is listed here. Where it matters the CSV note gives the other value ("en.wiki gives ..." or "Jolpica gives ...").

- Rd 1 (australia):
  - Q Q2 #2 wiki '1:26.297' vs jolpica '1:26.597'
- Rd 2 (malaysia):
  - R pos #23 wiki 22 vs jolpica 21
  - R pos #22 wiki 21 vs jolpica 22
- Rd 3 (china):
  - grid #17 wiki '18' vs jolpica '24'
  - grid #20 wiki '19' vs jolpica '18'
  - grid #21 wiki '20' vs jolpica '19'
  - grid #24 wiki '21' vs jolpica '20'
  - grid #25 wiki '22' vs jolpica '21'
  - grid #22 wiki '23' vs jolpica '22'
  - grid #23 wiki '24' vs jolpica '23'
- Rd 4 (bahrain):
  - Q Q1 #11 wiki '1:34.624' vs jolpica '1:36.624'
- Rd 5 (spain):
  - Q #4 wiki EX (jolpica pos 1)
- Rd 6 (monaco):
  - grid #18 wiki '23' vs jolpica '24'
- Rd 7 (canada):
  - Q Q1 #12 wiki '1:15.107' vs jolpica '1:15.106'
  - R laps #25 wiki 67 vs jolpica 69
  - R #24 jolpica classified P21 with 56/70 laps (Suspension); treated as DNF
- Rd 10 (germany):
  - R time #3 wiki '+6.931' vs jolpica +6.949
- Rd 11 (hungary):
  - R grid #7 wiki 'pit lane' vs jolpica '17'
- Rd 12 (belgium):
  - R laps #23 wiki 30 vs jolpica 29
  - R laps #18 wiki 5 vs jolpica 4
- Rd 14 (singapore):
  - Q Q1 #10 wiki '1:47.668' vs jolpica '1:47.688'
  - R time #2 wiki '+1:07.175' vs jolpica +1:27.175
  - R time #20 wiki '+1:47.467' vs jolpica +1:47.967
- Rd 15 (japan):
  - Q Q2 #10 wiki '1:31.968' vs jolpica '1:31.988'
  - R time #6 wiki '+20.632' vs jolpica +20.639
  - R laps #25 wiki 36 vs jolpica 37
  - R laps #15 wiki 19 vs jolpica 18
- Rd 16 (korea):
  - Q Q1 #17 wiki '1:38.774' vs jolpica '1:38.744'
- Rd 17 (india):
  - Q Q3 #3 wiki '1:25.649' vs jolpica '1:25.659'
  - R laps #22 wiki 42 vs jolpica 43
  - R laps #15 wiki 20 vs jolpica 21
- Rd 18 (abudhabi):
  - Q #1 wiki EX (jolpica pos 3)

## en.wiki footnotes not tied to one row

These footnotes name several drivers or start with a short name, so they are not copied into a CSV note.

- Rd 1 race: Both Pedro de la Rosa and Narain Karthikeyan failed to qualify within the 107% time and were not given permission by the stewards to start the race. As a result, they were not allowed to start or compete in the race.

## Notes and decisions

- Rd 5 Spain: Hamilton was excluded from qualifying (too little fuel for the FIA sample). Jolpica keeps him 1st in its qualifying list and every other driver one place lower. The files follow en.wiki: Maldonado 1st, Hamilton excluded, grid 24.
- Rd 5 Spain: Karthikeyan was outside the 107% time but allowed to start. en.wiki shows no position for him (sort value 23); the file uses 23.
- Rd 18 Abu Dhabi: Vettel was excluded from qualifying (car stopped on track without enough fuel for the sample) and started from the pit lane. Same handling as Spain.
- Rd 2 Malaysia: Karthikeyan got a 20-second post-race penalty. en.wiki puts him 22nd behind de la Rosa; Jolpica keeps him 21st. The file follows en.wiki. Points are not affected.
- Rd 3 China: Vergne started from the pit lane after parc-fermé changes. The en.wiki qualifying table gives the grid slots before that (Vergne 18); Jolpica gives the start order (Vergne 24, cars behind him one place higher). Qualifying notes give both.
- Rd 7 Canada: Jolpica lists Glock as classified 21st, but he retired after 56 of 70 laps, which is under 90%. The file shows him as DNF, as en.wiki does.
- Laps of retired cars: Jolpica gives laps completed. en.wiki sometimes gives one lap more or less. Jolpica values are used, the en.wiki value is in the note.
- Retirement reasons are media wording, not FIA data. Both versions are kept where they differ.
- Small time differences (for example Webber Q2 in Australia 1:26.597 vs 1:26.297, di Resta Q1 in Bahrain 1:36.624 vs 1:34.624) look like typing errors in one source. They were not checked against a third source. Jolpica values are used and the session ranks in the notes are computed from them.
- Rd 14 Singapore: en.wiki gives Webber +1:07.175, the gap before his 20-second post-race penalty (its footnote says he originally finished tenth). Jolpica gives +1:27.175, which includes the penalty. The file uses the Jolpica value.
