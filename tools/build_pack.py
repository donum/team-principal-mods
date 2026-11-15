"""Assemble a Team Principal data pack from a season source folder.

The repository only stores our own content (season data, track traces, art).
Everything else a pack needs (constants.py, audio, tyre model, ...) is copied
from a base pack of the user's local game install at build time, so no
proprietary game files ever end up in git (EULA section 4.3).

Season source layout (seasons/<id>/):
    season.json        build manifest (base pack, constants, workshop meta);
                       "base": "<id>" puts an era base (bases/<id>/, same
                       layout, manifest base.json) underneath, see layers.py
    data/<file>.json   replaces <file>.json of the base pack; list files may
                       use "$template" to deep-merge every record onto a
                       record taken from the base pack
    patches/regulations.json
                       per-category overrides ("default", extra "options")
    patches/config.json
                       deep-merged into the base pack's config.json (race
                       physics: dirty air, slipstream, DRS)
    tracks/<id>.json  our own traced tracks
    assets/...         our own images, copied over the base assets

Usage:
    python tools/build_pack.py seasons/dtm-1991 [--game PATH] [--install]
"""

import argparse
import copy
import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import layers  # noqa: E402
from layers import deep_merge  # noqa: E402,F401  (re-exported for other tools)
DEFAULT_GAME = Path(r"X:\SteamLibrary\steamapps\common\Team Principal A Racing Manager")
SCHEDULE_KEYWORDS = {None, "private", "test"}
# Base-pack art that would contradict a historic season; removed unless the
# season ships its own replacement.
FICTIONAL_ASSET_DIRS = ["Cars", "logos", "engines", "parts", "portraits", "sponsors", "tracks"]


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def dump_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def game_path(cli_value):
    if cli_value:
        return Path(cli_value)
    local = REPO / "local.json"
    if local.exists():
        return Path(load_json(local)["game_path"])
    return DEFAULT_GAME


RATING_KEYS = ("team_pace", "braking", "acceleration")
ATTR_KEYS = ("slow", "med", "high", "straight")


def apply_rating(record, profiles):
    """Expand "$rating": {"base": 55, "profile": "bmw_m3"} into car ratings.

    A profile holds deltas relative to the base rating, so the pecking order
    of a season is tuned in one place (the base) and the car character in
    another (the profile).
    """
    spec = record.pop("$rating", None)
    if spec is None:
        return record
    base = spec["base"]
    deltas = deep_merge(profiles.get(spec.get("profile"), {}), spec.get("adjust", {}))
    clamp = lambda v: round(max(1.0, min(100.0, v)), 1)
    for key in RATING_KEYS + ("tyre_management", "chassis_reliability", "aero_efficiency_rating"):
        record[key] = clamp(base + deltas.get(key, 0))
    record["attr"] = {k: clamp(base + deltas.get(k, 0)) for k in ATTR_KEYS}
    record["dirty_air_sensitivity"] = clamp(50 + deltas.get("dirty_air_sensitivity", 0))
    record["aero"] = {"efficiency_rating": record["aero_efficiency_rating"]}
    headroom = spec.get("potential", 6)
    potential = {k: clamp(record[k] + headroom) for k in RATING_KEYS + ("tyre_management", "chassis_reliability", "aero_efficiency_rating")}
    potential.update({k: clamp(v + headroom) for k, v in record["attr"].items()})
    potential["dirty_air_sensitivity"] = record["dirty_air_sensitivity"]
    record["chassis_starting_potential"] = potential
    return record


def expand_templates(name, data, base_dir):
    """Resolve {"$template": {...}, "records": [...]} list files.

    Dict files may instead set "$merge_base": true to deep-merge onto the
    base file; keys listed in "$replace" are swapped wholesale, and a null
    value removes a key.
    """
    if isinstance(data, dict) and data.get("$merge_base"):
        base = load_json(base_dir / name)
        for key in data.get("$replace", []):
            base.pop(key, None)
        body = {k: v for k, v in data.items() if not k.startswith("$")}
        return deep_merge(base, body)
    if not (isinstance(data, dict) and "$template" in data):
        return data
    spec = data["$template"]
    base_records = load_json(base_dir / name)
    if "match" in spec:
        key, value = next(iter(spec["match"].items()))
        template = next(r for r in base_records if r.get(key) == value)
    else:
        template = base_records[spec.get("index", 0)]
    template = deep_merge(template, spec.get("override", {}))
    for key in spec.get("drop", []):
        template.pop(key, None)
    profiles = data.get("$profiles", {})
    records = []
    for record in data["records"]:
        merged = deep_merge(template, record)
        for key in spec.get("drop_if_absent", []):
            if key not in record:
                merged.pop(key, None)
        records.append(apply_rating(merged, profiles))
    return records


