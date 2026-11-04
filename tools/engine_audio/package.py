"""Stage 5: turn the best segments into a game sound overlay (swappable target).

Target "team_principal" (Team Principal: A Racing Manager), per the game's
assets/audio/README_AUDIO.txt:
  session/  pass-bys: 4 s, 44.1 kHz stereo WAV, an RL file and an _lr mirror,
            crossing_s = centre of the loudest 80 ms. One key per make,
            tagged on the supplier through engines.json "passby_audio".
            Made from clean onboard full-throttle audio: Doppler shift,
            distance gain and air absorption, and a pan sweep for a car
            passing 12 m away at 220 km/h. Real TV pass-bys, if any are free
            of commentary, join the random bank as dtm13_tv_NN.
  race/     grid_idle_NN / grid_launch_NN pairs simulated from the clean
            onboards (start_synth.py: a 22-car grid heard from the
            grandstand), and pit_exit_NN (13 s, peak_s) from onboard pit
            exits. They replace the stock clips with the same key; fire-ups
            and wheelguns stay stock. These banks are shared by all cars
            (wishlist E8).
Levels follow the stock clips (whole-clip RMS x gain).

Output: private/engine_audio/pack/<pack_folder>/ (files/ + overlay.json).
--install applies it to the installed pack, never to dist/ or the repo.

    python tools/engine_audio/package.py [--season seasons/dtm-2013] [--install]
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfilt

import overlay
import start_synth
from common import MAKES, PACK_DIR, REPO, connect, decode, dump_json, game_path, load_json, slug, write_wav

SR = 44100
C = 343.0
FADE = 0.03


# ------------------------------------------------------------------ helpers

def rms_db(x: np.ndarray) -> float:
    return float(10 * np.log10(np.mean(np.square(x, dtype=np.float64)) + 1e-12))


def fades(x: np.ndarray) -> np.ndarray:
    n = min(int(FADE * SR), len(x) // 4)
    if n:
        r = np.linspace(0, 1, n, dtype=np.float32)[:, None]
        x[:n] *= r
        x[-n:] *= r[::-1]
    return x


def peak_normalise(x: np.ndarray, peak_db: float = -1.0) -> np.ndarray:
    return x * (10 ** (peak_db / 20) / (np.abs(x).max() + 1e-9))


def loudest_80ms(x: np.ndarray) -> float:
    """Centre of the loudest 80 ms RMS window, as the game's own cues are set."""
    w = int(0.08 * SR)
    e = np.convolve(np.square(x.mean(axis=1)), np.ones(w), mode="valid")
    return round((int(e.argmax()) + w / 2) / SR, 6)


def stock_level(base_audio: Path, manifest: str, prefix: str) -> float:
    """Median effective level (RMS dB + gain) of the stock clips with this key prefix."""
    m = load_json(base_audio / manifest, {"clips": []})
    folder = (base_audio / manifest).parent
    levels = []
    for c in m["clips"]:
        if c.get("key", "").startswith(prefix) and (folder / c["file"]).exists():
            x = decode(folder / c["file"], sr=SR, channels=2)
            levels.append(rms_db(x) + 20 * np.log10(max(c.get("gain", 1.0), 1e-3)))
    return float(np.median(levels)) if levels else -20.0


def gain_for(x: np.ndarray, target_db: float) -> float:
    return round(float(np.clip(10 ** ((target_db - rms_db(x)) / 20), 0.05, 1.0)), 6)


# ---------------------------------------------------------------- synthesis

def synth_passby(src: np.ndarray, dur: float = 4.0, speed_kmh: float = 220.0,
                 dist: float = 12.0, cross: float = 2.0) -> np.ndarray:
    """Right-to-left pass-by from a mono onboard recording (src at SR, >= dur + 0.5 s).

    Received sample at time t was emitted at tau with t = tau + r(tau)/c
    (solved by fixed-point iteration), which gives the Doppler shift; level
    falls with 1/r, high frequencies fade with distance, and an equal-power
    pan follows the car's bearing.
    """
    v = speed_kmh / 3.6
    t = np.arange(int(dur * SR)) / SR
    pos = lambda tau: -v * (tau - cross)                 # +x = listener's right
    tau = t.copy()
    for _ in range(4):
        tau = t - np.hypot(pos(tau), dist) / C
    lead = 0.45                                           # source pre-roll for the delay
    idx = (tau + lead) * SR
    if idx.min() < 0 or idx.max() >= len(src) - 1:
        raise ValueError("source too short for the pass-by")
    dry = np.interp(idx, np.arange(len(src)), src)
    x, r = pos(tau), np.hypot(pos(tau), dist)
    far = sosfilt(butter(2, 2500, fs=SR, output="sos"), dry)
    mix = np.clip((r - dist) / 80, 0, 0.75)               # more muffled when far
    mono = ((1 - mix) * dry + mix * far) * (dist / r)
    p = (1 + x / r) / 2                                   # 1 = fully right
    out = np.stack([mono * np.sqrt(1 - p), mono * np.sqrt(p)], axis=1).astype(np.float32)
    return out


