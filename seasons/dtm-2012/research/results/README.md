# DTM 2012: qualifying and race results

20 CSV files, one qualifying and one race file per round, in the same column format as
`seasons/dtm-2013/research/results/` (`pos,number,driver,entrant,car,laps,time,gap,fastest_lap,status,notes`).
Driver names, numbers, entrant and car strings come from `../entries.csv`.

## How the files are built

**Qualifying format in 2012.** Four knockout sessions. Q1 had all 22 cars and the slowest 6 were out (P17 to P22). Q2 had 16 cars and 6 more were out (P11 to P16). Q3 had 10 cars and 6 more were out (P5 to P10). Q4 was a single flying lap for the top 4. The official sheet sorts by final position, not by lap time.

**Qualifying (`NN-<venue>-qualifying.csv`)**
- `pos` is the final qualifying position.
- Rounds 2, 3, 4, 9 and 10 (official sheet found): `time` is the driver's best lap from any session (Q1 to Q4), and the session is named in `notes`. `notes` lists every session time with its rank inside that session. The Q4 shoot-out lap was often slower than Q2 or Q3, so `time` is often not the pole lap.
- Rounds 1, 5, 6, 7 and 8 (official sheet not found): only the time from the last session each driver reached is known. This is the time printed in the official classification. `time` is that lap and `notes` names the session. Earlier session times and session ranks are missing.
- `gap` is measured from the quickest known lap of the whole qualifying, not from the pole lap.
- `grid` in `notes` is the qualifying position. Starting grid sheets were found only for rounds 4, 6 and 10, and they match the qualifying order. No grid penalties were found for any round, but for the other rounds this was not checked against a grid sheet.

**Race (`NN-<venue>-race.csv`)**
- The winner's row has the race time. Every other car on the lead lap has `time` = winner's time + gap. The official sheets give both the total time and the gap, and they agree.
- For lapped cars, `gap` is "+N lap(s)" and `time` is left empty.
- Retirements that still covered at least 75% of the winner's laps are classified, as in the official results, and keep their `pos`. Other retirements have an empty `pos` and status `DNF`. Retirement reasons were not found.
- `fastest_lap` is each driver's best race lap, from the official sheet. For Lausitzring only Green's race fastest lap is known.
- Tyres: 2012 had one dry compound, so there is no tyre sequence. The rules required 2 pit stops with all four wheels changed and no refuelling. `notes` says "2 stops (mandatory)" for cars that finished. Individual stop laps were not found.
- Points: 25, 18, 15, 12, 10, 8, 6, 4, 2, 1 for the top 10.

## Sources per round

Two main sources:
- **Official timing sheets** (wige Solutions, the DTM timekeeper), saved on archive.org from the old dtm.com results folder. URL pattern: `http://www.dtm.com/ergebnisse/pdf/<date><letter>.pdf`, read through `https://web.archive.org/web/<timestamp>id_/<url>`. Letter `d` = combined qualifying (Q1 to Q4 per driver), `e` = starting grid, `g` = race result.
- **racingyears.com** race pages, for example `https://www.racingyears.com/race/2012_DTM_Hockenheim_2`. These hold the full race order with total times and the qualifying order with each driver's classification time. The qualifying data loads from `https://www.racingyears.com/race_section.php?GP=2012%20DTM%20Hockenheim%202&section=quali`.

The DTM fan wiki has no 2012 race pages (the season page links to them but they do not exist). results.motorsportstats.com redirects in a loop and touringcars.net is behind a bot check.

