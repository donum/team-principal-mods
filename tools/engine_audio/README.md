# Engine-audio pipeline (private)

Builds a DTM 2013 engine-sound library from downloaded onboard and TV videos,
and packages it as one sound overlay for the whole era base
[`bases/dtm-era4`](../../bases/dtm-era4) (DTM 2012–2018). Every installed
season on that base (`dtm2013` today; 2012, 2014... later) gets the same
sounds.

**Where the settings live:** `bases/dtm-era4/base.json` `"audio"`:
- `overlay`: the overlay id, `private/engine_audio/pack/<id>/`;
- `recording_years`: which cars may be heard (`common.ERA`, see "Era");
- `research_season`: the entry list that tells who drove which make in the
  videos (`catalog.py`);
- `key_prefix`: the start of our clip keys (`dtm13_audi`, `dtm13_grid_idle_01`...);
- `slots` (optional): the slot groups the set makes (`passby`, `tv`, `start`,
  `pit`, `cars`, `crowd`); all when left out;
- `inherit` (optional): `false` starts a fresh stack (a new car generation).

**Season sets.** A season can have its own set in `season.json` `"audio"`
(own `overlay` id and `key_prefix`), merged over its era's settings. It sits
on top of the era's set and makes only its `slots`; the era's set fills the
rest (`layers.audio_sets`, `overlay.combine`). Run the stages with
`ENGINE_AUDIO_BASE=<season id>`: it shares the era's library (same
`ENGINE_AUDIO_DATA`), and its loops and previews go to
`library/sets/<overlay id>/` (`common.SET_LIBRARY_DIR`; the era-4 set keeps
`library/` itself). See `bases/README.md`, "Sounds".

The pass-by tags are set per make when the overlay is applied
(`overlay.json` `"passby_by_make"`): every engine supplier whose name starts
with Audi, BMW or Mercedes gets that make's clip, whatever the season.

**Another generation** (say Group A, era 1) gets its own sound library: give
its base an `"audio"` section, then run the stages with
`ENGINE_AUDIO_BASE=<base id>` and its own `ENGINE_AUDIO_DATA` folder.

**Release.** The source audio belongs to ITR / DTM and the fan videos'
owners. We have the OK to ship the overlay (2026-11-12). Audio, clips and
caches still live in `private/engine_audio/` (gitignored); only code and the
metadata overrides are committed.

- `"in_pack": true` in the base's `"audio"` section (set for `dtm-era4`):
  `build_pack.py` bakes the overlay into `dist/` (`overlay.bake`: no backup,
  no marker), so it ships with the Workshop pack.
- Without it, the overlay goes onto the *installed* pack only, with an
  `assets/audio/PRIVATE_AUDIO_DO_NOT_UPLOAD.txt` marker while it is on.

Needs ffmpeg/ffprobe on PATH, numpy and scipy (`python -m pip install --user scipy`).
The source folder defaults to `C:\Users\dan\Videos\yt\DTM`; set
`"engine_audio_source"` in `local.json` to change it.

## Stages

Every stage is incremental and safe to re-run as downloads land:

```bash
python tools/engine_audio/catalog.py
```
```bash
python tools/engine_audio/extract.py
```
```bash
python tools/engine_audio/segment.py
```
```bash
python tools/engine_audio/library.py
```
```bash
python tools/engine_audio/package.py --install
```

