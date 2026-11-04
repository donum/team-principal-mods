# Engine-audio pipeline (private)

Builds a DTM 2013 engine-sound library from downloaded onboard and TV videos,
and packages it as a sound overlay for the locally installed `dtm2013` pack.

**Personal use only.** The source audio belongs to ITR / DTM. Audio, clips and
caches live in `private/engine_audio/` (gitignored). Only code and the
metadata overrides are committed. The overlay goes into the *installed* pack
only, never into `dist/` or the Workshop. The installed pack gets a
`assets/audio/PRIVATE_AUDIO_DO_NOT_UPLOAD.txt` marker while the overlay is on.

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
| `catalog.py` | each queue folder's `done.json` / `todo.json` (read-only), `seasons/dtm-2013/research` | `library.sqlite` table `videos`, `manifest.csv`, coverage matrix on stdout |
| `extract.py` | catalog rows with status `done` | `audio/<make>/<track>/<session>/<driver>/<id>.mka` (stream copy, no re-encode) |
| `segment.py` | extracted audio | `features/<id>.npz`, tables `analysis` and `segments` |
| `library.py` | segments | `library/index.html` (playable), `library/coverage.md`, ranked WAV clips |
| `events.py` | broadcast features (race and qualifying re-lives) | table `events`: race-start, pit-stop, pass-by and track-bed candidates |
| `starts.py` | fan recordings of race starts (hand-listed) | real grid idle loops and launches (used by `package.py`) |
| `ambience.py` | spectator montages | 393 s `cars_on_track` loop of real trackside shots, cut at camera cuts |
| `start_synth.py` | clean onboard windows | simulated 22-car grid idle and launch (only with `package.py --synth-starts`) |
| `package.py` | segments, base pack audio levels | `pack/dtm2013/` (files + `overlay.json`); `--install` applies it |
| `overlay.py` | `pack/dtm2013/` | `apply`, `remove`, `status` on the installed pack |

`build_pack.py --install` re-applies the overlay after reinstalling the pack.
`--no-private-audio` installs without it.

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
  - `grid_idle_NN` / `grid_launch_NN` pairs are cut from fan recordings of real starts by `starts.py` (simulated ones only with `--synth-starts`), and `pit_exit_NN` would come from onboard pit exits (none so far);
  - they replace the stock clips with the same key; fire-ups and wheelguns stay stock;
  - these banks are shared by all cars (wishlist E8).
- **Track bed** (`ambience/session_layers.json`): `cars.file` points to the `ambience.py` loop.
- **Levels** match the stock clips.

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

- **Starts (`starts.py`):** four fan recordings, listed by hand from level
  timelines and spectrograms: 2014 Nürburgring and Brands Hatch have 10+ s
  of grid revving before lights out; 2012 Hockenheim and 2015 Zandvoort only
  about 4 s. "Go" is refined to where the level steps up for good (median
  of the next 1.5 s against the previous 1.5 s), so a rev blip doesn't win.
  Phone cameras flatten the launch to +3–4 dB over the grid, and a raw cut
  stays loud until it stops dead, so in game the start felt toned down
  with sound missing at the end. The launch is therefore levelled onto the
  stock launch curve (`LAUNCH_SHAPE_DB`): a burst about 10 dB over the grid
  within the first second, then the field fading over six seconds. Only
  the level is automated (0.75 s window), so gear changes and blips stay
  as recorded.
- **Track bed (`ambience.py`):** the montages are cut into shots at camera
  cuts (a sudden spectral change between the 0.3 s before and after),
  keeping shots of 8+ s with engines, almost no speech and 9+ dB of level
  swing (cars coming and going; uploads whose level was flattened sound
  like a wall). V8 era only: from 2019 the DTM ran turbo four-cylinders.
  Start and grid clips stay out of the bed.

## Findings so far (2026-11-04, all downloads in)

- **Driver onboards (45, one flying lap each):** clean engine with only 2–5 % speech. They give about 1,000 s of steady high RPM and full throttle, roughly 950 upshifts and 180 downshifts. All three makes are covered at every track except Mercedes at Oschersleben.
- **No idle, grid or pit material:** the onboards are single laps, so the grid idle/launch and pit-exit banks stay stock.
- **Race and qualifying broadcasts (2 h each):** commentary almost throughout. About 50 pass-bys pass the commentary check, and 3 are good enough to package; listen to those before trusting them.
- **Race starts in the broadcasts:** found reliably (field surge after grid revs), but unusable: commentary peaks there and every separation model leaves watery gaps.
- **Separation:** usable only where commentary is quiet (pass-bys, track ambience). Demucs runs at ~4x real time on this CPU, Mel-RoFormer at ~1x.
- **Highlight shows:** commentary over 79–97 % of every show, so no clean pass-bys.
- **Trackviews:** spectra show mirrored bands, one rising while another falls, which a single engine cannot do. They stay in the library, labelled, but packaging skips them.
