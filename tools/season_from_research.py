"""Generate a season pack's data files from its research CSVs.

Reads seasons/<id>/research/{calendar,entries,standings}.csv plus a small
hand-written config seasons/<id>/gen.json, and writes season.json and
data/{teams,drivers,engines,tyre_suppliers,schedule,team_histories}.json.
Rules, car profiles and engines are taken from a template season (by
default dtm-1991) so every Group A season shares one tuned baseline.

Ratings are estimates, not history:
* team base rating from the team's best championship points;
* driver skills and talent from the driver's own points;
* full-season drivers (in at least half the rounds) get race seats, up to
  3 per team; everyone else becomes a reserve driver.

Edit gen.json (team names, colours, tyres, overrides) and re-run; the
generated data files are then the source for build_pack.py.

A season of a car generation names its era base: gen.json "base": "<id>"
(bases/<id>/, see tools/layers.py). The base's own gen.json is merged under
the season's, so the generation's rules, car profiles, engines and tyres are
written once. The season.json written then holds only the season's own
values ("base", title, teams, staff, sponsors, its own constants and
tracks); build_pack.py merges the base's base.json underneath.

Seasons outside the Group A era override the template's rules in gen.json:
* "rules": "own" keeps the season's hand-written patches/regulations.json
  instead of copying the template's;
* "constants" are merged into season.json's constants.py overrides;
* "profiles" (car-character deltas), "make_profiles" and "mass_kg" per make;
* "engines" replace or add engine suppliers, "tyre_suppliers" replace the
  template's tyre suppliers, "tyre_development" is merged onto the base
  game's tyre development rules (null removes a key);
* "default_tyre" names the tyre supplier of teams without one (a single-make
  series);
* "rating_range" [low, high] spreads team ratings (default [36, 60]), from
  each team's best driver, or from its average points per car with
  "team_rating_from": "average";
* "skill_range" [low, high] spreads driver skills (default [10, 18]);
* "track_placeholders" {id: {"from": track, "override": {...}}} copy a track
  under a new id, e.g. a second visit to a venue with its own rain chance;
* "races_per_round": 2 gives each round one game week per race (two races
  a weekend, from 2015); a round in "tracks" may also be a list of track
  ids, one per race. Later races move to the next free week;
* entries.csv "rounds" may be "all", or ranges joined by "," or ";";
* "economy": "budget_per_rating", "salary_min_m", "salary_max_m";
* a team's "previous_position" sets its previous_constructor_position (the
  year before's teams' standing); without it, the team's rank this season;
* "sponsors": {"pool": {name: {"industry", "nationality"}}, "teams": {team:
  [names, primary first]}} real starting deals, copied to season.json for
  build_pack.py, which swaps them in for the cloned teams' fictional deals.

Single-seater series (F1) name the car's maker by its engine, and tune each
team by hand rather than from its points:
* "make_from": "engine" reads the make from entries.csv's engine column,
  with "makes": {"text in the engine": "supplier key"};
* "test_weeks": {"private": [weeks], "test": [weeks]} (1-based) replace the
  default test weeks 3 (private), 5 and 6;
* per team in "teams": "make", "rating", "profile" (a car profile name),
  "adjust" (extra profile deltas), "potential" (development headroom above
  the starting ratings, default 6), "chassis" {"prefix", "names"},
  "headquarters" (merged over the generated levels), "budget_m",
  "starting_balance_m", "staff_level", "engine_contract_type", "mass_kg",
  "clone" (the vanilla team whose secondary settings it takes), "prestige"
  {"heritage", "form", "base"}, "difficulty", "nationality";
* "drivers": {name: {...}} is merged over a driver's generated record
  ("skill" sets all five skills at once; "contract" merges), so the
  pecking order of drivers is set by hand.

Usage:
    python tools/season_from_research.py seasons/dtm-1990
"""

import argparse
import copy
import csv
import datetime
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
import sys  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
import layers  # noqa: E402

NATIONALITY = {"GER": "german", "GDR": "german", "FRA": "french", "DEN": "danish", "AUT": "austrian", "SUI": "swiss",
               "ITA": "italian", "GBR": "british", "VEN": "venezuelan", "BEL": "belgian", "SWE": "swedish",
               "TCH": "czech", "CZE": "czech", "FIN": "finnish", "AUS": "australian", "NED": "dutch", "CAN": "canadian",
               "USA": "american", "JPN": "japanese", "ESP": "spanish", "POR": "portuguese", "BRA": "brazilian"}
