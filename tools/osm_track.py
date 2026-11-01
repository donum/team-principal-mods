"""Generate a Team Principal track (JSON + overview PNG) from OpenStreetMap.

The racing line is the loop formed by the circuit's oneway `highway=raceway`
ways, so the driving direction comes from OSM. Corners are classified from
the curvature of that line, and target speeds use the same reference scale
as the base game's tracks (F1-like speeds; the season's `car_profile`
regulation scales them down for slower cars).

Map data (c) OpenStreetMap contributors, ODbL 1.0. Every generated track
carries that attribution, and the season credits must keep it.

Usage:
    python tools/osm_track.py seasons/dtm-1991/track_specs/zolder.json
"""

import argparse
import json
import math
import random
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "build" / "osm"
OSM_API = "https://api.openstreetmap.org/api/0.6/map?bbox={w},{s},{e},{n}"
USER_AGENT = "team-principal-mods/0.1 (https://github.com/; track tracing)"
ATTRIBUTION = "Map data (c) OpenStreetMap contributors, ODbL 1.0 (openstreetmap.org/copyright)"

CANVAS = (1044, 1080)
MARGIN_PX = 90
# Reference speed scale shared with the base tracks: v = SPEED_K * sqrt(radius_m).
SPEED_K = 18.0
V_MAX_KMH = 370.0
STRAIGHT_ACCEL = 9.0          # m/s^2, average reference acceleration on straights
CORNER_RADIUS_M = 250.0       # tighter than this counts as a corner
STEP_M = 5.0                  # resampling step for curvature analysis
MIN_STRAIGHT_M = 40.0         # shorter straights are absorbed into the corner before them

COLORS = {
    "grass": (112, 150, 74), "wood": (84, 122, 60), "tree": (40, 66, 44), "water": (58, 128, 138),
    "building": (150, 150, 152), "parking": (110, 110, 112), "road": (118, 118, 120),
    "kerb": (235, 235, 235), "asphalt": (52, 52, 56), "pit": (78, 78, 82), "line": (250, 250, 250),
}


# --------------------------------------------------------------------------- OSM

def fetch(bbox, name):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{name}.osm"
    if not path.exists():
        url = OSM_API.format(w=bbox[0], s=bbox[1], e=bbox[2], n=bbox[3])
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        path.write_bytes(urllib.request.urlopen(req, timeout=180).read())
    return ET.parse(path).getroot()


def parse(root):
    nodes = {n.get("id"): (float(n.get("lat")), float(n.get("lon"))) for n in root.iter("node")}
    ways = {}
    for w in root.iter("way"):
        ways[w.get("id")] = {"nds": [n.get("ref") for n in w.findall("nd")],
                             "tags": {t.get("k"): t.get("v") for t in w.iter("tag")}}
    relations = []
    for r in root.iter("relation"):
        tags = {t.get("k"): t.get("v") for t in r.iter("tag")}
        members = [(m.get("ref"), m.get("role")) for m in r.iter("member") if m.get("type") == "way"]
        relations.append({"tags": tags, "members": members})
    return nodes, ways, relations


def racing_loop(ways, spec):
    """Find the directed cycle of raceway ways that covers the most named corners."""
    exclude = set(spec.get("exclude_way_names", ["Pitlane", "Safety Car Lane"]))
    exclude_ids = set(spec.get("exclude_way_ids", []))
    race = {wid: w for wid, w in ways.items()
            if w["tags"].get("highway") == "raceway" and w["tags"].get("name") not in exclude
            and w["tags"].get("access") != "no" and wid not in exclude_ids}
    starts = {}
    for wid, w in race.items():
        starts.setdefault(w["nds"][0], []).append(wid)
    best = [None]

    def score(path):
        return (len({race[p]["tags"].get("ref") or race[p]["tags"].get("name") for p in path
                     if race[p]["tags"].get("name")}), sum(len(race[p]["nds"]) for p in path))

    def dfs(path, seen):
        for nxt in starts.get(race[path[-1]]["nds"][-1], []):
            if nxt == path[0]:
                if best[0] is None or score(path) > score(best[0]):
                    best[0] = list(path)
            elif nxt not in seen and len(path) < 80:
                seen.add(nxt)
                path.append(nxt)
                dfs(path, seen)
                path.pop()
                seen.discard(nxt)

    for first in race:
        dfs([first], {first})
        if best[0]:
            break
    if not best[0]:
        raise SystemExit("no closed loop of oneway raceway ways found")
    nds = []
    for wid in best[0]:
        part = race[wid]["nds"]
        nds.extend(part if not nds else part[1:])
    return nds[:-1] if nds[0] == nds[-1] else nds, best[0], race


