"""Sort the DTM fandom wiki SVGs from a download folder into the picture library.

The wiki's image server (static.wikia.nocookie.net) answers scripts with a
Cloudflare check, so the files are saved by hand in a browser: open
reference/driver_careers/svg_urls.txt in a download manager (or save the links
one by one) into Downloads. This script then files them:

  cars           -> <out>/<year>/<Name_Year>.svg   (one per driver and season)
  track maps     -> <out>/tracks/
  autographs     -> <out>/autographs/
  everything else-> <out>/logos/

and writes <out>/SOURCES.csv (file, kind, year, uploader, uploaded, wiki page)
plus <out>/MISSING.txt with the wiki files not found yet. Run it again after
more downloads; files already in place are kept.

docs/drivers/fandom_svg_fixes.csv (file, field, value, reason) corrects SOURCES rows where
the wiki table is wrong, checked against what the drawing shows: number, driver, team, car,
kind ('logo' for a non-car), and placeholder 'yes' for the grey '?' cars (no livery known).

Usage: python -I tools/careers/sort_svgs.py [downloads] [out]
"""
import csv
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
FACTS = ["number", "driver", "make", "team", "car", "tyres", "guest"]
FILES = REPO / "reference" / "driver_careers" / "files.json"
FIXES = REPO / "docs" / "drivers" / "fandom_svg_fixes.csv"   # checked against the drawing itself


# The wiki redirects some files, so the browser saves them under the target's
# name. Saved name -> wiki file name (checked on the 1984 season page etc.).
RENAMED = {
    "Susie_Wolff_2011.svg": "Susie_Stoddart_2011.svg",
    "Eric_Helary_2002.svg": "Éric_Hélary_2002.svg",
    "Dieter_Miltz_1984.svg": "Dieter_Miltz_1984_(92).svg",
    "Robert_Walterscheid-Müller_1984_BMW.svg": "Robert_Walterscheid-Müller_1984_(12).svg",  # #12 BMW 635 CSi
    "Robert_Walterscheid-Müller_1984_Opel.svg": "Robert_Walterscheid-Müller_1984.svg",  # #46 Opel Manta
    "__2023.svg": "???_2023.svg",  # Windows has no "?" in file names
}


def safe(name):
    """A file name Windows accepts ("???_2023.svg" -> "unknown_2023.svg")."""
    return re.sub(r'[?<>:"|*]+', "unknown", name)


def norm(name):
    """Browsers save 'A_B.svg' as 'A_B.svg' or 'A B.svg', sometimes with ' (1)'."""
    name = unicodedata.normalize("NFC", name)
    name = re.sub(r" \(\d+\)(?=\.svg$)", "", name)
    return name.replace(" ", "_").lower()


def kind_of(name):
    if re.search(r"\((\d{4}-\d{4}|\d{4}-|seit_\d{4}|bis_\d{4})\)", name) or re.match(r"^[A-Za-z-]+_\(\d{4}\)\.svg$", name):
        return "logo", "", "logos"  # make logos by period: BMW_(1997-2020), Audi_(seit_2016)
    y = re.search(r"(19[89]\d|20[0-2]\d)", name)
    if y:
        return "car", y.group(1), y.group(1)
    if "Autogramm" in name:
        return "autograph", "", "autographs"
    if re.search(r"_\d+,\d{3}\.svg$", name):
        return "track", "", "tracks"
    return "logo", "", "logos"


def link_text(s):
    m = re.search(r"\[\[([^|\]]+)(?:\|([^\]]+))?\]\]", s)
    return (m.group(2) or m.group(1)).strip() if m else re.sub(r"<[^>]+>|\{\{[^{}]*\}\}", "", s).strip()


