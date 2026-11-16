"""In-game screenshots of every screen, with a box around each translated text.

Draws the game's screens with its own code, in one language, without
starting the game, and finds where every message of the locale file lands.
The pictures and boxes go to the translation review site (tools/review_site)
as screenshots, so reviewers see each text where the game shows it.

How the boxes are found: every screen is drawn twice, in two processes with
the same career and the same random seed. The first pass is the normal
picture. In the second, every text the game renders gets its own unique
colour (no anti-aliasing). Where a colour shows up in the second picture,
and not in the first, that text sits. The text is matched to its locale key
through the game's own lookups (ui.localization.tr and display_text), which
are wrapped to remember which key produced which string.

    python tools/screen_capture.py                 # German, all screens
    python tools/screen_capture.py --lang fr
    python tools/screen_capture.py --only Headquarters,Finance
    python tools/screen_capture.py --push http://127.0.0.1:8777 --user Admin

--push uploads to the review site (password from TP_REVIEW_PASSWORD or a
prompt) and replaces the pictures an earlier run uploaded for the same
screens and language. Without --push the results stay in
build/screens/<lang>/ (pictures and index.json).

Needs the Python the game was built with (private/sim-venv, see
tools/simulate.py). The game is never started and its folder never written:
build/screens/sandbox links to its ui/ and assets/ and copies the vanilla
pack (default26), and a fresh career with the first team is used.
"""
from __future__ import annotations

import argparse
import getpass
import http.cookiejar
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
import urllib.request
import uuid
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
VENV_PY = REPO / "private" / "sim-venv" / "Scripts" / "python.exe"
BUILD = REPO / "build" / "screens"
SANDBOX = BUILD / "sandbox"
PACK = "default26"
SIZE = (1920, 1080)
SEED = 7

# Screens opened with (manager, fonts, state) and nothing else. Screens that
# need a race weekend, an offer or a negotiation partner come later.
SIMPLE = [
    ("ui.screens.team_dashboard_screen", "TeamDashboardScreen"),
    ("ui.screens.headquarters_screen", "HeadquartersScreen"),
    ("ui.screens.finance_screen", "FinanceScreen"),
    ("ui.screens.budget_screen", "BudgetScreen"),
    ("ui.screens.mailbox_screen", "MailboxScreen"),
    ("ui.screens.schedule_screen", "ScheduleScreen"),
    ("ui.screens.standings_screen", "StandingsScreen"),
    ("ui.screens.standings_screen", "StandingsGraphScreen"),
    ("ui.screens.statistics_screen", "StatisticsScreen"),
    ("ui.screens.season_history_screen", "SeasonHistoryScreen"),
    ("ui.screens.regulations_screen", "RegulationsScreen"),
    ("ui.screens.development_screen", "DevelopmentScreen"),
    ("ui.screens.development_selection_screen", "DevelopmentSelectionScreen"),
    ("ui.screens.aerodynamics_screen", "AerodynamicsScreen"),
    ("ui.screens.engine_development_screen", "EngineDevelopmentScreen"),
    ("ui.screens.tyre_development_screen", "TyreDevelopmentScreen"),
    ("ui.screens.factory_screen", "FactoryScreen"),
    ("ui.screens.parts_warehouse_screen", "PartsWarehouseScreen"),
    ("ui.screens.performance_screen", "PerformanceScreen"),
    ("ui.screens.recon_screen", "ReconScreen"),
    ("ui.screens.academy_screen", "AcademyScreen"),
    ("ui.screens.driver_center_screen", "DriverCenterScreen"),
    ("ui.screens.driver_center_screen", "DriverAidDevelopmentScreen"),
    ("ui.screens.contracts_centre_screen", "ContractsCentreScreen"),
    ("ui.screens.driver_market_screen", "DriverMarketScreen"),
    ("ui.screens.staff_market_screen", "StaffMarketScreen"),
    ("ui.screens.sponsor_market_screen", "SponsorMarketScreen"),
    ("ui.screens.engine_market_screen", "EngineMarketScreen"),
    ("ui.screens.tyre_market_screen", "TyreMarketScreen"),
    ("ui.screens.parts_market_screen", "PartsMarketScreen"),
    ("ui.screens.team_lineup_screen", "TeamLineupScreen"),
    ("ui.screens.stock_market_screen", "StockMarketScreen"),
    ("ui.screens.valuation_history_screen", "ValuationHistoryScreen"),
    ("ui.screens.private_testing_screen", "PrivateTestingScreen"),
    ("ui.screens.options_screen", "OptionsScreen"),
    ("ui.screens.load_game_screen", "LoadGameScreen"),
    ("ui.screens.team_select_screen", "TeamSelectScreen"),
    ("ui.screens.team_principal_create_screen", "TeamPrincipalCreateScreen"),
    ("ui.screens.spectator_dashboard_screen", "SpectatorDashboardScreen"),
    ("ui.screens.season_review_screen", "SeasonReviewScreen"),
    ("ui.screens.test_screen", "TestScreen"),
]
# Screens opened with (manager, fonts) only.
BARE = [
    ("ui.screens.hub_screen", "HubScreen"),
    ("ui.screens.title_screen", "TitleScreen"),
    ("ui.screens.season_pack_screen", "SeasonPackScreen"),
    ("ui.screens.roster_editor_screen", "RosterEditorSelectScreen"),
    ("ui.screens.save_editor_screen", "SaveEditorSelectScreen"),
]


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def game_dir() -> Path:
    return Path(load_json(REPO / "local.json")["game_path"])


