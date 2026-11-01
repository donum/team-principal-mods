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
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "build" / "osm"
OSM_API = "https://api.openstreetmap.org/api/0.6/map?bbox={w},{s},{e},{n}"
USER_AGENT = "team-principal-mods/0.1 (https://github.com/; track tracing)"
ATTRIBUTION = "Map data (c) OpenStreetMap contributors, ODbL 1.0 (openstreetmap.org/copyright)"

CANVAS = (1044, 1080)
# Where the racing line may go on the canvas. The race screen covers the lower
# part of the map with driver cards and the event log, so the track stays in
# the upper area while the background map still fills the whole image.
SAFE_BOX = (70, 60, 974, 800)
BASE_RACE_LAPS = 50           # "laps" in the base pack's options.json
SUPERSAMPLE = 3
SMOOTH_PASSES = 3             # moving-average passes over the 5 m resampled line
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

def fetch(bbox, name, depth=0):
    """Download (and cache) an OSM extract; areas over the API's node limit are split in four."""
    CACHE.mkdir(parents=True, exist_ok=True)
    key = "_".join(f"{v:.4f}" for v in bbox)
    path = CACHE / f"{name}_{key}.osm"
    if not path.exists():
        url = OSM_API.format(w=bbox[0], s=bbox[1], e=bbox[2], n=bbox[3])
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            path.write_bytes(urllib.request.urlopen(req, timeout=180).read())
        except urllib.error.HTTPError as err:
            if err.code != 400 or depth >= 3:
                raise
            w, s, e, n = bbox
            mx, my = (w + e) / 2, (s + n) / 2
            merged = ET.Element("osm")
            for i, quad in enumerate(([w, s, mx, my], [mx, s, e, my], [w, my, mx, n], [mx, my, e, n])):
                merged.extend(list(fetch(quad, f"{name}_q{i}", depth + 1)))
            ET.ElementTree(merged).write(path, encoding="utf-8")
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
        relations.append({"id": r.get("id"), "tags": tags, "members": members})
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


def smooth(pts, passes=SMOOTH_PASSES, half_window=2):
    """Closed-loop moving average: removes OSM node kinks without cutting corners much."""
    n = len(pts)
    for _ in range(passes):
        pts = [(sum(pts[(i + k) % n][0] for k in range(-half_window, half_window + 1)) / (2 * half_window + 1),
                sum(pts[(i + k) % n][1] for k in range(-half_window, half_window + 1)) / (2 * half_window + 1))
               for i in range(n)]
    return pts


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


def drs_zones(cfg, raw, n):
    """DRS zones as lap fractions from the start line.

    cfg is a list of explicit zones ({detection_progress, start_progress,
    end_progress}) or {"longest_straights": k}: one zone on each of the k
    longest straights, opening 10% into the straight, with detection 4% of a
    lap before the zone.
    """
    if isinstance(cfg, list):
        return cfg
    straights = sorted((s for s in raw if s["type"] == "straight"), key=lambda s: -s["length_m"])
    zones = []
    for s in sorted(straights[:cfg["longest_straights"]], key=lambda s: s["start_index"]):
        start = (s["start_index"] + 0.1 * s["length_m"] / STEP_M) / n
        end = (s["start_index"] + s["length_m"] / STEP_M) / n
        zones.append({"detection_progress": round((start - 0.04) % 1.0, 4), "start_progress": round(start % 1.0, 4),
                      "end_progress": round(end % 1.0, 4)})
    return zones


# ------------------------------------------------------------------- render

