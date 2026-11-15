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

from common import LIBRARY_DIR, OVERLAY_ID, SET_LIBRARY_DIR, connect, decode, dump_json, load_json, write_wav

SR = 44100
OUT_DIR = SET_LIBRARY_DIR / "pits"
GAME_BOOST_MAX = 5.0          # race_engines.json pit_departure_gain
GAME_PEAK = 31128.65 / 32768  # the game boosts up to this peak
CROSSFADE_S = 0.65            # race_engines.json pit_fireup_crossfade_s
FADE_IN_S = {"fireup": 0.05, "exit": 0.4, "wheelguns": 0.03}
FADE_OUT_S = {"fireup": 0.05, "exit": 2.0, "wheelguns": 0.15}

# One dict per set: fireup / exit / wheelguns = (video id, from s, to s) or
# None; note says what it is. Times are seconds in the video.
# `exit_unconfirmed` marks an exit not yet confirmed by ear (package.py adds
# "UNCONFIRMED" to its source, which the mod browser shows).
# Exits (2026-11-07): "DTM Sound 1" (EMSlNAM8zC0, Don Blech, June 2013,
# probably the Lausitzring pit lane): 2013 cars wait by the camera, then pull
# away down the pit lane, no commentary. Picked from 15 departures by the
# frames and the level (waiting, a rise as the car leaves, 3-6 dB down as it
# goes); cut so the pull-away lands 5 s in (stock: 4.4-5.8 s). Not yet heard
# by the user. Before them, six Oschersleben 2013 cuts were the exits; by ear
# four were drive-bys and one a pit entry (FAN_CLIPS below), and the sixth,
# probably an exit, is in FAN_CLIPS too. Wheelguns: spectators at the 2013
# Brands Hatch pit-stop practice, the strongest flat broadband bursts of
# `pits.py --scan`, checked on the spectrogram and frames.
EXIT_VIDEO = "EMSlNAM8zC0"
PITS_ERA4: list[dict] = [
    dict(exit=(EXIT_VIDEO, 16.3, 29.3), exit_unconfirmed=True, wheelguns=("gpLEQ52Q4F4", 12.7, 15.3),
         note="2013 pit lane, Audi Red Bull pulls away; Audi Phoenix stop, Brands Hatch practice"),
    dict(exit=(EXIT_VIDEO, 146.3, 159.3), exit_unconfirmed=True, wheelguns=("1K5GsYD9vmI", 2.1, 5.7),
         note="2013 pit lane, Mercedes Thomas Sabo pulls away; BMW stop, Brands Hatch practice"),
    dict(exit=(EXIT_VIDEO, 120.2, 133.2), exit_unconfirmed=True, wheelguns=("Yy28JpRzFD0", 13.1, 15.6),
         note="2013 pit lane, Audi ultra pulls away; Audi stop, Brands Hatch practice"),
    dict(exit=(EXIT_VIDEO, 174.1, 187.1), exit_unconfirmed=True, wheelguns=("H64vMO6NpuY", 0.3, 3.4),
         note="2013 pit lane, Mercedes Euronics pulls away; BMW Schnitzer stop (Priaulx car), Brands Hatch practice"),
    dict(exit=(EXIT_VIDEO, 194.7, 207.7), exit_unconfirmed=True, wheelguns=("gpLEQ52Q4F4", 119.8, 122.3),
         note="2013 pit lane, orange Mercedes pulls away; Audi Phoenix stop, Brands Hatch practice"),
    dict(exit=(EXIT_VIDEO, 226.1, 239.1), exit_unconfirmed=True, wheelguns=("gpLEQ52Q4F4", 31.3, 33.4),
         note="2013 pit lane, silver AMG Mercedes pulls away; Audi Phoenix stop, Brands Hatch practice"),
    # 2026-11-07, user's second batch: a real 2013 race stop at the Lausitzring
    # (DPFz3gE17zQ, Mercedes, filmed close: four bursts 13-24 s, flatness up
    # to 0.5) and one more Brands Hatch BMW practice burst (HF-w0SiCD-Y).
    dict(exit=(EXIT_VIDEO, 31.5, 44.5), exit_unconfirmed=True, wheelguns=("DPFz3gE17zQ", 13.1, 15.4),
         note="2013 pit lane, Audi Schaeffler pulls away; Mercedes race stop, Lausitzring 2013"),
    dict(exit=(EXIT_VIDEO, 210.5, 223.5), exit_unconfirmed=True, wheelguns=("DPFz3gE17zQ", 15.9, 18.1),
         note="2013 pit lane, red-white Mercedes pulls away; Mercedes race stop, Lausitzring 2013"),
    dict(exit=(EXIT_VIDEO, 92.5, 105.5), exit_unconfirmed=True, wheelguns=("DPFz3gE17zQ", 21.2, 24.3),
         note="2013 pit lane, Mercedes VfB pulls away; Mercedes race stop, Lausitzring 2013"),
    dict(exit=(EXIT_VIDEO, 63.5, 76.5), exit_unconfirmed=True, wheelguns=("HF-w0SiCD-Y", 32.9, 35.0),
         note="2013 pit lane, dark red Mercedes pulls away; BMW stop, Brands Hatch practice"),
]

