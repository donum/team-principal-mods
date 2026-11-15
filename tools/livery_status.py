"""Livery status page: which DTM/BTCC cars have a final livery drawing, which have only a
generated stand-in, and how much reference material (photos, TV frames) we have.

Reads, for every seasons/dtm-*/ and btcc-*/ in the repo:
  research/entries.csv        the cars (number, driver, entrant, car)
  art/drawings.json           FINAL: artist drawings (e.g. Pappydhorn12), per car
  assets/Cars/*.png           GENERATED: one image per team when there is no drawing
and from the picture store (default ~/Pictures/mods/<series>-<year>/):
  livery_pack/labels.csv      labelled reference images per car and view
  teams/**                    raw photos per team (not yet labelled); shown per car when the
                              file name gives '#NN' or names the driver first
and from the video store (default ~/Videos/yt/<SERIES>/<year>/): number of videos.

Writes one self-contained HTML page (default ~/Pictures/mods/livery_status.html).
tools/livery_pack.py calls this after every pack build, so the page stays current;
run it by hand after adding drawings or photos:

    python tools/livery_status.py [--pictures DIR] [--videos DIR] [--out FILE]
"""
import argparse, csv, datetime as dt, html, json, os, re, sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
IMG = {".jpg", ".jpeg", ".png", ".webp"}
VID = {".mkv", ".mp4", ".webm"}
SIDES = ("left", "right")
QRANK = {"A": 0, "B": 1, "C": 2}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def best(rows, views):
    q = [r["quality"] for r in rows if r["view"] in views]
    return min(q, key=lambda x: QRANK.get(x, 9)) if q else ""


def season(year_dir, pics, vids):
    series, y = year_dir.name.split("-")[0], year_dir.name.split("-")[1]
    ent = year_dir / "research" / "entries.csv"
    if not ent.exists():
        return None
    cars = [r for r in csv.DictReader(open(ent, encoding="utf-8")) if r.get("number", "").strip()]
    final, artist = {}, ""
    dj = year_dir / "art" / "drawings.json"
    if dj.exists():
        d = json.load(open(dj, encoding="utf-8"))
        artist = d.get("artist", "")
        for sheet, s in d.get("sheets", {}).items():
            for n in s.get("cars", []):
                final[str(n)] = sheet
    team_img = {norm(p.stem): p for p in (year_dir / "assets" / "Cars").glob("*.png")}
    gen = set(team_img) if not final else set()
    per_car = {}                                   # art/liveries/<Team>_<NN>.png: the other car of a sheet
    for p in (year_dir / "art" / "liveries").glob("*.png"):
        m = re.search(r"_(\d+)$", p.stem)
        if m:
            per_car[str(int(m.group(1)))] = p
    sheet_team = {}
    if dj.exists():
        for sheet, s in json.load(open(dj, encoding="utf-8")).get("sheets", {}).items():
            for n in s.get("cars", []):
                sheet_team[str(n)] = s.get("team", "")
    pdir = pics / year_dir.name
    labels = defaultdict(list)
    lab = pdir / "livery_pack" / "labels.csv"
    if lab.exists():
        for r in csv.DictReader(open(lab, encoding="utf-8")):
            labels[r["car"].strip()].append(r)
    raw = defaultdict(int)
    photos = defaultdict(list)                     # car -> raw photos naming it (not yet labelled)
    labelled = {(pdir / "teams" / r["source"][6:]).resolve() for rs in labels.values() for r in rs
                if r["source"].startswith("photo:")}
    if (pdir / "teams").exists():
        for f in sorted((pdir / "teams").rglob("*")):
            if f.suffix.lower() in IMG and "_not_suitable" not in f.parts:
                team_dir = f.relative_to(pdir / "teams").parts[0]
                raw[team_dir] += 1
                if f.resolve() not in labelled and not NOT_CAR.intersection(x.lower() for x in f.parts):
                    for n in photo_cars(f, team_dir, cars):
                        photos[n].append(f)
    vdir = vids / series.upper() / y
    nvid = sum(1 for f in vdir.rglob("*") if f.suffix.lower() in VID) if vdir.exists() else 0
    rows = []
    for c in cars:
        n = c["number"].strip()
        lr = labels.get(n, [])
        status = "final" if n in final else ("generated" if norm(c.get("entrant", "")) in gen else "none")
        if status == "final":
            img = per_car.get(n) or team_img.get(norm(sheet_team.get(n, "")))
        elif status == "generated":
            img = team_img.get(norm(c.get("entrant", "")))
        else:
            img = None
        refs = []                                  # best labelled image per view group
        for tag, views in (("L", ("left",)), ("R", ("right",)), ("F", ("front", "front-left", "front-right")),
                           ("B", ("rear", "rear-left", "rear-right"))):
            cand = sorted((r for r in lr if r["view"] in views), key=lambda r: QRANK.get(r["quality"], 9))
            if cand:
                r = cand[0]
                src = r["source"]
                p = (pdir / "teams" / src[6:]) if src.startswith("photo:") else (pdir / "livery_pack" / "_video_candidates" / src)
                if p.exists():
                    refs.append((tag, r["quality"], r["view"], p, r.get("note", "")))
        rows.append({"n": n, "driver": c.get("driver", ""), "team": c.get("entrant", ""), "car": c.get("car", ""),
                     "status": status, "sheet": final.get(n, ""), "img": img, "refs": refs,
                     "left": best(lr, ("left",)), "right": best(lr, ("right",)),
                     "front": best(lr, ("front", "front-left", "front-right")),
                     "rear": best(lr, ("rear", "rear-left", "rear-right")), "nref": len(lr),
                     "photos": photos.get(n, []),
                     "teamraw": raw.get(c.get("entrant", ""), 0)})
    return {"year": y, "key": year_dir.name, "label": f"{series.upper()} {y}", "rows": rows, "artist": artist, "raw": sum(raw.values()), "videos": nvid,
            "pack": (pdir / "livery_pack" / "README.md").exists(), "packdir": pdir / "livery_pack"}