MAKES = [("Audi", "Audi"), ("BMW", "BMW"), ("Mercedes", "Mercedes-Benz"), ("Opel", "Opel"), ("Ford", "Ford"),
         ("Toyota", "Toyota"), ("Alfa", "Alfa Romeo"), ("Volvo", "Volvo"), ("Rover", "Rover")]
PROFILE = {"Audi": "audi_v8_quattro", "BMW": "bmw_m3_evo", "Mercedes-Benz": "mercedes_190e_evo2",
           "Opel": "opel_omega_evo500", "Ford": "ford_mustang_gt", "Toyota": "opel_omega_evo500"}
MASS = {"Audi": 1100.0, "BMW": 840.0, "Mercedes-Benz": 840.0, "Opel": 950.0, "Ford": 940.0, "Toyota": 960.0}
DEFAULT_TYRE = {"Audi": "Dunlop", "BMW": "Yokohama", "Mercedes-Benz": "Pirelli", "Opel": "Michelin", "Ford": "Dunlop",
                "Toyota": "Bridgestone"}
CLONE_TIERS = ["Red Boar", "Mercurion", "McMean", "Audex", "Scuderia Rossa", "Ashton Darting", "French Blue",
               "Alpha Bison", "Willens Racing", "Hossden GP", "Cadylacky Motors"]


