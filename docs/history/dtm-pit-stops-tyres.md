# DTM pit stops and tyres, 1984 to 2026

Part of the DTM rules history (qualifying, race format, pit stops and
tyres, points, weight balancing). Made from the season research in
`seasons/<id>/research/` and the rulebook page `docs/dtm_rules.html`.
The table image is made with
`python -I tools/history_table.py docs/history/dtm-pit-stops-tyres.md`.

`(?)` marks a detail the research files flag as unverified or
conflicting. No DTM ran from 1997 to 1999.

## Table

| Years | Mandatory stops | Fuel | Tyres | Stop rules |
|---|---|---|---|---|
| 1984 to 1987 | None. Stops only for damage or tyres. | | Open tyre war, each team picks its make. | |
| 1988 to 1996 | None. | No refuelling between the two races (1988). | 10 tyres per weekend (1988). | Stops for tyres or damage only (1993). |
| 2000 | None. | | Dunlop control tyre, 5 sets per weekend. | |
| 2001 to 2002 | One in the main race, all four tyres. | No refuelling. | Control tyre. | A 25-minute service window between the races for fuel, tyres and repairs (2001). |
| 2003 to 2007 | Two, with tyre changes. | Refuelling from churns, 70 litre tank (2003). | 9 sets (2005), 7 sets (2006). Tyre warmers banned (2003). | |
| 2008 | Two, both in the middle third of the race. From mid-season: in the 2nd and 3rd quarters. | Refuelling. | | |
| 2009 to 2011 | Two. | Refuelling, last year 2011. | Hankook control slick and wet (2011). | |
| 2012 | Two, each inside a window. | No refuelling, 120 litre tank. | | |
| 2013 | Two, no window, none in the first or last 3 laps. | No refuelling. | One option set per race, every driver must use it. | Stops for damage don't count. |
| 2014 | One, in the middle third of the race. | | Option tyre for at most half the distance. | Not under the safety car. No window in wet races. |
| 2015 to 2016 | Saturday none, Sunday one. | | 4 slick sets for both qualifyings and both races. Option tyre gone. | |
| 2017 to 2018 | One per race. | | | 8 mechanics, one wheelgun per side, tyre warmers banned. |
| 2019 to 2020 | One per race. | | 7 slick sets, at most 2 new in qualifying. | Not under the safety car. |
| 2021 | One, all four wheels. | | | A change under the safety car doesn't count. |
| 2022 | One, between minute 10 and 40. | | 3 sets per race day. | Rear wheels first, 4 wheel mechanics. Stops under the safety car count now, but not under full-course yellow. |
| 2023 | One, between minute 20 and 40. | | Pirelli, 3 or 4 new sets by track. The top 5 start on their qualifying tyres. | 6 crew, rear wheels first. A pit stop challenge award. |
| 2024 | One, between minute 20 and 40. | | The top 10 start on their qualifying tyres. | A change under safety car or full-course yellow doesn't count. |
| 2025 | Saturday one (minute 20 to 40). Sunday two (minute 10 to 20 and 39 to 45). | | 3 or 4 new sets, top 10 start on qualifying tyres. | |
| 2026 | As 2025. | | A race-day pool of 3 or 4 new sets per track, plus a test pool. A wheel that is thrown out leaves the allocation. | |

## Sources

- `seasons/dtm-<year>/research/season.md` for every season, summed up in
  `docs/dtm_rules.html`.
- Gaps: tyre suppliers and set counts are not listed for every year.

## Discord post

=== post | DTM pit stops and tyres history | dtm-pit-stops-tyres
## DTM pit stops and tyres, 1984 to 2026

Part three of the DTM rules history. The table is below. What stood out to me:

- **No stops until 2000.** An open tyre war in the 1980s, then a control tyre.
- **Stop count changes all the time:** one (2001), two with refuelling (2003 to 2011), two without (2012, 2013), one (2014), none on Saturday and one on Sunday (2015), one per race (2017), and since 2025 one on Saturday and two on Sunday.
- **Pit windows in many forms:** the middle third of the race, the 2nd and 3rd quarters, minute 10 to 40, minute 20 to 40, or two windows (10 to 20 and 39 to 45).
- **What counts as a stop:** not under the safety car, not for damage, all four wheels, later also not under full-course yellow.
- **Option tyre (2013, 2014):** one set per race that everyone must use, then at most half the distance on it.
- **Crew rules:** 8 mechanics and one wheelgun per side (2017), rear wheels first (2022).

For the game: mandatory stops per race, windows in minutes, laps or share of the race, what counts as a stop, set allocations per weekend or race day, a must-use tyre, and the start-on-qualifying-tyre rule for the top N. This is the rules engine from my earlier posts, with DTM rows.

Mistakes? Tell me!
