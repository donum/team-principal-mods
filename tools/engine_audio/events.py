"""Stage 3b: find broadcast moments worth separating from the commentary.

Scans the full race and qualifying re-lives (TV broadcasts over 20 min) and
stores candidate events as references (table `events`):

  race_start  the field launching from the grid: engines at grid revs
              (< ~4,800 rpm), then within a few seconds a jump above 6,500
              rpm and a level surge of 4+ dB. Up to 3 candidates per race,
              because camera cuts also make level jumps; review.py lets you
              confirm the real one by ear.
  pit_stop    clusters of wheelgun-like bursts: high-band (2.5-7.5 kHz)
              energy standing out from its surroundings with a 12-40 Hz
              impact rhythm, which sibilants and engines lack. Low
              confidence: up to 5 candidates per race, used only once kept.
  passby      the loudest broadcast pass-bys from segment.py (Doppler drop
              and pan sweep), whatever the commentary: separation removes it.
  track_bed   60 s windows of on-track sound, every 3 min through the
              middle of each race and session, for the cars_on_track bed.

Windows carry padding so separate.py has context. Re-running replaces the
events of a video only when its analysis or this file's VERSION changed.

    python tools/engine_audio/events.py [--only ID ...] [--force]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from scipy.ndimage import median_filter, uniform_filter1d

from common import FEATURE_DIR, connect, stream_decode

VERSION = 1
FPS = 20                      # segment.py feature rate
MIN_BROADCAST_S = 1200        # full re-lives only, not the short reports

SCHEMA = [
    """CREATE TABLE IF NOT EXISTS events (
        event_id TEXT PRIMARY KEY, video_id TEXT, kind TEXT, anchor_s REAL,
        start_s REAL, end_s REAL, score REAL, info TEXT, version INTEGER)""",
    "CREATE INDEX IF NOT EXISTS ev_video ON events(video_id)",
    """CREATE TABLE IF NOT EXISTS event_scans (
        video_id TEXT PRIMARY KEY, version INTEGER, analysis TEXT)""",
]


# ------------------------------------------------------------------ helpers

def blocks(x: np.ndarray, fn, size: int = FPS) -> np.ndarray:
    n = len(x) // size
    return np.array([fn(x[i * size:(i + 1) * size]) for i in range(n)])


def nanmed(a: np.ndarray) -> float:
    return float(np.nanmedian(a)) if np.isfinite(a).sum() >= max(2, len(a) // 4) else np.nan


def keep_apart(cands: list[tuple], gap: float, n: int) -> list[tuple]:
    """Best-first, at least `gap` seconds apart (cands: (score, t, ...))."""
    out = []
    for c in sorted(cands, key=lambda c: -c[0]):
        if all(abs(c[1] - k[1]) >= gap for k in out):
            out.append(c)
        if len(out) == n:
            break
    return out


# ------------------------------------------------------------------ detectors

def race_starts(f: dict, duration: float, n: int = 3) -> list[dict]:
    lr = np.log(np.where(f["clarity"] > 3.0, np.maximum(f["rpm"], 1), np.nan))
    rpm = blocks(lr, lambda a: nanmed(a))                       # 1 s blocks, ln rpm
    loud = blocks(f["loud"], np.median)
    cands = []
    for t in range(15, int(len(rpm) * 0.45)):
        pre, post = rpm[t - 12:t - 2], rpm[t + 1:t + 6]
        if np.isfinite(pre).sum() < 4 or np.isfinite(post).sum() < 3:
            continue
        r0, r1 = np.exp(np.nanmedian(pre)), np.exp(np.nanmedian(post))
        rise = np.log(r1 / r0)
        lrise = float(np.median(loud[t + 1:t + 6]) - np.median(loud[t - 12:t - 2]))
        if r1 > 6500 and r0 < 4800 and rise > 0.25 and lrise > 4.0:
            score = lrise / 10 + rise + (0.3 if r0 < 4300 else 0.0)
            cands.append((score, t, r0, r1, lrise))
    out = []
    for score, t, r0, r1, lrise in keep_apart(cands, 30, n):
        # refine "go" to 50 ms: steepest level rise within the second around t
        i0 = max(0, (t - 1) * FPS)
        sm = uniform_filter1d(f["loud"][i0:(t + 2) * FPS], 4)
        go = (i0 + int(np.argmax(np.gradient(sm)))) / FPS if len(sm) > 2 else float(t)
        out.append(dict(kind="race_start", anchor=go, start=go - 30, end=go + 15, score=score,
                        info=dict(rpm_before=round(r0), rpm_after=round(r1), level_rise_db=round(lrise, 1))))
    return out


def high_band_scan(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """2.5-7.5 kHz and 0.3-2 kHz levels (dB) at 100 frames/s."""
    sr, hop, n = 16000, 160, 512
    freqs = np.fft.rfftfreq(n, 1 / sr)
    hb, lb = (freqs >= 2500) & (freqs <= 7500), (freqs >= 300) & (freqs <= 2000)
    win = np.hanning(n).astype(np.float32)
    hi, lo, carry = [], [], np.zeros(0, np.float32)
    for blk in stream_decode(path, sr, 1):
        buf = np.concatenate([carry, blk[:, 0]])
        k = (len(buf) - n) // hop + 1
        if k <= 0:
            carry = buf
            continue
        fr = sliding_window_view(buf, n)[::hop][:k] * win
        carry = buf[k * hop:]
        p = np.abs(np.fft.rfft(fr, axis=1)) ** 2
        hi.append(10 * np.log10(p[:, hb].sum(1) + 1e-12))
        lo.append(10 * np.log10(p[:, lb].sum(1) + 1e-12))
    return np.concatenate(hi), np.concatenate(lo)


def pit_stops(hi: np.ndarray, duration: float, n: int = 5) -> list[dict]:
    fps, w, step = 100, 32, 5
    env = 10 ** (hi / 20)
    seg = sliding_window_view(env, w)[::step]
    seg = seg - seg.mean(1, keepdims=True)
    p = np.abs(np.fft.rfft(seg * np.hanning(w), axis=1)) ** 2
    f = np.fft.rfftfreq(w, 1 / fps)
    mod = p[:, (f >= 12) & (f <= 40)].sum(1) / (p[:, f >= 3].sum(1) + 1e-12)
    lvl = uniform_filter1d(hi, w)[::step][:len(mod)]
    prom = lvl - median_filter(lvl, size=10 * fps // step)
    t = np.arange(len(mod)) * step / fps
    hits = np.flatnonzero((mod > 0.55) & (prom > 6))
    clusters = []
    for i in hits:
        if clusters and t[i] - clusters[-1][-1] < 4:
            clusters[-1].append(t[i])
        else:
            clusters.append([t[i]])
    lo_t, hi_t = 0.15 * duration, 0.95 * duration          # stops happen during the race
    cands = [(len(c), c[0], c[-1]) for c in clusters if len(c) >= 6 and lo_t < c[0] < hi_t]
    return [dict(kind="pit_stop", anchor=a, start=a - 10, end=b + 15, score=k / 20,
                 info=dict(bursts=k, span_s=round(b - a, 1)))
            for k, a, b in keep_apart(cands, 60, n)]


def passbys(db, video_id: str, n: int = 25) -> list[dict]:
    rows = db.execute("""SELECT * FROM segments WHERE video_id=? AND label='passby'
                         AND direction IN ('rl','lr')""", (video_id,)).fetchall()
    out = []
    for r in rows:
        out.append(dict(kind="passby", anchor=r["peak_s"], start=r["peak_s"] - 5, end=r["peak_s"] + 5,
                        score=float(r["quality"] or 0) + float(r["clarity"] or 0) / 20,
                        info=dict(direction=r["direction"], seg_id=r["seg_id"],
                                  rpm=[round(r["rpm_start"]), round(r["rpm_end"])])))
    out.sort(key=lambda e: -e["score"])
    return out[:n]


def track_beds(f: dict, duration: float, n: int = 6) -> list[dict]:
    lo, hi = int(0.25 * duration), int(0.9 * duration) - 60
    cands = []
    for t0 in range(lo, max(lo, hi), 180):
        sl = slice(t0 * FPS, (t0 + 60) * FPS)
        clear = float((f["clarity"][sl] > 3).mean())
        talk = float(f["speech"][sl].mean())
        cands.append((clear - 0.5 * talk, t0 + 30, clear, talk))
    return [dict(kind="track_bed", anchor=t, start=t - 30, end=t + 30, score=s,
                 info=dict(engine_share=round(c, 2), speech=round(sp, 2)))
            for s, t, c, sp in keep_apart(cands, 120, n)]


# ---------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="*", help="video ids")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    db = connect()
    for s in SCHEMA:
        db.execute(s)
    rows = db.execute("""SELECT v.id, v.title, v.session, v.duration_s, a.path, an.analyzed
                         FROM videos v JOIN audio a ON a.id = v.id JOIN analysis an ON an.id = v.id
                         WHERE v.video_type = 'broadcast' AND v.duration_s >= ?
                         ORDER BY v.round, v.session""", (MIN_BROADCAST_S,)).fetchall()
    done = {r["video_id"]: (r["version"], r["analysis"]) for r in db.execute("SELECT * FROM event_scans")}
    total = 0
    for r in rows:
        if args.only and r["id"] not in args.only:
            continue
        if not args.force and done.get(r["id"]) == (VERSION, r["analyzed"]):
            continue
        t0 = time.time()
        feat = FEATURE_DIR / f"{r['id']}.npz"
        if not feat.exists():
            continue
        f = dict(np.load(feat))
        dur = float(r["duration_s"])
        evs = passbys(db, r["id"]) + track_beds(f, dur)
        if r["session"] == "race":
            evs += race_starts(f, dur)
            hb_cache = FEATURE_DIR / f"{r['id']}_hb.npz"
            if hb_cache.exists():
                hi = np.load(hb_cache)["hi"]
            else:
                hi, lo = high_band_scan(Path(r["path"]))
                np.savez_compressed(hb_cache, hi=hi.astype(np.float32), lo=lo.astype(np.float32))
            evs += pit_stops(hi, dur)
        db.execute("DELETE FROM events WHERE video_id=?", (r["id"],))
        for e in evs:
            start, end = max(0.0, e["start"]), min(dur, e["end"])
            eid = f"{r['id']}:{e['kind']}:{int(round(e['anchor'] * 1000))}"
            db.execute("INSERT OR REPLACE INTO events VALUES (?,?,?,?,?,?,?,?,?)",
                       (eid, r["id"], e["kind"], round(e["anchor"], 2), round(start, 2), round(end, 2),
                        round(float(e["score"]), 3), json.dumps(e["info"]), VERSION))
        db.execute("INSERT OR REPLACE INTO event_scans VALUES (?,?,?)", (r["id"], VERSION, r["analyzed"]))
        db.commit()
        kinds = {}
        for e in evs:
            kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
        total += len(evs)
        print(f"{r['id']} {r['title'][:46]:<46} {time.time() - t0:4.0f}s  "
              + " ".join(f"{k}:{v}" for k, v in sorted(kinds.items())))
    print(f"{total} events")
    return 0


if __name__ == "__main__":
    sys.exit(main())
