"""In-game screenshots of every screen, with a box around each translated text.

Draws the game's screens with its own code, in one language, without
starting the game, and finds where every message of the locale file lands.
The pictures and boxes go to the translation review site (tools/review_site)
as screenshots, so reviewers see each text where the game shows it.

How the boxes are found: every screen is drawn twice. The first time is the
normal picture. In the second, every text the game renders gets its own unique
colour (no anti-aliasing). Where a colour shows up in the second picture,
and not in the first, that text sits. Both pictures come from one process
at the same moment (text surfaces are repainted and caches rebuilt for the
second), so a race weekend simulating in the background matches too. The text is matched to its locale key
through the game's own lookups (ui.localization.tr and display_text), which
are wrapped to remember which key produced which string.

    python tools/screen_capture.py                 # German, all screens
    python tools/screen_capture.py --lang fr
    python tools/screen_capture.py --only Headquarters,Finance
    python tools/screen_capture.py --weekend-only       # practice to race results
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

# Screens opened with (manager, fonts, state) and nothing else. The race
# weekend's screens are walked through from the dashboard (walk_weekend), and
# each market opens its first entry (the negotiation screens). Mails and news
# are left out on purpose: they are full sentences that read fine without a picture.
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


# --- worker: draws every screen twice, normal and with every text in its own colour --------------


def id_colour(i: int) -> tuple[int, int, int]:
    """A unique colour per text id: an odd multiplier mod 2**24 is a bijection, and it spreads them."""
    c = ((i + 1) * 2654435761) % (1 << 24)
    return (c >> 16) & 255, (c >> 8) & 255, c & 255


def worker(lang: str, only: set[str], weekend: bool, static: bool) -> None:
    """Both pictures of a screen come from one process at one moment, so a running
    simulation (race weekends) can't change between them. For the coloured picture
    every text surface still alive is repainted in its colour, new texts are
    rendered in theirs, and the screen's cached panels are rebuilt."""
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    sys.dont_write_bytecode = True
    os.chdir(SANDBOX)          # the game writes logs (save_load_profiler.log) into the current folder
    import functools
    import gc
    import random
    import weakref
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
            made.pop(s, None)
            made[s] = key
        return s

    def display_text(text, *a, **kw):
        s = orig_display(text, *a, **kw)
        if isinstance(text, str) and isinstance(s, str) and s.strip() and text in en_to_keys:
            made.pop(s, None)
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
        recent = list(made.items())[-4000:]
        for s, k in reversed(recent):
            if s.casefold() == low:
                return k
        cut = re.sub(r"(…|\.\.\.)$", "", t).strip()
        if len(cut) >= 6:
            for s, k in reversed(recent):
                if cut.casefold() in s.casefold():      # one line of a wrapped text, or cut short
                    return k
        return None

    # 2. Every text the game renders goes through this font class, and comes back
    #    as a Tagged surface that can be repainted in its colour and back. A partial
    #    run (--only, --weekend-only) keeps the earlier pictures, so ids continue
    #    after the earlier run's texts.
    normal_dir, ids_dir = BUILD / lang / "normal", BUILD / lang / "ids"
    normal_dir.mkdir(parents=True, exist_ok=True)
    ids_dir.mkdir(parents=True, exist_ok=True)
    report_path = ids_dir / "report.json"
    partial = bool(only) or not (weekend and static)
    report = load_json(report_path) if partial and report_path.exists() else {}
    texts: list[dict] = load_json(ids_dir / "texts.json") if partial and (ids_dir / "texts.json").exists() else []
    Base = pygame.font.Font
    live: "weakref.WeakSet" = weakref.WeakSet()
    colour_mode = [False]

    class Tagged(pygame.Surface):
        pass

    def tagged_copy(src, size):
        t = Tagged(size, pygame.SRCALPHA)
        t.blit(src, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return t

    def paint(t, src):
        t.fill((0, 0, 0, 0))
        t.blit(src, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    class TrackedFont(Base):
        def render(self, text, antialias, color, background=None, *a, **kw):
            normal = Base.render(self, text, antialias, color, background, *a, **kw)
            if not isinstance(text, str) or not text.strip():
                return normal
            i = len(texts)
            texts.append({"id": i, "text": text, "key": key_for(text)})
            coloured = Base.render(self, text, False, id_colour(i), None, *a, **kw)
            t = tagged_copy(coloured if colour_mode[0] else normal, normal.get_size())
            t._normal, t._coloured = normal, coloured
            live.add(t)
            return t

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

    def clear_caches():
        """Forget rendered panels, so the next drawing renders its texts again."""
        try:
            manager._clear_frames()
        except Exception:
            pass
        from ui.render_cache import BoundedSurfaceCache
        for o in gc.get_objects():
            try:
                if isinstance(o, BoundedSurfaceCache):
                    o.clear()
                elif isinstance(o, functools._lru_cache_wrapper) and getattr(o, "__module__", "").startswith("ui"):
                    o.cache_clear()
            except Exception:
                pass
        try:      # what a window resize does: screens rebuild fonts and cached panels
            manager.apply_resize(manager._window_size, manager._viewport, manager._scale, notify_screen=True)
        except Exception:
            try:
                manager.current.on_resize(manager._window_size, manager._viewport, manager._scale)
            except Exception:
                pass

    def draw():
        canvas = pygame.Surface(manager.render_size)
        canvas.fill((0, 0, 0))
        manager.draw(canvas)
        return canvas

    def step(screen, frames=2):
        for _ in range(frames):
            try:
                screen.update(0.016)
            except TypeError:
                screen.update()

    seen: set[str] = set()       # messages already in a picture of this run

    def keys_between(a, b):
        return {t["key"] for t in texts[a:b] if t.get("key")}

    def shown_keys() -> set[str]:
        """The messages the current screen shows right now (drawn once, nothing saved)."""
        first = len(texts)
        clear_caches()
        draw()
        return keys_between(first, len(texts))

    def capture(name: str, module: str):
        first = len(texts)
        step(manager.current)
        clear_caches()
        normal = draw()
        seen.update(keys_between(first, len(texts)))
        colour_mode[0] = True
        for t in list(live):
            paint(t, t._coloured)
        clear_caches()
        coloured = draw()
        colour_mode[0] = False
        for t in list(live):
            paint(t, t._normal)
        clear_caches()
        pygame.image.save(normal, str(normal_dir / f"{name}.png"))
        pygame.image.save(coloured, str(ids_dir / f"{name}.png"))
        report[name] = {"ok": True, "module": module, "size": list(normal.get_size()), "texts": [first, len(texts)]}
        print(f"{name}: {len(texts) - first} texts", flush=True)

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

    def tab_rects(screen) -> list:
        """Every tab button the screen keeps: attributes named *tab* holding rectangles."""
        found = []
        for name, v in sorted(vars(screen).items()):
            if "tab" not in name.lower() or "table" in name.lower():
                continue
            items = v.values() if isinstance(v, dict) else v if isinstance(v, (list, tuple)) else []
            for i, x in enumerate(list(items)[:14]):
                r = x if isinstance(x, pygame.Rect) else next(
                    (y for y in (x.values() if isinstance(x, dict) else x if isinstance(x, (list, tuple)) else [])
                     if isinstance(y, pygame.Rect)), None)
                if r is not None and r.w > 8 and r.h > 8:
                    found.append((name, i))
        return found[:24]

    def rect_of(screen, name, i):
        v = getattr(screen, name, None)
        items = list(v.values() if isinstance(v, dict) else v or [])
        if i >= len(items):
            return None
        x = items[i]
        if isinstance(x, pygame.Rect):
            return x
        vals = x.values() if isinstance(x, dict) else x if isinstance(x, (list, tuple)) else []
        return next((y for y in vals if isinstance(y, pygame.Rect)), None)

    def click_at(screen, pos):
        for kind in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            screen.handle_event(pygame.event.Event(kind, pos=pos, button=1))

    def explore_tabs(make, base: str, module: str):
        """Click each tab on a fresh copy of the screen; keep the picture if it shows new messages."""
        n = 0
        for attr, i in tab_rects(manager.current):
            try:
                screen = make()
                manager.switch_to(screen)
                step(screen, 2)
                draw()
                r = rect_of(screen, attr, i)
                if r is None:
                    continue
                click_at(screen, r.center)
                if manager.current is not screen:
                    continue          # the click left the screen: not a tab
                step(screen, 2)
                new = shown_keys() - seen
                if len(new) >= 2:
                    n += 1
                    capture(f"{base}#tab{n}", module)
            except Exception as err:
                print(f"{base} tab {attr}[{i}]: {type(err).__name__}: {err}", flush=True)

    # Markets: open the first entry, which shows its negotiation screen.
    follow = {
        "DriverMarketScreen": lambda s: s._open_driver_profile_at((300, 262)),
        "StaffMarketScreen": lambda s: s._open_staff_profile_at((300, 262)),
        "EngineMarketScreen": lambda s: click_at(s, s.card_rects[min(1, len(s.card_rects) - 1)].center),
        "TyreMarketScreen": lambda s: click_at(s, s.card_rects[0].center),
        "PartsMarketScreen": lambda s: click_at(s, s.card_rects[0].center),
    }

    def follow_market(make, base: str):
        if base not in follow:
            return
        screen = make()
        manager.switch_to(screen)
        step(screen, 2)
        draw()
        try:
            follow[base](screen)
        except Exception as err:
            print(f"{base}: opening an entry failed: {type(err).__name__}: {err}", flush=True)
            return
        opened = manager.current
        if opened is screen:
            print(f"{base}: the first entry opened nothing", flush=True)
            return
        name = type(opened).__name__
        step(opened, 3)
        capture(name, type(opened).__module__)
        explore_tabs(lambda: opened, name, type(opened).__module__)

    import importlib
    if static:
        specs = [(m, c, True) for m, c in SIMPLE] + [(m, c, False) for m, c in BARE]
        for module, cls_name, with_state in specs:
            short = cls_name.removesuffix("Screen")
            if only and short not in only and cls_name not in only:
                continue
            random.seed(SEED)
            try:
                cls = getattr(importlib.import_module(module), cls_name)
                screen = cls(manager, fonts, state) if with_state else cls(manager, fonts)
                manager.switch_to(screen)
                step(screen, 3)
                capture(cls_name, module)
                make = (lambda c=cls, w=with_state: c(manager, fonts, state) if w else c(manager, fonts))
                explore_tabs(make, cls_name, module)
                follow_market(make, cls_name)
            except Exception as err:
                report[cls_name] = {"ok": False, "error": f"{type(err).__name__}: {err}", "module": module}
                print(f"{cls_name} failed: {type(err).__name__}: {err}", flush=True)
                traceback.print_exc(limit=3)
    if weekend:
        try:
            walk_weekend(state, manager, fonts, capture, step, pygame)
        except Exception as err:
            print(f"weekend stopped: {type(err).__name__}: {err}", flush=True)
            traceback.print_exc(limit=5)
    (ids_dir / "texts.json").write_text(json.dumps(texts, ensure_ascii=False), encoding="utf-8")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    (normal_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")


# How the player leaves each screen of a race weekend: simulate every session.
def press(pygame, screen, key):
    screen.handle_event(pygame.event.Event(pygame.KEYDOWN, key=key, mod=0, unicode="", scancode=0))


def click(pygame, screen, rect):
    pos = rect.center
    for kind in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
        screen.handle_event(pygame.event.Event(kind, pos=pos, button=1))


def teams_first(state):
    return next(iter(state.teams)) if isinstance(state.teams, dict) else state.teams[0].get("name")


def walk_weekend(state, manager, fonts, capture, step, pygame) -> None:
    """Jump to the first race, start it from the dashboard and capture every screen until it ends."""
    from ui.screens.team_dashboard_screen import TeamDashboardScreen
    tracks = SANDBOX / "data" / PACK / "tracks"
    races = [w for w in range(state.week_index, len(state.schedule))      # not "private" or "test" weeks
             if isinstance(state.schedule[w], str) and (tracks / f"{state.schedule[w]}.json").exists()]
    if not races:
        raise RuntimeError("no race on the schedule")
    state.week_index = races[0]
    state.player_team, state.spectator_mode = state.player_team or teams_first(state), False
    print(f"weekend: week {races[0]}, {state.schedule[races[0]]}", flush=True)
    dash = TeamDashboardScreen(manager, fonts, state)
    manager.switch_to(dash)
    # A fresh career has mails waiting for an answer, which would stop the week.
    # Only for this capture: no mailbox check and no pop-ups on this dashboard.
    dash._pending_mailbox_action_required = lambda *a, **k: False
    for name in ("_maybe_prompt_team_switch", "_maybe_prompt_buyout", "_maybe_prompt_driver_proposal",
                 "_maybe_prompt_engine_naming", "_open_pending_regulation_vote"):
        setattr(dash, name, lambda *a, **k: False)
    done: set[str] = set()
    # The player picks the weekend's tyre sets first (through a mail): capture that
    # screen, then confirm the recommended sets as its Confirm button does.
    weekend = state.get_or_create_race_weekend(state.schedule[state.week_index])
    tyres = getattr(state, "formula_weekend_tyre_manager", None)
    if tyres is not None and tyres.enabled() and tyres.player_allocation_pending(weekend):
        from ui.screens.tyre_allocation_screen import TyreAllocationScreen
        alloc = TyreAllocationScreen(manager, fonts, state, weekend)
        manager.switch_to(alloc)
        step(alloc, 3)
        capture("TyreAllocationScreen", type(alloc).__module__)
        done.add("TyreAllocationScreen")
        alloc._confirm()
        manager.switch_to(dash)
    dash._handle_next_action()
    leave = {
        "PracticeResultsScreen": lambda s: s._continue_to_qualifying(),
        "QualifyingScreen": lambda s: s._continue_to_grid(),
        "GridScreen": lambda s: s._continue_to_race(),
        "ResultsScreen": lambda s: s._finish_and_return(),
    }
    seen = []
    deadline = time.time() + 1800
    while time.time() < deadline:
        s = manager.current
        name = type(s).__name__
        if s is dash or name.endswith("DashboardScreen") or (seen and seen[-1] == "ResultsScreen" and name != "ResultsScreen"):
            break         # the weekend is over once the results are left
        if not seen or seen[-1] != name:
            seen.append(name)
        if name.startswith("Simulating") or name.startswith("Loading"):
            if name not in done:
                step(s, 20)
                time.sleep(0.5)
                if manager.current is s:
                    capture(name, type(s).__module__)
                    done.add(name)
            step(s, 1)
            time.sleep(0.02)
            continue
        if name not in done:
            step(s, 3)
            capture(name, type(s).__module__)
            done.add(name)
        if name in leave:
            leave[name](s)
        else:
            press(pygame, s, pygame.K_s)
            if manager.current is s and getattr(s, "sim_rect", None) is not None:
                click(pygame, s, s.sim_rect)
        if manager.current is s:
            raise RuntimeError(f"{name} did not move on (after {' > '.join(seen)})")
    print("weekend: " + " > ".join(seen), flush=True)


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
        base, _, variant = name.partition("#")
        screen = base.removesuffix("Screen")
        m = re.fullmatch(r"(tab|mail)(\d+)", variant)
        if m:
            screen += f" ({m.group(1)} {m.group(2)})"
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
    ap.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--skip-capture", action="store_true", help="only analyse and push an earlier capture")
    ap.add_argument("--no-weekend", action="store_true", help="skip the race weekend (much faster)")
    ap.add_argument("--weekend-only", action="store_true", help="only the race weekend screens")
    args = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    exe = game_dir() / "TeamPrincipal.exe"
    ensure_python(exe)
    only = {s.strip() for s in (args.only or "").split(",") if s.strip()}
    weekend, static = not args.no_weekend and not only, not args.weekend_only
    if args.worker:
        return worker(args.lang, only, weekend, static)
    if not args.skip_capture:
        import game_code
        game_code.unpack(exe)
        make_sandbox()
        t = time.time()
        cmd = [sys.executable, "-I", __file__, "--worker", "--lang", args.lang]
        cmd += ["--only", args.only] if args.only else []
        cmd += ["--no-weekend"] if args.no_weekend else []
        cmd += ["--weekend-only"] if args.weekend_only else []
        if subprocess.call(cmd) != 0:
            sys.exit("the capture failed")
        print(f"capture: {time.time() - t:.0f} s", flush=True)
    index = find_boxes(args.lang)
    n = sum(len(e["links"]) for e in index.values())
    keys = {l["key"] for e in index.values() for l in e["links"]}
    print(f"{len(index)} screens, {n} boxes, {len(keys)} different messages -> {BUILD / args.lang / 'index.json'}")
    if args.push:
        push(args.lang, index, args.push, args.user)


if __name__ == "__main__":
    main()
