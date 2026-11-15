"""DTM driver careers: one race database for every DTM and ITC season, and the
career history (`history` in drivers.json) for any pack built from it.

Sources (raw pages cached in reference/driver_careers/, gitignored):
  * dtm.fandom.com/de season pages: every driver's result in every race,
    1984-2015 and 2018-2022, with make and guest flag.
  * en.wikipedia season pages: drivers' standings per race, bold = pole,
    italic = fastest lap (1994, 1996, 2000-2026).
  * de.wikipedia season pages: pole sitter and winner per race (1984-2026).

Results come from en.wikipedia where it has a standings table and from the
fandom wiki for the other seasons (1984-1993, 1995). The other source is a
cross-check (docs/drivers/CHECKS.md).

Usage:
  python -I tools/driver_careers.py fetch            # refresh the cache
  python -I tools/driver_careers.py build            # write docs/drivers/*.csv
  python -I tools/driver_careers.py apply seasons/dtm-2013 [more packs]
  python -I tools/driver_careers.py history 2013 "Mike Rockenfeller"

`apply` writes `history` (seasons, championships, wins, podiums, poles,
starts, points: everything before the pack's year) into every driver record
of data/drivers.json and adds retired race winners and champions as
`retired: true` records, like the F1 Workshop packs do.
"""

import argparse
import collections
import csv
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent / "careers"))
import fandom  # noqa: E402
import wiki  # noqa: E402

CACHE = REPO / "reference" / "driver_careers"
OUT = REPO / "docs" / "drivers"
NO_START = {"DNS", "DNA", "DNQ", "DNP", "INJ", "WD", "C", "CANCELLED", "?", "UNPARSED", "DNPQ", "NQ", "DNAQ", "EX(DNS)"}
NATIONALITY = {"GER": "german", "GDR": "german", "FRG": "german", "DEU": "german", "FRA": "french", "DEN": "danish",
               "DNK": "danish", "AUT": "austrian", "SUI": "swiss", "CHE": "swiss", "ITA": "italian", "GBR": "british",
               "VEN": "venezuelan", "BEL": "belgian", "SWE": "swedish", "TCH": "czech", "CZE": "czech",
               "FIN": "finnish", "AUS": "australian", "NED": "dutch", "NLD": "dutch", "CAN": "canadian",
               "USA": "american", "JPN": "japanese", "ESP": "spanish", "POR": "portuguese", "PRT": "portuguese",
               "BRA": "brazilian", "NOR": "norwegian", "POL": "polish", "RUS": "russian", "ZAF": "south_african",
               "RSA": "south_african", "NZL": "new_zealander", "ARG": "argentine", "MEX": "mexican",
               "IRL": "irish", "HUN": "hungarian", "GRE": "greek", "LUX": "luxembourgish", "TUR": "turkish",
               "CHN": "chinese", "IND": "indian", "COL": "colombian", "THA": "thai", "MON": "monegasque",
               "MCO": "monegasque", "EST": "estonian", "HKG": "chinese", "UKR": "ukrainian"}
GERMAN_COUNTRY = {"Deutschland": "german", "Österreich": "austrian", "Schweiz": "swiss", "Dänemark": "danish",
                  "Schweden": "swedish", "Italien": "italian", "Frankreich": "french", "Großbritannien": "british",
                  "Vereinigtes Königreich": "british", "England": "british", "Schottland": "british",
                  "Belgien": "belgian", "Niederlande": "dutch", "Finnland": "finnish", "Kanada": "canadian",
                  "Brasilien": "brazilian", "Spanien": "spanish", "Portugal": "portuguese", "Venezuela": "venezuelan",
                  "Japan": "japanese", "Australien": "australian", "Norwegen": "norwegian", "USA": "american",
                  "Vereinigte Staaten": "american", "Südafrika": "south_african", "Neuseeland": "new_zealander",
                  "Polen": "polish", "Russland": "russian", "Tschechien": "czech", "Ungarn": "hungarian",
                  "Argentinien": "argentine", "Mexiko": "mexican", "Monaco": "monegasque", "Irland": "irish",
                  "Griechenland": "greek", "Kolumbien": "colombian", "Luxemburg": "luxembourgish"}


