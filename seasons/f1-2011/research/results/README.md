# F1 2011: qualifying and race results

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
| 1 | https://en.wikipedia.org/wiki/2011_Australian_Grand_Prix | /2011/1/qualifying, /2011/1/results, /2011/1/pitstops |
| 2 | https://en.wikipedia.org/wiki/2011_Malaysian_Grand_Prix | /2011/2/qualifying, /2011/2/results, /2011/2/pitstops |
| 3 | https://en.wikipedia.org/wiki/2011_Chinese_Grand_Prix | /2011/3/qualifying, /2011/3/results, /2011/3/pitstops |
| 4 | https://en.wikipedia.org/wiki/2011_Turkish_Grand_Prix | /2011/4/qualifying, /2011/4/results, /2011/4/pitstops |
| 5 | https://en.wikipedia.org/wiki/2011_Spanish_Grand_Prix | /2011/5/qualifying, /2011/5/results, /2011/5/pitstops |
| 6 | https://en.wikipedia.org/wiki/2011_Monaco_Grand_Prix | /2011/6/qualifying, /2011/6/results, /2011/6/pitstops |
| 7 | https://en.wikipedia.org/wiki/2011_Canadian_Grand_Prix | /2011/7/qualifying, /2011/7/results, /2011/7/pitstops |
| 8 | https://en.wikipedia.org/wiki/2011_European_Grand_Prix | /2011/8/qualifying, /2011/8/results, /2011/8/pitstops |
| 9 | https://en.wikipedia.org/wiki/2011_British_Grand_Prix | /2011/9/qualifying, /2011/9/results, /2011/9/pitstops |
| 10 | https://en.wikipedia.org/wiki/2011_German_Grand_Prix | /2011/10/qualifying, /2011/10/results, /2011/10/pitstops |
| 11 | https://en.wikipedia.org/wiki/2011_Hungarian_Grand_Prix | /2011/11/qualifying, /2011/11/results, /2011/11/pitstops |
| 12 | https://en.wikipedia.org/wiki/2011_Belgian_Grand_Prix | /2011/12/qualifying, /2011/12/results, /2011/12/pitstops |
| 13 | https://en.wikipedia.org/wiki/2011_Italian_Grand_Prix | /2011/13/qualifying, /2011/13/results, /2011/13/pitstops |
| 14 | https://en.wikipedia.org/wiki/2011_Singapore_Grand_Prix | /2011/14/qualifying, /2011/14/results, /2011/14/pitstops |
| 15 | https://en.wikipedia.org/wiki/2011_Japanese_Grand_Prix | /2011/15/qualifying, /2011/15/results, /2011/15/pitstops |
| 16 | https://en.wikipedia.org/wiki/2011_Korean_Grand_Prix | /2011/16/qualifying, /2011/16/results, /2011/16/pitstops |
| 17 | https://en.wikipedia.org/wiki/2011_Indian_Grand_Prix | /2011/17/qualifying, /2011/17/results, /2011/17/pitstops |
| 18 | https://en.wikipedia.org/wiki/2011_Abu_Dhabi_Grand_Prix | /2011/18/qualifying, /2011/18/results, /2011/18/pitstops |
| 19 | https://en.wikipedia.org/wiki/2011_Brazilian_Grand_Prix | /2011/19/qualifying, /2011/19/results, /2011/19/pitstops |

Season level: https://en.wikipedia.org/wiki/2011_Formula_One_World_Championship and Jolpica /2011/driverStandings, /2011/constructorStandings.

## Checks

- Sum of race points per driver and per constructor (Jolpica race results) against the final standings (`../standings.csv`, `../standings_other.csv`): all equal, no mismatch.
- Pole sitter, winner and fastest lap in `../calendar.csv` come from the en.wiki infobox and were compared with Jolpica (grid 1, position 1, fastest-lap rank 1). No mismatches.

## Conflicts between the two sources

Every cell that differs between Jolpica and en.wiki is listed here. Where it matters the CSV note gives the other value ("en.wiki gives ..." or "Jolpica gives ...").

- Rd 2 (malaysia):
  - R time #5 wiki '+57.248' vs jolpica +37.248
  - R laps #14 wiki 56 vs jolpica 55
- Rd 6 (monaco):
  - Q pos #3 wiki 9 vs jolpica 7
  - Q Q3 #3 wiki 'no time' vs jolpica '1:15.280'
  - Q pos #8 wiki 7 vs jolpica 8
  - Q pos #12 wiki 8 vs jolpica 9
  - grid #17 wiki 'did not start' vs jolpica 'pit lane'
  - R time #3 wiki '+47.210' vs jolpica +27.210
  - R grid #17 wiki '-' vs jolpica 'pit lane'
- Rd 9 (britain):
  - R time #8 wiki '+1:00.655' vs jolpica +1:00.665
- Rd 10 (nuerburgring):
  - Q #18 wiki EX (jolpica pos 16)
- Rd 12 (belgium):
  - R time #6 wiki '+1:06.706' vs jolpica +1:06.076
- Rd 15 (japan):
  - Q pos #7 wiki 8 vs jolpica 7
  - Q pos #9 wiki 9 vs jolpica 8
  - Q pos #10 wiki 10 vs jolpica 9
  - Q pos #16 wiki 7 vs jolpica 10
- Rd 16 (korea):
  - R time #15 wiki '+1:03.602' vs jolpica +1:08.602
- Rd 18 (abudhabi):
  - R time #4 wiki '+25.871' vs jolpica +25.881
  - R laps #22 wiki 47 vs jolpica 48
  - R laps #18 wiki 18 vs jolpica 19
  - R laps #25 wiki 17 vs jolpica 18

## Notes and decisions

- Rd 6 Monaco: Hamilton's Q3 time (1:15.280 in Jolpica) was deleted, en.wiki shows no Q3 time and places him 9th. The file keeps the Jolpica lap in the notes and uses the en.wiki position.
- Rd 6 Monaco: Pérez crashed in Q3 and did not start. Jolpica gives him a pit-lane grid slot; he did not take part in the race.
- Rd 10 Germany: Buemi was excluded from qualifying (fuel irregularity) and started 24th. Jolpica keeps him 16th in qualifying; the file follows en.wiki.
- Rd 15 Japan: Kobayashi set no Q3 time. en.wiki places him 7th, Jolpica 10th. The file follows en.wiki; the grid in the notes is from en.wiki.
- Rd 2 Malaysia and Rd 6 Monaco: post-race 20-second penalties (Alonso and Hamilton in Malaysia, Hamilton in Monaco). en.wiki shows the time with the penalty in some rows and before it in others; Jolpica times include the penalty.
- Laps of retired cars and a few gaps differ by one digit between the sources. Jolpica values are used and the en.wiki value is in the note.
- Rd 2 Malaysia (Alonso) and Rd 6 Monaco (Hamilton): Jolpica gives the gap without the 20-second penalty; the files use the en.wiki gap and recompute the time from it.
