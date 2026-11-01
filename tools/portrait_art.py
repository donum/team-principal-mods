"""Driver portraits (683x1024) from freely licensed photos on Wikimedia Commons.

For every driver in a season pack's data/drivers.json:

1. find the driver on Wikidata (a racing driver with that name), take the
   main image (P18) and the files in the driver's Commons category (P373);
2. keep only freely licensed files (public domain, CC0, CC BY, CC BY-SA);
3. prefer the photo taken closest to the season (DateTimeOriginal), so
   portraits look like the drivers did then;
4. crop around the detected face (OpenCV) to the game's portrait format.

Drivers without a usable photo get a drawn helmet card in team colours.
Each photo's author, licence and source page go to art/portraits.json and
into the pack's credits. Downloads are cached in build/portraits/.

Usage:
    python tools/portrait_art.py seasons/dtm-1991 [--only "Name"] [--refresh]
"""

import argparse
import io
import json
import math
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "build" / "portraits"
SIZE = (683, 1024)
UA = "team-principal-mods/0.1 (driver portraits; free-licence photos from Wikimedia Commons)"
FREE = re.compile(r"^(public domain|pd|cc0|cc by(-sa)?( \d\.\d)?( [a-z]{2})?|cc-by(-sa)?-\d\.\d)", re.I)
DRIVER_WORDS = ("racing driver", "racecar driver", "race car driver", "rennfahrer", "automobilrennfahrer",
                "pilote automobile", "pilota automobilistico", "motorsport", "racer")


def load_json(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def get(url, binary=False):
    for attempt in range(8):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90).read()
            time.sleep(0.6)
            return data if binary else json.loads(data)
        except urllib.error.HTTPError as err:
            if err.code not in (429, 503):
                raise
            time.sleep(15 * (attempt + 1))
    raise SystemExit(f"rate limited: {url}")


def wikidata_driver(name):
    q = urllib.parse.urlencode({"action": "wbsearchentities", "search": name, "language": "en", "limit": 8,
                                "type": "item", "format": "json"})
    hits = get("https://www.wikidata.org/w/api.php?" + q).get("search", [])
    for hit in hits:
        desc = (hit.get("description") or "").lower()
        if any(w in desc for w in DRIVER_WORDS):
            return hit["id"]
    return None


def claims(qid):
    q = urllib.parse.urlencode({"action": "wbgetentities", "ids": qid, "props": "claims", "format": "json"})
    c = get("https://www.wikidata.org/w/api.php?" + q)["entities"][qid]["claims"]
    val = lambda p: [x["mainsnak"]["datavalue"]["value"] for x in c.get(p, []) if "datavalue" in x["mainsnak"]]
    cats = val("P373")
    return val("P18"), (cats[0] if cats else None)


def commons_files(images, category):
    titles = ["File:" + t for t in images]
    if category:
        q = urllib.parse.urlencode({"action": "query", "list": "categorymembers", "cmtitle": "Category:" + category,
                                    "cmtype": "file", "cmlimit": 40, "format": "json"})
        titles += [m["title"] for m in get("https://commons.wikimedia.org/w/api.php?" + q)["query"]["categorymembers"]]
    titles = [t for t in dict.fromkeys(titles) if re.search(r"\.(jpe?g|png)$", t, re.I)][:40]
    files = []
    for i in range(0, len(titles), 20):
        q = urllib.parse.urlencode({"action": "query", "titles": "|".join(titles[i:i + 20]), "prop": "imageinfo",
                                    "iiprop": "url|extmetadata|size", "iiurlwidth": 1200, "format": "json"})
        for page in get("https://commons.wikimedia.org/w/api.php?" + q)["query"]["pages"].values():
            info = (page.get("imageinfo") or [{}])[0]
            meta = info.get("extmetadata", {})
            lic = re.sub(r"<[^>]+>", "", meta.get("LicenseShortName", {}).get("value", "")).strip()
            date = re.sub(r"<[^>]+>", "", meta.get("DateTimeOriginal", {}).get("value", ""))
            year = int(m.group(0)) if (m := re.search(r"(19|20)\d\d", date)) else None
            files.append({"title": page["title"], "thumb": info.get("thumburl"), "page": info.get("descriptionurl"),
                          "license": lic, "year": year, "main": page["title"] in titles[:len(images)],
                          "author": re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip()[:120]})
    return [f for f in files if f["thumb"] and FREE.match(f["license"])]


def face_crop(img):
    import cv2
    import numpy as np
    arr = np.array(img.convert("RGB"))
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = det.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(40, 40))
    if len(faces) == 0:
        return None
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    if w < 60:
        return None
    cw = w * 3.0
    ch = cw * SIZE[1] / SIZE[0]
    cx, cy = x + w / 2, y + h / 2
    left, top = cx - cw / 2, cy - ch * 0.36
    W, H = img.size
    # Keep inside the photo; shrink if the photo is too small around the face.
    scale = min(1.0, W / cw, H / ch)
    cw, ch = cw * scale, ch * scale
    left = min(max(0, cx - cw / 2), W - cw)
    top = min(max(0, cy - ch * 0.36), H - ch)
    if cw < 220:
        return None
    return img.crop((round(left), round(top), round(left + cw), round(top + ch))).resize(SIZE, Image.LANCZOS)


