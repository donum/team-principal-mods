"""Stage 4c: real grid idle / launch pairs from fan recordings of race starts.

The broadcast starts are buried under commentary, so the starts come from
spectators filming in the grandstands (catalog type `spectator`). Short
phone clips have no reliable structure to detect automatically, so the
starts are listed by hand below (picked from level timelines and
spectrograms, see README): the stretch of grid revving before lights out,
and roughly when the field launches. This stage

  1. refines "go" to 50 ms: the steepest broadband level rise within
     +-1.5 s of the listed time;
  2. cuts the launch from just before go, LAUNCH_S long (the game's clip
     length), ending earlier with a fade at a camera cut;
  3. loops the grid revving: up to IDLE_MAX_S of it, the tail crossfaded
     into the head so it repeats without a click.

Nothing is synthesised: both clips are the recording itself.

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


def render(path: Path, idle_a: float, idle_b: float, go_guess: float):
    t0 = idle_a
    x = decode(path, t0, (go_guess - t0) + LAUNCH_S + 2.0, SR, 2)
    go = refine_go(x, t0, go_guess)
    k = int((go - t0) * SR)
    launch = x[k:k + int(LAUNCH_S * SR)].copy()
    fo = int(1.5 * SR)
    launch[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
    idle_end = min(idle_b, go - 0.25)
    idle_start = max(idle_a, idle_end - IDLE_MAX_S)
    idle = make_loop(x[int((idle_start - t0) * SR):int((idle_end - t0) * SR)])
    return idle, launch, go


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
