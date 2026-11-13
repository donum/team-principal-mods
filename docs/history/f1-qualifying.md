# F1 qualifying formats, 1950 to 2026

Part of a series on how F1 rules changed (qualifying, points, tyres, pit
stops). Each file has the table, the sources and a Discord post. The table
image is made with `python -I tools/history_table.py docs/history/f1-qualifying.md`.

`(?)` marks a detail that the sources we read did not confirm. Check it
before you rely on it.

## Table

| Years | Format | How the grid is set | Fuel and tyres | Quirks |
|---|---|---|---|---|
| 1950 to 1960s | Practice times | Fastest lap from any practice session. Several sessions over two or three days, no lap limit. | Free. | The Indianapolis 500 counted for the championship until 1960 and kept its own qualifying (?). The number of starters was set per track, small at Monaco (?). |
| 1970s to 1992 | Two timed sessions | One hour on Friday and one on Saturday (Thursday at Monaco). The best lap from either day counts. | Qualifying tyres that last one or two laps (?). In the turbo years, extra boost and qualifying engines (?). | If Saturday is wet, Friday decides the grid. Pre-qualifying in the late 1970s and again from the late 1980s: the worst teams of the last 12 months run first, usually 4 go through, 30 cars fight for 26 places. Up to 39 entries. Pre-qualifying ended after Hungary 1992. |
| 1993 to 1995 | Two sessions, 12 laps | Friday and Saturday, one hour each. Best lap from either day counts. | 12 laps per driver per session (start year ?). | Fewer entries, so everyone who turns up starts. |
| 1996 to 2002 | One hour, Saturday | One session, 12 laps. Best lap counts. | Free fuel. | 107% rule: slower than 107% of pole does not start, unless the stewards allow it (13 of 37 were allowed, often after rain). Jerez 1997: three drivers set the same time to the thousandth. The first to set it got the better spot. |
| 2003 | One lap, two days | Friday: one lap each, order by championship. It only sets Saturday's order. Saturday: one lap each, slowest from Friday first. That lap sets the grid. | Saturday on race fuel. Parc fermé until the race, no refuelling. | Lighter fuel buys a better grid spot but means an earlier stop. Pole stops meaning "fastest car". 107% rule gone. |
| 2004 | Two single laps, Saturday | Run 1 in the order of the last race result. Run 2 in reverse order of run 1 (?). Run 2 sets the grid. | Run 2 on race fuel (?). | The two runs moved apart during the year. |
| 2005, rounds 1 to 6 | Aggregate | One lap Saturday plus one lap Sunday morning. The two times are added up. | Sunday lap on race fuel. | Hard to follow for fans and TV. Dropped after Monaco. |
| 2005, from round 7 | One lap, Saturday | One lap each, order is the reverse of the last race result. | Race fuel and race tyres. | The race winner goes out last, on the best track. |
| 2006 to 2007 | Knockout Q1/Q2/Q3 | 22 cars. Q1 and Q2 15 min, 6 out each. Top 10 in Q3. Unlimited laps. | Q3 cars start with race fuel and burn it off. Laps run in Q3 are paid back before the race ("fuel burn"). | Q3 was 20 min, cut to 15 from France 2006. Q3 was mostly slow laps to burn fuel. Monaco 2006: Schumacher stopped at Rascasse and was sent to the back. |
| 2008 to 2009 | Knockout, race fuel in Q3 | Q1 20, Q2 15, Q3 10 min. 6 out each, 5 out each once Super Aguri left in May 2008 (20 cars). | Q3 on race fuel. No fuel added back. | Top 10 still on heavy fuel, so a car from 11th could start lighter. |
| 2010 to 2013 | Knockout, low fuel | 24 cars, 7 out in Q1 and Q2 (2010 to 2012). 22 cars from 2013, 6 out. Q1 20, Q2 15, Q3 10 min (?). | Refuelling banned, so everyone runs light. Top 10 start on the tyres of their fastest Q3 lap. | 107% rule back from 2011, for Q1 only. HRT missed the cut in Australia 2011 and 2012. |
| 2014 to 2015 | Knockout | Q1 18, Q2 15, Q3 12 min. 22 cars, 6 out (2014). 20 cars, 5 out (2015). | Top 10 start on the tyres of their fastest Q2 lap (from 2014 or 2016, sources differ). | 107% relaxed early in 2014 for the new engines. |
| 2016, rounds 1 and 2 | Elimination | Same three parts, but from a few minutes in, the slowest car drops out every 90 seconds (?). 8 cars in the final part. | Top 10 start on Q2 tyres. | Cars sat in the pits at the end, Q3 finished with nobody running. Dropped after Bahrain, knockout back from China. |
| 2016 to 2021 | Knockout | 18/15/12 min. 22 cars in 2016 (6 out), then 20 cars (5 out). | Top 10 start on the tyres of their fastest Q2 lap. Extra soft set for Q3. | From 2018 the 107% rule does not apply in the wet. |
| 2021 | Knockout plus sprint qualifying | 3 weekends: Friday qualifying sets the grid for a 100 km Saturday sprint, the sprint sets the race grid. | Friday session soft tyres only. | The sprint winner gets pole, not the fastest in qualifying. Points 3-2-1. |
| 2022 | Knockout plus sprint | Same, now called "sprint". Qualifying winner is the official pole. | Top 10 tyre rule dropped: free choice of start tyre. | Sprint points 8 to 1 for the top 8. |
| 2023 | Knockout plus sprint shootout | 6 weekends. Friday qualifying sets the race grid. Saturday shootout (12/10/8 min) sets the sprint grid. | Shootout: new mediums in SQ1 and SQ2, softs in SQ3. Hungary and Monza: hard, medium, soft for Q1, Q2, Q3 with 11 sets instead of 13. | Norris had no softs left for SQ3 in Baku, so used softs were allowed from Austria. |
| 2024 to 2025 | Knockout plus sprint qualifying | Sprint qualifying on Friday, sprint and race qualifying on Saturday. | Same tyre rules for sprint qualifying. | Parc fermé twice: from sprint qualifying to sprint, from qualifying to race. |
| 2026 | Knockout, 22 cars | Q1 18, Q2 15, Q3 13 min. 6 out in Q1 and Q2. | Free start tyre. | 11 teams with Cadillac. Six sprint weekends (?). |