def helmet_card(name, number, colors):
    """Fallback: a stylised helmet in team colours on a dark card."""
    c1, c2 = tuple(colors[0]), tuple(colors[1])
    img = Image.new("RGB", SIZE, (32, 35, 40))
    d = ImageDraw.Draw(img)
    for y in range(SIZE[1]):
        f = y / SIZE[1]
        d.line([(0, y), (SIZE[0], y)], fill=tuple(int(32 + 30 * f) for _ in range(3)))
    cx, cy, r = SIZE[0] / 2, 470, 230
    d.ellipse([cx - r, cy - r, cx + r, cy + r * 1.05], fill=c1, outline=(15, 15, 15), width=10)
    d.rectangle([cx - r * 0.95, cy + r * 0.35, cx + r * 0.95, cy + r * 1.05], fill=(32, 35, 40))
    d.rounded_rectangle([cx - r * 0.95, cy + r * 0.25, cx + r * 0.95, cy + r * 0.62], radius=30, fill=c1, outline=(15, 15, 15), width=10)
    d.rounded_rectangle([cx - r * 0.78, cy - r * 0.15, cx + r * 0.62, cy + r * 0.22], radius=40, fill=(25, 30, 40), outline=(15, 15, 15), width=8)
    d.polygon([(cx - r * 0.9, cy - r * 0.55), (cx + r * 0.9, cy - r * 0.55), (cx + r * 0.75, cy - r * 0.38), (cx - r * 0.75, cy - r * 0.38)], fill=c2)
    from car_art import font
    if number:
        d.text((cx, cy - r * 0.75), str(number), font=font(110), anchor="mm", fill=c2, stroke_width=4, stroke_fill=(15, 15, 15))
    initials = "".join(p[0] for p in name.split()[:3] if p[0].isalpha()).upper()
    d.text((cx, 860), initials, font=font(120), anchor="mm", fill=(230, 230, 230))
    return img


def main():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("season", type=Path)
    ap.add_argument("--only")
    ap.add_argument("--refresh", action="store_true", help="ignore cached lookups")
    args = ap.parse_args()
    season = args.season.resolve()
    year = load_json(season / "season.json")["constants"]["SEASON_START_YEAR"]
    teams = {t["name"]: t for t in load_json(season / "data" / "teams.json")["records"]}
    drivers = load_json(season / "data" / "drivers.json")["records"]
    out_dir = season / "assets" / "portraits"
    out_dir.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    credits_path = season / "art" / "portraits.json"
    credits = load_json(credits_path) if credits_path.exists() else {}
    for d in drivers:
        name = d["name"]
        if args.only and name != args.only:
            continue
        team = teams.get(d.get("team") or d["contract"]["team"], {})
        number = d.get("number", d.get("reserve_number"))
        fname = name.replace(" ", "") + ".png"
        meta_path = CACHE / (fname + ".json")
        if meta_path.exists() and not args.refresh:
            files = load_json(meta_path)
        else:
            qid = wikidata_driver(name)
            files = commons_files(*claims(qid)) if qid else []
            meta_path.write_text(json.dumps(files, ensure_ascii=False), encoding="utf-8")
        # Closest to the season first; undated main images after dated ones.
        files.sort(key=lambda f: (abs((f["year"] or 2050) - year), not f["main"]))
        done = None
        for f in files[:8]:
            raw = CACHE / re.sub(r"[^\w.-]", "_", f["title"])
            if not raw.exists():
                raw.write_bytes(get(f["thumb"], binary=True))
            try:
                img = ImageOps.exif_transpose(Image.open(raw)).convert("RGB")
            except Exception:
                continue
            crop = face_crop(img)
            if crop:
                crop.save(out_dir / fname, optimize=True)
                done = {"source": "photo", "file": f["title"], "page": f["page"], "author": f["author"],
                        "license": f["license"], "year": f["year"]}
                break
        if not done:
            helmet_card(name, number, [team.get("color_rgb", [200, 200, 200]), team.get("secondary_color_rgb", [30, 30, 30])]).save(out_dir / fname, optimize=True)
            done = {"source": "helmet"}
        credits[name] = done
        print(f"{name:28s} {done['source']:6s} {done.get('year') or '':>5} {done.get('license', '')}")
    credits_path.write_text(json.dumps(credits, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    photos = sum(1 for v in credits.values() if v["source"] == "photo")
    print(f"\n{photos} photos, {len(credits) - photos} helmet cards -> {credits_path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