def load_json(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump_json(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def read_csv(p):
    with open(p, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def rounds_of(spec, total):
    out = set()
    if (spec or "").strip().lower() == "all":
        return set(range(1, total + 1))
    for part in (spec or "").replace(" ", "").replace(";", ",").split(","):
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", part)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
            out.update(r for r in range(lo, hi + 1) if r <= total)
    return out


def make_of(car, makes=None):
    pairs = list(makes.items()) if makes else MAKES
    return next((m for key, m in pairs if key.lower() in (car or "").lower()), pairs[0][1] if makes else "BMW")


def clean_name(name):
    return re.sub(r",\s*[A-Z]{1,3}$", "", name).strip()


def chassis_fields(cfg):
    """Team chassis naming (0.99.6+) from gen.json "chassis": {make: {"prefix", "names"}}.

    The game names each new chassis prefix + two-digit year (e.g. "M3/13");
    "names" pins whole years ({"2013": "M3 DTM"}) to the real car's name.
    """
    if not cfg:
        return {}
    out = {}
    if cfg.get("prefix"):
        out["chassis_prefix"] = cfg["prefix"]
    if cfg.get("names"):
        out["chassis_names"] = {str(y): n for y, n in cfg["names"].items()}
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("season", type=Path)
    args = ap.parse_args()
    season = args.season.resolve()
    own = load_json(season / "gen.json")
    gen = layers.gen_config(season, own)
    tmpl = layers.source_dir(gen.get("template", "dtm-1991"))
    year = gen["year"]
    research = season / "research"

    calendar = [r for r in read_csv(research / "calendar.csv") if r["round"].strip().isdigit()]
    total_rounds = len(calendar)
    standings = {clean_name(r["driver"]): float(r["points"] or 0) for r in read_csv(research / "standings.csv")}
    top_points = max(standings.values()) or 1.0

    # ---- entries -> teams and drivers
    rename = gen.get("teams", {})
    teams, drivers = {}, {}
    for e in read_csv(research / "entries.csv"):
        entrant = re.split(r" / (?![^\[]*\])", e["entrant"])[0].strip()  # not inside [operator] brackets
        cfg_key = next((k for k, v in rename.items() if entrant in v.get("entrants", [k])), entrant)
        if rename.get(cfg_key, {}).get("skip"):
            continue
        name = rename.get(cfg_key, {}).get("name", cfg_key)
        team = teams.setdefault(name, {"entrant": entrant, "cfg": rename.get(cfg_key, {}), "makes": [], "tyres": []})
        team["makes"].append(make_of(e["engine"], gen.get("makes")) if gen.get("make_from") == "engine"
                             else make_of(e["car"]))
        if e.get("tyres"):
            team["tyres"].append(e["tyres"])
        dname = clean_name(e["driver"])
        nat = e["nationality"].strip()
        d = drivers.setdefault(dname, {"name": dname, "team": name, "number": e["number"].strip(),
                                       "nationality": NATIONALITY.get(nat, nat if nat.islower() else "german"),
                                       "birth": e.get("birth_date", ""), "rounds": set()})
        if "friday practice only" not in (e.get("notes") or "").lower():   # F1 test drivers stay reserves
            d["rounds"] |= rounds_of(e["rounds"], total_rounds)

    # ---- per team: seats, points, rating
    profile_of = {**PROFILE, **gen.get("make_profiles", {})}
    mass_of = {**MASS, **gen.get("mass_kg", {})}
    rating_lo, rating_hi = gen.get("rating_range", [36, 60])
    econ = gen.get("economy", {})
    salary_lo, salary_hi = econ.get("salary_min_m", 0.2), econ.get("salary_max_m", 5.0)
    team_records, driver_records, staff_levels, clones = [], [], {}, {}
    ranked = []
    for name, t in teams.items():
        members = [d for d in drivers.values() if d["team"] == name]
        best = max((standings.get(d["name"], 0) for d in members), default=0)
        if gen.get("team_rating_from") == "average":
            seated = [d for d in members if len(d["rounds"]) >= total_rounds / 2] or members[:1]
            best = sum(standings.get(d["name"], 0) for d in seated) / len(seated)
        ranked.append((best, name))
    ranked.sort(reverse=True)
    top_team = ranked[0][0] or 1.0
    skill_lo, skill_hi = gen.get("skill_range", [10, 18])
    used_numbers = set()
    for pos, (best, name) in enumerate(ranked, 1):
        t = teams[name]
        cfg = t["cfg"]
        make = cfg.get("make") or max(set(t["makes"]), key=t["makes"].count)
        members = sorted([d for d in drivers.values() if d["team"] == name],
                         key=lambda d: (-len(d["rounds"]), -standings.get(d["name"], 0)))
        seated = [d for d in members if len(d["rounds"]) >= total_rounds / 2][:3] or members[:1]
        base = round(rating_lo + (rating_hi - rating_lo) * (best / top_team) ** 0.7, 1)
        base = cfg.get("rating", base)
        rating = {"base": base, "profile": cfg.get("profile", profile_of.get(make))}
        for key in ("adjust", "potential"):
            if key in cfg:
                rating[key] = cfg[key]
        tyre = cfg.get("tyres") or (max(set(t["tyres"]), key=t["tyres"].count) if t["tyres"]
                                    else gen.get("default_tyre") or DEFAULT_TYRE[make])
        works = cfg.get("works", best / top_team > 0.45)
        tier = min(len(CLONE_TIERS) - 1, (pos - 1) * len(CLONE_TIERS) // max(1, len(ranked)))
        clones[name] = cfg.get("clone", CLONE_TIERS[tier])
        staff_levels[name] = cfg.get("staff_level", max(4, min(16, round(4 + 12 * best / top_team))))
        prestige = cfg.get("prestige", {})
        rec = {
            "name": name, "nationality": cfg.get("nationality", "german"), "entry_count": len(seated),
            "color_rgb": cfg.get("color", [240, 240, 240]), "secondary_color_rgb": cfg.get("secondary", [30, 30, 30]),
            "engine": None, "engine_supplier": make,
            "engine_contract_type": cfg.get("engine_contract_type", "partner" if works else "customer"),
            "tyre_contract": {"supplier": tyre, "type": "partner" if works else "customer"},
            "car_mass_kg": cfg.get("mass_kg", mass_of[make]), "$rating": rating,
            "heritage_prestige": prestige.get("heritage", cfg.get("heritage", round(base + 12))),
            "form_prestige": prestige.get("form", round(base + 10)),
            "prestige_base": prestige.get("base", round(base + 11)),
            "budget_m": cfg.get("budget_m", round(base * econ.get("budget_per_rating", 1.6))),
            "starting_balance_m": cfg.get("starting_balance_m", round(base / 2, 1)),
            "difficulty": cfg.get("difficulty", "easy" if base >= 55 else "medium" if base >= 48 else "hard"),
            "previous_constructor_position": cfg.get("previous_position", pos),
            **chassis_fields(cfg.get("chassis") or gen.get("chassis", {}).get(make)),
            "headquarters": {"hospitality_pr_center": 2 + works, "wind_tunnel": 1 + works, "engine_plant": 0,
                             "test_track": int(works), "factory": 2 + 2 * works, "cfd_center": 1, "recon_centre": 1 + works,
                             "driver_centre": 1 + works, **cfg.get("headquarters", {})},
        }
        team_records.append(rec)
        for d in members:
            pts = standings.get(d["name"], 0)
            share = pts / top_points
            skill = max(9, min(skill_hi, round(skill_lo + (skill_hi - skill_lo) * share ** 0.6)))
            age, birth_year = 30, None
            if d["birth"][:4].isdigit():
                b = datetime.date.fromisoformat(d["birth"]) if len(d["birth"]) == 10 else datetime.date(int(d["birth"][:4]), 7, 1)
                age = year - b.year - ((3, 1) < (b.month, b.day))
                birth_year = b.year
            main = d in seated
            num = d["number"] if d["number"].isdigit() else ""
            if main and (not num or num in used_numbers):
                num = str(max([int(n) for n in used_numbers] + [0]) + 1)
            if main:
                used_numbers.add(num)
            r = {"name": d["name"], "cornering": skill, "braking": skill, "consistency": max(8, skill - 1),
                 "smoothness": skill, "control": skill, "balance_preference": 55, "traction_preference": 50,
                 "contract": {"team": name, "length_weeks": 52, "salary_m": round(salary_lo + (salary_hi - salary_lo) * share, 2), "start_week": 1,
                              "role": "main" if main else "reserve"},
                 "age": age, "talent": max(55, min(95, round(60 + 32 * share ** 0.6) - max(0, age - 34))),
                 "traits": [], "personalities": ["loyal"],
                 "career_stage": "top_veteran" if share > 0.6 and age >= 34 else "top_racer" if share > 0.6
                 else "reliable_veteran" if age >= 38 else "racer",
                 "nationality": d["nationality"]}
            if birth_year and gen.get("birth_years"):
                # 0.99.6+: the game ages the driver from SEASON_START_YEAR, and
                # birth_year wins over age. age stays as the fallback.
                r["birth_year"] = birth_year
            if main:
                r["team"] = name
                r["number"] = int(num) if num else len(driver_records) + 1
                r["contract"].update(status="equal", priority="equal")
            elif num:
                r["reserve_number"] = int(num)
            over = copy.deepcopy(gen.get("drivers", {}).get(d["name"], {}))
            if "skill" in over:
                lvl = over.pop("skill")
                r.update(cornering=lvl, braking=lvl, consistency=lvl, smoothness=lvl, control=lvl)
            r["contract"].update(over.pop("contract", {}))
            r.update(over)
            driver_records.append(r)

    # Fix team engine names from the template engines.
    engines = load_json(tmpl / "data" / "engines.json")
    extra = gen.get("engines", {})
    engines["suppliers"].update(extra)
    makes_used = {t["engine_supplier"] for t in team_records}
    engines["suppliers"] = {k: v for k, v in engines["suppliers"].items() if k in makes_used}
    for t in team_records:
        t["engine"] = engines["suppliers"][t["engine_supplier"]]["engine"]
    for k, v in engines["suppliers"].items():
        v["capacity"] = sum(1 for t in team_records if t["engine_supplier"] == k)

    teams_file = load_json(tmpl / "data" / "teams.json")
    out_data = season / "data"
    dump_json(out_data / "teams.json", {
        "$comment": f"{gen.get('series_label', 'DTM')} {year} entrants, generated by tools/season_from_research.py from research/entries.csv "
                    f"and gen.json. Ratings are estimates from the {year} standings.",
        "$template": teams_file["$template"], "$profiles": {**teams_file["$profiles"], **gen.get("profiles", {})},
        "records": team_records})
    drivers_file = load_json(tmpl / "data" / "drivers.json")
    dump_json(out_data / "drivers.json", {
        "$comment": f"{gen.get('series_label', 'DTM')} {year} drivers, generated from research/entries.csv and standings.csv. Skills and talent are "
                    f"estimates from championship points; part-timers are reserves.",
        "$template": drivers_file["$template"], "records": driver_records})
    dump_json(out_data / "engines.json", engines)
    tyres = load_json(tmpl / "data" / "tyre_suppliers.json")
    if "tyre_suppliers" in gen:
        tyres["suppliers"] = gen["tyre_suppliers"]
    if "tyre_development" in gen:
        tyres["development"] = gen["tyre_development"]
    dump_json(out_data / "tyre_suppliers.json", tyres)
    dump_json(out_data / "team_histories.json", {t["name"]: gen.get("teams", {}).get(t["name"], {}).get("history", "")
                                                 for t in team_records})

    # ---- calendar -> schedule
    schedule = [None] * 52
    tests = gen.get("test_weeks", {"private": [3], "test": [5, 6]})
    for kind, weeks in tests.items():
        for w in weeks:
            schedule[w - 1] = kind
    # A round with several races (two from 2015) gets one game week per race:
    # "tracks": {"1": ["hockenheim13", "hockenheim13_r2"]}, or "races_per_round": 2
    # to repeat a single id. The game runs one race per week (wish list A1, A4).
    track_map = gen["tracks"]
    per_round = gen.get("races_per_round", 1)
    for r in calendar:
        week = (datetime.date.fromisoformat(r["date"]) - datetime.date(year, 1, 1)).days // 7 + 1
        tids = track_map[r["round"]]
        for tid in tids if isinstance(tids, list) else [tids] * per_round:
            while schedule[week - 1] is not None:
                week += 1
            if week > 52:
                raise SystemExit(f"round {r['round']}: no free week left in the year")
            schedule[week - 1] = tid
    dump_json(out_data / "schedule.json", schedule)

    # ---- season.json
    title = gen.get("title", f"DTM {year} - Deutsche Tourenwagen-Meisterschaft")
    if own.get("base"):
        # Only the season's own values: the base's base.json supplies the rest
        # (base pack, series, shared constants and tracks) at build time.
        manifest = {"base": own["base"], "title": title, "pack_folder": gen.get("pack_folder", f"dtm{year}"), "version": "0.1",
                    "constants": {"SEASON_START_YEAR": year, **own.get("constants", {})}, "team_clones": clones}
        gen_tracks = own
    else:
        manifest = copy.deepcopy(load_json(tmpl / "season.json"))
        manifest.update({"title": title, "pack_folder": gen.get("pack_folder", f"dtm{year}"), "version": "0.1",
                         "team_clones": clones})
        manifest["constants"]["SEASON_START_YEAR"] = year
        manifest["constants"].update(gen.get("constants", {}))
        gen_tracks = {"shared_tracks": {}, "track_overrides": {}, **gen}
    manifest["staff"] = {"seed": year, "salary_per_level_m": 0.1, "named": [], "levels": staff_levels}
    for key in ("shared_tracks", "track_overrides", "track_placeholders"):
        if key in gen_tracks and (gen_tracks[key] or key != "track_placeholders"):
            manifest[key] = gen_tracks[key]
    if gen.get("sponsors"):
        manifest["sponsors"] = {k: v for k, v in gen["sponsors"].items() if not k.startswith("$")}
    dump_json(season / "season.json", manifest)
    regulations = season / "patches" / "regulations.json"
    if gen.get("rules") == "own":
        if not any((layer / "patches" / "regulations.json").exists() for layer in layers.chain(season)):
            raise SystemExit(f'gen.json says "rules": "own" but no patches/regulations.json in {season} or its base')
    else:
        regulations.parent.mkdir(exist_ok=True)
        regulations.write_text((tmpl / "patches" / "regulations.json").read_text(encoding="utf-8")
                               .replace("1991", str(year)), encoding="utf-8", newline="\n")
    print(f"{season.name}: {len(team_records)} teams, {sum(t['entry_count'] for t in team_records)} seats, "
          f"{len(driver_records)} drivers, {total_rounds} rounds")

    if gen.get("juniors"):
        juniors(season, gen, year, driver_records, out_data)


# Feeder series: the game's junior_series.json (see docs/CAPABILITIES.md). The
# game seats the listed drivers only in its first season, matched by name
# against free drivers (team null, no contract) inside the age band, and fills
# empty seats with free drivers at random. Results come from driver skill +
# 2 x team quality + luck; the track is only a label, one race per week.
FLAG_DIR = "ui/assets/flags"


def juniors(season, gen, year, driver_records, out_data):
    cfg = gen["juniors"]
    research = season / "research" / "juniors"
    venue_ids = cfg.get("venues", {})
    taken = {d["name"] for d in driver_records}   # DTM drivers stay DTM drivers
    series_out, licence, records, seen = [], {}, [], {}
    flags = None
    local = REPO / "local.json"
    game = Path(load_json(local)["game_path"]) if local.exists() and "game_path" in load_json(local) else None
    if game and (game / FLAG_DIR).is_dir():
        flags = {p.stem for p in (game / FLAG_DIR).glob("*.png")}

    # Each driver races in one series in the game: the first listed series in
    # which they did at least half the rounds, else the one with most rounds.
    entries = {}
    for s in cfg["series"]:
        cal = [r for r in read_csv(research / f"{s['id']}_calendar.csv") if r["round"].strip().isdigit()]
        total = len(cal)
        rows = read_csv(research / f"{s['id']}_entries.csv")
        per = {}
        for e in rows:
            name = clean_name(e["driver"])
            d = per.setdefault(name, {"rows": [], "rounds": set()})
            d["rows"].append(e)
            d["rounds"] |= rounds_of(e["rounds"], total)
        entries[s["id"]] = (cal, total, per)
    home = {}
    for s in cfg["series"]:
        cal, total, per = entries[s["id"]]
        for name, d in per.items():
            share = len(d["rounds"]) / max(1, total)
            best = home.get(name)
            if best is None or (share >= 0.5 and best[1] < 0.5):
                home[name] = (s["id"], share)

    for s in cfg["series"]:
        sid = s["id"]
        cal, total, per = entries[sid]
        # "classes": {"Division 2": 0.7} scales a slower class's points (notes start with its name)
        scale = s.get("classes", {})
        standings = {clean_name(r["driver"]): float(r["points"] or 0) * next(
                         (f for c, f in scale.items() if r["notes"].startswith(c)), 1.0)
                     for r in read_csv(research / f"{sid}_standings.csv") if r["pos"].strip().isdigit()}
        top = max(standings.values(), default=0) or 1.0
        colours = {r["team"]: r for r in read_csv(research / f"{sid}_teams.csv")}
        team_alias = s.get("team_names", {})
        skill_lo, skill_hi = s["skill_range"]
        min_rounds = s.get("min_rounds", 2)

        teams, skipped = {}, []
        for name, d in per.items():
            if name in taken or home[name][0] != sid or len(d["rounds"]) < min_rounds:
                continue
            # the entrant they raced for most
            counts = {}
            for e in d["rows"]:
                ent = team_alias.get(e["entrant"].strip(), e["entrant"].strip())
                counts[ent] = counts.get(ent, 0) + len(rounds_of(e["rounds"], total))
            team = max(counts, key=counts.get)
            e0 = d["rows"][0]
            pts = standings.get(name, 0.0)
            share = pts / top
            skill = max(6, min(skill_hi, round(skill_lo + (skill_hi - skill_lo) * share ** 0.6)))
            birth = (e0.get("birth_date") or "").strip()
            age, birth_year = s.get("default_age", 20), None
            if birth[:4].isdigit():
                b = datetime.date.fromisoformat(birth) if len(birth) == 10 else datetime.date(int(birth[:4]), 7, 1)
                age = year - b.year - ((3, 1) < (b.month, b.day))
                birth_year = b.year
            # with birth_year the game counts age as season year - birth year
            game_age = year - birth_year if birth_year and gen.get("birth_years") else age
            if not s["min_age"] <= game_age <= s["max_age"]:
                # the game would not seat them; leaving them out also keeps
                # the seat count honest
                skipped.append(f"{name} ({game_age})")
                continue
            talent = round(52 + 30 * share ** 0.6 + 2.5 * (s.get("talent_age", 21) - age))
            talent = max(45, min(s.get("talent_cap", 90), talent))
            nat = e0["nationality"].strip() or "german"
            if flags is not None and nat not in flags:
                print(f"  warning: {sid}: {name}: no flag for nationality {nat!r}")
            rec = {"name": name, "team": None, "licence_points": min(10, round(s.get("licence_start", 0) * share)),
                   "cornering": skill, "braking": skill, "consistency": max(6, skill - 1), "smoothness": skill,
                   "control": skill, "balance_preference": 50, "traction_preference": 50,
                   "age": age, "talent": talent, "traits": [], "personalities": ["loyal"],
                   "career_stage": "racer", "nationality": nat}
            if birth_year and gen.get("birth_years"):
                rec["birth_year"] = birth_year
            records.append(rec)
            teams.setdefault(team, []).append((len(d["rounds"]), pts, name))
            taken.add(name)
        if skipped:
            print(f"  junior {s['abbreviation']}: outside ages {s['min_age']}-{s['max_age']}, left out: {', '.join(skipped)}")

        ranked = sorted(teams, key=lambda t: -max(p for _, p, _ in teams[t]))
        best_team = max((max(p for _, p, _ in teams[t]) for t in teams), default=1.0) or 1.0
        q_lo, q_hi = s.get("quality_range", [3, 10])
        team_out = []
        for t in ranked:
            col = colours.get(t, {})
            members = sorted(teams[t], key=lambda m: (-m[0], -m[1]))
            best = max(p for _, p, _ in members)
            team_out.append({
                "name": t,
                "primary_color_rgb": hex_rgb(col.get("primary_color_hex"), [200, 200, 200]),
                "secondary_color_rgb": hex_rgb(col.get("secondary_color_hex"), [40, 40, 40]),
                "quality": round(q_lo + (q_hi - q_lo) * (best / best_team) ** 0.7),
                "drivers": [n for _, _, n in members[:s["drivers_per_team"]]],
            })

        schedule = [None] * 52
        for r in cal:
            day = datetime.date.fromisoformat(r["date_last_day"])
            week = (day - datetime.date(year, 1, 1)).days // 7 + 1
            venue = r["venue"].strip()
            tid = venue_ids.get(venue) or re.sub(r"[^a-z0-9]", "", venue.lower())[:12]
            while 0 < week <= 52 and schedule[week - 1] is not None:
                week += 1
            if 0 < week <= 52:
                schedule[week - 1] = tid
        series_out.append({
            "series_name": s["name"], "series_abbreviation": s["abbreviation"], "description": s["description"],
            "tier": s["tier"], "minimum_driver_age": s["min_age"], "maximum_driver_age": s["max_age"],
            "drivers_per_team": s["drivers_per_team"], "dnf_rate_percent": s["dnf_rate"],
            "points_format": {"points": s["points"]}, "teams": team_out, "schedule": schedule})
        licence[s["abbreviation"]] = {"tier": s["tier"], "points": s["licence_points"]}
        print(f"  junior {s['abbreviation']}: {len(team_out)} teams, "
              f"{sum(len(t['drivers']) for t in team_out)} seated, "
              f"{sum(1 for t in teams.values() for _ in t)} drivers, {len(cal)} rounds")

    # A few hand-rated free agents (ex-F1, Red Bull juniors) from
    # research/juniors/free_agents.csv. The game favours free agents when
    # teams sign drivers, so the list stays short.
    picks = cfg.get("free_agents", {})
    if picks:
        for r in read_csv(research / "free_agents.csv"):
            name = clean_name(r["driver"])
            if name not in picks or name in taken:
                continue
            p = picks[name]
            b = r["birth_date"].strip()
            rec = {"name": name, "team": None, "licence_points": p.get("licence", 10),
                   "cornering": p["skill"], "braking": p["skill"], "consistency": p["skill"] - 1,
                   "smoothness": p["skill"], "control": p["skill"], "balance_preference": 50,
                   "traction_preference": 50, "age": year - int(b[:4]) - (b[5:] > "03-01"), "talent": p["talent"],
                   "traits": [], "personalities": ["loyal"], "career_stage": "racer",
                   "nationality": r["nationality"].strip()}
            if gen.get("birth_years"):
                rec["birth_year"] = int(b[:4])
            records.append(rec)
            taken.add(name)
        names = [n for n in picks if not n.startswith("$")]
        print(f"  free agents: {sum(1 for n in names if n in taken)} of {len(names)}")
        # The game seats any free driver inside a feeder's age band, so a free
        # agent is kept for DTM only if every band stops below their age.
        for rec in records:
            if rec["name"] in picks:
                game_age = year - rec["birth_year"] if "birth_year" in rec else rec["age"]
                open_to = [x["abbreviation"] for x in cfg["series"] if x["min_age"] <= game_age <= x["max_age"]]
                if open_to:
                    print(f"  note: free agent {rec['name']} ({game_age}) can take a seat in {', '.join(open_to)}")

    dump_json(out_data / "junior_series.json", series_out)
    dump_json(out_data / "driverslicense.json", {"enabled": cfg.get("licences", True), "series": licence})
    drivers = load_json(out_data / "drivers.json")
    drivers["records"] = driver_records + records
    drivers["$comment"] += f" Feeder-series drivers ({len(records)}, team null) from research/juniors."
    dump_json(out_data / "drivers.json", drivers)


def hex_rgb(value, fallback):
    value = (value or "").strip().lstrip("#")
    return [int(value[i:i + 2], 16) for i in (0, 2, 4)] if len(value) == 6 else fallback


if __name__ == "__main__":
    main()
