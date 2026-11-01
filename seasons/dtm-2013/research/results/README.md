# DTM 2013: qualifying and race results

20 CSV files, one qualifying and one race file per round, in the column format of
`seasons/dtm-1991/research/results/` (`pos,number,driver,entrant,car,laps,time,gap,fastest_lap,status,notes`).
Driver names, numbers, entrant and car strings come from `../entries.csv`.

## How the files are built

**Qualifying (`NN-<venue>-qualifying.csv`)**
- `pos` is the final qualifying position, before grid penalties.
- `time` is the driver's best valid lap from any session (Q1 to Q4). The session is named in `notes`.
- `gap` is measured from the quickest valid lap of the whole qualifying, not from the pole time. In 2013 the Q4 shoot-out lap was often slower than Q3 or even Q2, so "best lap" and "position" do not line up.
- `notes` lists every session time with its session rank, the actual grid slot and any penalty.
- Deleted laps are not used for `time`. These are Wickens in Q4 at Hockenheim 1, Glock in Q4 at Hockenheim 2, and all of Tomczyk's laps at Brands Hatch.

**Race (`NN-<venue>-race.csv`)**
- The winner's row has the race time. Every other car on the lead lap has `time` = winner's time + official gap, worked out here by addition. `gap` is the official gap.
- For lapped cars, `gap` is "+N lap(s)" and `time` is left empty.
- Retirements that still reached 75% of the distance are classified, as in the official results, and keep their `pos`. Other retirements have an empty `pos` and status `DNF`.
- `notes` give the grid slot, the tyre sequence (Soft = option, Prime = standard, Wet = rain tyre), points, and any penalties.
- `fastest_lap` is each driver's best race lap.

## Sources per round

Main source for every round is the per-race page on the DTM fan wiki. These pages hold the Q1-Q4 times for every driver, the race classification, tyre strategies and per-driver fastest laps. The wiki compiled them from dtm.com news and results.motorsportstats.com. I pulled them through the MediaWiki API, `https://dtm.fandom.com/api.php?action=query&prop=revisions&rvprop=content&titles=<page>`.

| Rd | Fan-wiki page | Further sources (cited by the wiki or checked here) |
|---|---|---|
| 1 | https://dtm.fandom.com/wiki/2013_Hockenheim_Opening_Race | dtm.com/en/news/timo-scheider-claims-pole-position-hockenheim-2013-05-04.html; dtm.com/en/news/wittmann-and-merhi-dropped-grid-2013-05-05.html; dtm.com/en/news/1-2-bmw-hockenheim-season-opener-2013-05-05.html; https://www.touringcartimes.com/2013/05/05/augusto-farfus-wins-hockenheim-sizzler/; https://results.motorsportstats.com/results/2013-hockenheim-3; https://www.crash.net/dtm/results/190785/1/dtm-hockenheim-2013-race-results |
| 2 | https://dtm.fandom.com/wiki/2013_Brands_Hatch_Race | dtm.com/en/news/martin-tomczyk-claims-pole-position-brands-hatch-2013-05-18.html; dtm.com/en/news/car-underweight-tomczyk-loses-pole-position-rockenfeller-2013-05-18.html; https://press.bmwgroup.com/global/article/detail/T0142004EN (Tomczyk 41.158); https://www.autosport.com/dtm/news/107513/tomczyk-loses-brands-dtm-pole; https://www.crash.net/dtm/results/191378/1/dtm-brands-hatch-2013-race-results (checked: top 6, Paffett 5 s penalty, FL 42.124) |
| 3 | https://dtm.fandom.com/wiki/2013_Spielberg_Race | dtm.com/en/news/bmw-claims-front-row-grid-red-bull-ring-2013-06-01.html; dtm.com/en/news/bmw-scores-1-2-3-spielberg-2013-06-02.html |
| 4 | https://dtm.fandom.com/wiki/2013_Lausitzring_Race | dtm.com/en/news/maiden-dtm-pole-position-christian-vietoris-2013-06-15.html; dtm.com/en/news/timo-glock-dropped-three-places-2013-06-15.html; dtm.com/en/news/penalties-bmw-drivers-wittmann-hand-priaulx-and-tomczyk-2013-06-16.html; https://results.motorsportstats.com/results/2013-lausitzring |
| 5 | https://dtm.fandom.com/wiki/2013_Norisring_Race | dtm.com/en/news/robert-wickens-claims-his-maiden-dtm-pole-position-2013-07-13.html; dtm.com/en/news/rockenfeller-and-molina-relegated-2013-07-14.html; dtm.com/en/news/dmsb-appeal-court-confirms-ekstr-m-s-disqualification-2013-07-31.html |
| 6 | https://dtm.fandom.com/wiki/2013_Moscow_Raceway_Race | dtm.com/en/news/mike-rockenfeller-pole-dtm-premiere-moscow-2013-08-03.html; dtm.com/en/news/rockenfeller-becomes-first-dtm-race-winner-russia-2013-08-04.html; https://results.motorsportstats.com/results/2013-moscow-2 |
| 7 | https://dtm.fandom.com/wiki/2013_N%C3%BCrburgring_Race | dtm.com/en/news/farfus-and-wittmann-front-row-grid-eifel-2013-08-17.html; https://www.crash.net/dtm/race-report/194619/1/wickens-wins-nurburgring-thriller; https://results.motorsportstats.com/results/2013-nurburgring |
| 8 | https://dtm.fandom.com/wiki/2013_Oschersleben_Race | https://www.motorsport.com/dtm/news/bruno-spengler-is-back-pole-position-at-oschersleben/440211/; https://www.motorsport.com/dtm/news/spengler-loses-pole-position-green-moves-up/440219/; https://www.crash.net/dtm/race-report/195800/1/farfus-takes-commanding-oschersleben-win |
| 9 | https://dtm.fandom.com/wiki/2013_Zandvoort_Race | https://www.motorsport.com/dtm/news/maiden-pole-for-marco-wittmann-at-zandvoort/440949/; https://www.crash.net/dtm/race-report/196422/1/rockenfeller-champion-farfus-takes-win; https://results.motorsportstats.com/results/2013-zandvoort |
| 10 | https://dtm.fandom.com/wiki/2013_Hockenheim_Finale_Race | https://www.motorsport.com/dtm/news/bruno-spengler-claims-final-dtm-pole-of-the-year/442045/; https://www.touringcartimes.com/2013/10/20/timo-glock-wins-wet-hockenheim-thriller/ (checked: top 10 and winner time 1:16:44.053); https://www.touringcartimes.com/2013/10/19/bruno-spengler-takes-dominant-pole-in-hockenheim-season-finale (Glock Q4 lap deleted for track limits) |