def clone_team_records(out, clones, shipped):
    """Re-key every base-pack file that is indexed by team name.

    `clones` maps each new team to the base team whose secondary settings
    (supplier contracts, starting tech, ERS levels, ownership, sponsors) it
    inherits. Files the season or its base ship in data/ (`shipped`) are
    left alone.
    """

    def rekey_dict(mapping):
        return {new: copy.deepcopy(mapping[old]) for new, old in clones.items() if old in mapping}

    def rekey_list(items, key="team"):
        by_team = {item[key]: item for item in items}
        return [{**copy.deepcopy(by_team[old]), key: new} for new, old in clones.items() if old in by_team]

    def edit(name, fn):
        if name in shipped or not (out / name).exists():
            return
        dump_json(out / name, fn(load_json(out / name)))

    base_teams = set(clones.values())

    def rekey_ownership(mapping):
        owned = rekey_dict(mapping)
        for entry in owned.values():
            holders = entry.get("shareholders", {})
            for holder in [h for h in holders if h in base_teams]:
                holders["institutions"] = holders.get("institutions", 0.0) + holders.pop(holder)
        return owned

    edit("team_ownership.json", rekey_ownership)
    edit("team_histories.json", lambda d: {new: "" for new in clones})
    edit("team_buyouts.json", lambda d: [])
    edit("events.json", lambda d: [e for e in d if "team" not in e])
    edit("starting_sponsors.json", lambda d: {**d, "teams": rekey_list(d["teams"])})
    edit("startingtechnologies.json", lambda d: {**d, "teams": rekey_list(d["teams"])})
    edit("parts.json", lambda d: {**d, "default_contracts": rekey_dict(d["default_contracts"])})
    edit("ers_development.json", lambda d: {**d, "starting_levels": {"default": d["starting_levels"].get("default", {}), **rekey_dict(d["starting_levels"])}})
    edit("relationships.json", lambda d: {k: {} for k in d})


SPONSOR_TERMS = ("rating", "amount_m", "amount_range_m", "prestige_min", "active")


def apply_sponsors(out, spec):
    """Swap the cloned teams' fictional starting deals for their real sponsors.

    `spec` is season.json "sponsors": {"pool": {name: {"industry",
    "nationality"}}, "teams": {team: [names, primary first]}}. Each real
    sponsor takes the slot, contract length, rating and money of the inherited
    deal it replaces, so a team's sponsor income stays what its vanilla clone
    gave it. With fewer real sponsors than inherited deals, the left-over money
    goes to the primary sponsor. The replaced fictional sponsors leave the
    pool; the rest stay as the free market for later seasons.
    """
    starting = load_json(out / "starting_sponsors.json")
    pool = load_json(out / "sponsors.json")
    by_name = {s["name"]: s for s in pool}
    deals_of = {t["team"]: t for t in starting.get("teams", [])}
    replaced, added = set(), {}
    for team, names in spec["teams"].items():
        entry = deals_of.get(team)
        if entry is None:
            sys.exit(f"sponsors: {team!r} has no inherited deals (not in team_clones?)")
        old = entry["sponsors"]
        if not names or len(names) > len(old):
            sys.exit(f"sponsors: {team!r} lists {len(names)} sponsors, its clone has {len(old)} deals")
        for name in names:
            if name not in spec["pool"]:
                sys.exit(f"sponsors: {name!r} ({team}) is not in the sponsor pool")
            if name in added or name in by_name:
                sys.exit(f"sponsors: {name!r} is used twice or clashes with a vanilla sponsor")
        recs = []
        for deal, name in zip(old, names):
            src = by_name[deal["name"]]
            recs.append({"name": name, **{k: copy.deepcopy(src[k]) for k in SPONSOR_TERMS if k in src},
                         **spec["pool"][name]})
        for deal in old[len(names):]:
            extra = by_name[deal["name"]]
            recs[0]["amount_m"] = round(recs[0]["amount_m"] + extra["amount_m"], 1)
            if "amount_range_m" in recs[0] and "amount_range_m" in extra:
                recs[0]["amount_range_m"] = [round(a + b, 1) for a, b in zip(recs[0]["amount_range_m"], extra["amount_range_m"])]
        added.update({r["name"]: r for r in recs})
        replaced |= {d["name"] for d in old}
        entry["sponsors"] = [{**deal, "name": name} for deal, name in zip(old, names)]
    dump_json(out / "starting_sponsors.json", starting)
    dump_json(out / "sponsors.json", [s for s in pool if s["name"] not in replaced] + list(added.values()))


