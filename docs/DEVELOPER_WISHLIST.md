# Wish List for the Team Principal Developer

These are feature requests from building historically accurate DTM season
packs: 1987 and 1990–1992 (Group A), 2003, 2006 and 2010 (V8 Masters),
2012, 2013 and 2018 (Class One V8) and 2020 (Class One turbo). Each item lists the real-world need,
what the game can't do today, our current workaround, and what would solve
it. **Needed by** names the season packs (`seasons/dtm-*`) that would use
it. Findings are based on game version 0.99.5, rechecked against the
0.99.6 beta's modding guide (no item closed). 0.99.6 was released on
2026-11-11, with Patch #1 on 2026-11-15. See
[CAPABILITIES.md](CAPABILITIES.md) for what we confirmed works, and
[game/changelog.csv](game/changelog.csv) for every patch and what it means
for our packs.

Priority: **P1** = needed for an authentic series, **P2** = big gain,
**P3** = nice to have.

Whenever a pack hits something the game can't do, it goes in here (a new
item, or the season added to an existing one), and in that pack's README
under "Simplifications".

The items are grouped into ten **feature packages** in
[packages/](packages/README.md). Each package collects evidence, shows
where items overlap, how they fit the existing options, and what the
coming endurance mode needs. The README there proposes one shared way to
build them all.

| Season | Items |
|---|---|
| dtm-1987 | B1, B2, B3, B9, C2, C3, C9, D1, D9, E1, E2 |
| dtm-1990 | A1, A6, B1, B2, D1, D9, E1, E2 |
| dtm-1991 | A1–A6, B1–B4, C1–C5, D1–D4, D9, E1–E7 |
| dtm-1992 | A1, A6, B2, B3, C1, C2, D1, D9, E1, E2 |
| dtm-2012 | A3, A5, A6, B5, B7, B12, C4, C6, C7, D1, D3, D5, D6, D7, D8, E1, E2, E4, E5, E6, E8, E9, E12, E13, E15, E18, E20, E21, E22 |
| dtm-2003 | A5, A6, B4, B5, B7, C2, C4, D1, D3, D7, E1, E2, E8 |
| dtm-2006 | A6, B1, B2, B5, B7, B10, C2, C4, D1, D3, D7, E1, E2, E8 |
| dtm-2010 | A3, A5, A6, B5, B7, C2, C4, D1, D3, D7, E1, E2, E8, E22 |
| dtm-2013 | A3, A5, A6, B5, B6, B7, B11, B12, C4, C6, C7, C10, C11, D1, D3, D4, D5, D6, D7, D8, E1, E2, E4, E5, E6, E8, E9, E10, E11, E12, E13, E14, E15, E17, E18, E19, E20, E21, E22, E23, E24 |
| dtm-2018 | A1, A4, A6, B5, B6, B8, B9, D1, D3, E1, E2, E18, E21, E22 |
| dtm-2020 | A1, A3, A4, B4, B5, B6, B8, B12, B13, C1, C4, D1, D3, E1, E2 |
| f1-2012 | D8, D10, D11, D12, E1, E2 |
| btcc-1991 | C10, C11, C12 |

Seasons without a pack yet (research only) are covered for qualifying and
race rules in [dtm_rules.html](dtm_rules.html), which maps every season's
rules to these items:

| Seasons | Items |
|---|---|
| dtm-1984 to dtm-1989 | A1, A2, A3, A5, A6, B1, B2, B3, B7, B9, D9 |
| dtm-1993 to itc-1996 | A1, A5, A6, B2, B4, D2, D9 |
| dtm-2000 to dtm-2011 | A1, A2, A3, A5, A6, B1, B2, B3, B5, B7, B8, B10, B11, B12 |
| dtm-2014 to dtm-2018 | A1, A3, A6, B1, B5, B6, B7, B8, B9, B10, B12 |
| dtm-2019 to dtm-2020 | A1, A3, A6, B4, B6, B7, B8, B12 |
| dtm-2021 to dtm-2026 | A3, A6, B1, B2, B3, B4, B5, B7, B8, B9, B10, B11, B12 |

---

## A. Race weekend format

### A1. Several races per weekend (heats) · P1
- **Needed by:** dtm-1990, dtm-1991, dtm-1992 (each runs one race per round at heat distance), dtm-2018 and dtm-2020 (two races a weekend; each race is its own game week, which stretches the calendar on back-to-back weekends), btcc-1991 (two races at Donington and Brands Hatch; each takes its own week, and each paid half points to the top eight, 12-9-6-5-4-3-2-1, against 24-18-12 in the single races).
- **1991:** every DTM round had **two heats of about 100 km**, both with full
  points. The heat-2 grid was the heat-1 finishing order.
- **Today:** one race per scheduled week.
- **Workaround:** one race at heat distance, which gives half the season's
  points and races.
- **Request:** a weekend definition in data, e.g.
  `"races": [{"distance_km": 100}, {"distance_km": 100, "grid": "previous_result"}]`,
  with points per race. Grid options: `qualifying`, `previous_result`,
  `reversed_top_n`.

### A2. Qualification race · P1
- **Needed by:** dtm-1991.
- **1991:** places 1–16 came from qualifying. All other cars ran a ~50 km
  **qualification race** for places 17+.
- **Today:** no way to model this. Our 39-car field either all starts or is
  cut by DNQ.
- **Request:** a session type `qualification_race`, with `direct_grid_slots`
  and `distance_km`.

### A3. Configurable sessions and race format · P2
- **Needed by:** dtm-1986 (red-flag aggregate), dtm-1991, dtm-2000 to dtm-2002 (rolling starts, lap caps in qualifying), dtm-2003 to dtm-2011 (one-hour races), dtm-2012 (the Norisring, wet at the start, and Zandvoort, with showers and two safety cars, were stopped at the 75-minute limit), dtm-2013 (the wet Nürburgring and final Hockenheim races were time-limited to 75 minutes), dtm-2015 on (minutes plus one lap), dtm-2021 on (rolling two-abreast start), dtm-2010, dtm-2020.
- **Today:** a race is `laps × lap_modifier` with a standing start.
  `formula_red_flags` in `config.json` stops and restarts a race (up to 2
  per race), but the result can't be an aggregate. The oval mode already
  has a rolling two-abreast start (`oval_start_procedure`
  `double_file_pace_lap`); formula packs can't use it.
- **Request:**
  - Race length as laps, km, **minutes plus one lap**, or whichever comes
    first (F1: 305 km or two hours). Optional **safety-car laps added**
    (DTM 2019, 2025: up to 2).
  - Start type: standing, rolling single file, **rolling two abreast**
    in a start corridor.
  - Red flag: stop, restart, and the result as the **aggregate** of both
    parts or shortened (Zolder 1986, Hockenheim 1991).
  - Lap caps per qualifying session (`max_laps`: 12 in 2001 and 2002, 9 in
    2003) and two sessions where the best time counts.
  - Heats: gap between the races (15 or 30 minutes), a **repair window**
    (22 minutes in 1995, 25 in 2001), and points per heat (half points
    for the two-heat rounds of 1984 and 1985).

