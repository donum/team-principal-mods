# DTM race format, 1984 to 2026

Part of the DTM rules history (qualifying, race format, pit stops and
tyres, points, weight balancing). Made from the season research in
`seasons/<id>/research/` and the rulebook page `docs/dtm_rules.html`.
The table image is made with
`python -I tools/history_table.py docs/history/dtm-race-format.md`.

`(?)` marks a detail the research files flag as unverified or
conflicting. No DTM ran from 1997 to 1999.

## Table

| Years | Races per round | Length | Start | Overtaking aids and race control |
|---|---|---|---|---|
| 1984 to 1987 | Mostly one race. Some rounds ran two heats with half points each (AVUS, Nürburgring, Hockenheim 1984, Erding and Diepholz 1985). | About 100 to 114 km. | Standing. | Zolder 1986: red flag, restart, result on aggregate. |
| 1988 to 1992 | Two races or heats, about 15 minutes apart. | About 100 km each. | Standing (?). Heat 2 grid from the heat 1 order. | |
| 1993 to 1996 | Two heats. | 95 to 104 km each. | Standing (?). | 1995: heats 30 minutes apart, 22 minutes for repairs. |
| 2000 | Two races, equal points. | About 100 km or 40 minutes. | Rolling. | |
| 2001 | Qualifying race plus main race. | 30 to 35 km, then about 100 km. | Rolling. | |
| 2002 | Qualifying race plus main race. | Same. | Standing again. | |
| 2003 to 2011 | One race. | About one hour, 150 to 200 km. | Standing (?). | 2007: pit lane closed under the safety car. 2010 and 2011: time limit, Brands Hatch stopped at 88 of 98 laps. |
| 2012 | One race. | Set per track. | Standing. | |
| 2013 | One race. | Set per track. Wet Nürburgring and the Hockenheim final limited to 75 minutes. | Standing. | DRS once per lap anywhere on track, within 2 s, race only, not in the first or last 3 laps. |
| 2014 | One race. | Set per track. | Standing (?). | DRS now to the end of the race. |
| 2015 | Two races. | Saturday 40 min, Sunday 60 min, each plus one lap. | Standing (?). | DRS up to 3 times per lap, within 1 s, anywhere. |
| 2016 | Two races. | Same. | Standing (?). | DRS from lap 2 within 1 s, a number of uses per race by track length. |
| 2017 to 2018 | Two races. | Both 55 min plus one lap. | Standing (?). | No radio from team to driver (2017). |
| 2019 | Two races. | 55 min plus one lap, up to 2 laps added for the safety car. Round 1 on fixed laps. | Standing (?). | Push-to-pass +30 hp, 12 times per race. DRS within 3 s, in the last 5 laps everyone but the leader. |
| 2020 | Two races. | 55 min plus one lap. | Standing (?). | Push-to-pass +60 hp. DRS without limits. |
| 2021 | Two races. | 55 min plus one lap. | Rolling, two abreast. | GT3 cars, ABS and traction control allowed. |
| 2022 | Two races. | 55 min plus one lap. | Rolling. | Full-course yellow at 60 km/h. |
| 2023 to 2024 | Two races. | 60 min plus one lap. | Rolling, in a marked start corridor. | Penalty lap of about 5 s for small offences. |
| 2025 to 2026 | Two races. | 55 min plus one lap, up to 2 safety car laps added. | Rolling. | |

## Sources

- `seasons/dtm-<year>/research/season.md` for every season, summed up in
  `docs/dtm_rules.html`.
- Gaps: heat 2 grids in 1984 and 1985, race lengths per track 2012 to
  2014. Standing starts outside 1984, 2002 and 2012 are not stated in the
  research, marked `(?)`.

## Discord post

=== post | DTM race format history | dtm-race-format
## DTM race format, 1984 to 2026

Part two of the DTM rules history. The table is below. What stood out to me:

- **Heats:** two races per round with heat 2 starting in the heat 1 order (1988 to 1996). In 1984 and 1985 some rounds paid half points per heat.
- **Laps vs time:** 100 km sprints, then one-hour races, then "minutes plus one lap" since 2015 (40, 55 or 60), with up to two laps added for the safety car (2019, 2025).
- **Rolling starts** in 2000 and 2001, and again since 2021, two abreast in a marked corridor.
- **DRS in many shapes:** anywhere on track once per lap (2013), three times per lap (2015), a budget per race by track length (2016), within 3 s and free for all but the leader in the last 5 laps (2019).
- **Push-to-pass** in 2019 and 2020: +30 hp, then +60 hp, 12 times per race.
- **Race control:** pit lane closed under the safety car (2007), full-course yellow (2022), penalty lap (2023).

For the game: a race length in laps, time or both, start type, a grid rule for the second race, and an overtaking aid with uses per lap or race, a gap and a lap window. That's the same list as for F1.

Mistakes? Tell me!