# ---------------------------------------------------------------- selection

def candidates(db, labels, min_q, onboard=True, make=None):
    # Trackviews are left out: their spectra show mirrored bands (one rising
    # while another falls), which a real engine's harmonics cannot do, so they
    # look like processed or simulator audio rather than the real cars.
    types = ("onboard", "onboard_bestof") if onboard else ("broadcast", "highlights")
    q = f"""SELECT s.*, v.manufacturer, v.driver, v.track, v.title, a.path AS audio_path
            FROM segments s JOIN videos v ON v.id = s.video_id JOIN audio a ON a.id = s.video_id
            WHERE s.label IN ({','.join('?' * len(labels))})
              AND v.video_type IN ({','.join('?' * len(types))})
              AND s.flags IS NULL AND s.quality >= ?"""
    args = [*labels, *types, min_q]
    if make:
        q += " AND v.manufacturer = ?"
        args.append(make)
    return [dict(r) for r in db.execute(q + " ORDER BY s.quality DESC", args)]


def round_robin(rows, n):
    """Best first, alternating makes, so a bank isn't all one car."""
    by = {}
    for r in rows:
        by.setdefault(r["manufacturer"] or "_", []).append(r)
    out = []
    while len(out) < n and any(by.values()):
        for k in sorted(by, key=lambda k: -by[k][0]["quality"] if by[k] else 0):
            if by[k] and len(out) < n:
                out.append(by[k].pop(0))
    return out


def ref(r) -> str:
    return f"private: {r['video_id']} @ {r['start_s']:.2f}s ({r['manufacturer'] or 'mixed'}, {r['driver'] or ''}, {r['track']})"


# --------------------------------------------------------------------- main