def ensure_python(exe: Path) -> None:
    import game_code
    want = game_code.exe_python_version(exe)
    if sys.version_info[:2] == want:
        return
    if not VENV_PY.exists():
        sys.exit(f"Needs Python {want[0]}.{want[1]} (the game's). Set it up as in tools/simulate.py.")
    sys.exit(subprocess.call([str(VENV_PY), "-I", __file__, *sys.argv[1:]]))


def make_sandbox() -> None:
    """A folder the game can treat as its install. Links to ui/ and assets/, copies the vanilla pack."""
    g = game_dir()
    (SANDBOX / "data").mkdir(parents=True, exist_ok=True)
    (SANDBOX / "saves").mkdir(exist_ok=True)
    if not (SANDBOX / "data" / PACK).exists():
        shutil.copytree(g / "data" / PACK, SANDBOX / "data" / PACK)
    for name in ("ui", "assets"):
        link = SANDBOX / name
        if not link.exists():
            if os.name == "nt":
                subprocess.check_call(["cmd", "/c", "mklink", "/J", str(link), str(g / name)],
                                      stdout=subprocess.DEVNULL)
            else:
                link.symlink_to(g / name)
    (SANDBOX / "active_pack.json").write_text(json.dumps({"active_pack": PACK}), encoding="utf-8")
    # Windowed at a fixed size, so the pictures don't depend on this PC's monitor.
    (SANDBOX / "display.json").write_text(json.dumps({
        "schema_version": 2, "display_mode": "windowed", "monitor": 0, "windowed_size": list(SIZE),
        "windowed_position": None, "windowed_maximized": False, "fullscreen_size": list(SIZE),
        "frame_limit": 60, "ui_scale": 1.0, "ui_font": "consolas", "color_pack": "blue",
        "reduce_blue_light": "off", "high_contrast": "off", "hide_control_hints": "off"}), encoding="utf-8")


# --- worker: draws every screen, in one of two modes ------------------------------------------


def id_colour(i: int) -> tuple[int, int, int]:
    """A unique colour per text id: an odd multiplier mod 2**24 is a bijection, and it spreads them."""
    c = ((i + 1) * 2654435761) % (1 << 24)
    return (c >> 16) & 255, (c >> 8) & 255, c & 255


