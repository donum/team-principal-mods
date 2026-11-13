# F1 points systems, 1950 to 2026

Part of a series on how F1 rules changed (qualifying, points, tyres, pit
stops). Each file has the table, the sources and a Discord post. The table
image is made with `python -I tools/history_table.py docs/history/f1-points.md`.

`(?)` marks a detail that the sources we read did not confirm. Check it
before you rely on it.

## Table

| Years | Race points | Extra points | Results that count | Constructors | Quirks |
|---|---|---|---|---|---|
| 1950 to 1953 | 8-6-4-3-2 (top 5) | Fastest lap 1 | Best 4 | No title yet | Shared drives: the points are split equally, however many laps each driver did. The Indianapolis 500 counts for drivers until 1960. |
| 1954 to 1957 | 8-6-4-3-2 | Fastest lap 1 | Best 5 (?) | No title yet | British GP 1954: seven drivers set the same fastest lap and got 1/7 point each. A driver who shared two cars only got his best finish. |
| 1958 to 1959 | 8-6-4-3-2 | Fastest lap 1 | Best 6 (1958), best 5 (1959) | New in 1958. Only the best car of each make scores, privateers included. | Shared drives no longer score. Formula 2 cars in the German GP get no points. Indy 500 points go to drivers only. |
| 1960 | 8-6-4-3-2-1 (top 6) | None | Best 6 | Best car only | Fastest lap point gone. |
| 1961 to 1966 | 9-6-4-3-2-1 | None | Best 5 or 6, changes almost every year | Best car only. 1961: constructors still 8 for a win. | 1964: Graham Hill scored more points in total, but Surtees was champion after the dropped results (?). |
| 1967 to 1980 | 9-6-4-3-2-1 | None | Split season: best N from the first half plus best N from the second half (e.g. 1967: 5 of the first 6, 4 of the last 5) | Best car only until 1978. All cars from 1979 (?). | The split changes every year with the calendar. 1975 Spain: first half points race, Lella Lombardi scored 0.5, still the only woman to score. |
| 1981 to 1990 | 9-6-4-3-2-1 | None | Best 11 (1981 maybe best 10 (?)) | All cars | 1988: Prost scored 105 points, Senna 94. Only 11 results counted: Senna 90, Prost 87. Senna was champion. |
| 1991 to 2002 | 10-6-4-3-2-1 | None | All results | All cars | A win is worth more than before. Australia 1991: 14 laps in the rain, half points. |
| 2003 to 2009 | 10-8-6-5-4-3-2-1 (top 8) | None | All results | All cars | Second place gets closer to a win, so titles stay open longer. 2009: a medal system (most wins takes the title) was announced and then dropped (?). Malaysia 2009: half points. |
| 2010 to 2018 | 25-18-15-12-10-8-6-4-2-1 (top 10) | None | All results | All cars | 2014: double points at the last race, Abu Dhabi. Used once. |
| 2019 to 2020 | 25 to 1, top 10 | Fastest lap 1, only if in the top 10 | All results | Fastest lap point counts for the team too (?) | Teams pit late for fresh tyres just for the point. |
| 2021 | 25 to 1, top 10 | Fastest lap 1. Sprint 3-2-1. | All results | All cars | Spa 2021: no racing laps behind the safety car, still half points for the top 10. |
| 2022 to 2024 | 25 to 1, top 10 | Fastest lap 1. Sprint 8-7-6-5-4-3-2-1. | All results | All cars | Shortened races get a sliding scale (below). Japan 2022: 28 of 53 laps, but full points because of a gap in the rules, and Verstappen won the title that day. Fixed for 2023. |
| 2025 to 2026 | 25 to 1, top 10 | Sprint 8 to 1. No fastest lap point. | All results | All cars | Fastest lap point dropped. |

## Shortened races

| Years | Distance done | Points |
|---|---|---|
| 1975 to 1976 | under 30% / 30 to 60% / over 60% | none / half / full |
| 1980 to 2021 | under 2 laps / 2 laps to 75% / over 75% | none / half / full |
| 2022 on | under 2 laps | none |
| 2022 on | 2 laps to 25% | top 5: 6-4-3-2-1 |
| 2022 on | 25 to 50% | top 9: 13-10-8-6-5-4-3-2-1 |
| 2022 on | 50 to 75% | top 10: 19-14-12-10-8-6-4-3-2-1 |
| 2022 on | over 75% | full points |

## Rules across all years

- Points are only for race positions. Never for pole or laps led.
- Same points: the driver with more wins is ahead, then more 2nd places,
  and so on (?).
- The dropped results rule ended after 1990. Since 1991 every result
  counts.

## Sources

- Wikipedia, "List of Formula One World Championship points scoring
  systems" (read in full, but the table columns did not come through
  cleanly for some years).
- Filled from general knowledge, marked `(?)` where unsure: the 1954 to
  1957 count, 1964 and 1988 title stories (1988 is well known), the 1979
  constructors change (the page says "up until 1979"), 1981 best 10 or 11,
  the tie-break rule, the 2009 medal plan.

## Discord post

=== post | F1 points history | f1-points
## Every F1 points system, 1950 to 2026

Part two of the rules history (after qualifying). The table is below. What stood out to me:

- **Only some results counted until 1990.** From 1967 to 1980 even split by season half: e.g. best 5 of the first 6 races plus best 4 of the last 5. In 1988 Prost scored more points than Senna, but Senna was champion.
- **The winner got 8, 9, 10 and now 25 points.** Each change made 2nd place worth more or less compared to a win.
- **Bonus points come and go:** fastest lap (1950 to 1959 and 2019 to 2024), double points once (Abu Dhabi 2014), sprint points since 2021.
- **Constructors** only from 1958, and until 1978 only the best car of each make scored.
- **Shared drives** in the 1950s split the points. Seven drivers once shared one fastest lap point.
- **Shortened races:** half points, and since 2022 a scale in four steps. Japan 2022 still got full points because of a gap in the rules.

For the game this is mostly a points table per championship and per session (race, sprint), plus a few rules: best N results (also split by season half), fastest lap point with a condition, shared drives, a scale for shortened races, a multiplier for one race. With those, every season since 1950 works, and DTM too.

Next up: tyres. Mistakes? Tell me!
