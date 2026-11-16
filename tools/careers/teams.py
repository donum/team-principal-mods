"""Team entries and team history for the DTM career database.

Who ran which car: the "Teams and drivers" table of each en.wikipedia season
page (1987 on). Its team cell links the operator's article
([[HWA Team|D2 AMG-Mercedes]], [[Phoenix Racing (Germany)|Team Phoenix]]),
so a sponsor name still says who ran the car, and the rounds column covers
drivers who changed team. Seasons without that table (1984-1986) and drivers
missing from it fall back to the entrant name on the dtm.fandom.com (de)
season page ("Starterfeld").

Team titles: the first row of the en.wikipedia "Teams' championship" table
(2000 on; earlier seasons had no teams' title in these tables).

A pack team gets its history through docs/drivers/team_lineage.csv: rows of
(pack, team, pattern, from, to). `pattern` is a regular expression matched
against "<linked articles> | <entrant name>" of every entry in those years.
"""

import collections
import json
import re

ROW_SPLIT = re.compile(r"\n\|-[^\n]*")
DASH = "–—−�-"


def _strip_attrs(cell):
    """'rowspan="2" style=x | value' -> ('rowspan="2" style=x', 'value')."""
    depth = 0
    for i, ch in enumerate(cell):
        if cell.startswith(("[[", "{{"), i):
            depth += 1
        elif cell.startswith(("]]", "}}"), i):
            depth -= 1
        elif ch == "|" and depth == 0:
            head = cell[:i]
            if "=" in head and "[[" not in head and "{{" not in head:
                return head, cell[i + 1:]
            return "", cell
    return "", cell


def _split_cells(line):
    """One wikitext table line ('| a || b' or '! a !! b') -> raw cells."""
    body = line[1:]
    sep = "!!" if line.startswith("!") else "||"
    out, depth, start, i = [], 0, 0, 0
    while i < len(body):
        if body.startswith(("[[", "{{"), i):
            depth += 1
            i += 2
            continue
        if body.startswith(("]]", "}}"), i):
            depth -= 1
            i += 2
            continue
        if depth == 0 and body.startswith(sep, i):
            out.append(body[start:i])
            i += 2
            start = i
            continue
        i += 1
    out.append(body[start:])
    return out


def visible(s):
    """Wikitext -> the text a reader sees."""
    s = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"\{\{(?:[Tt]ooltip|[Aa]bbr)\|([^|}]*)\|[^}]*\}\}", r"\1", s)
    s = re.sub(r"\{\{(?:[Ii]ll|[Ii]nterlanguage link)\|([^|}]*)[^}]*\}\}", r"\1", s)
    s = re.sub(r"\{\{[^{}]*\}\}", "", s)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"<[^>]+>|'''?", "", s)
    return re.sub(r"\s+", " ", s).strip()


def links(s):
    return [m.group(1).strip() for m in re.finditer(r"\[\[([^|\]#]+)", s)]


def _header_name(cell):
    v = visible(cell).lower().rstrip(".")
    if v.startswith("driver"):
        return "driver"
    if v in ("no", "car number", "number", "#"):
        return "no"
    for k in ("team", "round", "manufacturer", "car", "note", "engine", "tyre", "chassis"):
        if v.startswith(k):
            return k
    return v


def parse_rounds(text, n_rounds):
    t = visible(text)
    if not t or re.fullmatch(r"(?i)all|all rounds", t):
        return set(range(1, n_rounds + 1))
    out = set()
    for a, b in re.findall(rf"(\d+)\s*(?:[{DASH}]\s*(\d+))?", t):
        a = int(a)
        out.update(range(a, int(b) + 1) if b else [a])
    return out or set(range(1, n_rounds + 1))


def section(text, title_re):
    m = re.search(rf"\n(=+)\s*{title_re}\s*=+\s*\n", text)
    if not m:
        return ""
    level = len(m.group(1))
    end = re.search(rf"\n={{2,{level}}}[^=]", text[m.end():])
    return text[m.end(): m.end() + end.start()] if end else text[m.end():]


def tables(text):
    """Top-level wikitables in `text` (nested tables are skipped)."""
    out, i = [], 0
    while True:
        s = text.find("{|", i)
        if s < 0:
            return out
        depth, j = 0, s
        while j < len(text):
            if text.startswith("{|", j):
                depth += 1
                j += 2
            elif text.startswith("|}", j):
                depth -= 1
                j += 2
                if depth == 0:
                    break
            else:
                j += 1
        out.append(text[s:j])
        i = j


