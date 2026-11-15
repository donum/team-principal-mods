# DTM 2013 sound status

What the engine audio overlay (`dtm-era4`, shared by every season on
`bases/dtm-era4`) changes in the installed `dtm2013` pack,
compared with the vanilla audio it copies from `default26`. Checked against
the installed pack on 2026-11-04, after the real starts and track bed went
in, and on 2026-11-07 after the pit sets. The audio itself is never in git; since 2026-11-12 it is baked into `dist/` and ships with the pack.

## Replaced

These vanilla clips no longer play. The vanilla files stay on disk, but
nothing points to them any more.

| Slot | Vanilla | Now | Made from |
|---|---|---|---|
| Pass-by, Audi | random bank (`engine_passby_01`–`05`) | `dtm13_audi` + `_lr` | Rockenfeller onboard, Hockenheim, simulated pass-by at 220 km/h |
| Pass-by, BMW | random bank | `dtm13_bmw` + `_lr` | Spengler onboard, Nürburgring |
| Pass-by, Mercedes | random bank | `dtm13_mercedes` + `_lr` | Juncadella onboard, Norisring |
| `grid_idle_01`, `grid_idle_02` | stock grid loops | real grid revving, 14 s loop: Hockenheim finale, grid and start (both slots) | fan recording, `starts.py` |
| `grid_launch_01`, `grid_launch_02` | stock launches | the real launch that follows, 14.5 s: 1.6 s of grid revving (the game starts the clip on the 3rd light), the getaway on lights out, the field swelling past (5 s of steady roar spliced out so the close pass lands 6.6 s in), then to the end of the 2013 recording with a 4 s fade (the 2017 tail went out on 2026-11-07: 2012–2013 cars only) | same |
| `cars_on_track` | stock 393 s bed | 393 s loop of real trackside 2013 recordings (Hockenheim sound check, Nürburgring, Norisring roll-out) | `ambience.py`, 11 shots of fan videos |
| `crowd` | stock 35 s murmur | 18 s loop of a real grandstand before the 2015 Nürburgring start | `ambience.py` (`CROWD`), picked from six candidates |
| `pit_exit_01`–`10` | 4 stock exits | 10 real 2013 cars pulling away down a pit lane (3 Audi, 7 Mercedes; June 2013, probably Lausitzring), 13 s, pull-away 5 s in; picked by frames and level, **not yet confirmed by ear** | fan recordings, `pits.py` |
| `pit_wheelguns_01`–`10` | 4 stock bursts | 10 real 2013 wheelgun bursts: 7 from the Brands Hatch pit-stop practice (Audi and BMW crews), 3 from a Mercedes race stop at the Lausitzring (2.1–3.6 s) | same |

The three makes are tagged in `engines.json` (`passby_audio`), so every
finish-line pass-by in practice, qualifying, testing and races is ours.
The pass-bys are still *simulated* (an onboard recording moved past a
virtual listener); everything else listed here is real recordings.
Simulated starts (`start_synth.py`) are off by default.

## Added

| Slot | What | Heard? |
|---|---|---|
| `dtm13_tv_01`–`03` + `_lr` | commentary-free pass-bys cut from the TV broadcasts | **no:** they sit in the random bank, which only untagged suppliers use, and all three suppliers are tagged |

## Still vanilla

| Folder | Slot | Count | Notes |
|---|---|---|---|
| `race/` | `pit_fireup_01`–`06` | 4 | no clean fire-up in any recording yet; the stock ones are re-levelled for our exits (`package.py`), and sets 05–06 reuse 01–02 |
| `race/` | `start_light.wav`, `lights_out.wav` | 2 | |
| `ambience/` | `base_01`, `base_02` | 2 | base beds |
| `ambience/` | `pa`, `helicopter`, `pit_blowers`, `rain` | 4 | |
| `session/` | `engine_passby_01`–`05` + `_lr` | 10 | still in the random bank, but never picked (see Added) |
| `music/` | 6 menu tracks | 6 | the shared CC0 tracks |
| `ui/` | clicks, confirm, error… | 12 | always taken from the shared folder; a pack can't change them |

## Toward a consistent qualifying and race

Starts, the track bed and the crowd are real recordings now. Still open:

1. **Real pass-bys:** the spectator videos are full of real pass-bys, but
   do not say which make passes, so they can't be tagged per make.
