"""Pit-lane geometry from OpenStreetMap and an estimate of the pit-lane time loss.

For each track spec (any season or base) it finds the pit lane in the cached
OSM extract: raceway or service ways named like a pit lane ("Pit Lane",
"Boxengasse", "Pitstraat", ...) or tagged service=pit_lane / raceway=pit_lane,
joined into one line, and keeps the one that runs closest to the start line.
Then it measures:

    pit_lane_length_m   along the pit lane, end to end as mapped
    bypassed_m          the racing line between the points where the pit lane leaves and rejoins it

and estimates the game's pit_lane_loss_s (the drive-through loss; the game
adds the service time itself). The speed limit holds only between the pit-in
and pit-out lines (limit_zone_m: a published pit_lane_length_m from
venue_facts.csv, else LIMIT_SHARE of the mapped lane); the rest of the lane,
the entry and exit roads, is driven at ENTRY_KMH:

    loss = zone / pit_limit + (lane - zone) / entry_speed - lane / track_speed

pit_limit comes from docs/venues/venue_facts.csv (pit_speed_limit_kmh, default
60 km/h), track_speed from the fastest race lap in docs/venues/race_stats.csv
times STRAIGHT_FACTOR (the pit straight is quicker than the lap average), and
A published loss for the same series in venue_facts.csv (pit_loss_s) wins
over the estimate (tools/venue_stats.py --apply writes it into the spec).

    python -I tools/pit_lane.py bases/dtm-era4/track_specs/*.json [--csv]
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import osm_track as o  # noqa: E402
from track_inventory import venue_key  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
FACTS = REPO / "docs" / "venues" / "venue_facts.csv"
STATS = REPO / "docs" / "venues" / "race_stats.csv"
PIT_NAME = re.compile(r"\bpit|boxen(gasse|stra)|pitstraat|voie des stands|corsia box", re.I)
STRAIGHT_FACTOR = 1.15
ENTRY_KMH = 110.0     # mean speed on the pit entry and exit roads, outside the limit
LIMIT_SHARE = 0.4     # limit zone / mapped lane where nothing is published (Hockenheim 0.36,
                      # Nürburgring 0.40, Red Bull Ring 0.33 from SRO briefings)
DEFAULT_LIMIT = 60.0


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def fact(venue: str, field: str, track_id: str = "", series: str = "") -> str | None:
    """Latest non-estimate value of a field for a venue (or a track id) in
    venue_facts.csv; with series, only facts whose applies_to names it."""
    hits = [r for r in read_rows(FACTS) if r["field"] == field and r["venue"] == venue
            and r.get("track", "") in ("", track_id) and r["value"] and r["status"] != "estimate"
            and (not series or re.search(rf"{series}", r.get("applies_to", ""), re.I))]
    return hits[-1]["value"] if hits else None


def pit_candidates(t: dict) -> list[list[tuple[float, float]]]:
    """Pit-lane ways, chained where they share end nodes, in metres."""
    ways = [w for w in t["ways"].values()
            if w["tags"].get("highway") in ("raceway", "service")
            and (PIT_NAME.search(w["tags"].get("name", "")) or "pit" in w["tags"].get("service", "")
                 or "pit" in w["tags"].get("raceway", ""))
            and not re.search(r"disused|abandoned|kart", w["tags"].get("name", ""), re.I)]
    chains = [list(w["nds"]) for w in ways]
    merged = True
    while merged:
        merged = False
        for i in range(len(chains)):
            for j in range(len(chains)):
                if i != j and chains[i] and chains[j]:
                    a, b = chains[i], chains[j]
                    if a[-1] == b[0]:
                        chains[i], chains[j], merged = a + b[1:], [], True
                    elif a[-1] == b[-1]:
                        chains[i], chains[j], merged = a + b[::-1][1:], [], True
        chains = [c for c in chains if c]
    proj, nodes = t["proj"], t["nodes"]
    return [[proj.metres(*nodes[n]) for n in c if n in nodes] for c in chains]


def measure(spec: dict) -> dict:
    t = o.trace(spec)
    dense = t["dense"]
    step = o.polyline_length(dense) / len(dense)
    best = None
    for pit in pit_candidates(t):
        if len(pit) < 2:
            continue
        ia = min(range(len(dense)), key=lambda i: math.dist(dense[i], pit[0]))
        ib = min(range(len(dense)), key=lambda i: math.dist(dense[i], pit[-1]))
        gap = max(math.dist(dense[ia], pit[0]), math.dist(dense[ib], pit[-1]))
        mid = min(math.dist(dense[0], p) for p in pit)   # how close it runs to the start line
        n = len(dense)
        arc = min((ib - ia) % n, (ia - ib) % n) * step
        length = o.polyline_length(pit, closed=False)
        if length < 150 or arc > 0.5 * n * step:
            continue
        score = mid + gap
        if best is None or score < best["score"]:
            best = {"score": score, "pit_lane_length_m": round(length), "bypassed_m": round(arc),
                    "end_gap_m": round(gap), "from_start_m": round(mid)}
    return best or {}


def fastest_lap_s(venue: str, series: str) -> float | None:
    """Fastest race lap at the venue in our results (any year of the series)."""
    best = None
    for r in read_rows(STATS):
        if r["venue"] == venue and r["series"] == series:
            for row in read_rows(REPO / r["file"]):
                m = re.match(r"^(?:(\d+):)?(\d+\.\d+)$", (row.get("fastest_lap") or "").strip())
                if m:
                    s = int(m.group(1) or 0) * 60 + float(m.group(2))
                    best = s if best is None or s < best else best
    return best


def estimate(spec: dict, geo: dict, series: str) -> dict:
    venue = venue_key(spec.get("name", spec["id"]), "", str(spec.get("length_km", ""))) or spec["id"]
    out = {"track": spec["id"], "venue": venue, **{k: v for k, v in geo.items() if k != "score"}}
    limit = float(fact(venue, "pit_speed_limit_kmh", spec["id"], series)
                  or fact("all", "pit_speed_limit_kmh", "", series) or DEFAULT_LIMIT)
    lap = fastest_lap_s(venue, series)
    published = fact(venue, "pit_loss_s", spec["id"], series)
    out.update({"limit_kmh": limit, "fastest_lap_s": lap, "published_s": published, "now_s": spec.get("pit_lane_loss_s")})
    zone = fact(venue, "pit_lane_length_m", spec["id"])
    if geo and lap and spec.get("length_km"):
        lane = geo["pit_lane_length_m"]
        zone = min(float(zone), lane) if zone else LIMIT_SHARE * lane
        v_track = spec["length_km"] * 1000 / lap * STRAIGHT_FACTOR
        out["limit_zone_m"] = round(zone)
        out["estimate_s"] = round(zone / (limit / 3.6) + (lane - zone) / (ENTRY_KMH / 3.6) - geo["bypassed_m"] / v_track, 1)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("specs", nargs="+", type=Path)
    ap.add_argument("--series", default="dtm", help="whose fastest laps set the track speed")
    ap.add_argument("--csv", action="store_true", help="print venue_facts.csv rows for the measured lengths")
    a = ap.parse_args()
    rows = []
    for p in a.specs:
        spec = json.loads(p.read_text(encoding="utf-8"))
        try:
            geo = measure(spec)
        except SystemExit as e:
            geo = {}
            print(f"{spec['id']}: {e}", file=sys.stderr)
        rows.append(estimate(spec, geo, a.series))
    if a.csv:
        for r in rows:
            if r.get("pit_lane_length_m"):
                print(f"{r['venue']},{r['track']},osm_pit_lane_m,{r['pit_lane_length_m']},m,,derived,"
                      f"OpenStreetMap via tools/pit_lane.py,\"pit lane as mapped; leaves and rejoins the racing line "
                      f"{r['bypassed_m']} m apart\"")
        return
    print(f"{'track':16} {'pit m':>6} {'zone':>5} {'bypass':>6} {'gap':>4} {'limit':>5} {'lap s':>6} {'est s':>6} {'pub s':>6} {'now':>5}")
    for r in rows:
        print(f"{r['track']:16} {r.get('pit_lane_length_m', '-'):>6} {r.get('limit_zone_m', '-'):>5} {r.get('bypassed_m', '-'):>6} {r.get('end_gap_m', '-'):>4} "
              f"{r['limit_kmh']:>5.0f} {r['fastest_lap_s'] or 0:>6.1f} {r.get('estimate_s', '-'):>6} "
              f"{r['published_s'] or '-':>6} {r['now_s']:>5}")


if __name__ == "__main__":
    main()
