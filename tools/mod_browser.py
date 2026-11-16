"""Build the mod browser: one interactive page showing everything a mod pack
contains, each item marked as ours (custom) or inherited from the vanilla
base pack.

It reads what the game actually loads, the installed pack
(<game>/data/<pack_folder>), and compares it with the vanilla base pack it was
built from (season.json "base_pack"), the season source (seasons/<id>/, with
its era base bases/<id>/ underneath, see tools/layers.py) and
the private audio overlay (tools/engine_audio). Tabs: overview, drivers,
teams and cars, feeder series, engines, calendar and tracks, backgrounds (the pack's own
slots and the shared game-wide art, in the order the game picks them),
sounds (vanilla and ours side by side), sound candidates, and every file.

Backgrounds, as the game picks them (read from its ui/main_menu.py,
ui/screens/team_dashboard_screen.py and ui/news_article_mail.py):
    main menu   <pack>/assets/title_bg.png, else assets/title_bg.png
    dashboard   <pack>/assets/[custom/]dashboard_bgs/<team name, alnum><N>.png|jpg
                for the player's team, else every <pack>/assets/[custom/]
                dashboard_bg<N>.png in number order, else
                ui/assets/Dashboard PNGs/Background.png
    hub tiles   ui/assets/Dashboard PNGs/*.png (shared)
    news        assets/news/bg/bg_<outlet>[_<variant>].png (shared)

Output (gitignored, it embeds private audio and game files):
    private/mod_browser/<pack_folder>/index.html   open locally
    private/mod_browser/<pack_folder>/page.html    same page for an Artifact publish
    private/mod_browser/<pack_folder>/media/       images and audio (OGG previews)

build_pack.py --install and engine_audio/package.py --install rebuild it,
so it stays in sync with the installed mod.

    python -I tools/mod_browser.py seasons/dtm-2013
    python -I tools/mod_browser.py --pack workshop_3821496627
    python -I tools/mod_browser.py --workshop      every installed Workshop pack

A pack without a season source here (a Workshop download) is read from the
installed folder alone: its title from workshop.json, and as its base the
vanilla pack with the most identical files. Everything that differs from that
base shows as the pack's own. private/mod_browser/index.html lists every
browser built so far.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import layers  # noqa: E402
TEMPLATE = Path(__file__).with_name("mod_browser_template.html")
OUT_ROOT = REPO / "private" / "mod_browser"
AUDIO_DATA = REPO / "private" / "engine_audio"
MUSIC_CANDIDATES = REPO / "private" / "music" / "candidates"
DEFAULT_GAME = Path(r"X:\SteamLibrary\steamapps\common\Team Principal A Racing Manager")
AUDIO_EXT = {".wav", ".ogg", ".mp3", ".flac"}
OVERLAY_DIR = "_private_overlay"                   # engine_audio/overlay.py STATE_DIR, under assets/audio

LAYER_FILES = {"pa": "pa.ogg", "pit_blowers": "pit_blowers.ogg", "rain": "rain.ogg", "crowd": "crowd.ogg",
               "cars": "cars_on_track.ogg", "helicopter": "helicopter.ogg"}
LAYER_NAMES = {"pa": "Public address", "pit_blowers": "Pit blowers", "rain": "Rain", "crowd": "Crowd",
               "cars": "Cars on track", "helicopter": "Helicopter"}
SLOT_NAMES = {"grid_idle": "Grid idle (loops until lights out)", "grid_launch": "Grid launch (from the 3rd light; lights out 1.5 s in)",
              "pit_exit": "Pit exit", "pit_fireup": "Pit fire-up", "pit_wheelguns": "Wheelguns",
              "engine_passby": "Finish-line pass-by"}

# Sound candidates: folders under private/engine_audio and what they are.
# New folders show up on their own under their folder name.
# Pilot folders ranked by an index.csv list only their best clips.
TOP_RANKED = 20
# Pilot folders shown on every season's page, whatever the year of the recording.
ERA_FREE = {"track_announcer"}

CANDIDATE_GROUPS = [
    ("library/starts", "ingame_start_*.wav", "Starts as the game plays them",
     "The installed pairs mixed with the game's timing and levels: grid idle, five lights 0.5 s apart, "
     "the launch from the 3rd light, lights out at 2.5 s (start_preview.py)."),
    ("library/starts", "*idle_then_launch.wav", "Real starts",
     "The real start in the pack: the grid revving loop, then the launch (with its borrowed ending)."),
    ("library/pits", "pit_*.wav", "Pit lane",
     "The pit sets in the pack (pits.py), paired by number: the fire-up, the exit, the departure "
     "(fire-up crossfaded into the exit, as practice and qualifying play it) and the wheelguns "
     "(race stops)."),
    ("library/fan_clips", "*.wav", "Fan clips: drive-bys, pit entries (not in the pack)",
     "Oschersleben 2013 cuts that were pit exits until the user heard them on 2026-11-07: four drive-bys "
     "and one pit entry, plus the probable exit (old 05), replaced by the 2013 pit-lane departures. Drive-bys of an unknown make can't be tagged per supplier, and the game has "
     "no pit-entry slot (wishlist E14)."),
    ("pilot/pit_candidates", "*.wav", "Pit-lane candidates",
     "Fire-ups, exits and wheelgun bursts found in the pit-lane fan videos, cut for listening. "
     "The exit_EMSlNAM8zC0 clips are 2013 cars stopping in a pit lane and pulling away (probably "
     "Lausitzring, June 2013): candidates for the pit exit, not in the pack yet."),
    ("library/ambience", "*preview*.wav", "Track bed",
     "First 90 s of the cars-on-track loop built from real trackside shots. In the pack."),
    ("pilot/crowd", "*.wav", "Crowd candidates",
     "Engine-free grandstand stretches from fan videos. One is looped as the crowd layer."),
    ("pilot/spectator", "*.wav", "Spectator stretches",
     "Long stretches of the trackside montages, cut for listening."),
    ("pilot/synth_start", "*idle_then_launch.wav", "Simulated starts (set aside)",
     "22-car grids simulated from onboard laps. Replaced by the real starts."),
    ("pilot/start_candidates", "*.wav", "Start candidates",
     "Raw excerpts of the cleanest fan start videos, scored for engine vs noise. The Hockenheim finale is in use."),
    ("pilot/ab_launch", "*.wav", "Launch level A/B (set aside)",
     "Nürburgring 2014 and Brands Hatch as recorded vs levelled. Both dropped: too noisy at the launch."),
    ("pilot/ab_start", "*.wav", "Commentary removal tests (set aside)",
     "The 2013 Hockenheim TV start through several separation models. Too watery to use."),
    ("pilot", "*.wav", "Early pilots (set aside)",
     "First broadcast tests: the mix, the voice stem and the stem without voice."),
]


# ------------------------------------------------------------------ helpers

def load_json(path: Path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def game_path(arg: str | None) -> Path:
    if arg:
        return Path(arg)
    local = load_json(REPO / "local.json", {}) or {}
    return Path(local.get("game_path", DEFAULT_GAME))


def nospace(name: str) -> str:
    return name.replace(" ", "")


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def same_file(a: Path, b: Path) -> bool:
    return a.exists() and b.exists() and a.stat().st_size == b.stat().st_size and sha1(a) == sha1(b)


def constants(path: Path) -> dict:
    out = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^([A-Z][A-Z0-9_]+)\s*=\s*(.+?)\s*(#.*)?$", line)
            if m:
                out[m.group(1)] = m.group(2)
    return out


def start_year(pack: Path) -> int | None:
    raw = constants(pack / "constants.py").get("SEASON_START_YEAR", "")
    return int(raw) if raw.isdigit() else None


class Media:
    """Copies images and transcodes audio next to the page (relative URLs)."""

    def __init__(self, root: Path):
        self.root = root
        self.used: set[Path] = set()

    def image(self, src: Path, rel: str) -> str | None:
        if not src.exists():
            return None
        dst = self.root / "img" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            shutil.copy2(src, dst)
        self.used.add(dst)
        return quote(f"media/img/{rel}")

    def audio(self, src: Path, rel: str) -> str | None:
        """OGG preview (keeps the browser page light), redone only when the source changes."""
        if not src.exists():
            return None
        dst = (self.root / "audio" / rel).with_suffix(".ogg")
        dst.parent.mkdir(parents=True, exist_ok=True)
        # a preview held open by a browser tab can't be replaced on Windows; the
        # fresh one then goes under a versioned name (new URL, so never stale)
        alt = dst.with_name(f"{dst.stem}.{int(src.stat().st_mtime)}.ogg")
        if alt.exists() and alt.stat().st_mtime >= src.stat().st_mtime:
            dst = alt
        elif not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            tmp = dst.with_name(dst.stem + ".tmp.ogg")
            res = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-map", "0:a:0", "-vn",
                                  "-c:a", "libvorbis", "-q:a", "3", str(tmp)], capture_output=True)
            if res.returncode or not tmp.exists():
                return None
            try:
                tmp.replace(dst)
            except PermissionError:
                tmp.replace(alt)
                dst = alt
        self.used.add(dst)
        # quoted: a file named "Cold%20Funk.mp3" must not be read as "Cold Funk"
        return quote(f"media/audio/{dst.relative_to(self.root / 'audio').as_posix()}")

    def prune(self) -> int:
        n = 0
        for p in sorted(self.root.rglob("*"), reverse=True):
            if p.is_file() and p not in self.used:
                try:
                    p.unlink()
                    n += 1
                except PermissionError:
                    pass          # held open by a browser tab; goes next time
            elif p.is_dir() and not any(p.iterdir()):
                p.rmdir()
        return n


def duration(path: Path) -> float | None:
    res = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True)
    try:
        return round(float(res.stdout.strip()), 1)
    except ValueError:
        return None


# ------------------------------------------------------------- provenance

def field_sources(season_file: Path, base_records: list, key: str = "name") -> dict:
    """{record name: {field: 'mod' | 'mod-default' | 'vanilla'}} for $template list files,
    plus the name of the vanilla record the template was taken from."""
    raw = load_json(season_file, {})
    if not (isinstance(raw, dict) and "$template" in raw):
        return {"$template_from": None}
    spec = raw["$template"]
    if "match" in spec:
        k, v = next(iter(spec["match"].items()))
        tpl = next((r for r in base_records if r.get(k) == v), {})
    else:
        tpl = base_records[spec.get("index", 0)] if base_records else {}
    override = set(spec.get("override", {}))
    sys.path.insert(0, str(Path(__file__).parent))
    from build_pack import ATTR_KEYS, RATING_KEYS     # fields a "$rating" spec computes
    rated = set(RATING_KEYS) | {"tyre_management", "chassis_reliability", "aero_efficiency_rating", "attr",
                                "dirty_air_sensitivity", "aero", "chassis_starting_potential"}
    out = {"$template_from": tpl.get(key)}
    for rec in raw.get("records", []):
        src = {}
        for f in set(tpl) | set(rec) | override | (rated if "$rating" in rec else set()):
            if f in rec or ("$rating" in rec and f in rated):
                src[f] = "mod"
            elif f in override:
                src[f] = "mod-default"
            else:
                src[f] = "vanilla"
        out[rec.get(key)] = src
    return out


def classify_files(pack: Path, base: Path, private: set[str], season: Path) -> list[dict]:
    rows = []
    for p in sorted(pack.rglob("*")):
        if not p.is_file() or OVERLAY_DIR in p.parts:
            continue
        rel = p.relative_to(pack).as_posix()
        b = base / rel
        if rel in private:
            status = "private"
        elif not b.exists():
            status = "custom"
        elif same_file(p, b):
            status = "vanilla"
        else:
            status = "changed"
        rows.append({"path": rel, "status": status, "size": p.stat().st_size})
    for p in sorted(base.rglob("*")):
        rel = p.relative_to(base).as_posix()
        if p.is_file() and not (pack / rel).exists():
            rows.append({"path": rel, "status": "removed", "size": p.stat().st_size})
    return rows


def data_patches(pack: Path, base: Path, season: Path) -> list[dict]:
    """Leaf values that the season's "$merge_base" data files change, vanilla vs mod."""
    rows = []

    def walk(path, b, m):
        if isinstance(b, dict) and isinstance(m, dict):
            for k in sorted(set(b) | set(m)):
                walk(f"{path}.{k}" if path else k, b.get(k), m.get(k))
        elif b != m:
            short = lambda v: v if v is None or isinstance(v, (int, float, str, bool)) else (
                f"{len(v)} lines" if isinstance(v, list) else json.dumps(v, ensure_ascii=False))
            rows.append({"file": name, "path": path, "vanilla": short(b), "mod": short(m),
                         "lines": m if isinstance(m, list) and all(isinstance(x, str) for x in m) else None})

    for src in layers.files(season, "data").values():
        spec = load_json(src, {})
        if not (isinstance(spec, dict) and spec.get("$merge_base")) or not (base / src.name).exists():
            continue
        name = src.name
        walk("", load_json(base / name, {}), load_json(pack / name, {}))
    return rows