| Stage | Reads | Writes |
|---|---|---|
| `catalog.py` | each queue folder's `done.json` / `todo.json` (read-only), the base's `research_season` (`seasons/dtm-2013/research`) | `library.sqlite` table `videos`, `manifest.csv`, coverage matrix on stdout |
| `extract.py` | catalog rows with status `done` | `audio/<make>/<track>/<session>/<driver>/<id>.mka` (stream copy, no re-encode) |
| `segment.py` | extracted audio | `features/<id>.npz`, tables `analysis` and `segments` |
| `library.py` | segments | `library/index.html` (playable), `library/coverage.md`, ranked WAV clips |
| `events.py` | broadcast features (race and qualifying re-lives) | table `events`: race-start, pit-stop, pass-by and track-bed candidates (the pit-stop finder mistakes speech for wheelguns: its top hits were all commentary) |
| `pits.py` | fan recordings of the pit lane and pit-stop practice (hand-listed) | pit sets: exit, wheelguns and (when found) fire-up, paired by number (used by `package.py`; previews `library/pits/pit_NN_*.wav`). `pits.py --scan <video id>...` cuts wheelgun bursts and fire-up onsets into `pilot/pit_candidates/` for listening |
| `starts.py` | fan recordings of race starts (hand-listed) | real grid idle loops and launches (used by `package.py`; its previews `library/starts/start_NN_*.wav` are rewritten by `package.py --install`) |
| `start_preview.py` | the installed pack | each start mixed with the game's own timing and levels (`library/starts/ingame_start_NN.wav`) |
| `ambience.py` | spectator montages | 393 s `cars_on_track` loop of real trackside shots, cut at camera cuts |
| `track_ambience.py` | spectator videos per venue, announcer index | `--candidates`: per-venue listening sets in `pilot/track_ambience/<venue>/` (track bed shots, crowd stretches, PA) with `candidates.md`; without: the `TRACK_PICKS` (and automatic beds where a venue has 120 s of clean shots) in `library/ambience/tracks/`. For the next game version's `tracks.<id>` block (wishlist E9) |
| `start_synth.py` | clean onboard windows | simulated 22-car grid idle and launch (only with `package.py --synth-starts`) |
| `announcer.py` | fan recordings (all years) and archive features named in `EXTRA` | `pilot/track_announcer/`: every speech stretch with its text (faster-whisper `small`), language, voice level against the 2 s around and bass share, in `index.csv`; `kind` and `note` from the hand labels in `announcer_labels.csv` (pa, feature, video, fan, crew, unsure). A reference for building track announcers per track; the mod browser lists it on every season's page |
| `archive_candidates.py --season <id>` | the season's audio `"sources"` (globs under `C:\Users\dan\Videos\yt`, kind tv / review / fan) | for a generation without an onboard library (BTCC 1991): speech-free pass-bys, getaways, bed windows, fire-ups and quiet stretches (Silero VAD plus level, pan and spectrum), best first, in `pilot/<set>/<kind>/` with `candidates.json` and a frame per pass-by. `--tv` cuts the strongest TV pass-bys and transcript-found starts whatever the speech and takes the commentary out (Mel-RoFormer, `models/`) into `passby_tv/` and `start_tv/`. Hand labels (make, drop) go in `archive_labels.csv`. The season's page in the mod browser lists only these (`"candidate_dirs"`) |
| `package.py` | segments, base pack audio levels | `pack/dtm-era4/` (files + `overlay.json`); `--install` applies it to every installed season of the base |
| `overlay.py` | `pack/dtm-era4/` | `apply`, `remove`, `status` on an installed pack (`--pack dtm2013`) |

`build_pack.py --install` re-applies the overlay after reinstalling the pack.
`--no-private-audio` installs without it.

## Next game version (announced 2026-11-16)

Two sound features are built already but only go into a pack when
`local.json` lists them in `"game_audio_features"` (`overlay.py`):

- `"passby_pools"`: `package.py` makes `PASSBY_POOL` (4) pass-bys per make,
  each from another driver's onboard (`dtm13_audi`, `dtm13_audi_02`...).
  With the feature, `passby_audio` gets the whole list; without it, the
  first key, as before.
- `"track_ambience"`: the per-venue layers of `track_ambience.py` go into
  `tracks.<id>` in `session_layers.json` (crowd, pa and cars). Without the
  feature their files are not copied either.

Turn them on once the modding guide of the new version confirms the keys.

