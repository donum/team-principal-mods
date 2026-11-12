# Package: Race Control and Overtaking Aids

Starts, flags, safety cars, penalties, DRS and push-to-pass. Part of the
[feature packages](README.md).

- **Wishlist items:** [B6](../DEVELOPER_WISHLIST.md#b6-drs-rules-per-session--p2),
  [B11](../DEVELOPER_WISHLIST.md#b11-race-control-rules--p3), and the start
  and red-flag parts of [A3](../DEVELOPER_WISHLIST.md#a3-configurable-sessions-and-race-format--p2).
- **Modes:** all three.
- **Status:** outline.

## 1. What the game has today

| Setting | Mode | What it does |
|---|---|---|
| `drs_policy` | Formula | On or off for the whole weekend, zones, from lap 3 |
| `ers_policy` | Formula | Spec, open development or off |
| `safety_car_policy` | Both | None, physical only, all types (VSC) |
| `formula_red_flags` | Formula | Stop and restart, up to 2 per race |
| `oval_start_procedure` | Oval | Double-file pace lap or direct start |
| `oval_green_white_checkered`, `oval_last_lap_caution`, `oval_lucky_lapper` | Oval | Oval finish and caution rules |
| `local_yellow` | Formula config | Local yellows after a spin |

## 2. Every need we know

| Seasons | Need |
|---|---|
| DTM 2000, 2001, 2021 on | Rolling starts, two abreast in a start corridor from 2021 |
| DTM 1986, 1991 | Red flag with the result on aggregate, or shortened |
| DTM 2007 | Pit lane closed under the safety car |
| DTM 2013 | DRS in the race only, once per lap anywhere, not the last 3 laps |
| DTM 2015, 2016 | DRS 3 times per lap; a budget per race by track length |
| DTM 2019, 2020 | Push-to-pass 12 times per race; DRS for all but the leader in the last 5 laps |
| DTM 2022 on | Full-course yellow at 60 km/h |
| DTM 2023 on | Penalty lap |

## 3. The building blocks

- **Start procedure** shared by all modes: standing, rolling single file,
  rolling two abreast.
- **Red flag result:** `restart`, `aggregate`, `shortened`.
- **Overtaking aids as a budget:** `uses_per_lap`, `uses_per_race`,
  `zones` or `anywhere`, `gap_s`, `disable_last_laps`, `not_for_leader`,
  per session. DRS, push-to-pass and attack modes are three presets.
- **Neutralisations:** safety car, VSC, FCY with a speed, slow zones, with
  `pit_lane_closed` and whether a stop under it counts.
- **Penalties:** time, drive-through, stop-go, penalty lap, grid drop.

## 4. Fits the existing options

- `drs_policy` and `ers_policy` keep their keys; options get the budget
  fields, with today's behaviour as the default.
- `oval_start_procedure` becomes a shared `start_procedure`.
- `formula_red_flags` gets a `result` field.

## 5. Overlaps

| Shared block | Package |
|---|---|
| Stops under SC or FCY don't count | [Tyres and pit stops](tyres-and-stops.md) |
| Per-session values | Scopes in the [README](README.md) |
| Rain red flags | [Calendar and weather](calendar-and-world.md) (D4) |

## 6. Endurance

- Slow zones (Code 60), several safety cars on long tracks.
- Penalties served at the next stop, minimum pit time.
- Night procedures.

## Evidence log

| Item | Season | Need | Source | Status |
|---|---|---|---|---|
| B6 | DTM 2013 to 2020 | DRS and push-to-pass rules | [dtm_rules.html](../dtm_rules.html) | Checked |
| B11 | DTM 2007, 2022, 2023 | Pit closure, FCY, penalty lap | [dtm_rules.html](../dtm_rules.html) | Checked |