### A4. More than one event per week · P3
- **Needed by:** dtm-1991, dtm-2018, dtm-2020 (a round's second race moves to the next week).
- **1991:** two rounds were on consecutive weekends (Nürburgring 8 Sep,
  Singen 15 Sep).
- **Today:** that works, but a double-header at one venue on one weekend
  can't be scheduled.
- **Request:** allow several events per week slot, or a real-date calendar
  (day of year).

### A5. Single-lap shootout (Q4) · P2
- **Needed by:** dtm-2013, dtm-2012 (the top 4 also had a single-lap shootout), dtm-2003, dtm-2010.
- **2013:** the four fastest from Q3 ran one timed lap each, alone on the
  track, for the first two rows.
- **Today:** the game's knockout stops at Q3.
- **Workaround:** the Q3 order is the grid.
- **Request:** a qualifying stage with `cars`, `laps_each: 1` and
  `run_order: "reverse"`.

### A6. Qualifying as a list of stages · P1
- **Needed by:** every DTM season (each era had a different format), dtm-2012, dtm-2013 (Q1 to Q3 plus Q4), dtm-2003, dtm-2006, dtm-2010, dtm-2018.
- **Today:** `qualifying_format` is `session_60` or a fixed Q1 to Q3
  knockout cut like F1 (10 cars in Q3, the rest split evenly over Q1 and
  Q2; 18, 15 and 12 minutes; none of it configurable). Pre-qualifying and the grid
  limit are global constants. Every race gets its grid from the one
  qualifying.
- **Request:** a qualifying format as a list of stages. Each race of the
  weekend names its grid source. Ship presets as `qualifying_format`
  options so packs pick one. This one model covers A2, A5, B8 and the
  grid part of A1.
  - **Stage types:** `timed`, `knockout` (any number of parts),
    `single_lap`, `elimination`, `qualification_race`, `prequalifying`,
    `duel`.
  - **Per stage:** minutes, `max_laps`, who runs (`all`, `top N`,
    `bottom N`, a group), how many go on (`keep N`), where the others
    start, `run_order` for single laps, car state (`fuel`, `parc_ferme`,
    `start_tyre`), tyre limits (`new_sets_max`, `compound`), a 107% cut,
    a points table. Any setting can differ per track.
  - **Grid sources per race:** `qualifying`, a named session,
    `previous_race` (with `retired_to_back`), `reverse_top_n`,
    `reverse_drawn`, then grid penalties.
- **Historic formats this has to cover:**

  | Seasons | Format | Built from |
  |---|---|---|
  | DTM 1984 to 1988 | Timed practice sets the grid; 1.8 s off pole meant DNQ at Mainz 1988 | `timed`, grid limit |
  | DTM 1989 | Timed, then a one-lap Top-Qualifying for the top 16 (top 20 at Zolder); the rest race for places 17 on | `timed`, `single_lap` (16), `qualification_race` |
  | DTM 1990 to 1992 | About 16 go straight through; the rest run a 40 to 50 km qualification race (none at the Eifel, AVUS and Nordschleife) | `timed`, `qualification_race`, per-track switch |
  | DTM 1991 | Two sessions set places 1 to 16 | `timed` with `sessions: 2, combine: best` |
  | DTM 1988 to 1996 | Heat 2 grid is the heat 1 order, retirements at the back | `previous_race`, `retired_to_back` |
  | DTM 1993 | Timed, then a top 10 shootout (top 15 at some rounds) | `timed`, `single_lap` with per-track `cars` |
  | DTM 2001, 2002 | 45 min, 12 laps max; a 30 to 35 km qualifying race on Sunday sets the main grid, 3-2-1 points | `timed` with `max_laps`, `qualification_race` with points |
  | DTM 2003 to 2005 | 20 min, 9 laps max, sets places 11 on; top 10 Superpole in reverse order | `timed`, `single_lap` (10, `reverse`) |
  | DTM 2006 to 2008 | Three-part knockout, the slowest six drop out each part | `knockout` with `keep` |
  | DTM 2009 to 2013 | Q1 14 to 16 min (top 14 to 16 go on), Q2 to 8 or 10, Q3 to 4, Q4 one timed lap each; parc fermé before Q4 | `knockout`, `single_lap` (4), `parc_ferme` |
  | DTM 2014 | Q1 to Q3 knockout like F1 | `knockout` |
  | DTM 2015 on | A 20 min session before each race; 3-2-1 points from 2018 | one `timed` per race, points table |
  | DTM 2019 | At most 2 new sets in qualifying | `new_sets_max: 2` |
  | F1 1950s to 1995 | Two sessions, best time counts, 26 starters | `timed` × 2, grid limit |
  | F1 1988 to 1992 | Pre-qualifying, top 4 go on | `prequalifying` with `keep: 4` |
  | F1 1996 to 2002 | One hour, 12 laps, 107% rule | `timed` with `max_laps`, cut |
  | F1 2003, 2004 | One lap each, order from a first single-lap run; race fuel, parc fermé | `single_lap` × 2, `fuel: race` |
  | F1 2005 | Aggregate of two single laps, then one lap in reverse order of the last race | `combine: aggregate`, `run_order: previous_race` |
  | F1 2006 to 2009 | Knockout; Q3 on race fuel, fuel used given back | `knockout`, `fuel: race_with_credit` |
  | F1 2010 to 2021 | Knockout; top 10 start on their best Q2 tyres (Q3 tyres to 2013) | `start_tyre` on a stage |
  | F1 2016 (two races) | Slowest car out every 90 s | `elimination` |
  | F1 2021 on | Sprint weekends: sprint grid from Friday qualifying or a Sprint Shootout; Grand Prix grid from the sprint (2021, 2022) or its own qualifying | two formats, two grid sources |
  | F1 2023 | Hard in Q1, medium in Q2, soft in Q3 (two rounds) | `compound` per stage |

- **Full brainstorm** (ranking, scalability, other series):
  [packages/weekend-format.md](packages/weekend-format.md).

## B. Rules and balance of performance

### B1. Success ballast · P1
- **Needed by:** dtm-1990 (up to 100 kg), dtm-1991, dtm-1987, dtm-2006.
- **1991:** weight penalties of up to **50 kg**, given for good results and
  removed for poor ones. Drivers new to the series started on the maximum.
- **Today:** not possible.
- **Request:** a regulation category with a per-position kg table, a
  maximum, a removal rule, and a value for newcomers.

### B2. Mid-season balance changes on a date · P1
- **Needed by:** dtm-1990 (Audi's 80 kg at Diepholz; the Mercedes 190E Evo II from the Nordschleife round), dtm-1991, dtm-1992 (BMW's bigger splitter and wing from the Nordschleife round), dtm-1987 (M3 +100 kg after round 2, Sierra -100 kg then +50 kg, Volvo and Alfa -50 kg, Mercedes -50 kg), dtm-2006.
- **1991:**
  - Audi had **40 kg removed from Wunstorf** onwards.
  - Opel could remove **50 kg after Hockenheim**.
  - Minimum weights depended on displacement and drivetrain (BMW and
    Mercedes 980 kg, Opel 1130 kg, Audi 1290 kg).
- **Today:** since 0.99.6 the guide documents `scripted_changes` rows
  (`key`, `effective_season`, `new_regulation`), but only per season, not per
  week or per make. The minimum weight is one global value.
- **Request:**
  - Scripted rule changes tied to season and week, e.g.
    `{"season": 1, "week": 23, "engine": "Audi", "mass_kg": -40}`.
  - Minimum weight per engine or car model.

### B3. Points table per race, drop scores · P2
- **Needed by:** dtm-1991, dtm-1992 (drop scores), dtm-1987 (points to 18th place, one drop result), btcc-1991 (the real totals don't fit a plain 20-15-12 scale; drop scores and fastest-lap points are likely but unconfirmed).
- **Request:** points tables per session (heat 1 and heat 2 can differ),
  qualification-race points, and drop scores (Streichresultate, used in
  1992).

### B4. More classifications · P2
- **Needed by:** dtm-1991, dtm-2003, dtm-2020.
- **1991:** besides the drivers' title there were a **teams'** and a
  **manufacturers'** title (only the best car of each make scored), the
  **ITR Fahrerpokal** (DTM plus the non-championship Brno and Donington
  rounds) and a **privateer cup** paid in prize money.
- **Request:** a list of championships in data, each with its own events,
  points rules and eligible entries (e.g. `"privateer": true`).

### B5. Mandatory pit stops and pit windows · P1
- **Needed by:** dtm-2001 to dtm-2026 (every season sets a stop count; most add a window), dtm-2012 (two stops, each inside a window), dtm-2013 (two stops, none in the first or last 3 laps), dtm-2003, dtm-2006, dtm-2010, dtm-2018, dtm-2020.
- **2013:** **two mandatory stops**, no pit window, but none in the first or
  last 3 laps. Damage stops don't count.
- **Today:** no regulation can require a number of stops or close the
  pits for part of the race.
- **Workaround:** tyre wear per track (`tyre_wear_mult`) is tuned so two
  stops is the fastest strategy. In season 5, 160 of 220 cars stopped twice;
  the rest stopped between zero and seven times. The balance is fine:
  Norisring went from mostly three or four stops at 0.65 to mostly one at
  0.50. Rain races always add tyre stops.
- **Why short tracks stay messy (DTM 2013, 2026-11-15, game 45440200):**
  tyre wear is per lap, so tracks with short laps and many laps need a low
  `tyre_wear_mult` (Brands Hatch Indy 0.42, Norisring 0.57, Moscow 0.68).
  In `managers/strategy.py`, `_default_stop_cap` gives every track with
  `track_wear_mult` at 1.2 or below a plan cap of 2 stops, and
  `_restrict_decision_defaults` then uses the restricted decision path.
  In the last two simulator rounds every 2013 track above 1.2 had 99 to
  100% two-stoppers in clean races, while the three tracks below it had
  10 to 22% one-stoppers and 20 to 49% three-stoppers. Over all rounds at
  today's values one-stoppers won 20 of 56 races there, and 10 of 16 after
  a safety car, because a stop under the safety car is cheap. In-game the same: Paffett won Brands Hatch from 6th
  on one stop after a safety car, and Ekström won Moscow from 12th on one
  stop. Raising the wear swaps one-stoppers for three-stoppers (Moscow 0.75:
  5% one stop, 50% three or more, one-stoppers still won 2 of 4).
- **Request:**
  - `mandatory_stops: N`, set **per race** of the weekend (2015: Saturday
    0, Sunday 1; 2025: Saturday 1, Sunday 2).
  - **Pit window closed for the first N and the last N laps:** a stop in
    those laps doesn't count (`no_stop_first_laps: 3`,
    `no_stop_last_laps: 3` in 2013).
  - A window per stop, in laps, minutes or share of the race: the middle
    third (2008, 2014), the 2nd and 3rd quarters (late 2008), minute 10 to
    40 (2022), 20 to 40 (2023, 2024), and in 2025 on Sunday stop 1 in
    minutes 10 to 20 and stop 2 in 39 to 45.
  - What a counting stop needs: four tyres changed (2001 on), not a damage
    stop (2013), not under safety car (2014, 2021, 2024) or FCY (2022);
    or stops under safety car allowed (2022).
  - `windows_off_if_wet` (2014).
  - A penalty when the rule is broken. The AI plans its stops inside the
    rules. B12 has the shared rule list.

### B6. DRS rules per session · P2
- **Needed by:** dtm-2013, dtm-2018, dtm-2020.
- **2013:** DRS in the **race only**, free use once per lap anywhere on the
  track, and not in the last 3 laps.
- **Today:** `drs_policy` is on or off for the whole weekend, so qualifying
  gets DRS too (8 km/h). It works in zones only, from lap 3, with no ban on
  the last laps.
- **Workaround:** one zone on each track's longest straight. Qualifying top
  speeds come out high (season 5: 285 km/h at Hockenheim).
- **Request:** DRS settings per session (`qualifying: false`), a per-lap
  activation budget instead of zones, and `disable_last_laps`.

### B7. Tyre allocation rules · P2
- **Needed by:** dtm-2013, dtm-2012 (one dry tyre for the whole season; the pack keeps the soft as a copy of the hard, since the game's need for a soft can't be checked), dtm-2003, dtm-2006, dtm-2010.
- **2013:** the Hankook hard was the standard tyre, plus **one set of the
  option (soft) per race**, which every driver had to use.
- **2013 look:** the tyres were called **standard** (white sidewall) and
  **option** (yellow sidewall). There was no medium.
- **Today:** `formula_compound_usage` asks for two different dry compounds,
  and `weekend_tyre_allocation` sets any number of dry, inter and wet sets
  per weekend (in the option payload). The weekend allocation screen always lists soft,
  medium and hard, even when `tyremodel.json` sets the medium to null:
  `DRY_COMPOUNDS` is fixed in `managers/weekend_tyre_allocation.py` and in
  the screen. The presets also hand out medium sets. Compound labels are
  the `tyremodel.json` keys in title case; colours follow the first letter
  (S red, M yellow, H white).
- **Workaround:** the two-compound rule. The player sets the medium to 0 by
  hand each weekend.
- **Request:** a set limit per compound and race, and "must use compound X"
  as a rule. Take the dry compounds for the allocation screen and presets
  from `tyremodel.json` (see D8 for names and colours).
- **Other seasons:** 3 to 9 sets per weekend (2000 to 2006, 2015, 2019,
  2022 on; per weekend this works today, per race or race day it doesn't), a cap of half the race
  distance on the option (2014), the top 5 or top 10 must start on their
  qualifying tyres (2023 on), tyre warmer bans (2003, 2017).

### B8. Qualifying points · P2
- **Needed by:** dtm-2001, dtm-2002 (3-2-1 for the qualifying race), dtm-2017 to dtm-2026 (3-2-1 for the top three in qualifying), dtm-2022 (fastest-lap point only for a top-10 finisher), dtm-2018, dtm-2020.
- **Today:** `pole_point` gives +1 to pole only, and `fastest_lap_point`
  gives +1 to the fastest-lap holder wherever they finish.
- **Workaround:** pole point on, which gives 1 point instead of 3 and
  nothing to second and third.
- **Request:** a qualifying points table (`[3, 2, 1]`), and an optional
  `min_finish_position` for the fastest-lap point.

### B9. Non-scoring guest entries · P2
- **Needed by:** dtm-1984 (only German drivers scored), dtm-1987 (guest Ludwig won round 7 and scored nothing), dtm-2018, dtm-2021 to dtm-2026 (guest and wildcard drivers).
- **Today:** every entry scores.
- **Request:** a `guest: true` flag on a driver or entry. Guests race and
  are classified, but the points go to the next eligible drivers.

### B10. Pit-stop procedure rules · P3
- **Needed by:** dtm-2001 (25-minute service window between the races), dtm-2017 (8 mechanics, one wheelgun per side), dtm-2021 (a stop under safety car doesn't count), dtm-2022 to dtm-2026 (rear wheels first, 4 to 6 crew), dtm-2006.
- **Today:** one stop-time model for every pack; no setting for crew size
  or what counts as the mandatory stop.
- **Request:** `pitstops.crew_size` or a base stop time per pack, and rules
  for which stops count (`not_under_sc`, `not_under_fcy`).

### B11. Race control rules · P3
- **Needed by:** dtm-2007 (pit lane closed under the safety car), dtm-2022 to dtm-2026 (full-course yellow at 60 km/h), dtm-2023 to dtm-2026 (penalty lap), dtm-2013 (the wet Nürburgring race started behind the safety car; a race stopped early added the track's in-and-out time, 29 s at Moscow, to every driver short of his mandatory stops).
- **Today:** `safety_car_policy` picks the safety car and the virtual
  safety car. The VSC stands in for the FCY.
- **Request:** `pit_lane_closed_under_sc`, and a penalty-lap penalty type
  next to time penalties. A safety-car start when the race starts wet. A
  time penalty per missing mandatory stop when a race ends early, set per
  track (it can default to the track's `pit_lane_loss_s` plus a stop).

### B12. Tyre and stop rules as data · P1
- **Needed by:** dtm-1988 on (set limits), dtm-2001 on (stop rules), dtm-2012, dtm-2013 (two stops, option tyre once), dtm-2014 (option cap), dtm-2023 on (start on qualifying tyres), dtm-2020.
- **Today:** one tyre rule (`mandatory_compound_count`, on or off for the
  whole season) and allocation options with any number of sets per weekend. No
  stop, window, must-use or start-tyre rule.
- **Request:** a list of rule rows checked after the race and read by the
  AI strategy planner. Each row has a scope (race, weekend, season), who it
  applies to (`all`, `top N` from qualifying, a class) and a penalty (time,
  drive-through, disqualification, grid drop). Rows can differ per race of
  the weekend. This one model covers B5, B7 and the counting part of B10.
- **Historic rules this has to cover:**

  | Rule | Historic use |
  |---|---|
  | `min_dry_compounds: N` | F1 2007 on (exists today) |
  | `mandatory_stops: N` per race | DTM 2001, 2002 (1); 2003 to 2013 (2); 2014 to 2024 (1); 2015 and 2016 Saturday (0); 2025, 2026 Sunday (2); F1 Monaco 2025 (2) |
  | `no_stop_first_laps`, `no_stop_last_laps` | DTM 2013 (3 and 3) |
  | `stop_window` per stop (laps, minutes, share) | DTM 2008, 2012, 2014, 2022 to 2026 |
  | `stop_counts_if` (four tyres, not damage, not under SC or FCY) | DTM 2001, 2013, 2014, 2021, 2022, 2024 |
  | `windows_off_if_wet` | DTM 2014 |
  | `no_tyre_change` | DTM 2016 Saturday; F1 2005 (one set for qualifying and race) |
  | `must_use: X` (once or min laps) | DTM 2013 option set; IndyCar (2 laps each); BTCC (option in 1 of 3 races, weekend scope) |
  | `max_share_on: X` | DTM 2014 (option for half the race at most) |
  | `max_stint_laps` | F1 Qatar 2023 (18 laps) |
  | `min_sets_used` | F1 Monaco 2025 (3 sets) |
  | `sets_per_weekend`, per compound | DTM 1988 (10 tyres), 2000 (5 sets), 2005 (9), 2006 (7), 2015 (4 for two races), 2019 (7); DTM 2013 (1 option set per race); F1 (13) |
  | `sets_per_race_day`, new sets per track | DTM 2022 (3), 2023 to 2026 (3 or 4 by track), plus a test pool in 2026 |
  | `new_sets_max` in qualifying | DTM 2019 (2) |
  | `discarded_set_lost` | DTM 2026 |
  | `start_on_qualifying_tyre: top N` | F1 2010 to 2021 (10), DTM 2023 (5), DTM 2024 on (10) |
  | `session_compound` | F1 2023 alternative allocation, F1 Sprint Shootout 2023 |
  | `tyre_warmers: banned` | DTM 2003, 2017 |
  | `rules_lapse_if_wet` | F1 compound rule, DTM 2014 window |
  | `wet_start_tyre` | F1: full wets when the race starts behind the safety car |

- **Full brainstorm:** [packages/tyres-and-stops.md](packages/tyres-and-stops.md).

### B13. Push-to-pass boost · P2
- **Needed by:** dtm-2020 (and dtm-2019).
- **2019 and 2020:** push-to-pass gave a fixed extra power for a few
  seconds, a set number of times per race (30 hp in 2019, 60 hp in 2020,
  with more fuel flow while it is used). There was no harvesting.
- **Today:** the game has ERS (`ers_policy`), which harvests and deploys
  energy. It has no fixed boost with a use count.
- **Workaround:** `ers_policy: spec`, so every car has the same system.
- **Request:** a boost option as data: extra power, duration, uses per race,
  and whether it is allowed in qualifying or the last laps.

## C. Entries, teams and drivers

### C1. More than 3 cars per team · P1
- **Needed by:** dtm-1991, dtm-1992 (AMG ran 4 cars; Lohr is a reserve), dtm-2020.
- **1991:** AMG ran **4 cars**, and some teams went up to 5.
- **Today:** `formula_team_entry_cap` stops at `three`, and a team's
  `entry_count` above 3 is cut to 3 (`team_entry_count`, 0.99.6 code).
- **Workaround:** Kreutzpointner (AMG #87) is a reserve driver.
- **Request:** allow 4–6 entries.

### C2. Entry lists per round (part-timers and guests) · P1
- **Needed by:** dtm-1991, dtm-1992 (Audi withdrew after round 6; in the game it races all season), dtm-1987, dtm-2003, dtm-2006, dtm-2010, btcc-1991 (Prodrive's car 44 was shared: Steve Soper drove 7 rounds around his DTM programme, Tim Sugden 5; in the game Soper races all 15, so the Mobil BMW team scores about 6 points too much in simulated seasons).
- **1991:**
  - Michael Schumacher drove 2 rounds for Zakspeed.
  - Walter Röhrl drove 1 round for SMS.
  - Bernd Schneider joined Zakspeed from round 8.
  - Jochen Mass did 3 rounds for MS-Jet.
- **Today:** contracts run the whole season.
- **Request:** a per-round entry list, or a contract with `rounds: [6, 7]`,
  so AI teams follow history in season 1.

### C3. Car numbers per entry and fixed numbers · P2
- **Needed by:** dtm-1991, dtm-1987.
- **1991:** numbers went to the entry, like Ludwig #8 and Stuck #1, not
  per-team pairs.
- **Today:** numbers work, but reserves and guests can't keep their real
  numbers.
- **Request:** a `number` on the contract, including for reserves.

### C4. Customer cars and homologation · P2
- **Needed by:** dtm-1991, dtm-2013 (chassis and aero were homologated and largely frozen; in the game teams develop at different rates, and in season 5 the gap between the fastest and slowest car grew from 3.6 to 4.3 rating points), dtm-2012, dtm-2003, dtm-2006, dtm-2010 (year-old cars beside new ones; modelled with lower ratings and potential), dtm-2020.
- **1991:** privateers bought homologated cars (Evo models) from BMW,
  Mercedes and Opel. Chassis development was mostly the manufacturer's job,
  not the team's.
- **Today:** every team designs its own chassis.
- **Request:** a "customer car" contract type, like engines, where chassis
  and aero performance come from the supplier's homologated model. Also
  homologation steps (Evo kits) as data.
- **Coming:** the 0.99.6 Patch #1 notes (2026-11-15) tease buyable and
  sellable chassis and buildable gearboxes and other parts for 0.99.7.
  Recheck this item and D1 when it lands.

### C5. Retirement and age tuning in data · P3
- **Needed by:** dtm-1991.
- **1991:** drivers raced competitively into their 40s and 50s (Quester was
  51, Laffite 47).
- **Today:** we changed `DRIVER_RETIREMENT_*` in `constants.py`.
- **Request:** expose these in JSON (see E2).

### C6. Driver timing codes · P3
- **Needed by:** dtm-2013, dtm-2012 (codes in `seasons/dtm-2012/research/spotter_guide.csv`).
- **2013:** every driver had a three-letter code on the timing screens and
  on the car (SPE, WER, PAF; Scheider was TSC, not SCH).
- **Today:** `drivers.json` has no field for it.
- **Workaround:** none. The codes are kept in
  `seasons/dtm-2013/research/spotter_guide.csv`.
- **Request:** an optional `code` per driver, shown in timing towers and
  results.

### C7. Feeder series with real race weekends · P2
- **Needed by:** dtm-2013 (five real feeder series in `junior_series.json`), dtm-2012 (the same five slots: F3 Euro Series and Formel Masters with 3 races a weekend, the others 2 or 3).
- **2013:** FIA F3 Europe and ADAC Formel Masters ran 3 races per weekend,
  German F3, the Carrera Cup and the DTC 2. The DTC scored two classes
  separately. German F3 gave points for pole and
  fastest lap, and its second race used a different points table.
- **Today:**
  - A junior series races at most once a week, so a weekend is one race.
  - Points go by finishing position only, with one table for all races.
  - The result is driver skill + 2 × team quality + luck. The track is
    only a label, and a venue without a track file has no country flag.
  - Feeder teams have colours but no logo, and the named drivers are only
    seated in the first season.
  - Any free driver inside a series' age band can take an open seat. A
    pack cannot keep a driver out, so ex-F1 drivers waiting for a DTM
    seat would race in F3 or the Carrera Cup.
- **Workaround:** one race per weekend, with the main race's points table.
  Venues of the DTM calendar use the DTM track ids. Every feeder stops at
  age 28, below the ex-F1 free agents (29 and up). The older gentleman
  drivers of the Carrera Cup, the DTC and the German F3 Trophy class are
  left out, among them the DTC champion Jens-Guido Weimann. The young
  Red Bull juniors still fit the F3 bands.
- **Request:** `races_per_event` and a points table per race (with
  pole/fastest-lap bonus) for junior series, a `nationality` per schedule
  entry, an optional team logo, and a per-driver flag (for example
  `"junior_eligible": false`) that keeps a free driver out of feeder seats.

### C8. Driver crews per car (endurance) · P3
- **Needed by:** no current pack. Fits the developers' planned endurance
  update.
- **Today:** one driver per car. Session tabs and timing are per driver.
- **Request:**
  - Entries as the unit: an entry has a car, a number, a car image (E4)
    and one to three drivers. Session tabs show entries; the driver card
    shows the crew.
  - Drive-time rules as pack data: minimum per driver, maximum stint,
    maximum total.
  - Fatigue that rises with stint length, heat and night driving.
  - A stint planner with an AI plan the player can accept or edit. AI
    teams use the same rules: swap at a stop that is already needed, give
    the faster driver the start and the finish, give the better wet driver
    the rain stint.

### C9. Several car models per make · P2
- **Needed by:** dtm-1987 (and the other Group A years).
- **1987:** BMW raced the M3 and the 635 CSi side by side, and Ford the
  Sierra XR4Ti and later the RS500. König, Reuter, Winkelhock and Hahne
  changed car model during the season.
- **Today:** one engine per make, and a team races one car all year.
- **Workaround:** a second engine supplier key (`BMW 635`) with its own
  engine, weight and profile. The changes during the season aren't modelled.
- **Request:** a car model per entry, with its own engine, weight and
  profile, that can change from a given round.

### C10. A grid with fewer than 10 teams · P2
- **Needed by:** dtm-2013 to dtm-2016 careers that run into 2017 and later,
  btcc-1991 (in 2000 the grid fell to 8 works teams), and any pack of a
  series with a small grid.
- **Real:** the DTM cut its grid to 18 cars in 2017: 3 makes with 3 teams
  of 2 cars, so 9 teams. In 2020 it had 8 teams (Audi 4, BMW 4).
- **Today:** `team_leave` is skipped when fewer than 10 teams would be
  left (hard-coded in `managers/team_leave_events.py`). Nothing tells the
  modder or the player.
- **Workaround:** `tools/real_history.py` checks the same rule at build
  time and drops a leave the game would skip. In a 2013 career, Audi Sport
  Team Abt stays from 2017 and one R-Motorsport team stays in 2020.
- **Request:** a minimum team count in `config.json` (default 10), or a
  minimum car count. A scripted leave with `guaranteed` could also always
  go ahead.

### C11. Title sponsor already in the team name · P3
- **Needed by:** every DTM pack with Mercedes teams (2000 to 2018),
  Orlen Team ART in 2020, and btcc-1991 (Kaliber ICS Team Toyota, Team
  Securicor + Listerine).
- **Real:** the Mercedes teams raced under their sponsor's name, such as
  STIHL AMG-Mercedes or Euronics AMG-Mercedes. Audi and BMW sponsors were
  only on the car name.
- **Today:** a sponsor with `"type": "title"` is put in front of the team
  name. Our names already hold the sponsor, so it would read "STIHL STIHL
  AMG-Mercedes". Two teams of the same owner can't both use the base name.
- **Workaround:** no title sponsors (`no_title_sponsors` in the era base).
  The sponsor stays in the team name, even when the deal ends.
- **Request:** an optional `title_base_name` per team, used with the title
  sponsor ("AMG-Mercedes"), while `name` stays the unique key. When the
  deal ends, the team shows the base name.

### C12. A team that changes make · P2
- **Needed by:** btcc-1991 careers from 1993 on.
- **Real:** BTCC teams often kept their crew and changed make. Andy Rouse
  went from Toyota (1991 to 1992) to Ford (1993 to 1995) and Nissan (1996).
  Ray Mallock went from Vauxhall to Nissan in 1997, Prodrive from BMW to
  Alfa Romeo, Honda and Ford. Schnitzer ran BMW in 1993 and 1994, left in
  1995 and came back in 1996.
- **Today:** a team keeps its engine supplier for good. Events can only add
  a team (`team_join`) or remove it (`team_leave`). A team that left can't
  come back.
- **Workaround:** `tools/real_history.py` writes a leave and a new team with
  its own name for each change (`docs/teams/btcc_game_events.csv`). The
  team history, staff and results don't carry over. Team Dynamics stays on
  BMW and two Toyota privateers keep Toyota in the series after the works
  teams left.
- **Request:** an event that moves a team to another engine supplier in a
  given season (`team_engine_change` with `team`, `supplier`,
  `exact_season`), and a `team_join` that can bring back a team that left.

## D. Cars and simulation

### D1. Touring-car part set · P1
- **Needed by:** dtm-1990, dtm-1991, dtm-1992, dtm-2013, dtm-2012, dtm-1987, dtm-2003, dtm-2006, dtm-2010, dtm-2018, dtm-2020.
- **Today:** the parts are open-wheel ones (front and rear wing, underfloor,
  diffuser, sidepods), plus ERS and DRS.
- **Request:** data-defined part categories with labels and effects, so a
  pack can use e.g. splitter, rear spoiler, suspension, brakes, gearbox and
  tyres. Also a way to remove categories completely.
- **2013 workaround:** the six slots are relabelled through
  `car_parts.json` (front splitter, rear wing, underbody, diffuser, side
  bodywork, monocoque), with low wear per lap. The Aerodynamics screen in
  the Development Centre uses the pack's `abbr` in the part codes
  (FS-13-A-1, UB-13-A-1). Other screens not yet checked.
- **Part drawings:** the Aerodynamics screen draws open-wheel sketches (an
  F1 front wing, a rear wing on a pylon). They load from the install
  folder (`ui/assets/aero/frontwing.png`, `rearwing.png`, `floor.png`,
  `diffuser.png`, `sidepod.png`), not from the pack. Swapping them there
  changes every pack and a game update puts them back. The Car Setup
  screen has the same problem: its controls say "Front Wing" and "Change
  Wing", and a touring car has a front splitter and dive planes instead. The stat names on
  the cards (Low Speed, Dirty Air...) are fixed in code too.
- **Request (art):** a pack folder for part drawings (for example
  `assets/parts/<part_key>.png`), used before the game's own, and a
  drawing per part category once categories are data-defined. The `front_wing` key still drives
  the lap-one damage outcome and the "wing damage" radio bank.

### D2. Drivetrain · P2
- **Needed by:** dtm-1991.
- **1991:** the 4WD Audi V8 had a big advantage in the wet. In Hockenheim's
  wet heat 2 the Audis finished about a minute clear.
- **Request:** a `drivetrain` value (`rwd` / `fwd` / `awd`) that affects
  traction, wet performance and tyre wear.

### D3. Documented lap-time controls · P1
- **Needed by:** dtm-1991, dtm-2013 (we fitted lap times by running the game's physics model offline), dtm-2012, dtm-2003, dtm-2006, dtm-2010, dtm-2018, dtm-2020.
- **What we found:**
  - `lap_modifier` sets the **number of laps**: race laps = `options.laps`
    × `lap_modifier`.
  - Lap time follows the micro-sector speeds and `car_profile`.
  - `track_time_mult` exists on some base tracks but is undocumented.
- **Request:**
  - Document every track and car field.
  - Add an explicit per-track lap-time multiplier.
  - Add a calibration helper that shows the expected pole time for a
    track and car profile.

### D4. Weather realism · P3
- **Needed by:** dtm-1991, dtm-2013 (a track has one
  `wet_weather_probability_multiplier` for every visit, so the May and
  October Hockenheim rounds can't have different rain chances; the pack now
  sets it from the climate in the race month, docs/venues).
- **Request:** weather probability per date and region (e.g. April in the
  Eifel), or at least per schedule round, red-flag or restart for heavy rain, and tyre changes to wets as
  real strategy.

### D5. Wider car-profile range · P2
- **Needed by:** dtm-2013, dtm-2012.
- **What we found:** `car_profile` multipliers must stay within 0.5–1.5 (the
  game raises an error otherwise). A 2013 DTM car (about 480 hp, 1,110 kg,
  a lot of drag) needs more drag and less acceleration than that allows.
- **Workaround:** drag 1.5 and acceleration 0.5, the limits. Top speeds still
  come out about 10 km/h high.
- **Request:** a wider range, or a profile given as power (hp), drag area and
  downforce instead of multipliers.

### D6. Damage repair at pit stops · P2
- **Needed by:** dtm-2013 (and the Group A packs), dtm-2012.
- **Real world:** a DTM front end is the splitter, bumper and bodywork, not
  a nose cone that clips off. After contact the crew pulls off loose
  pieces or tapes them up, and the driver carries the damage to the end.
  Swapping the front end costs far more than a tyre stop, so it rarely
  happens in a race.
- **Today:** contact sets part damage (`incidents.*_part_damage_fraction`,
  the lap-one `front_wing` outcome), and the pit-stop settings
  (`pitstops`) cover only tyre wear, pit-lane loss and stop failures.
  Seen in a 2013 race event log: "FRONT WING DAMAGE: <driver> has severe
  front wing damage", then at the next stop "FRONT WING: <driver> changed
  front wing". So the game swaps the part F1-style, and no setting turns
  that off or makes it slower.
- **Workaround:** lap-one pile-ups no longer break the front wing
  (`front_wing` 0.3 → 0, its share moved to `time_loss`), contact damages
  parts half as much as vanilla, and the radio lines say the driver carries
  on. Contact later in the race can still break it, and then it's swapped.
- **Request:** a per-pack `damage_repair` setting under `pitstops`: `none`
  (drive on with the damage), `repair` (fixed extra time, e.g. 20–40 s,
  restores part of the damage) or `swap` (today's behaviour), ideally per
  part.

### D7. Development freeze and homologation · P2
- **Needed by:** dtm-2013, dtm-2012, dtm-2003, dtm-2006, dtm-2010.
- **Real world:** 2013 DTM cars were homologated before the season, and
  aero development was largely frozen during it. Teams built spares to
  replace crash damage, not new designs.
- **Today:** teams design and build new part versions all season, as in
  F1. `build_cost_m` and `staff_hours` in `car_parts.json` are
  manufacturing values, so raising them only makes spares scarce; it
  doesn't stop development.
- **Workaround:** none.
- **Request:** a regulation for each part category: `frozen` (spares of
  the homologated design only), `tokens: N` (a set number of updates per
  season), or `open`; or a homologation date after which new designs are
  blocked until the next season. C4 (customer cars) covers who owns the
  homologated design; this item covers when it may change.

### D8. Custom tyre compounds · P2
- **Needed by:** dtm-2013, dtm-2012.
- **Real world:** 2013 had two Hankook dry tyres, the **standard** tyre
  (white or silver sidewall) and the **option** (yellow sidewall). 2012 had
  one dry tyre only.
- **Today:** the compound keys are fixed to soft, medium, hard,
  intermediate and wet. A pack can tune their grip, wear and temperature
  in `tyremodel.json` and set the medium to null, but the allocation
  screen, the presets, the strategy tools and the race screens still use
  the fixed list. Labels are the `tyremodel.json` keys in title case,
  but colours follow the first letter (S red, M yellow, H white).
- **Workaround:** soft stands in for the option and hard for the standard
  tyre. The option shows as a red "SOFT".
- **Request:** compounds defined in `tyremodel.json`, each with
  - an id, a `label` and a short letter (for 2013: "Option", "O"),
  - a `color` used on every screen (allocation, timing, strategy,
    telemetry),
  - its grip, wear, cliff and temperature values, as today,
  - whether it is dry or wet,
  - how many there are: one, two or more dry compounds, with the screens
    showing only the ones the pack defines.

### D9. Tyre suppliers beyond ratings · P2
- **Needed by:** dtm-1984 to dtm-1995 (open tyre war), dtm-1990, dtm-1991, dtm-1992, dtm-1987.
- **Today:** a tyre war works: each team has a supplier with its own grip,
  durability and temperature ratings per compound, which develop each
  season. All suppliers share the same compound list and the same
  physics curves.
- **Request:** per-supplier overrides of any compound field (warm-up,
  cliff, temperature window), grip by track temperature and in the wet,
  a compound range per supplier with per-event nomination, a works-partner
  performance gap, supply caps and control-tyre tenders, and the supplier
  logo and sidewall colour on screens. Details in
  [packages/tyres-and-stops.md](packages/tyres-and-stops.md), section 4.

### D10. Tyre temperature window strength as data · P2
- **Needed by:** f1-2012, f1-2011, f1-2013.
- **Real world:** the 2011 to 2013 Pirellis worked in a narrow
  temperature window. A car that could not switch them on (cold track,
  low downforce) or that overheated them (hot track, rear-limited car)
  lost a second a lap. This is why 2012 had seven winners in seven races.
- **Today:** a tyre outside its `temp_window_c` loses grip at fixed rates
  in the code: 0.005% per degree too cold and 0.025% per degree too hot
  (`TyreModel.grip_multipliers`, floor 0.8). Ten degrees too cold costs
  0.05% grip, so the window barely matters. The target temperature is the
  ambient plus a fixed 70 °C plus the pressure setup, the same for every
  car.
- **Workaround:** the narrow, low windows in `bases/f1-v8/data/tyremodel.json`
  only bite on hot days. The race-to-race shuffle comes from car profiles
  that suit different tracks and a raised weekend variability (D11).
- **Request:** per compound `cold_grip_loss_per_c` and
  `hot_grip_loss_per_c` in `tyremodel.json`, and a car or team term in the
  target temperature (rear downforce, a `tyre_heating` rating), so one car
  can run in the window while another can't.

### D11. Weekend variability per car, not only per driver · P2
- **Needed by:** f1-2012, f1-2013.
- **Today:** `WEEKEND_CORNERING_VARIABILITY_*` rolls one random cornering
  offset per driver per weekend (uniform, plus or minus level × km/h per
  level). Team-mates get separate rolls, so it reads as driver form, not
  as a car that found or lost the window that weekend.
- **Workaround:** the F1 2010 to 2013 packs raise the minimum level and the
  step, so every weekend has a real shuffle.
- **Request:** a second, per-team roll (`WEEKEND_CAR_VARIABILITY_*`), and a
  way to scale both by round or by season phase, so a pack can open a
  season up and let it settle later.

### D12. Scripted in-season development · P3
- **Needed by:** f1-2012, f1-2013 (Red Bull from mid-season), f1-2010.
- **Real world:** some upgrades changed a season: Red Bull's exhaust and
  floor upgrades from Valencia 2012, its Singapore 2013 package, the
  tyre change after Silverstone 2013 that suited it.
- **Today:** in-season development comes only from the AI's spending,
  staff and facilities, and the current-package catch-up rules
  (`CHASSIS_DEV_CURRENT_PACKAGE_CATCHUP_*`) slow a team that is ahead.
- **Workaround:** Red Bull gets the most development headroom
  (`chassis_starting_potential`), the best staff and facilities, so it
  should pull away by itself; checked with `tools/simulate.py`.
- **Request:** scripted events in data: from week N, a team's rating
  changes by x, or a supplier's compound changes (2013's tyre swap).

## E. Modding and data format

### E1. Overlay (partial) packs · P1
- **Needed by:** all packs.
- **Today:** a pack must be a full copy (~30 files plus audio and art). We
  build ours by copying the base pack, so updates to the base game don't
  reach our pack automatically.
- **Request:** `"base_pack": "default26"` in `workshop.json`, so a mod only
  ships the files it changes and the game merges them at load time.

### E2. Settings as data, not Python · P1
- **Needed by:** all packs.
- **Today:** since 0.99.6 a Workshop pack's `constants.py` is read as data
  (`workshop_manager.load_safe_constants`: literal assignments of
  whitelisted names, no calls or imports beyond `UITheme`). A local pack in
  `data/<pack>/` is still **executed Python**, and the file is still Python
  syntax, so tools can't edit it as data.
- **Request:** move pack settings (start year, points, grid size, salaries,
  retirement ages) to `constants.json`, and read local packs the safe way
  too.

### E3. Published schema and validation · P2
- **Needed by:** dtm-1991.
- **Request:**
  - A JSON schema for every pack file.
  - A validation mode that lists errors at load time (unknown team in a
    contract, missing track, bad enum value).
  - A list of fields that refer to team names: we found 10 files (sponsors,
    ownership, histories, technologies, parts contracts, ERS levels,
    buyouts, events, relationships, staff).

### E4. Documented asset names · P2
- **Needed by:** dtm-1991, dtm-2013, dtm-2012.
- **What we found:** engine logos are looked up by engine name without
  spaces (`fordcosworth.png`), and team images by team name without spaces.
- **Request:**
  - Document the lookups, and allow an explicit `"logo": "file.png"` field.
  - Allow a **car image per entry**, not just per team. In 1991, AMG's
    Ludwig ran König Pilsener black while Thiim ran West red-white.
  - **2013:** team-mates differed in sponsor and colour on almost every
    team (Schnitzer: BMW Bank black and a white-blue M3 car), down to
    details such as Abt Sportsline's red (#11) and yellow (#12) mirrors
    and dive planes. Wehrlein's #18 ran a one-off VfB Stuttgart design at
    one race. Request: a car image per entry, and optionally per round.
  - **Livery choice per team:** until per-entry images exist, let a pack
    ship several images for a team (for example `Cars/<Team>.png`,
    `Cars/<Team>_2.png`) and let the player pick which one the team shows,
    for any team. The 2013 pack has all 22 cars drawn and ready for this.
  - **Car Setup:** the screen draws the same open-wheel line art for every
    series. Request: show the selected entry's car image there instead.
    Fallback: entry image, then team image, then today's line art.
  - **Team selection:** the screen shows one car per team and the drivers
    as plain rows. Request: each driver row with portrait and car, and the
    big car image follows the selected driver. All optional: without
    per-entry images the team car shows, as today.
  - **Mockups** of this and E15 for the developers:
    https://claude.ai/artifact/Akt86veBSfVUJi4L1mYtSU

### E5. Track editor features · P2
- **Needed by:** dtm-1991, dtm-2013, dtm-2012.
- **What we found:** `use_raw_canvas_coordinates` and `raw_canvas_size` are
  needed so cars follow the drawn track.
- **Requests:**
  - Document this, plus the race screen's safe area (the bottom of the map
    is hidden behind driver cards). The session header at the top wraps to
    two lines (about 82 px) for long track names: in dtm-2013 it hid the top
    of Moscow, the Nürburgring and Zandvoort until we kept tracks below
    y=100.
  - Keep the map's aspect ratio. The overview image is stretched on each
    axis separately to fill the map panel, so a wide, short window squashes
    the track (Hockenheim 2013 at 976×423 px: ×0.94 across, ×0.39 down).
    Letterboxing, or fitting the track like the non-raw mode does, would
    keep corners the right shape.
  - Several layouts per venue, e.g. Hockenheim 1991 vs 1992.
  - Import a track from GPS/GPX coordinates.
  - A per-track pit-lane path and pit position. Today the pits are at the
    start line, so in dtm-2013 the start lines at Moscow, the Nürburgring,
    Oschersleben and Zandvoort were moved onto the pit straight. At the
    Norisring the pit lane crosses the line, so a stop spans two laps.
  - Document how the track values work. Found in the game code (dtm-2013,
    [docs/venues](venues/README.md)): `dnf_modifier` scales the crash and
    failure chance rolled every lap, so a 98-lap race at Brands Hatch retires
    four times as many cars as a 42-lap race at Hockenheim at the same value;
    `overtaking_difficulty` scales the dirty-air loss (default 1.0, not a 0–1
    scale); `pit_lane_loss_s` excludes the service time. A per-race
    retirement rate, or a note that the value is per lap, would save a
    simulator round per pack.

### E6. Currency and economy per pack · P3
- **Needed by:** dtm-1991, dtm-2013, dtm-2012.
- **1991:** DTM budgets were in Deutsche Mark and much smaller than F1.
- **2013:** the real 2013 sponsors replace the vanilla starting deals, but
  each keeps the money of the vanilla deal it replaces ($25–325m a deal,
  $137–410m a team against budgets of about $90m), so the economy the
  pack was tested with doesn't change. The amounts aren't real.
- **Request:** a currency label and symbol per pack, and global scale
  factors for salaries, costs, sponsor money and prize money.

### E7. Historical start state · P3
- **Needed by:** dtm-1991, every DTM pack (season records, see below).
- **Request:**
  - Previous-season standings and history per team and driver, to drive
    prestige and form.
  - A real date for each schedule week, for news and emails.
- **Season records (2026-11-16, game 45440200):** `history` in
  `drivers.json` fills the Drivers tab of the statistics screen with career
  totals (every DTM pack does this since the driver careers database). The
  Records tab (most wins, podiums, poles, points, DNFs in a season, best
  average finish) reads `driver_season_history`, which only
  `record_season_history` fills from seasons played in the save. A pack can't
  supply past seasons, so the tab stays empty until the first season ends.
  The same list feeds the **Career tab of the driver history window**
  (left- or right-click a driver): one row per season with `season`, `team`,
  `series`, `category` (main or junior), `races`, `wins`, `podiums`,
  `poles`, `points`, `position`. `DriverManager.load_initial` only starts an
  empty list per driver, so it says "no history recorded yet" for every real
  career.
  Request: an optional `season_history` list per driver in `drivers.json`,
  in the same row format with a calendar `year` instead of the save's
  season number, read at career start into `driver_season_history`, so both
  the Records tab and the Career tab show the real seasons. The same for
  teams if the team pages get a season list. dtm-2013 would fill it for 1984
  to 2012 from docs/drivers (position, points, races, wins, podiums, poles
  per driver and season, and now the team from dtm_team_entries.csv).

### E8. Engine sounds per supplier beyond pass-bys · P3
- **Needed by:** dtm-2013, dtm-2012, dtm-2003, dtm-2006, dtm-2010.
- **2013:** three V8s with clearly different voices (Audi RS 5, BMW M3,
  Mercedes C-Coupé).
- **Today:** only pass-bys can be tagged per supplier (`passby_audio` in
  `engines.json`). Grid idle and launch, pit fire-up and pit exit are one
  random bank (`race/race_engines.json`) shared by every car.
- **Workaround:** per-make pass-bys, and a mixed bank for the rest.
- **Request:** the same `passby_audio`-style tag for `grid_idle`,
  `grid_launch`, `pit_fireup` and `pit_exit`, so a BMW leaving its box
  sounds like a BMW.

### E9. Ambience and start sounds per track · P3
- **Answered:** implemented by the developer on 16 Nov 2026, expected in
  the next version. A `tracks.<track id>` block with `crowd` and `pa`,
  each `{"file": ..., "gain": ...}`, falling back to the pack-wide set.
  Grid and pit banks per track were not mentioned: still open.
- **Needed by:** dtm-2013, dtm-2012, dtm-2018.
- **2018:** ready to use once per-track sets exist: the Lausitzring 2018
  downshifts and starts (`JDtk4MRd1d0`, the user's favourite 2018
  recording, not in the pack today) for a Lausitzring pass-by and start, and
  the Norisring 2018 track announcer over the start
  (`pilot/pa_candidates/`, cut out of the 2018 launch) for a Norisring PA.
- **2013:** the venues sound very different: the Norisring street circuit
  between concrete walls and a packed grandstand, the open Lausitzring,
  the dunes at Zandvoort, a half-empty Moscow Raceway. The broadcasts give
  us a crowd and `cars_on_track` bed for every round.
- **Today:** `ambience/session_layers.json` and its files are one set per
  pack, so every round plays the same crowd, PA and track bed. The same
  holds for the grid and pit banks.
- **Workaround:** one season-wide set, picked for consistency.
- **Request:** an optional per-track override, for example a
  `tracks.<track id>` block in `session_layers.json` (and the race and
  session manifests) that names other files for that venue, falling back
  to the pack-wide set. This also allows a track announcer in the local
  language.
- **Post:** `docs/requests/ambience-per-track.md` (with the drive-by
  pools of E11).

### E10. Documented start-sound timing · P3
- **Needed by:** dtm-2013.
- **Today:** `grid_launch_NN` reads like "the launch", but the game starts
  it when the **3rd** of five lights comes on (0.5 s apart), 1.5 s before
  lights out; the cars move 0.5 s after that. None of this is documented,
  and a clip that starts with the getaway roars off two lights early.
  We found it by reading the game's start sequence.
- **Workaround:** every launch clip opens with 1.6 s of grid revving, so
  the getaway lands on lights out (`tools/engine_audio/starts.py`).
- **Request:** document the timing next to `race_engines.json`, or let a
  clip carry a `go_s` (where its getaway is) that the game lines up with
  lights out.

### E11. A full field crossing the line · P3
- **Answered (in part):** `passby_audio` takes a list of keys, implemented
  on 16 Nov 2026, expected in the next version. The mix settings
  (foreground count, background weight, headroom cap) are still open.
- **Needed by:** dtm-2013.
- **2013:** 22 cars, and on the first laps the field crosses the line
  nose to tail: a wall of sound, cars clearly one after another.
- **Today** (read from `ui/audio_manager.py` and `ui/hotlap_audio.py`):
  - every car gets a voice (no cap, channels grow as needed), but
    `_refresh_flyby_mix` keeps only the **3** voices nearest the line at
    full weight and turns the rest to **0.4** (-8 dB);
  - a headroom term (`min(1/sqrt(sum w^2), 2.5/sum w)`) then scales the
    whole group, so a pack is never much louder than about 2.5 cars. In
    game a full field sounds like 7 or 8 cars;
  - `passby_audio` is one clip key per supplier, so every Audi plays
    the same recording; two Audis a few tenths apart fuse into one car.
- **Workaround:** none in data for the mix. For the fusing: untag the
  suppliers so cars pick at random from a larger bank (losing the make
  sound per car), or live with it.
- **Request:**
  - make the foreground count, the background weight and the headroom
    cap settings in `hotlap_flybys.json` (or raise them for races);
  - let `passby_audio` take a list of keys, picked at random per car, so
    a make can have several recordings.

### E12. A sponsor on several teams · P3
- **Needed by:** dtm-2013, dtm-2012 (Deutsche Post on Abt Sportsline's Audi and Schnitzer's BMW).
- **2013:** make-wide partners ran on every car of a make: Puma, Sonax,
  Allgeier, Sachs and H&R on all eight BMWs, Petronas on all six
  Mercedes, Würth on all eight Audis.
- **Today:** a sponsor is one record in `sponsors.json`, and every vanilla
  sponsor backs one team. We didn't test whether two teams can hold a
  deal with the same sponsor.
- **Workaround:** each partner goes to one team of its make.
- **Request:** document whether a sponsor can back several teams, or
  allow a make-wide (supplier) deal.

### E13. Translated pack texts · P3
- **Needed by:** all packs (German first: the DTM is a German series).
- **Today (since 11 Nov 2026):** the game has a language setting with
  seven languages (en, de, fr, es, it, pt-BR, ru). The texts live in
  `ui/assets/locales/<lang>.json`, one flat file per language with about
  12,800 keys. Vanilla pack texts are in there too, under `text.pack.*`
  keys (rules, radio, nationality, team_prose and a few more), for example
  `text.pack.radio.damn_we_mistimed_that_75cc5d402`. Each key is a slug of
  the English text plus a hash, so the game seems to look a text up by its
  English wording. A pack text that matches vanilla word for word is
  probably translated. Our own texts stay in English. No pack has a locale
  file, no pack field refers to a text key, and `MODDING_GUIDE.md` does not
  mention languages. Not tested in-game.
- **Workaround:** English texts only. `tools/translatable_strings.py`
  lists a pack's own in-game texts in `seasons/<season>/translations.csv`
  (DTM 2013: 51 strings, mostly team histories, rule descriptions and
  radio messages), ready for a translator.
- **Request:** let a pack ship its own locale files, for example
  `<pack>/locales/de.json` in the same key format as the game's, merged
  over the game's files and falling back to English. Also document how a
  `text.pack.*` key is made from the English text, so a tool can write the
  keys for our texts.

### E14. Pit-entry sound · P3
- **Needed by:** dtm-2013.
- **2013:** fan recordings at the Oschersleben pit lane hold cars braking
  in off the track and rolling in on the limiter, as distinct as the exits.
- **Today:** `race/race_engines.json` has pit exits, fire-ups and
  wheelguns; nothing plays when a car enters the pit lane, so the stop
  starts in silence (or with the wheelguns).
- **Workaround:** the pit-entry recording stays a preview in the mod
  browser, outside the pack.
- **Request:** an optional `pit_entry_NN` bank, played as a car crosses
  the pit-lane entry, paired by number like the other pit clips.

### E15. Car and portrait in session screens · P3
- **Needed by:** dtm-2013, dtm-2012.
- **Why:** the player knows a car by its livery long before they read the
  name in the timing tower. The packs ship car images and portraits, but
  the race screens show neither.
- **Today:** the in-session driver panel shows name, position and team
  colour. The driver tabs show a name and a flag. The results podium shows
  flags.
- **Request:**
  - Portrait and car image (E4) in the driver panel header and the driver
    tabs.
  - Optional small car thumbnails in the timing tower and results, next to
    the number and the timing code (C6).
  - Cars and portraits on the results podium.

### E16. Track art styles the player picks · P3
- **Needed by:** dtm-2013 (and every later season with illustrated art).
- **Why:** the dtm-2013 race-day art is AI-made. Some players don't want
  AI art. The map-style images from OpenStreetMap still exist in
  `bases/dtm-era4`, in the same frame.
- **Today:** one image per track, `assets/tracks/<id>.png`.
- **Request:** an optional `track_art` block in the pack: named styles,
  each a folder with an optional `ai` flag, plus a default. The player
  picks a style in the settings, for one pack or all packs. A missing style
  falls back to the default; a pack without the block works as today.
- **Mockup:** `docs/packages/img/png/track-art-styles.png` (Hockenheim in
  map, illustrated and lines-only style).

### E17. Weekend images per track, session and result · P3
- **Needed by:** dtm-2013 (and every season with track photos).
- **Why:** the race weekend is the heart of the game, but its screens are
  plain: the loading screens are a bar on black, the Simulate / Take Part
  screens are two grey boxes, and the results are tables only. The team
  dashboard shows how much one photo adds.
- **Today:** no images on the weekend screens; the dashboard has a
  background photo. Weather, round and results are known but not shown
  with a picture.
- **Request:** optional images in the pack, picked by track, session,
  result of the player's team (win, podium, points, no points, retired),
  each falling back to a more general one and
  finally to today's screen. Used on the loading screens, the choice
  screens, a short card between sessions, the grid and the results.
  Two new screens: a start of the weekend (track, round, three-day
  weather, Start weekend) and an end of the weekend (your team's result
  and points, picture by outcome).
  Optional: an archive image per track with a year and a caption.
- **Mockup:** `docs/requests/img/weekend-images/` (19 screens, 2013
  season) and `docs/requests/img/weekend-journey/` (a full weekend).
  Request text in `docs/requests/weekend-images.md`.

### E18. Separate team logo and team icon · P3
- **Needed by:** dtm-2012, dtm-2013, btcc-1991 (maker emblems as team icons,
  `"team_tiles": "maker"` in `art/logos.json`), dtm-2018 (planned the same
  way), and every historic season.
- **Why:** older teams, and teams in other series, have classic logos:
  wide wordmarks, crests or fine detail. Shrunk to a table row they can't
  be read. On TV and timing screens the make usually stood in for the
  team, but every team still had its own logo on the trucks, the
  motorhome, the kit and its press material.
- **Today:** one image per team, used both in small tables and on large
  screens.
- **Workaround:** the engine maker's emblem as the team image. Tables read
  well, but the real team logos are not in the game at all.
- **Request:** two optional images per team: a **team logo** (full logo
  for team selection, dashboard, news and profile) and a **team icon**
  (small and square, for tables, standings, timing and lists). With only a
  logo, the game uses it for both, as today, so existing packs keep
  working.

### E19. Weekend images per team · P3
- **Needed by:** dtm-2013 (and every season with team photos).
- **Why:** the player follows one team all season. A photo of their own
  cars at this track says "this is my weekend" far more than a general
  track photo. Teams also have their own photos: the pit crew, the
  garage, their cars on the grid. Packs often have such photos with the
  team's permission.
- **Today:** no images on the weekend screens (E17). The dashboard has one
  background photo per pack, the same for every team.
- **Request:** let a team override the weekend images of E17. The game
  looks for a picture in this order:
  1. the player's team, this track, this session
  2. the player's team, this session (any track)
  3. this track, this session (E17)
  4. the pack, this session (E17)
  5. today's screen without a picture
  The same works for the start of the weekend, the result pictures (win,
  podium, points, no points, retired) and the dashboard background. Each
  entry can hold several pictures; the game picks one at random. A team
  without its own pictures sees the pack's pictures, so nothing changes
  for packs that don't use it.

  ```json
  "weekend_images": {
    "race": ["race.jpg"],
    "nuerburgring13": { "race": ["nbr_start.jpg"] },
    "teams": {
      "bmw_mtek": {
        "dashboard": ["mtek_garage.jpg"],
        "race": ["mtek_grid.jpg"],
        "nuerburgring13": { "qualifying": ["mtek_nbr_quali.jpg"] },
        "results": { "win": ["mtek_win.jpg"], "retired": ["mtek_garage.jpg"] }
      }
    }
  }
  ```
- **Mockup:** `docs/requests/img/weekend-journey/` (BMW Team MTEK at the
  Nürburgring). The qualifying screens there show Wittmann's MTEK car;
  with this item a pack could show it to MTEK players only and a neutral
  track photo to everyone else.

### E20. Dashboard images in random order · P3
- **Answered:** added by the developer on 16 Nov 2026, expected in the
  next version. Key name not given yet: check the next modding guide.
- **Needed by:** dtm-2013, dtm-2012 (every pack with several dashboard
  images).
- **Why:** a pack or team set has several dashboard pictures, but the
  player mostly sees the first one. It gets dull over a long career.
- **Today:** the dashboard moves through `dashboard_bg<N>.png` (and the
  team sets in `assets/dashboard_bgs/`) in number order, always starting
  with image 1.
- **Workaround:** put the favourite picture in slot 1.
- **Request:** an optional setting, for example
  `"dashboard_order": "random"`, that starts at a random image or
  shuffles the set. Without it the order stays as today.
- **Post:** `docs/requests/dashboard-random-order.md`.

### E21. Backgrounds that fit any window, and a pack logo · P2
- **Needed by:** dtm-2013 (wordmark in the menu image), dtm-2012 and
  dtm-2018 (planned the same way), and every pack with its own art.
- **Why:** on a wide window (here about 21:9, 2000×857) the menu photo is
  cut at the top and bottom. The "DTM 2013" wordmark sits in the top right
  of the image, so only the bottom half of "DTM" shows. The race map has
  the same problem the other way round: it is stretched to the panel (E5).
- **Today:** `assets/title_bg.png` is scaled to cover the window and the
  middle is cut out. A pack has no way to place a logo of its own, so we
  draw the series wordmark into the photo (`tools/menu_art.py`,
  `"logo"` in `art/menu.json`). The game's own `title_logo.png` is drawn
  as a separate layer and always fits.
- **Workaround:** keep the wordmark well inside the 16:9 frame. This only
  helps up to a certain width, and it is wasted space on 16:9.
- **Request:**
  - An optional **pack logo** (`assets/pack_logo.png`), drawn as its own
    layer in the top right of the main menu, sized and placed like the
    game logo so it is never cut. Optionally also small on the loading
    screens and the dashboard header.
  - An optional **focus point** per background image (for example
    `"title_bg_focus": [0.75, 0.6]`, fractions of the image) that the
    crop keeps in view, instead of always the middle. The same for the
    dashboard backgrounds.
  - Optionally, a second image for very wide windows
    (`title_bg_wide.png`, 21:9), used when the window is wider than
    about 2:1.
  - Packs without these files look as today.
- **Post:** `docs/requests/responsive-images.md` (with E5's map aspect
  ratio and safe areas), screenshots in `docs/requests/img/responsive/`.

### E22. Back-straight pass-bys (second listening point) · P3
- **Needed by:** dtm-2013, dtm-2012, dtm-2010, dtm-2018 (Brands Hatch,
  Norisring, Hockenheim, Oschersleben, Zandvoort, Shanghai, Valencia),
  and any pack with one of the tracks below.
- **Why:** on many tracks the cars come past a second time, close to the
  finish line: on the back straight (German *Gegengerade*), across a
  harbour or behind the pits. At the Norisring the grandstand sits between
  the start straight and the back straight, so a fan hears every car
  twice a lap: loud and close, then further away and from the other side.
- **Examples** (`tools/second_pass_maps.py`, layouts in
  `docs/requests/img/second-pass/`, all on `all.png`; lap progress where
  the cars come back within 250 m of the line, and the closest point):

  | Track | Second pass | Closest |
  |---|---|---|
  | Zandvoort | Hugenholtz, behind the pits, 0.12 to 0.26 | 48 m |
  | Brands Hatch Indy | Cooper Straight, 0.42 to 0.66 | 77 m |
  | Suzuka | the Esses, 0.18 to 0.28 | 79 m |
  | Adelaide (1989) | the last section, 0.80 to 0.89 | 93 m |
  | Brands Hatch GP | Cooper Straight, 0.31 to 0.41 | 95 m |
  | Norisring | back straight to the Schöller-S, 0.46 to 0.70 | 114 m |
  | Hockenheim | the Sachs hairpin in the Motodrom, 0.79 to 0.89 | 118 m |
  | Hungaroring | turns 2 and 3, 0.10 to 0.19 | 125 m |
  | Sepang | back straight, 0.75 to 0.83 | 126 m |
  | Shanghai Pudong (DTM 2010) | back straight, 0.49 to 0.67 | 126 m |
  | Donington Park | the Melbourne loop, 0.75 to 0.90 | 128 m |
  | Singapore | turns 1 to 3, 0.12 to 0.18 | 131 m |
  | Abu Dhabi | three times: 0.10 to 0.16, 0.77 to 0.80, 0.84 to 0.92 | 134 m |
  | Jarama | three times: 0.28 to 0.33, 0.37 to 0.45, 0.68 to 0.76 | 136 m |
  | Monaco (street circuit) | across the harbour, 0.61 to 0.68 | 141 m |
  | Oschersleben | back straight, 0.77 to 0.85 | 175 m |
  | Bahrain | the infield straight, 0.47 to 0.53 | 195 m |
  | Valencia Ricardo Tormo | the stadium section, 0.81 to 0.90 | 204 m |

  Counter-examples (`counter.png`), where nothing comes back within
  250 m and the finish line alone is right: Monza, Imola, Melbourne,
  the Red Bull Ring and the Lausitzring.

- **Today:** pass-bys play at one point only, the finish line
  (`ui/hotlap_audio.py`, the "finish line audio observer"). A car on the
  back straight is silent, so between two pass-bys the track goes quiet.
- **Workaround:** none in data. A track bed in the ambience (E9) can hint
  at distant cars, but not in time with the real ones.
- **Request:**
  - an optional list of extra listening points per track, for example
    `"flyby_points": [{"progress": 0.58}]` in the track file: the game
    plays a pass-by when a car crosses that progress (maybe muffled, or
    panned to the other side);
  - the volume set automatically from the distance between that point
    and the start line, which the game can work out from the track's
    `points`; an optional `"volume"` per point overrides it;
  - an optional **far pass-by pool** (`far_passby` clips in
    `hotlap_flybys.json`, recorded from across the track), used at those
    points, falling back to the normal pass-by played quieter;
  - tracks without the list sound as today.
- **Post:** `docs/requests/second-pass-sound.md`.

### E23. Car image per title sponsor · P3
- **Needed by:** every DTM pack from 2000 to 2018 (Mercedes teams named
  after their sponsor), and any pack with sponsor liveries.
- **Real:** a livery follows the main sponsor. When STIHL left a Mercedes
  team, the car changed colour from orange to the new sponsor's colours.
- **Today:** the car image is found by team name and, since 0.99.6, by
  season or year (`<Team>Season<N>.png`, `<Team><Year>.png`, found in the
  code, not in the modding guide). A pack can show a new livery from a
  given season, but it can't know who the sponsor will be in a career.
- **Workaround:** the real liveries by season, for the years that
  happened. In a career where the sponsor changes, the car keeps its old
  look.
- **Request:** an optional image per title sponsor, for example
  `Cars/<Team>_<Sponsor>.png`, used while that sponsor holds the title
  slot. Fallback: the season image, then the team image. Please also add
  the seasonal names to the modding guide.
- **Post:** `docs/requests/title-sponsor-liveries.md` (follow-up to
  johnduff71's "Seasonal Livery Support" thread).

### E24. Car numbers drawn by the game · P2
- **Needed by:** every pack with car images (all DTM packs).
- **Real:** numbers belong to the driver or the entry, and change: the
  champion takes #1, a new driver brings a new number.
- **Today:** the number is painted into the car image. When drivers move
  in a career, the image shows the old number. One image per team also
  shows one number for both cars.
- **Workaround:** none. Our images show the lower number of the 2013 pair.
- **Request:** an optional `number_box` per team or per image (position,
  size, font colour, background colour) where the game draws the entry's
  current number. Images without it stay as today. Works well with a car
  image per entry (E4). The same idea could cover the driver's name and
  flag on the car, and the title sponsor (E23).
- **Post:** raised as a follow-up in
  `docs/requests/title-sponsor-liveries.md` (number, driver name and
  flag, title sponsor drawn on the car).

---

*Kept up to date as we find more. Collected while building
`seasons/dtm-1990` to `dtm-1992` and `dtm-2013`.*