## Era

Only cars of the 2013 generation are heard: the 2012–2013 Audi RS 5, BMW M3
and Mercedes C-Coupé (`common.ERA`, `common.era_reason`). A fan video's
year is the year in its title, or else its upload year (`UPLOAD_YEARS`);
`ERA_EXCLUDE` drops in-era videos that mix in other cars. The track bed
(`ambience.py`) and the mod browser's candidate lists follow it. The
onboard, TV and archive playlists are the 2013 season itself.

## Catalog

- **Statuses:**
  - `done`: listed in `done.json`.
  - `queued`: still in `todo.json`.
  - `partial`: a file is on disk but not listed yet (download in progress).
  - `legacy`: an old yt-dlp download recorded in the root `done.txt`.
  - Only `done` is processed; `extract.py --include-legacy` adds legacy files.
- **Types:**
  - `onboard`, `onboard_bestof`, `taxi`
  - `trackview`: the German archive's manufacturer laps
  - `broadcast`: Re-Live, *Rennen*, *Qualifikation*
  - `highlights`, `feature`, `animation`
- **Drivers and cars** come from the 2013 entry list. Plain "Hockenheim" is read as the opener; both playlists run newest-first.
- **Hand fixes** go in `overrides.csv`, keyed by video id. Fill only the columns to change.

## Analysis (`segment.py`)

- **RPM:** tracked from engine order 2 (f = RPM/30). A crossplane V8 fires each bank unevenly, so real onboards show a strong order-2 series with the firing order (RPM/15) as every second line, while order 1 is weak. Each 50 ms frame scores candidates by the mean peak height of their harmonics below 4 kHz, and a Viterbi pass keeps the track continuous. Octave slips are then repaired (a ×2 or ×½ jump within 150 ms is undone; each stretch is kept inside 2,500–10,000 RPM).

  Checked against spectrograms of real onboards: the track follows the order-2 line through upshifts, braking and downshift blips. Across all 45 onboards the median is 6,600–7,100 RPM and the 90th percentile about 7,400.
- **Throttle state** comes from RPM direction, not loudness: onboard audio is compressed so hard that lifting off changes the level by under 1 dB. Smooth rise is full throttle, smooth fall is overrun, and sudden 7–12 % jumps are gear changes (checked just before and after, since the ignition cut itself has no clean pitch).
- **Flags:**
  - `commentary`: syllable gaps and 3–8 Hz rhythm in the voice band;
  - `wind`: low-frequency energy without harmonics;
  - `other_cars`: a second harmonic series unrelated to the tracked one.
- **Labels:**
  - onboards: idle, full_throttle, steady_high, overrun, upshift, downshift, plus launch (race start) and pit_exit;
  - TV: passby, a loudness peak with a Doppler drop and a pan sweep.
- Bump `VERSION` in `segment.py` whenever the analysis changes, so cached results are redone.

## Game target (Team Principal)

From the game's `assets/audio/README_AUDIO.txt`:

- **Pass-bys** (`session/hotlap_flybys.json`):
  - one per make, keys `dtm13_audi` / `dtm13_bmw` / `dtm13_mercedes` plus `_lr`;
  - tagged on the supplier through `engines.json` `passby_audio`;
  - made by simulating a pass-by at 220 km/h and 12 m (Doppler, distance, pan) from clean onboard full-throttle audio;
  - commentary-free TV pass-bys, if any, join the random bank as `dtm13_tv_NN`. With all three suppliers tagged, that bank is never used, so they are not heard today.
- **Grid and pit** (`race/race_engines.json`):
  - `grid_idle_NN` / `grid_launch_NN` pairs are cut from fan recordings of real starts by `starts.py` (simulated ones only with `--synth-starts`);
  - pit sets come from `pits.py` (see "Pit lane" below): `pit_exit_NN`, `pit_wheelguns_NN` and `pit_fireup_NN`, paired by number;
  - they replace the stock clips with the same key;
  - these banks are shared by all cars (wishlist E8).