# ------------------------------------------------------------- sections

def build_drivers(pack, base, season, media, sources):
    year = start_year(pack)
    portraits = layers.merged_json(season, "art/portraits.json") if season else {}
    teams = {t["name"]: t for t in load_json(pack / "teams.json", [])}
    out = []
    for d in load_json(pack / "drivers.json", []):
        art = portraits.get(d["name"], {})
        img = media.image(pack / "assets" / "portraits" / f"{nospace(d['name'])}.png",
                          f"portraits/{nospace(d['name'])}.png")
        team = teams.get(d.get("team"), {})
        if isinstance(d.get("birth_year"), int) and year:
            # 0.99.6+: birth_year wins over age; the game ages from SEASON_START_YEAR
            d = {**d, "age": year - d["birth_year"]}
        out.append({**d, "prov": "custom", "portrait": img,
                    "portrait_info": {k: art.get(k) for k in ("source", "author", "license", "page", "year")},
                    "team_color": team.get("color_rgb"), "fields": sources.get(d["name"], {})})
    vanilla = [{"name": d["name"], "team": d.get("team"), "nationality": d.get("nationality"), "age": d.get("age"),
                "talent": d.get("talent"), "prov": "replaced"} for d in load_json(base / "drivers.json", [])]
    return out, vanilla