def table_rows(table):
    """Rows of cells with rowspans resolved: [{column name: raw cell}]."""
    table = re.sub(r"<ref[^>/]*/>|<ref[^>]*>.*?</ref>", "", table, flags=re.S)  # citations span lines
    table = re.sub(r"<!--.*?-->", "", table, flags=re.S)
    parts = ROW_SPLIT.split("\n" + table)
    header, rows, spans = None, [], {}
    for part in parts:
        lines = [ln for ln in part.split("\n") if ln.startswith(("|", "!")) and not ln.startswith(("|}", "{|", "|+"))]
        cells = []
        for ln in lines:
            for c in _split_cells(ln):
                attrs, val = _strip_attrs(c)
                m = re.search(r"rowspan\s*=\s*\"?(\d+)", attrs)
                cells.append((int(m.group(1)) if m else 1, val, ln.startswith("!")))
        if not cells:
            continue
        if header is None:
            if all(h for _, _, h in cells):
                header = [_header_name(v) for _, v, _ in cells]
            continue
        row, it = {}, iter(cells)
        for col in range(len(header)):
            if spans.get(col, (0, None))[0] > 0:
                left, val = spans[col]
                spans[col] = (left - 1, val)
                row[header[col]] = val
                continue
            try:
                span, val, _ = next(it)
            except StopIteration:
                break
            row[header[col]] = val
            if span > 1:
                spans[col] = (span - 1, val)
        rows.append(row)
    return rows


def wiki_entries(text, n_rounds, canon):
    """[(driver, rounds set, linked articles, entrant name)] from an en.wikipedia season page."""
    sec = section(text, r"(?:Teams and drivers|Entry list|Entries|Teams)")
    out = []
    for tb in tables(sec):
        for row in table_rows(tb):
            team, drv = row.get("team"), row.get("driver")
            if not team or not drv:
                continue
            name = visible(drv)
            if not name or not re.search(r"[A-Za-z]", name):
                continue
            rounds = row.get("round")
            if rounds is None and row.get("note") and re.search(r"(?i)round", row["note"]):
                rounds = row["note"]
            out.append((canon(name), parse_rounds(rounds or "", n_rounds), links(team), visible(team)))
    return out


def team_champion(text):
    """(linked articles, entrant) of the first row of the teams' championship table, or None."""
    sec = section(text, r"Teams'? (?:[Cc]hampionship|[Ss]tandings)")
    for tb in tables(sec):
        for row in table_rows(tb):
            team = row.get("team")
            pos = visible(row.get("pos", "") or row.get("pos.", "") or "")
            if team and (pos in ("1", "") or pos.startswith("1")):
                return links(team), visible(team)
    return None


FANDOM_ROW = re.compile(r"\{\{(?:Gast|Junior|Test)?(?:[Ss]tarter|fahrer)\|(\d{4})\|([^|]*)\|([^|]+)\|([^|]*)\|([^|]*)\|")


def fandom_entries(text):
    """[(year, driver, entrant)] from the "Starterfeld" table of a dtm.fandom.com (de) season page."""
    i = text.find("Starterfeld")
    seg = text[i:text.find("\n==", i + 15)] if i >= 0 else ""
    out = []
    for m in FANDOM_ROW.finditer(seg):
        year, _no, driver, _make, team = m.groups()
        team = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", team).strip()
        if team:
            out.append((int(year), driver.strip(), team))
    return out


def build(wiki_en, fandom_pages, races, canon):
    """Rows for dtm_team_entries.csv and dtm_team_champions.csv."""
    text = lambda v: v if isinstance(v, str) else (v.get("text") or v.get("wikitext") or "")
    raced = collections.defaultdict(set)       # (season, driver) -> rounds with a race row
    n_rounds = collections.Counter()
    for r in races:
        if r["round"].isdigit() and r["series"] in ("DTM", "ITC"):
            raced[(r["season"], r["driver"])].add(int(r["round"]))
            n_rounds[r["season"]] = max(n_rounds[r["season"]], int(r["round"]))
    entries, champions = [], []
    fandom = {}                                 # (season, driver) -> entrant on the fandom wiki
    for title, p in fandom_pages.items():
        t = text(p)
        if re.fullmatch(r"\d{4}", title) and t.lstrip().startswith("{{Saison"):
            for year, driver, entrant in fandom_entries(t):
                fandom.setdefault((str(year), canon(driver)), entrant)
    seen = set()
    for y in sorted(wiki_en):
        page = text(wiki_en[y])
        for drv, rounds, arts, entrant in wiki_entries(page, n_rounds[y] or 12, canon):
            entries.append({"season": y, "driver": drv, "rounds": " ".join(map(str, sorted(rounds))),
                            "articles": ";".join(arts), "entrant": entrant,
                            "fandom_entrant": fandom.get((y, drv), ""), "source": "en.wikipedia"})
            seen.add((y, drv))
        champ = team_champion(page)
        if champ:
            champions.append({"season": y, "articles": ";".join(champ[0]), "entrant": champ[1],
                              "source": "en.wikipedia"})
    for (year, drv), entrant in sorted(fandom.items()):
        if (year, drv) in seen:
            continue
        seen.add((year, drv))
        rounds = raced.get((year, drv)) or set(range(1, (n_rounds[year] or 12) + 1))
        entries.append({"season": year, "driver": drv, "rounds": " ".join(map(str, sorted(rounds))),
                        "articles": "", "entrant": entrant, "fandom_entrant": entrant, "source": "dtm.fandom.com"})
    entries.sort(key=lambda e: (e["season"], e["entrant"], e["driver"]))
    return entries, champions