Season-level cross-check: https://en.wikipedia.org/wiki/2013_DTM_season. Pole, fastest lap and winner match for all 10 rounds, and Wittmann's Hockenheim 2 result is shown as DSQ there too.

## Verified vs uncertain

**Verified by two or more independent sources:**
- Pole, race fastest lap and winner for every round. The fan wiki, en.wiki and `../calendar.csv` all agree.
- Winner race times and the top-10 gaps at Brands Hatch (crash.net) and Hockenheim 2 (touringcartimes).
- Tomczyk's Brands Hatch exclusion and his 41.158 Q4 lap.
- Glock's deleted Q4 lap at Hockenheim 2.
- Ekström's Norisring disqualification, with no winner declared.

**Single source (fan wiki only), believed accurate but not checked against official timing:**
- Every Q1-Q4 time and session rank.
- All race gaps outside the checks above.
- Per-driver race fastest laps.
- Tyre sequences.
- Laps for retired cars.

The fan wiki had two driver-number typos. Both are corrected in the CSVs: Spengler is listed as #19 in the Red Bull Ring race table (he is #1), and Glock as #16 in the Hockenheim 2 qualifying table (he is #22).

**Open / uncertain:**
- Brands Hatch: Tomczyk's per-session times (Q1-Q3) were not found. His `time` cell is empty.
- Hockenheim 2: the reason for Marco Wittmann's disqualification was not found. The fan-wiki footnote is blank and en.wiki gives no reason. One search summary mentioned a missed post-race weighing, but no source confirmed it.
- Norisring: positions are kept as officially listed. Wickens is P2 and there is no P1. Ekström's race time and gap are not available.
- Hockenheim 1 qualifying ran on a drying track: Q1-Q2 about 1:49, Q3 about 1:39-1:43, Q4 about 1:36. Only the Q3/Q4 times are representative of dry pace.
- Moscow: the Q4 shoot-out was cancelled, because the rescue helicopter could not fly during an air-force flypast escorting President Putin. The top-4 grid follows Q3.
- Official dtm.com timing PDFs could not be retrieved. dtm.com's 2013 archive is gone and archive.org was offline during this research.

## Speed trap / top speed

No 2013 DTM speed-trap figures (official timing "speeds" sheets) were found for any venue. The cells are deliberately left empty. Only indirect figures were found:
- **DRS:** the rear wing flap opens 15°, worth about +5 to 7 km/h on the straight (touringcartimes, 2013-04-09: https://www.touringcartimes.com/2013/04/09/drs-and-option-tyres-confirmed-for-2013-dtm). DTM itself quoted up to about 10 km/h (see `../season.md`).
- **Hockenheim, Parabolika to hairpin:** preview articles quote "about 260 km/h" and "about 270 km/h". These are estimates, not measured values.
- **BMW M3 DTM (E92):** BMW quotes a top speed of "approx. 300 km/h". This is a generic specification, not a trap reading.

If official timing PDFs turn up, look for the "Speed trap" / "Maximum speeds" sheet that goes with each race.

## Real race durations

All races were scheduled by distance, with a 75-minute time limit that applied in the two rain races.

| Rd | Venue | Laps (sched.) | Laps run | Winner | Winner's time |
|---|---|---|---|---|---|
| 1 | Hockenheim | 42 | 42 | Farfus | 1:10:11.583 |
| 2 | Brands Hatch Indy | 98 | 98 | Rockenfeller | 1:11:28.719 |
| 3 | Red Bull Ring | 47 | 47 | Spengler | 1:08:35.249 |
| 4 | Lausitzring | 52 | 52 | Paffett | 1:09:58.562 |
| 5 | Norisring | 83 | 83 | (none; Wickens first classified) | 1:12:17.344 (Wickens) |
| 6 | Moscow Raceway | 74 | 74 | Rockenfeller | 1:14:38.512 |
| 7 | Nürburgring | 49 | 45 (75-min limit, wet) | Wickens | 1:15:33.710 |
| 8 | Oschersleben | 51 | 51 | Farfus | 1:11:40.894 |
| 9 | Zandvoort | 44 | 44 | Farfus | 1:13:26.294 |
| 10 | Hockenheim | 42 | 41 (75-min limit, wet) | Glock | 1:16:44.053 |

The `laps_per_heat` values in `../calendar.csv` are the laps actually run. For Nürburgring (49 → 45) and Hockenheim 2 (42 → 41) the scheduled distance was longer. Norisring is confirmed at 83 laps, which settles the 82-vs-83 question in `../season.md`.
