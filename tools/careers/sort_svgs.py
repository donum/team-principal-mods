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
FILES = REPO / "reference" / "driver_careers" / "files.json"


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
        rows.append({"file": f"{sub}/{dest.name}", "kind": kind, "year": year, "uploader": f.get("user", ""),
                     "uploaded": f.get("timestamp", ""), "page": f"https://dtm.fandom.com/de/wiki/Datei:{f['name']}",
                     "license": "CC BY-SA (fandom default); credit the uploader and dtm.fandom.com"})
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "SOURCES.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, ["file", "kind", "year", "uploader", "uploaded", "page", "license"])
        w.writeheader()
        w.writerows(rows)
    (out / "MISSING.txt").write_text("\n".join(missing) + ("\n" if missing else ""), encoding="utf-8")
    print(f"moved {moved}, in place {len(rows)} of {len(files)}, missing {len(missing)} (see {out / 'MISSING.txt'})")


if __name__ == "__main__":
    main()