| Rd | Qualifying sources | Race sources |
|---|---|---|
| 1 Hockenheim | racingyears; pole 1:34.680 also in touringcartimes 2012-04-28 and autoracing1 | official sheet `2012-04-29g.pdf`; racingyears |
| 2 Lausitzring | official sheet `2012-05-06d.pdf`; racingyears | racingyears; BMW press release T0126618EN and autosport.com (winner time and top 3) |
| 3 Brands Hatch | official sheet `2012-05-20d.pdf`; racingyears | official sheet `2012-05-20g.pdf`; racingyears |
| 4 Red Bull Ring | official sheet `2012-06-03d.pdf`, grid `2012-06-03e.pdf`; racingyears | official sheet `2012-06-03g.pdf`; racingyears |
| 5 Norisring | racingyears; pole 49.139 also in auto123; "35 degrees" from DTM "News am Sonntag" Norisring 2012 (archive.org) | official sheet `2012-07-01g.pdf`; racingyears; autosport.com race report (wet start) |
| 6 Nürburgring | racingyears; grid sheet `2012-08-19e.pdf` (same times); DTM "News am Sonntag" Nürburgring 2012 (pole 1:24.284) | official sheet `2012-08-19g.pdf`; racingyears |
| 7 Zandvoort | racingyears; BMW press release T0130745EN (pole 1:32.365, BMW times, damp Q1) | official sheet `2012-08-26g.pdf`; racingyears; Audi and autoracing1 reports (showers, two safety cars) |
| 8 Oschersleben | racingyears; pole 1:20.916 also in motorsport.com and auto123 reports | official sheet `2012-09-16g.pdf`; racingyears; BMW press release (Spengler won from pole, Paffett +0.629) |
| 9 Valencia | official sheet `2012-09-30d.pdf`; racingyears | official sheet `2012-09-30g.pdf`; racingyears |
| 10 Hockenheim | official sheet `2012-10-21d.pdf`, grid `2012-10-21e.pdf`; racingyears | official sheet `2012-10-21g.pdf`; racingyears; germancarscene.com 2012-10-21 (Spengler 1h07m59.069s, Paffett +2.214) |

Season-level cross-check: https://en.wikipedia.org/wiki/2012_Deutsche_Tourenwagen_Masters and the de.wiki page "DTM-Saison 2012". Pole, race fastest lap and winner match `../calendar.csv` for all 10 rounds.

## Verified vs single source

**Verified by two or more sources:**
- Pole sitter and pole lap for all 10 rounds.
- Winner and winner's race time for all 10 rounds.
- Race order, laps and total times for rounds 1, 3 to 10 (official sheet and racingyears).
- Q1 to Q4 times for rounds 2, 3, 4, 9 and 10 (official sheet, and racingyears shows the same classification times).
- Qualifying classification times for rounds 1, 5, 6, 7 and 8 (racingyears; round 6 also on the official grid sheet; BMW times at Zandvoort also in the BMW release).

**Single source:**
- Lausitzring race positions 4 to 21 (racingyears only; top 3 and winner time checked against BMW and autosport).
- Per-driver race fastest laps (official sheets only).

**Where the sources disagree, the official sheet is used:**
- Red Bull Ring: Merhi's total time is 1:13:20.616 on the official sheet (racingyears has 1:13:15.616, a typo; the official gap of 6.772 s to Schumacher confirms 1:13:20.616).
- Norisring: Tambay ran 76 laps (racingyears 77).
- Valencia: Hand ran 42 laps (racingyears 45) and Paffett 27 (racingyears 25).
- racingyears shows late retirements as DNF. The official sheets classify them: Merhi at Hockenheim 1, Wolff at Brands Hatch, Albuquerque at Zandvoort, Tambay and Priaulx at Oschersleben, Mortara at Valencia.

## Pole laps and calibration

Pole lap = the Q4 shoot-out lap. In 2012 the Q4 lap was often slower than the best Q2 or Q3 laps, so both are given.

| Rd | Venue | Pole | Pole lap (Q4) | Quickest known lap in qualifying | Conditions |
|---|---|---|---|---|---|
| 1 | Hockenheim | Ekström | 1:34.680 | 1:34.195 (Mortara, Q3) | dry, no rain reported |
| 2 | Lausitzring | Spengler | 1:18.777 | 1:17.840 (Farfus, Q3) | dry, no rain reported |
| 3 | Brands Hatch Indy | Paffett | 41.266 | 41.020 (Rockenfeller, Q3) | dry, no rain reported |
| 4 | Red Bull Ring | Mortara | 1:26.171 | 1:25.784 (Paffett, Q2) | dry, no rain reported |
| 5 | Norisring | Paffett | 49.139 | 49.023 (R. Schumacher, Q3) | dry and hot, about 35 C |
| 6 | Nürburgring | Spengler | 1:24.284 | 1:24.241 (Tomczyk, Q3) | dry, no rain reported |
| 7 | Zandvoort | Scheider | 1:32.365 | 1:31.605 (Ekström, Q3) | **damp at the start, drying**. Q1 began on a damp track after morning rain. Q4 was about 0.7 s slower than Q3, reason not found |
| 8 | Oschersleben | Spengler | 1:20.916 | 1:20.916 (Spengler, Q4) | dry, no rain reported |
| 9 | Valencia | Farfus | 1:26.446 | 1:26.446 (Farfus, Q4) | dry, no rain reported |
| 10 | Hockenheim | Farfus | 1:34.140 | 1:33.673 (Farfus, Q3) | dry, no rain reported |