2. **Pit lane:** the exits are six 2013 pit-lane departures, still to be
   confirmed by ear (no BMW among them). Wheelguns are real; fire-ups are still
   stock. The 18 pit-lane videos downloaded on 2026-11-07 had none: garage
   walks with no engine, cars on track, and one paddock clip that starts at
   an edit (in the Sound candidates tab to judge by ear). A video of a car
   being started in the garage or the pit box is what's missing.
3. **TV pass-bys:** either untag the suppliers, so the make clips and the TV
   clips share one bank, or drop the TV clips.

All of this is one set per pack, never per track (wishlist E9).

The mod browser (`tools/mod_browser.py`, rebuilt on every install) shows
the same picture live, with every clip playable.

# DTM 2018 sound status

2018 has its own sound set `dtm-2018` (`seasons/dtm-2018/season.json`
`"audio"`, 2017-2018 cars only) on top of the era-4 set. Checked on
2026-11-15.

## Do the 2017-2018 cars sound different?

Measured over the fan recordings (2012-13: 23, 2014-16: 12, 2017-18: 12),
in the loud frames where an engine is clearly heard:

| | 2012-13 | 2014-16 | 2017-18 |
|---|---|---|---|
| Engine speed, median | 6,515 rpm | 6,758 | 6,436 |
| Top revs (98th percentile) | 8,528 | 8,580 | 8,528 |
| Pops and crackles per minute, median | 0.3 | 0.8 | 2.6 |
| Treble vs midrange (2-8 kHz vs 0.2-2 kHz) | -10.2 dB | -11.9 | -8.6 |

Same revs; the 2017-2018 recordings pop on the overrun far more (the
backfires the 2018 videos are named for) and sound brighter. Phone mics
differ, so this was checked by ear: A/B clips in
`pilot/compare_2013_2018/` (the user chose to replace the 2018 sounds).

## Replaced

| Slot | Now | Made from |
|---|---|---|
| `cars_on_track` | `dtm18_cars_on_track`, 240 s loop | 10 hand-picked shots of cars on track (`ambience.BED_PICKS`): Misano 2018 night race (`maJ-qIGkz_o`), Misano 2018 by day (`1_f68-hUy8w`), a 2017 compilation (`plmbOpRMwHs`). Grids, practice starts and pit-exit shots left out by their frames. Shorter than stock: only ~290 s of 2017-2018 track sound passes. |
| `grid_launch_01`, `_02` | `dtm18_grid_launch_01`, 16 s | Norisring 2018 from the Schoeller stand (`bE-cwxQ42JA`), picked by ear: the field arrives at the hairpin and powers out (26-42 s). The track announcer before it (14-26 s) is cut away and kept as a PA reference (`pilot/pa_candidates/`). |
| `pit_exit_01`-`10` | 5 clips, cycled | Misano 2018 pit-exit practice starts (`1_f68-hUy8w`), picked by ear: a car standing at the line, then pulling away. Each ends at the camera cut or where the car has gone (13-20 s); 0.8-1.5 s fade-ins. |
| `pit_fireup_01`-`10` | stock, levelled for the 2018 exits | as in 2013 |
| Pass-by, Audi / BMW / Mercedes | `dtm18_audi`, `dtm18_bmw`, `dtm18_mercedes` + `_lr` | simulated pass-bys at 220 km/h from 2018 race onboards, picked by ear on 2026-11-15 from the sweep in `pilot/passby_candidates_2018/` (445 candidates, 79 onboards): René Rast, Spielberg race 1 (2637.7 s); Philipp Eng, Spielberg race 1 (1486.4 s); Pascal Wehrlein, Misano race 2 (1538.2 s). Set in `package.PASSBY_PICKS`. |

Picked by ear 2026-11-15 from `pilot/start_candidates_2018/` and
`pilot/pit_candidates_2018/`. Set aside: Hockenheim 2017 start (good but
broken), Hockenheim 2018 start and grid (not nice to listen to). The
Lausitzring 2018 downshifts and starts (`JDtk4MRd1d0`) are the user's
favourite and wait for per-track sounds (wishlist E9).

## Still the era's 2013 sounds

- **Grid revving** (`grid_idle`): the Norisring recording's grid is too far
  away to loop.
- **Wheelguns:** none recorded for 2017-2018.
- **Crowd:** no engines in it, so the year does not matter.

Heard in game and approved by the user (2026-11-15).
