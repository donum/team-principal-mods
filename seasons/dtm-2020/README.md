# DTM 2020: Season Pack

Status: **generated and builds, not yet tested in-game or in the simulator.**
The data was generated with `tools/season_from_research.py` from
`research/`, configured in `gen.json`. For the sourced facts behind it
(calendar, entry list, standings, rules, sources and unverified points), see
[research/season.md](research/season.md). Open work is in
[docs/plans/DTM2020_BACKLOG.md](../../docs/plans/DTM2020_BACKLOG.md).

2020 was Audi's last DTM season as a works maker: 9 weekends with 2 races
each, Audi and BMW only, 16 cars, run around COVID-19 in Germany and the
Benelux countries.

**Era base:** 2020 builds on [`bases/dtm-era5`](../../bases/dtm-era5)
(2019–2020, 2.0 turbo four-cylinders), which itself builds on
[`bases/dtm-era4`](../../bases/dtm-era4) (2012–2018). The Class One chassis
carried over, so the traced tracks, tyre model, damage, car parts, car
profiles and the Hankook tyre come from era 4. Era 5 changes the engines,
the weight, the rules and the sounds. 2020 is the **mother season** of
era 5: the first one built on it, so era-wide work (sounds, tracks,
calibration) is planned in its backlog, and 2019 inherits it later.

## How it's built

- **Teams and drivers:** 8 teams and 16 race seats from
  `research/entries.csv`, with the real car numbers. Audi Sport Team WRT
  runs three cars, Orlen Team ART one customer BMW for Robert Kubica.
  Benoît Tréluyer (Duval's stand-in at round 8) is a reserve.
- **Ratings:** from each team's average points per car
  (`team_rating_from: average`), spread over 53–58 (`rating_range`). That is
  wider than era 4's 55–57.5 because Audi won 16 of 18 races. Driver skill
  11–18 from the points. Estimates, not history.
- **Previous position:** the 2019 teams' standing
  (`seasons/dtm-2019/research/standings_other.csv`). ART, new in 2020, is
  last (8th).
- **Colours:** first estimates from each team's usual colours, not checked
  against 2020 photos yet. No sponsors yet.
- **Two races per round:** `"races_per_round": 2` gives each race its own
  game week, with its own qualifying, as in 2020. The back-to-back weekends
  (Lausitz, Nürburgring, Zolder twice) push the later races back, so the
  season runs from week 31 to week 48 instead of ending in early November.
- **Engines:** Audi RC8 2.0 TFSI and BMW P48 Turbo (`bases/dtm-era5/gen.json`),
  90 kg each on a 980 kg car for the 1,070 kg minimum with driver and fuel.
  Power and reliability are first estimates.
- **Sounds:** the game's vanilla sounds. No turbo recordings yet, and the
  era 4 V8 sounds are switched off for era 5 (`base.json` `"audio"`,
  `in_pack: false`).

## Rules (`bases/dtm-era5/patches/regulations.json`, then `patches/regulations.json`)

| Rule | 2020 | In the pack |
|---|---|---|
| Race | 55 min + 1 lap, 1 mandatory stop | `race_laps` per track from the calendar; tyre wear decides the stops |
| Qualifying | Separate session before each race | `qualifying_format: session_60` |
| Qualifying points | 3-2-1 for the top three | `pole_point: enabled` (1 point for pole only) |
| Points | 25-18-15-12-10-8-6-4-2-1 | `modern_top10` (era 4) |
| Push-to-pass | +60 hp (up from 30) | `ers_policy: spec` |
| DRS | Unrestricted use | `drs_policy: enabled` |
| Refuelling | Not allowed | `formula_refueling: banned` |
| Tyres | Hankook | era 4 tyre model and Hankook supplier |
| Weight | 1,070 kg with driver and fuel | `chassis_minimum_weight: dtm_2019` (980 kg + 90 kg engine) |
| Entries | WRT ran three cars | `formula_team_entry_cap: three` |
| Car speed | about 610 hp | `car_profile: dtm_class1_turbo` (uncalibrated) |

## Tracks

| Round | Venue | Track id | Source |
|---|---|---|---|
| 1 | Spa-Francorchamps | `spa` | F1 base (`bases/f1-v8`), `speed_mult` 1.09 |
| 2 | Lausitzring (Sprint) | `lausitzring` | era 4 |
| 3 | Lausitzring (Grand Prix) | `lausitzring_gp` | traced in `bases/dtm-era4` (inherited, shared with 2018) |
| 4 | TT Circuit Assen | `assen` | traced in `bases/dtm-era5`: 4,500 m (−1.2%) |
| 5 | Nürburgring (Grand Prix) | `nuerburgring` | F1 base, `speed_mult` 1.09 |
| 6 | Nürburgring (Sprint) | `nuerburgring13` | era 4 |
| 7, 8 | Circuit Zolder | `zolder20` | traced in `bases/dtm-era5`: 3,953 m (−1.4%) |
| 9 | Hockenheimring | `hockenheim13` | era 4 |

`speed_mult` 1.09 is the ratio of the average target speeds of era 4's
Hockenheim and the F1 base's Hockenheim (same layout): a first guess until
simulated.

Assen and Zolder are traced from OpenStreetMap into the era base
(`bases/dtm-era5/track_specs/`, `tools/osm_track.py`), so 2019 gets them
too. Their `speed_scale` is 1.0, not yet calibrated.

- **Assen:** the full 4.555 km TT circuit, clockwise, the layout the DTM
  raced in 2019 and 2020. Raceway loop over the TT Circuit ways, without
  the TT Junior Track. OSM names no pit lane, so the start line is placed by
  hand on the pit straight between the GT chicane and the Haarbocht.
- **Zolder:** today's 4.011 km layout, a raceway loop over OSM relation
  6006460 (Circuit Zolder), start on the pit straight. It is `zolder20`, not
  `zolder`: `dtm-1991`'s Zolder is the older layout with Group A speeds.

## Simplifications

Game gaps are listed in the
[wish list](../../docs/DEVELOPER_WISHLIST.md):
- **A1, A4:** two races per weekend become two game weeks, so the
  calendar stretches by up to two weeks per back-to-back weekend.
- **A3:** races were 55 minutes plus a lap; the game runs a fixed lap
  count, taken from the real race.
- **B5:** the one mandatory pit stop can't be required.
- **B6, B13:** DRS rules per session aren't data, and the game has no
  fixed push-to-pass boost; it is approximated with spec ERS.
- **B8:** qualifying points were 3-2-1; the game gives pole one point.
- **B4, B12:** no separate teams' rule (best two cars per race) and no
  tyre or stop rules as data.
- **C1:** three cars per team is the game's limit.
- **C4:** WRT and ART ran customer cars; they are customer engine deals here.
- Also D1, D3, E1, E2, as for 2012 and 2013.

## Rebuild

```bash
python tools/season_from_research.py seasons/dtm-2020
```

```bash
python tools/build_pack.py seasons/dtm-2020
```
