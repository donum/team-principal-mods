"""Stage 4c: real grid idle / launch pairs from fan recordings of race starts.

The broadcast starts are buried under commentary, so the starts come from
spectators filming in the grandstands (catalog type `spectator`). Short
phone clips have no reliable structure to detect automatically, so the
starts are listed by hand below (picked from level timelines and
spectrograms, see README): the stretch of grid revving before lights out,
and roughly when the field launches. This stage

  1. refines "go": the largest lasting level step within +-1.5 s of the
     listed time (see refine_go);
  2. cuts the launch so that go lands GO_AT_S into it: the game starts
     grid_launch when the 3rd of five lights comes on (0.5 s apart), so the
     clip opens with 1.5 s of the grid's last revving and lights out falls
     at 1.5 s (the cars move at 2.0 s). After go it is levelled onto
     LAUNCH_CURVE: a burst about 10 dB over the grid, then the field fading
     towards turn 1. Phone audio is compressed, so without this the launch
     is flat, barely louder than the grid, and stops abruptly;
  3. loops the grid revving: up to IDLE_MAX_S of it, the tail crossfaded
     into the head so it repeats without a click.

Nothing is synthesised: both clips are the recording itself, only its
level is automated.

    python tools/engine_audio/starts.py        # previews in private/.../library/starts
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import uniform_filter1d

from common import LIBRARY_DIR, connect, decode, dump_json, write_wav

SR = 44100
LAUNCH_S = 10.9          # stock grid_launch length
IDLE_MAX_S = 12.0
LOOP_XF_S = 1.0
# When the game plays the pair (ui/live_audio.py, ui/screens/race_screen.py):
# grid_idle loops on the grid; when the 3rd start light comes on (1.5 s into
# the sequence) the idle fades out in 0.2 s and grid_launch starts once;
# lights out is 1.5 s later and the cars move 0.5 s after that.
GO_AT_S = 1.6
# Level after go, dB over the recording's grid revving (seconds after go),
# modelled on the stock launches: a burst within half a second, a held roar,
# then the field fading towards turn 1. Before go the recording stays as is.
LAUNCH_CURVE = [(0.0, 2), (0.5, 10), (3.0, 9), (5.0, 5), (7.5, -6), (LAUNCH_S - GO_AT_S, -30)]
OUT_DIR = LIBRARY_DIR / "starts"

# (video id, grid revving from, grid revving to, go estimate, note); seconds in the video
STARTS = [
    ("x_JJhPIFjdY", 48.0, 61.0, 61.4, "Nurburgring 2014, main grandstand: revving with blips, then the launch"),
    ("4pue6jM-VQY", 40.0, 53.0, 53.3, "Brands Hatch: pulsing revs on the grid, then the launch"),
    ("kf4kpYMJ3vc", 0.0, 4.6, 4.9, "Hockenheim 2012: short grid stretch, strong launch"),
    ("8sTzEebHYSo", 0.5, 5.2, 5.5, "Zandvoort 2015 race 2: short grid stretch, field launches past"),
]


def refine_go(x: np.ndarray, t0: float, guess: float) -> float:
    """Where the level steps up for good: the largest rise of the median 10 ms
    level (dB) over the next 1.5 s against the 1.5 s before, within +-1.5 s of
    the guess. A single rev blip is too short to win this."""
    hop = int(0.01 * SR)
    m = x.mean(axis=1)
    n = len(m) // hop
    lvl = 10 * np.log10(np.square(m[:n * hop]).reshape(n, hop).mean(1) + 1e-12)
    w = 150
    a, b = int((guess - 1.5 - t0) / 0.01), int((guess + 1.5 - t0) / 0.01)
    a, b = max(a, w), min(b, n - w)
    step = [np.median(lvl[i:i + w]) - np.median(lvl[i - w:i]) for i in range(a, b)]
    return t0 + (a + int(np.argmax(step))) * 0.01 - 0.1


def make_loop(x: np.ndarray) -> np.ndarray:
    xf = int(LOOP_XF_S * SR)
    body = x[:len(x) - xf].copy()
    w = np.linspace(0, 1, xf)[:, None]
    body[:xf] = x[-xf:] * (1 - w) + x[:xf] * w
    return body


def shape_launch(launch: np.ndarray, idle: np.ndarray) -> np.ndarray:
    """Level automation after go onto LAUNCH_CURVE, relative to this
    recording's grid revving. The recording's own short-term level (0.75 s)
    is replaced by the curve; detail shorter than that (gear changes, blips)
    stays as recorded. The revving before go is left untouched, so it runs
    on from the idle loop."""
    hop = int(0.01 * SR)
    m = launch.mean(axis=1)
    n = len(m) // hop
    p = np.square(m[:n * hop]).reshape(n, hop).mean(1)
    own = 10 * np.log10(uniform_filter1d(p, 75, mode="nearest") + 1e-12)
    t = np.arange(n) * 0.01 - GO_AT_S
    ct, cdb = zip(*LAUNCH_CURVE)
    idle_db = 10 * np.log10(np.square(idle.mean(axis=1)).mean() + 1e-12)
    g_db = np.where(t < 0, 0.0, np.clip(idle_db + np.interp(t, ct, cdb) - own, -60, 14))
    g_db = uniform_filter1d(g_db, 30, mode="nearest")
    g = np.interp(np.arange(len(launch)) / SR, np.arange(n) * 0.01, 10 ** (g_db / 20))
    return launch * g[:, None]


def render(path: Path, idle_a: float, idle_b: float, go_guess: float):
    t0 = idle_a
    x = decode(path, t0, (go_guess - t0) + LAUNCH_S + 2.0, SR, 2)
    go = refine_go(x, t0, go_guess)
    k = int((go - GO_AT_S - t0) * SR)
    launch = x[k:k + int(LAUNCH_S * SR)].copy()
    idle_end = min(idle_b, go - 0.25)
    idle_start = max(idle_a, idle_end - IDLE_MAX_S)
    idle = make_loop(x[int((idle_start - t0) * SR):int((idle_end - t0) * SR)])
    return idle, shape_launch(launch, idle), go


def real_starts(db) -> list[dict]:
    out = []
    for vid, a, b, guess, note in STARTS:
        row = db.execute("SELECT v.title, a.path FROM videos v JOIN audio a ON a.id = v.id WHERE v.id=?",
                         (vid,)).fetchone()
        if not row or not Path(row["path"]).exists():
            continue
        idle, launch, go = render(Path(row["path"]), a, b, guess)
        out.append(dict(video_id=vid, title=row["title"], note=note, go_s=round(go, 2),
                        idle=idle, launch=launch))
    return out


def main() -> int:
    starts = real_starts(connect())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    meta = []
    for i, s in enumerate(starts, 1):
        peak = max(np.abs(s["idle"]).max(), np.abs(s["launch"]).max()) + 1e-9
        g = 10 ** (-1 / 20) / peak
        write_wav(OUT_DIR / f"start_{i:02d}_grid_idle.wav", s["idle"] * g, SR)
        write_wav(OUT_DIR / f"start_{i:02d}_grid_launch.wav", s["launch"] * g, SR)
        write_wav(OUT_DIR / f"start_{i:02d}_idle_then_launch.wav",
                  np.concatenate([s["idle"], s["idle"], s["launch"]]) * g, SR)
        meta.append({k: v for k, v in s.items() if k not in ("idle", "launch")}
                    | dict(idle_s=round(len(s["idle"]) / SR, 2)))
        print(f"start {i}: {s['video_id']} go {s['go_s']:.2f}s, grid loop {len(s['idle']) / SR:.1f}s  {s['note']}")
    dump_json(OUT_DIR / "starts.json", meta)
    return 0


if __name__ == "__main__":
    sys.exit(main())
