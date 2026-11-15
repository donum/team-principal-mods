"""Fetch every article (wikitext) and the file list of dtm.fandom.com/de into a cache dir."""
import json, sys, time, urllib.request, urllib.parse
from pathlib import Path
API = "https://dtm.fandom.com/de/api.php"
UA = {"User-Agent": "Mozilla/5.0 (research script)"}
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
def get(**p):
    p.update(format="json", formatversion="2")
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(p), headers=UA)
    for i in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)
        except Exception as e:
            print("retry", e); time.sleep(5 * (i + 1))
    raise SystemExit("failed")
pages, cont = {}, {}
while True:
    d = get(action="query", generator="allpages", gapnamespace=0, gaplimit=50, gapfilterredir="nonredirects",
            prop="revisions|categories", rvprop="content", rvslots="main", cllimit="max", **cont)
    for p in d["query"]["pages"]:
        rev = p.get("revisions", [{}])[0].get("slots", {}).get("main", {}).get("content")
        if rev is None:
            continue  # content comes in a later continue batch
        pages[p["title"]] = {"text": rev, "cats": [c["title"] for c in p.get("categories", [])]}
    print(len(pages)); cont = d.get("continue", {})
    if not cont: break
    cont.pop("continue", None); time.sleep(1)
(out / "pages.json").write_text(json.dumps(pages, ensure_ascii=False), encoding="utf-8")
files, cont = [], {}
while True:
    d = get(action="query", list="allimages", ailimit=500, aiprop="url|size|mime|timestamp|user", **cont)
    files += d["query"]["allimages"]; cont = d.get("continue", {})
    if not cont: break
    cont.pop("continue", None); time.sleep(1)
(out / "files.json").write_text(json.dumps(files, ensure_ascii=False), encoding="utf-8")
print("pages", len(pages), "files", len(files))
