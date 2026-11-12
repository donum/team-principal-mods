# F1 2010: qualifying and race results

38 CSV files, one qualifying and one race file per round, in the column format of
`seasons/dtm-2013/research/results/` (`pos,number,driver,entrant,car,laps,time,gap,fastest_lap,status,notes`).
Driver names, numbers, entrant and car strings come from `../entries.csv`.

## How the files are built

Two sources were read for every round and compared row by row (script output, see "Conflicts" below):

1. **Jolpica F1 API** (the open successor of the Ergast database), `https://api.jolpi.ca/ergast/f1/<year>/...`. Structured data: qualifying Q1-Q3 times and positions, race classification with total times in milliseconds, grid, laps, status, points, each driver's fastest race lap, and pit stops per driver (no pit-stop data exists for 2010).
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
- `notes` give the retirement reason (Jolpica status, with the en.wiki wording in brackets where it differs), the grid slot (en.wiki; "pit lane" for pit-lane starts), the number of pit stops (not available for 2010), points, and any en.wiki footnote.
- `fastest_lap` is each driver's best race lap (Jolpica).
- Tyre sequences per driver were not in either source and are not given.

## Sources per round

| Rd | en.wiki article | Jolpica endpoints |
|---|---|---|
| 1 | https://en.wikipedia.org/wiki/2010_Bahrain_Grand_Prix | /2010/1/qualifying, /2010/1/results |
| 2 | https://en.wikipedia.org/wiki/2010_Australian_Grand_Prix | /2010/2/qualifying, /2010/2/results |
| 3 | https://en.wikipedia.org/wiki/2010_Malaysian_Grand_Prix | /2010/3/qualifying, /2010/3/results |
| 4 | https://en.wikipedia.org/wiki/2010_Chinese_Grand_Prix | /2010/4/qualifying, /2010/4/results |
| 5 | https://en.wikipedia.org/wiki/2010_Spanish_Grand_Prix | /2010/5/qualifying, /2010/5/results |
| 6 | https://en.wikipedia.org/wiki/2010_Monaco_Grand_Prix | /2010/6/qualifying, /2010/6/results |
| 7 | https://en.wikipedia.org/wiki/2010_Turkish_Grand_Prix | /2010/7/qualifying, /2010/7/results |
| 8 | https://en.wikipedia.org/wiki/2010_Canadian_Grand_Prix | /2010/8/qualifying, /2010/8/results |
| 9 | https://en.wikipedia.org/wiki/2010_European_Grand_Prix | /2010/9/qualifying, /2010/9/results |
| 10 | https://en.wikipedia.org/wiki/2010_British_Grand_Prix | /2010/10/qualifying, /2010/10/results |
| 11 | https://en.wikipedia.org/wiki/2010_German_Grand_Prix | /2010/11/qualifying, /2010/11/results |
| 12 | https://en.wikipedia.org/wiki/2010_Hungarian_Grand_Prix | /2010/12/qualifying, /2010/12/results |
| 13 | https://en.wikipedia.org/wiki/2010_Belgian_Grand_Prix | /2010/13/qualifying, /2010/13/results |
| 14 | https://en.wikipedia.org/wiki/2010_Italian_Grand_Prix | /2010/14/qualifying, /2010/14/results |
| 15 | https://en.wikipedia.org/wiki/2010_Singapore_Grand_Prix | /2010/15/qualifying, /2010/15/results |
| 16 | https://en.wikipedia.org/wiki/2010_Japanese_Grand_Prix | /2010/16/qualifying, /2010/16/results |
| 17 | https://en.wikipedia.org/wiki/2010_Korean_Grand_Prix | /2010/17/qualifying, /2010/17/results |
| 18 | https://en.wikipedia.org/wiki/2010_Brazilian_Grand_Prix | /2010/18/qualifying, /2010/18/results |
| 19 | https://en.wikipedia.org/wiki/2010_Abu_Dhabi_Grand_Prix | /2010/19/qualifying, /2010/19/results |

Season level: https://en.wikipedia.org/wiki/2010_Formula_One_World_Championship and Jolpica /2010/driverStandings, /2010/constructorStandings.

## Checks