# 2018 set (2017-2018 cars), picked by ear 2026-11-15 from
# pilot/pit_candidates_2018: Misano 2018 pit-exit practice starts
# (1_f68-hUy8w), a car standing at the line and pulling away. Each clip
# ends at the camera cut or where the car has gone (ffmpeg scene cuts at
# 118.1, 311.9, 357.4 s), with a longer fade-in than the 2013 exits (the
# first cut started on a loud stretch). No wheelguns: the era's 2013 sets keep
# theirs. exit_fade_in / exit_fade_out override FADE_IN_S / FADE_OUT_S.
PITS_2018: list[dict] = [
    dict(exit=("1_f68-hUy8w", 104.0, 117.6), exit_fade_in=1.5, note="Misano 2018 practice start at the pit exit (fence)"),
    dict(exit=("1_f68-hUy8w", 113.85, 126.85), exit_fade_in=0.8, note="Misano 2018, BMW pulls away behind the fence"),
    dict(exit=("1_f68-hUy8w", 294.0, 311.7), exit_fade_in=1.0, exit_fade_out=1.5,
         note="Misano 2018, Audi (Castrol) pulls away, to the camera cut"),
    dict(exit=("1_f68-hUy8w", 317.0, 336.8), exit_fade_in=1.0, note="Misano 2018, blue Audi pulls away"),
    dict(exit=("1_f68-hUy8w", 332.0, 345.0), exit_fade_in=1.0, note="Misano 2018, black Audi pulls away"),
]
PITS = {"dtm-era4": PITS_ERA4, "dtm-2018": PITS_2018}.get(OVERLAY_ID, [])

# Fan clips that are not pit exits, set aside from the pack (by ear,
# 2026-11-07; old pit_exit_NN in brackets). Real drive-bys whose make is not
# known can't be tagged per supplier (README "Real pass-bys"), and the game
# has no pit-entry slot (wishlist E14), so they are previews only:
# library/fan_clips/<kind>_NN_<video id>.wav.
FAN_CLIPS: list[dict] = [
    dict(kind="passby", clip=("nUfRLnhcaKc", 5.5, 18.5), note="Oschersleben 2013 drive-by [old pit_exit_01]"),
    dict(kind="passby", clip=("UD-N3wMEJWg", 23.3, 34.0), note="Oschersleben 2013 drive-by [old pit_exit_02]"),
    dict(kind="passby", clip=("nUfRLnhcaKc", 15.0, 28.0), note="Oschersleben 2013 drive-by [old pit_exit_04]"),
    dict(kind="passby", clip=("UD-N3wMEJWg", 3.2, 16.2), note="Oschersleben 2013 drive-by [old pit_exit_06]"),
    dict(kind="pit_entry", clip=("UD-N3wMEJWg", 62.5, 75.5), note="Oschersleben 2013 pit entry [old pit_exit_03]"),
    dict(kind="pit_entry", clip=("DPFz3gE17zQ", 0.0, 12.9),
         note="Lausitzring 2013 race stop: the Mercedes rolls in on the pit limiter and stops"),
    dict(kind="pit_exit", clip=("UD-N3wMEJWg", 44.5, 57.5),
         note="Oschersleben 2013, probably a pit exit (user not sure) [old pit_exit_05]"),
]
FAN_DIR = LIBRARY_DIR / "fan_clips"


