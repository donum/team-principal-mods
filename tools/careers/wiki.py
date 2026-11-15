"""Parse en.wikipedia DTM season pages: drivers' standings (per race, bold = pole, italic = fastest lap)
and the season summary (pole + winner per race)."""
import csv, json, re, sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from fandom import top_split

def link_name(s):
    m = re.search(r"\[\[([^|\]]+)(?:\|([^\]]+))?\]\]", s)
    if not m: return None
    return (m.group(2) or m.group(1)).strip()

def link_target(s):
    m = re.search(r"\[\[([^|\]]+)(?:\|([^\]]+))?\]\]", s); return m.group(1).strip() if m else None

def strip_refs(s):
    s = re.sub(r"<ref[^>/]*/>", "", s); s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"\{\{\s*(refn|efn|ref|note|sfn)[^{}]*(\{\{[^{}]*\}\}[^{}]*)*\}\}", "", s, flags=re.I)
    return s

def rows_of(table):
    rows = re.split(r"\n\|-[^\n]*", table)
    out = []
    for r in rows:
        cells = []
        for line in r.split("\n"):
            if line[:1] in ("|", "!") and not line.startswith(("|}", "{|", "|+")):
                cells += [(line[0], c) for c in top_split(line[1:], "||" if line[0] == "|" else "!!")]
        out.append(cells)
    return out

def val(c):
    parts = top_split(c, "|")
    return parts[-1].strip() if len(parts) > 1 and re.search(r'(style|align|colspan|rowspan|nowrap|width|bgcolor)\s*=', parts[0]) else c.strip()

def span(c, k="colspan"):
    parts = top_split(c, "|")
    m = re.search(k + r'="?(\d+)', parts[0]) if len(parts) > 1 else None
    return int(m.group(1)) if m else 1

def standings(year, text):
    m = re.search(r"(==+|\n;)\s*'*Drivers'? ?(championship|standings)", text, re.I)
    if not m: return []
    head, pos0 = None, m.end()
    for _ in range(4):
        tm = re.compile(r'\{\|\s*class="?wikitable').search(text, pos0)
        if not tm: return []
        k = text.find("\n|}", tm.start())
        rows = rows_of(strip_refs(text[tm.start():k]))
        head = next((r for r in rows if any(val(c) == "Driver" for _, c in r)), None)
        if head: break
        pos0 = k
    if not head: return []
    events = []
    for kind, c in head:
        v = val(c)
        if not v or "Driver" in v or "Pos" in v or "Points" in v or "Pts" in v: continue
        code = re.sub(r"\{\{[^{}]*\}\}|<br\s*/?>", " ", v); code = link_name(code) or code.strip()
        events.append((code.strip(), link_target(v) or "", span(c)))
    out = []
    for r in rows:
        if r is head or len(r) < 3: continue
        name_cell = next((val(c) for k, c in r[:3] if "[[" in c and "flagicon" in c or ("[[" in c and k == "|")), None)
        if not name_cell: continue
        driver = link_name(re.sub(r"\{\{flagicon[^{}]*\}\}", "", name_cell))
        idx = [i for i, (k, c) in enumerate(r) if val(c) == name_cell][0]
        pos = val(r[0][1]) if idx > 0 else ""
        res = r[idx + 1:]
        if res and res[-1][0] == "!": res = res[:-1]
        ncols = sum(e[2] for e in events)
        cells = []
        for k, c in res: cells += [c] * span(c)
        if len(cells) == ncols + 1: cells = cells[:-1]
        if len(cells) != ncols:
            out.append({"season": year, "driver": driver, "error": f"{len(cells)} vs {ncols}"}); continue
        i = 0
        for rn, (code, target, sp) in enumerate(events, 1):
            for h in range(sp):
                c = cells[i]; i += 1
                v = re.sub(r"<sup>.*?</sup>|†|‡|&dagger;", "", val(c)).strip()
                pole = "'''" in v; fl = bool(re.search(r"(?<!')''(?!')|'''''", v))
                v = v.replace("'", "").strip()
                if not v: continue
                p = re.match(r"\d+", v)
                out.append({"season": year, "round": rn, "code": code, "heat": h + 1 if sp > 1 else "", "driver": driver,
                            "pos": p.group() if p else "", "status": "" if p else v.upper(), "pole": int(pole), "fastest_lap": int(fl),
                            "season_pos": re.sub(r"\D", "", pos)})
    return out

def person(cell):
    v = val(cell)
    v = re.sub(r"\{\{[^{}]*\}\}", "", v); v = re.sub(r"<br\s*/?>.*", "", v)
    n = link_name(v)
    if n: return n
    v = re.sub(r"\(.*?\)", "", v).replace("'", "").strip()
    return v if re.match(r"^[A-ZÀ-Þ][\w.\-' ]+$", v) else ""

def summary(year, text):
    """pole and winner per race from the summary table with a 'Pole' header."""
    out = []
    for m in re.finditer(r"\{\|\s*class=\"?wikitable", text):
        k = text.find("\n|}", m.start()); t = strip_refs(text[m.start():k])
        if not re.search(r"!\s*Pole", t): continue
        if re.search(r"!\s*(Pos|Fahrer)", t) and not re.search(r"Sieger|Winn", t): continue
        rows = rows_of(t); head = rows[0] if rows and rows[0] else rows[1]
        hdr = []
        for kind, c in [x for r in rows[:2] for x in r]:
            hdr += [val(c)] * span(c)
        try:
            pi = next(i for i, h in enumerate(hdr) if h.startswith("Pole")); wi = next(i for i, h in enumerate(hdr) if "Winning driver" in h or h.startswith("Winner") or "Race winner" in h or "Winning Driver" in h or h.startswith("Sieger"))
        except StopIteration:
            continue
        carry = {}; n = 0
        for r in rows[1:]:
            if not r: continue
            cells, col = [], 0
            # rowspan carry for leading cells
            flat = []
            for kind, c in r: flat.append((kind, c, span(c), span(c, "rowspan")))
            built = []; ci = 0; col = 0
            while col < len(hdr) and (ci < len(flat) or col in carry):
                if col in carry and carry[col][1] > 0:
                    built.append(carry[col][0]); carry[col][1] -= 1; col += 1; continue
                if ci >= len(flat): break
                kind, c, cs, rs = flat[ci]; ci += 1
                for _ in range(cs):
                    built.append(c)
                    if rs > 1: carry[col] = [c, rs - 1]
                    col += 1
            if len(built) <= max(pi, wi): continue
            pole, win = person(built[pi]), person(built[wi])
            if not win: continue
            n += 1
            out.append({"season": year, "race": n, "pole": pole or "", "winner": win, "label": " / ".join(val(b)[:40] for b in built[:3])})
        if out: break
    return out

if __name__ == "__main__":
    W = json.load(open(sys.argv[1], encoding="utf-8"))
    S, M, errs = [], [], []
    for y, p in sorted(W.items()):
        st = standings(y, p["text"]); errs += [f"{y} {r['driver']}: {r['error']}" for r in st if "error" in r]
        S += [r for r in st if "error" not in r]; M += summary(y, p["text"])
        print(y, "standings rows", sum(1 for r in st if "error" not in r), "summary races", sum(1 for r in M if r["season"] == y))
    for fn, rows in ((sys.argv[2], S), (sys.argv[3], M)):
        with open(fn, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
    print("\n".join(errs[:40]))
