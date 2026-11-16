# Team Principal Modding: Capabilities and Limits

This is a living reference for what a Team Principal data pack can change and
what it can't. It's based on game version **0.99.5** (the `VERSION` constant), with the
0.99.6 beta's new keys in [section 3a](#3a-new-in-0996)
(0.99.6 released 2026-11-11, Patch #1 2026-11-15; patch impact on our packs is
tracked in [game/changelog.csv](game/changelog.csv) by `tools/game_changelog.py`)
and on the installed default packs (`default22` to `default26`) plus eight
community Workshop seasons, as of 2026-11-01.

Status legend:

- ✅ **Confirmed.** Seen in game files or in working Workshop packs.
- 🧪 **To test.** Plausible from the data, but not yet verified in-game.
- ❌ **Not supported.** Needs an approximation.

---

## 1. How packs work

| Topic | Finding | Status |
|---|---|---|
| Location | Formula packs live in `<game>/data/<pack>/`. Oval packs live in `<game>/data/oval/<pack>/`. | ✅ |
| Active pack | `<game>/active_pack.json` holds `{"active_pack": "<folder>"}`. Oval uses `active_oval_pack.json`. | ✅ |
| Workshop installs | Workshop items are copied to `data/workshop_<itemId>/` and tracked in `<game>/.workshop/registry.json`. | ✅ |
| Pack manifest | `workshop.json` with `schema_version`, `app_id: 4340600`, `series` (`formula`/`oval`), `title`, `content_type: "season"`, `pack.source_name`, `version`. | ✅ |
| Completeness | Every Workshop season ships a **full** pack (all ~30 JSON files, `constants.py`, `tracks/`, `assets/`). There's no evidence of partial or overlay packs. | ✅ (partial packs ❓) |
| `constants.py` | Python that the game **executes** (`from ui.theme import UITheme`). Holds start year, points, grid size, salaries, development tuning. | ✅ |
| Local test packs | Copying a folder into `data/` and pointing `active_pack.json` at it should work like the defaults. | 🧪 |

> ⚠️ **Security note.** `constants.py` is arbitrary Python that runs with the
> game. Our packs only change literal values in it, and the build tool checks
> that. Never run a `constants.py` from an untrusted pack without reading it.

## 2. Data files, and what they mean for DTM