def game_boost(x: np.ndarray) -> float:
    """What the game multiplies a pit clip by before its gain."""
    return float(min(GAME_BOOST_MAX, GAME_PEAK / (np.abs(x).max() + 1e-9)))


def heard_db(x: np.ndarray, gain: float = 1.0) -> float:
    """RMS level as the game plays the clip: its boost, then the gain."""
    y = x * game_boost(x) * gain
    return float(10 * np.log10(np.mean(np.square(y, dtype=np.float64)) + 1e-12))


def fade(x: np.ndarray, kind: str, fade_in: float | None = None, fade_out: float | None = None) -> np.ndarray:
    x = x.copy()
    a = int((FADE_IN_S[kind] if fade_in is None else fade_in) * SR)
    b = int((FADE_OUT_S[kind] if fade_out is None else fade_out) * SR)
    if a:
        x[:a] *= np.linspace(0, 1, a, dtype=np.float32)[:, None]
    if b:
        x[-b:] *= np.cos(np.linspace(0, np.pi / 2, b, dtype=np.float32))[:, None]
    return x


def audio_path(db, vid: str) -> Path | None:
    row = db.execute("SELECT path FROM audio WHERE id=?", (vid,)).fetchone()
    return Path(row[0]) if row and Path(row[0]).exists() else None


def cut(db, spec, kind: str, fade_in: float | None = None, fade_out: float | None = None) -> np.ndarray | None:
    if not spec:
        return None
    vid, a, b = spec
    path = audio_path(db, vid)
    if not path:
        return None
    x = decode(path, a, b - a, SR, 2)
    return fade(x / (np.abs(x).max() + 1e-9) * 10 ** (-1 / 20), kind, fade_in, fade_out)


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
        clips = {k: cut(db, s.get(k), k, s.get(f"{k}_fade_in"), s.get(f"{k}_fade_out"))
                 for k in ("fireup", "exit", "wheelguns")}
        if clips["exit"] is None:
            continue
        out.append(dict(note=s["note"], sources={k: s.get(k) for k in clips},
                        exit_unconfirmed=bool(s.get("exit_unconfirmed")), **clips))
    return out


def write_fan_clips(db) -> list[dict]:
    """FAN_CLIPS as previews in library/fan_clips (not in the pack)."""
    FAN_DIR.mkdir(parents=True, exist_ok=True)
    for old in FAN_DIR.glob("*.wav"):
        old.unlink()
    meta, n = [], {}
    for c in FAN_CLIPS:
        x = cut(db, c["clip"], "exit")
        if x is None:
            continue
        n[c["kind"]] = n.get(c["kind"], 0) + 1
        name = f"{c['kind']}_{n[c['kind']]:02d}_{c['clip'][0]}.wav"
        write_wav(FAN_DIR / name, x, SR)
        meta.append(dict(c, file=name))
    dump_json(FAN_DIR / "fan_clips.json", meta)
    return meta


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
        meta.append(dict(note=s["note"], sources=s["sources"], exit_unconfirmed=s["exit_unconfirmed"]))
        print(f"pit set {i}: " + ", ".join(f"{k} {len(s[k]) / SR:.1f}s" for k in ("fireup", "exit", "wheelguns")
                                            if s[k] is not None) + f"  ({s['note']})")
    dump_json(OUT_DIR / "pits.json", meta)
    for c in write_fan_clips(connect()):
        print(f"fan clip {c['file']}  ({c['note']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