def strip_title_sponsors(out):
    """Stop sponsors from renaming teams ("Patronix BMW M Team Schnitzer").

    A title sponsor's name is prefixed to the team name. Historic seasons
    already carry the real sponsor in the entrant name, so neither the
    starting deals nor the sponsor pool may hand out title status.
    """
    starting = load_json(out / "starting_sponsors.json")
    for team in starting.get("teams", []):
        for deal in team.get("sponsors", []):
            deal.pop("title", None)
    dump_json(out / "starting_sponsors.json", starting)
    pool = load_json(out / "sponsors.json")
    for sponsor in pool:
        if sponsor.get("type") == "title":
            del sponsor["type"]
    dump_json(out / "sponsors.json", pool)


def contrast_ratio(a, b):
    """WCAG 2 contrast ratio between two RGB colours."""
    def luminance(rgb):
        c = [v / 255 for v in rgb]
        c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def readable_team_text(out):
    """The game writes team names in the secondary colour on the primary one.
    Where that pair is below WCAG AA (4.5:1), use white or black instead."""
    path = out / "teams.json"
    teams = load_json(path)
    for team in teams:
        bg, fg = team.get("color_rgb"), team.get("secondary_color_rgb")
        if bg and fg and contrast_ratio(bg, fg) < 4.5:
            team["secondary_color_rgb"] = max(([255, 255, 255], [20, 20, 20]), key=lambda c: contrast_ratio(bg, c))
    dump_json(path, teams)


STAFF_REF = REPO / "docs" / "staff"
ROLE_AGE = {"team_principal": (38, 64), "technical_director": (36, 60), "chief_designer": (34, 58),
            "head_of_aero": (30, 52), "head_of_engine": (36, 62), "head_of_dynamics": (30, 52),
            "chief_mechanic": (28, 54)}


def name_seed(*parts):
    import hashlib
    return int(hashlib.sha1("|".join(map(str, parts)).encode("utf-8")).hexdigest(), 16)


def person_age(name, role, year, born=None):
    """Age in `year`. Without a known birth year, a fixed one per name
    (1930 to 1985) keeps the person the same age across packs; it is pulled
    into the role's usual range only if it falls outside."""
    if born:
        return year - born
    lo, hi = ROLE_AGE.get(role, (30, 60))
    age = year - (1930 + name_seed(name, "born") % 56)
    return age if 25 <= age <= 75 else lo + name_seed(name, role, "age") % (hi - lo + 1)


def period_name(nationality, year, role, used, *seed):
    """A made-up name that fits the nationality and the period, from the
    same lists as tools/fictional_staff.py."""
    import fictional_staff as fs
    first_old, first_new, last = fs.NAMES.get(nationality) or fs.NAMES["german"]
    lo, hi = ROLE_AGE.get(role, (30, 60))
    born = year - (lo + name_seed(*seed, "age") % (hi - lo + 1))
    firsts = first_old if born < 1960 else first_new
    for i in range(400):
        name = f"{firsts[name_seed(*seed, 'f', i) % len(firsts)]} {last[name_seed(*seed, 'l', i) % len(last)]}"
        if name not in used:
            return name, born
    return name, born


