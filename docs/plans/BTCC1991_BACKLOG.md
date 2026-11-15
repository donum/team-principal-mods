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

## 2. Tracks

| Item | What | Prio |
|---|---|---|
| Trace six circuits | Done 2026-11-15 from the race-tracks repo's 1991 layouts (`tools/race_tracks.py`). Silverstone GP 1991, Snetterton 1990 and Oulton Park 1975 are traced lines marked approximate there. Calibrate `speed_scale` against the 1991 qualifying times. A British base is the place for them once more BTCC years follow. | P1 |
| Brands Hatch Indy | Shared from `bases/dtm-era4`, calibrated for 2013 DTM cars. Needs a `speed_mult` for 1991 Super Touring cars. | P1 |

## 3. Calibration

Checked before every tuning run: track layouts and lengths, and pole,
fastest race lap and average race lap against 1991 (see memory rule).

- **Tracks** · all eight from the race-tracks repo's 1991 layouts. Lengths
  within 1% of the 1991 figures, except Silverstone GP 1991 (traced 4.1%
  short) and Oulton Park 1975 (3.7% short), both marked approximate there:
  their speed factors make up for it, but the shapes want a second look in
  race-tracks · P2.
- **Lap times** · done 2026-11-15: `speed_mult` per track from three seasons
  of pole, fastest race lap and average race lap. Now (three seasons,
  build/sim/btcc-1991/20261115-130705): pole -0.4% to +1.6%, fastest lap
  -1.5% to +2.2%, race lap +0.5% to +3.7% per track.
- **Make balance** · done 2026-11-15 (three passes, gen.json). Three seasons
  against 1991: 5, 5 and 3 different winners (real 6); wins per season
  Cleland 5.3 (4), Rouse 3.3 (3), Soper 2.7 (3), Hoy 2.3 (3), Harvey 0.7 (1);
  points Securicor 21.9% (22.1%), Labatt's 10.9% (10.2%), Vauxhall 23.0%
  (20.5%), Toyota 20.2% (14.3%), Mobil 20.0% (14.4%; Soper races every
  round in the game, six fewer in 1991). Still open · P2: the independents
  score 1-2% against 3-4% (Middlehurst, Gravett, Sytner).
- **Report matching** · P3: the result files carry the printed entrant
  names, so `tools/simulate.py` files about 5% of the real points under "?".

## 4. Structure

- **BTCC base** · P2: if more Super Touring years follow (1992 to 2000), move
  rules, engines, profiles and the British tracks into `bases/btcc-st` with
  1991 as the mother season, as for the DTM eras.

## 5. Art

- Car images, team logos, portraits, track art · P3.
- Team colours are first guesses; check against photos · P3.