NOT_CAR = {"historic", "other_years", "people", "portrait", "portrait_frame"}   # folders that are no livery reference
MAXPHOTOS = 16                                      # raw photos shown per car
THUMBS = None                                       # set in main(): <pictures>/_status_thumbs


def thumb(p, out, width=360):
    """Cached small JPEG of p next to the page; returns its relative URL ('' if unreadable)."""
    import hashlib
    import cv2
    import numpy as np
    key = hashlib.sha1(f"{p}|{p.stat().st_mtime_ns}|{width}".encode()).hexdigest()[:16]
    t = THUMBS / f"{key}.jpg"
    if not t.exists():
        im = cv2.imdecode(np.fromfile(str(p), np.uint8), cv2.IMREAD_COLOR)
        if im is None:
            return ""
        h, w = im.shape[:2]
        if w > width:
            im = cv2.resize(im, (width, int(h * width / w)), interpolation=cv2.INTER_AREA)
        THUMBS.mkdir(parents=True, exist_ok=True)
        cv2.imencode(".jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 82])[1].tofile(str(t))
    return os.path.relpath(t, out.parent).replace(os.sep, "/")


def photo_cars(f, team_dir, cars):
    """Car numbers a raw photo shows, from its file name: '#NN' or the first named driver
    (Getty/Alamy/STR names list the subject first). Team folder breaks ties between a
    driver's cars. Returns [] when no entry driver is named."""
    name = f.stem
    nums = {c["number"].strip() for c in cars}
    hit = [m for m in re.findall(r"#(\d+)\b", name) if m in nums]
    if hit:
        return [hit[0]]
    desc = name.split(" - ", 2)[-1] if name.count(" - ") >= 2 else name.split(" - ", 1)[-1]
    best_pos, cand = None, []
    for c in cars:
        last = c["driver"].split()[-1]
        m = re.search(r"\b" + re.escape(last) + r"\b", desc, re.I) or \
            (re.search(r"\b" + re.escape(last.split("'")[-1]) + r"\b", desc, re.I) if "'" in last else None)
        if not m:
            continue
        if best_pos is None or m.start() < best_pos:
            best_pos, cand = m.start(), [c]
        elif m.start() == best_pos:
            cand.append(c)
    if len({c["number"] for c in cand}) > 1:      # same driver in several cars (Matt Neal 1991)
        t = norm(team_dir)
        narrowed = [c for c in cand if norm(c.get("entrant", ""))[:6] in t or t[:6] in norm(c.get("entrant", ""))]
        cand = narrowed or cand
    out = []
    for c in cand:
        if c["number"].strip() not in out:
            out.append(c["number"].strip())
    return out if len(out) == 1 else []


def ready(r):
    """Enough to draw from: both sides at A/B."""
    return r["left"] in ("A", "B") and r["right"] in ("A", "B")


def page(seasons, out):
    e = html.escape
    tot = defaultdict(int)
    for s in seasons:
        for r in s["rows"]:
            tot["cars"] += 1
            tot[r["status"]] += 1
            tot["ready"] += r["status"] != "final" and ready(r)
    summary = []
    for s in seasons:
        rs = s["rows"]
        f = sum(r["status"] == "final" for r in rs)
        g = sum(r["status"] == "generated" for r in rs)
        rd = sum(r["status"] != "final" and ready(r) for r in rs)
        one = sum(r["status"] != "final" and not ready(r) and bool(r["left"] or r["right"]) for r in rs)
        pct = round(100 * f / len(rs)) if rs else 0
        summary.append(f"<tr><td><a href='#{s['key']}'>{s['label']}</a></td><td>{len(rs)}</td>"
                       f"<td class='num'>{f or ''}</td><td class='num'>{g or ''}</td><td class='num'>{rd or ''}</td>"
                       f"<td class='num'>{one or ''}</td><td class='num'>{s['raw'] or ''}</td><td class='num'>{s['videos'] or ''}</td>"
                       f"<td><div class='bar'><span style='width:{pct}%'></span></div></td></tr>")
    details = []
    for s in seasons:
        rs = s["rows"]
        if not rs:
            continue
        open_ = " open" if s["pack"] else ""
        body, shown = [], set()
        for r in sorted(rs, key=lambda r: (int(re.sub(r"\D", "", r["n"]) or 0), r["n"])):
            st = {"final": "Final drawing", "generated": "Generated", "none": "Missing"}[r["status"]]
            chips = "".join(f"<td class='q q{r[k] or 'x'}'>{r[k] or '·'}</td>" for k in ("left", "right", "front", "rear"))
            pics = []
            if r["img"] is not None and (u := thumb(r["img"], out, 480)):
                pics.append(f"<a class='lv' href='{e(r['img'].as_uri())}' target='_blank' title='{e(r['img'].name)}'>"
                            f"<img loading='lazy' src='{e(u)}' alt='livery #{e(r['n'])}'><i>{st}</i></a>")
            for tag, q, view, p, note in r["refs"]:
                if u := thumb(p, out):
                    pics.append(f"<a class='rf' href='{e(p.as_uri())}' target='_blank' title='{e(view)} · {e(note)} · {e(p.name)}'>"
                                f"<img loading='lazy' src='{e(u)}' alt='{e(view)}'><i class='q{q}'>{tag} {q}</i></a>")
            if r["n"] not in shown:                # raw photos once per car number, not per driver row
                shown.add(r["n"])
                for p in r["photos"][:MAXPHOTOS]:
                    if u := thumb(p, out):
                        pics.append(f"<a class='ph' href='{e(p.as_uri())}' target='_blank' title='{e(p.name)}'>"
                                    f"<img loading='lazy' src='{e(u)}' alt='photo'><i>Photo</i></a>")
                if len(r["photos"]) > MAXPHOTOS:
                    pics.append(f"<span class='more'>+{len(r['photos']) - MAXPHOTOS} more in teams/</span>")
            body.append(f"<tr><td class='num'>{e(r['n'])}</td><td>{e(r['driver'])}</td><td class='team'>{e(r['team'])}</td>"
                        f"<td class='team'>{e(r['car'])}</td><td><span class='st {r['status']}'>{st}</span></td>{chips}"
                        f"<td class='num'>{r['nref'] or ''}</td><td class='num'>{r['teamraw'] or ''}</td></tr>")
            if pics:
                body.append(f"<tr class='pics'><td></td><td colspan='10'><div class='strip'>{''.join(pics)}</div></td></tr>")
        link = f" · <a href='{e(os.path.relpath(s['packdir'], out.parent).replace(os.sep, '/'))}/README.md'>pack</a>" if s["pack"] else ""
        art = f" · drawings by {e(s['artist'])}" if s["artist"] else ""
        details.append(f"<details id='{s['key']}'{open_}><summary>{s['label']} <small>{len(rs)} cars{art}"
                       f" · {s['raw']} raw photos · {s['videos']} videos{link}</small></summary>"
                       "<table class='cars'><thead><tr><th>#</th><th>Driver</th><th>Team</th><th>Car</th><th>Livery</th>"
                       "<th>Left</th><th>Right</th><th>Front</th><th>Rear</th><th>Refs</th><th>Team photos</th></tr></thead>"
                       f"<tbody>{''.join(body)}</tbody></table></details>")
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Livery Status</title>
<style>
:root{{--bg:#fafaf9;--fg:#1c1c1a;--mute:#6b6b66;--line:#e4e4e0;--card:#fff;--final:#1f7a4d;--gen:#a56a00;--none:#b42318;
--qa:#1f7a4d;--qb:#4a8f2a;--qc:#a56a00;--acc:#2f5dab}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151514;--fg:#ececea;--mute:#9a9a94;--line:#2c2c2a;--card:#1d1d1b;
--final:#4cc38a;--gen:#e0a23a;--none:#f0705f;--qa:#4cc38a;--qb:#9bd06a;--qc:#e0a23a;--acc:#7ea6ff}}}}
:root[data-theme="dark"]{{--bg:#151514;--fg:#ececea;--mute:#9a9a94;--line:#2c2c2a;--card:#1d1d1b;--final:#4cc38a;--gen:#e0a23a;--none:#f0705f;--qa:#4cc38a;--qb:#9bd06a;--qc:#e0a23a;--acc:#7ea6ff}}
body{{background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;margin:0;padding:24px 16px 64px}}
main{{max-width:1180px;margin:0 auto}} h1{{font-size:22px;margin:0 0 4px}} .sub{{color:var(--mute);margin:0 0 20px}}
a{{color:var(--acc)}} .kpis{{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:24px}}
.kpi{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 14px;min-width:130px}}
.kpi b{{display:block;font-size:22px;font-variant-numeric:tabular-nums}} .kpi span{{color:var(--mute);font-size:12px}}
.wrap{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;background:var(--card)}}
th,td{{text-align:left;padding:5px 8px;border-bottom:1px solid var(--line);white-space:nowrap}}
th{{font-weight:600;color:var(--mute);font-size:12px}} td.num{{text-align:right;font-variant-numeric:tabular-nums}}
td.team{{color:var(--mute);max-width:260px;overflow:hidden;text-overflow:ellipsis}}
.bar{{width:120px;height:8px;background:var(--line);border-radius:4px}} .bar span{{display:block;height:100%;background:var(--final);border-radius:4px}}
details{{margin:10px 0;border:1px solid var(--line);border-radius:8px;background:var(--card)}}
summary{{cursor:pointer;padding:10px 12px;font-weight:600}} summary small{{font-weight:400;color:var(--mute);margin-left:8px}}
details table{{border-top:1px solid var(--line)}}
.st{{font-size:12px;padding:1px 7px;border-radius:10px;border:1px solid currentColor}}
.st.final{{color:var(--final)}} .st.generated{{color:var(--gen)}} .st.none{{color:var(--none)}}
td.q{{text-align:center;font-weight:600;width:44px}} .qA{{color:var(--qa)}} .qB{{color:var(--qb)}} .qC{{color:var(--qc)}} .qx{{color:var(--line)}}
.legend{{color:var(--mute);font-size:12px;margin:8px 0 20px}}
tr.pics td{{border-bottom:1px solid var(--line);padding:2px 8px 10px;white-space:normal}}
.strip{{display:flex;flex-wrap:wrap;gap:8px;align-items:flex-end}}
.strip a{{position:relative;display:block;border:1px solid var(--line);border-radius:6px;overflow:hidden;background:#000;line-height:0}}
.strip a:hover{{outline:2px solid var(--acc)}}
.strip img{{height:96px;width:auto;display:block}} .strip a.lv img{{height:120px}}
.strip i{{position:absolute;left:0;bottom:0;font:600 11px/1 system-ui,sans-serif;font-style:normal;padding:3px 6px;
background:rgba(0,0,0,.72);color:#fff;border-top-right-radius:6px}}
.strip .more{{color:var(--mute);font-size:12px;align-self:center}} .strip a.ph i{{color:#9cc4ff}}
.strip i.qA{{color:#6ee7a8}} .strip i.qB{{color:#c3e88d}} .strip i.qC{{color:#ffcb6b}}
</style></head><body><main>
<h1>DTM &amp; BTCC Livery Status</h1>
<p class="sub">Generated {now} from the mod repo, the picture store and the video store. Re-run <code>python tools/livery_status.py</code>; pack builds update it automatically.</p>
<div class="kpis">
<div class="kpi"><b>{tot['cars']}</b><span>cars (all seasons)</span></div>
<div class="kpi"><b style="color:var(--final)">{tot['final']}</b><span>final drawings</span></div>
<div class="kpi"><b style="color:var(--gen)">{tot['generated']}</b><span>generated stand-ins</span></div>
<div class="kpi"><b style="color:var(--qa)">{tot['ready']}</b><span>ready to draw (both sides A/B)</span></div>
<div class="kpi"><b style="color:var(--none)">{tot['none']}</b><span>no livery image</span></div>
</div>
<p class="legend"><b>Livery:</b> Final drawing = artist sheet in <code>art/drawings.json</code>; Generated = team image from adapted outlines
(<code>assets/Cars</code>); Missing = nothing in-game. <b>Left/Right/Front/Rear:</b> best labelled reference
(A draw from it, B usable, C colours only, · none); left/right = the car's own side. <b>Ready</b> = both sides at A or B.
<b>Photo</b> = real period photo from the picture store (<code>teams/</code>), matched to the car by the name or number in its
file name and not yet labelled. Reference only: most need permission before any use.</p>
<div class="wrap"><table><thead><tr><th>Season</th><th>Cars</th><th>Final</th><th>Generated</th><th>Ready to draw</th>
<th>One side only</th><th>Raw photos</th><th>Videos</th><th>Final share</th></tr></thead><tbody>{''.join(summary)}</tbody></table></div>
<h2 style="font-size:17px;margin:28px 0 8px">Per car</h2>
<div class="wrap">{''.join(details)}</div>
</main></body></html>"""
    out.write_text(doc, encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pictures", type=Path, default=Path.home() / "Pictures" / "mods")
    ap.add_argument("--videos", type=Path, default=Path.home() / "Videos" / "yt")
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args(argv)
    out = a.out or a.pictures / "livery_status.html"
    global THUMBS
    THUMBS = out.parent / "_status_thumbs"
    seasons = [s for d in sorted((REPO / "seasons").glob("dtm-*")) + sorted((REPO / "seasons").glob("btcc-*")) if (s := season(d, a.pictures, a.videos))]
    page(seasons, out)
    print("status page:", out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
