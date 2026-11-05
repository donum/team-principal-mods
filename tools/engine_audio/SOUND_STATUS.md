# DTM 2013 sound status

What the private audio overlay changes in the installed `dtm2013` pack,
compared with the vanilla audio it copies from `default26`. Checked against
the installed pack on 2026-11-04, after the real starts and track bed went
in. The audio itself is private and never in git or `dist/`.

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
| `race/` | `pit_fireup_01`–`04` | 4 | the onboards have no fire-ups |
| `race/` | `pit_exit_01`–`04` | 4 | no onboard pit exits found yet |
| `race/` | `pit_wheelguns_01`–`04` | 4 | the broadcast pit-stop finder is unverified |
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
2. **Pit lane:** fire-ups, exits and wheelguns. The 2013 Spielberg and
   2018 Misano fan videos show pit-lane starts and exits.
3. **TV pass-bys:** either untag the suppliers, so the make clips and the TV
   clips share one bank, or drop the TV clips.

All of this is one set per pack, never per track (wishlist E9).

The mod browser (`tools/mod_browser.py`, rebuilt on every install) shows
the same picture live, with every clip playable.