# ---------------------------------------------------------------- history

def match_key(arts, entrant, fandom=""):
    """What a lineage pattern sees: "<linked articles> | <entrant> | <fandom entrant>"."""
    return " ; ".join(arts) + " | " + entrant + " | " + fandom


def lineage_rules(rows, pack, team):
    return [(re.compile(r["pattern"]), int(r["from"]), int(r["to"])) for r in rows
            if r["pack"] == pack and r["team"] == team]


def belongs(rules, year, arts, entrant, fandom=""):
    k = match_key(arts, entrant, fandom)
    return any(lo <= year <= hi and rx.search(k) for rx, lo, hi in rules)


def team_history(rules, year, entries, races, driver_seasons, champions):
    """History of one pack team over every season before `year`.

    entries: rows of dtm_team_entries.csv; races: rows of dtm_races.csv;
    driver_seasons: rows of dtm_driver_seasons.csv; champions: rows of dtm_team_champions.csv.
    """
    # A driver with one entry in a season raced every race of it for that team.
    # Only drivers who changed team need the rounds column. Older en.wikipedia
    # tables count heats there (1990: "Rounds 15-16" of 11 two-heat weekends),
    # so numbers above the season's weekends are read as race numbers.
    n_entries = collections.Counter((int(e["season"]), e["driver"]) for e in entries)
    weekends = collections.Counter()
    order = collections.defaultdict(set)
    for r in races:
        if r["kind"] == "race" and r["round"].isdigit():
            y = int(r["season"])
            weekends[y] = max(weekends[y], int(r["round"]))
            order[y].add((int(r["round"]), r["heat"]))
    race_no = {(y, rh): i + 1 for y, rhs in order.items() for i, rh in enumerate(sorted(rhs))}
    ours = {}                                   # (season, driver) -> (rounds, by race number) or None = all
    for e in entries:
        y = int(e["season"])
        if y < year and belongs(rules, y, e["articles"].split(";") if e["articles"] else [], e["entrant"],
                                e.get("fandom_entrant", "")):
            if n_entries[(y, e["driver"])] == 1:
                ours[(y, e["driver"])] = None
            else:
                rs = {int(r) for r in e["rounds"].split() if r}
                prev = ours.get((y, e["driver"]), (set(), False)) or (set(), False)
                ours[(y, e["driver"])] = (prev[0] | rs, prev[1] or max(rs, default=0) > weekends[y])
    h = {"seasons": 0, "championships": 0, "wins": 0, "podiums": 0, "poles": 0, "starts": 0, "points": 0}
    events, years = set(), set()
    starts_by = collections.Counter()           # (season, driver) -> starts for the team
    for r in races:
        y = int(r["season"])
        if y >= year or r["kind"] != "race" or r["series"] not in ("DTM", "ITC"):
            continue
        k = (y, r["driver"])
        if k not in ours:
            continue
        if ours[k] is not None:
            rounds, by_race = ours[k]
            n = race_no.get((y, (int(r["round"]), r["heat"]))) if by_race else (
                int(r["round"]) if r["round"].isdigit() else 0)
            if n not in rounds:
                continue
        if r["started"] != "1":
            continue
        years.add(y)
        events.add((y, r["series"], r["round"], r["heat"]))
        starts_by[(y, r["driver"])] += 1
        pos = r["pos"]
        if pos == "1":
            h["wins"] += 1
        if pos in ("1", "2", "3"):
            h["podiums"] += 1
        if r["pole"] == "1":
            h["poles"] += 1
    points = 0.0
    for s in driver_seasons:
        y = int(s["season"])
        k = (y, s["driver"])
        if y >= year or s["series"] not in ("DTM", "ITC") or k not in starts_by:
            continue
        all_starts = int(s["starts"] or 0) or starts_by[k]
        points += float(s["points"] or 0) * min(1.0, starts_by[k] / all_starts)
    h["seasons"] = len(years)
    h["starts"] = len(events)
    h["points"] = int(round(points))
    h["championships"] = sum(1 for c in champions if int(c["season"]) < year
                             and belongs(rules, int(c["season"]), c["articles"].split(";") if c["articles"] else [],
                                         c["entrant"]))
    return h


def dumps_entries(rows):
    return json.dumps(rows, ensure_ascii=False)
