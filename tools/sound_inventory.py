"""Sound inventory: every sound slot of every built pack, and every recording we hold.

For each built season (seasons/<id>/season.json) it works out where each
sound slot comes from: our private overlay (tools/engine_audio, set in the
era base's base.json "audio" section) or the game's stock clips. For the
overlay it names the recordings behind every clip and the year of the cars
in them, so a season that plays another year's cars shows as "shared".

It also lists the recordings in the private library
(private/engine_audio/library.sqlite) by the year of the cars in them, and
marks which are used in a pack, cut as candidates, or still spare.

The page holds metadata only (titles, ids, years, times), never audio.

    python tools/sound_inventory.py

Output: private/sound_inventory/index.html (from tools/sound_inventory_template.html).
"""
from __future__ import annotations

import ast
import json
import re
import sqlite3
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools" / "engine_audio"))
from common import ENGINE_TYPES, ERA_EXCLUDE, UPLOAD_YEARS, video_years  # noqa: E402
import layers  # noqa: E402

PRIVATE = REPO / "private" / "engine_audio"
TEMPLATE = REPO / "tools" / "sound_inventory_template.html"
OUT = REPO / "private" / "sound_inventory" / "index.html"

SERIES_NAMES = {"dtm": "DTM", "btcc": "BTCC", "f1": "Formula 1", "itc": "ITC"}

# Car generations per series, for years without a built pack too. The DTM
# eras follow docs/ERAS.md and bases/README.md.
ERAS = [
    ("dtm", 1984, 1992, "Group A", "dtm-1991 template"),
    ("dtm", 1993, 1996, "Class 1", None),
    ("dtm", 2000, 2011, "Era 3: Masters V8", "dtm-era3"),
    ("dtm", 2012, 2018, "Era 4: New DTM V8", "dtm-era4"),
    ("dtm", 2019, 2020, "Era 5: Class One turbo", "dtm-era5"),
    ("dtm", 2021, 2026, "GT3", None),
    ("btcc", 1991, 1991, "Supertouring", "dtm-1991 template"),
    ("f1", 2010, 2013, "2.4 V8", "f1-v8"),
    ("itc", 1996, 1996, "Class 1", None),
]

# Slots the game has, in page order. "layer" slots live in ambience/session_layers.json.
STOCK = {
    "start_light": "Start lights (five beeps)",
    "lights_out": "Lights out",
    "pa": "Track announcer",
    "helicopter": "Helicopter",
    "pit_blowers": "Pit blowers",
    "rain": "Rain",
    "base": "Base beds (base_01, base_02)",
}


