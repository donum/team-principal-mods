"""Fetch the en and de Wikipedia DTM season pages (1984-2026) into <cache>/wiki_<lang>.json.

Asks for many titles per request (de.wikipedia answers 429 to one request per page)."""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "dtm-history-research/0.1 (personal modding research)"}
YEARS = [y for y in range(1984, 2027) if not 1997 <= y <= 1999]


def titles(lang, y):
    if lang == "en":
        if y <= 1985:
            return [f"{y} Deutsche Produktionswagen Meisterschaft", f"{y} Deutsche Tourenwagen Meisterschaft"]
        if y <= 1995:
            return [f"{y} Deutsche Tourenwagen Meisterschaft"]
        if y == 1996:
            return ["1996 International Touring Car Championship"]
        return [f"{y} Deutsche Tourenwagen Masters"]
    return [f"DTM-Saison {y}"]  # de.wikipedia redirects every season to its real title


def get(lang, params):
    params.update(format="json", formatversion="2")
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for i in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            print("retry", lang, e)
            time.sleep(10 * (i + 1))
    raise SystemExit(f"{lang}.wikipedia did not answer")


def main():
    out = Path(sys.argv[1])
    for lang in ("en", "de"):
        wanted = [t for y in YEARS for t in titles(lang, y)]
        pages, redirects = {}, {}
        for i in range(0, len(wanted), 20):
            d = get(lang, {"action": "query", "titles": "|".join(wanted[i:i + 20]), "redirects": 1,
                           "prop": "revisions", "rvprop": "content", "rvslots": "main"})
            for r in d["query"].get("redirects", []):
                redirects[r["to"]] = r["from"]
            for p in d["query"]["pages"]:
                if "revisions" in p:
                    pages[p["title"]] = p["revisions"][0]["slots"]["main"]["content"]
            time.sleep(3)
        res = {}
        for title, text in pages.items():
            asked = redirects.get(title, title)
            m = re.search(r"(19|20)\d\d", asked)
            if m and m.group() not in res:
                res[m.group()] = {"title": title, "text": text}
        missing = [y for y in YEARS if str(y) not in res]
        print(lang, len(res), "seasons", "missing:", missing)
        (out / f"wiki_{lang}.json").write_text(json.dumps(res, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