def worker(mode: str, lang: str, out: Path, only: set[str]) -> None:
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    sys.dont_write_bytecode = True
    os.chdir(SANDBOX)          # the game writes logs (save_load_profiler.log) into the current folder
    import random
    import game_code
    exe = game_dir() / "TeamPrincipal.exe"
    game_code.install(exe, SANDBOX)
    game_code.load_pack_constants(SANDBOX, PACK)
    import pygame
    pygame.init()

    # 1. Remember which locale key produced which string. Patched before any
    #    screen module imports the functions by name.
    import ui.localization as loc
    loc.load_language(lang)
    en = load_json(SANDBOX / "ui" / "assets" / "locales" / "en.json")
    en_to_keys: dict[str, list[str]] = {}
    for k, v in en.items():
        if k.startswith("text."):
            en_to_keys.setdefault(v, []).append(k)
    made: dict[str, str] = {}          # shown string -> key, newest wins
    orig_tr, orig_display = loc.tr, loc.display_text

    def tr(key, *a, **kw):
        s = orig_tr(key, *a, **kw)
        if isinstance(s, str) and s.strip():
            made[s] = key
        return s

    def display_text(text, *a, **kw):
        s = orig_display(text, *a, **kw)
        if isinstance(text, str) and isinstance(s, str) and s.strip() and text in en_to_keys:
            made[s] = en_to_keys[text][0]
        return s

    loc.tr, loc.display_text = tr, display_text

    def key_for(text: str):
        """The key of a rendered piece of text: exact, case changed, a wrapped line, or cut short."""
        t = text.strip()
        if not t or not re.search(r"[^\W\d_]", t):
            return None
        if t in made:
            return made[t]
        low = t.casefold()
        for s, k in reversed(list(made.items())):
            if s.casefold() == low:
                return k
        cut = re.sub(r"(…|\.\.\.)$", "", t).strip()
        if len(cut) >= 4:
            for s, k in reversed(list(made.items())):
                sl = s.casefold()
                if len(cut) >= 6 and cut.casefold() in sl:      # one line of a wrapped text, or cut short
                    return k
        return None

    # 2. Every text the game renders goes through this font class.
    texts: list[dict] = []
    Base = pygame.font.Font

    class TrackedFont(Base):
        def render(self, text, antialias, color, background=None, *a, **kw):
            if not isinstance(text, str) or not text.strip():
                return Base.render(self, text, antialias, color, background, *a, **kw)
            i = len(texts)
            texts.append({"id": i, "text": text, "key": key_for(text)})
            if mode == "ids":
                return Base.render(self, text, False, id_colour(i), None, *a, **kw)
            return Base.render(self, text, antialias, color, background, *a, **kw)

    pygame.font.Font = TrackedFont
    import pygame.sysfont
    pygame.sysfont.Font = TrackedFont

    from ui.font_fallback import install_safe_sysfont
    install_safe_sysfont()
    from constants import SCREEN_WIDTH, SCREEN_HEIGHT
    from ui.display_manager import DisplayManager
    display = DisplayManager((SCREEN_WIDTH, SCREEN_HEIGHT), title="capture",
                             settings_path=str(SANDBOX / "display.json"), icon_path=str(SANDBOX / "ico.ico"))
    display.initialize(legacy_options_path=str(SANDBOX / "options.json"))
    from ui.responsive_layout import SHARED_FONTS
    fonts = (SHARED_FONTS.get(32, bold=True), SHARED_FONTS.get(22))
    from ui.screen_manager import ScreenManager
    from ui.screens.hub_screen import HubScreen
    manager = ScreenManager(HubScreen(None, fonts), display_manager=display)
    manager.current.manager = manager

    random.seed(SEED)
    from game_state import GameState
    save = SANDBOX / "saves" / "capture.json"
    if save.exists():
        save.unlink()
    state = GameState(str(SANDBOX / "data" / PACK), save_path=str(save))
    state.reset_season()
    teams = list(state.teams.keys()) if isinstance(state.teams, dict) else [t.get("name") for t in state.teams]
    state.player_team = teams[0]
    state.spectator_mode = False

    import importlib
    out.mkdir(parents=True, exist_ok=True)
    report = {}
    specs = [(m, c, True) for m, c in SIMPLE] + [(m, c, False) for m, c in BARE]
    for module, cls_name, with_state in specs:
        short = cls_name.removesuffix("Screen")
        if only and short not in only and cls_name not in only:
            continue
        random.seed(SEED)
        first = len(texts)
        try:
            cls = getattr(importlib.import_module(module), cls_name)
            screen = cls(manager, fonts, state) if with_state else cls(manager, fonts)
            manager.switch_to(screen)
            canvas = pygame.Surface(manager.render_size)
            for _ in range(3):          # a few frames, so layouts and caches settle
                cur = manager.current
                try:
                    cur.update(0.016)
                except TypeError:
                    cur.update()
                canvas.fill((0, 0, 0))
                manager.draw(canvas)
            pygame.image.save(canvas, str(out / f"{cls_name}.png"))
            report[cls_name] = {"ok": True, "texts": [first, len(texts)], "size": list(canvas.get_size()),
                                "module": module}
            print(f"{mode}: {cls_name} {canvas.get_size()} texts {len(texts) - first}", flush=True)
        except Exception as err:
            report[cls_name] = {"ok": False, "error": f"{type(err).__name__}: {err}", "module": module}
            print(f"{mode}: {cls_name} failed: {type(err).__name__}: {err}", flush=True)
            traceback.print_exc(limit=3)
    (out / "texts.json").write_text(json.dumps(texts, ensure_ascii=False), encoding="utf-8")
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")


