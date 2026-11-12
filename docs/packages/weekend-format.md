# Package: Weekend Format and Qualifying

How the grid is set, and how a weekend is built from sessions and races.
Part of the [feature packages](README.md).

- **Wishlist items:** [A1](../DEVELOPER_WISHLIST.md#a1-several-races-per-weekend-heats--p1),
  [A2](../DEVELOPER_WISHLIST.md#a2-qualification-race--p1),
  [A3](../DEVELOPER_WISHLIST.md#a3-configurable-sessions-and-race-format--p2),
  [A5](../DEVELOPER_WISHLIST.md#a5-single-lap-shootout-q4--p2),
  [A6](../DEVELOPER_WISHLIST.md#a6-qualifying-as-a-list-of-stages--p1).
  A6 has the full per-season table.
- **Modes:** formula, oval, endurance.
- **Checked against:** game version 0.99.6 (beta). F1 and other-series facts
  are from memory and still need sources (see the evidence log).

## 1. What the game has today

| Setting | Where | What it does |
|---|---|---|
| `qualifying_format` `session_60` | `regulations.json` | One hour, best lap counts |
| `qualifying_format` `knockout` | `regulations.json` | Q1, Q2, Q3, top 10 in Q3 |
| `QUALI_GRID_LIMIT`, `QUALI_MIN_ENTRANTS` | `constants.py` | Grid size, DNQ, 107% rule floor |
| `PREQUALIFYING_*` | `constants.py` | Pre-qualifying for big entries: trigger, field limit, protected teams, 30 minutes, 4 hot laps |
| `pole_point` | `regulations.json` | +1 point for pole |

Everything else on the lists below is not possible today.

## 2. Every format we need

**DTM**

| Seasons | Format |
|---|---|
| 1984 to 1988 | Timed practice or qualifying sets the grid. Two sessions, best time counts. |
| 1989 | Timed qualifying, then a one-lap **Top-Qualifying** for the top 16 (top 20 at Zolder). |
| 1989 to 1992 | Qualifying sets places 1 to 16. All others run a 40 to 50 km **qualification race** for the rest of the grid. Non-qualifiers from it don't start. |
| 1988 to 1995 | Two heats. The heat 2 grid is the heat 1 result. |
| Mid 1990s | Timed qualifying, then a top 10 shootout (top 15 at some rounds). |
| 2001, 2002 | 45 minutes, **12 laps at most**. It sets the grid of a 30 to 35 km **qualifying race** on Sunday, whose result sets the main-race grid. 3-2-1 points for it. |
| 2003 to 2005 | 20 minutes, 9 laps at most, for places 11 on. Then a top 10 **Superpole**: one flying lap each, alone, in reverse order. |
| 2006 to 2008 | Three-part knockout, the slowest six drop out after each part. |
| 2009 to 2013 | Knockout Q1 to Q3, then **Q4**: the top 4 run one lap each, alone. Parc fermé before Q4. |
| 2014 | Q1 to Q3 knockout like F1, shootout dropped. |
| 2015 on | Two races per weekend, **one qualifying session per race** (Saturday and Sunday), 20 minutes each. |
| 2018 on | 3-2-1 points for the top three in each qualifying. |
| 2019 | At most 2 new tyre sets in qualifying. |

**Formula 1**

| Seasons | Format |
|---|---|
| 1950s to 1995 | Two timed sessions (Friday and Saturday), best time counts. Grid limit 26, others DNQ. |
| 1988 to 1992 | **Pre-qualifying** on Friday morning for the weakest teams. Only the top 4 go on to qualifying. |
| 1996 to 2002 | One hour, 12 laps per driver, **107% rule**. |
| 2003 | **One-lap qualifying**: Friday single lap sets the Saturday run order. Saturday single lap, alone, in reverse order, with race fuel and parc fermé. |
| 2004 | Two single-lap sessions back to back on Saturday. The first sets the order of the second. |
| Early 2005 | **Aggregate** of a Saturday lap and a Sunday-morning lap. Dropped after six races. Then one lap, run order from the previous race result. |
| 2006 to 2009 | Knockout Q1 to Q3. Q3 with **race fuel**; fuel used in Q3 is given back. |
| 2010 to 2021 | Knockout, no refuelling. The top 10 **start on the tyres of their best Q2 lap** (Q3 tyres until 2013). |
| 2016 (two races) | **Elimination qualifying**: the slowest car drops out every 90 seconds. |
| 2021, 2022 | **Sprint weekend**: Friday qualifying sets the sprint grid. The sprint result sets the Grand Prix grid. |
| 2023 | Sprint weekend with a separate short **Sprint Shootout** (SQ1 to SQ3) for the sprint grid. New mediums in SQ1 and SQ2, softs in SQ3. |
| 2023 (two rounds) | **Alternative tyre allocation**: hard in Q1, medium in Q2, soft in Q3. |
| 2024 on | Sprint qualifying on Friday, sprint and GP qualifying on Saturday. |
| Always | Grid penalties after qualifying (engine parts, gearbox, incidents), back of grid, pit-lane start. |

## 3. The building blocks

All of the above can be built from a few parts. A **weekend** is a list of
sessions. Each session takes a list of cars and returns an order. A
**grid** is built by joining the outputs.

**Stage types**

| Stage | Settings | Covers |
|---|---|---|
| `timed` | minutes, `max_laps`, `sessions` with `combine: best / aggregate / average` | F1 1950 to 2002, DTM 1984 to 1988, DTM 2015 on, 2005 aggregate |
| `knockout` | list of parts, each with minutes and `keep` (cars that go on) | F1 2006 on, DTM 2009 to 2014 |
| `single_lap` | `cars`, `laps_each`, `run_order` (`reverse`, `forward`, `previous_race`, `previous_session`), alone on track | DTM Superpole and Q4, F1 2003 to 2005, Supercars Top 10 Shootout |
| `elimination` | `drop_every_s` | F1 2016 |
| `qualification_race` | km or laps, `slots` | DTM 1989 to 1992, DTM 2001 and 2002 |
| `prequalifying` | as today, but per session and per team list | F1 1988 to 1992 |
| `duel` | bracket size, pairs by seed | Formula E (group, then duels) |

**Settings every stage can have**

- **Who runs:** `all`, `top N` or `bottom N` from the stage before, or a
  list of groups (split by odd and even times, by class, by group draw).
- **Who goes on:** `keep N`, or `promote N` from a lower group into a
  higher one (MotoGP Q1 into Q2).
- **Where the rest start:** the positions the eliminated cars take
  (usually the slots just below those still running).
- **Car state:** `fuel: low / race / race_with_credit`,
  `parc_ferme: true` (setup locked after this stage),
  `tyre: any / new_set / compound X`, `start_tyre: true` (the tyres of the
  best lap are the race start tyres, see B12).
- **Cut:** `max_pct_of_best` (107%) with a stewards' exception.

**Grid sources for each race**

| Source | Example |
|---|---|
| `qualifying` (or a named session) | Normal grid |
| `previous_race` | DTM heats, F1 sprint 2021 and 2022 |
| `reverse_top_n` | F2 and F3 sprint (top 10), WTCC race 2 |
| `reverse_drawn` (draw N from a range) | BTCC race 3 (top 6 to 12 drawn) |
| `championship_reverse` | Some one-make series |
| then `penalties` | Grid drops, back of grid, pit-lane start |

**Points tied to qualifying:** a points table per stage (`[3, 2, 1]`),
see B8.

## 4. Why this scales

- **One engine, many formats.** The game already runs a timed session and
  a knockout. A knockout is a list of timed parts with `keep`. A shootout
  is a timed part with one car on track at a time. So most of the work is
  turning the current two formats into a loop over a list.
- **Presets in `options.json`.** Each format is an option in
  `qualifying_format`, so the governing body can vote between them like
  today. Ship presets (`f1_2006_knockout`, `dtm_2013_q4`,
  `f1_sprint_2023`) so most packs pick one and never write a stage list.
- **AI and screens read the same list.** The timing screen shows the stage
  names from data. The AI only needs two decisions per stage: when to go
  out, and on which tyre.
- **Sim cost is small.** A single-lap run is one simulated lap per car.
  A qualification race reuses the race engine with a shorter distance.

## 5. Ideas ranked

| Rank | Lever | Effort | Unlocks |
|---|---|---|---|
| 1 | Knockout with any number of parts and any `keep` | Small | DTM 2006 to 2013 cut sizes, F1 any year, MotoGP-like |
| 2 | `single_lap` stage after any stage | Small to medium | DTM 1989, 1994, 2003 to 2013, Supercars, F1 2003 |
| 3 | Several races per weekend with grid sources (A1) | Medium | DTM heats, DTM 2015 on, F1 sprint, F2, BTCC, WTCC, Supercars |
| 4 | One qualifying per race | Small after 3 | DTM 2015 on, F1 sprint 2023 on |
| 5 | Qualification race | Medium | DTM 1989 to 1992 and 2001, NASCAR heats, Indy-style Last Chance |
| 6 | Car state per stage (fuel, parc fermé, start tyre) | Medium | F1 2003 to 2009, F1 2010 to 2021 |
| 7 | Groups, promotion, duels | Medium | MotoGP, Formula E, IndyCar road courses |

## 6. Other series this unlocks

- **F1** every era, incl. sprint weekends and 1980s pre-qualifying.
- **F2 / F3**: one session, reverse top 10 for the sprint.
- **IndyCar**: road courses (two groups, Fast 12, Fast Six); the Indy 500
  (four-lap average, Fast 12, bumping, Last Chance qualifying).
- **BTCC**: one session, race 2 from race 1, drawn reverse grid for race 3.
- **WTCC / TCR**: knockout plus reverse top 10.
- **Supercars**: Top 10 Shootout, two or three races per weekend.
- **Super GT**: two parts, each driver of the car must run one; times
  added together.
- **MotoGP**: Q1, top 2 promoted into Q2.
- **Formula E**: groups, then knockout duels.
- **NASCAR**: single-car runs plus heat races.
- **Le Mans / WEC**: qualifying per class, then a top 8 **Hyperpole**.

## Fits the existing options

- `qualifying_format` stays a regulation category. `session_60` and
  `knockout` become two presets of the stage list and behave as today.
  New presets are new options, so voting and `scripted_changes` work
  unchanged.
- The stage list lives in a named block (like `oval_stage_racing` in the
  oval `config.json` today), and the option points to it:
  `{"key": "dtm_2013", "qualifying": "dtm_2013_q4"}`.
- `PREQUALIFYING_*`, `QUALI_GRID_LIMIT` and `quali_107_rule` become stage
  settings, with the constants as defaults.
- The formula `config.json` already has `formula_red_flags` (stop, restart,
  up to 2 per race). The oval mode already has `oval_start_procedure`
  `double_file_pace_lap`. A3's rolling start and red-flag result rules can
  build on both.

## Overlaps with other packages

| Shared block | Also used by |
|---|---|
| Weekend as a list of sessions | [Points](points-and-championships.md) (a table per session), [Tyres](tyres-and-stops.md) (rules per race), [Calendar](calendar-and-world.md) (junior weekends, C7) |
| Qualifying points (B8) | [Points](points-and-championships.md) owns the tables |
| Start tyre, sets in qualifying | [Tyres](tyres-and-stops.md) owns the rule rows |
| Groups and classes | [Entries](entries-and-crews.md) owns entry tags |
| Rolling start, red flags | [Race control](race-control.md) |

## Endurance

- Qualifying per class, then a top N **Hyperpole** per class.
- Qualifying by one named driver, or the **average of two drivers**
  (GT racing, Super GT).
- Race length in hours, with a clock that runs through the night.
- Warm-up and night practice as sessions.

## Evidence log

| Item | Season | Need | Source | Status |
|---|---|---|---|---|
| A6 | DTM 1984 to 2026 | See the A6 table | [dtm_rules.html](../dtm_rules.html), `seasons/*/research/season.md` | Checked |
| A6 | F1 1950s to 2024 | See section 2 | Memory | To source |
| A6 | Other series | See section 6 | Memory | To source |

## Open questions

- DTM 1993 to 1995 shootouts: which rounds, how many cars?
- DTM 2000: how was the race 2 grid set?
