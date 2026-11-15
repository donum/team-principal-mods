"""Simulate whole seasons with the game's own code, without starting the game.

Runs the real game logic (week advance, AI management, practice,
qualifying, race, scoring) in spectator mode, the same path the game
takes when you pick "Spectator" and press next. Every run gets its own
sandbox folder, so the game install is never written to. The results
are the game's own saves, plus a report against the real results in
<season>/research/results/.

Setup (once): a Python 3.13 venv with pygame 2.6.1, the versions the
game is built with:

    py -V:3.13 -m venv private/sim-venv
    private/sim-venv/Scripts/python -m pip install pygame==2.6.1

Usage:
    python tools/build_pack.py seasons/dtm-2013          # sims use dist/<pack>
    python tools/simulate.py dtm-2013                    # one season, new career
    python tools/simulate.py dtm-2013 --runs 6           # six seasons side by side
    python tools/simulate.py dtm-2013 --seasons 3        # three seasons in one career
    python tools/simulate.py dtm-2013 --save my.json     # continue from a save
    python tools/simulate.py dtm-2013 --installed        # the installed pack, not dist/
    python tools/simulate.py --report build/sim/dtm-2013/<stamp>

A season takes about 40 minutes per run (a race weekend about 3).
"""

import argparse
import csv
import json
import os
import random
import shutil
import statistics
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
VENV_PY = REPO / "private" / "sim-venv" / "Scripts" / "python.exe"


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def game_dir():
    local = REPO / "local.json"
    if local.exists():
        return Path(load_json(local)["game_path"])
    return Path(r"C:\Program Files (x86)\Steam\steamapps\common\Team Principal A Racing Manager")


# --------------------------------------------------------------------------
# Orchestrator


def make_sandbox(root, pack, source, save):
    """A folder the game can treat as its install: active_pack.json, data/<pack>, saves/."""
    data = root / "data" / pack
    shutil.copytree(source, data, ignore=shutil.ignore_patterns("assets"))
    (root / "saves").mkdir(parents=True, exist_ok=True)
    (root / "active_pack.json").write_text(json.dumps({"active_pack": pack}), encoding="utf-8")
    if save:
        shutil.copy2(save, root / "saves" / "start.json")