# ------------------------------------------------------------------- geometry

class Projection:
    def __init__(self, lat0, lon0):
        self.lat0, self.lon0 = lat0, lon0
        self.kx = 111320.0 * math.cos(math.radians(lat0))
        self.ky = 110540.0

    def metres(self, lat, lon):
        return ((lon - self.lon0) * self.kx, -(lat - self.lat0) * self.ky)


def polyline_length(pts, closed=True):
    seq = pts + [pts[0]] if closed else pts
    return sum(math.dist(a, b) for a, b in zip(seq, seq[1:]))


def resample(pts, step=None, count=None):
    """Evenly resample a closed polyline by distance step or point count."""
    total = polyline_length(pts)
    if count:
        step = total / count
    seq = pts + [pts[0]]
    out, carry = [pts[0]], 0.0
    for a, b in zip(seq, seq[1:]):
        seg = math.dist(a, b)
        d = step - carry
        while d <= seg:
            t = d / seg
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
            d += step
        carry = seg - (d - step)
    if math.dist(out[-1], out[0]) < step * 0.5:
        out.pop()
    return out


def radius(a, b, c):
    """Circumradius through three points (inf for collinear)."""
    ab, bc, ca = math.dist(a, b), math.dist(b, c), math.dist(c, a)
    cross = abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))
    return float("inf") if cross < 1e-9 else ab * bc * ca / (2.0 * cross)


def corner_speed_kmh(r):
    return min(V_MAX_KMH, SPEED_K * math.sqrt(r))


def micro_sectors(dense, smooth=4):
    """Split a dense closed line into straight/low/med/high sectors."""
    n = len(dense)
    radii = [radius(dense[(i - smooth) % n], dense[i], dense[(i + smooth) % n]) for i in range(n)]
    is_corner = [r < CORNER_RADIUS_M for r in radii]
    # Rotate so the analysis starts on a straight sample if the start line sits in a corner.
    runs = []
    for i in range(n):
        if runs and runs[-1]["corner"] == is_corner[i]:
            runs[-1]["idx"].append(i)
        else:
            runs.append({"corner": is_corner[i], "idx": [i]})
    if len(runs) > 1 and runs[0]["corner"] == runs[-1]["corner"]:
        runs[0]["idx"] = runs[-1]["idx"] + runs[0]["idx"]
        runs.pop()
    # Absorb very short straights into the preceding corner.
    merged = []
    for run in runs:
        if not run["corner"] and len(run["idx"]) * STEP_M < MIN_STRAIGHT_M and merged:
            merged[-1]["idx"] += run["idx"]
        elif merged and merged[-1]["corner"] == run["corner"]:
            merged[-1]["idx"] += run["idx"]
        else:
            merged.append(run)
    sectors = []
    for k, run in enumerate(merged):
        length_m = len(run["idx"]) * STEP_M
        if run["corner"]:
            v = corner_speed_kmh(min(radii[i] for i in run["idx"]))
            kind = "low" if v <= 130 else "med" if v <= 185 else "high"
        else:
            prev = merged[k - 1]
            v_in = corner_speed_kmh(min(radii[i] for i in prev["idx"])) if prev["corner"] else V_MAX_KMH
            v = min(V_MAX_KMH, math.sqrt((v_in / 3.6) ** 2 + 2 * STRAIGHT_ACCEL * length_m) * 3.6)
            kind = "straight"
        sectors.append({"type": kind, "length_m": length_m, "target_speed_kmh": round(v / 5) * 5,
                        "start_index": run["idx"][0]})
    total = sum(s["length_m"] for s in sectors)
    return [{"type": s["type"], "length_pct": 100.0 * s["length_m"] / total,
             "target_speed_kmh": float(s["target_speed_kmh"])} for s in sectors], sectors