| File | Holds | DTM 1991 use |
|---|---|---|
| `constants.py` | `SEASON_START_YEAR`, `POINTS_TOP10`, `QUALI_GRID_LIMIT`, `QUALI_MIN_ENTRANTS`, salary scales, dev tuning | Year 1991, grid size (~30 entries), salary scale (DTM budgets were much smaller than F1) |
| `teams.json` | Team name, colours, prestige, balance, HQ levels, car ratings (braking, acceleration, pace, slow/med/high/straight), `car_mass_kg`, reliability, tyre contract, engine contract, `entry_count`, history, nationality | One record per entrant (AMG, Zakspeed, Schnitzer, Linder, Bigazzi, MM Diebels, SMS, Isert, Irmscher, Snobeck...) |
| `drivers.json` | Name, team, number, 5 skills (1–20), talent, age, contract, traits, personalities, career stage, nationality, optional `pay_driver_amount_m` | Full 1991 driver roster plus free agents and youngsters |
| `staff.json` | Roles: `technical_director`, `chief_designer`, `head_of_aero`, `head_of_engine`, `head_of_dynamics`, `chief_mechanic` | Team managers and engineers. There's no "team principal" role: the player is the principal. |
| `engines.json` | Suppliers with `power_rating`, `reliability_rating`, `fuel_efficiency`, `mass_kg`, `cost_m`, `factory` (works), unit rules | BMW S14 2.5, Mercedes M102 2.5-16 (AMG/Cosworth head), Audi 3.6 V8, Opel C30SE 3.0 (Irmscher) |
| `tyre_suppliers.json` | Supplier grip, durability and temperature per compound, development | Yokohama, Pirelli, Dunlop, Michelin, Bridgestone (assignment per team from research) |
| `schedule.json` | **52-slot array, one slot per week**. Each slot is `null`, `"private"`, `"test"` or a track id. | 1991 calendar |
| `tracks/*.json` | Length, polyline `points` for the map, `micro_sectors` (straight/low/med/high with target speeds), DRS zones, pit loss, tyre wear, fuel use, overtaking difficulty, DNF modifier, grid layout | Zolder, Hockenheim, Nürburgring, AVUS, Wunstorf, Norisring, Diepholz, Alemannring... |
| `assets/tracks/<id>.png` | Track overview image | Our own traced layouts |
| `regulations.json` | Rule categories with data-driven options (points tables, min weight, car speed profile, refuelling, DRS, ERS...) plus voting / scripted change control | See §3 |
| `car_parts.json` | Manufactured part types with **labels**, wear, cost, stock | Maybe relabel as touring-car parts (splitter, rear spoiler...) 🧪 |
| `sponsors.json`, `starting_sponsors.json` | Sponsor pool (name, tier type, amount, industry, nationality) | Period sponsors (to keep trademark risk low, see LICENSE-CONTENT) |
| `junior_series.json` | Feeder series (no fixed limit; unique `series_abbreviation`) with teams (colours, `quality`), drivers, a 52-week schedule and points. Listed drivers are matched by name to free drivers in `drivers.json` (`team` null, no contract, inside the age band) and seated in season 1 only; empty seats get random free drivers. A result is skill + 2 × quality + luck; the track id is only a label; one race per week. `tier` must match `driverslicense.json`. ✅ (read from the game code, 2013 pack) | DTM 2013: FIA F3 Europe, Porsche Carrera Cup Deutschland, German F3, ADAC Formel Masters, ADAC Procar (DTC) |
| `team_histories.json`, `team_ownership.json`, `team_buyouts.json`, `relationships.json`, `events.json`, `radio_quotes.json` | Flavour and economy | Era storylines |
| `headquarters.json`, `startingtechnologies.json`, `ers_development.json`, `parts.json`, `tyremodel.json`, `config.json` | Mechanics tuning | Mostly inherit, turn off ERS |
| `assets/Cars/<TeamName>.png`, `assets/logos/`, `assets/engines/`, `assets/portraits/`, `assets/sponsors/` | Images, mapped by name with spaces removed (`Red Boar` → `RedBoar.png`) | Our own side-profile car drawings in team colours |
| `assets/title_bg.png`, `dashboard_bg*.png`, `assets/audio/` | Menu and dashboard art, sound and music | DTM-flavoured menu art (our own) |
| `assets/dashboard_bgs/<TeamName><N>.png` | Dashboard art for one team, numbered like the pack set (`BMWTeamSchnitzer.png`, `BMWTeamSchnitzer2.png`...). Name with letters and digits only: spaces and hyphens go (`STIHL AMG-Mercedes` → `STIHLAMGMercedes.png`). When the player's team has a set, it replaces the pack set. Several images per team work and the dashboard moves through them. ✅ (tested with DTM 2013) | Team-specific dashboard art |

### Track geometry (confirmed in-game)

- **`points` don't have to be image pixels.** By default the game fits the
  points' bounding box into a box about 790 px wide, centred on the overview
  image. Cars then run on a shrunken copy of the track.
- **`"use_raw_canvas_coordinates": true` with `"raw_canvas_size": [1044, 1080]`**
  makes the points exact image pixels. The base `spain.json` uses this, and so
  do all our generated tracks. ✅
- **The race screen covers the bottom of the map** with driver cards and the
  event log, so keep the racing line above y ≈ 800 on a 1080 px tall image. ✅
- **The overview image is stretched to fill the map panel, not fitted.** The
  panel is about 55% of the window width (1044/1920) and the full height
  under the title bar. Width and height scale separately, so the track
  changes shape with the window. Measured in qualifying at 1776×423 px:
  ×0.935 across, ×0.392 down. The whole image always shows. Only the
  session header (top) and the status bar (bottom) cover it, and they have
  fixed screen heights, so they hide more of the image in a short window:
  about 33 image px at the top and everything below y ≈ 954 in that window. ✅
  At 3840×2160 (16:9, measured 2026-11-10 from 47 screenshots registered
  to the track images): ×1.99 on both axes from the window's top-left, so
  the panel shows image x 9–1035, y 124–870; the driver cards cover
  y 788–870 in the race and the north arrow x < 80, y < 210. Tracks for
  this pack keep the whole lap inside (9, 124, 1035, 788) with 16 px padding
  (`tools/art_track.py`, race-track-themes `tools/reframe_2013.py`).
- **`lap_modifier` sets race length.** A race runs `options.json` `laps` ×
  `lap_modifier` laps. Confirmed from a save: Zolder 50 × 1.12 = 56 laps,
  Hockenheim 50 × 0.9 = 45. ✅
- **Lap time follows the micro-sector target speeds.** Some base tracks also
  have an undocumented `track_time_mult` (Shanghai 1.2). 🧪
- **Track art isn't cached in your save.** A career save only stores
  `data_pack`, so updated tracks show up after a reinstall and game restart. ✅

## 3. Rules: what's data-driven

