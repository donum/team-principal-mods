# F1 money and testing, 1950 to 2026

Part of a series on how F1 rules changed (qualifying, points, tyres, pit
stops, race format, safety car, overtaking aids, engines, parc fermé and
weight, money and testing). Each file has the table, the sources and a
Discord post. The table image is made with
`python -I tools/history_table.py docs/history/f1-money-testing.md`.

`(?)` marks a detail that the sources we read did not confirm. Check it
before you rely on it.

## Table

| Years | Money | Spending limits | Testing | Quirks |
|---|---|---|---|---|
| 1950 to 1973 | Each race organiser pays teams to start: start money and prize money per race (?). | None. | Free: test whenever and wherever you want. | Teams deal with every organiser on their own (?). |
| 1974 to 1980 | FOCA founded in 1974 to sell the teams as one package. Ecclestone runs it from 1978. | None. | Free. | Fights between FOCA and the governing body (FISA) about rules and money. |
| 1981 to 1996 | Concorde Agreement 1981: FOCA gets the TV rights, teams must start at every race. 1987: Ecclestone's company sells the TV rights and pays the prize money. | None. | Free. Big teams have their own test teams and tracks (?). | The TV money split changes with each Concorde Agreement (1987, 1992). |
| 1997 to 2008 | New Concorde Agreements (1997, 1998), extensions to 2012. Commercial rights sold on, CVC from 2006. | None. | Free, but limited km or days by agreement in later years (?). | Teams test more km than they race. Ferrari has its own test tracks. |
| 2009 to 2013 | Concorde Agreement 2009. | A cap for 2010 was planned and dropped. Resource Restriction Agreement between the teams instead (2009), no money limit. | In-season testing banned. Wind tunnel time cut. Only pre-season tests. 2012: one in-season test at Mugello. | Teams use straight-line "filming days" and simulators instead (?). Mugello 2012: teams said the test cost more than it helped. |
| 2014 to 2020 | Deals per team (2013), Liberty Media buys F1 in 2017. | None. | Two-day tests after some races (from 2014). End-of-season young driver test dropped (?). Pre-season 8 days in 2019. | Small teams can't afford to test, big teams can. |
| 2021 to 2025 | Concorde Agreement 2021: new prize money split. A new team pays 200 million USD to the others. | Cost cap 145 million USD (2021), then lower (see below). Drivers, top three managers and marketing not counted. | Pre-season 3 days. Wind tunnel and CFD time by championship position: last place gets the most. From 2022: rookies must drive FP1 twice per team per season, four times from 2025. | 2021: Red Bull went slightly over the cap. Penalty: a 7 million USD fine and 10% less wind tunnel time for a year. |
| 2026 | Concorde Agreement 2026 to 2030, signed by all 11 teams. Cadillac pays 450 million USD to join. | Cost cap 215 million USD, more costs now inside it. Engine makers: own cap, 130 million USD. | Three pre-season tests for the new cars, the first one private in Barcelona. | Williams missed the first test. |

## Cost cap by year

| Years | Team cost cap | Notes |
|---|---|---|
| 2021 | 145 million USD | base for 21 races, more for each extra race |
| 2022 | 140 million USD | raised by 3.1% mid-season for inflation |
| 2023 to 2025 | 135 million USD | plus race count and inflation adjustments |
| 2026 | 215 million USD | more costs moved inside the cap |
| Engines 2023 to 2025 | 95 million USD | |
| Engines 2026 | 130 million USD | |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Prize money by position | Yes | `prize_money_distribution` |
| Cost cap | No |  |
| Testing limits | Yes | `private_testing_limits` (laps), test weeks |
| Wind tunnel time by position | No | the wind tunnel is only a factory level |
| Fee for a new team | Partly | a fee per entry (`FORMULA_ENTRY_ADMIN_FEE_M`) |
| Sponsors, budgets, salaries | Yes | built in |

## Sources

- Wikipedia, "Concorde Agreement" (every agreement, 200 million fee,
  Cadillac 450 million, 2026 agreements), "Formula One Group" (FOCA 1974,
  TV rights 1981 and 1987, CVC, Liberty), season articles 2009, 2012,
  2014, 2021, 2022 and 2026 (via summaries: testing ban, Mugello, 2014
  tests, cost caps, Red Bull breach, rookie rule).
- Not found: a Wikipedia page on F1 testing or on the cost cap.
- Wikipedia "Formula One Teams Association" and RaceFans 2009 (2010 cap
  dropped, Resource Restriction Agreement). Autosport and Motor Sport 2022
  (Red Bull fine and wind tunnel cut). Williams F1 and Autosport (rookie
  FP1 rule, two per team 2022 to 2024, four from 2025).
- Not confirmed, marked `(?)`: start money, testing before 2009, filming
  days, the end of the young driver test (it came back after Abu Dhabi
  in later years).

## Discord post

=== post | F1 money and testing history | f1-money-testing
## F1 money and testing, 1950 to 2026

Part ten of the rules history, the one closest to a manager game. The table is below. What stood out to me:

- **Money first came from each race organiser.** From 1974 the teams sold themselves as one package (FOCA), from 1981 the TV rights were theirs. Every Concorde Agreement since then changed how the prize money is split.
- **No spending limit until 2021.** A cap was planned for 2010 and dropped. Since 2021 there's a cost cap: 145 million USD, then lower, and 215 million from 2026 with more costs inside it. Engine makers have their own cap.
- **Testing was free until 2008.** Then in-season testing was banned, wind tunnel time cut, and today there are only a few pre-season days.
- **Wind tunnel time by championship position:** the last team gets the most.
- **New teams pay to join:** 200 million USD (2021), Cadillac 450 million (2026).
- **Rookies must drive in FP1** a few times per season (since 2022).

For the game this is the team boss part: prize money per position, a cost cap with what counts and what doesn't, a penalty for breaking it, testing days, and development time that depends on the standings. The game already has a budget, so most of this would be settings per season.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