def render(path_png, proj, to_px, nodes, ways, relations, loop_px, pit_px, width_px, seed, px_per_m, spec=None):
    from PIL import Image, ImageDraw

    # Draw at SUPERSAMPLE x resolution and scale down for anti-aliased edges.
    ss = SUPERSAMPLE
    img = Image.new("RGB", (CANVAS[0] * ss, CANVAS[1] * ss), COLORS["grass"])
    draw = ImageDraw.Draw(img)
    rng = random.Random(seed)
    up = lambda pts: [(x * ss, y * ss) for x, y in pts]
    loop_px, width_px = up(loop_px), width_px * ss
    pit_px = up(pit_px) if pit_px else None

    def px(nid):
        x, y = to_px(*proj.metres(*nodes[nid]))
        return (x * ss, y * ss)

    def ring(wid):
        return [px(n) for n in ways[wid]["nds"] if n in nodes] if wid in ways else []

    spec = spec or {}
    # Historic look: areas that were forest in the season's year (e.g. land
    # cleared for a later rebuild). Modern features inside them are not drawn.
    historic = [[(lambda q: (q[0] * ss, q[1] * ss))(to_px(*proj.metres(lat, lon))) for lat, lon in poly]
                for poly in spec.get("historic_forest", [])]

    def modern(wid):
        pts = ring(wid)
        if not pts or not historic:
            return False
        cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
        return any(point_in_poly(cx, cy, poly) for poly in historic)

    def fill_areas(match, color):
        polys = [ring(wid) for wid, w in ways.items()
                 if match(w["tags"]) and w["nds"][0] == w["nds"][-1] and not modern(wid)]
        for rel in relations:
            if match(rel["tags"]):
                polys += [ring(ref) for ref, role in rel["members"] if role == "outer"]
        for poly in polys:
            if len(poly) >= 3:
                draw.polygon(poly, fill=color)
        return polys

    woods = fill_areas(lambda t: t.get("natural") == "wood" or t.get("landuse") == "forest", COLORS["wood"])
    for poly in historic:
        draw.polygon(poly, fill=COLORS["wood"])
    for poly in woods + historic:
        if len(poly) < 3:
            continue
        xs, ys = [p[0] for p in poly], [p[1] for p in poly]
        area = (max(xs) - min(xs)) * (max(ys) - min(ys))
        for _ in range(int(area / (900 * ss * ss))):
            x, y = rng.uniform(min(xs), max(xs)), rng.uniform(min(ys), max(ys))
            if point_in_poly(x, y, poly):
                r = rng.uniform(5, 9) * ss
                draw.ellipse([x - r, y - r, x + r, y + r], fill=COLORS["tree"])
    # Cleared verge along the circuit (grass run-off), so a forest track reads as a circuit.
    m_px = px_per_m * ss
    if spec.get("verge_m"):
        thick_line(draw, loop_px + loop_px[:1], COLORS["grass"], spec["verge_m"] * 2 * m_px + width_px)
    fill_areas(lambda t: t.get("natural") == "water" or t.get("landuse") in ("reservoir", "basin"), COLORS["water"])
    fill_areas(lambda t: t.get("amenity") == "parking", COLORS["parking"])

    # Runways and taxiways in metres, scaled like the track (airfield circuits use them).
    for wid, w in ways.items():
        kind = w["tags"].get("aeroway")
        if kind in ("runway", "taxiway") and not modern(wid):
            line = [px(n) for n in w["nds"] if n in nodes]
            if len(line) > 1:
                width_m = float(w["tags"].get("width", 0) or 0) or (40.0 if kind == "runway" else 18.0)
                thick_line(draw, line, COLORS["parking"], max(2 * ss, width_m * m_px))

    road_widths = {"motorway": 9, "trunk": 8, "primary": 7, "secondary": 6, "tertiary": 5,
                   "unclassified": 4, "residential": 4, "service": 3}
    for wid, w in ways.items():
        hw = w["tags"].get("highway")
        if hw in road_widths and not modern(wid):
            line = [px(n) for n in w["nds"] if n in nodes]
            if len(line) > 1:
                thick_line(draw, line, COLORS["road"], road_widths[hw] * ss)
    fill_areas(lambda t: "building" in t, COLORS["building"])

    if pit_px:
        thick_line(draw, pit_px, COLORS["pit"], max(3 * ss, width_px * 0.7))
    closed = loop_px + loop_px[:1]
    thick_line(draw, closed, COLORS["kerb"], width_px + 4 * ss)
    thick_line(draw, closed, COLORS["asphalt"], width_px)
    # Start/finish line across the track at points[0].
    (x0, y0), (x1, y1) = loop_px[0], loop_px[1]
    dx, dy = x1 - x0, y1 - y0
    norm = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / norm * (width_px * 0.8), dx / norm * (width_px * 0.8)
    draw.line([(x0 - nx, y0 - ny), (x0 + nx, y0 + ny)], fill=COLORS["line"], width=3 * ss)
    img.resize(CANVAS, Image.LANCZOS).save(path_png, optimize=True)


