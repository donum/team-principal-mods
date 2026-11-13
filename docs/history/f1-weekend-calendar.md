# F1 weekend schedule and calendar, 1950 to 2026

Part of a series on how F1 rules changed (qualifying, points, tyres, pit
stops, race format, safety car, overtaking aids, engines, parc fermé and
weight, money and testing, entries and drivers, team orders, weekend and
calendar). Each file has the table, the sources and a Discord post. The
table image is made with
`python -I tools/history_table.py docs/history/f1-weekend-calendar.md`.

`(?)` marks a detail that the sources we read did not confirm. Check it
before you rely on it.

## Table

| Years | Practice | Qualifying and race days | Races per season | Quirks |
|---|---|---|---|---|
| 1950 to 1959 | Practice on one to three days, the fastest lap sets the grid. | Most races on Sunday, some on Saturday (Britain 1950). | 7 to 11. Indianapolis counts until 1960. | Few races, most in Europe. |
| 1960 to 1969 | Practice over two or three days, every session timed and counted. | | 8 to 12. | |
| 1970 to 1979 | Timed practice over two or three days. By 1980: untimed practice in the morning, timed qualifying in the afternoon, Friday and Saturday. | Monaco: practice starts on Thursday. | 11 to 17. | More races outside Europe: South Africa, Brazil, Argentina, USA, Canada, Japan. |
| 1980 to 1995 | Free practice Friday and Saturday morning, qualifying in the afternoon. Warm-up on Sunday morning. | South Africa 1985: the last race on a Saturday for almost 40 years. | 14 to 17, mostly 16. | A 16-race season for about ten years. |
| 1996 to 2002 | Two free practice sessions Friday, two of 45 minutes Saturday morning. Warm-up on Sunday until 2002. | Qualifying Saturday, race Sunday. | 16 to 17. | |
| 2003 to 2005 | Friday practice, some teams run a third car on Friday (from 2004). | Qualifying on Friday and Saturday (2003), Saturday and Sunday morning (2005, first six races). | 16 to 19. | Asia and the Middle East join: Malaysia 1999, Bahrain and China 2004. |
| 2006 to 2020 | Three sessions: FP1 and FP2 on Friday, 60 minutes each in 2006, 90 minutes from 2007. FP3 on Saturday, 60 minutes. | Qualifying Saturday, race Sunday. Monaco: practice Thursday. | 17 to 21. 2020: 17 races after the pandemic changes. | Singapore 2008: first night race. Overnight curfews for team staff from 2011. 2020: two races in a row at the same track. |
| 2021 to 2022 | All three sessions 60 minutes. Sprint weekends: one session. | Monaco moves to the normal Friday start after 2021. | 22. | Sprint weekends change Friday and Saturday. |
| 2023 to 2026 | Same. 2024: sprint weekends with one practice on Friday morning. | Las Vegas races on Saturday night (from 2023). | 22 to 24. 2026: 22, Bahrain and Saudi Arabia cancelled. | Three races in a row (triple-headers): two planned in 2023 (one run after Imola was cancelled), three in 2024. The first was in 2018. FIA minimum: 8 races. |

## Races per season

| Decade | Races per year |
|---|---|
| 1950s | 7, 8, 8, 9, 9, 7, 8, 8, 11, 9 |
| 1960s | 10, 8, 9, 10, 10, 10, 9, 11, 12, 11 |
| 1970s | 13, 11, 12, 15, 15, 14, 16, 17, 16, 15 |
| 1980s | 14, 15, 16, 15, 16, 16, 16, 16, 16, 16 |
| 1990s | 16, 16, 16, 16, 16, 17, 16, 17, 16, 16 |
| 2000s | 17, 17, 17, 16, 18, 19, 18, 17, 18, 17 |
| 2010s | 19, 19, 20, 19, 19, 19, 21, 20, 21, 21 |
| 2020 to 2026 | 17, 22, 22, 22, 24, 24, 22 |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Calendar per week, number of races | Yes | `schedule.json`, 52 weeks |
| Test weeks | Yes | `schedule.json` test |
| Two races on one weekend | No | A1, A4 |
| Practice sessions, number and length | No | one 60-minute session, fixed |
| Real dates, Thursday or Saturday races | No | A4 |

## Sources

- Wikipedia, "Formula One race weekend" (three sessions since 2006,
  session lengths before and from 2021, Monaco Thursday to 2021, Las Vegas
  Saturday, South Africa 1985, sprint practice), "List of Formula One
  seasons" (races per season), "List of Formula One Grands Prix" (8-race
  minimum).
- ESPN, Sky Sports, Autosport, March 2026 (Bahrain and Saudi Arabia
  cancelled, 22 races, no replacements).
- Open items check: Wikipedia "1950 British Grand Prix" (qualifying on
  Friday, race on Saturday). Motor Sport race database (1954 Belgian GP:
  practice Friday and Saturday; 1970 Monaco: Thursday, Friday and
  Saturday, all times count). Motor Sport, September 2004, Roebuck
  (early 1970s: every session timed). Motor Sport 1980 race reports
  (untimed morning, timed afternoon hour). Autosport warm-up reports
  and "In praise of morning warm-up", Atlas F1 2003 preview (no Sunday
  warm-up from 2003). Atlas F1 and newsonf1 2001 reports (two Friday
  sessions, Saturday sessions of 45 minutes). Autosport and Dawn, 2010
  (curfew from 2011). Autosport, GPblog and motorsport.com
  (triple-headers 2018, 2023, 2024).
- Confirmation round: Autosport, WMSC 2007 rules and other 2006
  reports (Friday sessions from one hour to 90 minutes for 2007).
  Autosport and motorsport.com, 2017 (2018 France, Austria, Britain the
  first triple-header). Top Gear and GPfans, 2023 (two planned
  triple-headers, Imola cancelled). The Drive and The Race (three in
  2024). Wikipedia "Test driver" and Autosport (third cars in Friday
  practice from 2004).
- Not found: summer break, a race limit in the Concorde Agreement, season
  start and end dates.
- Note: in years with cancelled races, the list may count planned or held
  races.

## Discord post

=== post | F1 weekend and calendar history | f1-weekend-calendar
## F1 weekend schedule and calendar, 1950 to 2026

Part thirteen and the last one of the rules history. The table is below. What stood out to me:

- **Races per season:** 7 in 1950, about 16 for most of the 1980s and 1990s, 24 in 2024 and 2025, 22 in 2026. The picture has every year.
- **Practice:** for a long time free practice plus timed qualifying on Friday and Saturday, three sessions since 2006 (90, 90, 60 minutes from 2007), all 60 minutes since 2021, and only one on sprint weekends.
- **Monaco** practised on Thursday until 2021.
- **Not always Sunday:** South Africa 1985 was the last Saturday race until Las Vegas in 2023, a Saturday night race.
- **Night races** since Singapore 2008.

For the game this is: a weekend as a list of sessions (from my weekend builder post), each with a day, a length and a type (practice, qualifying, sprint, race). Plus a calendar with dates per round, so double-headers and Thursday starts work. With that, a 1950 weekend with long practice days, a 1990s Friday and Saturday qualifying, and a 2026 sprint weekend are all the same system. DTM fits too: two races per weekend since 2015.

The last table in the picture shows what the game can do today: yes, partly or no.

That's the whole series, 13 topics. If you spot a mistake anywhere, tell me!
