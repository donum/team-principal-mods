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
| 1950 to 1973 | Each race organiser pays teams to start: start money and prize money per race. | None. | Free: test whenever and wherever you want. | At first each team deals with each organiser. From 1964 the teams' association (F1CA) bargains for them, from 1973 Ecclestone signs the deals. |
| 1974 to 1980 | FOCA founded in 1974 to sell the teams as one package. Ecclestone runs it from 1978. | None. | Free. | Fights between FOCA and the governing body (FISA) about rules and money. |
| 1981 to 1996 | Concorde Agreement 1981: FOCA gets the TV rights, teams must start at every race. 1987: Ecclestone's company sells the TV rights and pays the prize money. | None. | Free. Ferrari tests at its own tracks: Fiorano (from 1972) and Mugello (from 1988). | The TV money split changes with each Concorde Agreement (1987, 1992). |
| 1997 to 2008 | New Concorde Agreements (1997, 1998), extensions to 2012. Commercial rights sold on, CVC from 2006. | None. | Free until 2004. 2005: nine teams agree on 30 test days, Ferrari does not. 2007 and 2008: 30,000 km per team. | Teams test more km than they race. Ferrari has its own test tracks. |
| 2009 to 2013 | Concorde Agreement 2009. | A cap for 2010 was planned and dropped. Resource Restriction Agreement between the teams instead (2009), no money limit. | In-season testing banned. Wind tunnel time cut. Only pre-season tests. 2012: one in-season test at Mugello. | Teams use straight-line aero tests and "filming days" instead. Mugello 2012: teams said the test cost more than it helped. |
| 2014 to 2020 | Deals per team (2013), Liberty Media buys F1 in 2017. | None. | Two-day tests after some races (from 2014). These replace the young driver test. Pre-season 8 days in 2019. | Small teams can't afford to test, big teams can. |
| 2021 to 2025 | Concorde Agreement 2021: new prize money split. A new team pays 200 million USD to the others. | Cost cap 145 million USD (2021), then lower (see below). Drivers, top three managers and marketing not counted. | Pre-season 3 days. Wind tunnel and CFD time by championship position: last place gets the most. From 2022: rookies must drive FP1 twice per team per season, four times from 2025. | 2021: Red Bull went slightly over the cap. Penalty: a 7 million USD fine and 10% less wind tunnel time for a year. |
| 2026 | Concorde Agreement 2026 to 2030, signed by all 11 teams. Cadillac pays 450 million USD to join. | Cost cap 215 million USD, more costs now inside it. Engine makers: own cap, 190 million USD. | Three pre-season tests for the new cars, the first one private in Barcelona. | Williams missed the first test. |

## Cost cap by year

| Years | Team cost cap | Notes |
|---|---|---|
| 2021 | 145 million USD | base for 21 races, more for each extra race |
| 2022 | 140 million USD | raised by 3.1% mid-season for inflation |
| 2023 to 2025 | 135 million USD | plus race count and inflation adjustments |
| 2026 | 215 million USD | more costs moved inside the cap |
| Engines 2023 to 2025 | 95 million USD | |
| Engines 2026 | 190 million USD | from a maker's first race season, 148.5 million in the years before |

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
- Open items check: Motor Sport and Autosport (Ecclestone: start money
  of about 1,000 GBP a car, agreed with each organiser), Forix 8W
  timeline (F1CA 1964, organisers sign with Ecclestone for 1973).
  Wikipedia "Fiorano Circuit" and "Mugello Circuit", Pirelli (Ferrari
  tracks). Autosport 2005 (30-day deal, Ferrari out) and October 2006
  (30,000 km for 2007), grandprix.com (30,000 km in the 2008 rules).
  Autosport 2010 (straight-line aero days, Ferrari "filming" day at
  Fiorano). Sky Sports and Autosport 2013 (the 2014 in-season tests
  replace the young driver test). A post-season test in Abu Dhabi came
  back in later years.
- Confirmation round: Wikipedia "Concorde Agreement" (1981 TV rights and
  start at every race, all agreement years, 200 million and 450 million
  fees, 2026 to 2030 agreement signed by all 11 teams), Wikipedia
  "Formula One Group" (FOCA 1974, Ecclestone chief executive 1978).
- FIA 2026 Financial Regulations for Power Unit Manufacturers, Issue 5,
  May 2026, Article E2.3 (190 million USD from a maker's first season,
  148.5 million before). Formula1.com cost cap explainer (145, 140, 135
  and 215 million; 190 million replaced the planned 130 million).
  Motorsport.com and Sky Sports, July 2022 (3.1% raise for 2022).
  Formula1.com and Racer, January 2026 (Williams missed the Barcelona
  test).
- Not settled: Forix says the F1CA was renamed FOCA in 1978, Wikipedia
  dates FOCA to 1974.

## Discord post

=== post | F1 money and testing history | f1-money-testing
## F1 money and testing, 1950 to 2026

Part ten of the rules history, the one closest to a manager game. The table is below. What stood out to me:

- **Money first came from each race organiser.** From 1974 the teams sold themselves as one package (FOCA), from 1981 the TV rights were theirs. Every Concorde Agreement since then changed how the prize money is split.
- **No spending limit until 2021.** A cap was planned for 2010 and dropped. Since 2021 there's a cost cap: 145 million USD, then lower, and 215 million from 2026 with more costs inside it. Engine makers have their own cap.
- **Testing was free until 2004.** Then limits by agreement (days, then km), from 2009 in-season testing was banned, wind tunnel time cut, and today there are only a few pre-season days.
- **Wind tunnel time by championship position:** the last team gets the most.
- **New teams pay to join:** 200 million USD (2021), Cadillac 450 million (2026).
- **Rookies must drive in FP1** a few times per season (since 2022).

For the game this is the team boss part: prize money per position, a cost cap with what counts and what doesn't, a penalty for breaking it, testing days, and development time that depends on the standings. The game already has a budget, so most of this would be settings per season.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
