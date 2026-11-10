"""List a built pack's own in-game texts that could be translated.

Reads dist/<pack_folder> (run tools/build_pack.py first) and the vanilla
base pack it was built from (<game>/data/<base_pack>), and keeps only text
the pack itself adds or changes: vanilla strings are the game's to translate.

Writes seasons/<season>/translations.csv with the columns

    file, key, kind, en, de

kind is one of
    text   a sentence or paragraph shown in-game (team histories, rule
           descriptions, radio messages)
    label  a short UI word or abbreviation (car part names)
    name   a proper name, usually kept as it is (tracks, the pack title)

The de column is left empty for a translator. Team, driver, sponsor and
engine names, ids, keys and "$comment" notes are left out: they are names or
are never shown. The game has no language setting yet (wishlist E13), so a
translation would ship as a second pack.

Usage:
    python tools/translatable_strings.py seasons/dtm-2013
"""

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import layers

REPO = Path(__file__).resolve().parent.parent


def load(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def rows(pack, vanilla):
    out = []

    def add(file, key, kind, text, old=None):
        if isinstance(text, str) and text.strip() and text != old:
            out.append({"file": file, "key": key, "kind": kind, "en": text, "de": ""})

    histories = load(pack / "team_histories.json") or {}
    old = load(vanilla / "team_histories.json") or {}
    for team, text in histories.items():
        add("team_histories.json", team, "text", text, old.get(team))

    regs = load(pack / "regulations.json") or {"categories": []}
    old_regs = load(vanilla / "regulations.json") or {"categories": []}
    old_opts = {(c["key"], o.get("key")): o for c in old_regs["categories"] for o in c.get("options", [])}
    for cat in regs["categories"]:
        for opt in cat.get("options", []):
            prev = old_opts.get((cat["key"], opt.get("key")), {})
            for field, kind in (("name", "name"), ("summary", "text"), ("description", "text")):
                add("regulations.json", f"{cat['key']}.{opt.get('key')}.{field}", kind, opt.get(field), prev.get(field))

    quotes = (load(pack / "radio_quotes.json") or {}).get("quotes", {})
    old_quotes = (load(vanilla / "radio_quotes.json") or {}).get("quotes", {})
    for event, lines in quotes.items():
        known = set(old_quotes.get(event, []))
        for i, line in enumerate(lines):
            if line not in known:
                add("radio_quotes.json", f"{event}[{i}]", "text", line)

    parts = (load(pack / "car_parts.json") or {}).get("parts", {})
    old_parts = (load(vanilla / "car_parts.json") or {}).get("parts", {})
    for part, spec in parts.items():
        for field in ("label", "abbr"):
            add("car_parts.json", f"{part}.{field}", "label", spec.get(field), old_parts.get(part, {}).get(field))

    for track in sorted((pack / "tracks").glob("*.json")):
        old_track = load(vanilla / "tracks" / track.name) or {}
        add(f"tracks/{track.name}", "name", "name", load(track).get("name"), old_track.get("name"))

    add("workshop.json", "title", "name", (load(pack / "workshop.json") or {}).get("title"))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("season", type=Path)
    parser.add_argument("--game", help="game folder (default: local.json game_path)")
    args = parser.parse_args()
    season = args.season.resolve()
    manifest = layers.manifest(season)
    game = Path(args.game or json.loads((REPO / "local.json").read_text(encoding="utf-8"))["game_path"])
    pack = REPO / "dist" / manifest["pack_folder"]
    if not pack.is_dir():
        sys.exit(f"{pack} not found: run tools/build_pack.py {args.season} first")
    vanilla = game / "data" / manifest["base_pack"]
    found = rows(pack, vanilla)
    out = season / "translations.csv"
    with open(out, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, ["file", "key", "kind", "en", "de"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(found)
    counts = {k: sum(r["kind"] == k for r in found) for k in ("text", "label", "name")}
    print(f"wrote {out.relative_to(REPO)}: {len(found)} strings ({counts['text']} text, "
          f"{counts['label']} label, {counts['name']} name)")


if __name__ == "__main__":
    main()