## Rules across all years

- No time set (crash, breakdown, penalty): start from the back.
- Grid of two cars per row, staggered. Older grids had 4-3-4 or 3-2-3 rows (?).
- No championship points for pole, ever. (Sprint points are for the sprint.)

## Sources

- Wikipedia, "Formula One race weekend" (qualifying, sprint and
  pre-qualifying sections), "107% rule", "Formula One tyres".
- Wikipedia season articles 2005, 2006, 2008, 2010, 2014, 2016, 2023, 2026.
- Not read yet, worth checking for the `(?)` items: the FIA sporting
  regulations per year, and season articles 1993, 2004, 2007, 2011 to 2013.
- Open conflicts: 107% rule ended at Japan 2002 or with 2003. Q1 went to 18
  minutes in 2010 or 2014. Top 10 Q2 tyre rule from 2014 or 2016.

## Discord post

=== post | F1 qualifying history | f1-qualifying
## Every F1 qualifying format, 1950 to 2026

Hey! While building the qualifying stages idea I went through every F1 qualifying format. I put them into one table (picture below). Some highlights:

- **1950s to 1992**: best lap from all the sessions counts. Friday and Saturday, pick the better one. Pre-qualifying when up to 39 cars entered for 26 places.
- **1996 to 2002**: one hour on Saturday, 12 laps, and the 107% rule.
- **2003 to 2005**: one lap, alone on track, on race fuel. In 2005 even two laps added up, Saturday plus Sunday morning. Dropped after six races.
- **2006 on**: knockout Q1 to Q3. Fuel burn in Q3 (2006 to 2007), race fuel (to 2009), then low fuel.
- **2016**: elimination every 90 seconds, gone after two races.
- **2021 on**: sprint weekends, with the grid for the race set three different ways in five years.

Fun ones: three drivers with the exact same pole time (Jerez 1997), and in 2021 the sprint winner got pole, not the fastest in qualifying.

Almost all of these are a short list of stages: timed, knockout, single lap, aggregate, elimination. Plus a few settings per stage: fuel, tyres, lap limit, 107%. That's why I think the stage list from my earlier post would cover all of F1's history, not only DTM.

Next up: points, tyres and pit stops. If you spot a mistake in the table, tell me!
