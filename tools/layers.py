"""Source layers: an era base under each season.

A season (seasons/<id>/, manifest season.json) may name a base with
"base": "<base id>". A base (bases/<id>/, manifest base.json) has the same
layout as a season and holds what a whole car generation shares: rules,
tyre and damage tuning, traced tracks, engine and tyre art, generator
defaults (gen.json) and the private sound overlay. A base may name its own
base, so a chain like "dtm" -> "dtm-era4" -> "dtm-2013" works.

Later layers win:
    manifests      deep-merged (dicts merge, other values replace, null removes)
    gen.json       deep-merged the same way (tools/season_from_research.py)
    data/, tracks/, track_specs/, art/portraits.json
                   per file: the season's file replaces the base's
    patches/regulations.json
                   every layer's patch is applied in order, base first
    assets/        copied base first, so a season's image replaces the base's
    credits.txt    the season's text first, then each base's

Standard library only (engine_audio/overlay.py imports it).
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SEASONS = REPO / "seasons"
BASES = REPO / "bases"


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def deep_merge(base, override):
    """Return base with override applied; dicts merge, everything else replaces.
    A null value in an override dict removes that key."""
    if isinstance(base, dict) and isinstance(override, dict):
        out = copy.deepcopy(base)
        for key, value in override.items():
            if value is None:
                out.pop(key, None)
            else:
                out[key] = deep_merge(out[key], value) if key in out else copy.deepcopy(value)
        return out
    return copy.deepcopy(override)


def source_dir(name: str) -> Path:
    """A season or base folder by id ("dtm-1991", "dtm-era4")."""
    for root in (SEASONS, BASES):
        if (root / name).is_dir():
            return root / name
    raise SystemExit(f"no season or base called {name!r} in seasons/ or bases/")


def manifest_file(folder: Path) -> Path:
    for name in ("season.json", "base.json"):
        if (folder / name).exists():
            return folder / name
    raise SystemExit(f"{folder} has neither season.json nor base.json")


def chain(folder: Path) -> list[Path]:
    """[root base, ..., folder]."""
    out, seen = [], set()
    while folder is not None:
        folder = Path(folder).resolve()
        if folder in seen:
            raise SystemExit(f"base cycle at {folder}")
        seen.add(folder)
        out.insert(0, folder)
        parent = load_json(manifest_file(folder)).get("base")
        folder = source_dir(parent) if parent else None
    return out


def manifest(folder: Path) -> dict:
    """The season's build manifest with its bases merged underneath."""
    merged = {}
    for layer in chain(folder):
        own = load_json(manifest_file(layer))
        merged = deep_merge(merged, {k: v for k, v in own.items() if not k.startswith("$")})
    return merged


def files(folder: Path, sub: str, pattern: str = "*.json") -> dict[str, Path]:
    """{file name: path} over all layers; a later layer's file wins."""
    found = {}
    for layer in chain(folder):
        for path in sorted((layer / sub).glob(pattern)) if (layer / sub).is_dir() else []:
            found[path.name] = path
    return dict(sorted(found.items()))


def layer_of(folder: Path, path: Path) -> Path:
    """The layer folder a file from files() comes from."""
    return next(layer for layer in chain(folder) if Path(path).resolve().is_relative_to(layer))


def gen_config(folder: Path, own: dict) -> dict:
    """A season's gen.json with its bases' gen.json merged underneath."""
    merged = {}
    if own.get("base"):
        for layer in chain(source_dir(own["base"])):
            if (layer / "gen.json").exists():
                merged = deep_merge(merged, load_json(layer / "gen.json"))
    merged = deep_merge(merged, own)
    merged.pop("$comment", None)
    return merged


def merged_json(folder: Path, rel: str) -> dict:
    """A dict file (like art/portraits.json) merged over all layers."""
    out = {}
    for layer in chain(folder):
        if (layer / rel).exists():
            out.update(load_json(layer / rel))
    return out


def audio_overlay(manifest_data: dict) -> str:
    """Id of the top sound set a pack gets (tools/engine_audio): the last
    layer's "audio": {"overlay": ...}; without one, the pack folder.
    audio_sets() gives the whole stack."""
    return manifest_data.get("audio", {}).get("overlay") or manifest_data["pack_folder"]


def audio_sets(folder: Path) -> list[dict]:
    """The sound sets a pack plays, bottom first.

    Any layer (era base or season) may hold a sound set: an "audio" section
    with its own "overlay" id. Each set's settings are the audio sections of
    its layer and the layers below, merged. A set fills only the slots it
    lists in "slots" (all when it has none); the sets below fill the rest,
    so a season can replace, say, its track loop and keep its era's pass-bys.
    A set with "inherit": false starts afresh (a new car generation on top
    of an older base). "in_pack" says whether a set may ship in dist/
    (build_pack.py bakes those); a set that is not built yet is skipped,
    so its slots keep the sets below or the game's own sounds."""
    stack, merged = [], {}
    for layer in chain(folder):
        own = load_json(manifest_file(layer)).get("audio") or {}
        merged = deep_merge(merged, {k: v for k, v in own.items() if not k.startswith("$")})
        if not own.get("overlay"):
            continue
        if own.get("inherit") is False:
            stack = []
        stack.append({**merged, "layer": layer.name})
    return stack


def seasons() -> list[Path]:
    return sorted(p for p in SEASONS.iterdir() if (p / "season.json").exists())


def seasons_on_overlay(overlay_id: str) -> list[Path]:
    """Seasons whose packs play this sound set, on its own or under another."""
    return [s for s in seasons() if overlay_id in (a["overlay"] for a in audio_sets(s))]


def season_for_pack(pack_folder: str) -> Path | None:
    return next((s for s in seasons() if load_json(s / "season.json").get("pack_folder") == pack_folder), None)