def entries():
    """norm(file name) -> car facts from the "Starterfeld" table of every season page.

    Two row forms: {{Starter|year|no|driver|make|team|car|tyres}} (draws "<driver> <year>.svg")
    and hand-written rows that link the drawing with [[Datei:...svg]]."""
    pages = json.loads((REPO / "reference" / "driver_careers" / "pages.json").read_text(encoding="utf-8"))
    out = {}
    for title, p in pages.items():
        if not p["text"].lstrip().startswith("{{Saison") or not re.fullmatch(r"\d{4}", title):
            continue
        w = p["text"]
        i = w.find("Starterfeld")
        seg = w[i:w.find("\n==", i + 15)] if i >= 0 else ""
        for line in seg.split("\n"):
            m = re.search(r"\{\{(Gast|Junior|Test)?(?:[Ss]tarter|fahrer)\|(\d{4})\|([^|]*)\|([^|]+)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|}]*)\}\}", line)
            if m:
                guest, year, no, driver, make, team, car, tyres = m.groups()
                key = norm(f"{driver}_{year}.svg".replace(" ", "_"))
                if key in out:   # a typo in the wiki table names a driver twice (2012: #9 'Timo Scheider')
                    continue     # the first row is the real one; the drawing of the other car gets a fix
                out[key] = {"number": no, "driver": driver, "make": make, "team": team,
                                                      "car": car, "tyres": tyres, "guest": {"Gast": "guest", "Test": "test driver", "Junior": "junior"}.get(guest or "", "")}
                continue
            f = re.search(r"\[\[Datei:([^|\]]+\.svg)", line)
            if not f or "{{Nr|" not in line:
                continue
            cells = [c.strip() for c in line.lstrip("|").split("||")]
            no = re.search(r"\{\{Nr\|([^}]*)\}\}", line).group(1)
            driver = re.sub(r"[{}]", "", cells[1]) if len(cells) > 1 else ""
            mk = re.search(r"\{\{([A-Za-zë\- ]+?) \d{4}\|", line)
            team_car = next((c for c in cells if "<br>" in c and "Datei:" not in c), "")
            team, _, car = team_car.partition("<br>")
            tyre = re.findall(r"\{\{(Dunlop|Pirelli|Michelin|Goodyear|Yokohama|Bridgestone|Hankook|Continental|Kumho)\}\}", line)
            out[norm(f.group(1).replace(" ", "_"))] = {"number": no, "driver": driver.strip(), "make": mk.group(1) if mk else "",
                                     "team": link_text(team).replace("&nbsp;", "").strip(), "car": link_text(car),
                                     "tyres": tyre[-1] if tyre else "", "guest": ""}
    return out


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Downloads"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.home() / "Pictures" / "mods" / "dtm_fandom_svgs"
    files = [f for f in json.loads(FILES.read_text(encoding="utf-8")) if f["mime"] == "image/svg+xml"]
    found = {norm(p.name): p for p in out.glob("*/*.svg")}  # already filed, maybe in the wrong folder
    found.update({norm(p.name): p for p in src.glob("*.svg")})
    for saved, wiki_name in RENAMED.items():
        p = found.pop(norm(saved), None)
        if p is not None:
            found[norm(wiki_name)] = p
    facts = entries()
    rows, missing, moved = [], [], 0
    for f in files:
        kind, year, sub = kind_of(f["name"])
        dest = out / sub / safe(f["name"])
        if not dest.exists():
            p = found.get(norm(f["name"]))
            if p is None:
                missing.append(f["url"])
                continue
            head = p.read_bytes()[:400].lower()
            if b"<svg" not in head and b"<?xml" not in head:
                missing.append(f["url"])  # a saved error page, not an SVG
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), dest)
            moved += 1
        fact = facts.get(norm(f["name"]), {}) if kind == "car" else {}
        rows.append({"file": f"{sub}/{dest.name}", "kind": kind, "year": year, **{k: fact.get(k, "") for k in FACTS}, "placeholder": "",
                     "uploader": f.get("user", ""),
                     "uploaded": f.get("timestamp", ""), "page": f"https://dtm.fandom.com/de/wiki/Datei:{f['name']}",
                     "license": "CC BY-SA (fandom default); credit the uploader and dtm.fandom.com"})
    fixes = list(csv.DictReader(open(FIXES, encoding="utf-8"))) if FIXES.exists() else []
    by_file = {r["file"]: r for r in rows}
    for fx in fixes:
        if fx["file"] in by_file:
            by_file[fx["file"]][fx["field"]] = fx["value"]
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "SOURCES.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, ["file", "kind", "year", *FACTS, "placeholder", "uploader", "uploaded", "page", "license"])
        w.writeheader()
        w.writerows(rows)
    (out / "MISSING.txt").write_text("\n".join(missing) + ("\n" if missing else ""), encoding="utf-8")
    print(f"moved {moved}, in place {len(rows)} of {len(files)}, missing {len(missing)} (see {out / 'MISSING.txt'})")


if __name__ == "__main__":
    main()