def build_teams(pack, base, season, manifest, media, sources):
    hist = load_json(pack / "team_histories.json", {}) or {}
    clones = manifest.get("team_clones", {})
    drivers = load_json(pack / "drivers.json", [])
    ours = set(manifest.get("sponsors", {}).get("pool", {}))
    pool = {s["name"]: s for s in load_json(pack / "sponsors.json", [])}
    deals = {t["team"]: t.get("sponsors", []) for t in (load_json(pack / "starting_sponsors.json", {}) or {}).get("teams", [])}
    # other liveries kept in the season source for a future livery choice
    # (tools/car_drawings.py, art/liveries; not in the pack, wishlist E4)
    liveries = (load_json(season / "art" / "liveries" / "liveries.json", {}) or {}).get("teams", {}) if season else {}
    year = start_year(pack)
    # Staff and principals (build_pack.py from docs/staff): real people are
    # the names in docs/staff/<series>_staff.csv, the rest are made up.
    real_people = set()
    ref = (manifest.get("staff") or {}).get("reference")
    if ref:
        import csv
        series = "btcc" if ref.startswith("btcc-") else "dtm"
        ref_csv = Path(__file__).resolve().parent.parent / "docs" / "staff" / f"{series}_staff.csv"
        if ref_csv.exists():
            with open(ref_csv, encoding="utf-8") as fh:
                real_people = {r["person"] for r in csv.DictReader(fh) if r["season"] == ref}
    staff_by_team = {}
    for st in load_json(pack / "staff.json", []) or []:
        staff_by_team.setdefault(st.get("team"), []).append(
            {"role": st.get("role"), "name": st.get("name"), "age": st.get("age"), "real": st.get("name") in real_people})
    principals = {}
    for tp in (load_json(pack / "teamprincipals.json", {}) or {}).get("principals", []):
        name = f"{tp.get('first_name', '')} {tp.get('last_name', '')}".strip()
        principals[tp.get("team")] = {"role": "team_principal", "name": name, "age": tp.get("age"),
                                      "real": name in real_people}
    # Scripted joins and exits in later seasons (tools/real_history.py)
    joins, leaves = {}, {}
    for e in load_json(pack / "events.json", []) or []:
        if e.get("type") in ("team_join", "team_leave") and e.get("exact_season"):
            (joins if e["type"] == "team_join" else leaves)[e["team"]] = e["exact_season"]
    def career(name):
        parts = []
        if name in joins:
            parts.append(f"Joins in season {joins[name]}" + (f" ({year + joins[name] - 1})" if year else ""))
        if name in leaves:
            last = leaves[name] - 1
            parts.append(f"Leaves after season {last}" + (f" ({year + last - 1})" if year else ""))
        return ". ".join(parts) or None
    out = []
    for t in load_json(pack / "teams.json", []):
        n = nospace(t["name"])
        # 0.99.6+ chassis naming: a pinned name for the year, else prefix + two-digit year
        chassis = (t.get("chassis_names") or {}).get(str(year)) or (
            f"{t['chassis_prefix']}{year % 100:02d}" if t.get("chassis_prefix") and year else None)
        other = [{"number": c["number"],
                  "car": media.image(season / c["file"], f"liveries/{Path(c['file']).name}")}
                 for c in liveries.get(t["name"], []) if not c["team_image"] and (season / c["file"]).exists()]
        sponsors = [{"slot": d["slot"], "name": d["name"], "seasons": d.get("seasons"),
                     "amount_m": pool.get(d["name"], {}).get("amount_m"),
                     "industry": pool.get(d["name"], {}).get("industry"),
                     "nationality": pool.get(d["name"], {}).get("nationality"),
                     "prov": "custom" if d["name"] in ours else "vanilla"} for d in deals.get(t["name"], [])]
        out.append({**t, "prov": "custom", "sponsors": sponsors, "chassis_name": chassis,
                    "car": media.image(pack / "assets" / "Cars" / f"{n}.png", f"cars/{n}.png"),
                    "car_number": next((c["number"] for c in liveries.get(t["name"], []) if c["team_image"]), None),
                    "other_liveries": other,
                    "logo": media.image(pack / "assets" / "logos" / f"{n}.png", f"logos/{n}.png"),
                    "history_text": hist.get(t["name"]), "cloned_from": clones.get(t["name"]),
                    "career": career(t["name"]), "future": t.get("active", True) is False,
                    "drivers": [d["name"] for d in drivers if d.get("team") == t["name"]],
                    "staff": ([principals[t["name"]]] if t["name"] in principals else []) +
                             sorted(staff_by_team.get(t["name"], []), key=lambda x: x["role"] or ""),
                    "fields": sources.get(t["name"], {})})
    vanilla = []
    for t in load_json(base / "teams.json", []):
        n = nospace(t["name"])
        vanilla.append({"name": t["name"], "engine": t.get("engine"), "color_rgb": t.get("color_rgb"),
                        "prov": "replaced",
                        "car": media.image(base / "assets" / "Cars" / f"{n}.png", f"vanilla/cars/{n}.png")})
    return out, vanilla


def build_juniors(pack, base):
    """The feeder series (junior_series.json) and licence rules (driverslicense.json)
    as installed; each series is "custom" unless it is the vanilla one."""
    vanilla = {s.get("series_abbreviation"): s for s in load_json(base / "junior_series.json", [])}
    out = []
    for s in load_json(pack / "junior_series.json", []):
        same = vanilla.get(s.get("series_abbreviation")) == s
        out.append({**s, "prov": "vanilla" if same else "custom"})
    return out, load_json(pack / "driverslicense.json", {})


