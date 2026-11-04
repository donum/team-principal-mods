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

- **RPM:** a V8 fires 4 times per revolution, so the firing frequency is RPM/15. Each 50 ms frame scores candidate firing frequencies by the mean peak height of their harmonics below 4 kHz, and a Viterbi pass keeps the track continuous. Octave errors are then repaired:
  - a ×2 or ×½ jump within 150 ms is undone, since no gear change is an octave;
  - a stretch whose midway peaks are as strong as its harmonics is halved;
  - each stretch is kept inside 2,500–10,000 RPM.

  On synthetic V8 sweeps this lands within 2%. On real audio it is a rough guide, and not yet checked against a real onboard.
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
  - commentary-free TV pass-bys, if any, join the random bank as `dtm13_tv_NN`.
- **Grid and pit** (`race/race_engines.json`):
  - `grid_idle_NN` / `grid_launch_NN` pairs come from onboard race starts, and `pit_exit_NN` from onboard pit exits;
  - they replace the stock clips with the same key; fire-ups and wheelguns stay stock;
  - these banks are shared by all cars (wishlist E8).
- **Levels** match the stock clips.

To target another game, add a builder next to `build()` in `package.py`. The
segment references in `library.sqlite` are game-independent.

## Findings so far (2026-11-04)

- **Highlight shows (48 min each):** commentary over 79–97% of every show, so no clean pass-bys.
- **Trackviews:** spectra show mirrored bands, one rising while another falls, which a real engine's harmonics cannot do. They look like simulator or processed audio, so packaging skips them. They stay in the library, labelled.
- **Real material:** depends on the 45 driver onboards, which are still queued.
