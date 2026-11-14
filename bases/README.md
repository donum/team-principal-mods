# Era bases

A **base** holds what a whole generation of DTM cars shares. A **season**
(`seasons/dtm-<year>/`) names its base and adds only what is its own. Each
season still builds into one full, standalone Workshop pack: the game has no
way to make one pack depend on another (see
[CAPABILITIES.md](../docs/CAPABILITIES.md), "Completeness"). The base exists
only in this repository.

```
bases/dtm-era3/          DTM 2000–2011: Masters, 4.0 V8 silhouettes, Dunlop ("era 3"); mother season 2003
bases/dtm-era4/          DTM 2012–2018: New DTM, 4.0 V8   ("era 4" in docs/ERAS.md); mother season 2013
bases/dtm-era5/          DTM 2019–2020: Class One 2.0 turbo, on top of dtm-era4 ("era 5"); mother season 2020
bases/f1-v8/             F1 2010–2013: 2.4 V8, Pirelli from 2011 (plan: docs/plans/F1_V8.md)
  base.json              shared build settings: base pack, constants, shared
                         tracks, and the "audio" section (private sounds)
  gen.json               generator defaults: rules, car profiles, engines, tyres,
                         chassis names per make and year
  data/                  shared data files (tyres, damage, punctures, pit crews,
                         part names, radio)
  patches/regulations.json
  tracks/ track_specs/   traced venues, shared by every season
  assets/                shared images (tracks, engine and tyre logos)
  art/logos.json         sources of the shared logos (tools/logo_art.py)
  credits.txt            credits for the shared content
seasons/dtm-2012/, seasons/dtm-2013/
                         "base": "dtm-era4"
  season.json gen.json   only the season's own values
  data/                  teams, drivers, engines, tyre suppliers, schedule
  assets/ art/           car images, team logos, portraits
  research/              sourced facts of the year
```

## What goes where

| In the base | In the season |
|---|---|
| Rules and points that hold for the generation | Teams, drivers, numbers, sponsors |
| Tyre model, damage, car part names | Calendar (`gen.json` `tracks`) |
| Traced tracks and their lap-time calibration | Car images and liveries |
| Engine and tyre logos, car profiles, chassis names | Team logos, driver portraits |
| Private engine sounds | Anything that differs that year |

Whatever a season puts in its own folder replaces the base's version. So when
one year differs from the rest of its generation, the season overrides only
that piece:

- **A data file** (`data/tyremodel.json`...): the season's file replaces the
  base's file.
- **Rules:** a season's `patches/regulations.json` is applied after the base's.
  For example 2012 (no DRS, no option tyre) sets `"drs_policy": {"default":
  "disabled"}` and ships its own `data/tyremodel.json`.
- **Generator settings:** a season's `gen.json` is merged over the base's.
  A changed engine is `"engines": {"BMW": {"engine": "..."}}`.
- **Constants and tracks:** a season's `season.json` is merged over the base's
  `base.json` (also `track_overrides`, e.g. `"speed_mult"` for a year whose
  cars were faster).
- **An image:** a file in the season's `assets/` replaces the base's file of
  the same name.
- **Tracks:** a base's tracks (and `shared_tracks`) go into a season's pack
  only when that season races them, so 2013 doesn't carry Valencia.

[seasons/dtm-2012](../seasons/dtm-2012) is the worked example: its
`patches/regulations.json` turns DRS and the two-compound rule off, its
`data/tyremodel.json` has one dry tyre, and its `gen.json` sets the lighter
cars and three race distances.

How the layers merge is written down in [tools/layers.py](../tools/layers.py).
A base can have a base of its own (`"base"` in `base.json`), for content
shared across eras.

## Add a season to a base (e.g. DTM 2014)

1. Research first: `seasons/dtm-2014/research/` (calendar, entries,
   standings).
2. Write `seasons/dtm-2014/gen.json`. The smallest one that builds:

   ```json
   {
     "base": "dtm-era4",
     "year": 2014,
     "title": "DTM 2014 - Deutsche Tourenwagen Masters",
     "tracks": {"1": "hockenheim13", "2": "oschersleben", "3": "hungaroring", "...": "..."},
     "track_placeholders": {"hungaroring": {"from": "redbullring", "override": {"name": "Hungaroring"}}}
   }
   ```

   Then add what 2013's `gen.json` has: `teams` (names, colours,
   `previous_position`, histories) and `sponsors`.
3. Generate and build:

   ```bash
   python tools/season_from_research.py seasons/dtm-2014
   ```

   ```bash
   python tools/build_pack.py seasons/dtm-2014 --install
   ```

   `--install` also puts the base's private sounds on the installed pack and
   rebuilds its mod browser.
4. Season art: car images (`tools/car_drawings.py`), team logos
   (`tools/logo_art.py seasons/dtm-2014`), portraits
   (`tools/portrait_art.py`).
5. New venues: trace them into the **base** (`bases/dtm-era4/track_specs/`,
   `tools/osm_track.py`), so later seasons get them too, and replace the
   placeholder in `gen.json`.

## Start a new era base

1. Create `bases/<id>/base.json` with `base_pack`, `series`, the shared
   `constants`, and (for private sounds) an `"audio"` section.
2. Move the content every season of the era shares out of the first season
   into the base, using the table above.
3. Put `"base": "<id>"` in each season's `gen.json`, re-run
   `tools/season_from_research.py`, and check that `dist/` is unchanged.

The Group A seasons (1987, 1990–1992) don't use a base yet: they share rules and
tracks through `"template": "dtm-1991"` and `shared_tracks`. Both still work.

## Mother seasons

Each base is tuned on one **mother season**: the first year of the era we
build. Its sounds, rules and car profiles are the era's defaults, and every
later year of the era inherits them and overrides only what differs. The
mother is named in `base.json` `"audio": {"research_season": ...}`.

| Base | Mother | Seasons on it | Sounds |
|---|---|---|---|
| (Group A template `dtm-1991`) | 1991 | 1987, 1990, 1992 | vanilla, none collected yet |
| `dtm-era3` | 2003 | 2006, 2010 | vanilla, none collected yet (`"in_pack": false`) |
| `dtm-era4` | 2013 | 2012, 2018 | private overlay from 2012 and 2013 recordings |
| `dtm-era5` | 2020 | (2019 later) | vanilla, none collected yet; overrides era 4's V8 overlay |

A base with `"in_pack": false` and no recordings leaves the game's own
engine sounds in the pack. When recordings of the mother season's cars are
collected (`tools/engine_audio`, `ENGINE_AUDIO_BASE=<base id>` with its own
`ENGINE_AUDIO_DATA`), every season on the base gets them.

## Sounds

The private engine sounds are built once per base, not per year
(`tools/engine_audio`, settings in `base.json` `"audio"`). Every installed
season on the base gets the same overlay: `build_pack.py --install` applies
it, and `tools/engine_audio/package.py --install` refreshes it on all of them.
The sounds stay private: never in git, `dist/` or the Workshop.
