# DTM qualifying formats, 1984 to 2026

Part of the DTM rules history (qualifying, race format, pit stops and
tyres, points, weight balancing). Made from the season research in
`seasons/<id>/research/` and the rulebook page `docs/dtm_rules.html`.
The table image is made with
`python -I tools/history_table.py docs/history/dtm-qualifying.md`.

`(?)` marks a detail the research files flag as unverified or
conflicting. No DTM ran from 1997 to 1999.

## Table

| Years | Format | How the grid is set | Second race or heat | Quirks |
|---|---|---|---|---|
| 1984 to 1987 | Timed practice | Best lap in timed practice and qualifying. | Where two heats ran, heat 2 grid not recorded. | |
| 1988 | Timed qualifying | Qualifying sets the race 1 grid. | Race 2 grid is the race 1 finishing order. | Mainz: 1.8 s off pole was enough to miss the race. |
| 1989 | Top-Qualifying plus qualification race | Timed qualifying, then one flying lap each for the top 16 (top 20 at Zolder). All other cars run an 8 to 22 lap qualification race for places 17 on. | Heat 2 from heat 1. | Cars that miss the cut in the qualification race don't start. |
| 1990 to 1992 | Qualification race | The top 12 in qualifying (16 in 1991 and at some 1990 rounds) go straight to the heats. The rest run a race of about 50 km for the remaining places. | Heat 2 grid is the heat 1 order. | No qualification race at the Nordschleife rounds, AVUS 1992 or the wet Eifel round 1992. 1991: qualifying split into two groups at some rounds. |
| 1993 | Top group | Timed qualifying, then a top-15 session for the front places (top 10 at Zolder, Hockenheim and the Eifel round). | Heat 2 grid is the heat 1 order, retirements at the back. | Class 1 cars, the first high-tech DTM. |
| 1994 to 1996 | Timed qualifying plus top group | Qualifying sets the heat 1 grid. The fastest cars then decide the front places: a single-lap Top Qualifying (1995), the top 10 in their own group (1996). The size of the top group in 1994 and 1995 is not confirmed (?). | Heat 2 grid is the heat 1 order. | 1995 ran as DTM and ITC, 1996 as ITC only. |
| 2000 | Timed qualifying | Qualifying sets the race 1 grid. | Race 2 grid is the race 1 finishing order. | New DTM with V8 silhouette cars. |
| 2001 to 2002 | Qualifying race | 45 minutes, at most 12 laps. Then a 30 to 35 km qualifying race on Sunday sets the main race grid. | | The qualifying race pays 3-2-1 points. |
| 2003 to 2005 | Superpole | 20 minutes, at most 9 laps, sets places 11 and down. The top 10 run one flying lap each, in reverse order. | | One lap, alone on track, for pole. |
| 2006 to 2008 | Knockout | Three parts, the slowest six drop out after each part. | | |
| 2009 to 2011 | Knockout plus Q4 | 2009: Q1 14 min, top 14 go on. Q2 10 min, top 8 go on. Q3 9 min, top 4 go on. Q4: one timed lap each. From 2010 the parts are shorter (Q3 6 min), still top 8 and top 4. | | Parc fermé before Q4. From 2010 the Q4 cars run one at a time. |
| 2012 to 2013 | Knockout plus Q4 | Q1 16 min, 22 cars cut to 16. Q2 11 min, to 10. Q3 11 min, to 4. Q4: one timed lap each. | | |
| 2014 | F1-style knockout | Q1 13 min, 23 cars cut to 18. Q2 11 min, to 8. Q3 11 min. The single-lap shootout is gone. | | |
| 2015 to 2016 | One per race | A separate 20-minute session before each race. | Own qualifying. | Two races per weekend from 2015. |
| 2017 to 2022 | One per race, with points | Separate qualifying per race. | Own qualifying. | The top 3 in each qualifying score 3-2-1 points. |
| 2023 to 2026 | Two 20-minute sessions | One qualifying per race, 3-2-1 points. | Own qualifying. | The top 5 (2023), then the top 10 (from 2024) start on the tyres they qualified on. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Timed qualifying | Yes | `qualifying_format` session_60 |
| Knockout | Partly | F1 cuts only: always 10 in Q3, no Q4 (A6) |
| Single-lap shootout (Top-Qualifying, Superpole, Q4) | No | A5 |
| Qualification race | No | A2 |
| Own qualifying per race | No | A1, A6 |
| Race 2 grid from race 1 | No | A1 |
| Qualifying points 3-2-1 | Partly | pole point only (B8) |
| Top 5 or 10 start on qualifying tyres | No | B12 |

