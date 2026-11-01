"""Calibrate per-track lap times against real qualifying results.

The game's lap time for a track behaves like

    game_time ~= F * reference_time(micro_sectors) * lap_modifier

where reference_time comes from tools/laptime.py and F is a factor of the
season's cars and car profile, measured from in-game sessions. This tool
picks each track's lap_modifier so the predicted pole matches the real one.

Observations (in-game poles) live in <season>/research/calibration.json.
A track with its own observation uses its own F; others use the median F.

Usage:
    python tools/calibrate.py seasons/dtm-1991                  # report
    python tools/calibrate.py seasons/dtm-1991 --apply          # write lap_modifier
    python tools/calibrate.py seasons/dtm-1991 --observe-save <save.json> [--session qualifying]
"""

import argparse
import csv
import json
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from laptime import reference_time  # noqa: E402
from build_pack import game_path, load_json  # noqa: E402


def parse_time(text):
    text = text.strip()
    if not text:
        return None
    minutes, _, seconds = text.rpartition(":")
    return (int(minutes) if minutes else 0) * 60 + float(seconds)


def real_poles(season_dir):
    """Pole time of each track's first round from research/results/NN-<track>-qualifying.csv."""
    poles = {}
    for path in sorted((season_dir / "research" / "results").glob("*-qualifying.csv")):
        track = path.stem.split("-", 1)[1].rsplit("-", 1)[0]
        if track in poles:
            continue
        with open(path, encoding="utf-8") as fh:
            times = [parse_time(r["time"]) for r in csv.DictReader(fh)]
        times = [t for t in times if t]
        if times:
            poles[track] = {"time": min(times), "source": path.name}
    return poles


def load_observations(season_dir):
    path = season_dir / "research" / "calibration.json"
    return path, (load_json(path) if path.exists() else {"observations": []})


def observe_save(season_dir, save_path, session):
    """Record in-game poles from a save's track_history against the installed track files."""
    manifest = load_json(season_dir / "season.json")
    installed = game_path(None) / "data" / manifest["pack_folder"] / "tracks"
    save = load_json(save_path)
    path, data = load_observations(season_dir)
    key = "recent_qualifying" if session == "qualifying" else f"recent_{session}"
    for track, hist in save.get("track_history", {}).items():
        for entry in hist.get(key, []):
            laps = [r["lap"] for r in entry.get("results", []) if r.get("lap") and not r.get("dnq")]
            if not laps:
                continue
            tfile = installed / f"{track}.json"
            if not tfile.exists():
                continue
            t = load_json(tfile)
            obs = {"track": track, "session": session, "season": entry.get("season"),
                   "game_pole_s": round(min(laps), 3), "reference_s": round(reference_time(t), 3),
                   "lap_modifier": t.get("lap_modifier"), "save": Path(save_path).name}
            if obs not in data["observations"]:
                data["observations"].append(obs)
                print(f"observed {track}: pole {obs['game_pole_s']} s (lap_modifier {obs['lap_modifier']})")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def factor(obs):
    return obs["game_pole_s"] / (obs["reference_s"] * obs["lap_modifier"])


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("season", type=Path)
    parser.add_argument("--apply", action="store_true", help="write the new lap_modifier into specs and tracks")
    parser.add_argument("--observe-save", type=Path, help="record in-game poles from a save file")
    parser.add_argument("--session", default="qualifying")
    args = parser.parse_args()
    season_dir = args.season.resolve()

    if args.observe_save:
        observe_save(season_dir, args.observe_save, args.session)

    _, data = load_observations(season_dir)
    by_track = {}
    for obs in data["observations"]:
        by_track.setdefault(obs["track"], []).append(factor(obs))
    if not by_track:
        sys.exit("no in-game observations yet (use --observe-save)")
    global_f = statistics.median(f for fs in by_track.values() for f in fs)
    poles = real_poles(season_dir)

    print(f"global F = {global_f:.4f} from {sum(map(len, by_track.values()))} observation(s)\n")
    print(f"{'track':14s} {'real pole':>9s} {'reference':>9s} {'F':>6s} {'old mod':>8s} {'new mod':>8s} {'predicted':>9s}")
    for spec_path in sorted((season_dir / "track_specs").glob("*.json")):
        spec = load_json(spec_path)
        tid = spec["id"]
        track_path = season_dir / "tracks" / f"{tid}.json"
        if tid not in poles or not track_path.exists():
            continue
        track = load_json(track_path)
        ref = reference_time(track)
        f = statistics.median(by_track[tid]) if tid in by_track else global_f
        new_mod = round(poles[tid]["time"] / (f * ref), 3)
        print(f"{tid:14s} {poles[tid]['time']:9.2f} {ref:9.2f} {f:6.3f} {spec.get('lap_modifier', 1):8.3f} "
              f"{new_mod:8.3f} {f * ref * new_mod:9.2f}{'' if tid in by_track else '  (global F)'}")
        if args.apply:
            # Specs are hand-formatted: replace only the lap_modifier line.
            text = spec_path.read_text(encoding="utf-8")
            text = re.sub(r'("lap_modifier":\s*)[0-9.]+', lambda m: m.group(1) + str(new_mod), text, count=1)
            spec_path.write_text(text, encoding="utf-8", newline="\n")
            track["lap_modifier"] = new_mod
            track_path.write_text(json.dumps(track, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    if args.apply:
        print("\nlap_modifier written to track_specs/ and tracks/; rebuild and install the pack.")


if __name__ == "__main__":
    main()