- Sum of race points per driver and per constructor (Jolpica race results) against the final standings (`../standings.csv`, `../standings_other.csv`): all equal, no mismatch.
- Pole sitter, winner and fastest lap in `../calendar.csv` come from the en.wiki infobox and were compared with Jolpica (grid 1, position 1, fastest-lap rank 1). No mismatches.

## Conflicts between the two sources

Every cell that differs between Jolpica and en.wiki is listed here. Where it matters the CSV note gives the other value ("en.wiki gives ..." or "Jolpica gives ...").

- Rd 1 (bahrain):
  - Q Q1 #21 wiki '2:03.240' vs jolpica '2:03.204'
- Rd 2 (australia):
  - grid #24 wiki '21' vs jolpica '23'
  - grid #25 wiki '22' vs jolpica '24'
  - grid #21 wiki '23' vs jolpica '21'
  - grid #20 wiki '24' vs jolpica '22'
  - R grid #18 wiki 'pit lane' vs jolpica '20'
- Rd 4 (china):
  - Q Q3 #6 wiki '1:34.806' vs jolpica '1:34.808'
- Rd 5 (spain):
  - R laps #22 wiki 20 vs jolpica 18
- Rd 6 (monaco):
  - R time #3 wiki '+25.712' vs jolpica +5.712
- Rd 8 (canada):
  - R laps #24 wiki 50 vs jolpica 55
  - R laps #18 wiki 42 vs jolpica 47
  - R laps #22 wiki 30 vs jolpica 31
  - R laps #21 wiki 13 vs jolpica 14
- Rd 9 (europe):
  - Q Q2 #17 wiki '1:39.548' vs jolpica '1:39.458'
- Rd 14 (italy):
  - R grid #23 wiki 'pit lane' vs jolpica '13'
- Rd 15 (singapore):
  - Q Q2 #6 wiki '1:46.908' vs jolpica '1:45.908'
  - Q Q1 #24 wiki '1:50.721' vs jolpica '1:50.271'
  - Q Q1 #20 wiki '1:52.964' vs jolpica '1:52.946'
  - R time #14 wiki '+2:12.416' vs jolpica +2:02.416

## en.wiki footnotes not tied to one row

These footnotes name several drivers or start with a short name, so they are not copied into a CSV note.

- Rd 1 race: Both Sébastien Buemi and Jarno Trulli were classified as they had completed 90% of the winner's race distance.
- Rd 5 qualifying: The Virgins of Timo Glock and Lucas di Grassi were both given five-place penalties after the team failed to notify the FIA of changes to their gearbox ratios before the deadline for doing so.
- Rd 5 qualifying: Hispania's Karun Chandhok was also issued a five-place penalty for a similar gearbox-related infringement.
- Rd 5 race: Both Lewis Hamilton and Vitantonio Liuzzi were classified as they had completed 90% of the winner's race distance.
- Rd 6 race: Barrichello's accident was caused by a manhole cover which damaged his rear suspension.
- Rd 9 race: Button, Barrichello, Kubica, Sutil, Buemi, De la Rosa, Petrov and Liuzzi were given five-second time penalties for exceeding the safety car-in lap time. Hülkenberg was also given a five-second penalty, but he retired from the race.
- Rd 9 race: Glock was given a 20-second time penalty for failing to observe blue flags.
- Rd 12 race: 1. An incident between Michael Schumacher and Rubens Barrichello coming down the pit straight, where Schumacher nearly forced Barrichello into the pit wall while he was attempting an overtake was investigated by the stewards after the race. The stewards then came to a decision by handing Schumacher a 10-place grid penalty at the next race.

## Notes and decisions

- No pit-stop data for 2010 in Jolpica, so race notes have no pit-stop count.
- No 107% rule in 2010: every car started.
- Rd 6 Monaco: Schumacher passed Alonso on the last corner behind the safety car and got a 20-second penalty (6th to 12th). Jolpica keeps the time without the penalty; the file uses the en.wiki gap +25.712 and the time is the winner's time plus that gap.
- Rd 2 Australia and others: the en.wiki qualifying 'Grid' column gives grid slots after penalties as listed there; Jolpica sometimes gives the actual start order (for example after a pit-lane start). Both are in the notes where they differ.