Notes for calibration:
- For rounds 1, 5, 6, 7 and 8 the "quickest known lap" only covers Q3 and Q4 for the top 10. A faster Q1 or Q2 lap may exist that we cannot see.
- Zandvoort is the only qualifying with confirmed damp running. The pole lap is likely dry but the session was mixed, so treat Zandvoort with care.
- Hockenheim 1: Mortara's 1:34.195 is his Q3 lap. He did not set a Q4 time. Werner's Q4 lap (1:36.276) is slow because he ran wide at the hairpin. One autosport report says both had their Q4 times taken away. Grid order (Werner 3rd, Mortara 4th) is the same either way.
- "Dry, no rain reported" means the reports read did not mention rain. Only Norisring and Zandvoort weather was checked in a direct report.

## Real race durations

All races were run to a set number of laps, with a time limit that ended two of them early (the winner's time just over 75 minutes in both).

| Rd | Venue | Laps (sched.) | Laps run | Winner | Winner's time |
|---|---|---|---|---|---|
| 1 | Hockenheim | 40 | 40 | Paffett | 1:04:37.615 |
| 2 | Lausitzring | 52 | 52 | Spengler | 1:09:45.795 |
| 3 | Brands Hatch Indy | 97 | 97 | Paffett | 1:10:01.585 |
| 4 | Red Bull Ring | 47 | 47 | Mortara | 1:12:30.277 |
| 5 | Norisring | 82 (one report, unconfirmed) | 78 (time limit, wet start) | Green | 1:15:00.005 |
| 6 | Nürburgring | 49 | 49 | Spengler | 1:11:12.847 |
| 7 | Zandvoort | 44 (BMW press release) | 43 (time limit, showers, two safety cars) | Mortara | 1:16:17.679 |
| 8 | Oschersleben | 51 | 51 | Spengler | 1:12:09.607 |
| 9 | Valencia | 46 | 46 | Farfus | 1:08:22.522 |
| 10 | Hockenheim | 42 | 42 | Spengler | 1:07:59.069 |

The `laps_per_heat` values in `../calendar.csv` are the laps actually run. Hockenheim 2 ran 42 laps (official sheet), which settles the 42 vs 38 question in `../calendar.csv`. The de.wiki figure of 173.812 km for that race is wrong.

For pace calibration, Norisring and Zandvoort winner times are not dry race pace. Red Bull Ring (47 laps in 1:12:30, about 92.6 s a lap against a best lap of 1:27.0) probably had safety-car laps (Vietoris and Tambay were out on lap 1; not checked in a report), so its average is slow too.

## Open questions

- Q1 to Q3 times for Hockenheim 1, Norisring, Nürburgring, Zandvoort and Oschersleben. The official `d` sheets for these rounds were not saved on archive.org. BMW and Audi press releases sometimes list their own drivers' times.
- Lausitzring race: the official sheet (`2012-05-06g.pdf`) was not on archive.org. Per-driver fastest laps are missing. Wickens stopped after 47 of 52 laps. He is put in 22nd as classified because he covered over 75% of the distance, but this is inferred, not read from an official sheet.
- Hockenheim 2: why Scheider has no qualifying time.
- Hockenheim 1: whether Werner and Mortara lost their Q4 times (autosport) or simply had slow or no laps (other reports).
- Zandvoort: why Q4 was slower than Q3, and whether rain was falling in Q4.
- Norisring: scheduled distance (82 laps from one report).
- Individual pit-stop laps and retirement reasons for all rounds.
- Grid penalties: only checked against grid sheets for rounds 4, 6 and 10.