def read_csv(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(p, rows, fields=None):
    p.parent.mkdir(parents=True, exist_ok=True)
    fields = fields or list(rows[0])
    with open(p, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def key(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]", "", s)


# ---------------------------------------------------------------- names

def alias_map():
    """alias key -> canonical name, from docs/drivers/aliases.csv."""
    p = OUT / "aliases.csv"
    return {key(r["alias"]): r["driver"] for r in read_csv(p)} if p.exists() else {}


class Names:
    """Canonical driver names: the fandom wiki page name, else the first spelling seen."""

    def __init__(self, fandom_names):
        self.aliases = alias_map()
        self.by_key = {}
        for n in fandom_names:
            self.by_key.setdefault(key(n), n)

    def canon(self, name):
        k = key(name)
        if k in self.aliases:
            return self.aliases[k]
        return self.by_key.setdefault(k, name)


# ---------------------------------------------------------------- build

def fandom_rows(pages):
    rows = []
    for title, p in sorted(pages.items()):
        if not p["text"].lstrip().startswith("{{Saison") or "Trophy" in title:
            continue
        if title == "1995":
            r1, _ = fandom.parse_season(title, p["text"], r"Fahrerwertung \(DTM\)", "DTM")
            r2, _ = fandom.parse_season(title, p["text"], r"Fahrerwertung \(ITC\)", "ITC")
            got = r1 + r2
        else:
            got, _ = fandom.parse_season(title, p["text"])
        rows += [r for r in got if "error" not in r]
    return [{k: str(v) for k, v in r.items()} for r in rows]


def infobox(text, field):
    m = re.search(r"\|\s*" + re.escape(field) + r"\s*=\s*([^\n]*)", text)
    return m.group(1).strip() if m else ""


def repo_bios():
    """canonical-key -> (birth_year, nationality) from every seasons/*/research/entries.csv."""
    out = {}
    for f in sorted(REPO.glob("seasons/*/research/entries.csv")):
        if not f.parent.parent.name.startswith(("dtm-", "itc-")):
            continue
        for e in read_csv(f):
            name = re.sub(r"\s*\(.*?\)", "", e.get("driver", "")).strip()
            if not name:
                continue
            by = (e.get("birth_date") or "")[:4]
            nat = (e.get("nationality") or "").strip()
            nat = NATIONALITY.get(nat.upper(), nat if nat.islower() else "")
            old = out.get(key(name), ("", ""))
            out[key(name)] = (old[0] or (by if by.isdigit() else ""), old[1] or nat)
    return out


def de_race_map(year, summ, rows, names):
    """(series, round, heat) -> pole sitter / winner, from the de.wikipedia race list.

    Its label starts with the round number ("3 / Lauf 2 / ..."); 1995 numbers DTM
    and ITC rounds together and sets the ITC rounds in bold, so 1995 is matched
    in order within each series."""
    parsed = []
    for s in summ:
        parts = [p.strip() for p in s["label"].split(" / ")]
        bold = "'''" in parts[0]
        rnd = re.sub(r"\D", "", parts[0])
        lauf = re.search(r"Lauf\s*(\d)", parts[1]) if len(parts) > 1 else None
        if not rnd:
            continue
        parsed.append(("ITC" if bold else "DTM", int(rnd), int(lauf.group(1)) if lauf else 1, s))
    fan = {}
    for r in rows:
        if r["kind"] == "race":
            fan.setdefault(r["series"], set()).add((int(r["round"]), int(r["heat"] or 1)))
    pole_at, win_at = {}, {}
    if year == "1995":
        for ser in ("DTM", "ITC"):
            mine = [p for p in parsed if p[0] == ser]
            order = sorted(fan.get(ser, ()))
            if len(mine) != len(order):
                continue
            for (rd, h), (_, _, _, s) in zip(order, mine):
                if s["pole"]:
                    pole_at[(ser, rd, h)] = names.canon(s["pole"])
                win_at[(ser, rd, h)] = names.canon(s["winner"])
        return pole_at, win_at
    have = fan.get("DTM", set())
    for ser, rd, h, s in parsed:
        if (rd, h) not in have:
            continue
        if s["pole"]:
            pole_at[("DTM", rd, h)] = names.canon(s["pole"])
        win_at[("DTM", rd, h)] = names.canon(s["winner"])
    return pole_at, win_at


# Non-championship rounds that the wiki tables list next to the real ones
# (de.wikipedia and the repo calendars agree they did not count).
NON_CHAMPIONSHIP = {"1993": {"DON"}, "1994": {"MUG", "DON"}, "2004": {"SHA"}, "2011": {"OLY"}, "2012": {"OLY"},
                    "2019": {"FUJ"}}
# (season, round, heat) of races that were run but annulled (no result, no points).
ANNULLED = {("1995", "2", "2")}


def build(args):
    pages = json.loads((CACHE / "pages.json").read_text(encoding="utf-8"))
    en = json.loads((CACHE / "wiki_en.json").read_text(encoding="utf-8"))
    de = json.loads((CACHE / "wiki_de.json").read_text(encoding="utf-8"))
    fan = fandom_rows(pages)
    driver_pages = {t: p["text"] for t, p in pages.items() if p["text"].lstrip().startswith("{{Infobox Fahrer")}
    names = Names(list(driver_pages) + sorted({r["driver"] for r in fan}))

    en_rows = {}
    for y, p in en.items():
        got = [r for r in wiki.standings(y, p["text"]) if "error" not in r and r.get("driver")]
        if got:
            en_rows[y] = got
    summaries = {}
    for y, p in de.items():
        s = [r for r in wiki.summary(y, p["text"]) if r["winner"] not in ("Sieger", "") and "Runde" not in r["label"]]
        if s:
            summaries[y] = s
    for y, p in en.items():
        if y not in summaries:
            s = wiki.summary(y, p["text"])
            if s:
                summaries[y] = s

    fan_by = collections.defaultdict(list)
    for r in fan:
        r["driver"] = names.canon(r["driver"])
        fan_by[r["season"]].append(r)
    make_of = {(r["season"], r["driver"]): r["make"] for r in fan if r["make"]}
    guest_of = {(r["season"], r["driver"]) for r in fan if r["guest"] == "1"}

    races, checks = [], []
    seasons = sorted(set(fan_by) | set(en_rows))
    for y in seasons:
        if y in en_rows:
            src = "en.wikipedia"
            qr_heat = y in ("2001", "2002")
            for r in en_rows[y]:
                d = names.canon(r["driver"])
                kind = "qr" if qr_heat and str(r["heat"]) == "1" else "race"
                status = r["status"].replace("RET", "DNF")
                races.append({"season": y, "series": "ITC" if y == "1996" else "DTM", "round": r["round"],
                              "heat": r["heat"], "kind": kind, "event": r["code"], "driver": d,
                              "make": make_of.get((y, d), ""), "pos": r["pos"], "status": status,
                              "pole": r["pole"], "fastest_lap": r["fastest_lap"],
                              "guest": int((y, d) in guest_of), "season_pos": r["season_pos"], "source": src})
        else:
            src = "dtm.fandom.com"
            rows = fan_by[y]
            # poles from the de.wikipedia race list, matched by round and heat
            summ = summaries.get(y, [])
            pole_at, win_at = de_race_map(y, summ, rows, names)
            if summ and not pole_at:
                checks.append(f"- {y}: could not match the de.wikipedia race list to the fandom table; "
                              f"poles are counted per season only.")
            for r in rows:
                rd, h = int(r["round"]), int(r["heat"] or 1)
                races.append({"season": y, "series": r["series"], "round": r["round"], "heat": r["heat"],
                              "kind": r["kind"], "event": r["code"], "driver": r["driver"], "make": r["make"],
                              "pos": r["pos"], "status": r["status"].replace("dropped", ""),
                              "pole": int(pole_at.get((r["series"], rd, h)) == r["driver"]),
                              "fastest_lap": "", "guest": r["guest"], "season_pos": r["season_pos"], "source": src})
            if summ and not pole_at:
                for s in summ:
                    if s["pole"]:
                        checks.append(f"  - {y} pole: {names.canon(s['pole'])}")
            for (ser, rd, h), w in win_at.items():
                got = {r["driver"] for r in rows if r["series"] == ser and int(r["round"]) == rd
                       and int(r["heat"] or 1) == h and r["pos"] == "1"}
                if got and w not in got:
                    checks.append(f"- {y} {ser} round {rd} heat {h}: fandom winner {', '.join(sorted(got))}, "
                                  f"de.wikipedia {w}")
    for r in races:
        r["started"] = int(r["status"] not in NO_START)
        if re.sub(r"\d+$", "", r["event"]) in NON_CHAMPIONSHIP.get(r["season"], ()):
            r["kind"] = "nc"
        if (r["season"], str(r["round"]), str(r["heat"])) in ANNULLED:
            r["kind"] = "annulled"

    # ---- per driver-season table
    seasons_tbl = collections.OrderedDict()
    pole_extra = collections.Counter()
    for line in checks:
        m = re.match(r"  - (\d{4}) pole: (.+)$", line)
        if m:
            pole_extra[(m.group(1), m.group(2))] += 1
    checks = [c for c in checks if not c.startswith("  - ")]
    for r in races:
        k = (r["driver"], r["season"], r["series"])
        s = seasons_tbl.setdefault(k, {"driver": r["driver"], "season": r["season"], "series": r["series"],
                                       "make": r["make"], "starts": 0, "wins": 0, "podiums": 0, "poles": 0,
                                       "fastest_laps": 0, "position": r["season_pos"], "points": "",
                                       "champion": 0, "guest": r["guest"], "source": r["source"]})
        if r["kind"] != "race" or not r["started"]:
            if r["kind"] == "qr" and r["pole"]:
                s["poles"] += 1
            continue
        s["starts"] += 1
        s["wins"] += r["pos"] == "1"
        s["podiums"] += r["pos"] in ("1", "2", "3")
        s["poles"] += int(r["pole"] or 0)
        s["fastest_laps"] += int(r["fastest_lap"] or 0)
    for (y, d), n in pole_extra.items():
        for k, s in seasons_tbl.items():
            if k[0] == d and k[1] == y and k[2] == "DTM":
                s["poles"] = n
    # points and position from the fandom tables / repo standings
    pts = {}
    for r in fan:
        pts.setdefault((r["driver"], r["season"], r["series"]), (r["season_points"], r["season_pos"]))
    for f in sorted(REPO.glob("seasons/dtm-*/research/standings.csv")) + sorted(REPO.glob("seasons/itc-*/research/standings.csv")):
        y = f.parent.parent.name[-4:]
        series = "ITC" if f.parent.parent.name.startswith("itc") else "DTM"
        for e in read_csv(f):
            if e.get("championship") and e["championship"] not in ("DTM", "ITC"):
                continue
            ser = e.get("championship") or series
            d = names.canon(re.sub(r"\s*\(.*?\)", "", e["driver"]).strip())
            pts[(d, y, ser)] = (e.get("points", ""), e.get("pos", ""))
    for k, s in seasons_tbl.items():
        p, pos = pts.get(k, ("", ""))
        s["points"] = re.sub(r"[^\d.,]", "", p).replace(",", ".") if p else ""
        s["position"] = s["position"] or (pos if str(pos).isdigit() else "")
        s["champion"] = int(s["position"] == "1")

    # ---- cross-checks: winners per race against the race lists
    for y in sorted(en_rows):
        summ = [s for s in summaries.get(y, []) if "Q.-Lauf" not in s["label"]
                and not any(c in s["label"] for c in ("Olympiastadion", "Shanghai", "Fuji", "Gold-Cup", "Gold Cup"))]
        mine = collections.Counter(r["driver"] for r in races if r["season"] == y and r["kind"] == "race"
                                   and r["pos"] == "1" and r["series"] == ("ITC" if y == "1996" else "DTM"))
        theirs = collections.Counter(names.canon(s["winner"]) for s in summ if s["winner"])
        if summ and mine != theirs:
            diff = sorted(set(mine) | set(theirs))
            d = [f"{n} {mine[n]} vs {theirs[n]}" for n in diff if mine[n] != theirs[n]]
            checks.append(f"- {y}: wins differ from the Wikipedia race list (database vs list): " + "; ".join(d))
    # fandom vs en totals where both exist
    nc = lambda y, code: re.sub(r"\d+$", "", code) in NON_CHAMPIONSHIP.get(y, ())  # noqa: E731
    for y in sorted(set(fan_by) & set(en_rows)):
        a = collections.Counter(r["driver"] for r in fan_by[y] if r["kind"] == "race" and r["pos"] == "1"
                                and not nc(y, r["code"]))
        b = collections.Counter(names.canon(r["driver"]) for r in en_rows[y] if r["pos"] == "1"
                                and not (y in ("2001", "2002") and str(r["heat"]) == "1") and not nc(y, r["code"]))
        if a != b:
            d = [f"{n} {a[n]} vs {b[n]}" for n in sorted(set(a) | set(b)) if a[n] != b[n]]
            checks.append(f"- {y}: wins fandom vs en.wikipedia: " + "; ".join(d))
    en_only = sorted({(r["season"], r["driver"]) for r in races if r["source"] == "en.wikipedia"
                      and r["kind"] != "nc" and r["season"] in fan_by and (r["season"], r["driver"]) not in
                      {(x["season"], x["driver"]) for x in fan}})
    if en_only:
        checks.append("- Names in en.wikipedia that the fandom table of the same season does not have "
                      "(add to aliases.csv if they are the same person): "
                      + ", ".join(f"{d} ({y})" for y, d in en_only))

    # ---- per driver
    bios = repo_bios()
    drivers = {}
    for s in seasons_tbl.values():
        d = drivers.setdefault(s["driver"], collections.Counter())
        for f in ("starts", "wins", "podiums", "poles", "fastest_laps", "champion"):
            d[f] += int(s[f] or 0)
    first_last = collections.defaultdict(list)
    for s in seasons_tbl.values():
        if s["starts"]:
            first_last[s["driver"]].append(int(s["season"]))
    drow = []
    for n, c in sorted(drivers.items(), key=lambda x: (-x[1]["wins"], -x[1]["starts"], x[0])):
        page = driver_pages.get(n, "")
        by, nat = bios.get(key(n), ("", ""))
        if not by and page:
            by = infobox(page, "Geburtsjahr")
        if not nat and page:
            nat = GERMAN_COUNTRY.get(infobox(page, "Nation"), "")
        yrs = sorted(set(first_last.get(n, [])))
        drow.append({"driver": n, "birth_year": by, "nationality": nat,
                     "first_season": yrs[0] if yrs else "", "last_season": yrs[-1] if yrs else "",
                     "seasons": len(yrs), "titles": c["champion"], "starts": c["starts"], "wins": c["wins"],
                     "podiums": c["podiums"], "poles": c["poles"], "fastest_laps": c["fastest_laps"],
                     "fandom_starts": infobox(page, "Rennen").replace(".", ""),
                     "fandom_wins": infobox(page, "Siege"), "fandom_poles": infobox(page, "Poles"),
                     "fandom_page": n if page else ""})

    write_csv(OUT / "dtm_races.csv", races, ["season", "series", "round", "heat", "kind", "event", "driver", "make",
                                              "pos", "status", "started", "pole", "fastest_lap", "guest", "source"])
    write_csv(OUT / "dtm_driver_seasons.csv", list(seasons_tbl.values()))
    write_csv(OUT / "dtm_drivers.csv", drow)
    big = [d for d in drow if d["fandom_wins"].isdigit() and d["fandom_starts"].isdigit() and d["last_season"]
           and int(d["last_season"]) <= 2022 and (abs(int(d["fandom_wins"]) - d["wins"]) > 0)]
    if big:
        checks.append("- Career wins that differ from the fandom career box (database vs box): "
                      + "; ".join(f"{d['driver']} {d['wins']} vs {d['fandom_wins']}" for d in big))
    (OUT / "CHECKS.md").write_text(
        "# Driver careers: source checks\n\nWritten by `python -I tools/driver_careers.py build`. "
        "Each line is a place where two sources disagree. Fix the source data or add a name to "
        "aliases.csv, then rebuild.\n\n" + "\n".join(checks) + "\n", encoding="utf-8")
    print(f"{len(races)} race rows, {len(seasons_tbl)} driver-seasons, {len(drow)} drivers, {len(checks)} check lines")


# ---------------------------------------------------------------- history

def load_db():
    seasons = read_csv(OUT / "dtm_driver_seasons.csv")
    drivers = {d["driver"]: d for d in read_csv(OUT / "dtm_drivers.csv")}
    return seasons, drivers


def history_before(seasons, year, series=("DTM", "ITC")):
    """driver -> history dict over every season before `year`."""
    out = collections.defaultdict(lambda: {"seasons": 0, "championships": 0, "wins": 0, "podiums": 0, "poles": 0,
                                           "starts": 0, "points": 0.0})
    years = collections.defaultdict(set)
    for s in seasons:
        if int(s["season"]) >= year or s["series"] not in series:
            continue
        h = out[s["driver"]]
        for f in ("wins", "podiums", "poles", "starts"):
            h[f] += int(s[f] or 0)
        h["points"] += float(s["points"] or 0)
        if int(s["starts"] or 0):
            years[s["driver"]].add(s["season"])
        if s["champion"] == "1":
            years[s["driver"] + "\0title"].add(s["season"])
    for d, h in out.items():
        h["seasons"] = len(years[d])
        h["championships"] = len(years[d + "\0title"])
        h["points"] = int(round(h["points"]))  # the game keeps whole points (int() on load)
    return out


def pack_year(pack):
    for f in ("gen.json", "season.json"):
        p = pack / f
        if p.exists():
            d = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(d.get("year"), int):
                return d["year"]
    m = re.search(r"(\d{4})$", pack.name)
    return int(m.group(1))


def apply_pack(pack, seasons, drivers, retired=True):
    year = pack_year(pack)
    names = Names(list(drivers))
    hist = history_before(seasons, year)
    path = pack / "data" / "drivers.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    recs = data["records"] if isinstance(data, dict) else data
    old = set(data.get("$career_retired", [])) if isinstance(data, dict) else set()
    recs = [r for r in recs if r["name"] not in old or not r.get("retired")]
    in_pack = set()
    filled = 0
    for r in recs:
        d = names.canon(r["name"])
        in_pack.add(d)
        h = hist.get(d)
        r["history"] = dict(h) if h else {"seasons": 0, "championships": 0, "wins": 0, "podiums": 0, "poles": 0,
                                          "starts": 0, "points": 0}
        filled += bool(h)
    active = {s["driver"] for s in seasons if int(s["season"]) == year}
    added = []
    if retired:
        for d, h in sorted(hist.items(), key=lambda x: (-x[1]["championships"], -x[1]["wins"], x[0])):
            if d in in_pack or d in active or not (h["wins"] or h["championships"]):
                continue
            info = drivers.get(d, {})
            by = int(info["birth_year"]) if str(info.get("birth_year", "")).isdigit() else None
            rec = {"name": d, "team": None, "retired": True,
                   "cornering": 5, "braking": 5, "consistency": 5, "smoothness": 5, "control": 5,
                   "talent": 5, "traits": [], "personalities": [],
                   "nationality": info.get("nationality") or "german", "history": dict(h)}
            if by:
                rec["birth_year"] = by
                rec["age"] = year - by
            else:
                rec["age"] = 60
            added.append(rec)
    recs += added
    if not isinstance(data, dict):
        data = {"records": recs}
    data["records"] = recs
    data["$career_retired"] = [r["name"] for r in added]
    data["$career_history"] = (f"history = DTM/ITC career before {year}, from docs/drivers "
                               f"(tools/driver_careers.py apply). Retired records: race winners and champions.")
    original = path.read_text(encoding="utf-8")
    if re.search(r'\n\s+\{"name": ', original):  # hand-kept file: one record per line
        head = {k: v for k, v in data.items() if k != "records"}
        lines = ["{"] + [f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}," for k, v in head.items()]
        lines.append('  "records": [')
        lines += [f"    {json.dumps(r, ensure_ascii=False)}," for r in recs]
        lines[-1] = lines[-1].rstrip(",")
        lines += ["  ]", "}"]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    else:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{pack.name}: {filled}/{len(recs) - len(added)} drivers have a DTM record before {year}; "
          f"{len(added)} retired winners and champions added")


def apply(args):
    seasons, drivers = load_db()
    for p in args.packs:
        apply_pack((REPO / p).resolve() if not Path(p).is_absolute() else Path(p), seasons, drivers,
                   retired=not args.no_retired)


def show(args):
    seasons, _ = load_db()
    names = Names([s["driver"] for s in seasons])
    h = history_before(seasons, args.year)
    for n in args.names:
        print(n, h.get(names.canon(n)))


def page(args):
    """Write the database page (tools/careers/page_template.html + data) to args.out."""
    races = read_csv(OUT / "dtm_races.csv")
    seasons, drivers = load_db()
    names = sorted(drivers, key=lambda n: (-int(drivers[n]["wins"]), -int(drivers[n]["starts"]), n))
    idx = {n: i for i, n in enumerate(names)}
    pts = collections.defaultdict(float)
    for s in seasons:
        pts[s["driver"]] += float(s["points"] or 0)
    D = {"drivers": [[n, drivers[n]["nationality"], drivers[n]["birth_year"], drivers[n]["first_season"],
                      drivers[n]["last_season"], int(drivers[n]["seasons"]), int(drivers[n]["titles"]),
                      int(drivers[n]["starts"]), int(drivers[n]["wins"]), int(drivers[n]["podiums"]),
                      int(drivers[n]["poles"]), round(pts[n], 1)] for n in names]}
    by_season = collections.defaultdict(list)
    for r in races:
        by_season[r["season"]].append(r)
    srow = {(s["driver"], s["season"], s["series"]): s for s in seasons}
    D["seasons"] = {}
    for y, rows in sorted(by_season.items()):
        cols = []
        for r in rows:
            c = (r["series"], int(r["round"]), int(r["heat"] or 0), r["event"], r["kind"])
            if c not in cols:
                cols.append(c)
        cols.sort(key=lambda c: (c[0], c[1], c[2]))
        ci = {c[:3]: i for i, c in enumerate(cols)}
        table = {}
        for r in rows:
            k = (r["driver"], r["series"])
            if k not in table:
                s = srow.get((r["driver"], y, r["series"]), {})
                table[k] = [idx[r["driver"]], r["series"], s.get("position", ""), s.get("points", ""),
                            r["make"], int(r["guest"] or 0)] + [""] * len(cols)
            cell = r["pos"] or r["status"]
            flags = ("P" if r["pole"] == "1" else "") + ("F" if r["fastest_lap"] == "1" else "")
            if flags:
                cell += "|" + flags
            table[k][6 + ci[(r["series"], int(r["round"]), int(r["heat"] or 0))]] = cell
        trs = sorted(table.values(), key=lambda t: (t[1] != "DTM", int(t[2]) if str(t[2]).isdigit() else 999,
                                                    -float(t[3] or 0), names[t[0]]))
        D["seasons"][y] = {"cols": [list(c) for c in cols], "rows": trs,
                           "source": rows[0]["source"]}
    D["packs"] = []
    for f in sorted(REPO.glob("seasons/*/data/drivers.json")):
        pk = f.parent.parent
        if not pk.name.startswith(("dtm-", "itc-")):
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        recs = d["records"] if isinstance(d, dict) else d
        out = []
        for r in recs:
            h = r.get("history") or {}
            if not (h.get("starts") or r.get("retired") or r.get("team")):
                continue  # skip free juniors without a record
            out.append([r["name"], r.get("team") or ("retired" if r.get("retired") else ""), h.get("seasons", 0),
                        h.get("championships", 0), h.get("wins", 0), h.get("podiums", 0), h.get("poles", 0),
                        h.get("starts", 0), h.get("points", 0)])
        D["packs"].append({"id": pk.name, "year": pack_year(pk), "drivers": out,
                           "total": len(recs)})
    checks = (OUT / "CHECKS.md").read_text(encoding="utf-8").split("\n")
    D["checks"] = [c[2:] for c in checks if c.startswith("- ")]
    D["counts"] = {"races": len(races), "driver_seasons": len(seasons), "drivers": len(drivers),
                   "seasons": len(by_season)}
    D["built"] = __import__("datetime").date.today().isoformat()
    tpl = (Path(__file__).resolve().parent / "careers" / "page_template.html").read_text(encoding="utf-8")
    html = tpl.replace("/*DATA*/null", json.dumps(D, ensure_ascii=False, separators=(",", ":")))
    Path(args.out).write_text(html, encoding="utf-8")
    print(f"wrote {args.out} ({len(html) // 1024} KB)")


def fetch(args):
    here = Path(__file__).resolve().parent / "careers"
    subprocess.run([sys.executable, "-I", str(here / "fetch_fandom.py"), str(CACHE)], check=True)
    subprocess.run([sys.executable, "-I", str(here / "fetch_wiki.py"), str(CACHE)], check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch").set_defaults(fn=fetch)
    sub.add_parser("build").set_defaults(fn=build)
    a = sub.add_parser("apply")
    a.add_argument("packs", nargs="+")
    a.add_argument("--no-retired", action="store_true")
    a.set_defaults(fn=apply)
    pg = sub.add_parser("page")
    pg.add_argument("out")
    pg.set_defaults(fn=page)
    h = sub.add_parser("history")
    h.add_argument("year", type=int)
    h.add_argument("names", nargs="+")
    h.set_defaults(fn=show)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
