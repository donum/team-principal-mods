# Package: Tyres and Pit Stops

Which tyres a series has, who makes them, and the rules for using them and
for stopping. Part of the [feature packages](README.md).

- **Wishlist items:** [B5](../DEVELOPER_WISHLIST.md#b5-mandatory-pit-stops-and-pit-windows--p1),
  [B7](../DEVELOPER_WISHLIST.md#b7-tyre-allocation-rules--p2),
  [B10](../DEVELOPER_WISHLIST.md#b10-pit-stop-procedure-rules--p3),
  [B12](../DEVELOPER_WISHLIST.md#b12-tyre-and-stop-rules-as-data--p1),
  [D6](../DEVELOPER_WISHLIST.md#d6-damage-repair-at-pit-stops--p2) (repair as a stop service),
  [D8](../DEVELOPER_WISHLIST.md#d8-custom-tyre-compounds--p2),
  [D9](../DEVELOPER_WISHLIST.md#d9-tyre-suppliers-beyond-ratings--p2).
  B12 has the full per-season table.
- **Modes:** formula, oval, endurance.
- **Checked against:** game version 0.99.6 (beta). F1 and other-series facts
  are from memory and still need sources (see the evidence log).

## 1. What the game has today

| Setting | Where | What it does |
|---|---|---|
| Compounds | `tyremodel.json` | Fixed keys soft, medium, hard, intermediate, wet. Each has grip, wear, cliff, warm-up and temperature window. Medium can be null. |
| `mandatory_compound_count` | `tyremodel.json` | Number of different dry compounds per race (F1 rule) |
| `formula_compound_usage` | `regulations.json` | Turns that rule on or off |
| `weekend_tyre_allocation` | `regulations.json` | `unlimited`, `light`, `strict` (12 sets at the lowest) |
| `tyre_profile` | `regulations.json` | All tyres wear faster or slower |
| Suppliers | `tyre_suppliers.json` | Several suppliers in one series. Each team has a contract. Grip, durability and temperature per compound, with yearly trend, variance and development. Works, partner and customer prices. Suppliers join and leave. |
| `pit_out_temp_c` | `tyremodel.json` | Tyre temperature after a stop (a stand-in for tyre warmers) |

So a **tyre war already works on track**: two teams on different
suppliers get different grip and wear. What is missing is mostly names,
rules and supplier detail.

## 2. Define the tyres a series has (D8)

Each compound in `tyremodel.json` gets:

- an id, a `label`, a short letter and a `color` used on every screen
  (DTM 2013: "Standard" S white, "Option" O yellow);
- `category: dry / wet`, with any number of each (one dry tyre in DTM 2012,
  two in 2013, three in F1, five in the F1 C1 to C5 range);
- its physics values, as today.

**Range and nomination.** A supplier has a range (F1: C1 to C6). For each
event the pack, or the supplier, picks which ones come and which label they
get (hard, medium, soft). The same tyre can be "soft" at one track and
"medium" at the next. Data: `range` in the supplier, `nomination` per track
or per event.

## 3. Tyre and stop rules (B12)

Every rule below is one row in a list. The game checks the list after the
race and gives the penalty. The AI strategy planner reads the same list
and only picks plans that pass.

| Rule | Example | Series |
|---|---|---|
| `min_dry_compounds: N` | 2 | F1 2007 on (exists today) |
| `must_use: X, min_laps` | Option at least once | DTM 2013, IndyCar (each tyre 2 laps), BTCC (option in 1 of 3 races) |
| `max_laps_on: X` or `max_share_on: X` | Option for half the race at most | DTM 2014 |
| `max_stint_laps` | 18 laps per set | F1 Qatar 2023 |
| `min_sets_used` | 3 sets | F1 Monaco 2025 |
| `min_stops: N`, per race | 2; Saturday 1 and Sunday 2 | DTM 2001 to 2026, F1 Monaco 2025, Super Formula (1) |
| `no_stop_first_laps`, `no_stop_last_laps` | Pit window closed in the first 3 and last 3 laps | DTM 2013 |
| `stop_window`, per stop | Middle third; minute 20 to 40; stop 1 in minutes 10 to 20, stop 2 in 39 to 45 | DTM 2008, 2012, 2014, 2022 to 2026, Super Formula |
| `stop_counts_if` | All four tyres; not a damage stop; not under SC or FCY | DTM 2001 on, 2013, 2014, 2021, 2022, 2024 |
| `windows_off_if_wet` | Window dropped in a wet race | DTM 2014 |
| `start_on_qualifying_tyre: top N` | Top 10 | F1 2010 to 2021, DTM 2023 on |
| `no_tyre_change` | One set for qualifying and race; no change in the Saturday race | F1 2005, DTM 2016 |
| `sets_per_weekend` and per compound | 10 tyres, 5, 7, 9 sets, 4 sets for two races | DTM 1988 to 2019, F1 13 sets |
| `sets_per_race_day`, per track | 3 or 4 new sets by track, plus a test pool | DTM 2022 to 2026 |
| `new_sets_max` in qualifying | 2 | DTM 2019 |
| `discarded_set_lost` | A wheel taken off leaves the allocation | DTM 2026 |
| `return_sets_after` | Hand back sets after each session | F1 |
| `session_compound` | Q1 hard, Q2 medium, Q3 soft | F1 2023 alternative allocation, F1 sprint 2023 |
| `tyre_warmers: banned / max_temp_c` | Banned | DTM 2003, 2017; F2 |
| `rules_lapse_if_wet` | Compound rule off once wets are used | F1 |
| `wet_start_tyre` | Full wets when the race starts behind the safety car | F1 |

The full list of which DTM season needs which row is in
[B12](../DEVELOPER_WISHLIST.md#b12-tyre-and-stop-rules-as-data--p1) and
[B5](../DEVELOPER_WISHLIST.md#b5-mandatory-pit-stops-and-pit-windows--p1).
Race length, start type, red flags and heat gaps are in
[A3](../DEVELOPER_WISHLIST.md#a3-configurable-sessions-and-race-format--p2).

**Scope** of each rule: `race`, `weekend` (BTCC) or `season`.
**Applies to:** `all`, a class, or `top N` from qualifying.
**Penalty:** time added, drive-through, disqualification, or grid drop
next round.

**What this answers from the questions:**

- *F1 must use both tyres:* exists today (`min_dry_compounds: 2`).
- *DTM 2013 two stops and two tyres:* `min_stops: 2`, no stop in the
  first or last 3 laps, and `must_use: option`. The two tyres came from the
  option rule, not from the two stops.
- *Monaco 2025:* `min_stops: 2`, `min_sets_used: 3`,
  `min_dry_compounds: 2`.

## 4. Suppliers (D9)

The supplier file already gives each tyre maker its own grip and wear.
Ideas to make a tyre war feel real:

- **Own physics per supplier.** A supplier can change any compound field:
  warm-up speed, cliff, temperature window. One make warms up fast and
  falls off a cliff; another is slow to warm and lasts.
- **Weather and heat strengths.** Grip by track temperature and in the
  wet (Michelin strong in heat, weak in the wet).
- **Own ranges.** Each supplier brings its own set of compounds, names and
  colours.
- **Works development.** The works partner gets tyres built for its car
  (Bridgestone and Ferrari in 2004). The prices for works, partner and
  customer exist; this would add a performance gap.
- **Supply caps and tenders.** A limit of teams per supplier, or a
  control-tyre tender that runs for N seasons (DTM: Dunlop 2000, Hankook
  2011, Michelin 2021, Pirelli 2023).
- **Failures.** Rare structural failures. They can lead to a new rule from
  race control, e.g. a stint limit for the next race (Indianapolis 2005,
  Qatar 2023).
- **Look.** Supplier logo and sidewall colour on the car art, and the
  supplier name in timing and strategy screens.

## 5. Why this scales

- **One rule checker** used by the race result, the strategy screen and
  the AI. A new rule is a new row type, not new code in many places.
- **The AI as a search over plans.** The planner lists stint plans
  (stops, compounds, laps) and keeps the fastest that passes the rules.
  With rules as data, it handles any mix without special cases.
- **Compound ids from data.** Remove the fixed soft, medium and hard list
  from the allocation screen, presets, strategy tools and timing. This is
  the base for everything else.
- **Defaults keep old packs working.** No rule list means today's F1
  rules.

## 6. Ideas ranked

| Rank | Lever | Effort | Unlocks |
|---|---|---|---|
| 1 | Compounds from data with names and colours (D8) | Medium | DTM 2012 and 2013, IndyCar, BTCC, any one-tyre series |
| 2 | `min_stops` and stop windows (B5) | Small | DTM 2000 to 2013, Super Formula, F1 Monaco 2025 |
| 3 | Rule list with `must_use`, `max_laps_on`, `max_stint_laps` | Medium | DTM 2013, 2014, IndyCar, BTCC, F1 Qatar 2023 |
| 4 | Sets per compound and per weekend (B7) | Small | DTM 2000s, F1 any year |
| 5 | `start_on_qualifying_tyre` | Small | F1 2010 to 2021, DTM 2023 on, Super GT |
| 6 | Supplier physics, weather strength, ranges | Medium | Tyre wars: DTM 1984 to 1995, F1 1997 to 2006, Super GT, WEC |
| 7 | Session compound rules | Small after 1 | F1 2023 alternative allocation, sprint shootouts |

## 7. Other series this unlocks

- **F1**: Goodyear and Bridgestone (1997, 1998), Bridgestone and Michelin
  (2001 to 2006), the 2005 no-change rule, the C1 to C6 range,
  Monaco 2025, Qatar 2023.
- **IndyCar**: primary and alternate tyres, each used for at least two
  laps on road and street courses.
- **BTCC**: hard and soft Dunlop, the soft used in one of three races.
- **Super GT**: open tyre war, teams must declare sets, start on
  qualifying tyres.
- **Super Formula**: one stop with a four-tyre change, after a set lap.
- **WEC / Le Mans**: sets per event, double stints, past tyre wars.
- **Supercars**: hard and soft sets per race.
- **Formula E**: one all-weather tyre.
- **F2 / F3**: a compound rule in the feature race only, warmers banned.

## Fits the existing options

- `formula_compound_usage`, `weekend_tyre_allocation` and `tyre_profile`
  stay regulation categories. Each option gets an optional `rules` list
  (rule rows) next to today's fields (`dry_sets_per_driver`). Old options
  without `rules` behave as today.
- `mandatory_compound_count` in `tyremodel.json` becomes the default for
  the `min_dry_compounds` row.
- `pitstops.strategy` is `wear_threshold` today. A rule-aware planner can
  be a new value (`plan`), so packs opt in.
- Supplier fields in `tyre_suppliers.json` stay. Physics overrides are an
  optional `compounds` block per supplier, merged over `tyremodel.json`.

## Overlaps with other packages

| Shared block | Also used by |
|---|---|
| Pit stop as a list of services (tyres, fuel, repair, driver change) | D6 damage repair, [Entries](entries-and-crews.md) (driver swaps, C8), endurance |
| What counts as a stop (not under SC or FCY) | [Race control](race-control.md) (B11) |
| Rules per race of the weekend | [Weekend format](weekend-format.md) |
| Start on qualifying tyres, sets in qualifying | [Weekend format](weekend-format.md) (stage car state) |
| Tyre supplier as a contract | [Balance](balance-and-homologation.md) (supplier contracts like customer cars, C4) |
| Supplier logo and colour | [Presentation](presentation.md) |

## Endurance

- Pit stop order and crew limits: refuel first, then tyres; a set number
  of mechanics; a minimum stop time.
- **Double stints** on one set, and sets per event instead of per race.
- Driver change as a stop service, with its own time.
- Refuel rate and fuel per stint as the real limit on stint length.

## Evidence log

| Item | Season | Need | Source | Status |
|---|---|---|---|---|
| B5, B12 | DTM 2001 to 2026 | See the B12 table | [dtm_rules.html](../dtm_rules.html) | Checked |
| B12 | F1 2005, 2007, 2010 to 2021, 2023, 2025 | See section 3 | Memory | To source |
| D9 | DTM 1984 to 1995 tyre war | Supplier per team | `seasons/dtm-199*/research` | Checked |
| D9 | F1 1997 to 2006 tyre wars | Supplier physics | Memory | To source |

## Open questions

- DTM 2012: the exact pit windows per round.
- DTM 2013: did both stops need four new tyres?