def build_backgrounds(pack, base, game, media):
    """Every full-screen or panel background the game draws, in the order the
    game picks them (read from ui/main_menu.py, ui/screens/team_dashboard_screen.py
    and ui/news_article_mail.py). Pack slots compare with the base pack; the
    shared ones are game-wide files a pack can't change."""
    def size_of(p: Path):
        try:
            from PIL import Image
            with Image.open(p) as im:
                return list(im.size)
        except Exception:
            return None

    def item(p: Path, rel_media: str, name: str, status: str, where: str, note: str = "") -> dict:
        return {"name": name, "img": media.image(p, rel_media), "status": status, "where": where,
                "note": note, "px": size_of(p), "bytes": p.stat().st_size}

    def pack_status(rel: str) -> str:
        b = base / rel
        return "custom" if not b.exists() else ("vanilla" if same_file(pack / rel, b) else "changed")

    groups = []
    # main menu
    items, rel = [], "assets/title_bg.png"
    if (pack / rel).exists():
        items.append(item(pack / rel, "backgrounds/pack/title_bg.png", "Main menu", pack_status(rel), f"data/{pack.name}/{rel}"))
    shared = game / "assets" / "title_bg.png"
    if shared.exists():
        items.append(item(shared, "backgrounds/shared/title_bg.png", "Main menu, shared fallback", "shared",
                          "assets/title_bg.png", "used when the pack has no title_bg.png"))
    groups.append({"id": "menu", "title": "Main menu", "scope": "pack", "items": items,
                   "rule": "The selected pack's assets/title_bg.png, else the shared one. Landscape, 16:9 "
                           "recommended; the menu draws its own logo and buttons on top."})

    # team dashboard: per-team sets, else the pack set, else the shared fallback
    roots = [pack / "assets" / "custom", pack / "assets"]
    num = lambda n: int(re.fullmatch(r"dashboard_bg(\d*)\.png", n, re.I).group(1) or 1)
    items = []
    for root in roots:
        if root.is_dir():
            for p in sorted((p for p in root.iterdir() if re.fullmatch(r"dashboard_bg(\d*)\.png", p.name, re.I)),
                            key=lambda p: num(p.name)):
                rel = p.relative_to(pack).as_posix()
                items.append(item(p, f"backgrounds/pack/{rel}", f"Dashboard {num(p.name)}", pack_status(rel),
                                  f"data/{pack.name}/{rel}"))
    for p in sorted((base / "assets").glob("dashboard_bg*.png")):
        if not (pack / "assets" / p.name).exists():
            items.append(item(p, f"backgrounds/base/{p.name}", f"Dashboard {num(p.name)} (vanilla)", "removed",
                              f"data/{base.name}/assets/{p.name}", "in the vanilla pack, not in ours"))
    groups.append({"id": "dashboard", "title": "Team dashboard", "scope": "pack", "items": items,
                   "rule": "Every dashboard_bg<N>.png in the pack's assets (or assets/custom), in number order. "
                           "Any count works; the dashboard rotates through them."})

    team_key = lambda name: "".join(c for c in str(name) if c.isalnum())
    items, missing = [], []
    for t in load_json(pack / "teams.json", []):
        key, found = team_key(t["name"]), []
        for root in roots:
            d = root / "dashboard_bgs"
            if d.is_dir():
                found += [p for p in sorted(d.iterdir()) if p.suffix.lower() in (".png", ".jpg", ".jpeg")
                          and re.fullmatch(re.escape(key) + r"(\d*)", p.stem, re.I)]
        for p in found:
            rel = p.relative_to(pack).as_posix()
            items.append(item(p, f"backgrounds/pack/{rel}", t["name"], pack_status(rel), f"data/{pack.name}/{rel}"))
        if not found:
            missing.append({"team": t["name"], "file": f"assets/dashboard_bgs/{key}.png"})
    groups.append({"id": "team", "title": "Team dashboard, per team", "scope": "pack", "items": items,
                   "missing": missing,
                   "rule": "assets/dashboard_bgs/<team name, letters and digits only><N>.png (or .jpg) in the pack. "
                           "When the player's team has one, it replaces the pack set."})

    fb = game / "ui" / "assets" / "Dashboard PNGs" / "Background.png"
    tiles_dir = fb.parent
    groups.append({"id": "dashfallback", "title": "Team dashboard, shared fallback", "scope": "shared",
                   "items": [item(fb, "backgrounds/shared/dashboard/Background.png", "Dashboard fallback", "shared",
                                  "ui/assets/Dashboard PNGs/Background.png",
                                  "used when the pack has no dashboard_bg")] if fb.exists() else [],
                   "rule": "Drawn when neither a team set nor a pack set exists."})
    tiles = [item(p, f"backgrounds/shared/dashboard/{p.name}", p.stem.replace("_", " ").capitalize(), "shared",
                  f"ui/assets/Dashboard PNGs/{p.name}")
             for p in sorted(tiles_dir.glob("*.png")) if p.name != "Background.png"] if tiles_dir.is_dir() else []
    groups.append({"id": "tiles", "title": "Hub tiles", "scope": "shared", "items": tiles,
                   "rule": "The picture behind each hub button (calendar, factory, finance…). Game-wide."})

    news = game / "assets" / "news" / "bg"
    outlets = {}
    for p in sorted(news.glob("bg_*.png")) if news.is_dir() else []:
        outlet, _, variant = p.stem[3:].partition("_")
        outlets.setdefault(outlet, []).append(
            item(p, f"backgrounds/shared/news/{p.name}", variant.replace("_", " ") or "default", "shared",
                 f"assets/news/bg/{p.name}"))
    for outlet, items in outlets.items():
        groups.append({"id": f"news-{outlet}", "title": f"News: {outlet}", "scope": "shared", "items": items,
                       "rule": "Tiled page texture of this news outlet's editions, with variants for "
                               "celebrations, titles, milestones and wet races. Game-wide."})
    return groups


def build_engines(pack, base, media):
    eng = load_json(pack / "engines.json", {}) or {}
    base_names = set((load_json(base / "engines.json", {}) or {}).get("suppliers", {}))
    out = []
    for name, s in eng.get("suppliers", {}).items():
        out.append({"supplier": name, **s, "prov": "vanilla" if name in base_names else "custom",
                    "logo": media.image(pack / "assets" / "engines" / f"{nospace(name)}.png",
                                        f"engines/{nospace(name)}.png"),
                    "engine_img": media.image(pack / "assets" / "engines" / f"{nospace(s.get('engine', ''))}.png",
                                              f"engines/{nospace(s.get('engine', ''))}.png")})
    rules = {k: v for k, v in (eng.get("unit_rules") or {}).items() if not isinstance(v, (dict, list))}
    tyres = load_json(pack / "tyre_suppliers.json", {}) or {}
    tyre = [{"supplier": n, **{k: v for k, v in s.items() if not isinstance(v, (dict, list))},
             "logo": media.image(pack / "assets" / "tyre" / f"{nospace(n)}.png", f"tyre/{nospace(n)}.png")}
            for n, s in tyres.get("suppliers", {}).items()]
    return out, rules, tyre