# --- analysis: where each text landed -----------------------------------------------------------


def largest_block(rects):
    """Join glyph pieces that sit close together (letters, words, lines) and return the biggest block."""
    if not rects:
        return None
    blocks = [r.copy() for r in rects]
    merged = True
    while merged:
        merged = False
        out = []
        for r in blocks:
            for o in out:
                lh = max(6, min(r.h, o.h))
                if r.inflate(lh * 2, lh).colliderect(o.inflate(lh * 2, lh)):
                    o.union_ip(r)
                    merged = True
                    break
            else:
                out.append(r)
        blocks = out
    return max(blocks, key=lambda b: b.w * b.h)


def find_boxes(lang: str) -> dict:
    import pygame
    norm_dir, ids_dir = BUILD / lang / "normal", BUILD / lang / "ids"
    texts = load_json(ids_dir / "texts.json")
    rep_n, rep_i = load_json(norm_dir / "report.json"), load_json(ids_dir / "report.json")
    by_colour = {id_colour(t["id"]): t for t in texts if t.get("key")}
    index = {}
    for name, r in rep_i.items():
        if not r.get("ok") or not rep_n.get(name, {}).get("ok"):
            continue
        ids_img = pygame.image.load(str(ids_dir / f"{name}.png"))
        norm_img = pygame.image.load(str(norm_dir / f"{name}.png"))
        if ids_img.get_size() != norm_img.get_size():
            print(f"{name}: the two passes differ in size, skipped")
            continue
        w, h = ids_img.get_size()
        raw = pygame.image.tobytes(ids_img, "RGB")
        present = set(zip(raw[0::3], raw[1::3], raw[2::3])) & by_colour.keys()
        # Glyph pieces per key. One key can be several render calls (the lines of a
        # wrapped text) and one render call can be drawn in several places (a cached label).
        pieces: dict[str, list] = {}
        sample: dict[str, str] = {}
        for colour in present:
            t = by_colour[colour]
            m = pygame.mask.from_threshold(ids_img, colour, (1, 1, 1, 255))
            m.erase(pygame.mask.from_threshold(norm_img, colour, (1, 1, 1, 255)), (0, 0))
            rects = [r for r in m.get_bounding_rects() if r.w * r.h >= 2]
            pieces.setdefault(t["key"], []).extend(rects)
            sample.setdefault(t["key"], t["text"])
        links = {}
        for key, rects in pieces.items():
            box = largest_block(rects)
            if box is None or (box.w > w * 0.9 and box.h > h * 0.5):    # a stray colour all over the picture
                continue
            box = box.inflate(6, 6).clip(pygame.Rect(0, 0, w, h))
            links[key] = {"key": key, "x": box.x / w, "y": box.y / h, "w": box.w / w, "h": box.h / h,
                          "text": sample[key]}
        index[name] = {"file": f"normal/{name}.png", "module": r["module"], "size": [w, h],
                       "links": sorted(links.values(), key=lambda l: (l["y"], l["x"]))}
        print(f"{name}: {len(links)} messages placed")
    (BUILD / lang / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    return index


# --- push to the review site ------------------------------------------------------------------


class Site:
    def __init__(self, base: str, lang: str):
        self.base, self.lang = base.rstrip("/"), lang
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        html = self.op.open(self.base + "/").read().decode("utf-8")
        boot = re.search(r'<script id="boot" type="application/json">(.*?)</script>', html, re.S)
        self.csrf = json.loads(boot.group(1))["csrf"]

    def call(self, action, body=None, files=None):
        url = f"{self.base}/api.php?a={action}&l={self.lang}"
        headers = {"X-CSRF": self.csrf}
        data = None
        if files:
            bnd = uuid.uuid4().hex
            parts = [f'--{bnd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
                     for k, v in (body or {}).items()]
            for k, (fn, content, ct) in files.items():
                parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="{k}"; filename="{fn}"\r\n'
                             f'Content-Type: {ct}\r\n\r\n'.encode() + content + b"\r\n")
            parts.append(f"--{bnd}--\r\n".encode())
            data, headers["Content-Type"] = b"".join(parts), f"multipart/form-data; boundary={bnd}"
        elif body is not None:
            data, headers["Content-Type"] = json.dumps(body).encode(), "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data is not None else "GET")
        try:
            res = json.loads(self.op.open(req).read().decode("utf-8") or "{}")
        except urllib.error.HTTPError as e:
            res = json.loads(e.read().decode("utf-8") or "{}")
        if res.get("error"):
            raise RuntimeError(f"{action}: {res['error']}")
        if "csrf" in res:
            self.csrf = res["csrf"]
        return res


