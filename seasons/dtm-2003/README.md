# DTM 2003: Season Pack

Status: **v0.1, generated and builds, not yet tested in-game.** Lap times
and tyre wear are first guesses, not simulated. The data was generated with
`tools/season_from_research.py` from `research/`, configured in `gen.json`.
For the sourced facts behind it (calendar, entry list, standings, rules,
sources and unverified points), see [research/season.md](research/season.md).
What is still open is in the [backlog](../../docs/plans/DTM2003_BACKLOG.md).

**Era base and mother template:** 2003 builds on
[`bases/dtm-era3`](../../bases/dtm-era3) (`"base": "dtm-era3"`), which holds
what every 2000–2011 season shares: rules, the Dunlop tyre, car profiles,
engines, chassis names, the maker logos and the track sharing. 2003 is the
first era-3 season built, so the base was set up on it, and its cars are the
ones the era's engine sounds will be recorded from (`base.json` `"audio"`,
`recording_years: [2003]`). 2006 and 2010 inherit them. No sounds are
collected yet: the pack uses the game's vanilla sounds.

## How it's built

- **Teams and drivers:** 10 teams, 21 seats and 22 drivers from
  `research/entries.csv`, with the real car numbers.
  - The HWA cars #3 (Vodafone) and #4 (Express-Service) are one team,
    "Vodafone AMG-Mercedes"; #9 and #10 are "AMG-Mercedes".
  - Abt Sportsline's three entries stay three teams: Hasseröder,
    PlayStation 2 Red Bull and the S line Audi Junior Team.
  - Persson's three cars (Original-Teile #11, #12 and ARTA #20) are one
    three-car team.
  - Rosberg: Paffett (#24 from round 3) has the seat, Huisman is a reserve.
- **Ratings:** from each team's average points per car, spread over
  53–57.5 (Mercedes won 9 of 10 races). Driver skill 11–18. Estimates, not
  history.
- **Year-old cars:** the four teams on 2002 cars (Junior Team, Euroteam,
  Persson, Rosberg) get `potential: 3` instead of 6, so they can't develop
  as far (wishlist C4, D7).
- **Previous position:** the 2002 teams' standing
  (`seasons/dtm-2002/research/standings_other.csv`).
- **Colours:** first estimates from the main sponsors, not checked against
  photos yet.
- **Calendar:** 10 rounds, one race each, real race laps.

## Rules

| Rule | 2003 | Pack |
|---|---|---|
| Points | 10-8-6-5-4-3-2-1 | `points_system: dtm_top8` (base) |
| Qualifying | 20 min session, then Superpole (top 10, one lap each) | `qualifying_format: session_60` (season patch) |
| Pit stops | 2 mandatory, with tyres | tyre wear makes two stops normal (`tyre_wear_mult`, wear 0.03) |
| Refuelling | allowed, 70 L tank | `formula_refueling: allowed`, `formula_fuel_tank: 60kg` |
| Tyres | Dunlop control tyre, no warmers | one dry compound (`data/tyremodel.json` in the base) |
| Weight | 1,080 kg incl. driver | `car_mass_kg` 935 + 145 kg engine |
| Engines | 4.0 V8, 2x28 mm restrictors, ~460–470 hp, 3 per team | `power_rating` 56–57 |
| DRS, ERS, driver aids | none | disabled, `full_prohibition` |

## Tracks

| Rd | Venue | Track id | Source |
|---|---|---|---|
| 1, 10 | Hockenheim GP | `hockenheim13` | era 4 trace (same layout since 2002) |
| 2 | Adria | `adria` | traced in the era base: 2,590 m against 2,702 m |
| 3, 7 | Nürburgring short | `nuerburgring13` | era 4 trace |
| 4 | EuroSpeedway Lausitz (with oval turn 1) | `lausitzring03` | traced in the era base along OSM's long course: 4,550 m against 4,575 m (layout of turn 1 to check) |
| 5 | Norisring | `norisring` | 1991 trace, `speed_mult` 1.27 |
| 6 | Donington Park | `donington` | traced in the era base (GP circuit): 3,963 m against 4,023 m |
| 8 | A1-Ring | `redbullring` | era 4 trace, renamed |
| 9 | Zandvoort | `zandvoort` | era 4 trace |

`tyre_wear_mult` per track is the 2012 pack's value scaled by 2012 laps /
2003 laps, so a tyre stint keeps the same share of the race.

## Simplifications

Game gaps are listed in the
[wish list](../../docs/DEVELOPER_WISHLIST.md):
- **A5, A6:** no Superpole (one lap each, reverse order); one open session
  sets the grid.
- **B5:** two mandatory stops can't be required; tyre wear decides.
- **B4:** the new manufacturers' championship isn't shown.
- **B7:** one spec dry tyre is a copy of the hard; no tyre-warmer ban.
- **C2:** Huisman's two rounds before Paffett are not modelled (reserve).
- **C4, D7:** year-old cars are a lower rating and less headroom, not a
  real older car.
- Also D1 (part names), D3 (lap-time controls), E1, E2, E8 (era-3 engine
  sounds).

## Gaps

- Tracks: Adria, Donington and the 2003 Lausitz layout are traced but not calibrated (`speed_scale` 1.0); the Lausitz turn 1 layout is not confirmed.
- No car images, team logos or portraits yet (build warnings).
- Sponsors not set (`sponsors` in `gen.json`).
- Lap times and tyre wear not simulated (`tools/simulate.py dtm-2003`).

## Rebuild

```bash
python tools/season_from_research.py seasons/dtm-2003
```

```bash
python tools/build_pack.py seasons/dtm-2003
```
