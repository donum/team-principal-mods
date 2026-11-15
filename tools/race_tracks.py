"""Read a circuit layout from the race-tracks repository (the track maps).

race-tracks (a sibling folder of this repo, or "race_tracks_repo" in
local.json) keeps every layout and era of a circuit, including layouts that
are no longer in OpenStreetMap (traced from old maps and imagery): Silverstone
GP 1991, Snetterton 1990, Oulton Park 1975... Its "base" SVG per layout holds
the finished racing line in metres, north up, starting at the start line,
in driving order, plus the pit lane and the start/finish line.

layout() turns that into [lat, lon] points, so tools/osm_track.py can build
a game track on the same line the track maps show. A track spec names it as

    "race_tracks": {"track": "silverstone", "layout": "gp@1991"}

Standard library only.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EARTH_R = 6378137.0          # race-tracks tools/common.py LocalProjection


def root() -> Path:
    local = REPO / "local.json"
    cfg = json.loads(local.read_text(encoding="utf-8")) if local.exists() else {}
    return Path(cfg.get("race_tracks_repo") or REPO.parent / "race-tracks")


def _points(d: str) -> list[tuple[float, float]]:
    nums = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", d)]
    return list(zip(nums[0::2], nums[1::2]))


def layout(track: str, layout_version: str) -> dict:
    """{"loop": [[lat, lon], ...] from the start line in driving order,
    "start": [lat, lon], "pit": [[lat, lon], ...] or None, "length_m", "direction",
    "approximate", "notes", "source"}."""
    base = root() / "tracks" / track
    svg = (base / "base" / f"{layout_version}.svg").read_text(encoding="utf-8")
    meta = json.loads(re.search(r'<metadata id="meta">(.*?)</metadata>', svg, re.S).group(1))
    if meta.get("rotate"):
        raise SystemExit(f"{track} {layout_version}: rotated base maps are not supported")
    lat0, lon0 = json.loads((base / "geometry.json").read_text(encoding="utf-8"))["osm"]["center"]
    kx = math.radians(1) * EARTH_R * math.cos(math.radians(lat0))
    ky = math.radians(1) * EARTH_R

    def ll(p):                                   # metres, y down -> [lat, lon]
        return [lat0 - p[1] / ky, lon0 + p[0] / kx]

    centre = re.search(r'id="centerline"[^>]*\sd="([^"]+)"', svg) or re.search(r'\sd="([^"]+)"[^>]*id="centerline"', svg)
    loop = [ll(p) for p in _points(centre.group(1))]
    if loop[0] == loop[-1]:
        loop.pop()
    sf = re.search(r'id="sf-line" x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"', svg)
    start = ll(((float(sf.group(1)) + float(sf.group(3))) / 2, (float(sf.group(2)) + float(sf.group(4))) / 2)) \
        if sf else loop[0]
    pit_layer = re.search(r'<g id="layer-pitlane">(.*?)</g>', svg, re.S)
    pits = [_points(d) for d in re.findall(r'\sd="([^"]+)"', pit_layer.group(1))] if pit_layer else []
    pit = [ll(p) for p in max(pits, key=len)] if pits else None
    return {"loop": loop, "start": start, "pit": pit, "length_m": meta.get("lengthM"),
            "official_length_m": meta.get("officialLengthM"), "direction": meta.get("direction"),
            "approximate": meta.get("approximate", False), "notes": meta.get("notes", ""),
            "source": meta.get("source", "")}


def bbox(track: str, layout_version: str, margin: float = 0.004) -> list[float]:
    """[west, south, east, north] around the layout, for the OSM background."""
    pts = layout(track, layout_version)["loop"]
    lats, lons = [p[0] for p in pts], [p[1] for p in pts]
    return [round(min(lons) - margin, 4), round(min(lats) - margin, 4),
            round(max(lons) + margin, 4), round(max(lats) + margin, 4)]


if __name__ == "__main__":
    import sys
    t, lv = sys.argv[1], sys.argv[2]
    r = layout(t, lv)
    print(f"{t} {lv}: {len(r['loop'])} points, {r['length_m']} m ({r['official_length_m']} official), "
          f"{r['direction']}, start {r['start']}, pit {'yes' if r['pit'] else 'no'}, bbox {bbox(t, lv)}")
