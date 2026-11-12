"""Track inventory for the season archive: every venue on a DPM, DTM or ITC
calendar, every race held there, and everything we have for it.

Venue names in the calendars vary ("Hockenheim – Jim-Clark-Rennen",
"Hockenheimring"), so VENUES maps them to one key. The Nürburgring is split
into the GP circuit and the Nordschleife.

For each venue it collects:
    races       every calendar row (season, round, date, layout, length, winners)
                plus the round's results files (research/results/NN-*.csv)
    layouts     the distinct layouts by length, with the years they were used
    game        our generated tracks: specs (track_specs/), laps (tracks/),
                maps (assets/tracks/) and art-matched tracks (track_art.json),
                in seasons/ and bases/, with the rounds of playable packs that
                run on them (data/schedule.json)
    history     the layout versions from the sibling race-tracks repo
    media       photo research: InMotion albums, imago candidates,
                media_sources.csv rows, and the local 2013 photo gallery

Paths are relative to the repository root; the page turns them into links.
Sources outside the repo (race-tracks, the gallery) are optional.

    python tools/track_inventory.py      print a summary
"""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RACE_TRACKS = REPO.parent / "race-tracks"
RACE_TRACK_THEMES = REPO.parent / "race-track-themes"
GALLERY = Path.home() / "Pictures" / "mods" / "dtm-2013-gallery"

# (pattern, key, country). Patterns are searched in venue names and in free
# text (file names, captions), so short names need word boundaries.
VENUES = [
    (r"AVUS", "AVUS", "GER"),
    (r"Alemannenring|\bSingen\b", "Alemannenring (Singen)", "GER"),
    (r"\bBrno\b|Masaryk", "Brno", "CZE"),
    (r"\bBologna\b", "Bologna Motor Show", "ITA"),
    (r"Zolder", "Zolder", "BEL"),
    (r"Diepholz", "Diepholz", "GER"),
    (r"Donington", "Donington Park", "GBR"),
    (r"\bErding\b", "Erding", "GER"),
    (r"Estoril", "Estoril", "POR"),
    (r"Wunstorf", "Wunstorf", "GER"),
    (r"Mainz", "Mainz-Finthen", "GER"),
    (r"Helsinki", "Helsinki", "FIN"),
    (r"Hockenheim", "Hockenheim", "GER"),
    (r"Hungaroring", "Hungaroring", "HUN"),
    (r"Interlagos", "Interlagos", "BRA"),
    (r"Magny", "Magny-Cours", "FRA"),
    (r"Mugello", "Mugello", "ITA"),
    (r"Norisring", "Norisring", "GER"),
    (r"Salzburg", "Salzburgring", "AUT"),
    (r"Siegerland", "Siegerland", "GER"),
    (r"Silverstone", "Silverstone", "GBR"),
    (r"Suzuka", "Suzuka", "JPN"),
    (r"A1-Ring|Red ?Bull ?Ring|Spielberg", "Red Bull Ring (A1-Ring)", "AUT"),
    (r"Lausitz", "Lausitzring", "GER"),
    (r"Oschersleben", "Oschersleben", "GER"),
    (r"Zandvoort", "Zandvoort", "NED"),
    (r"\bAdria\b", "Adria", "ITA"),
    (r"\bMonza\b", "Monza", "ITA"),
    (r"Algarve|Portim", "Portimão", "POR"),
    (r"Catalunya|Barcelona", "Barcelona", "ESP"),
    (r"\bSpa\b|Francorchamps", "Spa-Francorchamps", "BEL"),
    (r"Dijon", "Dijon-Prenois", "FRA"),
    (r"Istanbul", "Istanbul Park", "TUR"),
    (r"Misano", "Misano", "ITA"),
    (r"Moscow|Moskau", "Moscow Raceway", "RUS"),
    (r"\bAssen\b", "Assen", "NED"),
    (r"München|Munich|Olympiastadion", "Munich (Olympic Stadium)", "GER"),
    (r"Sachsenring", "Sachsenring", "GER"),
    (r"Valencia|Ricardo Tormo", "Valencia", "ESP"),
    (r"\bImola\b", "Imola", "ITA"),
    (r"Le Mans", "Le Mans", "FRA"),
    (r"Brands ?Hatch", "Brands Hatch", "GBR"),
]
VENUES = [(re.compile(p, re.I), k, c) for p, k, c in VENUES]
NUERBURG = re.compile(r"N(ü|u|ue)rburg", re.I)
NORDSCHLEIFE = "Nürburgring Nordschleife"
NUERBURG_GP = "Nürburgring GP"
COUNTRY = {k: c for _, k, c in VENUES} | {NORDSCHLEIFE: "GER", NUERBURG_GP: "GER"}


