"""Game track files that match the track artwork: the racing line, start line and sector splits come
from the same race-tracks centreline the art's exact overlay is drawn from, in the art's own frame.

    python tools/art_track.py seasons/dtm-2013            # every track in <season>/track_art.json
    python tools/art_track.py seasons/dtm-2013 moscow     # one track

<season>/track_art.json, per game track id:
    "race_tracks": {"track": "moscow-raceway", "layout": "sprint@2013"}   race-tracks base SVG
    "spec":  "bases/dtm-era4/track_specs/moscow.json"   name, length, laps, width, DRS ... (as osm_track.py)
    "viewBoxMetres": [x, y, w, h]   optional: the art's frame in race-tracks local metres; default the
                                    race-tracks plan frame (dist/styles/plan/<track>/<layout>.json), which
                                    is the game frame (whole lap in the visible map area). px = (m - (x, y)) * 1044 / w
    "speed_scale": 1.0              lap-time calibration (tools/calibrate.py), replaces the spec's
    "art": "..."                    where the image came from (provenance only)

Unlike osm_track.py there is no OSM trace and no fit into a box: the art decides the frame, so the
cars run exactly on the drawn track. The start line is race-tracks lap 0 (the reviewed start/finish of
that year), the sector splits are race-tracks' timing intermediates (geometry.json "sectors": lapM, else
mapLapM) as lap fractions. Writes <season>/tracks/<id>.json, which replaces the base's file.

race-tracks is found through local.json "race_tracks_path", else ../race-tracks next to this repository.
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import osm_track as ot  # noqa: E402
from laptime import reference_time  # noqa: E402
import layers  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
CANVAS = ot.CANVAS


def race_tracks_root():
    local = REPO / "local.json"
    if local.exists():
        p = json.loads(local.read_text(encoding="utf-8")).get("race_tracks_path")
        if p:
            return Path(p)
    return REPO.parent / "race-tracks"


def centreline(root, track, layout):
    sys.path.insert(0, str(root / "tools" / "i2"))
    sys.path.insert(0, str(root / "tools"))
    import lib  # race-tracks tools/i2/lib.py
    return [tuple(p) for p in lib.centerline(track, layout)]


def plan_view(root, track, layout):
    """The race-tracks plan frame: the game frame (styles/scene.py Scene.frame)."""
    plan = root / "dist" / "styles" / "plan" / track / f"{layout}.json"
    return json.loads(plan.read_text(encoding="utf-8"))["image"]["viewBoxMetres"]


def sectors(root, track, layout):
    """Timing intermediates of the layout version as lap metres (race-tracks geometry.json)."""
    geo = json.loads((root / "tracks" / track / "geometry.json").read_text(encoding="utf-8"))
    name, version = layout.split("@")
    spec = geo["layouts"][name]["versions"][version]
    return [(s["name"], s.get("lapM", s.get("mapLapM"))) for s in spec.get("sectors", [])]


def build(season, tid, cfg, root, quiet=False):
    spec = json.loads((REPO / cfg["spec"]).read_text(encoding="utf-8"))
    rt = cfg["race_tracks"]
    cl = centreline(root, rt["track"], rt["layout"])
    lap_m = ot.polyline_length(cl)
    view = cfg.get("viewBoxMetres") or plan_view(root, rt["track"], rt["layout"])
    vx, vy, vw, vh = view
    scale = CANVAS[0] / vw
    if abs(CANVAS[1] / vh - scale) > 1e-3 * scale:
        raise SystemExit(f"{tid}: viewBoxMetres is not 1044:1080")
    to_px = lambda x, y: ((x - vx) * scale, (y - vy) * scale)

    dense = ot.smooth(ot.resample(cl, step=ot.STEP_M))      # same curvature analysis as osm_track.py
    micro, raw = ot.micro_sectors(dense, spec.get("width_m", 11.0))
    speed_scale = cfg.get("speed_scale", spec.get("speed_scale", 1.0))
    for m in micro:
        m["target_speed_kmh"] = round(m["target_speed_kmh"] * speed_scale, 1)
    points = [[round(c, 1) for c in to_px(*p)] for p in ot.resample(cl, count=spec.get("point_count", 300))]
    off = [p for p in points if not (0 <= p[0] <= CANVAS[0] and 0 <= p[1] <= CANVAS[1])]
    if off:
        raise SystemExit(f"{tid}: {len(off)} line points outside the canvas")
    splits = sorted(round(m / lap_m, 4) for _, m in sectors(root, rt["track"], rt["layout"]) if m is not None)
    if len(splits) != 2:
        print(f"  {tid}: race-tracks has {len(splits)} intermediates, using thirds")
        splits = [round(1 / 3, 4), round(2 / 3, 4)]

    track = {
        "name": spec["name"],
        "nationality": spec["nationality"],
        "length_km": spec.get("length_km", round(lap_m / 1000, 3)),
        "lap_modifier": round(spec["race_laps"] / ot.BASE_RACE_LAPS, 4) if "race_laps" in spec else spec.get("lap_modifier", 1.0),
        "dnf_modifier": spec.get("dnf_modifier", 1.0),
        "overtaking_difficulty": spec.get("overtaking_difficulty", 0.6),
        "pit_lane_loss_s": spec.get("pit_lane_loss_s", 20.0),
        "tyre_wear_mult": spec.get("tyre_wear_mult", 0.9),
        "fuel_consumption": spec.get("fuel_consumption", 1.0),
        "wet_weather_probability_multiplier": spec.get("wet_weather_probability_multiplier", 1.0),
        "use_raw_canvas_coordinates": True,
        "raw_canvas_size": list(CANVAS),
        "hide_polyline_visual": True,
        "racing_surface": {"enabled": True, "mode": "road_course", "width_m": spec.get("width_m", 11.0),
                           "edge_margin_m": 0.6, "corridor_count": 3, "visual_lateral_scale": 1.5},
        "starting_grid": {"pole_side": spec.get("pole_side", "left"), "row_spacing_m": 10.0,
                          "column_spacing_m": 3.0, "stagger_m": 4.0},
        "drs_zones": ot.drs_zones(spec.get("drs_zones", []), raw, len(dense)),
        "sector_splits": splits,
        "micro_sectors": micro,
        "points": points,
        "source": {"generator": "tools/art_track.py", "race_tracks": dict(rt), "art": cfg.get("art", ""),
                   "viewBoxMetres": view, "geometry_length_m": round(lap_m),
                   "notes": spec.get("notes", ""), "speed_scale": speed_scale,
                   "canvas_transform": {"metres": "race-tracks local (x east, y south)", "scale": scale,
                                        "ox": -vx * scale, "oy": -vy * scale}},
    }
    out = REPO / season / "tracks" / f"{tid}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(track, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not quiet:
        print(f"{tid}: {lap_m:.0f} m centreline ({track['length_km']} km official), {len(micro)} micro-sectors, "
              f"splits {splits}, reference lap {reference_time(track):.2f} s -> {out.relative_to(REPO)}")
    return track


def in_pack(track, over):
    """The track as the pack ships it: the season's track_overrides speed_mult applied (build_pack.py)."""
    t = json.loads(json.dumps(track))
    for m in t["micro_sectors"]:
        m["target_speed_kmh"] = round(m["target_speed_kmh"] * over.get("speed_mult", 1.0), 1)
    t.update({k: v for k, v in over.items() if k in ("length_km",)})
    return t