def staff_reference(season):
    """team -> role -> list of (name, born, nationality) from docs/staff.

    Real people (dtm_staff.csv, verified or assumed) come first, then the
    made-up names of dtm_staff_fictional.csv for roles nobody was found for.
    """
    import csv

    ref = {}
    for path in (STAFF_REF / "dtm_staff.csv", STAFF_REF / "dtm_staff_fictional.csv"):
        if not path.exists():
            continue
        with open(path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row["season"] != season:
                    continue
                born = int(row["born"]) if row.get("born") else None
                ref.setdefault(row["team"], {}).setdefault(row["role"], []).append(
                    (row["person"], born, row.get("nationality") or None))
    return ref


def generate_staff(out, base_dir, spec, teams):
    """Fill every team with one staff member per role.

    Order of precedence per team and role:
    1. spec["named"]: full records written into season.json.
    2. spec["reference"] (a season id like "dtm-2013"): the people in
       docs/staff (real first, then the made-up names for empty roles).
       A person can work for one team only, so a name shared by several
       teams (a manufacturer-level designer) goes to the highest-level team.
    3. A random name from the game's nationality pool.
    Skills always scale with the team's level.
    """
    import random

    rng = random.Random(spec.get("seed", 1991))
    base_staff = load_json(base_dir / "staff.json")
    pools = load_json(base_dir / "driver_names.json")["names_by_nationality"]
    roles = sorted({s["role"] for s in base_staff})
    templates = {r: next(s for s in base_staff if s["role"] == r and s.get("team")) for r in roles}
    named = spec.get("named", [])
    used = {s["name"] for s in named}
    staff = list(named)
    levels = spec["levels"]
    season = spec.get("reference")
    ref = staff_reference(season) if season else {}
    year = int(season.split("-")[1]) if season else None
    for team in sorted(teams, key=lambda t: -levels[t["name"]]):
        level = levels[team["name"]]
        filled = {s["role"] for s in named if s.get("team") == team["name"]}
        pool = pools.get(team["nationality"]) or pools["german"]
        for role in roles:
            if role in filled:
                continue
            tpl = copy.deepcopy(templates[role])
            age, nat = rng.randint(32, 58), None
            for name, born, ref_nat in ref.get(team["name"], {}).get(role, []):
                if name not in used:
                    age = person_age(name, role, year, born)
                    nat = ref_nat
                    break
            else:
                if season:
                    name, born = period_name(team["nationality"], year, role, used, season, team["name"], role)
                    age = year - born
                else:
                    for _ in range(200):
                        name = f"{rng.choice(pool['first_names'])} {rng.choice(pool['last_names'])}"
                        if name not in used:
                            break
            used.add(name)
            jitter = lambda: max(1, min(20, level + rng.randint(-2, 2)))
            nat = nat if nat in pools else (team["nationality"] if team["nationality"] in pools else "german")
            tpl.update({
                "name": name,
                "team": team["name"],
                "skill": jitter(),
                "age": age,
                "nationality": nat,
                "skills": {k: jitter() for k in tpl["skills"]},
                "talent": {k: min(20, jitter() + 2) for k in tpl["talent"]},
                "contract": {"team": team["name"], "length_weeks": 104,
                             "salary_m": round(spec.get("salary_per_level_m", 0.1) * level, 2), "start_week": 1},
            })
            staff.append(tpl)
    dump_json(out / "staff.json", staff)
    if season:
        generate_team_principals(out, spec, teams, ref, year, used)


def generate_team_principals(out, spec, teams, ref, year, used_staff_names):
    """Replace the base pack's fictional principals with one per DTM team.

    The principal comes from docs/staff (real, else made-up). A name the
    game already uses (a second team of the same owner, or a staff member)
    falls back to a made-up name from the team's other roles' pool. Ratings
    scale with the team's level; the background is fixed per name.
    """
    import hashlib
    import random

    path = out / "teamprincipals.json"
    data = load_json(path)
    backgrounds = [b for b in data.get("backgrounds", {}) if b != "newcomer"] or ["newcomer"]
    rng = random.Random(f"tp-{spec.get('seed', year)}")
    pools = load_json(out / "driver_names.json")["names_by_nationality"]
    levels = spec["levels"]
    used = set(used_staff_names)
    principals = []
    for team in sorted(teams, key=lambda t: -levels[t["name"]]):
        level = levels[team["name"]]
        name, born, nat = None, None, None
        for cand, cand_born, cand_nat in ref.get(team["name"], {}).get("team_principal", []):
            if cand not in used:
                name, born, nat = cand, cand_born, cand_nat
                break
        if name is None:
            name, born = period_name(team["nationality"], year, "team_principal", used,
                                     "tp", team["name"])
        used.add(name)
        first, _, last = name.partition(" ")
        seed = int(hashlib.sha1(name.encode("utf-8")).hexdigest(), 16)
        age = person_age(name, "team_principal", year, born)
        rate = lambda k: max(5, min(18, level + (seed >> (4 * k)) % 5 - 2))
        principals.append({
            "first_name": first,
            "last_name": last,
            "nationality": nat if nat in pools else (team["nationality"] if team["nationality"] in pools else "german"),
            "age": age,
            "background": backgrounds[seed % len(backgrounds)],
            "team": team["name"],
            "stats": {"reputation": rate(1), "finance": rate(2), "leadership": rate(3), "organization": rate(4)},
        })
    data["description"] = ("DTM team principals from docs/staff/dtm_staff.csv (real people, verified or "
                           "assumed); made-up names where no principal is known.")
    data["principals"] = principals
    dump_json(path, data)


def patch_constants(text, overrides):
    """Replace top-level literal assignments in constants.py.

    Only literal values are written (via repr of JSON values), so a season
    can never inject code into the executed constants file.
    """
    for name, value in overrides.items():
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", name):
            raise ValueError(f"invalid constant name {name!r}")
        if not isinstance(value, (int, float, str, bool, list)):
            raise ValueError(f"{name}: only literal values are allowed")
        pattern = re.compile(rf"^{name}\s*=.*$", re.MULTILINE)
        line = f"{name} = {value!r}"
        if pattern.search(text):
            text = pattern.sub(lambda _m: line, text, count=1)
        else:
            text += f"\n# Added by team-principal-mods build\n{line}\n"
    return text


def patch_regulations(regs, patch):
    by_key = {c["key"]: c for c in regs["categories"]}
    for key, change in patch.get("categories", {}).items():
        cat = by_key.get(key)
        if cat is None:
            raise ValueError(f"regulations: unknown category {key!r}")
        options = cat.setdefault("options", [])
        next_id = max((o.get("id", 0) for o in options), default=0) + 1
        for option in change.get("add_options", []):
            # An option with a key already there (e.g. a season replacing its
            # base's) keeps its place and id: the game rejects gaps in the ids.
            same = next((i for i, o in enumerate(options) if o.get("key") == option["key"]), None)
            if same is not None:
                options[same] = {"id": options[same].get("id", next_id), **option}
            else:
                options.append({"id": next_id, **option})
                next_id += 1
        if "default" in change:
            if change["default"] not in {o.get("key") for o in options}:
                raise ValueError(f"regulations: {key} default {change['default']!r} is not an option")
            cat["default"] = change["default"]
    if "change_control" in patch:
        regs["change_control"] = deep_merge(regs["change_control"], patch["change_control"])
    return regs


def place_tracks(season_dir, out, manifest):
    """Copy our traced tracks, then fill placeholders for untraced venues.

    The season's own tracks are always copied. A base's tracks and shared
    tracks only when the season races them (or a placeholder copies them),
    so a season doesn't carry the whole era's venues.
    """
    tracks_dir = out / "tracks"
    art_dir = out / "assets" / "tracks"
    raced = set(load_json(out / "schedule.json")) - SCHEDULE_KEYWORDS
    sources = {spec["from"] for key, spec in manifest.get("track_placeholders", {}).items() if not key.startswith("$")}
    needed = raced | sources
    keep = set()
    for track in layers.files(season_dir, "tracks").values():
        if layers.layer_of(season_dir, track) != season_dir.resolve() and track.stem not in needed:
            continue
        shutil.copy2(track, tracks_dir / track.name)
        keep.add(track.stem)
    # Tracks reused from another season ("shared_tracks": {"zolder": "dtm-1991"}),
    # with per-season overrides (length_km, race_laps -> lap_modifier, speed;
    # speed_mult scales every micro-sector target speed for this season only).
    for track_id, src_season in manifest.get("shared_tracks", {}).items():
        if track_id in keep or track_id not in needed:
            continue
        src = layers.source_dir(src_season)
        shutil.copy2(src / "tracks" / f"{track_id}.json", tracks_dir / f"{track_id}.json")
        shutil.copy2(src / "assets" / "tracks" / f"{track_id}.png", art_dir / f"{track_id}.png")
        keep.add(track_id)
    placeholders = {}
    for track_id, spec in manifest.get("track_placeholders", {}).items():
        if track_id.startswith("$") or track_id in keep:
            continue
        data = load_json(tracks_dir / f"{spec['from']}.json")
        data.update(spec.get("override", {}))
        dump_json(tracks_dir / f"{track_id}.json", data)
        art = art_dir / f"{spec['from']}.png"
        if art.exists():
            shutil.copy2(art, art_dir / f"{track_id}.png")
        placeholders[track_id] = spec["from"]
        keep.add(track_id)
    # After the placeholders, so a placeholder takes its source's file as it
    # was and gets its own overrides (race_laps, speed_mult) on top.
    for track_id, over in manifest.get("track_overrides", {}).items():
        if track_id.startswith("$"):
            continue
        path = tracks_dir / f"{track_id}.json"
        if not path.exists():
            continue
        data = load_json(path)
        if "race_laps" in over:
            data["lap_modifier"] = round(over["race_laps"] / 50, 4)
        for sector in data["micro_sectors"] if "speed_mult" in over else []:
            sector["target_speed_kmh"] = round(sector["target_speed_kmh"] * over["speed_mult"], 1)
        data.update({k: v for k, v in over.items() if k not in ("race_laps", "speed_mult")})
        dump_json(path, data)
    # A placeholder's source track leaves again unless the season races it
    # (or it is the season's own track, which always ships).
    own = {p.stem for p in (season_dir / "tracks").glob("*.json")}
    keep -= sources - raced - own
    keep.add("testtrack")
    for track in tracks_dir.glob("*.json"):
        if track.stem not in keep:
            track.unlink()
            (art_dir / f"{track.stem}.png").unlink(missing_ok=True)
    return placeholders


def strip_notes(out):
    """Drop our "$..." note keys ("$comment" and the like) from every JSON file
    in the pack. They are notes for us; the game's own files never have them,
    and a player reported a pack file with one as invalid (2026-11-15)."""
    def clean(d):
        if isinstance(d, dict):
            return {k: clean(v) for k, v in d.items() if not k.startswith("$")}
        if isinstance(d, list):
            return [clean(v) for v in d]
        return d
    changed = []
    for path in sorted(out.rglob("*.json")):
        try:
            data = load_json(path)
        except (ValueError, UnicodeDecodeError):
            continue                      # validate() reports broken JSON
        tidy = clean(data)
        if tidy != data:
            dump_json(path, tidy)
            changed.append(path.relative_to(out).as_posix())
    return changed


def validate(out):
    errors, warnings = [], []
    teams = load_json(out / "teams.json")
    drivers = load_json(out / "drivers.json")
    engines = load_json(out / "engines.json")["suppliers"]
    tyres = load_json(out / "tyre_suppliers.json")["suppliers"]
    staff = load_json(out / "staff.json")
    schedule = load_json(out / "schedule.json")
    team_names = {t["name"] for t in teams}

    if len(team_names) != len(teams):
        errors.append("teams.json: duplicate team names")
    for team in teams:
        if team.get("engine_supplier") not in engines:
            errors.append(f"team {team['name']}: unknown engine supplier {team.get('engine_supplier')!r}")
        supplier = team.get("tyre_contract", {}).get("supplier")
        if supplier not in tyres:
            errors.append(f"team {team['name']}: unknown tyre supplier {supplier!r}")
        if team.get("entry_count", 2) > 3:
            errors.append(f"team {team['name']}: entry_count above 3 is not supported by formula_team_entry_cap")
        mains = [d for d in drivers if d.get("team") == team["name"] and d.get("contract", {}).get("role") == "main"]
        if team.get("active", True) and len(mains) != team.get("entry_count", 2):
            errors.append(f"team {team['name']}: entry_count {team.get('entry_count')} but {len(mains)} main drivers")

    numbers = {}
    for driver in drivers:
        if driver.get("team") and driver["team"] not in team_names:
            errors.append(f"driver {driver['name']}: unknown team {driver['team']!r}")
        if driver.get("team") and "number" in driver:
            if driver["number"] in numbers:
                errors.append(f"number {driver['number']} used by {numbers[driver['number']]} and {driver['name']}")
            numbers[driver["number"]] = driver["name"]
        for skill in ("cornering", "braking", "consistency", "smoothness", "control"):
            if not 1 <= driver.get(skill, 0) <= 20:
                errors.append(f"driver {driver['name']}: {skill} must be 1-20")

    for member in staff:
        if member.get("team") and member["team"] not in team_names:
            errors.append(f"staff {member['name']}: unknown team {member['team']!r}")

    if len(schedule) != 52:
        errors.append(f"schedule.json: expected 52 weeks, got {len(schedule)}")
    track_ids = {p.stem for p in (out / "tracks").glob("*.json")}
    for week, slot in enumerate(schedule, start=1):
        if slot not in SCHEDULE_KEYWORDS and slot not in track_ids:
            errors.append(f"schedule week {week}: track {slot!r} has no tracks/{slot}.json")
    for track in track_ids:
        if not (out / "assets" / "tracks" / f"{track}.png").exists():
            warnings.append(f"track {track}: no overview image assets/tracks/{track}.png")
    for team in teams:
        if not (out / "assets" / "Cars" / f"{team['name'].replace(' ', '')}.png").exists():
            warnings.append(f"team {team['name']}: no car image")
    return errors, warnings


def build(season_dir, game, install, private_audio=True, private_art=True):
    manifest = layers.manifest(season_dir)
    chain = layers.chain(season_dir)
    base_dir = game / "data" / manifest["base_pack"]
    if not base_dir.is_dir():
        sys.exit(f"base pack not found: {base_dir}")
    out = REPO / "dist" / manifest["pack_folder"]
    if out.exists():
        # An Explorer window open inside dist/ holds its folder; keep such a
        # folder (it is emptied) instead of failing the whole build.
        held = []
        shutil.rmtree(out, onexc=lambda fn, path, exc: held.append(path))
        for path in held:
            if Path(path).is_file():
                sys.exit(f"cannot remove {path}: in use by another program")
        if held:
            print(f"note: {len(held)} folder(s) in dist/ are open in another program and were kept empty")
    shutil.copytree(base_dir, out, dirs_exist_ok=True)

    art_root = out / "assets"
    for sub in FICTIONAL_ASSET_DIRS:
        if sub != "tracks" and (art_root / sub).is_dir():
            shutil.rmtree(art_root / sub)
            (art_root / sub).mkdir()

    data_files = layers.files(season_dir, "data")
    for name, src in data_files.items():
        dump_json(out / name, expand_templates(name, load_json(src), base_dir))

    if "team_clones" in manifest:
        clone_team_records(out, manifest["team_clones"], set(data_files))
    if "sponsors" in manifest:
        apply_sponsors(out, manifest["sponsors"])
    if manifest.get("no_title_sponsors"):
        strip_title_sponsors(out)
    readable_team_text(out)
    if "staff" in manifest and "staff.json" not in data_files:
        generate_staff(out, base_dir, manifest["staff"], load_json(out / "teams.json"))

    for layer in chain:
        patch = layer / "patches" / "regulations.json"
        if patch.exists():
            dump_json(out / "regulations.json", patch_regulations(load_json(out / "regulations.json"), load_json(patch)))
        # config.json (race physics: dirty air, slipstream, DRS...) is deep-merged;
        # keys starting with "$" are comments.
        patch = layer / "patches" / "config.json"
        if patch.exists():
            body = {k: v for k, v in load_json(patch).items() if not k.startswith("$")}
            dump_json(out / "config.json", deep_merge(load_json(out / "config.json"), body))

    constants = out / "constants.py"
    raw = constants.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in raw else "\n"
    patched = patch_constants(raw.replace("\r\n", "\n"), manifest.get("constants", {}))
    constants.write_bytes(patched.replace("\n", eol).encode("utf-8"))

    options = out / "options.json"
    if options.exists():
        dump_json(options, {**load_json(options), "last_save": None})

    placeholders = place_tracks(season_dir, out, manifest)

    # "vanilla_music": false drops the base pack's menu tracks, so the game
    # plays only the season's own assets/audio/music (it plays every file there).
    if manifest.get("vanilla_music", True) is False:
        music = art_root / "audio" / "music"
        if not any((layer / "assets" / "audio" / "music").glob("*") for layer in chain):
            sys.exit("vanilla_music is false, but no layer ships assets/audio/music")
        shutil.rmtree(music, ignore_errors=True)
    for layer in chain:
        if (layer / "assets").is_dir():
            shutil.copytree(layer / "assets", art_root, dirs_exist_ok=True)
    # A placeholder of one of our own tracks only finds its image now (before the source's image may go below).
    for track_id, source in placeholders.items():
        art = art_root / "tracks" / f"{source}.png"
        if art.exists() and not (art_root / "tracks" / f"{track_id}.png").exists():
            shutil.copy2(art, art_root / "tracks" / f"{track_id}.png")
    # A base's track images for venues this season doesn't race.
    for layer in chain[:-1]:
        for art in (layer / "assets" / "tracks").glob("*.png"):
            if not (out / "tracks" / f"{art.stem}.json").exists() and art.stem not in placeholders:
                (art_root / "tracks" / art.name).unlink(missing_ok=True)

    dump_json(out / "workshop.json", {
        "schema_version": 1,
        "app_id": 4340600,
        "series": manifest.get("series", "formula"),
        "title": manifest["title"],
        "content_type": "season",
        "pack": {"source_name": manifest["pack_folder"]},
        "version": manifest["version"],
    })
    readme = [layer / "README.txt" for layer in chain if (layer / "README.txt").exists()]
    if readme:
        shutil.copy2(readme[-1], out / "README.txt")
    # Credits: the season's own text first, then each base's (tracks, makers...).
    credits = [(layer / "credits.txt").read_text(encoding="utf-8").strip("\n") for layer in reversed(chain)
               if (layer / "credits.txt").exists()]
    if credits:
        with open(out / "credits.txt", "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n\n".join(credits) + "\n")
    portraits = layers.merged_json(season_dir, "art/portraits.json")
    if portraits and (out / "credits.txt").exists():
        lines = ["", "Driver portraits (assets/portraits), free-licence photos from Wikimedia Commons:"]
        for name, c in sorted(portraits.items()):
            if c.get("source") == "photo":
                lines.append(f"  {name}: {c['author'] or 'unknown author'}, {c['license']} - {c['page']}")
        lines.append("  Photos are cropped to the head and shoulders; a few close-ups have")
        lines.append("  their edges extended with a blurred copy of the photo.")
        lines.append("  Drivers without a free photo have a drawn helmet card.")
        with open(out / "credits.txt", "a", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
    # Sound sets cleared for release ("audio": {"in_pack": true}, in the era
    # base or the season) are baked into dist/, so they ship with the pack:
    # the era's set first, a season's own set on top (layers.audio_sets).
    # The files themselves stay in private/engine_audio (gitignored).
    # See tools/engine_audio/README.md.
    sound_sets = layers.audio_sets(season_dir)
    baked = [s["overlay"] for s in sound_sets if s.get("in_pack")]
    private_sets = [s["overlay"] for s in sound_sets if not s.get("in_pack")]
    if baked:
        sys.path.insert(0, str(Path(__file__).with_name("engine_audio")))
        import overlay
        missing = [s for s in baked if not overlay.overlay_for(s)]
        if missing:
            sys.exit(f"audio in_pack, but no overlay built at private/engine_audio/pack/{missing[0]}; run tools/engine_audio/package.py")
        print(overlay.bake(out, baked))

    for rel in strip_notes(out):
        print(f"notes stripped: {rel}")
    errors, warnings = validate(out)
    for track_id, source in placeholders.items():
        print(f"placeholder: track {track_id} uses geometry of base track {source}")
    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        sys.exit(f"{len(errors)} error(s); pack left at {out} for inspection")
    print(f"built {out}")

    if install:
        target = game / "data" / manifest["pack_folder"]
        # Copy over in place instead of deleting first: the running game keeps
        # some pack files (music) open, and a failed delete must never leave a
        # half-removed pack behind. Stale files are removed only where possible.
        try:
            shutil.copytree(out, target, dirs_exist_ok=True)
        except shutil.Error as err:
            for src, dst, why in err.args[0]:
                print(f"warning: not updated (in use by the game? restart it and reinstall): {dst} ({why})")
        fresh = {p.relative_to(out) for p in out.rglob("*")}
        for path in sorted(target.rglob("*"), reverse=True):
            if path.relative_to(target) not in fresh:
                try:
                    path.rmdir() if path.is_dir() else path.unlink()
                except OSError as err:
                    print(f"warning: could not remove stale {path.relative_to(target)}: {err}")
        print(f"installed to {target} (select it in-game or via active_pack.json)")
        # Private engine audio (private/engine_audio, never in dist/ or git) goes
        # onto the installed copy only. See tools/engine_audio/README.md.
        if private_audio and private_sets:
            sys.path.insert(0, str(Path(__file__).with_name("engine_audio")))
            import overlay
            if any(overlay.overlay_for(s) for s in private_sets):
                print(overlay.apply(target, [s["overlay"] for s in sound_sets], manifest["pack_folder"]))
                print("  NOTE: this installed pack now holds private audio; do not upload it to the Workshop")
        # Private menu background (private/menu_art, never in dist/ or git; see
        # tools/menu_art.py) goes onto the installed copy only, like the audio.
        own_title_bg = (season_dir / "assets" / "title_bg.png").exists()   # free, ships in the pack
        if private_art and own_title_bg:
            print("menu background: the pack's own assets/title_bg.png (no private overlay)")
        if private_art and not own_title_bg:
            import menu_art
            title_bg = menu_art.private_title_bg(season_dir)
            if title_bg.exists():
                (target / "assets").mkdir(exist_ok=True)
                shutil.copy2(title_bg, target / "assets" / "title_bg.png")
                spec = menu_art.active_photo(season_dir)
                with open(target / "credits.txt", "a", encoding="utf-8", newline="\n") as fh:
                    fh.write(f"\nMain menu background (assets/title_bg.png, this install only):\n"
                             f"  {spec.get('caption', '')}\n  {spec.get('rights', '')} - {spec.get('page', '')}\n")
                print(f"menu background: {title_bg.relative_to(REPO)}")
                print("  NOTE: this installed pack now holds a press photo; do not upload it to the Workshop")
            elif (season_dir / "art" / "menu.json").exists():
                print(f"warning: no {title_bg.relative_to(REPO)}; run tools/menu_art.py {season_dir.relative_to(REPO)}")
        # Keep the mod browser (private/mod_browser, see tools/mod_browser.py) in
        # sync with what is installed.
        sys.path.insert(0, str(Path(__file__).parent))
        import mod_browser
        try:
            mod_browser.build(season_dir, game)
        except Exception as err:          # the browser is a view; never fail an install over it
            print(f"warning: mod browser not rebuilt: {err}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("season", type=Path, help="season source folder, e.g. seasons/dtm-1991")
    parser.add_argument("--game", help="Team Principal install folder (else local.json, else default)")
    parser.add_argument("--install", action="store_true", help="copy the built pack into <game>/data/")
    parser.add_argument("--no-private-audio", action="store_true",
                        help="install without the private engine-audio overlay (tools/engine_audio)")
    parser.add_argument("--no-private-art", action="store_true",
                        help="install without the private menu background (tools/menu_art.py)")
    args = parser.parse_args()
    build(args.season.resolve(), game_path(args.game), args.install, not args.no_private_audio,
          not args.no_private_art)


if __name__ == "__main__":
    main()
