"""Calibrate per-track lap times against the real 1991 qualifying results.

In the game a track's lap time scales roughly with 1 / target speed, so each
track spec carries a "speed_scale" that multiplies all its micro-sector target
speeds (tools/osm_track.py). After an in-game qualifying session:

    new speed_scale = old speed_scale * game_pole / real_pole

(Note: a track's "lap_modifier" sets the number of race laps, not lap time;
osm_track.py derives it from the spec's "race_laps".)

Observations (in-game poles) are logged in <season>/research/calibration.json.

Usage:
    python tools/calibrate.py seasons/dtm-1991 --observe-save <save.json>   # record poles
    python tools/calibrate.py seasons/dtm-1991                              # report
    python tools/calibrate.py seasons/dtm-1991 --apply                      # update specs
then regenerate the tracks (tools/osm_track.py) and rebuild the pack.
"""

import argparse
import csv
import json
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_pack import game_path, load_json  # noqa: E402


def parse_time(text):
    text = text.strip()
    if not text:
        return None
    minutes, _, seconds = text.rpartition(":")
    return (int(minutes) if minutes else 0) * 60 + float(seconds)


def real_poles(season_dir):
    """Best qualifying time per track over all its 1991 rounds (dry reference)."""
    poles = {}
    for path in sorted((season_dir / "research" / "results").glob("*-qualifying.csv")):
        track = path.stem.split("-", 1)[1].rsplit("-", 1)[0]
        with open(path, encoding="utf-8") as fh:
            times = [t for t in (parse_time(r["time"]) for r in csv.DictReader(fh)) if t]
        if times and (track not in poles or min(times) < poles[track]):
            poles[track] = min(times)
    return poles


def observe_save(season_dir, save_path):
    manifest = load_json(season_dir / "season.json")
    installed = game_path(None) / "data" / manifest["pack_folder"] / "tracks"
    save = load_json(save_path)
    path = season_dir / "research" / "calibration.json"
    data = load_json(path) if path.exists() else {"observations": []}
    for track, hist in save.get("track_history", {}).items():
        for entry in hist.get("recent_qualifying", []):
            laps = [r["lap"] for r in entry.get("results", []) if r.get("lap") and not r.get("dnq")]
            tfile = installed / f"{track}.json"
            if not laps or not tfile.exists():
                continue
            obs = {"track": track, "session": "qualifying", "season": entry.get("season"),
                   "game_pole_s": round(min(laps), 3),
                   "speed_scale": load_json(tfile).get("source", {}).get("speed_scale", 1.0),
                   "save": Path(save_path).name}
            if obs not in data["observations"]:
                data["observations"].append(obs)
                print(f"observed {track}: pole {obs['game_pole_s']} s at speed_scale {obs['speed_scale']}")
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("season", type=Path)
    parser.add_argument("--observe-save", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    season_dir = args.season.resolve()
    if args.observe_save:
        observe_save(season_dir, args.observe_save)
    path = season_dir / "research" / "calibration.json"
    obs = load_json(path)["observations"] if path.exists() else []
    poles = real_poles(season_dir)
    print(f"{'track':14s} {'real pole':>9s} {'game pole':>9s} {'scale':>6s} {'new':>6s}")
    for spec_path in sorted((season_dir / "track_specs").glob("*.json")):
        spec = load_json(spec_path)
        tid = spec["id"]
        mine = [o for o in obs if o["track"] == tid and o.get("session") == "qualifying" and "speed_scale" in o]
        if not mine or tid not in poles:
            print(f"{tid:14s} {poles.get(tid, 0):9.2f} {'-':>9s} {spec.get('speed_scale', 1.0):6.3f}   (no in-game data)")
            continue
        last = mine[-1]
        new = round(last["speed_scale"] * last["game_pole_s"] / poles[tid], 3)
        print(f"{tid:14s} {poles[tid]:9.2f} {last['game_pole_s']:9.2f} {last['speed_scale']:6.3f} {new:6.3f}")
        if args.apply:
            text = spec_path.read_text(encoding="utf-8")
            text = re.sub(r'("speed_scale":\s*)[0-9.]+', lambda m: m.group(1) + str(new), text, count=1)
            spec_path.write_text(text, encoding="utf-8", newline="\n")
    if args.apply:
        print("\nspeed_scale updated; regenerate tracks and rebuild the pack.")


if __name__ == "__main__":
    main()