def thick_line(draw, pts, color, width):
    """Polyline with round caps at every vertex, so bends stay smooth at any width."""
    draw.line(pts, fill=color, width=int(width))
    r = width / 2
    for x, y in pts:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)


def point_in_poly(x, y, poly):
    inside = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


# ------------------------------------------------------------------- main

def way_matches(tags, rules):
    """A rule is {key: value} (value "*" = any, list = one of); a way matches any rule."""
    for rule in rules:
        if all(tags.get(k) is not None and (v == "*" or tags.get(k) == v or (isinstance(v, list) and tags.get(k) in v))
               for k, v in rule.items()):
            return True
    return False


def via_route(nodes, ways, spec, relations=()):
    """Build the lap by shortest paths between `via` points over the allowed ways.

    For circuits that are not (or no longer) tagged as a closed raceway loop:
    street circuits, airfield courses and demolished sections. `via` points
    are [lat, lon] in driving order; each snaps to the nearest graph node.
    Pairs with no graph connection are joined by a straight line, so missing
    OSM sections can be bridged with extra via points.
    """
    import heapq

    # Allowed ways: members of an OSM circuit relation and/or ways matching tag filters.
    members = set()
    if "route_relation" in spec:
        rel = next((r for r in relations if r["id"] == str(spec["route_relation"])), None)
        if rel is None:
            raise SystemExit(f"relation {spec['route_relation']} not in the downloaded area")
        members = {ref for ref, _ in rel["members"]}
    members |= set(spec.get("route_way_ids", []))
    allowed = {wid: w for wid, w in ways.items()
               if (wid in members or way_matches(w["tags"], spec.get("route_ways", [])))
               and wid not in set(spec.get("exclude_way_ids", []))}
    graph = {}
    for wid, w in allowed.items():
        # Densify to <= 10 m steps so via points snap onto the right way even
        # where OSM has few nodes (long straights, runways).
        nds = []
        raw = [n for n in w["nds"] if n in nodes]
        for a, b in zip(raw, raw[1:]):
            (y1, x1), (y2, x2) = nodes[a], nodes[b]
            seg = math.hypot((x2 - x1) * 111320 * math.cos(math.radians(y1)), (y2 - y1) * 110540)
            steps = max(1, int(seg // 10))
            nds.append(a)
            for k in range(1, steps):
                sid = f"{wid}:{a}:{k}"
                nodes[sid] = (y1 + (y2 - y1) * k / steps, x1 + (x2 - x1) * k / steps)
                nds.append(sid)
        if raw:
            nds.append(raw[-1])
        w = {**w, "nds": nds}
        allowed[wid] = w
        for a, b in zip(nds, nds[1:]):
            (y1, x1), (y2, x2) = nodes[a], nodes[b]
            d = math.hypot((x2 - x1) * 111320 * math.cos(math.radians(y1)), (y2 - y1) * 110540)
            graph.setdefault(a, []).append((b, d, wid))
            graph.setdefault(b, []).append((a, d, wid))
    if not graph:
        raise SystemExit("route_ways matched no OSM ways")
    # Abandoned or partly mapped sections often stop a few metres short of the
    # next way: join every way end to the closest node of another way nearby.
    snap = spec.get("snap_gap_m", 40.0)
    node_way = {}
    for wid, w in allowed.items():
        for n in w["nds"]:
            node_way.setdefault(n, set()).add(wid)
    for wid, w in allowed.items():
        for end in (w["nds"][0], w["nds"][-1]):
            if end not in nodes or len(graph.get(end, [])) > 1:
                continue
            (y1, x1), k = nodes[end], math.cos(math.radians(nodes[end][0]))
            best = min(((math.hypot((nodes[n][1] - x1) * 111320 * k, (nodes[n][0] - y1) * 110540), n)
                        for n in graph if wid not in node_way.get(n, ())), default=(math.inf, None))
            if best[0] <= snap:
                graph[end].append((best[1], best[0], "gap"))
                graph[best[1]].append((end, best[0], "gap"))

    def nearest(lat, lon):
        k = math.cos(math.radians(lat))
        return min(graph, key=lambda n: ((nodes[n][0] - lat) ** 2 + ((nodes[n][1] - lon) * k) ** 2))

    # Explicit links for sections that no longer exist in OSM at all
    # (e.g. demolished track between two surviving pieces).
    # A bridge with more than two points is a hand-placed polyline: its first
    # and last points snap to the graph, the inner points become new nodes.
    for k, bridge in enumerate(spec.get("bridges", [])):
        chain = [nearest(*bridge[0])]
        for i, p in enumerate(bridge[1:-1]):
            sid = f"bridge{k}:{i}"
            nodes[sid] = tuple(p)
            graph[sid] = []
            chain.append(sid)
        chain.append(nearest(*bridge[-1]))
        for a, b in zip(chain, chain[1:]):
            d = math.hypot((nodes[b][1] - nodes[a][1]) * 111320 * math.cos(math.radians(nodes[a][0])),
                           (nodes[b][0] - nodes[a][0]) * 110540)
            graph[a].append((b, d, "gap"))
            graph[b].append((a, d, "gap"))

    def shortest(a, b):
        dist, prev, heap = {a: 0.0}, {}, [(0.0, a)]
        while heap:
            d, n = heapq.heappop(heap)
            if n == b:
                break
            if d > dist.get(n, math.inf):
                continue
            for m, w, _ in graph[n]:
                nd = d + w
                if nd < dist.get(m, math.inf):
                    dist[m], prev[m] = nd, n
                    heapq.heappush(heap, (nd, m))
        if b not in dist:
            return None
        path = [b]
        while path[-1] != a:
            path.append(prev[path[-1]])
        return path[::-1]

    snapped = [nearest(*v) for v in spec["via"]]
    coords, used, gaps = [], set(), 0
    for a, b in zip(snapped, snapped[1:] + snapped[:1]):
        path = shortest(a, b)
        if path is None:
            path, gaps = [a, b], gaps + 1
        for x, y in zip(path, path[1:]):
            used.update(wid for m, _, wid in graph.get(x, []) if m == y and wid != "gap")
        seg = [nodes[n] for n in path]
        if spec.get("debug"):
            leg = sum(math.hypot((q[1] - p[1]) * 111320 * math.cos(math.radians(p[0])), (q[0] - p[0]) * 110540)
                      for p, q in zip(seg, seg[1:]))
            print(f"  leg {len(coords) and '...' or 'start'} {nodes[a]} -> {nodes[b]}: {leg:.0f} m")
        coords.extend(seg if not coords else seg[1:])
    if coords[0] == coords[-1]:
        coords.pop()
    if gaps:
        print(f"note: {gaps} via leg(s) had no OSM connection and were bridged with straight lines")
    return coords, sorted(used)


def build(spec_path):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    season_dir = Path(spec_path).resolve().parent.parent
    # Dense cities exceed the OSM API's node limit, so a spec may split its
    # area into "bbox_tiles" that are fetched separately and merged.
    nodes, ways, relations = parse(fetch(spec["bbox"], spec["id"]))
    for i, tile in enumerate(spec.get("bbox_tiles", [])):
        t_nodes, t_ways, t_relations = parse(fetch(tile, f"{spec['id']}_{i}"))
        nodes.update(t_nodes)
        ways.update(t_ways)
        relations += t_relations
    if "via" in spec:
        loop_ll, loop_ways = via_route(nodes, ways, spec, relations)
    elif "loop_relation" in spec:
        # Raceway loop restricted to one circuit relation's members (e.g. a
        # short layout that shares its corners with the GP loop).
        rel = next((r for r in relations if r["id"] == str(spec["loop_relation"])), None)
        if rel is None:
            raise SystemExit(f"relation {spec['loop_relation']} not in the downloaded area")
        members = {m for m, _ in rel["members"]}
        loop_nds, loop_ways, _ = racing_loop({k: w for k, w in ways.items() if k in members}, spec)
        loop_ll = [nodes[n] for n in loop_nds]
    else:
        loop_nds, loop_ways, _ = racing_loop(ways, spec)
        loop_ll = [nodes[n] for n in loop_nds]

    lat0 = sum(p[0] for p in loop_ll) / len(loop_ll)
    lon0 = sum(p[1] for p in loop_ll) / len(loop_ll)
    proj = Projection(lat0, lon0)
    loop_m = [proj.metres(*p) for p in loop_ll]

    pit = next((w for w in ways.values() if w["tags"].get("highway") == "raceway"
                and w["tags"].get("name") in spec.get("pit_way_names", ["Pitlane"])), None)
    pit_m = [proj.metres(*nodes[n]) for n in pit["nds"] if n in nodes] if pit else None
    # Start/finish: an explicit position, else the racing line nearest the middle of the pit lane.
    if "start" in spec:
        anchor = proj.metres(*spec["start"])
    else:
        anchor = pit_m[len(pit_m) // 2] if pit_m else loop_m[0]
    dense = resample(loop_m, step=STEP_M)
    start = min(range(len(dense)), key=lambda i: math.dist(dense[i], anchor))
    dense = smooth(dense[start:] + dense[:start])

    xs, ys = [p[0] for p in dense], [p[1] for p in dense]
    box_w, box_h = SAFE_BOX[2] - SAFE_BOX[0], SAFE_BOX[3] - SAFE_BOX[1]
    scale = min(box_w / (max(xs) - min(xs)), box_h / (max(ys) - min(ys)))
    ox = SAFE_BOX[0] + (box_w - (max(xs) - min(xs)) * scale) / 2 - min(xs) * scale
    oy = SAFE_BOX[1] + (box_h - (max(ys) - min(ys)) * scale) / 2 - min(ys) * scale
    to_px = lambda x, y: (x * scale + ox, y * scale + oy)

    # The overview shows more than the circuit; make sure map data covers the whole canvas.
    inv = lambda px_, py_: ((px_ - ox) / scale, (py_ - oy) / scale)
    corners = [inv(0, 0), inv(CANVAS[0], CANVAS[1])]
    lons = [proj.lon0 + x / proj.kx for x, _ in corners]
    lats = [proj.lat0 - y / proj.ky for _, y in corners]
    canvas_bbox = [round(min(lons), 4), round(min(lats), 4), round(max(lons), 4), round(max(lats), 4)]
    if (canvas_bbox[0] < spec["bbox"][0] or canvas_bbox[1] < spec["bbox"][1]
            or canvas_bbox[2] > spec["bbox"][2] or canvas_bbox[3] > spec["bbox"][3]):
        bg_nodes, bg_ways, bg_relations = parse(fetch(canvas_bbox, spec["id"] + "_canvas"))
        nodes, ways, relations = {**bg_nodes, **nodes}, {**bg_ways, **ways}, bg_relations + relations

    sectors, raw = micro_sectors(dense)
    # Lap-time calibration: scale every target speed (fitted by tools/calibrate.py).
    for sector in sectors:
        sector["target_speed_kmh"] = round(sector["target_speed_kmh"] * spec.get("speed_scale", 1.0), 1)
    geometry_m = polyline_length(dense)
    outline = resample(dense, count=spec.get("point_count", 300))
    points = [[round(c, 1) for c in to_px(*p)] for p in outline]

    # Sector splits snap to the start of the straight nearest to each third.
    starts = [s["start_index"] / len(dense) for s in raw if s["type"] == "straight" and s["start_index"] > 0]
    splits = sorted(min(starts, key=lambda f: abs(f - t)) for t in (1 / 3, 2 / 3)) if len(starts) >= 2 else [1 / 3, 2 / 3]

    track = {
        "name": spec["name"],
        "nationality": spec["nationality"],
        "length_km": spec.get("length_km", round(geometry_m / 1000, 3)),
        # The game races (pack options.json "laps") x lap_modifier laps, so this
        # sets the race distance, not the lap time.
        "lap_modifier": round(spec["race_laps"] / BASE_RACE_LAPS, 4) if "race_laps" in spec else spec.get("lap_modifier", 1.0),
        "dnf_modifier": spec.get("dnf_modifier", 1.0),
        "overtaking_difficulty": spec.get("overtaking_difficulty", 0.6),
        "pit_lane_loss_s": spec.get("pit_lane_loss_s", 20.0),
        "tyre_wear_mult": spec.get("tyre_wear_mult", 0.9),
        "fuel_consumption": spec.get("fuel_consumption", 1.0),
        "wet_weather_probability_multiplier": spec.get("wet_weather_probability_multiplier", 1.0),
        # Points are image pixels. Without this flag the game re-fits the
        # points' bounding box into its own frame and cars leave the drawn track.
        "use_raw_canvas_coordinates": True,
        "raw_canvas_size": list(CANVAS),
        "hide_polyline_visual": True,
        "racing_surface": {"enabled": True, "mode": "road_course", "width_m": spec.get("width_m", 11.0),
                           "edge_margin_m": 0.6, "corridor_count": 3, "visual_lateral_scale": 1.5},
        "starting_grid": {"pole_side": spec.get("pole_side", "left"), "row_spacing_m": 10.0,
                          "column_spacing_m": 3.0, "stagger_m": 4.0},
        "drs_zones": drs_zones(spec.get("drs_zones", []), raw, len(dense)),
        "sector_splits": splits,
        "micro_sectors": sectors,
        "points": points,
        "source": {"generator": "tools/osm_track.py", "osm_bbox": spec["bbox"],
                   "osm_ways": loop_ways, "geometry_length_m": round(geometry_m),
                   "attribution": ATTRIBUTION, "notes": spec.get("notes", ""),
                   "speed_scale": spec.get("speed_scale", 1.0),
                   # pixel = (metres from (lat0, lon0)) * scale + offset; lets specs place
                   # map-relative features (e.g. historic_forest) from pixel positions.
                   "canvas_transform": {"lat0": proj.lat0, "lon0": proj.lon0, "kx": proj.kx, "ky": proj.ky,
                                        "scale": scale, "ox": ox, "oy": oy}},
    }
    out_json = season_dir / "tracks" / f"{spec['id']}.json"
    out_png = season_dir / "assets" / "tracks" / f"{spec['id']}.png"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(track, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Long circuits shrink to a thin line at map scale; keep the drawn track readable.
    width_px = max(spec.get("width_m", 11.0) * scale * 1.4, spec.get("min_track_px", 9))
    pit_px = [to_px(*p) for p in pit_m] if pit_m else None
    render(out_png, proj, to_px, nodes, ways, relations, [to_px(*p) for p in dense[::2]], pit_px, width_px, spec["id"], scale, spec)

    print(f"{spec['id']}: {len(loop_ways)} ways, {geometry_m:.0f} m traced (game length {track['length_km']} km), "
          f"{len(points)} points, {len(sectors)} micro-sectors (from the start line)")
    for s in sectors:
        print(f"  {s['type']:8s} {s['length_pct']:5.1f}%  {s['target_speed_kmh']:.0f} km/h")
    for z in track["drs_zones"]:
        print(f"  DRS {z['start_progress']:.3f} -> {z['end_progress']:.3f} (detection {z['detection_progress']:.3f})")
    print(f"wrote {out_json.relative_to(REPO)} and {out_png.relative_to(REPO)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("specs", nargs="+", help="track spec JSON file(s)")
    for spec in parser.parse_args().specs:
        build(spec)


if __name__ == "__main__":
    main()