def load(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def era_of(series: str, year: int) -> str:
    for s, a, b, label, _ in ERAS:
        if s == series and a <= year <= b:
            return label
    return "Other"


def car_year(vid: str, title: str, vtype: str) -> int | None:
    """Year of the cars heard. The onboard, TV and archive playlists are the
    2013 season itself (tools/engine_audio/README.md, "Era")."""
    if vtype != "spectator":
        return 2013
    years = video_years(title) or ([UPLOAD_YEARS[vid]] if vid in UPLOAD_YEARS else [])
    return min(years) if years else None


def recordings() -> dict[str, dict]:
    db = PRIVATE / "library.sqlite"
    if not db.exists():
        return {}
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    out = {}
    for r in con.execute("select * from videos where status = 'done'"):
        vtype = r["video_type"]
        if vtype not in ENGINE_TYPES:      # features and animations carry no usable engine sound
            continue
        out[r["id"]] = {
            "id": r["id"],
            "title": (r["title"] or "").strip(),
            "type": vtype,
            "year": car_year(r["id"], r["title"] or "", vtype),
            "track": r["track"] or "",
            "make": r["manufacturer"] or "",
            "driver": r["driver"] or "",
            "min": round((r["duration_s"] or 0) / 60, 1),
            "commentary": r["commentary"] or "",
            "exclude": ERA_EXCLUDE.get(r["id"], ""),
            "uses": [],          # filled below: which pack slots play it
            "candidates": 0,     # clips cut from it for listening
        }
    return out


def parse_source(src: str) -> dict:
    """'private: <vid> ...' -> video id and a short note; anything else is stock."""
    m = re.match(r"private:\s*(\S+)\s*(.*)", src or "")
    if not m:
        return {"vid": None, "note": src or ""}
    note = m.group(2).strip()
    times = re.match(r"@\s*([\d.]+)s|go @ ([\d.]+)s|([\d.]+) ([\d.]+)", note)
    at = None
    if times:
        if times.group(1) or times.group(2):
            at = float(times.group(1) or times.group(2))
        else:
            at = float(times.group(3))
    note = re.sub(r"^(go )?@\s*[\d.]+s\s*|^[\d.]+ [\d.]+\s*", "", note).strip(" ()")
    return {"vid": m.group(1), "at": at, "note": note}


def crowd_source() -> tuple[str, float, float, str] | None:
    text = (REPO / "tools" / "engine_audio" / "ambience.py").read_text(encoding="utf-8")
    m = re.search(r"^CROWD = (\(.*\))$", text, re.M)
    return ast.literal_eval(m.group(1)) if m else None


def overlay_slots(overlay_id: str, recs: dict) -> dict | None:
    """What an overlay puts in each slot, with sources."""
    ov = load(PRIVATE / "pack" / overlay_id / "overlay.json")
    if not ov:
        return None
    clips = ov.get("clips", {})
    flyby = {c["key"]: c for c in clips.get("assets/audio/session/hotlap_flybys.json", [])}
    race = {c["key"]: c for c in clips.get("assets/audio/race/race_engines.json", [])}

    def src(c, use):
        s = parse_source(c.get("source", ""))
        if s["vid"] and s["vid"] in recs and use not in recs[s["vid"]]["uses"]:
            recs[s["vid"]]["uses"].append(use)
        return s

    out = {"passby": {}, "tv": [], "grid_idle": [], "grid_launch": [], "pit_exit": [],
           "pit_wheelguns": [], "pit_fireup": [], "cars": [], "crowd": []}
    for make, keys in ov.get("passby_by_make", {}).items():
        # a list since the pass-by pools (wishlist E11): the first is the
        # one 0.99.6 plays, the rest wait for the next game version
        keys = [k for k in (keys if isinstance(keys, list) else [keys]) if k in flyby]
        if keys:
            out["passby"][make] = {"key": keys[0], **src(flyby[keys[0]], f"Pass-by {make}"),
                                   "pool": [{"key": k, **src(flyby[k], f"Pass-by {make} (pool, next version)")}
                                            for k in keys[1:]]}
    for key, c in flyby.items():
        if re.search(r"_tv_\d+$", key):
            out["tv"].append({"key": key, **src(c, "TV pass-by (not heard)")})
    for key, c in sorted(race.items()):
        kind = re.sub(r"_\d+$", "", key)
        if kind in out:
            label = {"grid_idle": "Grid idle", "grid_launch": "Launch", "pit_exit": "Pit exit",
                     "pit_wheelguns": "Wheelguns", "pit_fireup": "Fire-up"}[kind]
            out[kind].append({"key": key, **src(c, label)})
    # The long track loop and the crowd, when this set makes them: every shot
    # of the set's shots.json, summed per recording (the era-4 set keeps
    # library/ itself, others library/sets/<id>/, as tools/engine_audio/common.py).
    layer_set = ov.get("set", {}).get("assets/audio/ambience/session_layers.json", {})
    amb = PRIVATE / "library" / ("ambience" if overlay_id == "dtm-era4" else f"sets/{overlay_id}/ambience")
    if "cars.file" in layer_set:
        per = defaultdict(float)
        for shot in load(amb / "shots.json", []) or []:
            per[shot["video_id"]] += shot.get("used_s", 0)
        for vid, secs in sorted(per.items(), key=lambda kv: -kv[1]):
            if vid in recs and "Track loop" not in recs[vid]["uses"]:
                recs[vid]["uses"].append("Track loop")
            out["cars"].append({"vid": vid, "secs": round(secs, 1)})
        if not out["cars"]:
            out["cars"].append({"vid": None, "note": f"loop of the {overlay_id} set"})
    if "crowd.file" in layer_set:
        crowd = crowd_source() if overlay_id == "dtm-era4" else None
        meta = load(amb / "crowd.json")
        if meta:
            crowd = (meta["vid"], meta["at"], meta["secs"], meta.get("note", ""))
        if crowd:
            vid, at, length, note = crowd
            if vid in recs:
                recs[vid]["uses"].append("Crowd")
            out["crowd"].append({"vid": vid, "at": at, "secs": length, "note": note})
        else:
            out["crowd"].append({"vid": None, "note": f"crowd of the {overlay_id} set"})
    return out


def candidate_counts(recs: dict) -> list[dict]:
    """Clips cut for listening (pilot/ and library/fan_clips), per recording;
    start candidates are named by track and year, so they are listed apart."""
    for folder in (PRIVATE / "pilot" / "pit_candidates", PRIVATE / "library" / "fan_clips"):
        for f in folder.glob("*.wav"):
            for vid in recs:
                if vid in f.name:
                    recs[vid]["candidates"] += 1
                    break
    starts = []
    for f in sorted((PRIVATE / "pilot" / "start_candidates").glob("*.wav")):
        y = re.search(r"(20\d\d)", f.stem)
        starts.append({"name": f.stem, "year": int(y.group(1)) if y else 2013})
    return starts


GROUP_KEYS = {"passby": ("passby",), "tv": ("tv",), "start": ("grid_idle", "grid_launch"),
              "pit": ("pit_exit", "pit_wheelguns", "pit_fireup"), "cars": ("cars",), "crowd": ("crowd",)}


def stack_slots(sets: list[dict], overlays: dict, recs: dict) -> dict | None:
    """The slots a pack hears from its stack of sound sets: per slot group,
    the topmost built set that makes it (tools/engine_audio/overlay.combine)."""
    out, src = None, {}
    for s in sets:
        oid = s["overlay"]
        if oid not in overlays:
            overlays[oid] = overlay_slots(oid, recs)
        one = overlays[oid]
        if one is None:
            continue
        if out is None:
            out = {k: ({} if k == "passby" else []) for k in one}
        for group, keys in GROUP_KEYS.items():
            if group == "passby":
                if one["passby"]:
                    out["passby"].update(one["passby"])
                    src[group] = oid
            else:
                for k in keys:             # per clip kind: a set may make launches but not grid loops
                    if one[k]:
                        out[k] = one[k]
                        src[group] = oid
    if out is not None:
        out["from"] = src
    return out


def season_rows(recs: dict) -> list[dict]:
    overlays: dict[str, dict | None] = {}
    rows = []
    for sdir in sorted((REPO / "seasons").iterdir()):
        if not (sdir / "season.json").exists():
            continue
        series, year = sdir.name.split("-")[0], int(sdir.name.split("-")[1])
        gen = load(sdir / "gen.json", {}) or {}
        base_id = gen.get("base")
        template = gen.get("template") or ("dtm-1991" if sdir.name == "dtm-1991" else None)
        engines = (load(sdir / "data" / "engines.json", {}) or {}).get("suppliers", {})
        makes = [m for m, e in engines.items() if e.get("active", True)]
        stock_passby = {m: e.get("passby_audio", "") for m, e in engines.items()}

        sets = layers.audio_sets(sdir)
        built = [s for s in sets if (PRIVATE / "pack" / s["overlay"] / "overlay.json").exists()]
        slots = stack_slots(built, overlays, recs)
        era_set = sets[0] if sets else None
        rows.append({
            "id": sdir.name,
            "series": series,
            "year": year,
            "era": era_of(series, year),
            "base": base_id or (f"template {template}" if template and template != sdir.name else None),
            "overlay": " + ".join(s["overlay"] for s in built) if slots else None,
            "planned_overlay": sets[-1]["overlay"] if sets and not slots else None,
            "sets": [{"id": s["overlay"], "layer": s["layer"], "built": s in built, "in_pack": bool(s.get("in_pack")),
                      "slots": s.get("slots"), "years": s.get("recording_years")} for s in sets],
            "mother": era_set.get("research_season") if era_set else None,
            "recording_years": era_set.get("recording_years") if era_set else None,
            "makes": makes,
            "stock_passby": stock_passby,
            "slots": slots,
        })
    return rows


def main() -> None:
    recs = recordings()
    seasons = season_rows(recs)
    starts = candidate_counts(recs)
    data = {
        "built": date.today().isoformat(),
        "series": SERIES_NAMES,
        "eras": [{"series": s, "from": a, "to": b, "label": l, "base": base} for s, a, b, l, base in ERAS],
        "stock": STOCK,
        "seasons": seasons,
        "recordings": sorted(recs.values(), key=lambda r: (r["year"] or 0, r["type"], r["track"], r["title"])),
        "start_candidates": starts,
    }
    html = TEMPLATE.read_text(encoding="utf-8").replace(
        "/*DATA*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    used = sum(1 for r in recs.values() if r["uses"])
    print(f"{len(seasons)} packs, {len(recs)} recordings ({used} used) -> {OUT}")


if __name__ == "__main__":
    main()