def venue_key(name, layout="", length=""):
    """The venue key for a calendar row or a track name, or None."""
    if NUERBURG.search(name):
        try:
            long_lap = float(length) > 20
        except (TypeError, ValueError):
            long_lap = False
        return NORDSCHLEIFE if re.search(r"Nordschleife", name + " " + layout, re.I) or long_lap else NUERBURG_GP
    hit = next((k for rx, k, _ in VENUES if rx.search(name)), None)
    return hit


def venues_in_text(text):
    """Every venue mentioned in a free text (a file name, a caption)."""
    found = []
    if NUERBURG.search(text):
        found.append(NORDSCHLEIFE if re.search(r"Nordschleife", text, re.I) else NUERBURG_GP)
    found += [k for rx, k, _ in VENUES if rx.search(text) and k not in found]
    return found


def rel(path):
    return Path(path).resolve().relative_to(REPO).as_posix()


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def read_rows(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def season_dirs():
    return [d for d in sorted((REPO / "seasons").iterdir()) if re.match(r"^(dtm|itc)-\d{4}$", d.name)]


# ---------------------------------------------------------------- races

def collect_races(venues):
    for folder in season_dirs():
        year = int(folder.name.split("-")[1])
        results = defaultdict(list)
        for f in sorted((folder / "research" / "results").glob("*.csv")):
            m = re.match(r"^(\d+)-[^-]+-(.+)\.csv$", f.name)
            if m:
                results[int(m.group(1))].append({"session": m.group(2), "path": rel(f)})
        for r in read_rows(folder / "research" / "calendar.csv"):
            name = (r.get("venue") or "").strip()
            if not name:
                continue
            layout, length = (r.get("circuit_layout") or "").strip(), (r.get("length_km") or "").strip()
            key = venue_key(name, layout, length) or re.split(r"\s+[–(-]", name)[0].strip()
            rnd = (r.get("round") or "").strip()
            v = venues[key]
            v.setdefault("country", COUNTRY.get(key) or (r.get("country") or "").strip())
            v["races"].append({
                "season": folder.name, "year": year, "round": rnd, "date": (r.get("date") or "").strip(),
                "event": name, "layout": layout, "length_km": length, "heats": (r.get("heats") or "").strip(),
                "winners": (r.get("winners") or "").strip(),
                "results": results.get(int(rnd), []) if rnd.isdigit() else [],
            })


def summarise_layouts(v):
    """Group the races by lap length: one row per distinct layout. Sources
    round the same lap differently (6.797, 6.815, 6.840 km), so lengths
    within 1% of the group's shortest lap count as one layout."""
    def length(r):
        try:
            return float(r["length_km"])
        except ValueError:
            return None
    groups = []
    for r in sorted(v["races"], key=lambda r: (length(r) is None, length(r) or 0)):
        km = length(r)
        g = groups[-1] if groups and (km is None) == (groups[-1]["lo"] is None) and (
            km is None or km <= groups[-1]["lo"] * 1.01) else None
        if g is None:
            g = {"lo": km, "hi": km, "names": [], "years": set(), "races": 0}
            groups.append(g)
        g["hi"] = km
        name = re.sub(r"\s*\((?:[^()]*(?:Preis|Rennen|Festival|Trophäe|Cup|Gold|Eifel|Meilen)[^()]*)\)", "", r["layout"]).strip()
        if name and name not in g["names"]:
            g["names"].append(name)
        g["years"].add(r["year"])
        g["races"] += 1
    for g in groups:
        g["length_km"] = "?" if g["lo"] is None else (
            f"{g['lo']:.3f}" if g["hi"] - g["lo"] < 0.001 else f"{g['lo']:.3f}–{g['hi']:.3f}")
        g["years"] = sorted(g["years"])
        del g["lo"], g["hi"]
    v["layouts"] = sorted(groups, key=lambda g: (g["length_km"] == "?", g["years"][0]))


# ---------------------------------------------------------------- game tracks

def collect_game_tracks(venues):
    """Every track we have generated, in seasons/ and bases/, keyed by owner/id."""
    owners = [("season", d) for d in season_dirs()] + [("base", d) for d in sorted((REPO / "bases").iterdir()) if d.is_dir()]
    tracks = {}
    for kind, d in owners:
        ids = {p.stem for p in (d / "track_specs").glob("*.json")} | {p.stem for p in (d / "tracks").glob("*.json")}
        art = (read_json(d / "track_art.json") or {}).get("tracks", {})
        for tid in sorted(ids):
            spec = d / "track_specs" / f"{tid}.json"
            lap = d / "tracks" / f"{tid}.json"
            png = d / "assets" / "tracks" / f"{tid}.png"
            a = art.get(tid, {})
            if not spec.exists() and a.get("spec"):
                spec = REPO / a["spec"]
            meta = read_json(spec) if spec.exists() else None
            meta = meta or read_json(lap) or {}
            name = meta.get("name") if isinstance(meta.get("name"), str) else tid
            art_path = a.get("art") or ""
            art_file = RACE_TRACK_THEMES / art_path if art_path else None
            tracks[(d.name, tid)] = {
                "id": tid, "owner": d.name, "owner_kind": kind, "name": name,
                "length_km": meta.get("length_km"),
                "spec": rel(spec) if spec.exists() else "",
                "lap": rel(lap) if lap.exists() else "",
                "map": rel(png) if png.exists() else "",
                "art": art_file.resolve().as_uri() if art_file and art_file.exists() else "",
                "art_layout": "/".join(filter(None, [a.get("race_tracks", {}).get("track"), a.get("race_tracks", {}).get("layout")])),
                "notes": meta.get("notes", "") if isinstance(meta.get("notes"), str) else "",
                "used_by": [],
            }
    # Which rounds of the playable packs run on which track file.
    for d in season_dirs():
        season = read_json(d / "season.json")
        schedule = read_json(d / "data" / "schedule.json")
        if not season or not isinstance(schedule, list):
            continue
        shared = season.get("shared_tracks", {})
        base = season.get("base")
        races = [t for t in schedule if t and t not in ("private", "test")]
        for n, tid in enumerate(races, 1):
            for owner in (d.name, shared.get(tid), base):
                if owner and (owner, tid) in tracks:
                    tracks[(owner, tid)]["used_by"].append({"season": d.name, "round": str(n)})
                    break
    for t in tracks.values():
        key = venue_key(t["name"], "", t["length_km"] or "") or venue_key(t["id"])
        if key in venues:
            venues[key]["game"].append(t)


# ---------------------------------------------------------------- race-tracks repo

def collect_race_tracks(venues):
    if not (RACE_TRACKS / "tracks").is_dir():
        return
    index = (RACE_TRACKS / "index.html").resolve().as_uri()
    for d in sorted((RACE_TRACKS / "tracks").iterdir()):
        t = read_json(d / "track.json")
        if not t:
            continue
        keys = {venue_key(t.get("name", "")) or venue_key(d.name)}
        if NUERBURG.search(t.get("name", "")):
            keys = {NUERBURG_GP, NORDSCHLEIFE}
        for key in keys:
            if key not in venues:
                continue
            versions = []
            for lay in t.get("layouts", []):
                if key == NORDSCHLEIFE and not re.search(r"nordschleife", lay.get("id", "") + lay.get("name", ""), re.I):
                    continue
                if key == NUERBURG_GP and re.search(r"nordschleife", lay.get("id", "") + lay.get("name", ""), re.I):
                    continue
                for ver in lay.get("versions", []):
                    versions.append({"layout": lay.get("name", lay.get("id")), "id": f"{lay.get('id')}@{ver.get('id')}",
                                     "from": ver.get("from"), "to": ver.get("to"), "length_m": ver.get("lengthM"),
                                     "changes": ver.get("changes", "")})
            venues[key]["history"] = {
                "id": d.name, "summary": t.get("summary", ""), "type": t.get("type", ""), "opened": t.get("opened"),
                "wikipedia": t.get("wikipedia", {}), "link": f"{index}#/tracks/{d.name}",
                "versions": sorted(versions, key=lambda x: (x["from"] or 0, x["layout"])),
            }


# ---------------------------------------------------------------- media

def add_media(venues, key, item):
    if key in venues:
        venues[key]["media"].append(item)


def collect_media(venues):
    for d in season_dirs():
        year = int(d.name.split("-")[1])
        research = d / "research"
        # media_sources.csv: photos and drawings listed per driver; the venue is in the title or notes.
        hits = defaultdict(list)
        for r in read_rows(research / "media_sources.csv"):
            for key in venues_in_text(f"{r.get('title', '')} {r.get('notes', '')}"):
                hits[key].append({"title": r.get("title", ""), "url": r.get("url", ""), "year": r.get("year", "")})
        for key, items in hits.items():
            add_media(venues, key, {"kind": "Media sources", "season": d.name, "year": year, "count": len(items),
                                    "path": rel(research / "media_sources.csv"), "items": items[:12]})
        # inmotion_photos.md: one table row per album, "[Zandvoort 2013](url) | date | photos".
        md = research / "inmotion_photos.md"
        if md.exists():
            for m in re.finditer(r"^\|\s*\[([^\]]+?)\s+(\d{4})\]\((https?://[^)]+)\)\s*\|[^|]*\|\s*(\d+)", md.read_text(encoding="utf-8"), re.M):
                key = venue_key(m.group(1))
                local = REPO / "reference" / "inmotion-photos" / f"dtm-{m.group(1).lower()}-{m.group(2)}"
                add_media(venues, key, {"kind": "InMotion Photos album", "season": d.name, "year": int(m.group(2)),
                                        "count": int(m.group(4)), "url": m.group(3), "path": rel(md),
                                        "local": local.resolve().as_uri() if local.is_dir() else "",
                                        "note": "Permission granted (credit and backlink)"})
        # imago_candidates.md: shot rows mention the venue.
        md = research / "imago_candidates.md"
        if md.exists():
            counts = defaultdict(int)
            for line in md.read_text(encoding="utf-8").splitlines():
                if line.startswith("|") and "imago-images" in line:
                    for key in venues_in_text(line):
                        counts[key] += 1
            for key, n in counts.items():
                add_media(venues, key, {"kind": "imago candidates", "season": d.name, "year": year, "count": n,
                                        "path": rel(md), "note": "Rights-managed: ask before use"})
    # The local 2013 gallery (outside the repo): photos whose file name or caption names the venue.
    data = GALLERY / "data.js"
    if data.exists():
        text = data.read_text(encoding="utf-8")
        start = text.find("window.GALLERY=")
        try:
            photos = json.JSONDecoder().raw_decode(text[start + len("window.GALLERY="):])[0]
        except ValueError:
            photos = []
        hits = defaultdict(list)
        for p in photos:
            if p.get("kind") != "photo" or p.get("unsuitable"):
                continue
            for key in venues_in_text(f"{p.get('rel', '')} {p.get('caption') or ''}"):
                hits[(key, p.get("year") or "")].append(p)
        for (key, yr), ps in hits.items():
            add_media(venues, key, {
                "kind": "Photo gallery", "season": f"dtm-{yr}" if yr else "", "year": int(yr) if str(yr).isdigit() else None,
                "count": len(ps), "url": (GALLERY / "index.html").resolve().as_uri(),
                "note": ", ".join(f"{n} {s}" for s, n in sorted(_count(p.get("source") for p in ps).items(), key=lambda x: -x[1])),
                "thumbs": [(GALLERY / p["thumb"]).resolve().as_uri() for p in ps if p.get("thumb")
                           and p.get("source") in ("commons", "flickr_cc", "permission")][:6],
            })


def _count(it):
    out = defaultdict(int)
    for x in it:
        out[x or "?"] += 1
    return out


# ---------------------------------------------------------------- main

def build():
    venues = defaultdict(lambda: {"races": [], "game": [], "media": [], "history": None})
    collect_races(venues)
    collect_game_tracks(venues)
    collect_race_tracks(venues)
    collect_media(venues)
    out = []
    for key, v in venues.items():
        if not v["races"]:
            continue
        summarise_layouts(v)
        v["races"].sort(key=lambda r: (r["year"], int(r["round"]) if r["round"].isdigit() else 99))
        years = sorted({r["year"] for r in v["races"]})
        v["game"].sort(key=lambda t: (t["owner_kind"] != "season", t["owner"], t["id"]))
        v["media"].sort(key=lambda m: (m.get("year") or 0, m["kind"]))
        out.append({"key": key, "slug": re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-"),
                    "country": v.get("country", ""), "years": years, **v})
    out.sort(key=lambda v: (-len(v["races"]), v["key"]))
    return out


if __name__ == "__main__":
    vs = build()
    for v in vs:
        print(f"{len(v['races']):3} races {len(v['years']):2} yrs  game {len(v['game'])}  media {len(v['media'])}  "
              f"{'history ' if v['history'] else '        '}{v['key']}")