def build(season: Path, min_q: float, n_grid: int, n_pit: int, n_tv: int) -> Path:
    manifest = load_json(season / "season.json")
    pack, base = manifest["pack_folder"], manifest["base_pack"]
    base_audio = game_path() / "data" / base / "assets" / "audio"
    out = PACK_DIR / pack
    if out.exists():
        shutil.rmtree(out)
    files, clips, sets, report = [], {}, {}, []
    flyby = "assets/audio/session/hotlap_flybys.json"
    race = "assets/audio/race/race_engines.json"
    db = connect()

    def save(rel: str, audio: np.ndarray) -> None:
        write_wav(out / "files" / rel, fades(audio), SR)
        files.append(rel)

    # pass-bys, one per make, tagged on the supplier
    lvl = stock_level(base_audio, "session/hotlap_flybys.json", "engine_passby")
    suppliers = load_json(season / "data" / "engines.json", {}).get("suppliers", {})
    for make in MAKES:
        for r in candidates(db, ("full_throttle", "steady_high"), min_q, make=make):
            if r["end_s"] - r["start_s"] < 2.0:
                continue
            src = decode(Path(r["audio_path"]), max(0, r["start_s"] - 0.5), 4.9, SR, 2).mean(axis=1)
            try:
                rl = peak_normalise(synth_passby(src))
            except ValueError:
                continue
            key = f"dtm13_{slug(make).lower()}"
            gain, cross = gain_for(rl, lvl), loudest_80ms(rl)
            save(f"assets/audio/session/{key}.wav", rl)
            save(f"assets/audio/session/{key}_lr.wav", rl[:, ::-1].copy())
            clips.setdefault(flyby, []).extend([
                {"key": key, "file": f"{key}.wav", "crossing_s": cross, "gain": gain, "source": ref(r)},
                {"key": f"{key}_lr", "file": f"{key}_lr.wav", "direction": "lr",
                 "crossing_s": cross, "gain": gain, "source": ref(r)}])
            for name in suppliers:
                if slug(name).lower().startswith(slug(make).lower()):
                    sets.setdefault("engines.json", {})[f"suppliers.{name}.passby_audio"] = key
            report.append(f"pass-by {make}: synthesised from {ref(r)}, q={r['quality']:.2f}")
            break
        else:
            report.append(f"pass-by {make}: no clean onboard full-throttle yet (stock tag kept)")

    # real TV pass-bys: random bank only
    tv = [r for r in candidates(db, ("passby",), min_q, onboard=False) if r["direction"] in ("rl", "lr")]
    for i, r in enumerate(tv[:n_tv], 1):
        x = peak_normalise(decode(Path(r["audio_path"]), r["peak_s"] - 2.0, 4.0, SR, 2))
        rl = x if r["direction"] == "rl" else x[:, ::-1].copy()
        key = f"dtm13_tv_{i:02d}"
        gain, cross = gain_for(rl, lvl), loudest_80ms(rl)
        save(f"assets/audio/session/{key}.wav", rl)
        save(f"assets/audio/session/{key}_lr.wav", rl[:, ::-1].copy())
        clips.setdefault(flyby, []).extend([
            {"key": key, "file": f"{key}.wav", "crossing_s": cross, "gain": gain, "source": ref(r)},
            {"key": f"{key}_lr", "file": f"{key}_lr.wav", "direction": "lr",
             "crossing_s": cross, "gain": gain, "source": ref(r)}])
    report.append(f"TV pass-bys: {min(len(tv), n_tv)} clean (of {len(tv)})")

    # grid idle + launch pairs: simulated from clean onboards (start_synth.py).
    # Broadcast starts are unusable (commentary peaks there), and the onboards
    # are flying laps, so each pair is a 22-car grid rendered from a different
    # seed (grid order, listener spot in the grandstand).
    lvl_idle = stock_level(base_audio, "race/race_engines.json", "grid_idle")
    lvl_launch = stock_level(base_audio, "race/race_engines.json", "grid_launch")
    sources = start_synth.find_sources(db)
    used = 0
    if len(sources) >= 12:
        for i in range(1, n_grid + 1):
            idle, launch, info = start_synth.render_start(sources, seed=i)
            g = 10 ** (-1 / 20) / (max(np.abs(idle).max(), np.abs(launch).max()) + 1e-9)
            idle, launch = idle * g, launch * g
            save(f"assets/audio/race/dtm13_grid_idle_{i:02d}.ogg", idle)
            save(f"assets/audio/race/dtm13_grid_launch_{i:02d}.wav", launch)
            src = f"private: simulated 22-car start, seed {i}, listener {info['listener']}"
            clips.setdefault(race, []).extend([
                {"key": f"grid_idle_{i:02d}", "file": f"dtm13_grid_idle_{i:02d}.ogg",
                 "gain": gain_for(idle, lvl_idle), "source": src},
                {"key": f"grid_launch_{i:02d}", "file": f"dtm13_grid_launch_{i:02d}.wav",
                 "gain": gain_for(launch, lvl_launch), "source": src}])
            used += 1
    report.append(f"grid idle/launch pairs: {used} simulated from {len(sources)} clean onboards"
                  + ("" if used else " (too few sources, stock kept)"))

    # pit exits
    lvl_pit = stock_level(base_audio, "race/race_engines.json", "pit_exit")
    exits = round_robin(candidates(db, ("pit_exit",), min_q), n_pit)
    for i, r in enumerate(exits, 1):
        x = peak_normalise(decode(Path(r["audio_path"]), max(0, r["peak_s"] - 6.0), 13.0, SR, 2))
        save(f"assets/audio/race/dtm13_pit_exit_{i:02d}.wav", x)
        clips.setdefault(race, []).append(
            {"key": f"pit_exit_{i:02d}", "file": f"dtm13_pit_exit_{i:02d}.wav",
             "gain": gain_for(x, lvl_pit), "peak_s": loudest_80ms(x), "source": ref(r)})
    report.append(f"pit exits: {len(exits)} (stock kept for the rest; fire-ups and wheelguns stay stock)")

    if files:
        dump_json(out / "overlay.json", {"pack": pack, "files": files, "clips": clips, "set": sets})
        (out / "report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(f"{len(files)} files -> {out}" if files else "nothing clean enough to package yet")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--season", type=Path, default=REPO / "seasons" / "dtm-2013")
    ap.add_argument("--target", default="team_principal", choices=["team_principal"])
    ap.add_argument("--min-quality", type=float, default=0.3)
    ap.add_argument("--grid-pairs", type=int, default=4)
    ap.add_argument("--pit-exits", type=int, default=4)
    ap.add_argument("--tv-passbys", type=int, default=5)
    ap.add_argument("--install", action="store_true", help="apply to <game>/data/<pack_folder>")
    args = ap.parse_args()
    build(args.season, args.min_quality, args.grid_pairs, args.pit_exits, args.tv_passbys)
    if args.install:
        pack = load_json(args.season / "season.json")["pack_folder"]
        target = game_path() / "data" / pack
        if not target.is_dir():
            raise SystemExit(f"pack not installed yet: {target} (run build_pack.py --install)")
        print(overlay.apply(target, pack) if overlay.overlay_for(pack) else overlay.remove(target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
