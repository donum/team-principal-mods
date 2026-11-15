# Backlog: BTCC 1991 pack

Everything still open for the first BTCC pack, as of 13 November 2026. Game
limits are in [DEVELOPER_WISHLIST.md](../DEVELOPER_WISHLIST.md), not here.
The pack uses the DTM Group A season (`"template": "dtm-1991"`) for its data
layout only; rules, engines and profiles are its own.

Priority: **P1** = changes how the game plays, **P2** = more of the real
1991 world, **P3** = presentation.

## 1. Research

| Item | What | Prio |
|---|---|---|
| Second source | Done 2026-11-15: calendar, every result, every total, points, weights, tyres, laps and lengths checked against Autosport (1990sbtcc.com), touringcars.net and touringcarracing.net (research/season.md). | done |
| Birth dates | 24 of 31 regulars found (racingsportscars.com). Missing: Gravett, Baird, Forrest, Leech, Llewellyn, Lindgren, Andersson. | P2 |
| Engines | Outputs for Toyota, Vauxhall and Ford (BMW about 270 hp and Nissan 265 hp are known). | P2 |
| Results files | Per-race qualifying and race CSVs in `research/results/`, as in dtm-1991, so `tools/simulate.py` can compare poles. `research/race_results.csv` has finishing positions only. The qualifying tables per round are on https://1990sbtcc.com/race-archive/. | P2 |

## 2. Tracks

| Item | What | Prio |
|---|---|---|
| Trace six circuits | Done 2026-11-15 from the race-tracks repo's 1991 layouts (`tools/race_tracks.py`). Silverstone GP 1991, Snetterton 1990 and Oulton Park 1975 are traced lines marked approximate there. Calibrate `speed_scale` against the 1991 qualifying times. A British base is the place for them once more BTCC years follow. | P1 |
| Brands Hatch Indy | Shared from `bases/dtm-era4`, calibrated for 2013 DTM cars. Needs a `speed_mult` for 1991 Super Touring cars. | P1 |

## 3. Calibration

- **Lap times** · P1: car profile `super_touring_1991` multipliers and the
  engine power ratings are first guesses. Run `tools/simulate.py btcc-1991`
  once the tracks have real lap times.
- **Make balance** · P1: in 1991 BMW won most races, Vauxhall and Toyota won
  several, Ford, Nissan and Mitsubishi did not win. Check the simulated
  points per make.

## 4. Structure

- **BTCC base** · P2: if more Super Touring years follow (1992 to 2000), move
  rules, engines, profiles and the British tracks into `bases/btcc-st` with
  1991 as the mother season, as for the DTM eras.

## 5. Art

- Car images, team logos, portraits, track art · P3.
- Team colours are first guesses; check against photos · P3.
