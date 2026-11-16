"""Translation review: every message of a game locale file, with where the game shows it.

The game keeps its texts in ui/assets/locales/<lang>.json (flat key -> text).
This tool reads the game's own code (tools/game_code.py unpacks it) and finds,
for every key, the module and function whose code holds the key, its key
prefix, or its English text (text.* keys are looked up by the English
wording). Module names become screen names ("ui.screens.headquarters_screen"
-> "Headquarters"), grouped into areas of the game.

It also runs simple checks on the translation: text still in English,
placeholders that differ, informal address (du, tu, ty) in a formal text, much longer than
the English (may not fit), English words left in, and short terms translated
in more than one way.

    python tools/locale_review.py                       # the game's de.json
    python tools/locale_review.py --lang fr
    python tools/locale_review.py --file C:/Users/me/Downloads/de.json

Needs the Python the game was built with (3.13, private/sim-venv, see
tools/simulate.py); started with another Python it re-runs itself there.

Output: private/locale_review/index.html (from tools/locale_review_template.html),
and private/locale_review/<lang>-<date>-<hash>.json, the data file for the
team review site (tools/review_site, upload it on the site's admin page).
It holds the game's texts, so it stays private (published only as a private
artifact for the reviewer).
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import marshal
import re
import subprocess
import sys
import types
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
import game_code  # noqa: E402

VENV_PY = REPO / "private" / "sim-venv" / "Scripts" / "python.exe"
TEMPLATE = REPO / "tools" / "locale_review_template.html"
OUT = REPO / "private" / "locale_review" / "index.html"

# Library modules in the game's archive; only the game's own code is scanned.
LIBRARY = re.compile(
    r"^(numpy|pygame|encodings|email|json|http|xml|urllib|importlib|collections|concurrent|"
    r"asyncio|ctypes|logging|multiprocessing|unittest|tkinter|_|jaraco|backports|pkg_resources|"
    r"setuptools|steamworks|PIL|curses|pydoc|distutils|zipfile|tomllib|sqlite3|wsgiref|lib2to3|"
    r"idlelib|xmlrpc|dbm|html|re\.|sre)")
# Modules that touch every key (the catalog loader) say nothing about where a text shows.
GENERIC = {"ui.localization"}
# Modules that translate whole families of texts; used only when nothing better is known.
WEAK = {"ui.mail_text", "ui.localization"}

PLACEHOLDER = re.compile(r"\{[^{}\n]*\}|<[^>\n]+>|\[[A-Z_/]+\]|%[sd]")

# Areas of the game, first match wins (on module name, then key).
AREAS = [
    ("Mailbox and news", r"mail|news|headline|announcement|email"),
    ("Race weekend", r"live|session|practice|quali|race|testing|telemetry|grid|timing|weather|wind|radio|"
                     r"pit|hotlap|stint|fuel|setup_panel|spectator|red_flag|yellows|speed_trap|track_map|"
                     r"standings_colors|stage|caution|lucky_lapper|lap_stats"),
    ("Markets and contracts", r"market|negotiation|sponsor|staff|contract|deal|buyout|proposal|lineup|"
                              r"charter|entry_purchase|entries|engine_naming"),
    ("Team and car", r"headquarters|factory|development|aero|hq|parts|performance|recon|academy|junior|"
                     r"ers|tyre|engine|chassis|technology|car_condition|team_dashboard|dashboard|"
                     r"needs_attention|management|driver_center"),
    ("Money", r"finance|budget|stock|valuation|holdings|purse"),
    ("Season and rules", r"standing|statistic|result|schedule|calendar|history|season_review|season_complete|"
                         r"regulation|rules|vote|points|championship|season"),
    ("Editors and Workshop", r"editor|roster|workshop|season_pack|pack"),
    ("Menus and setup", r"title|main_menu|options|tutorial|loading|load_game|team_select|series_select|"
                        r"principal|team_switch|menu|career|hub|first_load|tips"),
]

PACK_PARTS = {
    "rules": ("Season and rules", "Regulations (pack rules text)"),
    "radio": ("Race weekend", "Team radio messages"),
    "nationality": ("Menus and setup", "Nationality names"),
    "team_prose": ("Menus and setup", "Team descriptions (team select)"),
    "hotlap": ("Race weekend", "Hotlap texts"),
    "concepts": ("Team and car", "Car concept names"),
    "career": ("Menus and setup", "Career texts from the pack"),
    "technologies": ("Team and car", "Technology names"),
}

SCREEN_NAMES = {
    "ui.screens.hub_screen": "Hub (home screen)",
    "ui.oval.screens.oval_hub_screen": "Hub (home screen)",
    "ui.screens.mailbox_screen": "Mailbox",
    "ui.race_view": "Live race view",
    "ui.screens.title_screen": "Title screen",
    "ui.main_menu": "Main menu",
    "ui.first_load_tutorial_content": "First-start tutorial",
    "ui.first_load_tutorial": "First-start tutorial",
    "ui.loading_tips": "Loading screen tips",
    "ui.market_stat_help": "Market stat help tooltips",
    "ui.race_event_log": "Race event log",
    "ui.mail_text": "Mailbox (mail texts)",
    "nationalities": "Nationality names",
    "game_state": "Game messages",
}


def area_of(*names: str) -> str:
    for name in names:
        for area, pat in AREAS:
            if re.search(pat, name):
                return area
    return "Other"


def screen_of(module: str) -> str:
    if module in SCREEN_NAMES:
        return SCREEN_NAMES[module]
    name = module
    for pre in ("ui.oval.screens.", "ui.screens.", "ui.oval.", "ui.widgets.", "ui.", "managers.", "oval."):
        if name.startswith(pre):
            name = name[len(pre):]
            break
    name = re.sub(r"_screen$", "", name)
    words = name.replace(".", " ").replace("_", " ").strip()
    label = words[:1].upper() + words[1:]
    if module.startswith("managers.") or (module.startswith("oval.") and not module.startswith("oval.screens")):
        return f"Messages from {label.lower()}"
    if module.startswith("ui.widgets."):
        return f"{label} (shared widget)"
    return label


def part_of(qualname: str) -> str:
    """'HeadquartersScreen._draw_upgrade_panel.<locals>.row' -> 'upgrade panel'."""
    if not qualname:
        return ""
    bits = [b for b in qualname.split(".") if b and not b.startswith("<")]
    if bits and re.match(r"[A-Z]", bits[0]) and len(bits) > 1:
        bits = bits[1:]
    if not bits:
        return ""
    fn = bits[0]
    if fn in ("__init__", "draw", "render", "_draw", "build"):
        return ""
    fn = re.sub(r"^_+", "", fn)
    fn = re.sub(r"^(draw|render|build|make|get|format|fmt|compute|layout|show|update|handle)_", "", fn)
    return fn.replace("_", " ").strip()


def ensure_python(exe: Path) -> None:
    want = game_code.exe_python_version(exe)
    if sys.version_info[:2] == want:
        return
    if not VENV_PY.exists():
        sys.exit(f"Needs Python {want[0]}.{want[1]} (the game's). Set it up as in tools/simulate.py.")
    sys.exit(subprocess.call([str(VENV_PY), "-I", __file__, *sys.argv[1:]]))


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip(" :.!?-—–").lower()


def scan_code(pyz: Path, en: dict) -> dict[str, set]:
    keys = set(en)
    by_text = collections.defaultdict(list)
    for k, v in en.items():
        if k.startswith("text."):
            by_text[v].append(k)
    hits: dict[str, set] = collections.defaultdict(set)
    prefixes: dict[str, set] = collections.defaultdict(set)
    loose: dict[str, set] = collections.defaultdict(set)  # every constant, lower-cased and trimmed

    def note(s, mod, q):
        if 3 <= len(s) < 400:
            loose[norm(s)].add((mod, q))
            if "_" in s and " " not in s:
                loose[norm(s.replace("_", " "))].add((mod, q))
        if s in keys:
            hits[s].add((mod, q))
        elif s in by_text:
            for kk in by_text[s]:
                hits[kk].add((mod, q))
        elif (s.endswith(".") or s.endswith("_")) and 8 < len(s) < 90 and s.count(".") >= 2 \
                and re.fullmatch(r"[a-z0-9_.]+", s):
            prefixes[s].add((mod, q))

    for f in sorted(pyz.glob("*.marshal")):
        mod = f.stem
        if LIBRARY.match(mod) or mod in GENERIC:
            continue
        try:
            co = marshal.loads(f.read_bytes())
        except Exception:
            continue

        def walk(c, q):
            q2 = c.co_name if not q else f"{q}.{c.co_name}"
            if q2 == "<module>":
                q2 = ""
            for k in c.co_consts:
                if isinstance(k, str):
                    note(k, mod, q2)
                elif isinstance(k, (tuple, frozenset)):
                    for s in k:
                        if isinstance(s, str):
                            note(s, mod, q2)
                elif isinstance(k, types.CodeType):
                    walk(k, q2)
        walk(co, "")

    # Texts the code builds at runtime: an f-string piece or an upper-cased label.
    for k in keys:
        if k in hits or not k.startswith("text."):
            continue
        e = en[k]
        if norm(e) in loose:
            hits[k] |= loose[norm(e)]
            continue
        pieces = sorted((norm(p) for p in PLACEHOLDER.split(e)), key=len, reverse=True)
        for piece in pieces[:2]:
            if len(piece) >= 8 and piece in loose and len(loose[piece]) <= 6:
                hits[k] |= loose[piece]
                break

    # Keys built at runtime: a prefix constant plus a computed ending.
    plist = sorted(prefixes, key=len, reverse=True)
    for k in keys:
        if k in hits:
            continue
        for p in plist:
            if k.startswith(p):
                hits[k] |= prefixes[p]
                break
    return hits


def locate(key: str, found: set) -> list[dict]:
    """Where a key shows: [{area, screen, part, module, how}] best first."""
    strong = [(m, q) for m, q in found if m not in WEAK]
    use = strong or ([] if key.startswith("mail.template.") else list(found))
    out = []
    if key.startswith("text.pack."):
        part = key.split(".")[2]
        area, screen = PACK_PARTS.get(part, ("Other", f"Pack text ({part})"))
        out.append({"area": area, "screen": screen, "part": "", "module": "season pack data", "how": "pack"})
    if key.startswith("mail.template.") and not strong:
        src = key.split(".")[2]
        out.append({"area": "Mailbox and news", "screen": "Mailbox",
                    "part": f"mails from {src.replace('_', ' ')}", "module": f"managers.{src}", "how": "key"})
    seen = set()
    # UI screens first, then other modules.
    for m, q in sorted(use, key=lambda mq: (not mq[0].startswith("ui."), mq[0], mq[1])):
        screen = screen_of(m)
        if m.startswith("managers.") and key.startswith("mail."):
            area = "Mailbox and news"
            screen = "Mailbox"
            part = f"mails from {m.split('.', 1)[1].replace('_', ' ')}"
        else:
            area = area_of(m, key)
            part = part_of(q)
        if m.startswith("ui.oval") or m.startswith("oval.") or key.startswith(("oval.", "text.oval.")):
            area = "Oval series: " + area
        sig = (area, screen, part)
        if sig in seen:
            continue
        seen.add(sig)
        out.append({"area": area, "screen": screen, "part": part, "module": m + (f" · {q}" if q else ""),
                    "how": "code"})
    if not out:
        ns = key.split(".")
        family = ns[1] if ns[0] == "text" else ns[0]
        if ns[0] == "text" and family in ("career", "markets", "oval") and len(ns) > 3:
            family = ns[2]
        label = family.replace("_", " ")
        area = area_of(key)
        if key.startswith(("oval.", "text.oval")):
            area = "Oval series: " + area_of(".".join(ns[2:])) if family == "oval" else "Oval series: " + area
        out.append({"area": area, "screen": label[:1].upper() + label[1:], "part": "",
                    "module": "", "how": "guess"})
    return out[:6]


# --- translation checks -------------------------------------------------------

# Words German UI text uses as well; not flagged as English leftovers.
SHARED_WORDS = {
    "team", "teams", "start", "status", "name", "test", "tests", "sponsor", "sponsors", "budget", "manager",
    "setup", "setups", "motor", "pole", "position", "finish", "start", "stint", "stints", "boxen", "safety",
    "car", "drs", "ers", "kers", "hybrid", "hotlap", "slick", "slicks", "intermediate", "pit", "lap",
    "workshop", "steam", "online", "offline", "info", "details", "level", "bonus", "media", "marketing",
    "design", "chassis", "monocoque", "sprint", "super", "pro", "rookie", "academy", "scouting", "oval",
    "rennen", "gas", "plan", "pack", "packs", "mod", "mods", "limit", "spoiler", "diffusor", "ok", "top",
    "standard", "normal", "optimal", "minimal", "maximal", "total", "fan", "fans", "hospitality", "pr",
    "charter", "charters", "playoff", "playoffs", "stage", "stages", "caution", "chase", "image", "trend",
    "fokus", "feedback", "training", "service", "event", "events", "management", "staff", "technik",
    "aero", "grip", "balance", "downforce", "update", "updates", "upgrade", "upgrades", "screen", "tab",
    "qualifying", "grand", "prix", "junior", "sport", "partner", "prestige", "podium", "garage", "option",
    "ranking", "form", "system", "json", "enter", "formula", "rest", "chance", "live", "designs", "detail",
    "logo", "editor", "text", "delta", "preset", "protest", "simulation", "superspeedway", "paddock",
    "talent", "moment", "agent", "pool", "maximum", "minimum", "legacy", "dashboard", "format", "file",
    "control", "operation", "spin", "drag", "boss", "chief", "formel", "slot", "slots", "reserve", "stop",
    "timing", "offseason", "benchmark", "rating", "ratings", "crew", "deal", "deals", "tier",
}
# Informal and formal address per language. A text is flagged "informal" only when
# the language's file is mostly formal.
ADDRESS = {
    "de": (r"\b(du|dich|dein|deine|deinen|deinem|deiner|deines|euch|euer|eure)\b", r"\b(Sie|Ihr|Ihre|Ihren|Ihrem|Ihrer|Ihnen)\b"),
    "fr": (r"\b(tu|toi|ton|ta|tes)\b", r"\b(vous|votre|vos)\b"),
    "it": (r"\b(tu|ti|tuo|tua|tuoi|tue)\b", r"\b(Lei|Suo|Sua|Suoi|Sue)\b"),
    "ru": (r"(?<![а-яё])(ты|тебя|тебе|твой|твоя|твоё|твои)(?![а-яё])", r"(?<![а-яё])(вы|вас|вам|ваш|ваша|ваше|ваши)(?![а-яё])"),
}
WORD = re.compile(r"[^\W\d_]{4,}")


def check(en: dict, de: dict, lang: str) -> tuple[dict[str, list[str]], list[dict]]:
    flags: dict[str, list[str]] = collections.defaultdict(list)
    de_words = collections.Counter()
    for k, v in de.items():
        if v != en.get(k):
            de_words.update(w.lower() for w in WORD.findall(PLACEHOLDER.sub(" ", v)))
    informal = None
    if lang in ADDRESS:
        inf, formal = (re.compile(x, re.I if lang != "it" else 0) for x in ADDRESS[lang])
        if lang == "de":
            formal = re.compile(ADDRESS["de"][1])          # "Sie" only with a capital S
        texts = [PLACEHOLDER.sub(" ", v) for v in de.values()]
        n_inf = sum(1 for t in texts if inf.search(t))
        n_formal = sum(1 for t in texts if formal.search(t))
        if n_formal > n_inf:
            informal = inf
    for k, e in en.items():
        d = de.get(k)
        if d is None:
            flags[k].append("missing")
            continue
        es, ds = PLACEHOLDER.sub(" ", e), PLACEHOLDER.sub(" ", d)
        letters = re.sub(r"[^A-Za-z]", "", es)
        if d == e and len(letters) >= 3:
            flags[k].append("english")
        if sorted(PLACEHOLDER.findall(e)) != sorted(PLACEHOLDER.findall(d)):
            flags[k].append("placeholder")
        if informal and informal.search(ds):
            flags[k].append("informal")
        if d != e and len(e) <= 30 and len(d) > max(len(e) * 1.6, len(e) + 8):
            flags[k].append("long")
        if d != e and letters.isupper() and len(letters) > 2 and re.search(r"[^\W\d_]", ds) and ds != ds.upper():
            flags[k].append("caps")
        if d != e:
            en_words = {w.lower() for w in WORD.findall(es)}
            left = [w for w in WORD.findall(ds) if w.lower() in en_words and w.lower() not in SHARED_WORDS
                    and w.isascii()]
            if left:
                flags[k].append("leftover:" + ",".join(dict.fromkeys(left)))
        if d.strip() != d and e.strip() == e or d.count("\n") != e.count("\n"):
            flags[k].append("spacing")

    # One short English term, several German ones.
    groups = collections.defaultdict(lambda: collections.defaultdict(list))
    for k, e in en.items():
        d = de.get(k)
        if not d or d == e:
            continue
        norm = re.sub(r"[\s:.!]+$", "", e.strip()).lower()
        if not norm or len(norm.split()) > 3 or PLACEHOLDER.search(norm) or not re.search(r"[a-z]", norm):
            continue
        groups[norm][re.sub(r"[\s:.!]+$", "", d.strip()).lower().replace("ß", "ss")].append(k)
    terms = []
    for norm, variants in groups.items():
        if len(variants) > 1:
            n = sum(len(v) for v in variants.values())
            terms.append({"en": norm, "n": n,
                          "variants": sorted(([de[ks[0]], ks] for ks in variants.values()),
                                             key=lambda x: -len(x[1]))})
            for ks in variants.values():
                for k in ks:
                    flags[k].append("terms")
    terms.sort(key=lambda t: -t["n"])
    return flags, terms


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--lang", default="de")
    ap.add_argument("--file", help="locale file to review (default: the game's own)")
    args = ap.parse_args()
    local = json.loads((REPO / "local.json").read_text(encoding="utf-8"))
    game = Path(local["game_path"])
    exe = game / "TeamPrincipal.exe"
    ensure_python(exe)
    locales = game / "ui" / "assets" / "locales"
    en = json.loads((locales / "en.json").read_text(encoding="utf-8-sig"))
    src = Path(args.file) if args.file else locales / f"{args.lang}.json"
    tr = json.loads(src.read_text(encoding="utf-8-sig"))
    game_tr = json.loads((locales / f"{args.lang}.json").read_text(encoding="utf-8-sig"))

    pyz = game_code.unpack(exe)
    hits = scan_code(pyz, en)
    flags, terms = check(en, tr, args.lang)

    places: list[list[str]] = []
    place_ix: dict[tuple, int] = {}
    rows = []
    for k in sorted(en, key=lambda k: k):
        locs = locate(k, hits.get(k, set()))
        ix = []
        for loc in locs:
            t = (loc["area"], loc["screen"], loc["part"], loc["module"], loc["how"])
            if t not in place_ix:
                place_ix[t] = len(places)
                places.append(list(t))
            ix.append(place_ix[t])
        note = []
        if k not in tr:
            note.append("new")
        elif game_tr.get(k) != tr[k]:
            note.append("changed")
        rows.append([k, en[k], tr.get(k, ""), ix, flags.get(k, []), note])

    digest = hashlib.sha1(src.read_bytes()).hexdigest()[:8]
    data = {
        "release": f"{args.lang}-{date.today().isoformat()}-{digest}",
        "lang": args.lang,
        "file": src.name,
        "source": "game" if not args.file else "file",
        "built": date.today().isoformat(),
        "game_build": game_code.build_id(exe),
        "places": places,
        "rows": rows,
        "terms": terms[:600],
        "located": sum(1 for r in rows if places[r[3][0]][4] != "guess"),
    }
    html = TEMPLATE.read_text(encoding="utf-8").replace(
        "/*DATA*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    # The data file for the team review site (tools/review_site): upload it on its admin page.
    site_json = OUT.parent / f"{data['release']}.json"
    site_json.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    c = collections.Counter(f.split(":")[0] for r in rows for f in r[4])
    print(f"{len(rows)} keys, {data['located']} located in code, {len(places)} places -> {OUT}")
    print("checks:", dict(c))
    print("term groups:", len(terms))
    print(f"review site data: {site_json}")


if __name__ == "__main__":
    main()
