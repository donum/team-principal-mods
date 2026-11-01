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
    for part in (spec or "").replace(" ", "").split(","):
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", part)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
            out.update(r for r in range(lo, hi + 1) if r <= total)
    return out


def make_of(car):
    return next((m for key, m in MAKES if key.lower() in (car or "").lower()), "BMW")


def clean_name(name):
    return re.sub(r",\s*[A-Z]{1,3}$", "", name).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("season", type=Path)
    args = ap.parse_args()
    season = args.season.resolve()
    gen = load_json(season / "gen.json")
    tmpl = (REPO / "seasons" / gen.get("template", "dtm-1991")).resolve()
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
        entrant = e["entrant"].split(" / ")[0].strip()
        cfg_key = next((k for k, v in rename.items() if entrant in v.get("entrants", [k])), entrant)
        if rename.get(cfg_key, {}).get("skip"):
            continue
        name = rename.get(cfg_key, {}).get("name", cfg_key)
        team = teams.setdefault(name, {"entrant": entrant, "cfg": rename.get(cfg_key, {}), "makes": [], "tyres": []})
        team["makes"].append(make_of(e["car"]))
        if e.get("tyres"):
            team["tyres"].append(e["tyres"])
        dname = clean_name(e["driver"])
        d = drivers.setdefault(dname, {"name": dname, "team": name, "number": e["number"].strip(),
                                       "nationality": NATIONALITY.get(e["nationality"].strip(), "german"),
                                       "birth": e.get("birth_date", ""), "rounds": set()})
        d["rounds"] |= rounds_of(e["rounds"], total_rounds)

    # ---- per team: seats, points, rating
    team_records, driver_records, staff_levels, clones = [], [], {}, {}
    ranked = []
    for name, t in teams.items():
        members = [d for d in drivers.values() if d["team"] == name]
        best = max((standings.get(d["name"], 0) for d in members), default=0)
        ranked.append((best, name))
    ranked.sort(reverse=True)
    used_numbers = set()
    for pos, (best, name) in enumerate(ranked, 1):
        t = teams[name]
        cfg = t["cfg"]
        make = cfg.get("make") or max(set(t["makes"]), key=t["makes"].count)
        members = sorted([d for d in drivers.values() if d["team"] == name],
                         key=lambda d: (-len(d["rounds"]), -standings.get(d["name"], 0)))
        seated = [d for d in members if len(d["rounds"]) >= total_rounds / 2][:3] or members[:1]
        base = round(36 + 24 * (best / top_points) ** 0.7, 1)
        base = cfg.get("rating", base)
        tyre = cfg.get("tyres") or (max(set(t["tyres"]), key=t["tyres"].count) if t["tyres"] else DEFAULT_TYRE[make])
        works = cfg.get("works", best / top_points > 0.45)
        tier = min(len(CLONE_TIERS) - 1, (pos - 1) * len(CLONE_TIERS) // max(1, len(ranked)))
        clones[name] = CLONE_TIERS[tier]
        staff_levels[name] = max(4, min(16, round(4 + 12 * best / top_points)))
        rec = {
            "name": name, "nationality": cfg.get("nationality", "german"), "entry_count": len(seated),
            "color_rgb": cfg.get("color", [240, 240, 240]), "secondary_color_rgb": cfg.get("secondary", [30, 30, 30]),
            "engine": None, "engine_supplier": make, "engine_contract_type": "partner" if works else "customer",
            "tyre_contract": {"supplier": tyre, "type": "partner" if works else "customer"},
            "car_mass_kg": MASS[make], "$rating": {"base": base, "profile": PROFILE[make]},
            "heritage_prestige": cfg.get("heritage", round(base + 12)), "form_prestige": round(base + 10),
            "prestige_base": round(base + 11), "budget_m": round(base * 1.6), "starting_balance_m": round(base / 2, 1),
            "difficulty": "easy" if base >= 55 else "medium" if base >= 48 else "hard",
            "previous_constructor_position": pos,
            "headquarters": {"hospitality_pr_center": 2 + works, "wind_tunnel": 1 + works, "engine_plant": 0,
                             "test_track": int(works), "factory": 2 + 2 * works, "cfd_center": 1, "recon_centre": 1 + works,
                             "driver_centre": 1 + works},
        }
        team_records.append(rec)
        for d in members:
            pts = standings.get(d["name"], 0)
            share = pts / top_points
            skill = max(9, min(18, round(10 + 8 * share ** 0.6)))
            age = 30
            if d["birth"][:4].isdigit():
                b = datetime.date.fromisoformat(d["birth"]) if len(d["birth"]) == 10 else datetime.date(int(d["birth"][:4]), 7, 1)
                age = year - b.year - ((3, 1) < (b.month, b.day))
            main = d in seated
            num = d["number"] if d["number"].isdigit() else ""
            if main and (not num or num in used_numbers):
                num = str(max([int(n) for n in used_numbers] + [0]) + 1)
            if main:
                used_numbers.add(num)
            r = {"name": d["name"], "cornering": skill, "braking": skill, "consistency": max(8, skill - 1),
                 "smoothness": skill, "control": skill, "balance_preference": 55, "traction_preference": 50,
                 "contract": {"team": name, "length_weeks": 52, "salary_m": round(0.2 + 4.8 * share, 2), "start_week": 1,
                              "role": "main" if main else "reserve"},
                 "age": age, "talent": max(55, min(95, round(60 + 32 * share ** 0.6) - max(0, age - 34))),
                 "traits": [], "personalities": ["loyal"],
                 "career_stage": "top_veteran" if share > 0.6 and age >= 34 else "top_racer" if share > 0.6
                 else "reliable_veteran" if age >= 38 else "racer",
                 "nationality": d["nationality"]}
            if main:
                r["team"] = name
                r["number"] = int(num) if num else len(driver_records) + 1
                r["contract"].update(status="equal", priority="equal")
            elif num:
                r["reserve_number"] = int(num)
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
        "$comment": f"DTM {year} entrants, generated by tools/season_from_research.py from research/entries.csv "
                    f"and gen.json. Ratings are estimates from the {year} standings.",
        "$template": teams_file["$template"], "$profiles": teams_file["$profiles"], "records": team_records})
    drivers_file = load_json(tmpl / "data" / "drivers.json")
    dump_json(out_data / "drivers.json", {
        "$comment": f"DTM {year} drivers, generated from research/entries.csv and standings.csv. Skills and talent are "
                    f"estimates from championship points; part-timers are reserves.",
        "$template": drivers_file["$template"], "records": driver_records})
    dump_json(out_data / "engines.json", engines)
    dump_json(out_data / "tyre_suppliers.json", load_json(tmpl / "data" / "tyre_suppliers.json"))
    dump_json(out_data / "team_histories.json", {t["name"]: gen.get("teams", {}).get(t["name"], {}).get("history", "")
                                                 for t in team_records})

    # ---- calendar -> schedule
    schedule = [None] * 52
    schedule[2], schedule[4], schedule[5] = "private", "test", "test"
    track_map = gen["tracks"]
    for r in calendar:
        week = (datetime.date.fromisoformat(r["date"]) - datetime.date(year, 1, 1)).days // 7 + 1
        tid = track_map[r["round"]]
        while schedule[week - 1] is not None:
            week += 1
        schedule[week - 1] = tid
    dump_json(out_data / "schedule.json", schedule)

    # ---- season.json
    manifest = copy.deepcopy(load_json(tmpl / "season.json"))
    manifest.update({"title": f"DTM {year} - Deutsche Tourenwagen-Meisterschaft", "pack_folder": f"dtm{year}",
                     "version": "0.1", "team_clones": clones})
    manifest["constants"]["SEASON_START_YEAR"] = year
    manifest["staff"] = {"seed": year, "salary_per_level_m": 0.1, "named": [], "levels": staff_levels}
    manifest["shared_tracks"] = gen.get("shared_tracks", {})
    manifest["track_overrides"] = gen.get("track_overrides", {})
    dump_json(season / "season.json", manifest)
    (season / "patches").mkdir(exist_ok=True)
    (season / "patches" / "regulations.json").write_text(
        (tmpl / "patches" / "regulations.json").read_text(encoding="utf-8").replace("1991", str(year)),
        encoding="utf-8", newline="\n")
    print(f"{season.name}: {len(team_records)} teams, {sum(t['entry_count'] for t in team_records)} seats, "
          f"{len(driver_records)} drivers, {total_rounds} rounds")


if __name__ == "__main__":
    main()
