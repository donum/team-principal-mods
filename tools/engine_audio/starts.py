"""Stage 4c: real grid idle / launch pairs from fan recordings of race starts.

The broadcast starts are buried under commentary, so the starts come from
spectators filming in the grandstands (catalog type `spectator`). Most of
those are poor at the one moment that matters: as the field launches the
crowd cheers and the phone mic overloads, so the launch turns into noise.
The starts are therefore picked by ear and by measurement (see README),
and listed by hand below. This stage

  1. refines "go": the largest lasting level step within +-1.5 s of the
     listed time (see refine_go);
  2. cuts the launch so that go lands GO_AT_S into it. The game starts
     grid_launch when the 3rd of five lights comes on (0.5 s apart), so the
     clip opens with the grid's last revving and lights out falls 1.5 s in
     (the cars move at 2.0 s). The launch can have a stretch spliced out
     (`skip`), runs to the end of the recording or on into a `tail` from
     another recording (equal-power crossfade, levels matched), is cut to
     `launch_s` if set, then fades out;
  3. loops the grid revving: up to IDLE_MAX_S of it, the tail crossfaded
     into the head so it repeats without a click.

Nothing is synthesised or levelled: both clips are the recordings as they
are (an earlier level automation made the phone audio sound squashed).

    python tools/engine_audio/starts.py        # previews in private/.../library/starts
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from common import LIBRARY_DIR, connect, decode, dump_json, write_wav

SR = 44100
IDLE_MAX_S = 15.0
LOOP_XF_S = 1.0
TAIL_XF_S = 2.0
SPLICE_XF_S = 1.0
END_FADE_S = 2.5
# When the game plays the pair (ui/live_audio.py, ui/screens/race_screen.py):
# grid_idle loops on the grid; when the 3rd start light comes on (1.5 s into
# the sequence) the idle fades out in 0.2 s and grid_launch starts once;
# lights out is 1.5 s later and the cars move 0.5 s after that.
GO_AT_S = 1.6
OUT_DIR = LIBRARY_DIR / "starts"

# video id, grid revving from/to, go estimate (refine=False: exact), launch end
# (None: end of the video), note; optional: skip (a, b: launch seconds spliced
# out), tail (video id, from, to) joined at join_s launch seconds (default:
# the end) over tail_xf_s, launch_s (clip length), fade_s (default
# END_FADE_S) and fade_db (a steady fall of that many dB; default a cosine);
# seconds in the video
STARTS = [
    # go set by hand: the 1-4 kHz roar steps up 6 dB at 54.6 s and stays; the
    # phone's gain control smears the broadband level, so refine_go is off
    # 14.5 s, picked by ear 2026-11-05. 5-10 s of steady roar are spliced out
    # so the close pass lands at 6.6 s (the plain 12 s cut lost it and sounded
    # flat); at 8 s it crossfades into the 2017 Hockenheim field leaving
    # towards turn 1, real distance (already dull: centroid 2.4 -> 1.3 kHz),
    # then a 4 s fade falling steadily in dB. The cosine fade sounded like a
    # file fading out, not cars moving away; a sliding low-pass (on our own
    # recording, or on this ending) was tried and left out.
    # 2026-11-07: the 2017 Hockenheim tail ("IBuEsBSh9_I", 16.0, 22.5, joined
    # at join_s=8.0 over 1.5 s) is out: only 2012-2013 cars may be heard
    # (common.ERA). Until an in-era recording of the field leaving is found,
    # the launch runs to the end of this recording and fades there.
    dict(vid="fk9f2Qt5x20", idle=(37.0, 52.0), go=54.5, refine=False, end=None,
         skip=(5.0, 10.0), tail=None, fade_s=4.0, fade_db=30,
         note="Hockenheim finale 2013, grid and start: clean revving, the getaway, the field "
              "swelling past (5-10 s spliced out), to the end of the recording, then a 4 s fade"),
]
# Set aside after listening in game (2026-11-04): noise and mic overload at the
# launch (Nurburgring 2014 x_JJhPIFjdY, Hockenheim 2012 kf4kpYMJ3vc, Zandvoort
# 2015 8sTzEebHYSo), Brands Hatch 4pue6jM-VQY dropped with them.


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


def rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(x, dtype=np.float64))) + 1e-12)


def join_tail(launch: np.ndarray, tail: np.ndarray, xf_s: float = TAIL_XF_S) -> np.ndarray:
    """Equal-power crossfade, the tail scaled to the launch's level where they meet."""
    xf = int(xf_s * SR)
    tail = tail * (rms(launch[-xf:]) / rms(tail[:xf]))
    th = np.linspace(0, np.pi / 2, xf)[:, None]
    mid = launch[-xf:] * np.cos(th) + tail[:xf] * np.sin(th)
    return np.concatenate([launch[:-xf], mid, tail[xf:]])


def splice(x: np.ndarray, a: float, b: float) -> np.ndarray:
    """Take out a..b s (equal-power crossfade of SPLICE_XF_S centred on the
    cut, no level change): moves a later moment of the same recording earlier."""
    xf = int(SPLICE_XF_S * SR)
    i, j = int(a * SR) - xf // 2, int(b * SR) - xf // 2
    th = np.linspace(0, np.pi / 2, xf)[:, None]
    mid = x[i:i + xf] * np.cos(th) + x[j:j + xf] * np.sin(th)
    return np.concatenate([x[:i], mid, x[j + xf:]])


