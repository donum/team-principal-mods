"""Stage 4b: the cars-on-track bed from real trackside recordings.

The spectator uploads (catalog type `spectator`: fans filming from the
grandstands and fences, no commentary) are montages: a few seconds to a
minute per camera position, then a hard cut. This stage

  1. finds the cuts: a sudden change of the sound's spectral balance
     between the 0.3 s before and after a frame, standing far out from the
     video's own frame-to-frame variation;
  2. keeps the shots in between that are long enough (>= MIN_SHOT_S), carry
     engines (clarity) and almost no speech, breathe (cars coming and going,
     MIN_DR_DB), and come from the V8 era (title year 2011-2018 or none;
     from 2019 the cars had turbo four-cylinders); start, grid and
     formation-lap clips stay out (a start mid-session would be wrong);
  3. joins them into one loop of BED_S seconds, every shot level-matched to
     the others but with its own dynamics kept, 2 s equal-power crossfades,
     no video twice in a row, the end crossfaded into the start.

Nothing is synthesised or filtered: every second is a real recording.
Output: private/engine_audio/library/ambience/cars_on_track.ogg (+ a
listening preview and shots.json listing every source second used).

    python tools/engine_audio/ambience.py [--seconds 393] [--seed 1]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import uniform_filter1d

from common import FEATURE_DIR, LIBRARY_DIR, connect, decode, dump_json, write_wav

SR = 44100
FPS = 20                 # segment.py feature rate
BED_S = 393.0            # length of the stock cars_on_track loop
MIN_SHOT_S = 8.0
MIN_DR_DB = 9.0          # level swing (p95 - p10) a shot needs: cars coming and going.
                         # Uploads whose camera or editor flattened the level (3-5 dB)
                         # sound like a constant wall of engines.
MAX_SHOT_S = 60.0
TRIM_S = 0.4             # dropped at both ends of a shot (camera handling around cuts)
XF_S = 2.0
OUT_DIR = LIBRARY_DIR / "ambience"


NOT_BED = re.compile(r"start|grid|aufstellung|einf.hrung|runde 1|1ste runde|warm.?up", re.I)


def era_ok(title: str) -> bool:
    years = [int(y) for y in re.findall(r"\b(20[0-2]\d)\b", title)]
    years += [2000 + int(y) for y in re.findall(r"\b\d{1,2}\.\d{1,2}\.(\d{2})\b", title)]
    return all(2011 <= y <= 2018 for y in years)


def band_frames(path: Path) -> np.ndarray:
    """24 log-spaced band levels (dB) at FPS frames per second, mono."""
    sr = 22050
    x = decode(path, 0, None, sr, 1)[:, 0]
    hop, n = sr // FPS, 2048
    frames = np.lib.stride_tricks.sliding_window_view(np.pad(x, (n // 2, n)), n)[::hop]
    spec = np.abs(np.fft.rfft(frames * np.hanning(n), axis=1)) ** 2
    edges = np.geomspace(60, 9000, 25)
    f = np.fft.rfftfreq(n, 1 / sr)
    bands = np.stack([spec[:, (f >= a) & (f < b)].sum(1) for a, b in zip(edges[:-1], edges[1:])], 1)
    return 10 * np.log10(bands + 1e-10)


def find_cuts(B: np.ndarray) -> list[int]:
    w = int(0.3 * FPS)
    c = np.cumsum(np.vstack([np.zeros(B.shape[1]), B]), 0)
    t = np.arange(w, len(B) - w)
    before = (c[t] - c[t - w]) / w
    after = (c[t + w] - c[t]) / w
    d = np.zeros(len(B))
    d[t] = np.sqrt(((after - before) ** 2).mean(1))
    jump = np.zeros(len(B))
    jump[1:] = np.sqrt(((B[1:] - B[:-1]) ** 2).mean(1))
    med = np.median(d[t])
    mad = np.median(np.abs(d[t] - med)) + 1e-6
    cand = np.flatnonzero((d > med + 6 * mad) & (d > 4.0) & (jump > np.percentile(jump, 97)))
    cuts = []
    for i in cand:
        if cuts and i - cuts[-1] < FPS:
            if d[i] > d[cuts[-1]]:
                cuts[-1] = i
            continue
        cuts.append(int(i))
    return cuts


def shots_of(row, path: Path) -> list[dict]:
    feat = np.load(FEATURE_DIR / f"{row['id']}.npz")
    B = band_frames(path)
    n = min(len(B), len(feat["speech"]))
    bounds = [0] + find_cuts(B[:n]) + [n]
    out = []
    trim = int(TRIM_S * FPS)
    for a, b in zip(bounds[:-1], bounds[1:]):
        a, b = a + trim, b - trim
        if (b - a) / FPS < MIN_SHOT_S:
            continue
        sl = slice(a, b)
        speech = float(feat["speech"][sl].mean())
        engine = float((feat["clarity"][sl] > 3).mean())
        lvl = uniform_filter1d(feat["loud"][sl], 10)
        dr = float(np.percentile(lvl, 95) - np.percentile(lvl, 10))
        if speech > 0.12 or engine < 0.3 or dr < MIN_DR_DB:
            continue
        out.append(dict(video_id=row["id"], title=row["title"], path=str(path), start_s=a / FPS,
                        end_s=b / FPS, speech=round(speech, 3), engine=round(engine, 2),
                        dynamics_db=round(dr, 1)))
    return out


def rms_db(x: np.ndarray) -> float:
    return float(10 * np.log10(np.mean(np.square(x)) + 1e-12))


def build_bed(shots: list[dict], seconds: float, rng) -> tuple[np.ndarray, list[dict]]:
    by_video: dict[str, list[dict]] = {}
    for s in shots:
        by_video.setdefault(s["video_id"], []).append(s)
    for v in by_video.values():
        rng.shuffle(v)
    order, last = [], None
    total = 0.0
    pools = {k: list(v) for k, v in by_video.items()}
    while total < seconds + XF_S and any(pools.values()):
        keys = [k for k, v in pools.items() if v and k != last] or [k for k, v in pools.items() if v]
        k = max(keys, key=lambda k: len(pools[k]) + rng.random())     # spread videos evenly
        s = pools[k].pop()
        order.append(s)
        total += min(s["end_s"] - s["start_s"], MAX_SHOT_S) - XF_S
        last = k
    xf = int(XF_S * SR)
    fade_in = np.sin(np.linspace(0, np.pi / 2, xf)) [:, None]
    fade_out = np.cos(np.linspace(0, np.pi / 2, xf))[:, None]
    out = np.zeros((0, 2), np.float32)
    used = []
    for s in order:
        dur = min(s["end_s"] - s["start_s"], MAX_SHOT_S)
        start = s["start_s"] + rng.uniform(0, (s["end_s"] - s["start_s"]) - dur)
        x = decode(Path(s["path"]), start, dur, SR, 2)
        x = x * 10 ** ((-20.0 - rms_db(x)) / 20)                        # shots level-matched
        if len(out) >= xf:
            out[-xf:] = out[-xf:] * fade_out + x[:xf] * fade_in
            out = np.concatenate([out, x[xf:]])
        else:
            out = x.copy()
        used.append(dict(s, used_from=round(start, 2), used_s=round(dur, 2)))
    n = int(seconds * SR)
    if len(out) < n + xf:
        raise SystemExit(f"only {len(out) / SR:.0f} s of shots for a {seconds:.0f} s bed")
    loop = out[:n].copy()
    loop[:xf] = out[n:n + xf] * fade_out + loop[:xf] * fade_in               # seamless wrap
    return loop, used


def collect_shots(db) -> list[dict]:
    rows = db.execute("""SELECT v.id, v.title, a.path FROM videos v JOIN audio a ON a.id = v.id
                         WHERE v.video_type = 'spectator' AND v.status = 'done'""").fetchall()
    shots = []
    for r in rows:
        if not era_ok(r["title"]) or NOT_BED.search(r["title"]) or not (FEATURE_DIR / f"{r['id']}.npz").exists():
            continue
        s = shots_of(r, Path(r["path"]))
        print(f"{r['id']} {r['title'][:50]:<50} {len(s):3} shots, {sum(x['end_s'] - x['start_s'] for x in s):5.0f} s")
        shots += s
    return shots


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seconds", type=float, default=BED_S)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    shots = collect_shots(connect())
    bed, used = build_bed(shots, args.seconds, np.random.default_rng(args.seed))
    bed *= 10 ** (-1 / 20) / (np.abs(bed).max() + 1e-9)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_wav(OUT_DIR / "cars_on_track.ogg", bed, SR)
    write_wav(OUT_DIR / "cars_on_track_preview.wav", bed[:int(90 * SR)], SR)
    dump_json(OUT_DIR / "shots.json", used)
    print(f"bed {len(bed) / SR:.0f} s from {len(used)} shots of {len({u['video_id'] for u in used})} videos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