- **Track bed** (`ambience/session_layers.json`): `cars.file` points to the `ambience.py` loop.
- **Levels** match the stock clips as the game plays them. For pit clips that includes the game's own boost (below).

## Pit lane (`pits.py`)

**How the game plays them** (read from its `ui/audio_manager.py` and `ui/pit_exit_audio.py`):
- A pit set is picked from a shuffled bag of the `pit_exit_NN` keys; the fire-up and wheelguns of the same NN go with it.
- *Practice and qualifying:* the fire-up is scaled by fire-up gain / exit gain and crossfaded into the exit over `pit_fireup_crossfade_s` (0.65 s), played as one "departure".
- *Race:* the wheelguns play when the stop starts; at release they fade out over 0.65 s as the exit fades in. No fire-up.
- *Level:* each clip, and the joined departure, is boosted by min(`pit_departure_gain` = 5, 0.95 full scale / its peak), then played at its gain. Gains are clamped to 1.0. The stock clips peak 15–35 dB under full scale, so the game plays them about 14 dB louder than the files.

**What `package.py` does with that:**
- Exits and wheelguns are written peak-normalised. Their gain is set so that the clip, after the game's boost, plays at the stock clips' median level.
- Fire-ups are written at the level they should be heard at, with gain 1.0. Our exits are already near full scale, so the joined departure is hardly boosted, and with the clamp the exit gain would otherwise leave the fire-up about 13 dB quieter than vanilla.
- Until a real fire-up is found, each set carries a stock fire-up, levelled the same way.
- Every stock set number points at one of ours, so the bag never draws a stock exit.

**Sources** (2026-11-07):
- *Exits:* six 2013 cars pulling away down a pit lane in "DTM Sound 1" (`EMSlNAM8zC0`, Don Blech, June 2013, probably Lausitzring), no commentary: ten sets, three Audis and seven Mercedes (no BMW leaves in it). Picked from 15 departures by frames and level, not yet confirmed by ear (`exit_unconfirmed`, shown in the mod browser); the pull-away lands 5 s in (stock: 4.4–5.8 s). The rest are in `pilot/pit_candidates/exit_EMSlNAM8zC0_*.wav`.
- *Oschersleben cuts (old exits):* by ear (2026-11-07) four were drive-bys, one a pit entry and one probably an exit. All six are in `FAN_CLIPS`, previews only (`library/fan_clips`): unknown-make drive-bys can't be tagged and the game has no pit-entry slot (wishlist E14).
- *Wheelguns:* spectators at the 2013 Brands Hatch pit-stop practice, Audi and BMW crews (`gpLEQ52Q4F4`, `Yy28JpRzFD0`, `1K5GsYD9vmI`, `H64vMO6NpuY`, `HF-w0SiCD-Y`), and a Mercedes race stop filmed close at the 2013 Lausitzring (`DPFz3gE17zQ`, which also opens with the car rolling in: a pit entry, kept as a preview). These are the strongest bursts of `--scan`, checked on the spectrogram and frames.
- *Fire-ups:* none found. The Lausitzring 2013 pit-lane clips are a garage walk with no engines running. The Norisring "roll-out" and the Hockenheim sound check are cars on track. The Norisring paddock clip of the Euronics AMG starts with the engine already running, apparently at an edit, so it is only a candidate.
- *Set aside:* the Spielberg 2013 pit-exit practice starts (`0sl-m42P15Q`) are faint and windy behind a fence. Misano 2018 is mostly distant generator hum.

Check in game: the pit-lane sound in practice (fire-up then exit) and at a race stop (wheelguns then exit).

`package.py --install` also rebuilds the mod browser (`tools/mod_browser.py`),
whose Sounds tab plays vanilla and our clips side by side and whose Sound
candidates tab lists the `pilot/` and `library/` folders here.

