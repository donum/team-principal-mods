"""Stage 4c: ambience per track (wishlist E9, announced for the next game version).

The next game version reads an optional block per track in
ambience/session_layers.json, falling back to the pack-wide layers:

    "tracks": {"norisring": {"crowd": {"file": "...", "gain": 0.9},
                             "pa": {"file": "..."}}}

The developer named "crowd" and "pa" (2026-11-16). We also write "cars"
(the track bed) in case every layer works; check the next modding guide.

Two steps, as for the starts, pit sets and 2018 pass-bys: candidates to
pick by ear, then the picks are built.

  --candidates   per venue, pilot/track_ambience/<venue>/:
                   cars_NN_*.wav   trackside shots (spectator videos of the
                                   set's recording years, no starts or pit
                                   lanes), looser filters than ambience.py;
                   crowd_NN_*.wav  15 s stretches with crowd and no engines
                                   (any year: a crowd has no car in it);
                   pa_NN_*.wav     announcer stretches of announcer.py's
                                   index (kind pa or unsure) at that venue;
                 and candidates.md listing every one with its source.
  (no option)    builds TRACK_PICKS, plus a cars bed for every venue with
                 at least AUTO_BED_MIN_S of shots ambience.py would take,
                 into library/ambience/tracks/<venue>_{cars_on_track,crowd,pa}.ogg.
                 package.py adds them to the overlay ("track_set"), applied
                 only when local.json "game_audio_features" lists
                 "track_ambience".

Venues without a pick keep the pack-wide layer. Nothing is synthesised.

    python tools/engine_audio/track_ambience.py --candidates
    python tools/engine_audio/track_ambience.py
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import uniform_filter1d

import ambience
from common import (DATA, ERA, FEATURE_DIR, OVERLAY_ID, SET_LIBRARY_DIR, connect, decode, dump_json, era_reason,
                    slug, write_wav)

SR = 44100
FPS = ambience.FPS

# Catalog venue -> the game's track ids in the packs of this base (2012,
# 2013, 2018 use the same ids; the 2018 GP layouts get the same sound).
VENUES = {
    "Hockenheim": ["hockenheim13"],
    "Brands Hatch": ["brandshatch", "brandshatch_gp"],
    "Spielberg": ["redbullring"],
    "Lausitzring": ["lausitzring", "lausitzring_gp"],
    "Norisring": ["norisring"],
    "Moscow": ["moscow"],
    "Nurburgring": ["nuerburgring13"],
    "Oschersleben": ["oschersleben"],
    "Zandvoort": ["zandvoort"],
}

# Picked by ear from pilot/track_ambience/ (per sound set):
#   "cars":  [(video id, from s, to s, what it is), ...]  -> a bed loop
#   "crowd": (video id, from s, to s, what it is)          -> a crowd loop
#   "pa":    (video id, from s, to s, what it is)          -> played as is
TRACK_PICKS: dict[str, dict[str, dict]] = {
    "dtm-era4": {},
}

AUTO_BED_MIN_S = 120.0     # venues with this much clean shot time get a bed without picks
BED_MAX_S = 240.0          # per-track beds: shorter than the pack-wide 393 s
OUT_DIR = SET_LIBRARY_DIR / "ambience" / "tracks"
PILOT = DATA / "pilot" / "track_ambience"
ANNOUNCER = DATA / "pilot" / "track_announcer" / "index.csv"
NOT_TRACK = ambience.NOT_BED.pattern + r"|boxengasse|pit|stop"
CROWD_S = 15.0
LOOSE = dict(speech=0.25, engine=0.15, dr=6.0, min_s=6.0)


# --------------------------------------------------------------- candidates

def venue_rows(db, venue: str, any_year: bool = False):
    rows = db.execute("""SELECT v.id, v.title, v.video_type, a.path FROM videos v JOIN audio a ON a.id = v.id
                         WHERE v.video_type = 'spectator' AND v.status = 'done' AND v.track = ?""",
                      (venue,)).fetchall()
    return [r for r in rows if (FEATURE_DIR / f"{r['id']}.npz").exists() and Path(r["path"]).exists()
            and (any_year or not era_reason(r["id"], r["title"]))]


def loose_shots(row) -> list[dict]:
    """ambience.shots_of with looser limits: fan montages of the smaller
    venues hold short shots and some talking."""
    feat = np.load(FEATURE_DIR / f"{row['id']}.npz")
    B = ambience.band_frames(Path(row["path"]))
    n = min(len(B), len(feat["speech"]))
    bounds = [0] + ambience.find_cuts(B[:n]) + [n]
    trim = int(ambience.TRIM_S * FPS)
    out = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        a, b = a + trim, b - trim
        if (b - a) / FPS < LOOSE["min_s"]:
            continue
        sl = slice(a, b)
        speech = float(feat["speech"][sl].mean())
        engine = float((feat["clarity"][sl] > 3).mean())
        lvl = uniform_filter1d(feat["loud"][sl], 10)
        dr = float(np.percentile(lvl, 95) - np.percentile(lvl, 10))
        if speech > LOOSE["speech"] or engine < LOOSE["engine"] or dr < LOOSE["dr"]:
            continue
        out.append(dict(video_id=row["id"], title=row["title"], path=row["path"], start_s=a / FPS, end_s=b / FPS,
                        score=round(engine * 2 + dr / 10 - speech * 3, 2),
                        note=f"engine {engine:.2f}, speech {speech:.2f}, swing {dr:.0f} dB"))
    return out


def crowd_windows(row, n: int = 3) -> list[dict]:
    """Stretches of CROWD_S with no engine and a steady, busy level: the
    grandstand between sessions or before the start."""
    feat = np.load(FEATURE_DIR / f"{row['id']}.npz")
    w = int(CROWD_S * FPS)
    if len(feat["loud"]) < w:
        return []
    engine = uniform_filter1d((feat["clarity"] > 3).astype(float), w)
    wind = uniform_filter1d(feat["wind"].astype(float), w)
    loud = uniform_filter1d(feat["loud"], w)
    speech = uniform_filter1d(feat["speech"].astype(float), w)
    ok = (engine < 0.05) & (wind < 0.2)
    score = np.where(ok, loud - 10 * np.abs(speech - 0.4), -np.inf)   # some voices, not one talker
    out = []
    for _ in range(n):
        i = int(np.argmax(score))
        if not np.isfinite(score[i]):
            break
        a = max(0, i - w // 2)
        out.append(dict(video_id=row["id"], title=row["title"], path=row["path"], start_s=a / FPS,
                        end_s=a / FPS + CROWD_S, score=round(float(score[i]), 1),
                        note=f"engine {engine[i]:.2f}, speech {speech[i]:.2f}"))
        score[max(0, i - 2 * w):i + 2 * w] = -np.inf
    return out


def pa_stretches(venue: str) -> list[dict]:
    if not ANNOUNCER.exists():
        return []
    db = connect()
    out = []
    for r in csv.DictReader(ANNOUNCER.open(encoding="utf-8-sig")):
        if r["track"] != venue or r["kind"] not in ("pa", "unsure"):
            continue
        row = db.execute("SELECT path FROM audio WHERE id=?", (r["video_id"],)).fetchone()
        if not row:
            continue
        out.append(dict(video_id=r["video_id"], title=r["title"], path=row["path"], start_s=float(r["start_s"]),
                        end_s=float(r["end_s"]), score=float(r["quality"]),
                        note=f"{r['kind']}, {r['year']}, {r['language']}: {r['text'][:120]}"))
    return out


def write_candidates(db) -> None:
    lines = ["# Track ambience candidates", "",
             f"Set {OVERLAY_ID}, cars of {', '.join(map(str, ERA))}. Pick by ear, then fill "
             "`track_ambience.TRACK_PICKS` with (video id, from, to, note).", ""]
    for venue in VENUES:
        out = PILOT / slug(venue).lower()
        out.mkdir(parents=True, exist_ok=True)
        for f in out.glob("*.wav"):
            f.unlink()
        cars = []
        for r in venue_rows(db, venue):
            if not re.search(NOT_TRACK, r["title"], re.I):
                cars += loose_shots(r)
        crowd = [c for r in venue_rows(db, venue, any_year=True) for c in crowd_windows(r)]
        groups = {"cars": sorted(cars, key=lambda c: -c["score"])[:8],
                  "crowd": sorted(crowd, key=lambda c: -c["score"])[:6],
                  "pa": pa_stretches(venue)}
        lines += [f"## {venue} ({', '.join(VENUES[venue])})", ""]
        for kind, rows in groups.items():
            if not rows:
                lines.append(f"- **{kind}:** nothing found")
                continue
            for i, c in enumerate(rows, 1):
                dur = min(c["end_s"] - c["start_s"], 30.0)
                name = f"{kind}_{i:02d}_{c['video_id']}_{c['start_s']:.0f}s.wav"
                write_wav(out / name, decode(Path(c["path"]), c["start_s"], dur, SR, 2), SR)
                lines.append(f"- **{kind} {i:02d}** `{name}`: `(\"{c['video_id']}\", {c['start_s']:.1f}, "
                             f"{c['end_s']:.1f})` {c['title'][:60]}; {c['note']}")
        lines.append("")
        print(f"{venue:13} cars {len(groups['cars'])}, crowd {len(groups['crowd'])}, pa {len(groups['pa'])}")
    (PILOT / "candidates.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"-> {PILOT}")


# -------------------------------------------------------------------- build

def loop_of(x: np.ndarray, xf_s: float = 1.5) -> np.ndarray:
    xf = int(xf_s * SR)
    loop = x[:len(x) - xf].copy()
    w = np.linspace(0, 1, xf)[:, None]
    loop[:xf] = x[-xf:] * (1 - w) + x[:xf] * w
    return loop


def norm(x: np.ndarray) -> np.ndarray:
    return x * 10 ** (-1 / 20) / (np.abs(x).max() + 1e-9)


def auto_shots(db, venue: str) -> list[dict]:
    shots = []
    for r in venue_rows(db, venue):
        if not ambience.NOT_BED.search(r["title"]):
            shots += ambience.shots_of(r, Path(r["path"]))
    return shots


def build(db) -> dict:
    picks = TRACK_PICKS.get(OVERLAY_ID, {})
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for f in OUT_DIR.glob("*.ogg"):
        f.unlink()
    made = {}
    for venue in VENUES:
        p = picks.get(venue, {})
        name = slug(venue).lower()
        got = {}
        shots = ambience.picked_shots(db, p["cars"]) if p.get("cars") else auto_shots(db, venue)
        total = sum(min(s["end_s"] - s["start_s"], ambience.MAX_SHOT_S) - ambience.XF_S for s in shots)
        if shots and (p.get("cars") or total >= AUTO_BED_MIN_S):
            seconds = min(BED_MAX_S, 0.8 * total)
            bed, used = ambience.build_bed(shots, seconds, np.random.default_rng(1))
            write_wav(OUT_DIR / f"{name}_cars_on_track.ogg", norm(bed), SR)
            got["cars"] = dict(seconds=round(seconds), shots=used, picked=bool(p.get("cars")))
        for layer in ("crowd", "pa"):
            if layer not in p:
                continue
            vid, a, b, note = p[layer]
            row = db.execute("SELECT path FROM audio WHERE id=?", (vid,)).fetchone()
            if not row:
                print(f"{venue} {layer}: {vid} not extracted")
                continue
            x = decode(Path(row["path"]), a, b - a, SR, 2)
            x = loop_of(x) if layer == "crowd" else ambience_fades(x)
            write_wav(OUT_DIR / f"{name}_{layer}.ogg", norm(x), SR)
            got[layer] = dict(video_id=vid, start_s=a, end_s=b, note=note)
        made[venue] = got
        print(f"{venue:13} " + (", ".join(f"{k} ({'picked' if k != 'cars' or v['picked'] else 'auto'})"
                                         for k, v in got.items()) or "pack-wide layers"))
    dump_json(OUT_DIR / "tracks.json", {"venues": VENUES, "made": made})
    return made


def ambience_fades(x: np.ndarray, s: float = 0.3) -> np.ndarray:
    n = min(int(s * SR), len(x) // 2)
    x = x.copy()
    x[:n] *= np.linspace(0, 1, n)[:, None]
    x[-n:] *= np.linspace(1, 0, n)[:, None]
    return x


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--candidates", action="store_true", help="write listening candidates per venue")
    args = ap.parse_args()
    db = connect()
    if args.candidates:
        write_candidates(db)
    else:
        build(db)
    return 0


if __name__ == "__main__":
    sys.exit(main())
