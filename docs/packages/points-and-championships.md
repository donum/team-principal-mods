# Package: Points and Championships

How results turn into points, and which titles a series awards. Part of
the [feature packages](README.md).

- **Wishlist items:** [B3](../DEVELOPER_WISHLIST.md#b3-points-table-per-race-drop-scores--p2),
  [B4](../DEVELOPER_WISHLIST.md#b4-more-classifications--p2),
  [B8](../DEVELOPER_WISHLIST.md#b8-qualifying-points--p2),
  [B9](../DEVELOPER_WISHLIST.md#b9-non-scoring-guest-entries--p2),
  the points part of [C7](../DEVELOPER_WISHLIST.md#c7-feeder-series-with-real-race-weekends--p2).
- **Modes:** formula, oval, endurance.
- **Status:** outline. DTM needs come from the wish list and
  [dtm_rules.html](../dtm_rules.html); F1 and others are from memory.

## 1. What the game has today

| Setting | Mode | What it does |
|---|---|---|
| `points_system` options with a `points` array | Both | One table for every race (`modern_top10`, `top12`, `top8`; oval top 35 and top 40) |
| `POINTS_TOP10` | Formula `constants.py` | The default table |
| `pole_point`, `fastest_lap_point` | Formula | +1 each; the fastest-lap point goes to the holder wherever they finish |
| `oval_pole_point`, `oval_fastest_lap_point` | Oval | The same for oval packs |
| `oval_stage_racing` | Oval | Three stages (`stage_fractions` 0.25, 0.25, 0.5), `stage_points` 10 to 1 for the first two, a caution at each stage end |
| `oval_championship_format` `chase`, `oval_chase_field`, `oval_chase_length` | Oval | A playoff: 8 to 16 drivers over the last 5 to 10 races, seeded (`oval_chase.seed_base`, `seed_step`) |
| Junior series | Both | One points table for all races |

## 2. Every need we know

**DTM**

| Seasons | Need |
|---|---|
| 1984, 1985 | Two-heat rounds give **half points** per heat |
| 1988 to 1996 | Two heats, full points each |
| 1987, 2018, 2021 on | **Guests** race but don't score; points go to the next eligible driver |
| 1984 | Only German drivers scored |
| 1991 | Drivers', teams' and manufacturers' titles (only the best car of each make scores), the **ITR Fahrerpokal** (DTM rounds plus non-championship rounds), a **privateer cup** paid in prize money |
| 1992 | **Drop scores** (Streichresultate) |
| 2001, 2002 | Qualifying race 3-2-1, main race 20-15-12-10-8-6-4-3-2-1 |
| 2018 on | 3-2-1 for the top three in each qualifying |
| 2022 | Fastest-lap point only for a top-10 finisher |
| 2013 feeders (C7) | Points per race of the weekend, pole and fastest-lap points (German F3), two classes scored apart (DTC) |

**Formula 1**

| Seasons | Need |
|---|---|
| 1950 to 1990 | Only the best N results count, sometimes split by half-season |
| 1950s | Shared drives: points split between the drivers of one car |
| 1950 to 1959, 2019 to 2024 | Fastest-lap point (from 2019 only in the top 10) |
| Since 1958 | Constructors' title; until 1978 only the best car of each team scores |
| Any | **Half points** when a race stops before 75% |
| 2014 finale | **Double points** |
| 2021 on | Sprint points (3-2-1, then top 8) |

**Others:** NASCAR stage points and playoffs (in the game for ovals),
IndyCar double points at the Indy 500 and a point for leading a lap,
WEC points scaled by race length and points for pole, BTCC
independents' trophy and a point for leading a lap, Super GT points that
also set the success ballast (see [Balance](balance-and-homologation.md)).

## 3. The building blocks

- **A points scheme** is a named block with tables per session type:
  `race`, `sprint`, `heat`, `qualifying`, `qualification_race`, `stage`.
  Each race of the weekend ([Weekend format](weekend-format.md)) names the
  table it uses.
- **Bonuses** as rows with a condition: `pole`, `fastest_lap`
  (`min_finish_position: 10`), `led_a_lap`, `most_laps_led`.
- **Multipliers:** per event (`double: true`), by distance completed
  (half points below 75%), by race length (endurance).
- **Who scores:** reads entry tags from [Entries](entries-and-crews.md)
  (`guest`, nationality rule). Points of non-scorers go to the next
  eligible driver or are dropped.
- **Counting rules:** drop the worst N, best N of each half, best car of
  each team or make.
- **Championships as a list:** drivers, teams, makes, classes, cups, each
  with its own events (including non-championship rounds), eligible entries
  (`privateer`, `rookie`, `class: "Pro-Am"`) and its own scheme. A prize
  can be money instead of a title.
- **Formats:** `full_season` or `chase` (exists for ovals), so a formula
  or endurance pack can pick a playoff too.

## 4. Fits the existing options

- `points_system` stays the category, and an option's `points` array keeps
  working as the race table. A new optional `scheme` field points to a
  named block for anything more.
- `pole_point` and `fastest_lap_point` become bonus rows in the default
  scheme; the options switch them as today.
- `oval_stage_racing` and the chase options become shared, so any mode can
  use them. The `oval_` keys stay as aliases.

## 5. Overlaps

| Shared block | Package |
|---|---|
| A table per session and race | [Weekend format](weekend-format.md) |
| Entry tags (guest, privateer, class) | [Entries](entries-and-crews.md) |
| Results feed success ballast | [Balance](balance-and-homologation.md) |
| Junior weekends (C7) | [Calendar and world](calendar-and-world.md) |
| Prize money per championship | E6 in [Calendar and world](calendar-and-world.md) |

## 6. Endurance

- Points scaled by race length (6 h, 8 h, 24 h), double points at Le Mans.
- Points per class, per crew (all drivers of the car score), with a
  minimum drive time to score.
- Points at the 6 h and 12 h marks of a 24 h race, like stage points.
- Separate titles for drivers, teams and makes in each class.

## Evidence log

| Item | Season | Need | Source | Status |
|---|---|---|---|---|
| B3 | DTM 1984, 1985 | Half points per heat | [dtm_rules.html](../dtm_rules.html) | Checked |
| B3 | DTM 1992 | Drop scores | `seasons/dtm-1992/research` | Checked |
| B4 | DTM 1991 | Teams', makes', ITR Fahrerpokal, privateer cup | `seasons/dtm-1991/research` | Checked |
| B8 | DTM 2001, 2002, 2018 on, 2022 | Qualifying race and qualifying points | [dtm_rules.html](../dtm_rules.html) | Checked |
| B9 | DTM 1984, 1987, 2018, 2021 on | Non-scoring guests | [dtm_rules.html](../dtm_rules.html) | Checked |
| B3 | F1 1950 to 1990, 2014, 2021 on | Best results, double points, sprint | Memory | To source |

## Open questions

- DTM 1991 privateer cup: the payout table.
- DTM 1980s: which seasons used drop scores?