To target another game, add a builder next to `build()` in `package.py`. The
segment references in `library.sqlite` are game-independent.

## Simulated start (`start_synth.py`)

The broadcasts can't give a clean start: the commentators talk loudest exactly
there, and neither Demucs (`htdemucs`, `htdemucs_ft`, with shifts) nor the
RoFormer vocal models remove it without watery gaps. So the start is built
from the clean onboards:

- **Grid:** 22 cars in the 2013 make mix (8 Audi, 8 BMW, 6 Mercedes), each
  from a different onboard, on the staggered grid; the listener stands
  13–20 m away, beside the front half.
- **Grid revs:** each car's onboard audio replayed at a rate set from its
  tracked rpm. Drivers hold 5,000–6,500 rpm and jab the throttle about once
  a second, up to 7,000 rpm or onto the 8,500 rpm limiter.
- **Launch:** a rev flare as the clutch drops, the bog as it bites, then
  within a second the onboard's real acceleration with its upshifts. Full
  throttle at once with a bark: the level jumps about 11 dB in under 0.25 s.
- **Real pack:** from half a second after lights out, a real trackside
  recording of a pack arriving (`Oz5JnogDN_Q`, 2015 Hockenheim, 81.5 s on)
  plays 3 dB under the simulated field. It is skipped if not extracted.
- **Physics:** emission-time solving (travel time, Doppler), 1/r level,
  distance damping, an AB microphone pair, grandstand reflections.
- **Cleanup:** a comb mask on each car's known rpm removes the onboard
  wind and road noise; stereo narrowed to the stock clips' width.

Each of the four game pairs uses its own seed (grid order, listener spot).
Previews: `python tools/engine_audio/start_synth.py` writes
`private/engine_audio/pilot/synth_start/start_NN_idle_then_launch.wav`.

Simulated starts were set aside in favour of real recordings (see below);
the code stays for reference.

## Real starts and track bed (spectator recordings)

Fans filming from the grandstands (queue folder `spectator_recordings`,
catalog type `spectator`, no commentary) give what the broadcasts can't:

