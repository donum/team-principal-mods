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
| Second source | Everything comes from one Wikipedia page tagged "sources needed". Check entries, results and points against a period source (Autosport, touringcarracing.net). | P1 |
| Points scale | 20-15-12-10-8-6-4-3-2-1 matches half the drivers exactly but not the top (Rouse -21, Gravett -17). Find the real scale, drop scores and fastest-lap points. | P1 |
| Weights and tyres | Super Touring minimum weight in 1991, and which tyre each team ran. The pack uses 950 kg and Dunlop for all. | P1 |
| Lap counts and lengths | Race laps per meeting and the 1991 lengths of Silverstone National and GP, Snetterton, Thruxton, Donington National and Oulton Park. | P2 |
| Birth dates | Needed for driver ages (all 30 for now). | P2 |
| Engines | Real engine names and outputs (`entries.csv` has generic "2.0 L4"). | P2 |
| Results files | Per-race qualifying and race CSVs in `research/results/`, as in dtm-1991, so `tools/simulate.py` can compare poles. `research/race_results.csv` has finishing positions only. | P2 |

## 2. Tracks

| Item | What | Prio |
|---|---|---|
| Trace six circuits | Silverstone (National and GP, 1991 layouts), Snetterton, Thruxton, Donington Park (GP and National), Oulton Park (International) with `tools/osm_track.py`. Each is a placeholder on a DTM track now. A British base (or the BTCC base below) is the place for them. | P1 |
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