# ------------------------------------------------------------------- render

def render(path_png, proj, to_px, nodes, ways, relations, loop_px, pit_px, width_px, seed):
    from PIL import Image, ImageDraw

    img = Image.new("RGB", CANVAS, COLORS["grass"])
    draw = ImageDraw.Draw(img)
    rng = random.Random(seed)

    def px(nid):
        return to_px(*proj.metres(*nodes[nid]))

    def ring(wid):
        return [px(n) for n in ways[wid]["nds"] if n in nodes] if wid in ways else []

    def fill_areas(match, color):
        polys = [ring(wid) for wid, w in ways.items() if match(w["tags"]) and w["nds"][0] == w["nds"][-1]]
        for rel in relations:
            if match(rel["tags"]):
                polys += [ring(ref) for ref, role in rel["members"] if role == "outer"]
        for poly in polys:
            if len(poly) >= 3:
                draw.polygon(poly, fill=color)
        return polys

    woods = fill_areas(lambda t: t.get("natural") == "wood" or t.get("landuse") == "forest", COLORS["wood"])
    for poly in woods:
        if len(poly) < 3:
            continue
        xs, ys = [p[0] for p in poly], [p[1] for p in poly]
        area = (max(xs) - min(xs)) * (max(ys) - min(ys))
        for _ in range(int(area / 900)):
            x, y = rng.uniform(min(xs), max(xs)), rng.uniform(min(ys), max(ys))
            if point_in_poly(x, y, poly):
                r = rng.uniform(5, 9)
                draw.ellipse([x - r, y - r, x + r, y + r], fill=COLORS["tree"])
    fill_areas(lambda t: t.get("natural") == "water" or t.get("landuse") in ("reservoir", "basin"), COLORS["water"])
    fill_areas(lambda t: t.get("amenity") == "parking", COLORS["parking"])

    road_widths = {"motorway": 9, "trunk": 8, "primary": 7, "secondary": 6, "tertiary": 5,
                   "unclassified": 4, "residential": 4, "service": 3}
    for w in ways.values():
        hw = w["tags"].get("highway")
        if hw in road_widths:
            line = [px(n) for n in w["nds"] if n in nodes]
            if len(line) > 1:
                draw.line(line, fill=COLORS["road"], width=road_widths[hw], joint="curve")
    fill_areas(lambda t: "building" in t, COLORS["building"])

    if pit_px:
        draw.line(pit_px, fill=COLORS["pit"], width=max(3, int(width_px * 0.7)), joint="curve")
    closed = loop_px + loop_px[:1]
    draw.line(closed, fill=COLORS["kerb"], width=int(width_px + 4), joint="curve")
    draw.line(closed, fill=COLORS["asphalt"], width=int(width_px), joint="curve")
    # Start/finish line across the track at points[0].
    (x0, y0), (x1, y1) = loop_px[0], loop_px[1]
    dx, dy = x1 - x0, y1 - y0
    norm = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / norm * (width_px * 0.8), dx / norm * (width_px * 0.8)
    draw.line([(x0 - nx, y0 - ny), (x0 + nx, y0 + ny)], fill=COLORS["line"], width=3)
    img.save(path_png, optimize=True)


def point_in_poly(x, y, poly):
    inside = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


# ------------------------------------------------------------------- main

