"""Stage 1 of the engine-audio pipeline: catalog the downloaded DTM 2013 videos.

Scans the yt-dlp queue folders (read-only) and maintains an incremental
manifest keyed by YouTube video id:

    private/engine_audio/library.sqlite   table `videos`
    private/engine_audio/manifest.csv     same rows, for eyeballing

Sources of truth, per queue folder:
    done.json   finished downloads            -> status "done"
    todo.json   still queued                  -> status "queued"
    a queued item whose "NNN - " file is already on disk:
                id in the root done.txt       -> status "legacy" (old yt-dlp run)
                otherwise                     -> status "partial" (do not trust)

Only "done" rows are processed by later stages unless they opt in to legacy.
Driver -> car and venue -> round come from seasons/dtm-2013/research, so
nothing here is tied to the current file list. Hand fixes go in
tools/engine_audio/overrides.csv (committed; metadata only, no audio).

    python tools/engine_audio/catalog.py [--source DIR] [--reprobe]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sqlite3
import subprocess
import sys
import unicodedata
from pathlib import Path

from common import DATA, DEFAULT_SOURCE, REPO

SEASON = REPO / "seasons" / "dtm-2013" / "research"
OVERRIDES = Path(__file__).with_name("overrides.csv")

MEDIA_EXT = {".mkv", ".webm", ".mp4", ".m4a", ".opus", ".ogg", ".mka"}

COLUMNS = [
    "id", "status", "folder", "idx", "title", "url", "file",
    "video_type", "manufacturer", "driver", "car", "track", "round", "session",
    "commentary", "confidence", "parse_notes", "overridden",
    "duration_s", "audio_codec", "sample_rate", "channels", "video_codec",
    "file_size", "file_mtime", "finished", "first_seen", "updated",
]

# Venue patterns run against folded titles; '.' covers a lost or mangled umlaut.
VENUES = [
    (r"brands\s*hatch", 2),
    (r"spielberg|red\s*bull\s*ring", 3),
    (r"lausitz", 4),
    (r"nor[i]?s[i]?\s*ring", 5),        # "Norsiring" typo exists
    (r"moscow|moskau", 6),
    (r"n(?:.|ue)rburgring", 7),
    (r"oschersleben", 8),
    (r"zandvoort", 9),
    (r"hockenheim", None),               # round decided below
    (r"barcelona|valencia", 0),          # pre-season tests
]

MAKES = [
    ("Audi", r"\baudi\b|\brs\s?5\b"),
    ("BMW", r"\bbmw\b|\bm3\b"),
    ("Mercedes", r"mercedes|\bamg\b|c-coup"),
]


def now() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def fold(s: str) -> str:
    """Lowercase ASCII; accents dropped, anything else non-ASCII becomes '?'."""
    out = []
    for ch in unicodedata.normalize("NFKD", s):
        if unicodedata.category(ch) == "Mn":
            continue
        out.append(ch.lower() if ord(ch) < 128 else "?")
    return "".join(out)


def name_regex(name: str) -> re.Pattern:
    """'Mattias Ekström' -> r'mattias\\s+ekstr.m' (matches ö, o, ? or a lost char)."""
    parts = []
    for ch in name:
        if ch == " ":
            parts.append(r"\s+")
        elif ord(ch) < 128:
            parts.append(re.escape(ch.lower()))
        else:
            parts.append(".")
    return re.compile("".join(parts))


def make_of(text: str) -> str | None:
    hits = [m for m, rx in MAKES if re.search(rx, text)]
    return hits[0] if len(hits) == 1 else None


# ---------------------------------------------------------------- season data

def load_season():
    drivers = []
    with open(SEASON / "entries.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            drivers.append({
                "name": row["driver"],
                "rx": name_regex(row["driver"]),
                "car": row["car"],
                "make": make_of(fold(row["car"] + " " + row["engine"])),
            })
    venues = {}
    with open(SEASON / "calendar.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            venues.setdefault(row["venue"], []).append(int(row["round"]))
    return drivers, venues


# --------------------------------------------------------------------- parser

def parse_title(title: str, drivers) -> dict:
    t = fold(title)
    notes = []
    r = {"video_type": "feature", "manufacturer": None, "driver": None, "car": None,
         "track": None, "round": None, "session": None, "commentary": "likely"}

    # venue / round
    for rx, rnd in VENUES:
        if re.search(rx, t):
            if rnd is None:  # Hockenheim: opener (1) or final (10)
                if re.search(r"final|finale|hockenheim\s+ii\b", t):
                    rnd = 10
                else:
                    rnd = 1
                    if not re.search(r"hockenheim\s+i\b|auftakt|generalprobe", t):
                        notes.append("plain 'Hockenheim' read as the opener")
            r["round"] = rnd
            break
    r["track"] = {0: "Test", 1: "Hockenheim", 2: "Brands Hatch", 3: "Spielberg", 4: "Lausitzring",
                  5: "Norisring", 6: "Moscow", 7: "Nurburgring", 8: "Oschersleben",
                  9: "Zandvoort", 10: "Hockenheim"}.get(r["round"])

    # session
    if re.search(r"qualif", t):
        r["session"] = "qualifying"
    elif re.search(r"\brace\b|\brennen\b", t):
        r["session"] = "race"

    # type
    if "streckenanimation" in t or "animation" in t:
        r["video_type"], r["commentary"] = "animation", "no-engine"
    elif re.match(r"onboards?\s+best\s+of", t):
        r["video_type"], r["commentary"] = "onboard_bestof", "no"
        r["session"] = r["session"] or "race"
    elif "taxi" in t:
        r["video_type"], r["commentary"] = "taxi", "possible"
    elif t.startswith("onboard"):
        r["video_type"], r["commentary"] = "onboard", "no"
        r["session"] = r["session"] or "race"
    elif "trackview" in t:
        r["video_type"], r["commentary"] = "trackview", "possible"
    elif re.search(r"re-?live", t) or re.match(r"(rennen|qualifikation)\b", t):
        r["video_type"] = "broadcast"
    elif "highlight" in t:
        r["video_type"] = "highlights"
        r["session"] = r["session"] or "race"

    # driver, matched against the season entry list
    hits = [d for d in drivers if d["rx"].search(t)]
    if len(hits) == 1:
        r["driver"] = hits[0]["name"]
    elif len(hits) > 1:
        notes.append("several drivers named: " + ", ".join(d["name"] for d in hits))

    # manufacturer: title first, entry list as fallback/cross-check
    title_make = make_of(t)
    entry = hits[0] if len(hits) == 1 else None
    if entry:
        r["car"] = entry["car"]
    if title_make and entry and entry["make"] and title_make != entry["make"]:
        notes.append(f"title says {title_make}, entry list says {entry['make']}")
        r["manufacturer"] = title_make
    elif title_make:
        r["manufacturer"] = title_make
    elif entry and entry["make"]:
        r["manufacturer"] = entry["make"]
        notes.append("car taken from entry list")

    r["confidence"] = score(r, notes)
    r["parse_notes"] = "; ".join(notes)
    return r


def score(r: dict, notes) -> float:
    vt = r["video_type"]
    if vt == "onboard":
        c = 1.0
        if not r["driver"]:
            c -= 0.5
            notes.append("no driver matched")
        if not r["manufacturer"]:
            c -= 0.3
        if not r["track"]:
            c -= 0.4
            notes.append("no track matched")
    elif vt == "trackview":
        c = 0.9 if (r["manufacturer"] and r["track"]) else 0.4
    elif vt in ("broadcast", "highlights", "onboard_bestof"):
        c = 0.9 if (r["track"] and r["session"]) else 0.5
    elif vt == "taxi":
        c = 0.3
        notes.append("passenger ride: car and driver need an override")
    else:
        c = 0.6 if r["track"] else 0.4
    if any(n.startswith("title says") for n in notes):
        c -= 0.3
    if any(n.startswith("plain 'Hockenheim'") for n in notes):
        c -= 0.1
    if any(n == "car taken from entry list" for n in notes):
        c -= 0.05
    return round(max(c, 0.0), 2)


def load_overrides() -> dict:
    """overrides.csv: id + any manifest column; blank cells are ignored."""
    if not OVERRIDES.exists():
        return {}
    out = {}
    with open(OVERRIDES, encoding="utf-8") as f:
        for row in csv.DictReader(line for line in f if not line.startswith("#")):
            vid = (row.pop("id") or "").strip()
            if vid:
                out[vid] = {k: v.strip() for k, v in row.items() if k in COLUMNS and v and v.strip()}
    return out


# --------------------------------------------------------------------- probing

def probe(path: Path) -> dict:
    cmd = ["ffprobe", "-v", "error", "-print_format", "json",
           "-show_format", "-show_streams", str(path)]
    try:
        info = json.loads(subprocess.run(cmd, capture_output=True, text=True,
                                         encoding="utf-8", check=True).stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        return {"probe_error": str(e)[:200]}
    a = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), {})
    v = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"
              and not s.get("disposition", {}).get("attached_pic")), {})
    dur = info.get("format", {}).get("duration")
    return {
        "duration_s": round(float(dur), 2) if dur else None,
        "audio_codec": a.get("codec_name"),
        "sample_rate": int(a["sample_rate"]) if a.get("sample_rate") else None,
        "channels": a.get("channels"),
        "video_codec": v.get("codec_name"),
    }


# ------------------------------------------------------------------- scanning

def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def find_numbered(folder: Path, idx) -> list[Path]:
    """Media files named 'NNN - *' (fragments, .part and .temp files excluded)."""
    if idx is None:
        return []
    return sorted(p for p in folder.glob(f"{int(idx):03d} - *")
                  if p.suffix.lower() in MEDIA_EXT and ".temp." not in p.name
                  and not re.search(r"\.f\d+\.\w+$", p.name))   # unmerged yt-dlp fragment


def scan(source: Path):
    legacy_ids = set()
    archive = source / "done.txt"
    if archive.exists():
        legacy_ids = {line.split()[-1] for line in archive.read_text(encoding="utf-8").splitlines() if line.strip()}

    for folder in sorted(p for p in source.iterdir() if p.is_dir()):
        done = load_json(folder / "done.json", [])
        todo = load_json(folder / "todo.json", {}).get("items", [])
        seen = set()
        for e in done:
            seen.add(e["id"])
            base = folder / e["subdir"] if e.get("subdir") else folder
            if e.get("file"):
                path = folder / e["file"]
            else:
                hits = find_numbered(base, e.get("index"))
                path = hits[0] if len(hits) == 1 else None
            yield "done", folder, e, path
        for e in todo:
            if e["id"] in seen:
                continue
            base = folder / e["subdir"] if e.get("subdir") else folder
            hits = find_numbered(base, e.get("index"))
            if not hits:
                yield "queued", folder, e, None
            else:   # on disk but not in done.json: never trusted by later stages
                path = hits[0] if len(hits) == 1 else None
                yield ("legacy" if e["id"] in legacy_ids else "partial"), folder, e, path


# ----------------------------------------------------------------------- main

def open_db() -> sqlite3.Connection:
    DATA.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DATA / "library.sqlite")
    db.row_factory = sqlite3.Row
    cols = ", ".join(f"{c} {'TEXT PRIMARY KEY' if c == 'id' else ''}" for c in COLUMNS)
    db.execute(f"CREATE TABLE IF NOT EXISTS videos ({cols})")
    have = {r[1] for r in db.execute("PRAGMA table_info(videos)")}
    for c in COLUMNS:
        if c not in have:
            db.execute(f"ALTER TABLE videos ADD COLUMN {c}")
    return db


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", type=Path, default=None, help="yt-dlp DTM root (read-only)")
    ap.add_argument("--reprobe", action="store_true", help="ffprobe every file again")
    args = ap.parse_args()

    local = load_json(REPO / "local.json", {})
    source = args.source or Path(local.get("engine_audio_source", DEFAULT_SOURCE))
    drivers, _ = load_season()
    overrides = load_overrides()
    db = open_db()
    old = {r["id"]: dict(r) for r in db.execute("SELECT * FROM videos")}

    stamp = now()
    seen, probed, new = set(), 0, 0
    # A video can sit in several playlists: keep its most finished copy.
    rank = {"done": 0, "legacy": 1, "partial": 2, "queued": 3}
    best = {}
    for item in scan(source):
        vid = item[2]["id"]
        if vid not in best or rank[item[0]] < rank[best[vid][0]]:
            best[vid] = item
    for status, folder, e, path in best.values():
        vid = e["id"]
        seen.add(vid)
        prev = old.get(vid, {})
        row = {c: prev.get(c) for c in COLUMNS}
        row.update(id=vid, status=status, folder=folder.name, idx=e.get("index"),
                   title=e.get("title"), url=e.get("url"),
                   file=str(path.relative_to(source)) if path else None,
                   finished=e.get("finished"), updated=stamp,
                   first_seen=prev.get("first_seen") or stamp)
        if not prev:
            new += 1
        row.update(parse_title(e.get("title") or "", drivers))
        ov = overrides.get(vid, {})
        row.update(ov)
        row["overridden"] = ",".join(sorted(ov)) or None

        if path and path.exists():
            st = path.stat()
            stale = (args.reprobe or prev.get("file_size") != st.st_size
                     or prev.get("file_mtime") != int(st.st_mtime) or not prev.get("audio_codec"))
            if stale:
                info = probe(path)
                if "probe_error" in info:
                    row["parse_notes"] = "; ".join(filter(None, [row["parse_notes"],
                                                                 "ffprobe failed"]))
                    info = {}
                row.update(info)
                probed += 1
            row["file_size"], row["file_mtime"] = st.st_size, int(st.st_mtime)
        else:
            for c in ("duration_s", "audio_codec", "sample_rate", "channels", "video_codec",
                      "file_size", "file_mtime"):
                row[c] = None

        db.execute(f"INSERT OR REPLACE INTO videos ({', '.join(COLUMNS)}) "
                   f"VALUES ({', '.join('?' * len(COLUMNS))})", [row[c] for c in COLUMNS])

    gone = set(old) - seen
    for vid in gone:
        db.execute("UPDATE videos SET status='missing', updated=? WHERE id=?", (stamp, vid))
    db.commit()

    rows = [dict(r) for r in db.execute("SELECT * FROM videos ORDER BY folder, idx")]
    with open(DATA / "manifest.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)

    print(f"{len(seen)} videos ({new} new, {probed} probed, {len(gone)} no longer listed) "
          f"-> {DATA / 'library.sqlite'}")
    report(rows)
    return 0


ROUNDS = ["Hockenheim", "Brands Hatch", "Spielberg", "Lausitzring", "Norisring",
          "Moscow", "Nurburgring", "Oschersleben", "Zandvoort", "Hockenheim F"]


def report(rows) -> None:
    """Coverage: cells are 'done/known (minutes done)'; known includes queued."""
    def cell(sel):
        done = [r for r in sel if r["status"] == "done"]
        if not sel:
            return "."
        mins = sum(r["duration_s"] or 0 for r in done) / 60
        return f"{len(done)}/{len(sel)}" + (f" {mins:.0f}m" if done else "")

    def table(title, cols, pick):
        print(f"\n{title}")
        print(f"{'round':<16}" + "".join(f"{c:>14}" for c in cols))
        for i, name in enumerate(ROUNDS, 1):
            line = [cell([r for r in rows if r["round"] == i and pick(r, c)]) for c in cols]
            print(f"{i:>2} {name:<13}" + "".join(f"{x:>14}" for x in line))

    table("Onboard laps (driver onboards + manufacturer trackviews)",
          ["Audi", "BMW", "Mercedes", "best-of"],
          lambda r, c: (r["video_type"] in ("onboard", "trackview") and r["manufacturer"] == c)
          or (c == "best-of" and r["video_type"] in ("onboard_bestof", "taxi")))
    table("TV material (commentary over trackside engine sound)",
          ["race", "qualifying", "highlights"],
          lambda r, c: (r["video_type"] == "broadcast" and r["session"] == c)
          or (c == "highlights" and r["video_type"] == "highlights"))
    statuses = {}
    for r in rows:
        statuses[r["status"]] = statuses.get(r["status"], 0) + 1
    print("\nstatus: " + ", ".join(f"{k} {v}" for k, v in sorted(statuses.items())))


if __name__ == "__main__":
    sys.exit(main())
