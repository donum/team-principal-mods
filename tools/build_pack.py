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
    tracks/<id>.json   our own traced tracks
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


def generate_staff(out, base_dir, spec, teams):
    """Fill every team with one placeholder staff member per role.

    Real 1991 engineers are mostly undocumented, so names come from the
    game's nationality name pool and skills scale with the team's level.
    Records listed in spec["named"] (researched people) take precedence.
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
    for team in teams:
        level = levels[team["name"]]
        filled = {s["role"] for s in named if s.get("team") == team["name"]}
        pool = pools.get(team["nationality"]) or pools["german"]
        for role in roles:
            if role in filled:
                continue
            tpl = copy.deepcopy(templates[role])
            for _ in range(200):
                name = f"{rng.choice(pool['first_names'])} {rng.choice(pool['last_names'])}"
                if name not in used:
                    break
            used.add(name)
            jitter = lambda: max(1, min(20, level + rng.randint(-2, 2)))
            tpl.update({
                "name": name,
                "team": team["name"],
                "skill": jitter(),
                "age": rng.randint(32, 58),
                "nationality": team["nationality"] if team["nationality"] in pools else "german",
                "skills": {k: jitter() for k in tpl["skills"]},
                "talent": {k: min(20, jitter() + 2) for k in tpl["talent"]},
                "contract": {"team": team["name"], "length_weeks": 104,
                             "salary_m": round(spec.get("salary_per_level_m", 0.1) * level, 2), "start_week": 1},
            })
            staff.append(tpl)
    dump_json(out / "staff.json", staff)


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
    needed = set(load_json(out / "schedule.json")) - SCHEDULE_KEYWORDS
    needed |= {spec["from"] for spec in manifest.get("track_placeholders", {}).values()}
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
    for track_id, over in manifest.get("track_overrides", {}).items():
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
    placeholders = {}
    for track_id, spec in manifest.get("track_placeholders", {}).items():
        if track_id in keep:
            continue
        data = load_json(tracks_dir / f"{spec['from']}.json")
        data.update(spec.get("override", {}))
        dump_json(tracks_dir / f"{track_id}.json", data)
        art = art_dir / f"{spec['from']}.png"
        if art.exists():
            shutil.copy2(art, art_dir / f"{track_id}.png")
        placeholders[track_id] = spec["from"]
        keep.add(track_id)
    keep.add("testtrack")
    for track in tracks_dir.glob("*.json"):
        if track.stem not in keep:
            track.unlink()
            (art_dir / f"{track.stem}.png").unlink(missing_ok=True)
    return placeholders


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


def build(season_dir, game, install, private_audio=True):
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

    constants = out / "constants.py"
    raw = constants.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in raw else "\n"
    patched = patch_constants(raw.replace("\r\n", "\n"), manifest.get("constants", {}))
    constants.write_bytes(patched.replace("\n", eol).encode("utf-8"))

    options = out / "options.json"
    if options.exists():
        dump_json(options, {**load_json(options), "last_save": None})

    placeholders = place_tracks(season_dir, out, manifest)

    for layer in chain:
        if (layer / "assets").is_dir():
            shutil.copytree(layer / "assets", art_root, dirs_exist_ok=True)
    # A base's track images for venues this season doesn't race.
    for layer in chain[:-1]:
        for art in (layer / "assets" / "tracks").glob("*.png"):
            if not (out / "tracks" / f"{art.stem}.json").exists() and art.stem not in placeholders:
                (art_root / "tracks" / art.name).unlink(missing_ok=True)
    # A placeholder of one of our own tracks only finds its image now.
    for track_id, source in placeholders.items():
        art = art_root / "tracks" / f"{source}.png"
        if art.exists() and not (art_root / "tracks" / f"{track_id}.png").exists():
            shutil.copy2(art, art_root / "tracks" / f"{track_id}.png")

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
        if private_audio:
            sys.path.insert(0, str(Path(__file__).with_name("engine_audio")))
            import overlay
            sound = layers.audio_overlay(manifest)
            if overlay.overlay_for(sound):
                print(overlay.apply(target, sound, manifest["pack_folder"]))
                print("  NOTE: this installed pack now holds private audio; do not upload it to the Workshop")
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
    args = parser.parse_args()
    build(args.season.resolve(), game_path(args.game), args.install, not args.no_private_audio)


if __name__ == "__main__":
    main()
