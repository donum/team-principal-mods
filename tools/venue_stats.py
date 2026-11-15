"""Per-race venue statistics from our own results files, for every series.

Reads seasons/*/research/calendar.csv and research/results/NN-<venue>-race*.csv
(DTM, ITC, F1, BTCC: any season that has results) and writes one row per race
to docs/venues/race_stats.csv:

    starters, classified, retirements by cause (accident / mechanical / other),
    grid-to-finish swaps (pairs of classified cars that finished in the other
    order than they started: a proxy for overtakes, pit-stop shuffles included),
    safety cars and wet running named in the notes.

The game's track values are relative multipliers (see docs/venues/README.md),
so --pack turns the stats into suggestions for one pack: each venue's rate
divided by the mean of the same series over the same years.

    python -I tools/venue_stats.py                     rebuild docs/venues/race_stats.csv
    python -I tools/venue_stats.py --pack seasons/dtm-2013 [--years 2012-2013]
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from track_inventory import venue_key  # noqa: E402  (one venue key for the whole repo)

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "docs" / "venues" / "race_stats.csv"
FACTS = REPO / "docs" / "venues" / "venue_facts.csv"

ACCIDENT = re.compile(r"accident|crash|collision|contact|damage|spun|spin|off\b|hit\b|barrier|wall", re.I)
MECHANICAL = re.compile(r"engine|gearbox|wheel|brake|suspension|electr|hydraul|fuel|drive ?shaft|clutch|"
                        r"puncture|tyre|overheat|oil|water|throttle|steering|transmission|power|exhaust|"
                        r"radiator|alternator|battery|differential|turbo|mechanical|technical|fire|halfshaft", re.I)
SAFETY_CAR = re.compile(r"safety car|\bSC\b", re.I)
WET = re.compile(r"\bwet|rain|damp|drying|shower|intermediate", re.I)
COLUMNS = ["series", "season", "round", "venue", "event", "layout", "length_km", "laps", "file",
           "starters", "classified", "dnf", "dnf_accident", "dnf_mechanical", "dnf_other",
           "with_grid", "swaps", "swaps_per_car", "mean_abs_change", "safety_car", "wet"]


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def grid_of(row: dict) -> int | None:
    m = re.search(r"(?:source )?grid(?:/qual pos)? (\d+)", row.get("notes") or "")
    return int(m.group(1)) if m else None


def race_stats(rows: list[dict]) -> dict:
    started = [r for r in rows if (r.get("status") or "").upper() not in ("DNQ", "DNS", "DNPQ", "EXCL", "WD")]
    classified = [r for r in started if (r.get("status") or "").lower() == "classified"]
    out = [r for r in started if (r.get("status") or "").upper() in ("DNF", "RET", "NC")]
    acc = sum(1 for r in out if ACCIDENT.search(r.get("notes") or "") and not MECHANICAL.search((r.get("notes") or "").split(";")[0]))
    mech = sum(1 for r in out if MECHANICAL.search((r.get("notes") or "").split(";")[0]))
    pairs = [(grid_of(r), int(r["pos"])) for r in classified if grid_of(r) and (r.get("pos") or "").isdigit()]
    swaps = sum(1 for i, (g1, p1) in enumerate(pairs) for g2, p2 in pairs[i + 1:] if (g1 - g2) * (p1 - p2) < 0)
    # Changes between the finishing order and the grid order of the same cars (rank, not raw slot).
    gr = {g: i for i, g in enumerate(sorted(g for g, _ in pairs))}
    pr = {p: i for i, p in enumerate(sorted(p for _, p in pairs))}
    change = statistics.mean(abs(gr[g] - pr[p]) for g, p in pairs) if pairs else None
    text = " ".join(r.get("notes") or "" for r in rows)
    laps = max((int(r["laps"]) for r in rows if (r.get("laps") or "").isdigit()), default=None)
    return {
        "laps": laps, "starters": len(started), "classified": len(classified), "dnf": len(out),
        "dnf_accident": acc, "dnf_mechanical": mech, "dnf_other": len(out) - acc - mech,
        "with_grid": len(pairs), "swaps": swaps,
        "swaps_per_car": round(swaps / len(pairs), 2) if pairs else "",
        "mean_abs_change": round(change, 2) if change is not None else "",
        "safety_car": "yes" if SAFETY_CAR.search(text) else "",
        "wet": "yes" if WET.search(text) else "",
    }


def collect() -> list[dict]:
    rows = []
    for season in sorted((REPO / "seasons").iterdir()):
        results = season / "research" / "results"
        if not results.is_dir():
            continue
        series = season.name.split("-")[0]
        cal = {r.get("round", "").strip(): r for r in read_rows(season / "research" / "calendar.csv")}
        for f in sorted(results.glob("*.csv")):
            m = re.match(r"^(\d+)-(.+?)-(race\w*|qualrace|heat\w*|final\w*)\.csv$", f.name)
            if not m:
                continue
            rnd = str(int(m.group(1)))
            c = cal.get(rnd, {})
            name = (c.get("venue") or m.group(2)).strip()
            layout, length = (c.get("circuit_layout") or "").strip(), (c.get("length_km") or "").strip()
            key = venue_key(name, layout, length) or venue_key(m.group(2)) or name
            rows.append({"series": series, "season": season.name, "round": rnd, "venue": key, "event": name,
                         "layout": layout, "length_km": length, "file": f.relative_to(REPO).as_posix(),
                         **race_stats(read_rows(f))})
    return rows


def write(rows: list[dict]) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, COLUMNS, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT.relative_to(REPO)}: {len(rows)} races, {len({r['venue'] for r in rows})} venues")


def by_venue(rows: list[dict]) -> dict[str, dict]:
    """Rates per venue: retirements per starter, swaps per car, share of races with a safety car / rain."""
    acc = defaultdict(lambda: defaultdict(float))
    for r in rows:
        a = acc[r["venue"]]
        a["races"] += 1
        a["starters"] += r["starters"]
        a["dnf"] += r["dnf"]
        a["dnf_accident"] += r["dnf_accident"]
        a["dnf_mechanical"] += r["dnf_mechanical"]
        a["swaps"] += r["swaps"]
        a["with_grid"] += r["with_grid"]
        a["safety_car"] += r["safety_car"] == "yes"
        a["wet"] += r["wet"] == "yes"
    out = {}
    for v, a in acc.items():
        out[v] = {"races": int(a["races"]),
                  "dnf_rate": a["dnf"] / a["starters"] if a["starters"] else None,
                  "accident_rate": a["dnf_accident"] / a["starters"] if a["starters"] else None,
                  "swaps_per_car": a["swaps"] / a["with_grid"] if a["with_grid"] else None,
                  "sc_share": a["safety_car"] / a["races"], "wet_share": a["wet"] / a["races"]}
    return out


def pack_report(pack: Path, rows: list[dict], years: tuple[int, int] | None) -> None:
    """Suggested relative values for the tracks of one pack."""
    season = json.loads((pack / "season.json").read_text(encoding="utf-8"))
    series = pack.name.split("-")[0]
    year = int(pack.name.split("-")[1])
    lo, hi = years or (year, year)
    pool = [r for r in rows if r["series"] == series and lo <= int(r["season"].split("-")[1]) <= hi]
    venues = by_venue(pool)
    total = by_venue([{**r, "venue": "*"} for r in pool])["*"]
    base = season.get("base")
    specs = {}
    for d in [pack] + ([REPO / "bases" / base] if base else []):
        for p in (d / "track_specs").glob("*.json"):
            specs.setdefault(p.stem, p)
    schedule = json.loads((pack / "data" / "schedule.json").read_text(encoding="utf-8"))
    tids = list(dict.fromkeys(t for t in schedule if t and t not in ("private", "test")))
    print(f"{series} {lo}-{hi}: {len(pool)} races, DNF {total['dnf_rate']:.1%} of starters, "
          f"{total['swaps_per_car']:.2f} swaps per car\n")
    rows_out = []
    for tid in tids:
        spec = json.loads(specs[tid].read_text(encoding="utf-8")) if tid in specs else {}
        key = venue_key(spec.get("name", tid), "", str(spec.get("length_km", ""))) or venue_key(tid) or tid
        rows_out.append((tid, key, spec, venues.get(key)))
    # The pack's own mean overtaking value is the anchor: the suggestion moves each
    # venue around it by the inverse of its swap ratio.
    wet = wet_multipliers(pack, [t for t in schedule if t and t not in ("private", "test")])
    od_now = [s.get("overtaking_difficulty", 0.6) for _, _, s, _ in rows_out]
    od_mean = statistics.mean(od_now) if od_now else 0.6
    print(f"{'track':16} {'venue':24} {'races':>5} {'dnf%':>6} {'ratio':>6} {'now':>5} {'sugg':>5}   "
          f"{'swaps':>5} {'ratio':>6} {'now':>5} {'sugg':>5}   {'SC':>4} {'wet':>4}   {'rain x':>6} {'now':>5}")
    for tid, key, spec, v in rows_out:
        if not v:
            print(f"{tid:16} {key:24} {'0':>5}  (no results in {lo}-{hi})")
            continue
        dr, sr = shrunk_ratios(v, total)
        print(f"{tid:16} {key:24} {v['races']:>5} {v['dnf_rate']:>6.1%} {dr:>6.2f} {spec.get('dnf_modifier', 1.0):>5} {dr:>5.2f}   "
              f"{v['swaps_per_car'] or 0:>5.2f} {sr:>6.2f} {spec.get('overtaking_difficulty', 0.6):>5} {od_mean / sr:>5.2f}   "
              f"{v['sc_share']:>4.0%} {v['wet_share']:>4.0%}   {wet.get(tid, '-'):>6} "
              f"{spec.get('wet_weather_probability_multiplier', 1.0):>5}")
    print(f"\nratio: the venue's rate over the series mean, pulled towards 1.0 as if the mean had {PRIOR_RACES} more races there.\n"
          f"dnf_modifier = ratio. overtaking_difficulty = pack mean ({od_mean:.2f}) / swap ratio. Check with tools/simulate.py.\n"
          f"rain x: rain-day chance in the race month over the calendar mean (venue_facts climate rows); --apply writes it.")


PRIOR_RACES = 2   # weight of the series mean, in races, when a venue has few

# Facts that go straight into a track spec: venue_facts field -> spec key.
SPEC_FIELDS = {"pole_side": "pole_side", "pit_loss_s": "pit_lane_loss_s"}


def latest_facts(venue: str, track: str, series: str) -> dict[str, str]:
    """The last non-empty verified/derived value per field for a venue and track,
    from facts that hold for this series ("DTM 2013", "DTM 2012-2014"...): a GT4 pit
    delta or an F1 figure is kept for reference but never written into a DTM pack."""
    out = {}
    for r in read_rows(FACTS):
        if (r["venue"] == venue and r.get("track", "") in ("", track) and r["value"] and r["status"] != "estimate"
                and re.search(rf"\b{series}\b", r.get("applies_to", ""), re.I)):
            out[r["field"]] = r["value"]
    return out


def sim_rows(sim_dir: Path) -> list[dict]:
    """The same per-race stats from tools/simulate.py output: run-*/races.jsonl
    (every race of the run), else the saves' race_results (the current season).
    A retirement counts only when the car is unclassified, as in the real results."""
    rows = []
    for run in sorted(sim_dir.glob("run-*")):
        races = []
        if (run / "races.jsonl").exists():
            races = [json.loads(l) for l in (run / "races.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        else:
            for save in sorted(run.glob("saves/*.json")):
                try:
                    races += json.loads(save.read_text(encoding="utf-8")).get("race_results", [])
                except (OSError, ValueError):
                    continue
        for r in races:
            grid = r.get("grid") or []
            out = set(r.get("unclassified") if r.get("unclassified") is not None else r.get("retired") or [])
            reasons = r.get("dnf_reason") or {}
            fin = {d: int(p) for d, p in (r.get("drivers") or {}).items() if str(p).isdigit() and d not in out}
            pairs = [(grid.index(d) + 1, p) for d, p in fin.items() if d in grid]
            swaps = sum(1 for i, (g1, p1) in enumerate(pairs) for g2, p2 in pairs[i + 1:] if (g1 - g2) * (p1 - p2) < 0)
            acc = sum(1 for d in out if reasons.get(d) in ("crash", "accident", "collision", "spin", "damage"))
            ev = r.get("regulation_evidence") or {}
            rows.append({"series": "sim", "season": run.name, "round": r.get("week"),
                         "venue": r.get("track"), "starters": len(grid), "classified": len(fin), "dnf": len(out),
                         "dnf_accident": acc, "dnf_mechanical": len(out) - acc,
                         "with_grid": len(pairs), "swaps": swaps,
                         "swaps_per_car": round(swaps / len(pairs), 2) if pairs else "",
                         "safety_car": "yes" if ev.get("safety_car_count") else "",
                         "wet": "yes" if "wet race" in (r.get("weather") or "").lower() else ""})
    return rows


# swaps ~ overtaking_difficulty ** (-1 / OVERTAKE_POWER). Measured on DTM 2013: values
# 20% lower gave 21% more swaps (wear-v2 -> venues-fit1), so about 1.2.
OVERTAKE_POWER = 1.2


def sim_fit(pack: Path, sim_dirs: list[Path], real: list[dict], years: tuple[int, int] | None,
            write: bool = False, overtake_factor: float = 1.0, only: str | None = None) -> None:
    """Calibrate dnf_modifier and overtaking_difficulty against the real races,
    like tools/calibrate.py does for lap times: pool the given simulate.py runs
    (all made with the same track values, the ones in dist/<pack>), then

        dnf_modifier          *= target retirement rate / simulated rate
        overtaking_difficulty *= (simulated swaps / target swaps) ** OVERTAKE_POWER

    The target per venue is the real rate (years) pulled towards the series mean
    (PRIOR_RACES). The game rolls failures every lap, so a long race (Brands
    Hatch, 98 laps) retires far more cars at the same modifier; a track with
    fewer than 2 simulated races is predicted from the per-lap rate of the others.
    --write puts the new values into the specs (or the base's track_overrides);
    only="dnf" or "overtaking" writes just that one."""
    series = pack.name.split("-")[0]
    year = int(pack.name.split("-")[1])
    lo, hi = years or (year, year)
    pool = [r for r in real if r["series"] == series and lo <= int(r["season"].split("-")[1]) <= hi]
    real_v, real_t = by_venue(pool), by_venue([{**r, "venue": "*"} for r in pool])["*"]
    season = json.loads((pack / "season.json").read_text(encoding="utf-8"))
    folder = season.get("pack_folder", pack.name.replace("-", ""))
    # The values the simulated races ran with: the pack copy in the first run's
    # sandbox (dist/ may already hold newer values), else dist/.
    sandbox = sorted(sim_dirs[0].glob(f"run-*/data/{folder}/tracks"))
    dist = sandbox[0].parent if sandbox else REPO / "dist" / folder
    schedule = json.loads((pack / "data" / "schedule.json").read_text(encoding="utf-8"))
    tids = list(dict.fromkeys(t for t in schedule if t and t not in ("private", "test")))
    rows = [r for d in sim_dirs for r in sim_rows(d)]
    if not rows:
        raise SystemExit("no simulated races in " + ", ".join(map(str, sim_dirs)))
    sv, st = by_venue(rows), by_venue([{**r, "venue": "*"} for r in rows])["*"]
    now = {t: json.loads((dist / "tracks" / f"{t}.json").read_text(encoding="utf-8")) for t in tids
           if (dist / "tracks" / f"{t}.json").exists()}
    laps = {t: round(now[t].get("lap_modifier", 1.0) * 50) for t in now}
    # Retirements per lap at modifier 1.0, from the tracks the sims raced at least twice.
    per_lap = [sv[t]["dnf_rate"] / now[t].get("dnf_modifier", 1.0) / laps[t]
               for t in tids if t in sv and t in now and sv[t]["races"] >= 2]
    k = statistics.mean(per_lap) if per_lap else None
    print(f"{len(rows)} simulated races: DNF {st['dnf_rate']:.1%} (real {real_t['dnf_rate']:.1%}), "
          f"swaps/car {st['swaps_per_car']:.2f} (real {real_t['swaps_per_car']:.2f})"
          + (f"; {k:.3%} of starters retire per lap at dnf_modifier 1.0" if k else ""))
    print(f"{'track':16} {'laps':>4} {'sim':>4}  {'dnf sim':>7} {'target':>6} {'now':>5} {'new':>5}   "
          f"{'swaps sim':>9} {'target':>6} {'now':>5} {'new':>5}")
    new_vals = {}
    for tid in tids:
        if tid not in now:
            continue
        spec = spec_path(pack, tid)
        name = json.loads(spec.read_text(encoding="utf-8")).get("name", tid) if spec else tid
        rv = real_v.get(venue_key(name, "", str(now[tid].get("length_km", ""))) or tid)
        dr, sr = shrunk_ratios(rv, real_t) if rv else (1.0, 1.0)
        # overtake_factor: a game is more fun with a bit more passing than the real races had
        t_dnf, t_swaps = dr * real_t["dnf_rate"], sr * real_t["swaps_per_car"] * overtake_factor
        dm, od = now[tid].get("dnf_modifier", 1.0), now[tid].get("overtaking_difficulty", 1.0)
        v = sv.get(tid)
        n = v["races"] if v else 0
        # Simulated rate, pulled towards the per-lap prediction when there are few races.
        pred = k * laps[tid] * dm if k else st["dnf_rate"]
        s_dnf = (n * v["dnf_rate"] + PRIOR_RACES * pred) / (n + PRIOR_RACES) if v else pred
        s_sw = (n * (v["swaps_per_car"] or 0) + PRIOR_RACES * st["swaps_per_car"]) / (n + PRIOR_RACES) if v \
            else st["swaps_per_car"]
        new_dm = round(min(3.0, max(0.15, dm * t_dnf / s_dnf)), 2) if s_dnf else dm
        new_od = round(min(1.5, max(0.05, od * (s_sw / t_swaps) ** OVERTAKE_POWER)), 2) if t_swaps else od
        new_vals[tid] = {k: v for k, v in (("dnf_modifier", new_dm), ("overtaking_difficulty", new_od))
                         if only is None or k.startswith(only[:3])}
        print(f"{tid:16} {laps[tid]:>4} {n:>4}  {s_dnf:>7.1%} {t_dnf:>6.1%} {dm:>5} {new_dm:>5}   "
              f"{s_sw:>9.2f} {t_swaps:>6.2f} {od:>5} {new_od:>5}")
    if write:
        for tid, vals in new_vals.items():
            set_track_values(pack, tid, vals)


MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def wet_multipliers(pack: Path, tids: list[str]) -> dict[str, float]:
    """wet_weather_probability_multiplier per track: the chance of a rain day
    (>= 1 mm) in the race month at the venue, over the mean of the pack's
    calendar. The game multiplies its base wet chance by it, so the season's
    rain stays the same overall and moves to the wetter venues and months.
    A track raced twice gets the mean of its months."""
    cal = read_rows(pack / "research" / "calendar.csv")
    chances: dict[str, list[float]] = defaultdict(list)
    for r, tid in zip(cal, tids):
        m = re.match(r"\d{4}-(\d{2})", r.get("date", ""))
        if not m:
            continue
        month = int(m.group(1)) - 1
        key = venue_key(r.get("venue", ""), r.get("circuit_layout", ""), r.get("length_km", "")) or tid
        days = [f["value"] for f in read_rows(FACTS) if f["venue"] == key and f["field"] == f"rain_days_{MONTHS[month]}"
                and f["value"] and f["status"] != "estimate"]
        if days:
            chances[tid].append(float(days[-1]) / MONTH_DAYS[month])
    if not chances:
        return {}
    mean = statistics.mean(c for cs in chances.values() for c in cs)
    return {tid: round(statistics.mean(cs) / mean, 2) for tid, cs in chances.items()}


def spec_path(pack: Path, tid: str) -> Path | None:
    """The spec a pack's track is built from (track_art.json, the pack, then its base)."""
    art = json.loads((pack / "track_art.json").read_text(encoding="utf-8")) if (pack / "track_art.json").exists() else {}
    if tid in art.get("tracks", {}) and art["tracks"][tid].get("spec"):
        return REPO / art["tracks"][tid]["spec"]
    base = json.loads((pack / "season.json").read_text(encoding="utf-8")).get("base")
    for d in [pack] + ([REPO / "bases" / base] if base else []):
        if (d / "track_specs" / f"{tid}.json").exists():
            return d / "track_specs" / f"{tid}.json"
    return None


def write_spec_values(path: Path, values: dict) -> None:
    """Set top-level scalar keys in a hand-formatted spec and keep its layout.
    A key the spec doesn't have yet goes in just before "notes"."""
    text = path.read_text(encoding="utf-8")
    for k, v in values.items():
        lit = json.dumps(v, ensure_ascii=False)
        rx = re.compile(r'^(\s*"' + re.escape(k) + r'":\s*)("[^"]*"|[-0-9.eE]+|true|false|null)', re.M)
        if rx.search(text):
            text = rx.sub(lambda m: m.group(1) + lit, text, count=1)
        else:
            m = re.search(r'^(\s*)"notes":', text, re.M)
            if not m:
                raise SystemExit(f"{path}: no {k} and no notes to insert before")
            text = text[:m.start()] + f'{m.group(1)}"{k}": {lit},' + text[m.start():]
        json.loads(text)   # still valid JSON
    path.write_text(text, encoding="utf-8")


def set_track_values(pack: Path, tid: str, values: dict) -> None:
    """Write track values for a pack's track: into the spec when the pack or its
    base owns it (keeping the spec's layout), else into the base's (or the
    pack's season.json) track_overrides. pole_side becomes starting_grid there."""
    path = spec_path(pack, tid)
    if not path:
        print(f"{tid}: no spec, skipped")
        return
    season = json.loads((pack / "season.json").read_text(encoding="utf-8"))
    base = season.get("base")
    owners = {pack.resolve()} | ({(REPO / "bases" / base).resolve()} if base else set())
    if path.parent.parent.resolve() in owners:
        spec = json.loads(path.read_text(encoding="utf-8"))
        diff = {k: v for k, v in values.items() if spec.get(k) != v}
        if diff:
            write_spec_values(path, diff)
            print(f"{tid}: {diff} -> {path.relative_to(REPO)}")
        return
    owner_file = REPO / "bases" / base / "base.json" if base else pack / "season.json"
    doc = json.loads(owner_file.read_text(encoding="utf-8"))
    over = doc.setdefault("track_overrides", {}).setdefault(tid, {})
    values = dict(values)
    if "pole_side" in values:
        values["starting_grid"] = {"pole_side": values.pop("pole_side"), "row_spacing_m": 10.0,
                                   "column_spacing_m": 3.0, "stagger_m": 4.0}
    diff = {k: v for k, v in values.items() if over.get(k) != v}
    if diff:
        over.update(diff)
        owner_file.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{tid}: {diff} -> {owner_file.relative_to(REPO)} track_overrides")


def apply_facts(pack: Path) -> None:
    """Write sourced facts into the track values the pack uses (set_track_values)."""
    schedule = json.loads((pack / "data" / "schedule.json").read_text(encoding="utf-8"))
    wet = wet_multipliers(pack, [t for t in schedule if t and t not in ("private", "test")])
    for tid in dict.fromkeys(t for t in schedule if t and t not in ("private", "test")):
        path = spec_path(pack, tid)
        if not path:
            continue
        spec = json.loads(path.read_text(encoding="utf-8"))
        key = venue_key(spec.get("name", tid), "", str(spec.get("length_km", ""))) or tid
        facts = {SPEC_FIELDS[f]: v for f, v in latest_facts(key, tid, pack.name.split("-")[0]).items() if f in SPEC_FIELDS}
        if "pit_lane_loss_s" in facts:
            facts["pit_lane_loss_s"] = float(facts["pit_lane_loss_s"])
        if tid in wet:
            facts["wet_weather_probability_multiplier"] = wet[tid]
        set_track_values(pack, tid, facts)


def shrunk_ratios(v: dict, total: dict) -> tuple[float, float]:
    """Retirement and swap ratios against the series mean, shrunk for small samples."""
    n = v["races"]
    w = n / (n + PRIOR_RACES)
    dr = w * (v["dnf_rate"] / total["dnf_rate"]) + (1 - w) if total["dnf_rate"] else 1.0
    sr = w * (v["swaps_per_car"] / total["swaps_per_car"]) + (1 - w) if v["swaps_per_car"] and total["swaps_per_car"] else 1.0
    return round(dr, 2), round(sr, 2)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pack", type=Path)
    ap.add_argument("--years", help="e.g. 2012-2013 (default: the pack's year)")
    ap.add_argument("--apply", action="store_true",
                    help="write sourced facts (pole side, published pit loss) into the pack's track specs")
    ap.add_argument("--sim", type=Path, nargs="+",
                    help="tools/simulate.py output folders (same track values): fit dnf_modifier and "
                         "overtaking_difficulty against the real races")
    ap.add_argument("--fit", action="store_true", help="with --sim: write the fitted values")
    ap.add_argument("--fit-only", choices=["dnf", "overtaking"],
                    help="with --fit: write only this value (overtaking stops responding below ~0.3)")
    ap.add_argument("--overtake-factor", type=float, default=1.0,
                    help="with --sim: aim for this many times the real swaps (DTM 2013: 1.15)")
    a = ap.parse_args()
    rows = collect()
    write(rows)
    if a.pack:
        pack = a.pack if a.pack.is_absolute() else REPO / a.pack
        if a.apply:
            apply_facts(pack)
        years = tuple(int(y) for y in a.years.split("-")) if a.years else None
        if a.sim:
            sim_fit(pack, [d if d.is_absolute() else REPO / d for d in a.sim], rows, years, write=a.fit,
                    overtake_factor=a.overtake_factor, only=a.fit_only)
        else:
            pack_report(pack, rows, years)


if __name__ == "__main__":
    main()