def calibrate(season, tid, c, root, old_path):
    """speed_scale for which the new line's reference lap equals the shipped file's (keeps the lap-time fit)."""
    over = layers.manifest(REPO / season).get("track_overrides", {}).get(tid, {})
    target = reference_time(json.loads(Path(old_path).read_text(encoding="utf-8")))
    lo, hi = 0.5, 2.0
    for _ in range(30):
        c["speed_scale"] = round((lo + hi) / 2, 5)
        t = reference_time(in_pack(build(season, tid, c, root, quiet=True), over))
        lo, hi = (c["speed_scale"], hi) if t > target else (lo, c["speed_scale"])
    c["speed_scale"] = round((lo + hi) / 2, 4)
    t = reference_time(in_pack(build(season, tid, c, root), over))
    print(f"  {tid}: speed_scale {c['speed_scale']} -> reference {t:.2f} s (shipped file {target:.2f} s)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("season")
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--calibrate", metavar="PACK_TRACKS",
                    help="folder of the previously shipped track files (e.g. dist/dtm2013/tracks): set each "
                         "speed_scale so the reference lap stays the same, and save it in track_art.json")
    a = ap.parse_args()
    season = Path(a.season)
    cfg_path = REPO / season / "track_art.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    root = race_tracks_root()
    for tid, c in cfg["tracks"].items():
        if a.ids and tid not in a.ids:
            continue
        if a.calibrate:
            calibrate(season, tid, c, root, Path(a.calibrate) / f"{tid}.json")
        else:
            build(season, tid, c, root)
    if a.calibrate:
        cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
