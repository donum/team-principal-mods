"""Stage 5: turn the best segments into a game sound overlay (swappable target).

Target "team_principal" (Team Principal: A Racing Manager), per the game's
assets/audio/README_AUDIO.txt:
  session/  pass-bys: 4 s, 44.1 kHz stereo WAV, an RL file and an _lr mirror,
            crossing_s = centre of the loudest 80 ms. One key per make,
            tagged on the supplier through engines.json "passby_audio".
            Made from clean onboard full-throttle audio: Doppler shift,
            distance gain and air absorption, and a pan sweep for a car
            passing 12 m away at 220 km/h. Real TV pass-bys, if any are free
            of commentary, join the random bank as <prefix>_tv_NN.
  race/     grid_idle_NN / grid_launch_NN pairs cut from fan recordings of
            real race starts (starts.py; simulated ones from start_synth.py
            only with --synth-starts), and pit sets (pits.py): pit_fireup_NN,
            pit_exit_NN (peak_s) and pit_wheelguns_NN cut from fan recordings
            of the pit lane, paired by number. They replace the stock clips
            with the same key. These banks are shared by all cars (wishlist E8).
  ambience/ cars_on_track and crowd: loops of real trackside recordings
            (ambience.py), set through session_layers.json "cars.file" and
            "crowd.file".
Levels follow the stock clips (whole-clip RMS x gain).

Output: private/engine_audio/pack/<overlay id>/ (files/ + overlay.json), one
overlay per sound set: an era base's (bases/<id>/base.json "audio"), shared by
all its seasons, or a season's own (season.json "audio", ENGINE_AUDIO_BASE=<season>),
which makes only its "slots" and sits on top of the era's. --install applies
every installed pack's whole stack of sets, never to dist/ or the repo.

    python tools/engine_audio/package.py [--install]
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfilt

import overlay
import pits
import start_synth
import starts
from common import (BASE_ID, KEY_PREFIX, MAKES, OVERLAY_ID, PACK_DIR, REPO, SET_LIBRARY_DIR, SLOTS, connect, decode,
                    dump_json, game_path, load_json, slug, write_wav)

sys.path.insert(0, str(REPO / "tools"))
import layers as source_layers  # noqa: E402  (build() has a local "layers")

SR = 44100
C = 343.0
FADE = 0.03


# ------------------------------------------------------------------ helpers

START_IDLE_BOOST_DB = 5.0     # over the stock grid idle level
START_LAUNCH_BOOST_DB = 7.0   # over the stock launch burst: lands on pass-by level


def rms_db(x: np.ndarray) -> float:
    return float(10 * np.log10(np.mean(np.square(x, dtype=np.float64)) + 1e-12))


def loudest_db(x: np.ndarray, win_s: float = 0.5) -> float:
    """RMS dB of the loudest win_s stretch: what a launch burst is heard at."""
    w = int(win_s * SR)
    p = np.square(x.mean(axis=1), dtype=np.float64)
    return float(10 * np.log10(np.convolve(p, np.ones(w) / w, mode="valid").max() + 1e-12))


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


def stock_level(base_audio: Path, manifest: str, prefix: str, measure=rms_db) -> float:
    """Median effective level (measure dB + gain) of the stock clips with this key prefix."""
    m = load_json(base_audio / manifest, {"clips": []})
    folder = (base_audio / manifest).parent
    levels = []
    for c in m["clips"]:
        if c.get("key", "").startswith(prefix) and (folder / c["file"]).exists():
            x = decode(folder / c["file"], sr=SR, channels=2)
            levels.append(measure(x) + 20 * np.log10(max(c.get("gain", 1.0), 1e-3)))
    return float(np.median(levels)) if levels else -20.0


def gain_for(x: np.ndarray, target_db: float, measure=rms_db) -> float:
    return round(float(np.clip(10 ** ((target_db - measure(x)) / 20), 0.05, 1.0)), 6)


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

def build(min_q: float, n_grid: int, n_pit: int, n_tv: int,
          synth_starts: bool = False, test_start: bool = False) -> Path:
    manifest = source_layers.manifest(source_layers.source_dir(BASE_ID))
    pack, base = OVERLAY_ID, manifest["base_pack"]
    base_audio = game_path() / "data" / base / "assets" / "audio"
    out = PACK_DIR / pack
    if out.exists():
        shutil.rmtree(out)
    files, clips, sets, report = [], {}, {}, []
    if set(SLOTS) != {"passby", "tv", "start", "pit", "cars", "crowd"}:
        report.append(f"set {pack} makes only: {', '.join(SLOTS)} (the sets below it fill the rest)")
    flyby = "assets/audio/session/hotlap_flybys.json"
    race = "assets/audio/race/race_engines.json"
    db = connect()

    def below_count(prefix: str) -> int:
        """How many numbered keys (grid_launch_NN, pit_exit_NN) the sets under
        this one fill: a season set covers them all, so none of the era's
        clips is drawn in its pack."""
        n = 0
        for s in source_layers.audio_sets(source_layers.source_dir(BASE_ID)):
            if s["overlay"] == pack:
                continue
            ov = load_json(PACK_DIR / s["overlay"] / "overlay.json", {}) or {}
            n = max(n, sum(1 for c in ov.get("clips", {}).get(race, []) if c.get("key", "").startswith(prefix)))
        return n

    def save(rel: str, audio: np.ndarray, loop: bool = False) -> None:
        write_wav(out / "files" / rel, audio if loop else fades(audio), SR)
        files.append(rel)

    # pass-bys, one per make, tagged on the supplier
    lvl = stock_level(base_audio, "session/hotlap_flybys.json", "engine_passby")
    by_make = {}          # make -> clip key; overlay.py tags each season's suppliers by name
    for make in (MAKES if "passby" in SLOTS else ()):
        for r in candidates(db, ("full_throttle", "steady_high"), min_q, make=make):
            if r["end_s"] - r["start_s"] < 2.0:
                continue
            src = decode(Path(r["audio_path"]), max(0, r["start_s"] - 0.5), 4.9, SR, 2).mean(axis=1)
            try:
                rl = peak_normalise(synth_passby(src))
            except ValueError:
                continue
            key = f"{KEY_PREFIX}_{slug(make).lower()}"
            gain, cross = gain_for(rl, lvl), loudest_80ms(rl)
            save(f"assets/audio/session/{key}.wav", rl)
            save(f"assets/audio/session/{key}_lr.wav", rl[:, ::-1].copy())
            clips.setdefault(flyby, []).extend([
                {"key": key, "file": f"{key}.wav", "crossing_s": cross, "gain": gain, "source": ref(r)},
                {"key": f"{key}_lr", "file": f"{key}_lr.wav", "direction": "lr",
                 "crossing_s": cross, "gain": gain, "source": ref(r)}])
            by_make[make] = key
            report.append(f"pass-by {make}: synthesised from {ref(r)}, q={r['quality']:.2f}")
            break
        else:
            report.append(f"pass-by {make}: no clean onboard full-throttle yet (stock tag kept)")

    # real TV pass-bys: random bank only
    tv = [r for r in candidates(db, ("passby",), min_q, onboard=False)
          if r["direction"] in ("rl", "lr")] if "tv" in SLOTS else []
    for i, r in enumerate(tv[:n_tv], 1):
        x = peak_normalise(decode(Path(r["audio_path"]), r["peak_s"] - 2.0, 4.0, SR, 2))
        rl = x if r["direction"] == "rl" else x[:, ::-1].copy()
        key = f"{KEY_PREFIX}_tv_{i:02d}"
        gain, cross = gain_for(rl, lvl), loudest_80ms(rl)
        save(f"assets/audio/session/{key}.wav", rl)
        save(f"assets/audio/session/{key}_lr.wav", rl[:, ::-1].copy())
        clips.setdefault(flyby, []).extend([
            {"key": key, "file": f"{key}.wav", "crossing_s": cross, "gain": gain, "source": ref(r)},
            {"key": f"{key}_lr", "file": f"{key}_lr.wav", "direction": "lr",
             "crossing_s": cross, "gain": gain, "source": ref(r)}])
    if "tv" in SLOTS:
        report.append(f"TV pass-bys: {min(len(tv), n_tv)} clean (of {len(tv)})")

    # grid idle + launch pairs: real fan recordings of race starts (starts.py).
    # The broadcast starts are unusable (commentary peaks there). Simulated
    # pairs (start_synth.py) only with --synth-starts; otherwise the stock
    # pairs stay for any slot without a real recording.
    lvl_idle = stock_level(base_audio, "race/race_engines.json", "grid_idle")
    # launches are matched on their burst (loudest 0.5 s), not the whole clip:
    # ours hold the roar longer than stock, so whole-clip RMS left the burst
    # 2-4 dB under the stock one
    lvl_launch = stock_level(base_audio, "race/race_engines.json", "grid_launch", loudest_db)
    pairs = []
    if test_start:
        idle, launch = starts.test_pair()
        pairs.append((idle, launch, "TEST TONES (package.py --test-start): not a car"))
    for s in ([] if test_start or "start" not in SLOTS else starts.real_starts(db)[:n_grid]):
        pairs.append((s["idle"], s["launch"], f"private: {s['video_id']} go @ {s['go_s']:.2f}s ({s['note']})"))
    if synth_starts and not test_start and "start" in SLOTS:
        sources = start_synth.find_sources(db)
        for seed in range(1, n_grid - len(pairs) + 1):
            idle, launch, info = start_synth.render_start(sources, seed=seed)
            pairs.append((idle, launch, f"private: simulated 22-car start, seed {seed}, listener {info['listener']}"))
    entries = []
    for i, (idle, launch, src) in enumerate(pairs, 1):
        # idle None: the start has no grid loop of its own (starts.py), the
        # set below keeps its grid idle and only the launch is ours
        g = 10 ** (-1 / 20) / (max(np.abs(idle).max() if idle is not None else 0, np.abs(launch).max()) + 1e-9)
        launch = launch * g
        if idle is not None:
            idle = idle * g
            save(f"assets/audio/race/{KEY_PREFIX}_grid_idle_{i:02d}.ogg", idle, loop=True)
        save(f"assets/audio/race/{KEY_PREFIX}_grid_launch_{i:02d}.wav", launch)
        # matched to stock, the real start was inaudible in game (2026-11-04):
        # the stock start is quiet, its burst ~6 dB under a pass-by, and our
        # 22 s grandstand roar then reads as background. The launch's loudest
        # 0.5 s now sits at pass-by level, the grid revving 5 dB over stock.
        idle_g = round(min(1.0, gain_for(idle, lvl_idle) * 10 ** (START_IDLE_BOOST_DB / 20)), 6) if idle is not None else None
        launch_g = round(min(1.0, gain_for(launch, lvl_launch, loudest_db) * 10 ** (START_LAUNCH_BOOST_DB / 20)), 6)
        entries.append((f"{KEY_PREFIX}_grid_idle_{i:02d}.ogg" if idle is not None else None, 0.5 if test_start else idle_g,
                        f"{KEY_PREFIX}_grid_launch_{i:02d}.wav", 0.8 if test_start else launch_g, src))
    # fewer pairs than the stock bank: the stock slots left over would still be
    # picked at random, so they point at our files too
    stock_pairs = sum(1 for c in load_json(base_audio / "race/race_engines.json", {"clips": []})["clips"]
                      if c.get("key", "").startswith("grid_launch_"))
    stock_pairs = max(stock_pairs, below_count("grid_launch_"))
    for i in range(max(len(entries), stock_pairs if entries else 0)):
        idle_f, idle_g, launch_f, launch_g, src = entries[i % len(entries)]
        if idle_f:
            clips.setdefault(race, []).append({"key": f"grid_idle_{i + 1:02d}", "file": idle_f, "gain": idle_g, "source": src})
        clips.setdefault(race, []).append({"key": f"grid_launch_{i + 1:02d}", "file": launch_f, "gain": launch_g, "source": src})
    if "start" in SLOTS:
        report.append(f"grid idle/launch pairs: {len(pairs)} " + ("(TEST TONES)" if test_start else f"({sum('simulated' not in p[2] for p in pairs)} real fan recordings)")
                  + (f", filling {stock_pairs} stock slots" if pairs and len(pairs) < stock_pairs else "")
                  + ("" if pairs else ", stock kept"))

    # pit sets (pits.py): fire-up / exit / wheelguns, paired by number. The
    # game boosts each pit clip toward full scale (pits.game_boost), so levels
    # are matched as heard, not as the files are. Every stock set number is
    # pointed at one of ours (cycling), so the shuffled bag never draws a
    # stock exit; a kind our set lacks keeps the stock clip of that number.
    stock_race = load_json(base_audio / "race" / "race_engines.json", {"clips": []})
    stock_n = sum(1 for c in stock_race["clips"] if c.get("key", "").startswith("pit_exit_"))
    cover_n = max(stock_n, below_count("pit_exit_"))
    heard = {}
    for kind in ("fireup", "exit", "wheelguns"):
        lv = [pits.heard_db(decode(base_audio / "race" / c["file"], sr=SR, channels=2), c.get("gain", 1.0))
              for c in stock_race["clips"] if c.get("key", "").startswith(f"pit_{kind}_")]
        heard[kind] = float(np.median(lv)) if lv else -24.0
    pit_sets = [] if test_start or "pit" not in SLOTS else pits.real_pits(db)[:n_pit]
    stock_by_key = {c["key"]: c for c in stock_race["clips"] if "key" in c}

    def fireup_entry(x: np.ndarray, name: str, source: str) -> dict:
        # The game clamps clip gains to 1.0 and scales the fire-up by
        # fireup_gain / exit_gain before joining it to the exit; the joined
        # departure is then boosted by pits.game_boost, which is ~1 for our
        # near-full-scale exits (stock exits are boosted 5x). So the fire-up
        # is written at the level it should be heard at, gain 1.0, and the
        # exit gain no longer turns it down.
        boost = pits.GAME_PEAK / 10 ** (-1 / 20)
        x = x * 10 ** ((heard["fireup"] - rms_db(x)) / 20) / boost
        x = x * min(1.0, 0.89 / (np.abs(x).max() + 1e-9))
        write_wav(out / "files" / f"assets/audio/race/{name}", x, SR)
        files.append(f"assets/audio/race/{name}")
        return {"file": name, "gain": 1.0, "source": source}

    files_for, written = [], {}       # (kind, source) -> entry: a clip shared by sets is written once
    for i, s in enumerate(pit_sets, 1):
        entry = {}
        for kind in ("exit", "wheelguns", "fireup"):
            x = s[kind]
            name = f"{KEY_PREFIX}_pit_{kind}_{i:02d}.wav"
            if s["sources"].get(kind) and (kind, s["sources"][kind]) in written:
                entry[kind] = dict(written[(kind, s["sources"][kind])])
                continue
            if kind == "fireup":
                if x is not None:
                    entry[kind] = fireup_entry(x, name, "private: " + " ".join(map(str, s["sources"][kind])))
                else:
                    # no real fire-up yet: the stock one of a stock set
                    # number, levelled the same way
                    src = stock_by_key.get(f"pit_fireup_{(i - 1) % stock_n + 1:02d}") if stock_n else None
                    if src:
                        entry[kind] = fireup_entry(decode(base_audio / "race" / src["file"], sr=SR, channels=2),
                                                   name, f"stock {src['file']}, levelled for our exits")
                continue
            if x is None:
                continue
            write_wav(out / "files" / f"assets/audio/race/{name}", x, SR)   # pits.py already faded it
            files.append(f"assets/audio/race/{name}")
            gain = round(float(np.clip(10 ** ((heard[kind] - pits.heard_db(x)) / 20), 0.02, 1.0)), 6)
            entry[kind] = {"file": name, "gain": gain, "source": "private: " + " ".join(map(str, s["sources"][kind]))}
            if kind == "exit":
                entry[kind]["peak_s"] = loudest_80ms(x)
                if s.get("exit_unconfirmed"):
                    entry[kind]["source"] += " (UNCONFIRMED pit exit: not yet confirmed by ear)"
            written[(kind, s["sources"][kind])] = entry[kind]
        files_for.append(entry)
    for n in range(max(len(files_for), cover_n if files_for else 0)):
        for kind, e in files_for[n % len(files_for)].items():
            clips.setdefault(race, []).append({"key": f"pit_{kind}_{n + 1:02d}", **e})
    real = {k: sum(k in e and e[k]["source"].startswith("private") for e in files_for) for k in ("fireup", "exit", "wheelguns")}
    if "pit" in SLOTS:
        report.append(f"pit sets: {len(files_for)} (real: " + ", ".join(f"{v} {k}" for k, v in real.items())
                  + ("; the rest of the fire-ups are stock, levelled for our exits)" if files_for else "), stock kept"))

    # ambience layers from real trackside recordings (ambience.py): seamless
    # loops, so written without the clip fades; gains keep the stock level.
    layers = "assets/audio/ambience/session_layers.json"
    stock_layers = load_json(base_audio / "ambience" / "session_layers.json", {})
    for layer, stock_file, name in (("cars", "cars_on_track.ogg", "cars on track"), ("crowd", "crowd.ogg", "crowd")):
        if layer not in SLOTS:
            continue
        src_file = SET_LIBRARY_DIR / "ambience" / stock_file
        if not src_file.exists():
            report.append(f"{name}: stock (run ambience.py)")
            continue
        rel = f"assets/audio/ambience/{KEY_PREFIX}_{stock_file}"
        new_audio = decode(src_file, 0, None, SR, 2)
        stock = decode(base_audio / "ambience" / stock_file, 0, None, SR, 2)
        stock_gain = stock_layers.get(layer, {}).get("gain", 1.0)
        gain = round(float(np.clip(stock_gain * 10 ** ((rms_db(stock) - rms_db(new_audio)) / 20), 0.005, 1.0)), 6)
        (out / "files" / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, out / "files" / rel)
        files.append(rel)
        sets.setdefault(layers, {}).update({f"{layer}.file": Path(rel).name, f"{layer}.gain": gain})
        report.append(f"{name}: real trackside recording ({len(new_audio) / SR:.0f} s loop), gain {gain}")

    if files:
        dump_json(out / "overlay.json", {"pack": pack, "files": files, "clips": clips, "set": sets,
                                         "passby_by_make": by_make})
        (out / "report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(f"{len(files)} files -> {out}" if files else "nothing clean enough to package yet")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", default="team_principal", choices=["team_principal"])
    ap.add_argument("--min-quality", type=float, default=0.3)
    ap.add_argument("--grid-pairs", type=int, default=4)
    ap.add_argument("--synth-starts", action="store_true",
                    help="use simulated grid/launch pairs (off: only real recordings, else stock)")
    ap.add_argument("--test-start", action="store_true",
                    help="replace the start with loud test tones (checks the game plays the start slots)")
    ap.add_argument("--pit-sets", type=int, default=12)
    ap.add_argument("--tv-passbys", type=int, default=5)
    ap.add_argument("--install", action="store_true",
                    help="apply to every installed pack that plays this set (with the sets under it)")
    args = ap.parse_args()
    build(args.min_quality, args.grid_pairs, args.pit_sets, args.tv_passbys,
          args.synth_starts, args.test_start)
    if args.install:
        installed = [(s, load_json(s / "season.json")["pack_folder"]) for s in source_layers.seasons_on_overlay(OVERLAY_ID)]
        installed = [(s, pack) for s, pack in installed if (game_path() / "data" / pack).is_dir()]
        if not installed:
            raise SystemExit(f"no pack playing {OVERLAY_ID} is installed yet (run build_pack.py <season> --install)")
        for season, pack in installed:
            target = game_path() / "data" / pack
            stack = [a["overlay"] for a in source_layers.audio_sets(season)]
            print(f"{pack}: " + (overlay.apply(target, stack, pack) if any(overlay.overlay_for(s) for s in stack)
                                 else overlay.remove(target)))
        if "start" in SLOTS:
            starts.main()             # library/starts/start_NN_*.wav, the browser's "Real starts"
            import start_preview      # the starts as the game mixes them, for the browser
            start_preview.main(installed[0][1])
        if "pit" in SLOTS:
            pits.main()               # library/pits/pit_NN_*.wav, the browser's "Pit lane"
        # keep the mod browser (tools/mod_browser.py) in sync with what is installed
        import mod_browser
        for season, pack in installed:
            try:
                mod_browser.build(season, game_path())
            except Exception as err:
                print(f"warning: mod browser for {pack} not rebuilt: {err}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