def build_tracks(pack, base, season, manifest, media):
    sched = load_json(pack / "schedule.json", []) or []
    own = {name[:-5]: layers.layer_of(season, path) for name, path in layers.files(season, "tracks").items()} if season else {}
    shared = manifest.get("shared_tracks", {})
    overrides = manifest.get("track_overrides", {})
    placeholders = {k: v["from"] for k, v in manifest.get("track_placeholders", {}).items() if not k.startswith("$")}
    tracks = []
    for p in sorted((pack / "tracks").glob("*.json")):
        t = load_json(p, {})
        tid = p.stem
        if tid in own:
            prov, origin = "custom", f"Our own trace ({own[tid].relative_to(REPO).as_posix()}/tracks)"
        elif tid in shared:
            prov, origin = "custom", f"Our trace, shared from {shared[tid]}"
        elif tid in placeholders:
            prov, origin = "custom", f"Placeholder: not traced yet, uses the geometry of {placeholders[tid]}"
        elif same_file(p, base / "tracks" / p.name):
            prov, origin = "vanilla", "Vanilla track from the base pack"
        else:
            prov, origin = "changed", "Vanilla track, changed by the build"
        rounds = [i for i, w in enumerate(sched, 1) if w == tid]
        tracks.append({"id": tid, "name": t.get("name", tid), "prov": prov, "origin": origin, "weeks": rounds,
                       "img": media.image(pack / "assets" / "tracks" / f"{tid}.png", f"tracks/{tid}.png"),
                       "img_prov": "vanilla" if same_file(pack / "assets" / "tracks" / f"{tid}.png",
                                                          base / "assets" / "tracks" / f"{tid}.png") else "custom",
                       "stats": {**{k: v for k, v in t.items() if isinstance(v, (int, float, str)) and k != "name"},
                                 "pole_side": (t.get("starting_grid") or {}).get("pole_side", "left")},
                       "drs_zones": len(t.get("drs_zones", []) or []), "overrides": overrides.get(tid),
                       "source": t.get("source")})
    calendar = []
    rnd = 0
    for week, w in enumerate(sched, 1):
        if w:
            if w not in ("private", "test"):
                rnd += 1
            calendar.append({"week": week, "event": w, "round": rnd if w not in ("private", "test") else None})
    return tracks, calendar


def build_sounds(pack, base, media, private):
    pa, ba = pack / "assets" / "audio", base / "assets" / "audio"
    rows = []

    def player(path: Path, tag: str) -> dict | None:
        if not path.exists():
            return None
        return {"audio": media.audio(path, f"{tag}/{path.parent.name}/{path.name}"), "file": path.name,
                "seconds": duration(path)}

    def manifest_rows(rel_manifest: str, area: str, heard_fn=None):
        pm = load_json(pa / rel_manifest, {"clips": []})
        bm = load_json(ba / rel_manifest, {"clips": []})
        folder_p, folder_b = (pa / rel_manifest).parent, (ba / rel_manifest).parent
        bclips = {c["key"]: c for c in bm.get("clips", [])}
        for c in pm.get("clips", []):
            key = c["key"]
            slot = re.sub(r"(_\d+)?(_lr)?$", "", key)
            b = bclips.get(key)
            same = b and b["file"] == c["file"] and same_file(folder_p / c["file"], folder_b / b["file"])
            status = "vanilla" if same else ("replaced" if b else "added")
            heard, why = heard_fn(key) if heard_fn else (True, "")
            rows.append({"area": area, "slot": SLOT_NAMES.get(slot, slot.replace("_", " ")), "key": key,
                         "status": status, "private": c["file"] in private or f"{folder_p.name}/{c['file']}" in private,
                         "now": player(folder_p / c["file"], "pack"),
                         "vanilla": player(folder_b / b["file"], "vanilla") if b and not same else None,
                         "source": c.get("source", "" if same else ""), "gain": c.get("gain"),
                         "heard": heard, "why": why})

    engines = load_json(pack / "engines.json", {}) or {}
    tags = {s.get("passby_audio") for s in engines.get("suppliers", {}).values() if s.get("passby_audio")}
    untagged = any(not s.get("passby_audio") for s in engines.get("suppliers", {}).values())

    def passby_heard(key):
        base_key = re.sub(r"_lr$", "", key)
        if base_key in tags:
            return True, "tagged on a supplier"
        if untagged:
            return True, "random bank (untagged suppliers)"
        return False, "random bank, but every supplier has its own tag"

    manifest_rows("race/race_engines.json", "Race")
    manifest_rows("session/hotlap_flybys.json", "Pass-bys", passby_heard)

    pl = load_json(pa / "ambience" / "session_layers.json", {}) or {}
    bl = load_json(ba / "ambience" / "session_layers.json", {}) or {}
    for layer, default in LAYER_FILES.items():
        cfg, bcfg = pl.get(layer, {}), bl.get(layer, {})
        f = cfg.get("file", default)
        bf = bcfg.get("file", default)
        same = f == bf and same_file(pa / "ambience" / f, ba / "ambience" / bf)
        rows.append({"area": "Ambience", "slot": LAYER_NAMES[layer], "key": layer,
                     "status": "vanilla" if same else "replaced", "private": f"ambience/{f}" in private,
                     "now": player(pa / "ambience" / f, "pack"),
                     "vanilla": None if same else player(ba / "ambience" / bf, "vanilla"),
                     "source": "", "gain": cfg.get("gain"), "heard": True,
                     "why": "sessions: " + ", ".join(cfg.get("sessions", []))})
    for f in ("base_01.ogg", "base_02.ogg"):
        same = same_file(pa / "ambience" / f, ba / "ambience" / f)
        rows.append({"area": "Ambience", "slot": "Base bed", "key": Path(f).stem,
                     "status": "vanilla" if same else "replaced", "private": False,
                     "now": player(pa / "ambience" / f, "pack"), "vanilla": None, "source": "", "gain": None,
                     "heard": True, "why": ""})
    for f in ("start_light.wav", "lights_out.wav"):
        same = same_file(pa / "race" / f, ba / "race" / f)
        rows.append({"area": "Start cues", "slot": f.replace(".wav", "").replace("_", " ").capitalize(),
                     "key": Path(f).stem, "status": "vanilla" if same else "replaced", "private": False,
                     "now": player(pa / "race" / f, "pack"),
                     "vanilla": None if same else player(ba / "race" / f, "vanilla"),
                     "source": "", "gain": None, "heard": True, "why": ""})
    for p in sorted((pa / "music").glob("*")):
        if p.suffix.lower() in AUDIO_EXT:
            same = same_file(p, ba / "music" / p.name)
            rows.append({"area": "Menu music", "slot": "Track", "key": p.stem,
                         "status": "vanilla" if same else "added", "private": False,
                         "now": player(p, "pack"), "vanilla": None, "source": "", "gain": None,
                         "heard": True, "why": ""})
    for p in sorted((pa / "ui").glob("*")):
        if p.suffix.lower() in AUDIO_EXT:
            rows.append({"area": "Interface", "slot": "UI sound", "key": p.stem, "status": "vanilla",
                         "private": False, "now": player(p, "pack"), "vanilla": None, "source": "",
                         "gain": None, "heard": True,
                         "why": "the game always takes UI sounds from its shared folder"})
    return rows