`regulations.json` options carry their own values, so you can add new options
with custom values. Proven example: default26 adds a `top12` points option
that older packs don't have.

| Need (DTM 1991) | Mechanism | Status |
|---|---|---|
| DTM points table per race | `points_system` option with a custom `points` array, plus `POINTS_TOP10` in `constants.py` | ✅ data, any length (checked in the 0.99.6 code) |
| No DRS, no ERS | `drs_policy: disabled`, `ers_policy: disabled` | ✅ |
| No refuelling | `formula_refueling: banned` | ✅ |
| Grid speed of heavy Group A saloons | `car_profile` option with corner/accel/braking/drag multipliers (custom "touring" option) | ✅ data / 🧪 custom key |
| Minimum weight | `chassis_minimum_weight` option `min_car_mass_kg` (1991 base ~1,000+ kg, varies by displacement) | ✅ data |
| Multi-car teams (AMG and Zakspeed ran 3+ cars) | `formula_team_entry_cap` (`one`/`two`/`three`), `formula_team_entry_requirement` `variable`, team `entry_count` | ✅ up to 3; more than 3 ❌ (`entry_count` is cut to 3) |
| Grid size of ~30 cars | `QUALI_GRID_LIMIT`, `PREQUALIFYING_*` in `constants.py` | ✅ |
| 107% rule | `config.json` `quali_107_rule` (`enabled`, `percent`); off when `enabled` is missing | ✅ (code) |
| Tyre sets per weekend | `weekend_tyre_allocation` option payload: `dry_sets_per_driver` (any number, null = unlimited), `intermediate_sets_per_driver`, `wet_sets_per_driver`. The allocation screen only knows soft, medium and hard. | ✅ (code) |
| Rule evolution over seasons | `change_control.mode` (`voting`), `scripted_changes` list | ✅ structure / 🧪 scripted format |

## 3a. New in 0.99.6

From the 0.99.6 beta's modding guide (2026-11-09), checked against the game
code. ✅ here means the key is in the code and our build writes it; 🧪 means
it hasn't been seen in a game yet.

| Feature | Key | What we use it for | Status |
|---|---|---|---|
| Shared pit crew per team | `config.json` `pitstops.double_stack_enabled` (default **on** for Formula packs) | Kept on in `dtm-era4`: team-mates queue in one box | ✅ code / 🧪 effect |
| Punctures | `config.json` `incidents.punctures` (off by default) | On in `dtm-era4`, game rates, `contact_prob` 0.04 | ✅ code / 🧪 effect |
| Chassis names | `teams.json` `chassis_prefix`, `chassis_names` {year: name}. The prefix keeps letters, digits and `/` (12 max) and gets the two-digit year. | Each make's real car per year 2012 to 2018 (`dtm-era4/gen.json` `chassis`) | ✅ code / 🧪 in game |
| Birth years | `drivers.json` `birth_year`, wins over `age`; age = `SEASON_START_YEAR` + season − 1 − birth year | Written from `entries.csv` birth dates (`gen.json` `birth_years`) | ✅ code |
| Safe `constants.py` | Workshop packs (`data/workshop_*`) are read with `workshop_manager.load_safe_constants`: literal values of whitelisted names only. Local packs are still executed (`main._load_constants`), with missing names taken from the built-in defaults. | Our build only writes literals, so both paths load it. `tools/simulate.py` now does the same step (`game_code.load_pack_constants`). | ✅ |
| Banned-aid cheating | `DRIVER_AID_*` in `constants.py` (whitelisted) | AI cheat chance 0.01 per team per season (vanilla 0.05) | ✅ |
| Espionage | `ESPIONAGE_*` in `constants.py` (whitelisted) | At most one operation per team and per grid per season (vanilla 2 and 4) | ✅ |
| Scripted test weeks | `regulations.json` `scripted_changes`, `calendar` rows `add_test` / `remove_test` | Not used: our test weeks are in `schedule.json` | ✅ documented |
| Season windows, team announcements, revivals, guaranteed events, supplier join/leave, factory programme ending, rebrand nationality | `events.json`, `team_buyouts.json` | Real joins and exits after the pack's year, from `docs/teams/dtm_game_events.csv` (`tools/real_history.py`, season.json `real_history`). Teams that join are inactive in `teams.json` and get a generated car from `entry_performance_tag`. The game keeps at least 10 teams (wishlist C10). No rebrands yet. | ✅ code / ✅ 8-season rollover test (dtm-2013) |
| Pay drivers, licence practice point | `drivers.json` `pay_driver_amount_m`, `driverslicense.json` `practicepoint` | Pay drivers from `docs/teams/dtm_driver_backing.csv` (amounts are estimates). `practicepoint` is 0: the DTM had no licence points for practice runs. | ✅ code / 🧪 in game |
| Car images and logos per season | `assets/cars/<Team>Season<N>.png`, `<Team><Year>.png`, `Season<N>/<Team>.png`, `<Year>/<Team>.png` (same for logos). Names lose every non-letter, non-digit. Found in `ui_assets.get_team_car_image`, not in the modding guide. | Teams that join later show their real debut livery. Use `Season<N>`: `<Year>` counts from `config.json` `start_year`, which our packs don't set. | ✅ code / 🧪 in game |
| Title sponsors | `sponsors.json` `"type": "title"` | Not used: the game puts the sponsor in front of the team name, and our names already hold it (wishlist C11) | ✅ code |
| Safety progression, staff role unlock years, staff with negative ages | `config.json`, `staff.json` | Not needed for 2012 to 2018 | ✅ documented |

