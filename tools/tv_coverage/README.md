# TV coverage: commentary and pictures as a research source

The video archive (`C:\Users\dan\Videos\yt\DTM\<year>\`, or `tv_coverage_source`
in `local.json`) holds race and qualifying re-lives for most seasons. These
tools turn them into something we can search and look at, for any year:

| Tool | What it does | Output (private, gitignored) |
|---|---|---|
| `transcribe.py` | Speech to text with timestamps (faster-whisper, `medium`, on the CPU: about 10× real time). Driver and venue names from `seasons/<series>-<year>/research/` go into the prompt so they come out right. Incremental | `private/tv_coverage/transcripts/<year>/<folder>__<video>.json` and `.txt` |
| `search.py` | Regex over the transcripts, with the video time of each hit | stdout |
| `frames.py` | Stills (`--at`) and contact sheets (`--every`) with the time burnt in | `private/tv_coverage/frames/<year>/` |

```bash
python tools/tv_coverage/transcribe.py --year 2013 --match "re-?live" --list
```
```bash
python tools/tv_coverage/transcribe.py --year 2013 --match "race.*re-?live"
```
```bash
python tools/tv_coverage/search.py --year 2013 "drive.?through|safety car" --context 1
```
```bash
python tools/tv_coverage/frames.py --year 2013 --video "Spielberg.*Race" --from 0:18:00 --to 0:20:00 --every 4
```

Run them with plain `python` (faster-whisper and Pillow are in the user
site-packages). Setup: `python -m pip install --user faster-whisper`; the
model downloads on first use.

**Rights.** The commentary and the pictures belong to the broadcaster (ITR /
DTM) and the uploaders. Transcripts and frames stay in `private/`. Only facts
read from them go into the repo, with the source written as
`tv: <video path under the archive> @ h:mm:ss` (see
[docs/venues/README.md](../../docs/venues/README.md)).

## What the coverage gives

- **Grid side:** the grid seen from the front under the lights, a few minutes
  before the lap counter starts (contact sheet every 60 s, then every 4 s).
  The front row's names are in `research/results/*-race.csv` (`grid N`).
  Mind the camera: cars facing the camera have their left on screen-right.
- **Weather:** the AIR / TRACK / WIND SPEED graphic before the start.
- **Tyres:** the starting-grid graphic marks each car's tyre (option = yellow).
- **Drive-throughs, safety cars, retirements:** named by the commentators; search
  the transcripts, then check the picture.

File names can mislead: in 2013 "Hockenheim II" is the finale and plain
"Hockenheim 2013" the opener.
