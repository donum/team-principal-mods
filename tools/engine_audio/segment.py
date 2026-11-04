"""Stage 3: analyse extracted audio and store labelled segments as references.

Per video (cached in private/engine_audio/features/<id>.npz, 20 frames/s):
  rpm       engine speed from the firing-order pitch. A four-stroke V8 fires
            4 times per crank revolution, so f_fire = rpm / 60 * 4 = rpm / 15.
            Each frame scores candidate firing frequencies by their harmonic
            series in a whitened spectrum, a Viterbi pass keeps the track
            continuous, and a per-video octave check against the expected
            redline fixes half-order locks. Rough: +-5 % when the engine is
            clear, meaningless in commentary.
  clarity   how strongly that harmonic series stands out (whitened dB)
  loud      RMS level (dBFS)
  pan       L/R energy balance, -1 right .. +1 left
  speech    3-8 Hz syllable modulation in the voice band (commentary, radio)
  wind      share of energy below 100 Hz without harmonic structure
  multi     a second, unrelated harmonic series (other cars)

Segments (table `segments`, times in seconds of the source file):
  idle, full_throttle, steady_high, overrun, upshift, downshift   (any video)
  launch, pit_exit       idle/limiter followed by full throttle (onboards)
  passby                 loudness peak + Doppler pitch drop (TV/trackview)

Each has rpm/loudness stats, flags (commentary, wind, other_cars) and a 0-1
quality score, so clips can be re-cut later without re-analysing.

    python tools/engine_audio/segment.py [--force] [--only ID ...]
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from scipy.ndimage import maximum_filter1d, median_filter, uniform_filter1d

from common import FEATURE_DIR, connect, stream_decode

VERSION = 2
SR = 16000
HOP = 800                    # 50 ms -> 20 frames/s
NFFT = 4096                  # 256 ms window, 3.9 Hz bins
FPS = SR / HOP
REDLINE = 8500.0             # rough DTM 2013 V8 rev limit, used for octave fixing
RPM_LO, RPM_HI, NCAND = 1500.0, 10500.0, 160
HARMONICS = 40              # every harmonic below FMAX counts
FMAX = 4000.0
LOW_BIAS = 0.05              # per octave: breaks the f0 / 2*f0 tie toward f0
MAX_STEP = 24                # Viterbi: max candidate jump per frame (~30 %)
STEP_COST = 0.01             # Viterbi: cost per candidate step (scores are 0..1)
CLEAR_DB = 5.0               # clarity above which the pitch track is trusted (noise: ~2-3)
ODD_RATIO = 0.75             # midway/harmonic peak ratio above which a run is an octave too high

CAND_RPM = np.geomspace(RPM_LO, RPM_HI, NCAND)
CAND_F = CAND_RPM / 15.0
FREQS = np.fft.rfftfreq(NFFT, 1 / SR)
HBIN = np.rint(np.outer(CAND_F, np.arange(1, HARMONICS + 1)) * NFFT / SR).astype(int)
HMASK = (np.outer(CAND_F, np.arange(1, HARMONICS + 1)) < FMAX).astype(np.float32)
HWEIGHT = ((1 - LOW_BIAS * np.log2(CAND_F / CAND_F[0])) / HMASK.sum(axis=1)).astype(np.float32)
HBIN = np.minimum(HBIN, len(FREQS) - 1)
# Midway points (k - 0.5) * f. If the tracker sits an octave too high, these
# are the true firing harmonics and as strong as its own; for the true series
# they are only the weaker half-order peaks.
GPOS = np.outer(CAND_F, np.arange(1, HARMONICS + 1) - 0.5)
GBIN = np.minimum(np.rint(GPOS * NFFT / SR).astype(int), len(FREQS) - 1)
GMASK = (GPOS < FMAX).astype(np.float32)
WINDOW = np.hanning(NFFT).astype(np.float32)
SHORT_WIN = np.hanning(HOP).astype(np.float32)
SV_LO, SV_HI = int(300 * HOP / SR), int(3400 * HOP / SR) + 1     # voice band bins, 20 Hz each

SCHEMA = [
    """CREATE TABLE IF NOT EXISTS analysis (
        id TEXT PRIMARY KEY, version INTEGER, audio_path TEXT, audio_mtime INTEGER,
        frames INTEGER, rpm_factor REAL, clarity_median REAL, speech_share REAL,
        analyzed TEXT)""",
    """CREATE TABLE IF NOT EXISTS segments (
        seg_id TEXT PRIMARY KEY, video_id TEXT, label TEXT, start_s REAL, end_s REAL,
        peak_s REAL, direction TEXT, rpm_start REAL, rpm_end REAL, rpm_mean REAL,
        rpm_max REAL, loud_db REAL, clarity REAL, speech REAL, wind REAL, multi REAL,
        flags TEXT, quality REAL, version INTEGER)""",
    "CREATE INDEX IF NOT EXISTS seg_video ON segments(video_id)",
    "CREATE INDEX IF NOT EXISTS seg_label ON segments(label, quality)",
]


# ------------------------------------------------------------------ features

def frame_features(path: Path) -> dict:
    """Stream the file once and return per-frame arrays plus the harmonic score matrix."""
    carry = np.zeros((0, 2), np.float32)
    out = {k: [] for k in ("loud", "pan", "low", "voice", "score", "oddr")}
    lo_bin = np.searchsorted(FREQS, 100)
    for block in stream_decode(path, SR, 2):
        buf = np.concatenate([carry, block])
        n = (len(buf) - NFFT) // HOP + 1
        if n <= 0:
            carry = buf
            continue
        frames = sliding_window_view(buf, NFFT, axis=0)[::HOP][:n]     # (n, 2, NFFT)
        carry = buf[n * HOP:]
        mono = frames.mean(axis=1) * WINDOW
        spec = np.abs(np.fft.rfft(mono, axis=1)).astype(np.float32) + 1e-7
        power = spec ** 2
        total = power.sum(axis=1) + 1e-12
        # level and balance over the central hop only (no window smearing)
        mid = frames[:, :, (NFFT - HOP) // 2:(NFFT + HOP) // 2]
        e = (mid ** 2).mean(axis=2) + 1e-12                              # (n, 2)
        out["loud"].append(10 * np.log10(e.mean(axis=1)))
        out["pan"].append((e[:, 0] - e[:, 1]) / (e[:, 0] + e[:, 1]))
        out["low"].append(power[:, :lo_bin].sum(axis=1) / total)
        # voice-band level from the 50 ms centre only: the 256 ms window would
        # smooth away the 3-8 Hz syllable rhythm the speech detector looks for
        short = np.abs(np.fft.rfft(mid.mean(axis=1) * SHORT_WIN, axis=1)) ** 2
        out["voice"].append(10 * np.log10(short[:, SV_LO:SV_HI].sum(axis=1) + 1e-12))
        # whitened log spectrum: peaks above the local spectral envelope
        logs = 20 * np.log10(spec)
        env = uniform_filter1d(logs, size=51, axis=1)                    # ~200 Hz
        # peak height as a linear ratio over the envelope: weak half-order
        # peaks then count far less than the firing-order series
        # (square-root compressed, so one huge peak cannot carry a candidate)
        white = np.clip(10 ** (np.clip(logs - env, 0, 60) / 40) - 1, 0, None)
        white = maximum_filter1d(white, size=3, axis=1)                  # +-1 bin tolerance
        # mean peak height over the candidate's harmonics below FMAX: a series
        # padded with weak half-order peaks scores lower than the firing series,
        # whatever the rpm. Done per chunk to bound memory.
        sc = np.empty((len(white), NCAND), np.float32)
        oddr = np.empty((len(white), NCAND), np.float16)
        for i in range(0, len(white), 200):
            w = white[i:i + 200]
            on = (w[:, HBIN] * HMASK[None]).sum(axis=2)
            sc[i:i + 200] = on * HWEIGHT
            midway = (w[:, GBIN] * GMASK[None]).sum(axis=2) / GMASK.sum(axis=1)
            oddr[i:i + 200] = midway / (on / HMASK.sum(axis=1) + 1e-3)
        out["score"].append(sc)
        out["oddr"].append(oddr)
    return {k: (np.concatenate(v) if v else np.zeros(0)) for k, v in out.items()}


def viterbi(score: np.ndarray) -> np.ndarray:
    """Best continuous path through the candidate grid (index per frame)."""
    n, m = score.shape
    offsets = np.arange(-MAX_STEP, MAX_STEP + 1)
    penalty = STEP_COST * np.abs(offsets)
    back = np.zeros((n, m), np.int8)
    acc = score[0].astype(np.float64)
    for t in range(1, n):
        padded = np.pad(acc, MAX_STEP, constant_values=-1e9)
        win = sliding_window_view(padded, 2 * MAX_STEP + 1) - penalty    # (m, offsets)
        k = win.argmax(axis=1)
        acc = win[np.arange(m), k] + score[t]
        back[t] = k - MAX_STEP
    path = np.empty(n, int)
    path[-1] = int(acc.argmax())
    for t in range(n - 1, 0, -1):
        path[t - 1] = path[t] + back[t, path[t]]
    return path


def unwrap_octaves(rpm: np.ndarray, valid: np.ndarray, oddr: np.ndarray) -> np.ndarray:
    """Undo x2 / x0.5 jumps inside clear stretches: no gear change is an octave.

    DTM upshifts drop revs by roughly 15-25 %, downshift blips raise them by
    20-35 %, so a near-exact factor of two within 150 ms is the tracker
    switching harmonic series. A run whose midway peaks are about as strong
    as its harmonics (ODD_RATIO) is an octave too high and is halved. Each run
    is then kept inside a plausible 2500-10000 rpm band where possible.
    """
    out = rpm.astype(np.float64).copy()
    lg = np.log2(out)
    for s, e in runs(valid, 3):
        seg = lg[s:e].copy()
        jump = np.zeros_like(seg)
        d = seg[3:] - seg[:-3]
        for i in np.flatnonzero(np.abs(np.abs(d) - 1) < 0.2):
            if not jump[i + 1:i + 4].any():
                jump[i + 3] = -np.round(d[i])
        seg += np.cumsum(jump)
        if np.median(oddr[s:e]) > ODD_RATIO:
            seg -= 1
        med = np.median(seg)
        if 2 ** med < 2500 and 2 ** (seg.max() + 1) <= 10000:
            seg += 1
        elif 2 ** seg.max() > 10000:
            seg -= 1
        lg[s:e] = seg
    return 2 ** lg


def speech_score(voice_db: np.ndarray) -> np.ndarray:
    """0-1 likelihood of speech (commentary, radio) per frame.

    Two cues on the 300-3400 Hz level at 20 frames/s:
      gaps    share of 50 ms frames in each second that fall well below that
              second's mean: speech pauses between syllables, an engine (or
              the engine bed under an onboard) does not. Clean engine ~0,
              commentary 0.4-0.6.
      rhythm  share of 3-8 Hz modulation over 1.6 s (syllable rate), which can
              still catch radio talking over a loud engine.
    """
    n = len(voice_db)
    if n < 32:
        return np.zeros(n, np.float32)
    lin = 10 ** (voice_db / 10)
    w = int(FPS)
    win = sliding_window_view(np.pad(lin, (w // 2, w - w // 2 - 1), mode="edge"), w)
    gaps = (win < 0.3 * win.mean(axis=1, keepdims=True)).mean(axis=1)
    gaps = np.clip((gaps - 0.1) / 0.25, 0, 1)

    m = 32
    env = voice_db - uniform_filter1d(voice_db, size=m)
    segs = sliding_window_view(np.pad(env, (m // 2, m - m // 2 - 1), mode="edge"), m)
    spec = np.abs(np.fft.rfft(segs * np.hanning(m), axis=1)) ** 2
    f = np.fft.rfftfreq(m, 1 / FPS)
    ratio = spec[:, (f >= 3) & (f <= 8)].sum(axis=1) / (spec[:, f >= 0.5].sum(axis=1) + 1e-9)
    # a flat envelope's leftover noise also has "3-8 Hz content": demand real depth
    depth = np.clip((segs.std(axis=1) - 1.5) / 2.0, 0, 1)
    rhythm = np.clip((ratio - 0.5) / 0.3, 0, 1) * depth
    return uniform_filter1d(np.maximum(gaps, rhythm), w).astype(np.float32)


def analyse(path: Path, octave_fix: bool) -> dict:
    f = frame_features(path)
    score = f.pop("score")
    oddr_all = f.pop("oddr")
    if len(score) < 10:
        raise ValueError("too short")
    norm = score / (score.max(axis=1, keepdims=True) + 1e-6)
    path_idx = viterbi(norm)
    rows = np.arange(len(score))
    best = score[rows, path_idx]
    med = np.median(score, axis=1) + 1e-3
    clarity = 10 * np.log10(best / med + 1e-6)          # dB above a typical candidate
    # other cars: a strong series not sharing harmonics with the tracked one
    # (octaves, 3:2 and 4:3 overlap a single engine's own harmonics)
    lr = np.log(CAND_RPM)
    dist = np.abs(lr[None, :] - lr[path_idx][:, None])
    related = np.min(np.abs(dist[..., None] - np.log([1, 2, 3, 4, 1.5, 4 / 3])[None, None, :]), axis=2) < 0.06
    other = np.where(related, -np.inf, score).max(axis=1)
    multi = np.clip((other / np.maximum(best, 1e-6) - 0.6) / 0.3, 0, 1)

    oddr = oddr_all[np.arange(len(path_idx)), path_idx].astype(np.float32)
    rpm_raw = unwrap_octaves(CAND_RPM[path_idx], clarity > CLEAR_DB, oddr)
    factor = 1.0
    good = clarity > CLEAR_DB
    if octave_fix and good.sum() > FPS * 20:
        r95 = np.percentile(rpm_raw[good], 95)
        factor = float(2.0 ** np.clip(np.round(np.log2(REDLINE * 0.97 / r95)), -1, 1))
    rpm = median_filter(rpm_raw * factor, size=3)
    wind = np.clip((f["low"] - 0.45) / 0.4, 0, 1) * np.clip(1 - clarity / (2 * CLEAR_DB), 0, 1)
    return {
        "rpm": rpm.astype(np.float32), "rpm_raw": rpm_raw.astype(np.float32),
        "clarity": clarity.astype(np.float32), "loud": f["loud"].astype(np.float32),
        "pan": f["pan"].astype(np.float32), "speech": speech_score(f["voice"]).astype(np.float32),
        "wind": wind.astype(np.float32), "multi": multi.astype(np.float32),
        "rpm_factor": factor,
    }


# ----------------------------------------------------------------- segments

def runs(mask: np.ndarray, min_frames: int):
    """(start, end) frame ranges where mask is True for at least min_frames."""
    d = np.diff(np.concatenate([[0], mask.astype(np.int8), [0]]))
    starts, ends = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
    return [(s, e) for s, e in zip(starts, ends) if e - s >= min_frames]


def find_segments(a: dict, video_type: str, duration_s: float) -> list[dict]:
    n = len(a["rpm"])
    sec = lambda x: int(round(x * FPS))
    loud = uniform_filter1d(a["loud"], sec(0.25))
    lr = np.log(np.maximum(a["rpm"], 1))
    slope = np.gradient(uniform_filter1d(lr, 5)) * FPS            # d ln(rpm) / s
    valid = a["clarity"] > CLEAR_DB
    ref = np.percentile(loud[valid], 70) if valid.any() else np.percentile(loud, 70)
    on = loud > ref - 6
    off = loud < ref - 9
    onboard = video_type in ("onboard", "onboard_bestof", "taxi", "trackview")
    segs = []

    def add(label, s, e, **extra):
        s, e = max(0, int(s)), min(n, int(e))
        if e - s < 2:
            return
        segs.append(dict(label=label, s=s, e=e, **extra))

    if onboard:
        for s, e in runs(on & valid & (slope > 0.15), sec(0.8)):
            add("full_throttle", s, e)
        for s, e in runs(on & valid & (np.abs(slope) < 0.08) & (a["rpm"] > 0.75 * REDLINE), sec(1.0)):
            add("steady_high", s, e)
        for s, e in runs(off & valid & (slope < -0.05), sec(0.6)):
            add("overrun", s, e)
        idle_runs = runs(valid & (a["rpm"] < 0.55 * REDLINE) & (np.abs(slope) < 0.1), sec(2.0))
        for s, e in idle_runs:
            add("idle", s, e)
        # gear changes: fast pitch jumps
        jump = np.concatenate([lr[3:] - lr[:-3], np.zeros(3)])      # change over 150 ms
        for label, sign, thr, ctx, pre, post in (("upshift", -1, 0.12, on, 0.6, 0.6),
                                                 ("downshift", 1, 0.08, off, 0.5, 0.7)):
            cand = np.flatnonzero(sign * jump > thr)
            last = -10 ** 9
            # strongest jump first; nothing within 0.5 s of an accepted one
            for t in cand[np.argsort(-sign * jump[cand])]:
                if abs(t - last) < sec(0.5) or any(abs(t - g["peak"]) < sec(0.5)
                                                   for g in segs if g["label"] == label):
                    continue
                if t > 0 and ctx[max(0, t - sec(0.5)):t].mean() > 0.5 and valid[t:t + 4].all():
                    add(label, t - sec(pre), t + sec(post), peak=t + 2)
                    last = t
        # idle/limiter straight into full throttle: race start or pit exit
        throttle_starts = [s for s, e in runs(on & valid & (slope > 0.15), sec(1.5))]
        first_launch = True
        for s, e in idle_runs:
            nxt = [t for t in throttle_starts if e - sec(0.3) <= t <= e + sec(0.5)]
            if not nxt:
                continue
            go = nxt[0]
            if first_launch and go < 0.15 * n and e - s >= sec(3):
                add("launch", go - sec(4), go + sec(7), peak=go)
                first_launch = False
            elif e - s >= sec(5):
                add("pit_exit", go - sec(6), go + sec(7), peak=go)
    else:
        # pass-bys: prominent loudness peak with a Doppler drop and a pan sweep
        sm = uniform_filter1d(a["loud"], sec(0.4))
        w = sec(2.0)
        for t in range(w, n - w):
            if sm[t] != sm[t - w:t + w].max():
                continue
            prom = sm[t] - max(sm[t - w:t].min(), sm[t:t + w].min())
            if prom < 8:
                continue
            before = np.median(lr[t - sec(1.0):t - sec(0.2)])
            after = np.median(lr[t + sec(0.2):t + sec(1.0)])
            drop = before - after
            if drop < 0.05 or not valid[t - sec(1.0):t + sec(1.0)].mean() > 0.5:
                continue
            p0 = a["pan"][t - sec(0.9):t - sec(0.4)].mean()
            p1 = a["pan"][t + sec(0.4):t + sec(0.9)].mean()
            direction = "rl" if p1 - p0 > 0.1 else "lr" if p0 - p1 > 0.1 else "mono"
            add("passby", t - w, t + w, peak=t, direction=direction, prominence=prom, doppler=drop)

    out = []
    for g in segs:
        s, e = g["s"], g["e"]
        sl = slice(s, e)
        speech, wind, multi = (float(a[k][sl].mean()) for k in ("speech", "wind", "multi"))
        clarity = float(a["clarity"][sl].mean())
        dur = (e - s) / FPS
        q = np.clip((clarity - CLEAR_DB) / 6, 0, 1) * (1 - speech) * (1 - 0.8 * wind) * (1 - 0.5 * multi)
        if g["label"] == "passby":
            q *= min(1.0, g["prominence"] / 15) * min(1.0, g["doppler"] / 0.12)
        elif g["label"] in ("full_throttle", "steady_high", "idle", "overrun"):
            q *= min(1.0, dur / {"idle": 6, "overrun": 1.5}.get(g["label"], 3))
        flags = [f for f, v in (("commentary", speech), ("wind", wind), ("other_cars", multi)) if v > 0.4]
        rpm = a["rpm"][sl]
        out.append({
            "label": g["label"], "start_s": round(s / FPS, 2), "end_s": round(e / FPS, 2),
            "peak_s": round(g["peak"] / FPS, 2) if "peak" in g else None,
            "direction": g.get("direction"),
            "rpm_start": float(np.median(rpm[:3])), "rpm_end": float(np.median(rpm[-3:])),
            "rpm_mean": float(rpm.mean()), "rpm_max": float(rpm.max()),
            "loud_db": float(a["loud"][sl].mean()), "clarity": clarity, "speech": speech,
            "wind": wind, "multi": multi, "flags": ",".join(flags) or None,
            "quality": round(float(q), 3),
        })
    return out


# ---------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="re-analyse everything")
    ap.add_argument("--resegment", action="store_true", help="re-cut segments from cached features")
    ap.add_argument("--only", nargs="*", help="video ids")
    args = ap.parse_args()

    db = connect()
    for s in SCHEMA:
        db.execute(s)
    if not db.execute("SELECT name FROM sqlite_master WHERE name='audio'").fetchone():
        raise SystemExit("nothing extracted yet; run extract.py first")
    have = {r["id"]: dict(r) for r in db.execute("SELECT * FROM analysis")}
    todo = db.execute("""SELECT a.id, a.path, v.video_type, v.duration_s, v.title
                         FROM audio a JOIN videos v ON v.id = a.id ORDER BY v.folder, v.idx""").fetchall()
    FEATURE_DIR.mkdir(parents=True, exist_ok=True)
    n_new = n_seg = 0
    for r in todo:
        if args.only and r["id"] not in args.only:
            continue
        path = Path(r["path"])
        if not path.exists():
            continue
        mtime = int(path.stat().st_mtime)
        cache = FEATURE_DIR / f"{r['id']}.npz"
        prev = have.get(r["id"])
        fresh = (prev and prev["version"] == VERSION and prev["audio_mtime"] == mtime
                 and cache.exists() and not args.force)
        if fresh and not args.resegment:
            continue
        t0 = dt.datetime.now()
        if fresh:
            a = dict(np.load(cache))
            a["rpm_factor"] = float(a["rpm_factor"])
        else:
            onboard = r["video_type"] in ("onboard", "onboard_bestof", "taxi", "trackview")
            try:
                a = analyse(path, octave_fix=onboard)
            except Exception as e:  # noqa: BLE001 - one bad file must not stop the batch
                print(f"FAILED {r['id']} {r['title']}: {e}")
                continue
            np.savez_compressed(cache, **a)
        segs = find_segments(a, r["video_type"], r["duration_s"] or 0)
        db.execute("DELETE FROM segments WHERE video_id=?", (r["id"],))
        for s in segs:
            sid = f"{r['id']}:{s['label']}:{int(s['start_s'] * 1000)}"
            db.execute("INSERT OR REPLACE INTO segments VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (sid, r["id"], s["label"], s["start_s"], s["end_s"], s["peak_s"], s["direction"],
                        s["rpm_start"], s["rpm_end"], s["rpm_mean"], s["rpm_max"], s["loud_db"],
                        s["clarity"], s["speech"], s["wind"], s["multi"], s["flags"], s["quality"], VERSION))
        db.execute("INSERT OR REPLACE INTO analysis VALUES (?,?,?,?,?,?,?,?,?)",
                   (r["id"], VERSION, str(path), mtime, len(a["rpm"]), a["rpm_factor"],
                    float(np.median(a["clarity"])), float((a["speech"] > 0.4).mean()),
                    dt.datetime.now().isoformat(timespec="seconds")))
        db.commit()
        n_new += 1
        n_seg += len(segs)
        labels = {}
        for s in segs:
            labels[s["label"]] = labels.get(s["label"], 0) + 1
        secs = (dt.datetime.now() - t0).total_seconds()
        print(f"{r['id']} {r['title'][:50]:<50} {secs:5.0f}s  "
              + " ".join(f"{k}:{v}" for k, v in sorted(labels.items())))
    print(f"{n_new} analysed, {n_seg} segments")
    return 0


if __name__ == "__main__":
    sys.exit(main())