def launch(args):
    season_dir = REPO / "seasons" / args.season
    pack = load_json(season_dir / "season.json")["pack_folder"]
    source = game_dir() / "data" / pack if args.installed else REPO / "dist" / pack
    if not source.exists():
        sys.exit(f"{source} not found (run tools/build_pack.py first, or pass --installed)")
    if not VENV_PY.exists():
        sys.exit("no simulator venv yet; create it once with:\n"
                 "    py -V:3.13 -m venv private/sim-venv\n"
                 "    private/sim-venv/Scripts/python -m pip install pygame==2.6.1")
    out = Path(args.out) if args.out else REPO / "build" / "sim" / args.season / time.strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True, exist_ok=True)
    # Unpack a new game build once, here: parallel workers unpacking it at the
    # same time collide on the shared pyz.partial folder (2026-11-15, build 45440200).
    import game_code
    game_code.unpack(game_dir() / "TeamPrincipal.exe")
    seed0 = args.seed if args.seed is not None else random.randrange(1_000_000)
    meta = {"season": args.season, "pack": pack, "source": str(source), "seasons": args.seasons,
            "runs": args.runs, "seed": seed0, "save": str(args.save) if args.save else None}
    (out / "sim.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    pending = []
    for i in range(args.runs):
        run = out / f"run-{i + 1:02d}"
        make_sandbox(run, pack, source, args.save)
        pending.append((run, seed0 + i))
    jobs = args.jobs or min(args.runs, max(1, (os.cpu_count() or 2) // 2))
    print(f"{args.runs} run(s) of {args.seasons} season(s) from {source}, {jobs} at a time -> {out}", flush=True)
    running = []
    start = time.time()
    while pending or running:
        while pending and len(running) < jobs:
            run, seed = pending.pop(0)
            cmd = [str(VENV_PY), "-I", str(Path(__file__).resolve()), "--worker", str(run),
                   "--seasons", str(args.seasons), "--seed", str(seed), "--exe", str(game_dir() / "TeamPrincipal.exe")]
            log = open(run / "log.txt", "w", encoding="utf-8")
            running.append((run, subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT), log))
        time.sleep(5)
        for item in list(running):
            run, proc, log = item
            if proc.poll() is not None:
                log.close()
                running.remove(item)
                status = "done" if proc.returncode == 0 else f"failed ({proc.returncode}), see {run / 'log.txt'}"
                print(f"{run.name} {status} after {(time.time() - start) / 60:.0f} min", flush=True)
    report(out, season_dir)


# --------------------------------------------------------------------------
# Worker: drives the game's screens with a stub screen manager.


def worker(args):
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    sys.dont_write_bytecode = True
    sandbox = Path(args.worker).resolve()
    import game_code
    game_code.install(args.exe, sandbox)
    pack_constants = game_code.load_pack_constants(sandbox, load_json(sandbox / "active_pack.json")["active_pack"])
    print(f"constants: SEASON_START_YEAR {getattr(pack_constants, 'SEASON_START_YEAR', '?')}", flush=True)
    random.seed(args.seed)
    import pygame
    pygame.init()
    pygame.display.set_mode((1280, 720))
    fonts = (pygame.font.Font(None, 32), pygame.font.Font(None, 20))

    from game_state import GameState
    import ui.base_screen as base_screen
    from ui.screens.spectator_dashboard_screen import SpectatorDashboardScreen

    dashboard = object()

    class Manager:
        """Stands in for the game's ScreenManager: only remembers the current screen."""

        def __init__(self):
            self.current = None

        def switch_to(self, screen, *a, **k):
            self.current = screen

        def __getattr__(self, name):
            return lambda *a, **k: None

    def to_dashboard(self, state, *a, **k):
        self.manager.switch_to(dashboard)

    base_screen.BaseScreen.go_to_team_dashboard = to_dashboard

    def press(screen, key):
        screen.handle_event(pygame.event.Event(pygame.KEYDOWN, key=key, mod=0, unicode="", scancode=0))

    # How a player in spectator mode leaves each screen of a weekend.
    leave = {
        "PracticeChoiceScreen": lambda s: press(s, pygame.K_s),
        "TestingChoiceScreen": lambda s: press(s, pygame.K_s),
        "PreQualifyingChoiceScreen": lambda s: press(s, pygame.K_s),
        "QualifyingChoiceScreen": lambda s: press(s, pygame.K_s),
        "RaceChoiceScreen": lambda s: press(s, pygame.K_s),
        "PracticeResultsScreen": lambda s: s._continue_to_qualifying(),
        "QualifyingScreen": lambda s: s._continue_to_grid(),
        "GridScreen": lambda s: s._continue_to_race(),
        "ResultsScreen": lambda s: s._finish_and_return(),
    }

    mgr = Manager()

    def next_week(state):
        """The spectator dashboard's "next" button, then every screen until it returns."""
        mgr.current = None
        SpectatorDashboardScreen(mgr, fonts, state)._handle_next_action()
        seen = []
        while mgr.current is not None and mgr.current is not dashboard:
            s = mgr.current
            name = type(s).__name__
            if not seen or seen[-1] != name:
                seen.append(name)
            if name.startswith("Simulating"):
                try:
                    s.update(0.05)
                except TypeError:
                    s.update()
                if mgr.current is s:
                    err = getattr(s, "_worker_error_text", lambda: None)()
                    if err:
                        raise RuntimeError(f"{name}: {err}")
                    time.sleep(0.02)
                continue
            if name not in leave:
                raise RuntimeError(f"no headless way out of {name} (after {' > '.join(seen)})")
            leave[name](s)
            if mgr.current is s:
                raise RuntimeError(f"{name} did not move on (after {' > '.join(seen)})")
        return seen

    pack = load_json(sandbox / "active_pack.json")["active_pack"]
    start = sandbox / "saves" / "start.json"
    if start.exists():
        state = GameState(str(sandbox / "data" / pack), save_path=str(start))
        state.load_season()
    else:  # a new career, as the hub's "new game" and the team screen's "Spectator" do it
        state = GameState(str(sandbox / "data" / pack), save_path=str(sandbox / "saves" / "career.json"))
        state.reset_season()
    state.player_team = None
    state.spectator_mode = True
    state.save_season()

    races = open(sandbox / "races.jsonl", "a", encoding="utf-8")
    standings = open(sandbox / "standings.jsonl", "a", encoding="utf-8")
    # The cars as they raced: one line per race with every team's ratings,
    # so the report can show how the pecking order moves over a season.
    cars = open(sandbox / "cars.jsonl", "a", encoding="utf-8")

    def car_snapshot(race):
        out = {}
        teams = state.teams.items() if isinstance(state.teams, dict) else ((t.get("name"), t) for t in state.teams)
        for name, t in teams:
            if not isinstance(t, dict) or not t.get("active", True):
                continue
            row = {k: t.get(k) for k in ("team_pace", "braking", "acceleration", "tyre_management", "chassis_reliability")}
            row.update({f"attr_{k}": v for k, v in (t.get("attr") or {}).items()})
            out[name] = {k: round(float(v), 2) for k, v in row.items() if isinstance(v, (int, float))}
        return {"season": race.get("season"), "week": race.get("week"), "track": race.get("track"), "teams": out}
    first_season = state.season_no
    seen_events = {r.get("event_id") for r in state.race_results}
    while state.season_no < first_season + args.seasons:
        season = state.season_no
        snapshot = {"season": season, "drivers": dict(state.drivers_points),
                    "teams": dict(state.constructors_points)}
        t = time.time()
        week = state.week_index
        track = state.schedule[week] if week < len(state.schedule) else None
        screens = next_week(state)
        for r in state.race_results:
            if r.get("event_id") not in seen_events:
                seen_events.add(r.get("event_id"))
                races.write(json.dumps(r, ensure_ascii=False) + "\n")
                races.flush()
                try:
                    cars.write(json.dumps(car_snapshot(r), ensure_ascii=False) + "\n")
                    cars.flush()
                except Exception as err:  # a view only; never stop a run over it
                    print(f"car snapshot failed: {err}", flush=True)
        if screens or time.time() - t > 5:
            print(f"season {season} week {week} {track or '-'}: {' > '.join(screens) or 'week'} "
                  f"({time.time() - t:.0f} s)", flush=True)
        if state.season_no != season:
            standings.write(json.dumps(snapshot, ensure_ascii=False) + "\n")
            standings.flush()
            print(f"season {season} finished", flush=True)
    state.save_season()


# --------------------------------------------------------------------------
# Report


def parse_time(text):
    text = (text or "").strip()
    if not text or not text[0].isdigit():
        return None
    minutes, _, seconds = text.rpartition(":")
    try:
        return (int(minutes) if minutes else 0) * 60 + float(seconds)
    except ValueError:
        return None


def real_results(season_dir):
    """Per round: pole time and driver, winner, and finishing order from research/results."""
    rounds = {}
    folder = season_dir / "research" / "results"
    for path in sorted(folder.glob("*-race.csv")):
        rnd = int(path.name.split("-")[0])
        with open(path, encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        order = [r["driver"] for r in rows if r.get("status", "").startswith("classified") and r["pos"].isdigit()]
        rounds[rnd] = {"winner": order[0] if order else None, "order": order}
        quali = path.with_name(path.name.replace("-race.csv", "-qualifying.csv"))
        if quali.exists():
            with open(quali, encoding="utf-8") as fh:
                q = [r for r in csv.DictReader(fh) if r["pos"] == "1"]
            if q:
                rounds[rnd]["pole_driver"] = q[0]["driver"]
                rounds[rnd]["pole_s"] = parse_time(q[0]["time"])
    return rounds


def fmt_lap(s):
    return f"{int(s // 60)}:{s % 60:06.3f}" if s else "-"


def share(points):
    total = sum(points.values()) or 1
    return {k: 100.0 * v / total for k, v in points.items()}


def report(out, season_dir=None):
    out = Path(out)
    meta = load_json(out / "sim.json")
    season_dir = season_dir or REPO / "seasons" / meta["season"]
    real = real_results(season_dir)
    points_table = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    seasons = []  # one list of races per simulated season
    for run in sorted(out.glob("run-*")):
        f = run / "races.jsonl"
        if not f.exists():
            continue
        by_season = defaultdict(list)
        for line in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            by_season[r["season"]].append(r)
        for s in sorted(by_season):
            seasons.append((run.name, s, sorted(by_season[s], key=lambda r: r["week"])))
    if not seasons:
        print("no finished races yet")
        return
    lines = [f"# Simulated {meta['season']}", "",
             f"{len(seasons)} simulated season(s) from `{meta['source']}`, seed {meta['seed']}.", ""]

    # Per round: pole time against the real pole, and who wins.
    lines += ["## Rounds", "",
              "| Round | Track | Real pole | Sim pole (median) | Diff | Sim poles | Real winner | Sim winners |",
              "|---|---|---|---|---|---|---|---|"]
    n_rounds = max(len(r) for _, _, r in seasons)
    driver_team = {}
    for rnd in range(1, n_rounds + 1):
        races = [r[rnd - 1] for _, _, r in seasons if len(r) >= rnd]
        for r in races:
            driver_team.update(r.get("driver_teams", {}))
        track = races[0]["track"]
        poles = [r["pole"]["time"] for r in races if r.get("pole", {}).get("time")]
        sim_pole = statistics.median(poles) if poles else None
        rp = real.get(rnd, {})
        diff = f"{100 * (sim_pole / rp['pole_s'] - 1):+.1f}%" if sim_pole and rp.get("pole_s") else "-"
        pole_by = Counter(r["pole"]["driver"] for r in races if r.get("pole"))
        winners = Counter(next(iter(sorted(r["drivers"], key=lambda d: int(r["drivers"][d]) if str(r["drivers"][d]).isdigit() else 99)), None) for r in races)
        top = lambda c: ", ".join(f"{k.split()[-1]} {v}" for k, v in c.most_common(3))
        lines.append(f"| {rnd} | {track} | {fmt_lap(rp.get('pole_s'))} | {fmt_lap(sim_pole)} | {diff} | "
                     f"{top(pole_by)} | {rp.get('winner') or '-'} | {top(winners)} |")

    # Championship: driver and team points shares, simulated mean vs real.
    real_driver = Counter()
    for rp in real.values():
        for pos, d in enumerate(rp["order"][:10]):
            real_driver[d] += points_table[pos]
    real_team = Counter()
    for d, p in real_driver.items():
        real_team[driver_team.get(d, "?")] += p
    sim_driver = defaultdict(list)
    sim_team = defaultdict(list)
    wins = Counter()
    distinct_winners = []
    for _, _, races in seasons:
        dp, tp = Counter(), Counter()
        ws = set()
        for r in races:
            for d, p in r.get("awarded_points", {}).items():
                dp[d] += p
                tp[r["driver_teams"].get(d, "?")] += p
            win = min(r["drivers"], key=lambda d: int(r["drivers"][d]) if str(r["drivers"][d]).isdigit() else 99)
            wins[win] += 1
            ws.add(win)
        distinct_winners.append(len(ws))
        for d, v in share(dp).items():
            sim_driver[d].append(v)
        for t, v in share(tp).items():
            sim_team[t].append(v)
    n = len(seasons)
    mean = lambda xs: sum(xs) / n  # seasons where someone scored nothing count as 0
    rd, rt = share(real_driver), share(real_team)
    real_winners = len({rp["winner"] for rp in real.values() if rp.get("winner")})
    lines += ["", "## Teams (share of all points)", "", "| Team | Real | Sim | Diff |", "|---|---|---|---|"]
    for t in sorted(set(rt) | set(sim_team), key=lambda t: -rt.get(t, 0)):
        lines.append(f"| {t} | {rt.get(t, 0):.1f}% | {mean(sim_team.get(t, [])):.1f}% | "
                     f"{mean(sim_team.get(t, [])) - rt.get(t, 0):+.1f} |")
    lines += ["", "## Drivers (share of all points)", "", "| Driver | Real | Sim | Sim wins per season |", "|---|---|---|---|"]
    for d in sorted(set(rd) | set(sim_driver), key=lambda d: -(rd.get(d, 0) + mean(sim_driver.get(d, [])))):
        lines.append(f"| {d} | {rd.get(d, 0):.1f}% | {mean(sim_driver.get(d, [])):.1f}% | {wins[d] / n:.1f} |")
    lines += ["", f"Different winners per season: real {real_winners}, "
              f"sim {', '.join(map(str, distinct_winners))}.", ""]
    lines += halves(seasons, real, n_rounds)
    lines += development(out, n_rounds)
    text = "\n".join(lines)
    (out / "report.md").write_text(text, encoding="utf-8")
    print(text)
    print(f"\nreport: {out / 'report.md'}")


def win_of(r):
    return min(r["drivers"], key=lambda d: int(r["drivers"][d]) if str(r["drivers"][d]).isdigit() else 99)


def halves(seasons, real, n_rounds):
    """First half against second half: how many winners, who wins, which teams score.

    A season that should open up and then close down (F1 2012: seven winners
    in seven races, then Vettel) shows it here, real against simulated.
    """
    if n_rounds < 4:
        return []
    cut = n_rounds // 2
    parts = [(f"Rounds 1-{cut}", range(1, cut + 1)), (f"Rounds {cut + 1}-{n_rounds}", range(cut + 1, n_rounds + 1))]
    lines = ["## First half and second half", "",
             "| Part | Real winners | Sim winners per season | Sim wins per season (top 4) | Sim points share (top 4 teams) |",
             "|---|---|---|---|---|"]
    n = len(seasons)
    for label, rounds in parts:
        real_w = [real[r]["winner"] for r in rounds if real.get(r, {}).get("winner")]
        distinct, wins, team_pts = [], Counter(), Counter()
        for _, _, races in seasons:
            ws = set()
            for r in races[rounds.start - 1:rounds.stop - 1]:
                w = win_of(r)
                ws.add(w)
                wins[w] += 1
                for d, p in r.get("awarded_points", {}).items():
                    team_pts[r["driver_teams"].get(d, "?")] += p
            distinct.append(len(ws))
        total = sum(team_pts.values()) or 1
        top_w = ", ".join(f"{d.split()[-1]} {c / n:.1f}" for d, c in wins.most_common(4))
        top_t = ", ".join(f"{t} {100 * p / total:.0f}%" for t, p in team_pts.most_common(4))
        real_names = ", ".join(dict.fromkeys(w.split()[-1] for w in real_w))
        lines.append(f"| {label} | {len(set(real_w))} ({real_names}) | {', '.join(map(str, distinct))} | {top_w} | {top_t} |")
    return lines + [""]


def development(out, n_rounds):
    """Each team's car rating (team_pace) at the first, middle and last race, mean over runs."""
    snaps = defaultdict(lambda: defaultdict(list))  # team -> race index -> values
    for run in sorted(Path(out).glob("run-*")):
        f = run / "cars.jsonl"
        if not f.exists():
            continue
        per_season = defaultdict(list)
        for line in f.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            per_season[row.get("season")].append(row)
        for rows in per_season.values():
            rows.sort(key=lambda r: r.get("week") or 0)
            for i, row in enumerate(rows):
                for team, vals in row["teams"].items():
                    if "team_pace" in vals:
                        snaps[team][i].append(vals["team_pace"])
    if not snaps:
        return []
    marks = sorted({0, n_rounds // 2 - 1, n_rounds - 1})
    lines = ["## Car development (team_pace after each race, mean of runs)", "",
             "| Team | " + " | ".join(f"Round {m + 1}" for m in marks) + " | Change |",
             "|---|" + "---|" * (len(marks) + 1)]
    mean = lambda xs: sum(xs) / len(xs) if xs else None
    rows = []
    for team, by_race in snaps.items():
        vals = [mean(by_race.get(m, [])) for m in marks]
        rows.append((vals[-1] or 0, team, vals))
    for _, team, vals in sorted(rows, reverse=True):
        cells = " | ".join(f"{v:.1f}" if v is not None else "-" for v in vals)
        change = f"{vals[-1] - vals[0]:+.1f}" if vals[0] is not None and vals[-1] is not None else "-"
        lines.append(f"| {team} | {cells} | {change} |")
    return lines + [""]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("season", nargs="?", help="season folder name, e.g. dtm-2013")
    ap.add_argument("--seasons", type=int, default=1, help="seasons per career (default 1)")
    ap.add_argument("--runs", type=int, default=1, help="independent careers (default 1)")
    ap.add_argument("--jobs", type=int, help="runs at the same time (default: half the CPU cores)")
    ap.add_argument("--save", type=Path, help="start from this save instead of a new career")
    ap.add_argument("--installed", action="store_true", help="use the installed pack instead of dist/")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--out", help="output folder (default build/sim/<season>/<time>)")
    ap.add_argument("--report", help="only (re)write the report of an earlier output folder")
    ap.add_argument("--worker", help=argparse.SUPPRESS)
    ap.add_argument("--exe", help=argparse.SUPPRESS)
    args = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    if args.worker:
        worker(args)
    elif args.report:
        report(args.report)
    elif args.season:
        launch(args)
    else:
        ap.error("give a season (e.g. dtm-2013) or --report <folder>")


if __name__ == "__main__":
    main()