def path_of(db, vid: str) -> tuple[str, Path] | None:
    row = db.execute("SELECT v.title, a.path FROM videos v JOIN audio a ON a.id = v.id WHERE v.id=?",
                     (vid,)).fetchone()
    return (row["title"], Path(row["path"])) if row and Path(row["path"]).exists() else None


def render(db, s: dict):
    title, path = path_of(db, s["vid"])
    t0 = s["idle"][0]
    x = decode(path, t0, None if s["end"] is None else s["end"] - t0, SR, 2)
    go = refine_go(x, t0, s["go"]) if s.get("refine", True) else s["go"]
    launch = x[int((go - GO_AT_S - t0) * SR):].copy()
    if s.get("skip"):
        launch = splice(launch, *s["skip"])
    if s.get("tail"):
        if s.get("join_s"):
            launch = launch[:int((s["join_s"] + s.get("tail_xf_s", TAIL_XF_S)) * SR)]
        _, tpath = path_of(db, s["tail"][0])
        launch = join_tail(launch, decode(tpath, s["tail"][1], s["tail"][2] - s["tail"][1], SR, 2),
                           s.get("tail_xf_s", TAIL_XF_S))
    if s.get("launch_s"):
        launch = launch[:int(s["launch_s"] * SR)]
    fo = int(s.get("fade_s", END_FADE_S) * SR)
    if s.get("fade_db"):
        # steady fall in dB (how a receding field sounds), not a cosine that
        # holds and then drops; the last 30 ms go to silence in package.fades
        launch[-fo:] *= (10 ** (-s["fade_db"] * np.linspace(0, 1, fo) / 20))[:, None]
    else:
        launch[-fo:] *= np.cos(np.linspace(0, np.pi / 2, fo))[:, None]
    idle_end = min(s["idle"][1], go - 0.25)
    idle_start = max(s["idle"][0], idle_end - IDLE_MAX_S)
    idle = make_loop(x[int((idle_start - t0) * SR):int((idle_end - t0) * SR)])
    return title, idle, launch, go


def test_pair() -> tuple[np.ndarray, np.ndarray]:
    """Unmistakable non-car tones for checking that the game plays the start
    slots at all (package.py --test-start). Grid: a 660 Hz beep every second.
    Launch: three 880 Hz beeps from the 3rd light, a siren rising 300->900 Hz
    from lights out (GO_AT_S), then a 440 Hz tone fading over 6 s."""
    def tone(f, dur, amp=0.5):
        t = np.arange(int(dur * SR)) / SR
        f = np.broadcast_to(f, t.shape) if np.ndim(f) else np.full(t.shape, f)
        ph = 2 * np.pi * np.cumsum(f) / SR
        env = np.minimum(1, np.minimum(t, t[-1] - t) / 0.01)
        return (amp * env * np.sin(ph)).astype(np.float32)
    idle = np.zeros(int(4 * SR), np.float32)
    for k in range(4):
        b = tone(660, 0.15); idle[k * SR:k * SR + len(b)] += b
    launch = np.zeros(int(12 * SR), np.float32)
    for k in range(3):
        b = tone(880, 0.1); i = int(k * 0.5 * SR); launch[i:i + len(b)] += b
    sweep = tone(np.linspace(300, 900, int(3 * SR)), 3.0, 0.6)
    i = int(GO_AT_S * SR); launch[i:i + len(sweep)] += sweep
    tail = tone(440, 12 - GO_AT_S - 3.0) * np.linspace(1, 0, int((12 - GO_AT_S - 3.0) * SR), dtype=np.float32)
    launch[i + len(sweep):i + len(sweep) + len(tail)] += tail[:len(launch) - i - len(sweep)]
    return np.stack([idle, idle], 1), np.stack([launch, launch], 1)


def real_starts(db) -> list[dict]:
    out = []
    for s in STARTS:
        if not path_of(db, s["vid"]) or (s.get("tail") and not path_of(db, s["tail"][0])):
            continue
        title, idle, launch, go = render(db, s)
        out.append(dict(video_id=s["vid"], title=title, note=s["note"], go_s=round(go, 2),
                        tail=s.get("tail"), idle=idle, launch=launch))
    return out


def main() -> int:
    starts = real_starts(connect())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("start_*.wav"):
        old.unlink()
    meta = []
    for i, s in enumerate(starts, 1):
        peak = max(np.abs(s["idle"]).max(), np.abs(s["launch"]).max()) + 1e-9
        g = 10 ** (-1 / 20) / peak
        write_wav(OUT_DIR / f"start_{i:02d}_grid_idle.wav", s["idle"] * g, SR)
        write_wav(OUT_DIR / f"start_{i:02d}_grid_launch.wav", s["launch"] * g, SR)
        write_wav(OUT_DIR / f"start_{i:02d}_idle_then_launch.wav",
                  np.concatenate([s["idle"], s["launch"]]) * g, SR)
        meta.append({k: v for k, v in s.items() if k not in ("idle", "launch")}
                    | dict(idle_s=round(len(s["idle"]) / SR, 2), launch_s=round(len(s["launch"]) / SR, 2)))
        print(f"start {i}: {s['video_id']} go {s['go_s']:.2f}s, grid loop {len(s['idle']) / SR:.1f}s, "
              f"launch {len(s['launch']) / SR:.1f}s")
    dump_json(OUT_DIR / "starts.json", meta)
    return 0


if __name__ == "__main__":
    sys.exit(main())