def build(spec_path):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    season_dir = Path(spec_path).resolve().parent.parent
    root = fetch(spec["bbox"], spec["id"])
    nodes, ways, relations = parse(root)
    loop_nds, loop_ways, race = racing_loop(ways, spec)

    lat0 = sum(nodes[n][0] for n in loop_nds) / len(loop_nds)
    lon0 = sum(nodes[n][1] for n in loop_nds) / len(loop_nds)
    proj = Projection(lat0, lon0)
    loop_m = [proj.metres(*nodes[n]) for n in loop_nds]

    pit = next((w for w in ways.values() if w["tags"].get("highway") == "raceway"
                and w["tags"].get("name") in spec.get("pit_way_names", ["Pitlane"])), None)
    pit_m = [proj.metres(*nodes[n]) for n in pit["nds"]] if pit else None
    # Start/finish: point of the racing line nearest the middle of the pit lane.
    anchor = pit_m[len(pit_m) // 2] if pit_m else loop_m[0]
    dense = resample(loop_m, step=STEP_M)
    start = min(range(len(dense)), key=lambda i: math.dist(dense[i], anchor))
    dense = dense[start:] + dense[:start]

    xs, ys = [p[0] for p in dense], [p[1] for p in dense]
    scale = min((CANVAS[0] - 2 * MARGIN_PX) / (max(xs) - min(xs)), (CANVAS[1] - 2 * MARGIN_PX) / (max(ys) - min(ys)))
    ox = (CANVAS[0] - (max(xs) - min(xs)) * scale) / 2 - min(xs) * scale
    oy = (CANVAS[1] - (max(ys) - min(ys)) * scale) / 2 - min(ys) * scale
    to_px = lambda x, y: (x * scale + ox, y * scale + oy)

    sectors, raw = micro_sectors(dense)
    geometry_m = polyline_length(dense)
    outline = resample(dense, count=spec.get("point_count", 150))
    points = [[round(c) for c in to_px(*p)] for p in outline]

    # Sector splits snap to the start of the straight nearest to each third.
    starts = [s["start_index"] / len(dense) for s in raw if s["type"] == "straight" and s["start_index"] > 0]
    splits = sorted(min(starts, key=lambda f: abs(f - t)) for t in (1 / 3, 2 / 3)) if len(starts) >= 2 else [1 / 3, 2 / 3]

    track = {
        "name": spec["name"],
        "nationality": spec["nationality"],
        "length_km": spec.get("length_km", round(geometry_m / 1000, 3)),
        "lap_modifier": spec.get("lap_modifier", 1.1),
        "dnf_modifier": spec.get("dnf_modifier", 1.0),
        "overtaking_difficulty": spec.get("overtaking_difficulty", 0.6),
        "pit_lane_loss_s": spec.get("pit_lane_loss_s", 20.0),
        "tyre_wear_mult": spec.get("tyre_wear_mult", 0.9),
        "fuel_consumption": spec.get("fuel_consumption", 1.0),
        "wet_weather_probability_multiplier": spec.get("wet_weather_probability_multiplier", 1.0),
        "hide_polyline_visual": True,
        "racing_surface": {"enabled": True, "mode": "road_course", "width_m": spec.get("width_m", 11.0),
                           "edge_margin_m": 0.6, "corridor_count": 3, "visual_lateral_scale": 1.5},
        "starting_grid": {"pole_side": spec.get("pole_side", "left"), "row_spacing_m": 10.0,
                          "column_spacing_m": 3.0, "stagger_m": 4.0},
        "drs_zones": [],
        "sector_splits": splits,
        "micro_sectors": sectors,
        "points": points,
        "source": {"generator": "tools/osm_track.py", "osm_bbox": spec["bbox"],
                   "osm_ways": loop_ways, "geometry_length_m": round(geometry_m),
                   "attribution": ATTRIBUTION, "notes": spec.get("notes", "")},
    }
    out_json = season_dir / "tracks" / f"{spec['id']}.json"
    out_png = season_dir / "assets" / "tracks" / f"{spec['id']}.png"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(track, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    width_px = spec.get("width_m", 11.0) * scale * 1.4
    pit_px = [to_px(*p) for p in pit_m] if pit_m else None
    render(out_png, proj, to_px, nodes, ways, relations, [to_px(*p) for p in dense[::2]], pit_px, width_px, spec["id"])

    print(f"{spec['id']}: {len(loop_ways)} ways, {geometry_m:.0f} m traced (game length {track['length_km']} km), "
          f"{len(points)} points, {len(sectors)} micro-sectors (from the start line)")
    for s in sectors:
        print(f"  {s['type']:8s} {s['length_pct']:5.1f}%  {s['target_speed_kmh']:.0f} km/h")
    print(f"wrote {out_json.relative_to(REPO)} and {out_png.relative_to(REPO)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("specs", nargs="+", help="track spec JSON file(s)")
    for spec in parser.parse_args().specs:
        build(spec)


if __name__ == "__main__":
    main()