- **Starts (`starts.py`):** one start, picked by ear: the Hockenheim
  finale "Grid and Start" video (`fk9f2Qt5x20`), 15 s of clean grid
  revving and the field swelling past.
  **Shape and length** (14.5 s, tuned by ear against previews):
  - *Climax:* the close pass (11.6 s into the recording) must stay in;
    a plain 12 s fade lost it and sounded flat (the level rule then
    lifted an even roar). 5–10 s of steady roar are spliced out (`skip`,
    1 s equal-power crossfade, no level change), so the pass lands at
    6.6 s, about 4.6 s after the cars move.
  - *Moving away:* the stock launches are 10.9 s and fade out from the
    getaway; ours ended on the field still loud. Until 2026-11-07 it
    crossfaded at 8 s into the 2017 Hockenheim start (`IBuEsBSh9_I`,
    16–22.5 s), the field leaving towards turn 1. That tail is out (era
    rule), so the launch now runs to the end of the 2013 recording and
    fades there. An in-era recording of the field leaving is wanted. Phone recordings lose little level as cars leave (the
    gain control holds it up) but go dull, the spectral centroid falling
    from ~4 kHz on the pass to 1.3 kHz here.
  - *Fade:* the last 4 s fall a steady 30 dB (`fade_db`); the cosine
    fade held and then dropped, which sounded like a file fading out.
    A sliding low-pass on top was tried and left out: the recording is
    already dull there.
  - As played: about -20 dB after the getaway, -18 through the roar,
    -15 on the pass, -17 to -18 in the 2017 part, then the fade.
  Both stock slots (`grid_*_01`, `_02`) point at it, so the random pick
  never falls back to stock.
  **Why so few:** in most fan videos the crowd cheers and the phone mic
  overloads exactly as the field launches. Scored over the 8 s after go,
  the dropped Nürburgring 2014 start had 14.5 % of its energy above 5 kHz
  and a spectral flatness (150 Hz–4 kHz) of 0.20; the Hockenheim 2015 clip
  the user loved has 0.2 % and 0.06. In game the dropped starts sounded
  "broken": noise rather than cars. Hockenheim 2012, Zandvoort 2015 and
  Brands Hatch went with it. Other clean candidates (Hockenheim 2017 and
  2011, Norisring 2018 Schöller) are cut in `pilot/start_candidates/`.
  **Go** is set by hand where the 1–4 kHz roar steps up for good (54.6 s
  here); the phone's gain control smears the broadband level, which
  `refine_go` relies on.
  **Game timing** (read from the game's `ui/live_audio.py` and
  `ui/screens/race_screen.py`): five lights come on 0.5 s apart; on the
  3rd light the idle fades out in 0.2 s and `grid_launch` starts once;
  lights out is 1.5 s later and the cars move 0.5 s after that. So a
  launch clip is *not* "from lights out": it opens with 1.6 s of the
  recording's own last grid revving (`GO_AT_S`), and the real getaway
  lands on lights out. The first cut started at the getaway, so in game
  the field roared off on the 3rd light.
  **Level:** the recording stays as it is. A level automation onto the
  stock launch shape was tried and dropped: raising squashed phone audio
  made it sound broken. `package.py` sets the launch's loudest 0.5 s
  7 dB over the stock burst, so it peaks at pass-by level, and the grid
  loop 5 dB over the stock idle (`START_*_BOOST_DB`). Matched to stock it
  was inaudible in game: the stock start is quiet, and a 22 s grandstand
  roar at that level reads as background. A `--test-start` run proved the
  slots play.
  **Test:** `package.py --install --test-start` swaps the start for loud
  non-car tones (a beep a second on the grid; three beeps, then a rising
  siren from lights out), to check in game that the start slots play at
  all. Install again without the flag to put the real start back.
  **Check:** `start_preview.py` (run by `package.py --install`) mixes
  each installed pair the way the game does, lights included, into
  `library/starts/ingame_start_NN.wav`; the mod browser lists them first.
- **Track bed (`ambience.py`):** the montages are cut into shots at camera
  cuts (a sudden spectral change between the 0.3 s before and after),
  keeping shots of 8+ s with engines, almost no speech and 9+ dB of level
  swing (cars coming and going; uploads whose level was flattened sound
  like a wall). 2012–2013 cars only (see "Era"): since 2026-11-07 the
  bed is the 2013 Hockenheim sound check, Nürburgring and Norisring roll-out.
  Start and grid clips stay out of the bed.

## Findings so far (2026-11-04, all downloads in)

- **Driver onboards (45, one flying lap each):** clean engine with only 2–5 % speech. They give about 1,000 s of steady high RPM and full throttle, roughly 950 upshifts and 180 downshifts. All three makes are covered at every track except Mercedes at Oschersleben.
- **No idle, grid or pit material:** the onboards are single laps. The grid and pit banks came later, from fan recordings (`starts.py`, `pits.py`).
- **Race and qualifying broadcasts (2 h each):** commentary almost throughout. About 50 pass-bys pass the commentary check, and 3 are good enough to package; listen to those before trusting them.
- **Race starts in the broadcasts:** found reliably (field surge after grid revs), but unusable: commentary peaks there and every separation model leaves watery gaps.
- **Separation:** usable only where commentary is quiet (pass-bys, track ambience). Demucs runs at ~4x real time on this CPU, Mel-RoFormer at ~1x.
- **Highlight shows:** commentary over 79–97 % of every show, so no clean pass-bys.
- **Trackviews:** spectra show mirrored bands, one rising while another falls, which a single engine cannot do. They stay in the library, labelled, but packaging skips them.
