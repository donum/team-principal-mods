"""Track the game's Steam patch notes in docs/game/changelog.csv.

Pulls the official announcements from the Steam news feed (ISteamNews,
app 4340600, the same posts as steamcommunity.com/app/4340600/eventcomments)
and adds any post not yet in the CSV, with an empty mod_impact column. That
column is written by hand: what the post means for our packs, or "none".

The CSV keeps only date, title, link and our own notes. The full text of the
new posts is printed (and with --text saved to the scratch file you name),
so it can be read once and summed up in mod_impact.

    python -I tools/game_changelog.py                 add new posts, print them
    python -I tools/game_changelog.py --text out.txt  also save their text
    python -I tools/game_changelog.py --open          list rows still without mod_impact
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

APP_ID = 4340600
FEED = (
    "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
    f"?appid={APP_ID}&count=100&maxlength=0&format=json"
)
PAGE = f"https://store.steampowered.com/news/app/{APP_ID}/view/"
ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "docs" / "game" / "changelog.csv"
FIELDS = ["date", "title", "gid", "url", "mod_impact"]


def fetch() -> list[dict]:
    req = urllib.request.Request(FEED, headers={"User-Agent": "tp-mods-changelog/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["appnews"]["newsitems"]


def plain(bbcode: str) -> str:
    """Steam BBCode to readable text."""
    t = re.sub(r"\[/?(p|h\d|list|olist|\*|hr|quote|table|tr|td|th)\]", "\n", bbcode)
    t = re.sub(r"\[/?[a-z]+(=[^\]]*)?\]", "", t)
    t = re.sub(r"\{STEAM_CLAN_IMAGE\}\S*", "", t)
    return re.sub(r"\n\s*\n+", "\n", html.unescape(t)).strip()


def load() -> list[dict]:
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save(rows: list[dict]) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows.sort(key=lambda r: (r["date"], r["gid"]), reverse=True)
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--text", type=Path, help="save the new posts' text to this file")
    ap.add_argument("--open", action="store_true", help="list rows without mod_impact")
    a = ap.parse_args()

    rows = load()
    if a.open:
        for r in rows:
            if not r["mod_impact"].strip():
                print(r["date"], r["title"], r["url"])
        return 0

    known = {r["gid"] for r in rows}
    new = [n for n in fetch() if str(n["gid"]) not in known]
    new.sort(key=lambda n: n["date"])
    out = []
    for n in new:
        date = dt.datetime.fromtimestamp(n["date"], dt.timezone.utc).date().isoformat()
        rows.append({"date": date, "title": n["title"].strip(), "gid": str(n["gid"]),
                     "url": f"{PAGE}{n['gid']}", "mod_impact": ""})
        out.append(f"=== {date} {n['title'].strip()}\n{PAGE}{n['gid']}\n\n{plain(n['contents'])}\n")
    save(rows)

    if not new:
        print("No new posts.")
        return 0
    text = "\n".join(out)
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"{len(new)} new post(s) added to {CSV_PATH.relative_to(ROOT)}:\n")
    print(text)
    if a.text:
        a.text.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
