"""Assemble a livery reference pack (raw material for a livery artist) for one season.

Inputs, all under <Pictures>/mods/dtm-<year>/livery_pack/:
  labels.csv   one row per kept image:
               source   path of a video candidate (relative to _video_candidates/)
                        or of a photo (relative to <Pictures>/mods/dtm-<year>/teams/)
               car      car number
               view     left | right | front | rear | front-left | front-right |
                        rear-left | rear-right | top | detail
                        (left/right = the car's own side: nose pointing right in
                        the image shows its LEFT side)
               quality  A (draw from it) | B (usable) | C (only for colours)
               note     free text: what it shows, sponsors read, doubts
  liveries.csv per car: number, driver, team, base_colors, main_sponsor,
               layout_notes (same columns as seasons/*/research/liveries.csv)

Output: one folder per car, "NN Driver - Team/", with the kept images copied and
renamed <quality>_<view>_<source>.jpg, a livery.md per car and a README.md with
the coverage table (which cars still miss a side). Video frames get their
broadcast timestamp in the name so they can be re-grabbed.

    python tools/livery_pack.py 2018 [--pictures C:/Users/dan/Pictures/mods]
"""
import argparse, csv, re, shutil, sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VIEWS = ["left", "right", "front-left", "front-right", "rear-left", "rear-right", "front", "rear", "top", "detail"]


def slug(s):
    return re.sub(r'[<>:"/\\|?*]', "_", s).strip(" .")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("year")
    ap.add_argument("--pictures", type=Path, default=Path.home() / "Pictures" / "mods")
    a = ap.parse_args()
    root = a.pictures / f"dtm-{a.year}"
    pack = root / "livery_pack"
    cand = pack / "_video_candidates"
    entries = {r["number"]: r for r in csv.DictReader(open(REPO / f"seasons/dtm-{a.year}/research/entries.csv", encoding="utf-8"))}
    liv = {}
    if (pack / "liveries.csv").exists():
        liv = {r["number"]: r for r in csv.DictReader(open(pack / "liveries.csv", encoding="utf-8"))}
    labels = list(csv.DictReader(open(pack / "labels.csv", encoding="utf-8")))

    # credits of photos (permission status travels with the file)
    credit = {}
    for c in (root / "teams").rglob("CREDITS_*.csv"):
        for r in csv.DictReader(open(c, encoding="utf-8-sig")):
            credit[(c.parent / r["file"]).resolve()] = r

    by_car = defaultdict(list)
    for r in labels:
        by_car[r["car"]].append(r)

    def folder(num):
        e = entries.get(num, {})
        return pack / slug(f"{int(num):02d} {e.get('driver', '?')} - {e.get('entrant', '?')}")

    for d in pack.iterdir():                    # rebuild car folders from scratch
        if d.is_dir() and re.match(r"\d\d ", d.name):
            shutil.rmtree(d)

    cover = {}
    for num in sorted(entries, key=int):
        rows = by_car.get(num, [])
        dst = folder(num)
        dst.mkdir(parents=True, exist_ok=True)
        lines, have = [], defaultdict(list)
        for r in sorted(rows, key=lambda r: (r["quality"], VIEWS.index(r["view"]) if r["view"] in VIEWS else 99)):
            src = r["source"]
            if src.startswith("photo:"):
                p = (root / "teams" / src[6:]).resolve()
                tag = "photo_" + p.stem
                cr = credit.get(p, {})
                rights = f"{cr.get('author', '?')}, {cr.get('license', 'unknown rights')}"
            else:
                p = (cand / src).resolve()
                vid = Path((cand / Path(src).parent / "source.txt").read_text(encoding="utf-8").strip()).stem
                ev = re.sub(r"\s*\(Multicam\).*|^\d+ - ", "", vid)
                tag = f"tv_{slug(ev)}_{p.stem.replace('_crop', '')}"
                rights = "TV broadcast frame (DTM / ITR), private reference only"
            if not p.exists():
                print("missing:", p)
                continue
            name = f"{r['quality']}_{r['view']}_{tag}{p.suffix}"
            shutil.copy2(p, dst / name)
            have[r["view"]].append(r["quality"])
            lines.append(f"| {r['quality']} | {r['view']} | `{name}` | {r.get('note', '')} | {rights} |")
        e, l = entries.get(num, {}), liv.get(num, {})
        md = [f"# #{num} {e.get('driver', '')} ({e.get('entrant', '')}, {e.get('car', '')}) - DTM {a.year}", ""]
        if l:
            md += [f"- **Base colours:** {l.get('base_colors', '')}", f"- **Main sponsor:** {l.get('main_sponsor', '')}",
                   f"- **Layout:** {l.get('layout_notes', '')}", ""]
        md += ["| Q | View | File | What it shows | Rights |", "|---|---|---|---|---|"] + (lines or ["| | | nothing yet | | |"])
        (dst / "livery.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        cover[num] = have

    def cell(h, v):
        q = sorted(h.get(v, []))
        return q[0] if q else "-"
    md = [f"# DTM {a.year} livery reference pack", "",
          "Raw material for side-view livery drawings in the style of the DTM 2012/2013 sheets.",
          "One folder per car. File names: `<quality>_<view>_<source>`; quality A = draw from it,",
          "B = usable, C = colours only. left/right = the car's own side.", "",
          "| # | Driver | Team | left | right | front¾ | rear¾ | front | rear |", "|---|---|---|---|---|---|---|---|---|"]
    for num in sorted(entries, key=int):
        h, e = cover[num], entries[num]
        fq = min([q for q in (cell(h, "front-left"), cell(h, "front-right")) if q != "-"] or ["-"])
        rq = min([q for q in (cell(h, "rear-left"), cell(h, "rear-right")) if q != "-"] or ["-"])
        md.append(f"| {num} | {e['driver']} | {e['entrant']} | {cell(h, 'left')} | {cell(h, 'right')} | {fq} | {rq} | {cell(h, 'front')} | {cell(h, 'rear')} |")
    (pack / "README.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("pack written:", pack)
    sys.path.insert(0, str(Path(__file__).parent))
    import livery_status                        # keep the status page current
    livery_status.main(["--pictures", str(a.pictures)])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