def tags(path: Path) -> dict:
    """ID3/Vorbis tags of an audio file, keys lower-cased."""
    res = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format_tags", "-of", "json", str(path)],
                         capture_output=True, text=True)
    try:
        return {k.lower(): v for k, v in json.loads(res.stdout)["format"].get("tags", {}).items()}
    except (ValueError, KeyError):
        return {}


def music_candidates(media, pack: Path | None) -> dict | None:
    """Menu music considered for the pack (private/music/candidates, not shipped)."""
    files = [p for p in sorted(MUSIC_CANDIDATES.glob("*")) if p.suffix.lower() in AUDIO_EXT]
    if not files:
        return None
    playlist = {p.name for p in (pack / "assets" / "audio" / "music").glob("*")} if pack else set()
    items = []
    for p in files:
        t = tags(p)
        artist = t.get("artist") or t.get("tcm") or ""
        bits = [b for b in (artist, t.get("genre"), t.get("date")) if b]
        if "incompetech" in t.get("comment", "").lower() or artist == "Kevin MacLeod":
            bits.append("incompetech.com, CC BY 4.0 (credit needed)")
        items.append({"name": t.get("title") or p.stem, "file": p.name,
                      "audio": media.audio(p, f"candidates/music/{p.name}"), "seconds": duration(p),
                      "in_use": p.name in playlist, "note": ", ".join(bits)})
    return {"title": "Menu music", "folder": "private/music/candidates",
            "note": "Tracks for the dashboard playlist. Not in the pack until copied into the season's assets/audio/music.",
            "items": items}