## 3b. Announced for the next version

Confirmed by the developer on Discord (16 Nov 2026), not in 0.99.6 yet.
Check each against the next modding guide before our build writes it.

| Feature | Key (as given) | What we use it for | Wishlist |
|---|---|---|---|
| Ambience per track | `tracks.<track id>.crowd` / `.pa` = `{"file": ..., "gain": ...}`, optional, falls back to the pack-wide set | Crowd bed per venue from the broadcasts, local track announcer (Norisring 2018 PA) | E9 |
| Pass-by pools | `engines.json` `passby_audio` as a list of keys | Several recordings per make, so two Audis no longer fuse into one | E11 |
| Dashboard images in random order | not given yet | Every dashboard picture gets seen | E20 |

## 4. Gaps: not natively supported

| DTM reality | Problem | Proposed approximation |
|---|---|---|
| **Two heats per round** | One race per scheduled week | (a) Put heat 2 in the following week at the same track 🧪, or (b) one longer race with doubled points |
| **Displacement-based weight and success ballast** | No ballast mechanic | Bake typical weight into each team's `car_mass_kg`. Model the BMW/Mercedes/Audi balance through engine `mass_kg` and ratings. |
| **Audi quattro 4WD** | No drivetrain model | Higher `acceleration` and wet traction (team ratings), heavier mass |
| **Touring-car aero** (no wings or underfloor in the F1 sense) | The parts system is wing-based | Keep part keys, rename `label`s 🧪, and lower aero sensitivity |
| **Privateer customer cars** (Group A homologated cars bought from the manufacturer) | Engines are supplier contracts. The chassis is always team-built. | Customer engine contracts from works suppliers. Privateers get lower HQ levels. |
| **Grid of 30+ cars** | Limited to 3 entries per team | Split big organisations into entrant-name teams, as the real entry list did (e.g. "AMG Mercedes" and "MS-Jet Racing") |
| **Track layouts** | Need polyline `points` and `micro_sectors` | Trace our own overview images with `tools/Formula Track Editor/Formula Track Tracer.exe` |

## 5. Assets and IP rules (EULA §4)

- Free, non-commercial mods are explicitly allowed (§4.1–4.2).
- Mods must not contain "substantial proprietary assets" of the game (§4.3).
  That's why this repo stores only **our** files and copies base-game files
  from the local install at build time.
- Real-world trademarks and likenesses aren't covered by the game's
  permission (§4.7). Use names descriptively. Graphics must be our own drawings,
  not photos or official logos.
- Other mods (Workshop packs, AMS2 DTM 1991) are **inspiration only**. Don't
  copy their files or textures without the author's written permission.

## 6. Open questions to verify in-game

0. Does `team_pace` etc. accept the mass scale of touring cars (`car_mass_kg`
   around 840–1100) together with the engine `mass_kg`? Is engine mass
   added to chassis mass?

1. Does a pack in `data/<custom>` load when `active_pack.json` names it?
2. Are custom option keys in `regulations.json` (e.g. `dtm_1991`) accepted?
3. Can the same track appear in two consecutive weeks (heat 1 and heat 2)?
4. ~~Does `entry_count` above 3 work?~~ No: the 0.99.6 code cuts it to 3
   (`team_entry_count`).
5. Does relabelling `car_parts.json` parts carry through to the UI? Not
   everywhere: the race event log writes "FRONT WING DAMAGE" and "changed
   front wing" (seen in a 2013 race). The Factory and Parts Warehouse
   screens are still to check.
6. How does the schedule key resolve: by track file stem (`hoc`) or by `name`
   (`Hockenheim`)? Both styles appear in the wild.
7. Does a minimum mass above 1,000 kg break the speed model? Lap-time
   calibration is needed against real 1991 qualifying times.
