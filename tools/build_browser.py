"""Build the season browser: one self-contained HTML page with all research data.

Reads seasons/*/research/{calendar,entries,standings,standings_other}.csv and
the season dossier (research/season.md, or the season README.md), and writes
build/season-browser/index.html.

Usage:
    python tools/build_browser.py
"""

import csv
import json
import re
from pathlib import Path

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
            "playable": (folder / "season.json").exists(),
            "champion": champion,
            "calendar": read_csv(research / "calendar.csv"),
            "entries": read_csv(research / "entries.csv"),
            "standings": standings,
            "standings_other": read_csv(research / "standings_other.csv"),
            "dossier": md,
        })
    data = json.dumps({"seasons": seasons}, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", data)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(REPO)}: {len(seasons)} seasons, {len(html) // 1024} KB")


if __name__ == "__main__":
    main()