def build_candidates(media, pack: Path | None = None, season: Path | None = None):
    groups, seen = [], set()
    music = music_candidates(media, pack)
    if music:
        groups.append(music)
    try:
        sys.path.insert(0, str(REPO / "tools" / "engine_audio"))
        from ambience import CROWD          # the crowd stretch in use
        crowd_tag = f"{CROWD[0]}_{CROWD[1]:.0f}s"
    except Exception:
        crowd_tag = None
    # only cars this pack may play are listed: the recording years of its
    # sound sets (an era's, plus a season's own, e.g. 2018: 2012-2013 and
    # 2017-2018; layers.audio_sets). Clips cut from other years' videos are
    # left out, and counted. Without sets: the default set's years.
    try:
        from common import ERA, ERA_EXCLUDE, UPLOAD_YEARS, video_years
        import sqlite3
        with sqlite3.connect(AUDIO_DATA / "library.sqlite") as db:
            videos = {i: (t, ty) for i, t, ty in db.execute("SELECT id, title, video_type FROM videos")}
        allowed = {y for s in (layers.audio_sets(season) if season else []) for y in s.get("recording_years", [])}
        allowed = allowed or set(range(ERA[0], ERA[-1] + 1))
    except Exception:
        videos, allowed = None, set()

    def video_out(vid: str, title: str, vtype: str) -> bool:
        if vid in ERA_EXCLUDE:
            return True
        if vtype != "spectator":          # the onboard, TV and archive playlists are 2013
            return 2013 not in allowed
        years = video_years(title) or ([UPLOAD_YEARS[vid]] if vid in UPLOAD_YEARS else [])
        return not years or any(y not in allowed for y in years)

    def out_of_era(name: str) -> bool:
        if videos is None:
            return False
        years = [int(y) for y in re.findall(r"(?<!\d)(20[0-2]\d)(?!\d)", name)]   # e.g. hockenheim2017_start
        return (any(y not in allowed for y in years)
                or any(video_out(i, t, ty) for i, (t, ty) in videos.items() if i in name))

    starts_meta = load_json(AUDIO_DATA / "library" / "starts" / "starts.json", []) or []
    pit_cand = {c["file"]: c for c in load_json(AUDIO_DATA / "pilot" / "pit_candidates" / "candidates.json", []) or []}
    pits_meta = load_json(AUDIO_DATA / "library" / "pits" / "pits.json", []) or []
    fan_meta = {c["file"]: c["note"] for c in load_json(AUDIO_DATA / "library" / "fan_clips" / "fan_clips.json", []) or []}
    for folder, pattern, title, note in CANDIDATE_GROUPS:
        d = AUDIO_DATA / folder
        files = [p for p in sorted(d.glob(pattern)) if p.is_file() and p not in seen]
        hidden = [p for p in files if out_of_era(p.name)]
        seen.update(hidden)
        files = [p for p in files if p not in hidden]
        if hidden:
            note = f"{note} {len(hidden)} clip(s) from other years' cars are hidden.".strip()
        if not files:
            continue
        items = []
        for p in files:
            seen.add(p)
            item = {"name": p.stem.replace("_", " "), "file": p.name,
                    "audio": media.audio(p, f"candidates/{folder}/{p.name}"), "seconds": duration(p),
                    "in_use": folder in ("library/starts", "library/ambience", "library/pits")
                              or bool(crowd_tag and crowd_tag in p.name),
                    "note": ""}
            m = re.match(r"start_(\d+)_", p.name)
            if folder == "library/starts" and m and int(m.group(1)) <= len(starts_meta):
                s = starts_meta[int(m.group(1)) - 1]
                item["note"] = f"{s['title']} — {s['note']} (go at {s['go_s']} s, grid loop {s['idle_s']} s)"
            m = re.match(r"pit_(\d+)_", p.name)
            if folder == "library/pits" and m and int(m.group(1)) <= len(pits_meta):
                item["note"] = pits_meta[int(m.group(1)) - 1]["note"]
            if folder == "library/fan_clips":
                item["note"] = fan_meta.get(p.name, "")
            if folder == "pilot/pit_candidates" and p.name in pit_cand:
                c = pit_cand[p.name]
                item["note"] = c.get("note") or f"{c['kind']}, {c['video_id']} {c['start_s']}-{c['end_s']} s"
            items.append(item)
        groups.append({"title": title, "folder": f"private/engine_audio/{folder}", "note": note, "items": items})
    pilot_dirs = []
    for d in sorted((AUDIO_DATA / "pilot").glob("*")):
        if d.is_dir() and not any(g[0] == f"pilot/{d.name}" for g in CANDIDATE_GROUPS):
            pilot_dirs.append(d)
            pilot_dirs += [s for s in sorted(d.glob("*")) if s.is_dir()]   # e.g. one subfolder per make
    for d in pilot_dirs:
        rel = d.relative_to(AUDIO_DATA / "pilot").as_posix()
        # a folder's index.csv (file relative to the folder, quality, ...) ranks its
        # clips best first; only the top ones are listed, the rest stay in the folder
        index = d.parent / "index.csv" if (d.parent / "index.csv").exists() else d / "index.csv"
        ranked = {}
        if index.exists():
            with open(index, encoding="utf-8-sig") as fh:
                for r in csv.DictReader(fh):
                    ranked[(index.parent / r["file"]).resolve()] = r
        # a folder's candidates.json (file -> note, frames, scores) labels its clips
        meta = {c["file"]: c for c in load_json(d / "candidates.json", []) or [] if isinstance(c, dict) and "file" in c}
        for p, r in ranked.items():
            if p.parent == d.resolve():
                if "text" in r:   # announcer.py: what is said
                    note = (f"{r['kind'] or 'unsorted'} · {r['year']} {r['track']} · {r['language']} · voice "
                            f"{r['voice_db']} dB over the 2 s around, bass {r['low_db']} dB · “{r['text']}” · {r['title']}")
                else:             # pass-by sweep
                    note = (f"score {float(r['quality']):.2f} · {r['year']} {r['track']} {r['race']}, "
                            f"{r['driver']}, {r['label'].replace('_', ' ')} at {r['rpm_mean']} rpm, "
                            f"{r['at_s']} s into {Path(r['source']).name}")
                meta[p.name] = {"note": note}

        def label(c: dict) -> str:
            bits = [c.get("note"), c.get("frames"), c.get("title")]
            if "hf_share" in c:
                bits.append(f"above 5 kHz {c['hf_share'] * 100:.1f} %, flatness {c['flatness']} (2013 pick: 0.2 %, 0.06)")
            if c.get("standing_start"):
                bits.append("standing start")
            return " · ".join(b for b in bits if b)
        # people talking are not tied to a car generation: every season lists them
        wavs = [p for p in sorted(d.glob("*.wav")) if rel in ERA_FREE or not out_of_era(p.name)]
        note = ""
        if ranked and rel in ERA_FREE:
            # announcer.py: the announcer first, by year and track; clips sorted
            # out by hand as fans or video voice-overs are left in the folder
            row = lambda p: ranked.get(p.resolve(), {})
            wavs = [p for p in wavs if row(p).get("kind") not in ("fan", "video", "noise")]
            wavs.sort(key=lambda p: (row(p).get("kind") != "pa", row(p).get("year") or "", row(p).get("track") or "", p.name))
            note = "The track announcer (pa) first, then unsorted speech; fans and video voice-overs are left out (index.csv)."
        elif ranked:
            wavs.sort(key=lambda p: -float(ranked.get(p.resolve(), {}).get("quality") or 0))
            if len(wavs) > TOP_RANKED:
                note = f"The {TOP_RANKED} best of {len(wavs)} by score (index.csv); the rest are in the folder."
                wavs = wavs[:TOP_RANKED]
        items = [{"name": p.stem.replace("_", " "), "file": p.name,
                  "audio": media.audio(p, f"candidates/pilot/{rel}/{p.name}"), "seconds": duration(p),
                  "in_use": False, "note": label(meta.get(p.name, {}))}
                 for p in wavs]
        if items:
            top, _, sub = rel.partition("/")
            groups.append({"title": top.replace("_", " ").capitalize() + (f": {sub}" if sub else ""),
                           "folder": f"private/engine_audio/pilot/{rel}", "note": note, "items": items})
    lib = AUDIO_DATA / "library" / "index.html"
    return groups, (lib.as_uri() if lib.exists() else None)


# --------------------------------------------------------------------- main

def closest_base(pack: Path, game: Path) -> tuple[str, int, int]:
    """The vanilla pack (data/default*) sharing the most identical files with pack."""
    files = [p for p in pack.rglob("*") if p.is_file()]
    best = (None, -1, len(files))
    for cand in sorted((game / "data").glob("default*")):
        same = 0
        for p in files:
            b = cand / p.relative_to(pack)
            if b.is_file() and b.stat().st_size == p.stat().st_size and sha1(b) == sha1(p):
                same += 1
        if same > best[1]:
            best = (cand.name, same, len(files))
    return best


def steam_workshop(game: Path) -> Path:
    """Steam's download folder for this game's Workshop items (steamapps/workshop/content/<app id>)."""
    return game.parent.parent / "workshop" / "content" / "4340600"


def pack_dir(pack_folder: str, game: Path) -> Path:
    """data/<pack_folder>, else a Workshop item Steam downloaded but the game
    has not copied into data/ yet (it does that when it starts)."""
    installed = game / "data" / pack_folder
    if installed.is_dir() or not pack_folder.startswith("workshop_"):
        return installed
    return steam_workshop(game) / pack_folder.removeprefix("workshop_")


def pack_manifest(pack_folder: str, game: Path) -> tuple[dict, str]:
    """A season-like manifest for an installed pack with no source here."""
    pack = pack_dir(pack_folder, game)
    meta = load_json(pack / "workshop.json", {}) or {}
    base_name, same, total = closest_base(pack, game)
    item = pack_folder.removeprefix("workshop_")
    origin = (f"Workshop item {item}" if pack_folder.startswith("workshop_") else pack_folder) + \
        f" (no source here; base picked by {same} of {total} files identical" + \
        ("" if pack.parent == game / "data" else "; read from Steam's download, not yet installed by the game") + ")"
    return {"pack_folder": pack_folder, "base_pack": base_name, "title": meta.get("title") or pack_folder,
            "version": meta.get("version"), "series": meta.get("series"),
            "workshop_item": item if pack_folder.startswith("workshop_") else None}, origin


