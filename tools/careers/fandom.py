"""Parse the Fahrerwertung table of every DTM season page of dtm.fandom.com/de into race rows."""
import csv, json, re, sys
from pathlib import Path

POS_TPL = {"gold", "silber", "bronze", "grün", "blau", "grau", "weiß", "pink"}
START_NOFIN = {"dnf": "DNF", "nc": "NC", "dsq": "DSQ", "ex": "DSQ"}
NO_START = {"dns": "DNS", "dna": "DNA", "dnq": "DNQ", "dnp": "DNP", "inj": "INJ", "none": "WD", "c": "CANCELLED"}

def top_split(s, sep):
    out, depth, buf, i = [], 0, "", 0
    while i < len(s):
        two = s[i:i + 2]
        if two in ("{{", "[["): depth += 1; buf += two; i += 2; continue
        if two in ("}}", "]]"): depth -= 1; buf += two; i += 2; continue
        if depth == 0 and s.startswith(sep, i): out.append(buf); buf = ""; i += len(sep); continue
        buf += s[i]; i += 1
    out.append(buf); return out

def cell_value(c):
    parts = top_split(c, "|")
    return parts[-1].strip() if len(parts) > 1 and re.match(r'\s*(align|width|colspan|rowspan|style|class)\b', parts[0]) else c.strip()

def cell_attr(c, name):
    m = re.match(r'\s*[^{\[]*?\b' + name + r'="?(\d+)', c); return int(m.group(1)) if m and "|" in top_split(c, "|")[0] + "|" else 1

def table_after(text, heading):
    i = re.search(r"==\s*" + heading + r"\s*==", text)
    if not i: return None
    j = text.find("{|", i.end()); k = text.find("\n|}", j)
    return text[j:k]

def parse_result(v):
    """-> (kind, pos, status, raw). kind: race or qr."""
    raw = v
    v = re.sub(r'^\s*(?:(?:width|align|style)="[^"]*"\s*)+', "", v)
    m = re.match(r"\{\{\s*([^|{}]+?)\s*(?:\|([^{}]*))?\}\}(.*)$", v, re.S)
    if not m:
        return None if not v.strip() else ("race", None, "UNPARSED", raw)
    tpl, arg, rest = m.group(1).strip().lower(), m.group(2) or "", m.group(3)
    if tpl in ("none",) or (tpl == "grau" and not arg.strip()): return None  # not entered
    kind = "race"
    if tpl.endswith(" q"): kind, tpl = "qr", tpl[:-2].strip()
    if tpl in POS_TPL:
        n = re.search(r"\d+", arg)
        if n: return (kind, int(n.group()), "dropped" if "(" in arg else "", raw)
        a = arg.strip("'() ").upper()
        tpl = a.lower() if a.lower() in START_NOFIN or a.lower() in NO_START else tpl
        if tpl in POS_TPL: return (kind, None, a or "UNPARSED", raw)
    if tpl in START_NOFIN: return (kind, None, START_NOFIN[tpl], raw)
    if tpl in NO_START: return (kind, None, NO_START[tpl], raw)
    return (kind, None, "UNPARSED:" + tpl, raw)

def parse_season(title, text, heading="Fahrerwertung", series=None):
    t = table_after(text, heading)
    if not t: return [], f"{title}: no {heading}"
    rows = re.split(r"\n\|-[^\n]*", t)
    head, events = None, []
    for r in rows:
        if "Fahrer" in r and ("[[" in r) and not events:
            for line in r.split("\n"):
                if not line.startswith("|"): continue
                for c in top_split(line[1:], "||"):
                    m = re.search(r"\[\[([^|\]]+)\|([^\]]+)\]\]\s*$", c.strip())
                    if m and "Datei:" not in m.group(1):
                        span = re.search(r'colspan="?(\d+)', top_split(c, "|")[0]) if len(top_split(c, "|")) > 1 else None
                        events.append((m.group(1).strip(), m.group(2).strip(), int(span.group(1)) if span else 1))
            head = r; break
    out = []
    season_no = re.search(r"\d{4}", title).group()
    for r in rows:
        if r is head: continue
        cells = []
        for line in r.split("\n"):
            if line.startswith("|") and not line.startswith("|}") and not line.startswith("{|"):
                cells += [x for x in top_split(line[1:], "||")]
        if len(cells) < 3: continue
        vals = [cell_value(c) for c in cells]
        dm = re.match(r"\{\{\s*([^|{}]+?)\s*\}\}$", vals[1])
        if not dm or "Fahrer" in vals[1]: continue
        driver = dm.group(1).replace("&nbsp;", " ")
        guest = "gast" in vals[0].lower() or "gast" in r.lower().split("\n")[0]
        pos_txt = re.sub(r"\{\{\s*Gast\s*\|(.*?)\}\}", r"\1", vals[0]).strip(" .")
        make = re.sub(r"\{\{\s*center\s*\|", "", vals[2]); mm = re.search(r"\{\{\s*([^|{}]+?)\s+\d{4}", make)
        res = vals[3:-1]; pts = re.sub(r"\{\{\s*Gast\s*\|(.*?)\}\}", r"\1", vals[-1]).strip()
        ncols = sum(e[2] for e in events)
        if len(res) != ncols:
            out.append({"season": season_no, "driver": driver, "error": f"{len(res)} cells vs {ncols} columns"}); continue
        i = 0
        for en, (ev, code, span) in enumerate(events, 1):
            for h in range(span):
                pr = parse_result(res[i]); i += 1
                if pr is None: continue
                kind, pos, status, raw = pr
                out.append({"season": season_no, "series": series or ("ITC" if season_no == "1996" else "DTM"), "round": en, "event": ev, "code": code, "heat": h + 1 if span > 1 else "",
                            "kind": kind, "driver": driver, "make": mm.group(1) if mm else "", "guest": int(guest),
                            "pos": pos if pos is not None else "", "status": status, "season_pos": pos_txt if pos_txt.isdigit() else "",
                            "season_points": pts, "raw": raw})
    return out, None

if __name__ == "__main__":
    P = json.load(open(sys.argv[1], encoding="utf-8"))
    allrows, errs = [], []
    for title, p in sorted(P.items()):
        if not p["text"].lstrip().startswith("{{Saison") or "Trophy" in title: continue
        if title == "1995":
            rows, err = parse_season(title, p["text"], r"Fahrerwertung \(DTM\)", "DTM")
            r2, e2 = parse_season(title, p["text"], r"Fahrerwertung \(ITC\)", "ITC"); rows += r2; err = err or e2
        else:
            rows, err = parse_season(title, p["text"])
        if err: errs.append(err)
        errs += [f"{r['season']} {r['driver']}: {r['error']}" for r in rows if "error" in r]
        allrows += [r for r in rows if "error" not in r]
    with open(sys.argv[2], "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, list(allrows[0])); w.writeheader(); w.writerows(allrows)
    print(len(allrows), "rows"); print("\n".join(errs[:60]))
    import collections
    print(collections.Counter(r["status"] for r in allrows if r["status"]).most_common(30))