## Sources

- `seasons/dtm-<year>/research/season.md` for every season, summed up in
  `docs/dtm_rules.html` (touringcarracing.net, de and en Wikipedia,
  period magazines, the 2023 and 2025 sporting regulations). 2012
  knockout cuts from Audi and BMW press material.
- Fact check: de.wikipedia DTM-Saison 2001 (12 laps in 45 min, 3-2-1),
  Audi press release 2006 (three parts, six out after each), Audi/BMW
  2012 reports (16, 11, 11 min), Autosport and Autobild 2014 rule changes
  (Q1 13, Q2 11, Q3 11 min), motorpasion 2010 (Q3 6 min), Motorsport.com
  2024 changes (top 10 rule, top 5 before). Q1 to Q3 lengths for 2009 and
  2011 not found.
- Open items check: crash.net 2009 rule changes (Q1 14 min and top 14, Q2
  10 min, Q3 9 min, top 4, Q4 one lap). touringcartimes 2010 Hockenheim and
  Audi 2011 Lausitz reports (ninth place misses Q3, so the top 8 go on).
  ru.wikipedia 2010 and motorpasion 2010 (shorter parts, Q4 one car at a
  time). de.wikipedia DTM-Saison 2008 (Q1, Q2, Q3 at the Nürburgring) and
  the Audi 2008 Norisring report (three segments) settle the 2008 format.
  Autosport 2000 Oschersleben and Nürburgring reports (race 1 order gives
  the race 2 grid). en.wikipedia 1996 ITC (race 2 grid from race 1) and
  the 1996 Norisring round (top 10 in qualifying group A). Motorsport.com
  1995 Norisring "Top Qualifying" quotes (one timed lap). The size of the
  top group in 1994 and 1995 was not found.
- Confirmation round: touringcarracing.net race pages 1989 to 1993 (grid
  remarks per round: top 16 Top-Qualifying in 1989, top 20 at Zolder, 12 or
  16 cars direct in 1990 to 1992, split groups in 1991, top 15 or top 10 in
  1993). Audi press 2012 and Motorsport.com 2012 Hockenheim (16, 11, 11 min,
  six out per part). Autosport and Autobild 2014 rule changes. Autobild 2006
  preview (14 and 10 min, six out). crash.net 2009 rule changes.

## Discord post

=== post | DTM qualifying history | dtm-qualifying
## Every DTM qualifying format, 1984 to 2026

After the F1 series, here's DTM. All of it comes from the research for my season packs (1984 to 2026). The table is below. What stood out to me:

- **Qualification races (1989 to 1992):** 12 to 16 cars went straight to the heats, everyone else raced about 50 km for the last places.
- **Single-lap shootouts** came back again and again: Top-Qualifying (1989), Superpole (2003 to 2005), Q4 for the top 4 (2009 to 2013).
- **A qualifying race (2001, 2002)** set the main race grid and paid 3-2-1 points.
- **Knockout** from 2006, F1-style from 2014.
- **One qualifying per race** since 2015, with 3-2-1 points for the top 3 since 2017. Since 2024 the top 10 start on their qualifying tyres.
- **The second race** used the first race's finishing order for a long time.

Almost every format here is in the F1 table too, just in a different order. A list of stages (timed, knockout, single lap, qualification race) with points per stage and a grid rule per race covers both series.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