def build(season: Path | None, game: Path, pack_folder: str | None = None) -> Path:
    if season is not None:
        manifest = layers.manifest(season)
        origin = " + ".join(layer.name for layer in layers.chain(season))
    else:
        manifest, origin = pack_manifest(pack_folder, game)
    pack_folder, base_name = manifest["pack_folder"], manifest["base_pack"]
    pack, base = pack_dir(pack_folder, game), game / "data" / base_name
    if not pack.is_dir():
        sys.exit(f"pack not installed: {pack} (run build_pack.py --install first)")
    out = OUT_ROOT / pack_folder
    media = Media(out / "media")
    applied = load_json(pack / "assets" / "audio" / OVERLAY_DIR / "applied.json", {}) or {}
    if not applied and season:
        # baked into the pack (build_pack.py, no backup state): read the baked sets' own lists
        baked = [s["overlay"] for s in layers.audio_sets(season) if s.get("in_pack")]
        applied = {"files": sorted({f for s in baked
                                    for f in (load_json(AUDIO_DATA / "pack" / s / "overlay.json", {}) or {}).get("files", [])})}
    private = set(applied.get("files", []))
    private_audio = {f.split("assets/audio/", 1)[-1] for f in private}

    data_files = layers.files(season, "data") if season else {}
    none = Path("-")
    dsrc = field_sources(data_files.get("drivers.json", none), load_json(base / "drivers.json", []))
    tsrc = field_sources(data_files.get("teams.json", none), load_json(base / "teams.json", []))
    drivers, vanilla_drivers = build_drivers(pack, base, season, media, dsrc)
    teams, vanilla_teams = build_teams(pack, base, season, manifest, media, tsrc)
    engines, unit_rules, tyres = build_engines(pack, base, media)
    tracks, calendar = build_tracks(pack, base, season, manifest, media)
    juniors, licences = build_juniors(pack, base)
    junior_of = {n: s["series_abbreviation"] + " · " + t["name"] for s in juniors for t in s.get("teams", []) for n in t.get("drivers", [])}
    drivers = [{**d, "junior": junior_of.get(d["name"])} for d in drivers]
    backgrounds = build_backgrounds(pack, base, game, media)
    sounds = build_sounds(pack, base, media, private_audio | private)
    # candidates belong to the private audio pipeline: packs carrying its overlay show them, and
    # packs with a sound set still being made (unbuilt, e.g. dtm-2010) so its candidates can be heard
    has_set = bool(season and layers.audio_sets(season))
    candidates, library_page = build_candidates(media, pack, season) if private or has_set else ([], None)
    files = classify_files(pack, base, private, season)
    bc, pc = constants(base / "constants.py"), constants(pack / "constants.py")
    data = {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "pack": {"title": manifest["title"], "folder": pack_folder, "version": manifest.get("version"),
                 "base": base_name, "season": origin,
                 "workshop_item": manifest.get("workshop_item"),
                 "series": manifest.get("series"),
                 "private_audio": bool(private)},
        "drivers": drivers, "vanilla_drivers": vanilla_drivers,
        "driver_template": dsrc.get("$template_from"), "team_template": tsrc.get("$template_from"),
        "teams": teams, "vanilla_teams": vanilla_teams,
        "juniors": juniors, "licences": licences,
        "engines": engines, "unit_rules": unit_rules, "tyres": tyres,
        "tracks": tracks, "calendar": calendar, "backgrounds": backgrounds,
        "sounds": sounds, "candidates": candidates, "library_page": library_page,
        "files": files,
        "data_patches": data_patches(pack, base, season) if season else [],
        "constants": [{"name": k, "vanilla": bc.get(k), "mod": v} for k, v in pc.items() if bc.get(k) != v],
        "credits": (pack / "credits.txt").read_text(encoding="utf-8") if (pack / "credits.txt").exists() else "",
    }
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    short = re.sub(r"\s+mod$", "", re.split(r"\s+[-–]\s+", manifest["title"])[0], flags=re.I)
    page = (TEMPLATE.read_text(encoding="utf-8").replace("/*MOD_DATA*/null", blob)
            .replace("__PAGE_TITLE__", f"{short} Mod Browser".replace("&", "&amp;").replace("<", "&lt;")))
    out.mkdir(parents=True, exist_ok=True)
    (out / "page.html").write_text(page, encoding="utf-8")
    (out / "index.html").write_text(
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>\n'
        + page + "\n</body></html>\n", encoding="utf-8")
    removed = media.prune()
    n_audio = sum(1 for _ in (out / "media" / "audio").rglob("*.ogg")) if (out / "media" / "audio").exists() else 0
    print(f"mod browser: {out / 'index.html'} ({len(drivers)} drivers, {len(teams)} teams, {len(juniors)} feeder series, {len(tracks)} tracks, "
          f"{sum(len(g['items']) for g in backgrounds)} backgrounds, {len(sounds)} sound slots, {sum(len(g['items']) for g in candidates)} candidates, {n_audio} audio previews"
          + (f", {removed} stale media removed" if removed else "") + ")")
    return out / "index.html"


def write_index() -> Path:
    """private/mod_browser/index.html: a link to every browser built so far."""
    rows = []
    for page in sorted(OUT_ROOT.glob("*/page.html")):
        m = re.search(r"<title>(.*?)</title>", page.read_text(encoding="utf-8")[:20000])
        title = m.group(1) if m else page.parent.name
        rows.append(f'<li><a href="{page.parent.name}/index.html">{title}</a> <code>{page.parent.name}</code></li>')
    out = OUT_ROOT / "index.html"
    out.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Mod browsers</title>'
                   '<style>body{font:15px system-ui,sans-serif;margin:24px;line-height:1.7}code{color:#777}</style>'
                   '</head><body><h1>Mod browsers</h1><ul>' + "".join(rows) + "</ul></body></html>\n", encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("season", type=Path, nargs="?", default=REPO / "seasons" / "dtm-2013")
    ap.add_argument("--game", help="game folder (default: local.json game_path)")
    ap.add_argument("--pack", action="append", default=[], help="installed pack folder with no season source (repeatable)")
    ap.add_argument("--workshop", action="store_true", help="every installed data/workshop_* pack")
    args = ap.parse_args()
    game = game_path(args.game)
    packs = list(args.pack)
    if args.workshop:
        found = {p.name for p in (game / "data").glob("workshop_*") if p.is_dir()}
        found |= {f"workshop_{p.name}" for p in steam_workshop(game).glob("*") if p.is_dir()}
        packs += sorted(found)
    if packs:
        for folder in packs:
            build(None, game, folder)
    else:
        season = args.season if args.season.is_absolute() else REPO / args.season
        build(season, game)
    print(f"index: {write_index()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
