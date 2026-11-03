# Backlog: DTM 2013 pack

Things the game lets a pack change that the 2013 pack doesn't change yet.
Game limits are in [DEVELOPER_WISHLIST.md](../DEVELOPER_WISHLIST.md), not here.
Formats were read from the installed `default26` pack (game 0.99.5).

Priority: **P1** = changes how the game plays, **P2** = more of the real
2013 world, **P3** = presentation.

## 1. Per-track values · P1

`tools/osm_track.py` writes defaults unless the spec sets a value. Research
each one per venue and set it in `track_specs/*.json` (Norisring:
`track_overrides` in `season.json`).

| Field | Now | To do |
|---|---|---|
| `pit_lane_loss_s` | Estimates, 17–21 s | Real 2013 pit-lane times (pit-in to pit-out minus a racing lap) |
| `dnf_modifier` | 1.0 everywhere | Higher for walled tracks (Norisring, Moscow?), lower for open ones (Hockenheim, Red Bull Ring); compare with 2013 retirements |
| `overtaking_difficulty` | Estimates, 0.45–0.7 | Calibrate against 2013 position changes per race |
| `starting_grid` | Same everywhere (pole on the left) | Real pole side and grid spacing per track |
| `wet_weather_probability_multiplier` | Set only for Brands Hatch, Zandvoort, Nürburgring | One value per venue from climate data for the race month |
| `fuel_consumption` | 1.0 everywhere | Check that 120 L lasts a race with no refuelling |

After the change, play a season and check pit stops, retirements and race times.

## 2. Drivers for the years after 2013 · P1

`data/drivers.json` holds only the 22 race drivers: no free agents, reserves
or youngsters. A career past 2013 then fills seats from the game's
generated drivers.

- Add real drivers who were reserves, test drivers or juniors in 2013,
  especially those who came into the DTM in 2014–2016. Give each the right
  age, `career_stage`, `talent` and a free-agent contract.
- Candidates to verify: the 2014 rookies, plus the F3 and Porsche drivers
  under §3. Research them first (`research/entries_future.csv`, with sources).
- Fill `driver_names.json` with German, British and other European names
  that fit the era, so generated drivers fit in too.
- **Open:** are junior-series drivers (named in `junior_series.json`
  teams) separate from `drivers.json`, and do they move up into the DTM?

## 3. Feeder series · P2

`junior_series.json` is a list of up to 4 series. Each has `series_name`,
`series_abbreviation`, `description`, `tier`, `minimum_driver_age`,
`maximum_driver_age`, `drivers_per_team`, `dnf_rate_percent`, `points_format`,
a 52-week `schedule`, and `teams` (`name`, `primary_color_rgb`,
`secondary_color_rgb`, `quality`, `drivers` by name). `junior_teams.json`
also exists (not looked at yet). The base pack has three made-up series
(tiers 2–4).

- **FIA Formula 3 European Championship 2013:** teams, drivers, calendar
  and points.
- **Porsche Mobil 1 Supercup and/or Porsche Carrera Cup Deutschland 2013.**
- Maybe a fourth: ADAC Formel Masters or the ADAC GT Masters.
- Research into `research/junior/<series>.csv` the way the DTM entries were
  done, then generate the file with `season_from_research.py`.
- Check in-game how tiers and ages decide promotion into the DTM.

## 4. Sponsors · P2

`sponsors.json` (the pool: name, tier type, amount, industry, nationality)
and `starting_sponsors.json` (each team's deals) come from the base pack.
`no_title_sponsors` only removes title status.

- Starting deals per team from the 2013 liveries (`research/liveries.csv`
  has the main sponsors).
- A pool of sponsors from the period for later seasons.
- Check trademarks first: [LICENSE-CONTENT.md](../../LICENSE-CONTENT.md)
  says to use real names descriptively only. Sponsor logos
  (`assets/sponsors/`) only as our own drawings, or left out.

## 5. Audio · P3

Pack audio goes in `assets/audio/` (the game's `README_AUDIO.txt`). A pack
can supply:

| Folder | What | How |
|---|---|---|
| `music/` | Menu music (WAV/OGG/MP3/FLAC) | The pack's playlist replaces the shared one when it has any tracks |
| `session/` | Finish-line pass-bys, both directions (`_lr`) | `hotlap_flybys.json` clips (`key`, `file`, `crossing_s`, `gain`); no limit on how many; assign them with `passby_audio` in `engines.json` |
| `race/` | Grid idle/launch pairs, start light, lights out, pit fire-up/exit/wheelguns | `race_engines.json`; numbered sets can be extended (`grid_idle_03`, `pit_exit_05`...) |
| `ambience/` | Base sound beds, cars on track, crowd, helicopter, PA, pit blowers, rain | `session_layers.json`: gains, sessions, cycles, custom `file` |

UI sounds always come from the shared folder. Audio never changes the
simulation.

- **Engine sounds:** a V8 pass-by for each make (Audi, BMW, Mercedes)
  instead of base clips 03/01/04. Needs freely licensed recordings (CC0 or
  CC BY, credited in `credits.txt`), not base-game or other mods' files.
- **Menu music:** CC0 tracks that fit the period, or none.
- **Ambience:** a German-language PA and a crowd bed, if free recordings exist.
- `build_pack.py` copies the base audio. Make sure it puts ours over the
  base files and that no base file ends up in git.

## 6. Smaller items

- **Staff:** named real technical staff instead of placeholders
  (`season.json` `staff.named`). · P2
- **Rule changes over time:** `change_control` / `scripted_changes` for
  2014 onwards (needs research on what changed). · P2
- **Part labels:** touring-car names in `car_parts.json` (🧪 whether the UI
  uses them). · P3
- **Events and radio quotes:** DTM-flavoured `events.json` and
  `radio_quotes.json`. · P3
- **Menu and dashboard art:** our own `title_bg.png`, `dashboard_bg*.png`. · P3
- **Engines:** all three makes have `factory: false` while every team is
  `works: true`. Check whether that's intended. · P2
- **Portraits:** 2 of 22 drivers have helmet cards; look for free photos. · P3
- **Moscow length:** 2.555 vs 2.661 km still open.

## 7. Still to check in-game

From the README: top speeds after the refit, the Nürburgring lap with the
F1 chicane, two stops at the long races.
