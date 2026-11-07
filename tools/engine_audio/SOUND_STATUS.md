# DTM 2013 sound status

What the private audio overlay changes in the installed `dtm2013` pack,
compared with the vanilla audio it copies from `default26`. Checked against
the installed pack on 2026-11-04, after the real starts and track bed went
in, and on 2026-11-07 after the pit sets. The audio itself is private and never in git or `dist/`.

## Replaced

These vanilla clips no longer play. The vanilla files stay on disk, but
nothing points to them any more.

| Slot | Vanilla | Now | Made from |
|---|---|---|---|
| Pass-by, Audi | random bank (`engine_passby_01`–`05`) | `dtm13_audi` + `_lr` | Rockenfeller onboard, Hockenheim, simulated pass-by at 220 km/h |
| Pass-by, BMW | random bank | `dtm13_bmw` + `_lr` | Spengler onboard, Nürburgring |
| Pass-by, Mercedes | random bank | `dtm13_mercedes` + `_lr` | Juncadella onboard, Norisring |
| `grid_idle_01`, `grid_idle_02` | stock grid loops | real grid revving, 14 s loop: Hockenheim finale, grid and start (both slots) | fan recording, `starts.py` |
| `grid_launch_01`, `grid_launch_02` | stock launches | the real launch that follows, 14.5 s: 1.6 s of grid revving (the game starts the clip on the 3rd light), the getaway on lights out, the field swelling past (5 s of steady roar spliced out so the close pass lands 6.6 s in), then the field leaving towards turn 1 (from the 2017 Hockenheim start) and a 4 s fade | same |
| `cars_on_track` | stock 393 s bed | 393 s loop of real trackside DTM V8 recordings (Hockenheim 2013–2016) | `ambience.py`, 11 shots of fan videos |
| `crowd` | stock 35 s murmur | 18 s loop of a real grandstand before the 2015 Nürburgring start | `ambience.py` (`CROWD`), picked from six candidates |
| `pit_exit_01`–`06` | 4 stock exits | 6 real 2013 cars on the Oschersleben pit-exit lane: on the limiter, the pass, away (10.7–13 s, pass 4.4–5.6 s in) | fan recordings, `pits.py` |
| `pit_wheelguns_01`–`06` | 4 stock bursts | 6 real wheelgun bursts from the 2013 Brands Hatch pit-stop practice (Audi and BMW crews, 2.1–3.6 s) | same |

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
2. **Pit lane:** exits and wheelguns are real now; fire-ups are still
   stock. The 18 pit-lane videos downloaded on 2026-11-07 had none: garage
   walks with no engine, cars on track, and one paddock clip that starts at
   an edit (in the Sound candidates tab to judge by ear). A video of a car
   being started in the garage or the pit box is what's missing.
3. **TV pass-bys:** either untag the suppliers, so the make clips and the TV
   clips share one bank, or drop the TV clips.

All of this is one set per pack, never per track (wishlist E9).

The mod browser (`tools/mod_browser.py`, rebuilt on every install) shows
the same picture live, with every clip playable.