def push(lang: str, index: dict, base: str, user: str) -> None:
    pw = os.environ.get("TP_REVIEW_PASSWORD") or getpass.getpass(f"Password for {user} on {base}: ")
    site = Site(base, lang)
    site.call("login", {"name": user, "password": pw})
    state = site.call("state")
    data_keys = None
    # Earlier automatic pictures of these screens in this language are replaced.
    for sh in state["shots"]:
        cap = sh.get("caption") or ""
        if cap.startswith("auto:") and sh["lang"] == lang and cap[5:] in index:
            site.call("shot_delete", {"id": sh["id"]})
    for name, entry in index.items():
        if not entry["links"]:
            continue
        img = (BUILD / lang / entry["file"]).read_bytes()
        screen = name.removesuffix("Screen")
        up = site.call("shot_upload", {"area": "", "screen": screen, "caption": f"auto:{name}", "shot_lang": lang},
                       files={"file": (f"{name}.png", img, "image/png")})
        ok = 0
        for l in entry["links"]:
            try:
                site.call("shot_link", {"shot_id": up["id"], "key": l["key"], "x": l["x"], "y": l["y"], "w": l["w"], "h": l["h"]})
                ok += 1
            except RuntimeError:
                pass        # a key the site's game file doesn't have
        print(f"pushed {name}: {ok} of {len(entry['links'])} messages", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--lang", default="de")
    ap.add_argument("--only", help="comma list of screens, e.g. Headquarters,Finance")
    ap.add_argument("--push", help="review site address, e.g. https://example.com/translation-review")
    ap.add_argument("--user", default="Admin", help="site account for --push (a lead or admin)")
    ap.add_argument("--worker", choices=["normal", "ids"], help=argparse.SUPPRESS)
    ap.add_argument("--skip-capture", action="store_true", help="only analyse and push an earlier capture")
    args = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    exe = game_dir() / "TeamPrincipal.exe"
    ensure_python(exe)
    only = {s.strip() for s in (args.only or "").split(",") if s.strip()}
    if args.worker:
        return worker(args.worker, args.lang, BUILD / args.lang / args.worker, only)
    if not args.skip_capture:
        import game_code
        game_code.unpack(exe)
        make_sandbox()
        for mode in ("normal", "ids"):
            t = time.time()
            cmd = [sys.executable, "-I", __file__, "--worker", mode, "--lang", args.lang]
            if args.only:
                cmd += ["--only", args.only]
            if subprocess.call(cmd) != 0:
                sys.exit(f"the {mode} pass failed")
            print(f"{mode} pass: {time.time() - t:.0f} s", flush=True)
    index = find_boxes(args.lang)
    n = sum(len(e["links"]) for e in index.values())
    keys = {l["key"] for e in index.values() for l in e["links"]}
    print(f"{len(index)} screens, {n} boxes, {len(keys)} different messages -> {BUILD / args.lang / 'index.json'}")
    if args.push:
        push(args.lang, index, args.push, args.user)


if __name__ == "__main__":
    main()
