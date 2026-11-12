"""Build the season browser: one self-contained HTML page with all research data.

Reads seasons/*/research/{calendar,entries,standings,standings_other}.csv and
the season dossier (research/season.md, or the season README.md), and writes
build/season-browser/index.html. The Tracks section comes from
tools/track_inventory.py: every venue, every race held there, and our track
files, results and photo research for it.

Usage:
    python tools/build_browser.py
"""

import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import track_inventory  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "build" / "season-browser" / "index.html"
TEMPLATE = Path(__file__).resolve().parent / "browser_template.html"


def read_csv(path):
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    return {"header": rows[0], "rows": rows[1:]} if rows else None


def series_of(folder, md):
    if folder.startswith("itc"):
        return "ITC"
    year = int(folder.split("-")[1])
    if year <= 1985:
        return "DPM"
    if year == 1995:
        return "DTM / ITC"
    return "DTM"


ERAS = [(1984, 1992, "Production & Group A"), (1993, 1996, "Class 1"), (2000, 2011, "Masters V8"),
        (2012, 2018, "Class One"), (2019, 2020, "Class One turbo"), (2021, 2100, "GT3")]


# How closely each period's sporting rules match what Team Principal can model
# (see docs/ERAS.md). Ranked best first; score is out of 5.
GAME_FIT = [
    {"years": "2013", "score": 5, "fits": "One race per weekend; F1 points 25-18-15...; DRS; option tyre that must be used (compound rule); no refuelling; knockout qualifying; no ballast or performance weights; 2-car teams; single tyre supplier",
     "gaps": "Q4 single-lap shootout; second mandatory stop; DRS off for the last 3 laps"},
    {"years": "2014", "score": 5, "fits": "Same as 2013, plus F1-style Q1-Q3 knockout exactly as in the game, one mandatory stop and DRS to the end of the race",
     "gaps": "Performance weights per make (up to 10 kg); soft tyre limited to half the race distance; pit window"},
    {"years": "2012", "score": 4, "fits": "One race; F1 points; knockout qualifying; no refuelling; two mandatory stops",
     "gaps": "Mandatory pit windows; Q4 shootout; no DRS or option tyre, so the game's modern features stay unused"},
    {"years": "2003-2011", "score": 3, "fits": "One race per event; mandatory stops; refuelling (2003); custom points table 10-8-6-5-4-3-2-1",
     "gaps": "Placement weights (+/-5 kg per race); weight breaks for year-old cars; Superpole qualifying; pit windows"},
    {"years": "2015-2020", "score": 2, "fits": "DRS; mandatory stop; F1 points; push-to-pass (2019-20) via spec ERS",
     "gaps": "Two races per weekend; time-limited races; performance weights; qualifying points"},
    {"years": "2021-2026", "score": 2, "fits": "Mandatory stops; qualifying points as a bonus-point rule; many makes",
     "gaps": "Two races per weekend; time-limited races; balance of performance; success ballast; pit windows; customer GT3 cars"},
    {"years": "2000-2002", "score": 2, "fits": "Mandatory stop (2001-02); no refuelling",
     "gaps": "Qualifying race plus main race per event; points split between both races"},
    {"years": "1993-1996", "score": 1, "fits": "Driver aids and 4WD allowed via driver-aid rules",
     "gaps": "Two heats per round; weight rules; no planned stops"},
    {"years": "1984-1992", "score": 1, "fits": "Custom points table; no pit stops",
     "gaps": "Two heats and a qualification race per round; success ballast up to 50-100 kg; displacement-based weights"},
]


def era_of(year):
    return next((name for lo, hi, name in ERAS if lo <= year <= hi), "")


def main():
    seasons = []
    for folder in sorted((REPO / "seasons").iterdir()):
        research = folder / "research"
        if not research.is_dir() or not re.match(r"^(dtm|itc)-\d{4}$", folder.name):
            continue
        md_path = research / "season.md" if (research / "season.md").exists() else folder / "README.md"
        md = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
        standings = read_csv(research / "standings.csv")
        champion = ""
        if standings:
            h = standings["header"]
            rows = standings["rows"]
            if "championship" in h:
                rows = [r for r in rows if r[h.index("championship")] in ("DTM", "ITC")] or rows
            first = next((r for r in rows if r[h.index("pos")] == "1"), None)
            champion = first[h.index("driver")] if first else ""
        seasons.append({
            "id": folder.name,
            "year": int(folder.name.split("-")[1]),
            "series": series_of(folder.name, md),
            "era": era_of(int(folder.name.split("-")[1])),
            "playable": (folder / "season.json").exists(),
            "champion": champion,
            "calendar": read_csv(research / "calendar.csv"),
            "entries": read_csv(research / "entries.csv"),
            "standings": standings,
            "standings_other": read_csv(research / "standings_other.csv"),
            "dossier": md,
        })
    tracks = track_inventory.build()
    data = json.dumps({"seasons": seasons, "fit": GAME_FIT, "tracks": tracks}, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", data)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(REPO)}: {len(seasons)} seasons, {len(tracks)} venues, {len(html) // 1024} KB")


if __name__ == "__main__":
    main()
