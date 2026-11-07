"""Stage 4d: real pit-lane sets (fire-up, exit, wheelguns) from fan recordings.

How the game plays them (ui/audio_manager.py, ui/pit_exit_audio.py):
  - The three banks are paired by number: set NN is pit_fireup_NN,
    pit_exit_NN and pit_wheelguns_NN. A set is drawn from a shuffled bag of
    the pit_exit_NN keys, so every set needs an exit; the fire-up and the
    wheelguns are optional (a set without one plays none).
  - Practice and qualifying (a car leaving its garage): the fire-up is
    crossfaded into the exit over `pit_fireup_crossfade_s` (0.65 s) and
    played once as one "departure" clip. The fire-up is scaled by
    fireup_gain / exit_gain first.
  - Race: the wheelguns play when the service starts; on release they fade
    out over 0.65 s while the exit fades in over 0.65 s. No fire-up (the
    engine keeps running).
  - Level: each clip (and the joined departure) is boosted by
    min(pit_departure_gain = 5, 0.95 full scale / its peak), then played at
    the clip's `gain`. Stock clips peak 15-35 dB under full scale, so the
    game plays them about 14 dB louder than the files are.
  - `peak_s` (the exit's loudest moment) times the duck of the pass-by mix.

Stock shapes, copied here: fire-up 4 s with ~1.7 s of quiet before the
engine catches; exit ~13 s, the car rolling down the pit lane, passing
~5 s in and accelerating away; wheelguns 2-2.5 s of bursts.

The sets are listed by hand (PITS) after looking at each video's
spectrogram and frames, like starts.py. Each clip is a (video id, from, to)
stretch of a recording, cut as it is: no synthesis, no level automation,
just short edge fades.

    python tools/engine_audio/pits.py        # previews in private/.../library/pits
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from common import LIBRARY_DIR, connect, decode, dump_json, load_json, write_wav

SR = 44100
OUT_DIR = LIBRARY_DIR / "pits"
GAME_BOOST_MAX = 5.0          # race_engines.json pit_departure_gain
GAME_PEAK = 31128.65 / 32768  # the game boosts up to this peak
CROSSFADE_S = 0.65            # race_engines.json pit_fireup_crossfade_s
FADE_IN_S = {"fireup": 0.05, "exit": 0.4, "wheelguns": 0.03}
FADE_OUT_S = {"fireup": 0.05, "exit": 2.0, "wheelguns": 0.15}

# One dict per set: fireup / exit / wheelguns = (video id, from s, to s) or
# None; note says what it is. Times are seconds in the video.
# Exits: Oschersleben 2013, filmed at the fence of the pit-exit lane (quiet,
# no commentary): each car holds the pit limiter (steady harmonics), passes
# with a Doppler drop and pulls away, like the stock exits; cut so the pass
# lands ~5 s in. Wheelguns: spectators at the 2013 Brands Hatch pit-stop
# practice, the strongest flat broadband bursts of `pits.py --scan`
# (2026-11-07), checked on the spectrogram and frames.
PITS: list[dict] = [
    dict(exit=("nUfRLnhcaKc", 5.5, 18.5), wheelguns=("gpLEQ52Q4F4", 12.7, 15.3),
         note="Oschersleben 2013 pit exit; Audi Phoenix stop, Brands Hatch practice"),
    dict(exit=("UD-N3wMEJWg", 23.3, 34.0), wheelguns=("1K5GsYD9vmI", 2.1, 5.7),
         note="Oschersleben 2013 pit exit; BMW stop, Brands Hatch practice"),
    dict(exit=("UD-N3wMEJWg", 62.5, 75.5), wheelguns=("Yy28JpRzFD0", 13.1, 15.6),
         note="Oschersleben 2013 pit exit; Audi stop, Brands Hatch practice"),
    dict(exit=("nUfRLnhcaKc", 15.0, 28.0), wheelguns=("H64vMO6NpuY", 0.3, 3.4),
         note="Oschersleben 2013 pit exit; BMW Schnitzer stop (Priaulx car), Brands Hatch practice"),
    dict(exit=("UD-N3wMEJWg", 44.5, 57.5), wheelguns=("gpLEQ52Q4F4", 119.8, 122.3),
         note="Oschersleben 2013 pit exit; Audi Phoenix stop, Brands Hatch practice"),
    dict(exit=("UD-N3wMEJWg", 3.2, 16.2), wheelguns=("gpLEQ52Q4F4", 31.3, 33.4),
         note="Oschersleben 2013 pit exit; Audi Phoenix stop, Brands Hatch practice"),
]


def game_boost(x: np.ndarray) -> float:
    """What the game multiplies a pit clip by before its gain."""
    return float(min(GAME_BOOST_MAX, GAME_PEAK / (np.abs(x).max() + 1e-9)))


def heard_db(x: np.ndarray, gain: float = 1.0) -> float:
    """RMS level as the game plays the clip: its boost, then the gain."""
    y = x * game_boost(x) * gain
    return float(10 * np.log10(np.mean(np.square(y, dtype=np.float64)) + 1e-12))


def fade(x: np.ndarray, kind: str) -> np.ndarray:
    x = x.copy()
    a, b = int(FADE_IN_S[kind] * SR), int(FADE_OUT_S[kind] * SR)
    if a:
        x[:a] *= np.linspace(0, 1, a, dtype=np.float32)[:, None]
    if b:
        x[-b:] *= np.cos(np.linspace(0, np.pi / 2, b, dtype=np.float32))[:, None]
    return x


def audio_path(db, vid: str) -> Path | None:
    row = db.execute("SELECT path FROM audio WHERE id=?", (vid,)).fetchone()
    return Path(row[0]) if row and Path(row[0]).exists() else None


def cut(db, spec, kind: str) -> np.ndarray | None:
    if not spec:
        return None
    vid, a, b = spec
    path = audio_path(db, vid)
    if not path:
        return None
    x = decode(path, a, b - a, SR, 2)
    return fade(x / (np.abs(x).max() + 1e-9) * 10 ** (-1 / 20), kind)


def departure(fireup: np.ndarray, exit_: np.ndarray, scale: float = 1.0) -> np.ndarray:
    """The game's practice/qualifying departure: fire-up crossfaded (linear,
    CROSSFADE_S) into the exit."""
    n = min(int(CROSSFADE_S * SR), len(fireup), len(exit_))
    w = np.linspace(0, 1, n, dtype=np.float32)[:, None]
    lead = fireup * scale
    return np.concatenate([lead[:-n], lead[-n:] * (1 - w) + exit_[:n] * w, exit_[n:]])


def real_pits(db) -> list[dict]:
    out = []
    for s in PITS:
        clips = {k: cut(db, s.get(k), k) for k in ("fireup", "exit", "wheelguns")}
        if clips["exit"] is None:
            continue
        out.append(dict(note=s["note"], sources={k: s.get(k) for k in clips}, **clips))
    return out


CAND_DIR = LIBRARY_DIR.parent / "pilot" / "pit_candidates"
HOP_S = 0.02


def _frames(x: np.ndarray):
    """Level (dB) and spectral flatness 1-10 kHz per HOP_S frame."""
    m = x.mean(axis=1)
    h = int(HOP_S * SR)
    n = len(m) // h - 2
    win = np.hanning(2 * h)
    f = np.fft.rfftfreq(2 * h, 1 / SR)
    band = (f >= 1000) & (f <= 10000)
    lvl, flat = np.empty(n), np.empty(n)
    for i in range(n):
        seg = m[i * h:i * h + 2 * h]
        P = np.abs(np.fft.rfft(seg * win)) ** 2 + 1e-12
        lvl[i] = 10 * np.log10(P.sum())
        pb = P[band]
        flat[i] = np.exp(np.mean(np.log(pb))) / np.mean(pb)
    return lvl, flat


def scan(db, vid: str) -> list[dict]:
    """Candidate moments in one recording.

    wheelguns: 0.25-2.5 s where the level stands >= 9 dB over the median of
    the 6 s around it and the 1-10 kHz spectrum is flat (impact-wrench
    rattle, not an engine's harmonics); bursts closer than 1.2 s are one
    cluster. fireup: a jump of >= 12 dB from >= 1.5 s of quiet that holds
    for >= 1 s (an engine catching). Each candidate keeps its score; nothing
    here decides what goes in the pack."""
    path = audio_path(db, vid)
    if not path:
        return []
    x = decode(path, 0, None, SR, 2)
    lvl, flat = _frames(x)
    k = int(3.0 / HOP_S)
    base = np.array([np.median(lvl[max(0, i - k):i + k]) for i in range(0, len(lvl), 10)]).repeat(10)[:len(lvl)]
    hot = (lvl - base >= 9) & (flat >= 0.25)
    out, i = [], 0
    while i < len(hot):
        if not hot[i]:
            i += 1
            continue
        j = i
        while j < len(hot) and (hot[j] or hot[j:j + int(1.2 / HOP_S)].any()):
            j += 1
        dur = (j - i) * HOP_S
        if 0.25 <= dur <= 2.5 * 3:
            out.append(dict(kind="wheelguns", t=round(i * HOP_S, 2), dur=round(dur, 2),
                            score=round(float((lvl[i:j] - base[i:j]).mean() * flat[i:j].mean()), 2)))
        i = j
    q, hold = int(1.5 / HOP_S), int(1.0 / HOP_S)
    i = q
    while i < len(lvl) - hold:
        before = np.median(lvl[i - q:i])
        after = np.median(lvl[i:i + hold])
        if after - before >= 12 and lvl[i - q:i].max() < before + 6:
            out.append(dict(kind="fireup", t=round(i * HOP_S, 2), dur=1.0,
                            score=round(float(after - before), 2)))
            i += hold * 3
        else:
            i += 1
    return out


def cut_candidates(db, vids: list[str]) -> list[dict]:
    """Write every scan hit as a WAV (wheelguns: 0.3 s before to 0.5 s
    after the cluster; fire-ups: 1.7 s before to 2.3 s after, the stock
    shape) to pilot/pit_candidates, best first per video."""
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    index = CAND_DIR / "candidates.json"
    rows = [r for r in (load_json(index, []) or []) if r["video_id"] not in vids]
    for vid in vids:
        path = audio_path(db, vid)
        if not path:
            continue
        for old in CAND_DIR.glob(f"*_{vid}_*.wav"):
            old.unlink()
        for c in sorted(scan(db, vid), key=lambda c: -c["score"])[:12]:
            a = max(0.0, c["t"] - (0.3 if c["kind"] == "wheelguns" else 1.7))
            b = c["t"] + c["dur"] + (0.5 if c["kind"] == "wheelguns" else 2.3)
            x = decode(path, a, b - a, SR, 2)
            x = fade(x / (np.abs(x).max() + 1e-9) * 10 ** (-1 / 20), c["kind"])
            name = f"{c['kind']}_{vid}_{c['t']:07.2f}s.wav"
            write_wav(CAND_DIR / name, x, SR)
            rows.append(dict(c, video_id=vid, file=name, start_s=round(a, 2), end_s=round(b, 2)))
    dump_json(index, rows)
    return [r for r in rows if r["video_id"] in vids]


def main() -> int:
    if len(sys.argv) > 2 and sys.argv[1] == "--scan":
        for r in cut_candidates(connect(), sys.argv[2:]):
            print(f"{r['kind']:9s} {r['video_id']} {r['start_s']:8.2f}-{r['end_s']:8.2f}s score {r['score']}")
        return 0
    sets = real_pits(connect())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("pit_*.wav"):
        old.unlink()
    meta = []
    for i, s in enumerate(sets, 1):
        for k in ("fireup", "exit", "wheelguns"):
            if s[k] is not None:
                write_wav(OUT_DIR / f"pit_{i:02d}_{k}.wav", s[k], SR)
        if s["fireup"] is not None:
            write_wav(OUT_DIR / f"pit_{i:02d}_departure.wav", departure(s["fireup"], s["exit"]), SR)
        meta.append(dict(note=s["note"], sources=s["sources"]))
        print(f"pit set {i}: " + ", ".join(f"{k} {len(s[k]) / SR:.1f}s" for k in ("fireup", "exit", "wheelguns")
                                            if s[k] is not None) + f"  ({s['note']})")
    dump_json(OUT_DIR / "pits.json", meta)
    return 0


if __name__ == "__main__":
    sys.exit(main())
