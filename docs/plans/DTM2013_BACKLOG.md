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
| `pit_lane_loss_s` | From TV and `tools/pit_lane.py`; Moscow 25.8 s | Brands Hatch is still an estimate |
| `dnf_modifier` | Fitted in six simulator rounds | Done |
| `overtaking_difficulty` | Fitted; passing accepted at about 2.2 swaps per car | Done (more would need driver consistency or DRS) |
| `starting_grid` | Pole side from the TV starts | Done (Nürburgring started behind the safety car) |
| `wet_weather_probability_multiplier` | From climate data for the race month | Done |
| `fuel_consumption` | 1.0 everywhere | Check that 120 L lasts a race with no refuelling |

After the change, play a season and check pit stops, retirements and race times.

**Status (2026-11-15).** The facts now live in [docs/venues](../venues/README.md),
shared by every pack, and `tools/venue_stats.py --pack seasons/dtm-2013 --apply`
writes the sourced ones into the specs.
- Done: `starting_grid` pole side from the TV starts (8 of 9 venues; five specs
  changed) and `wet_weather_probability_multiplier` from the climate in the
  race month (Red Bull Ring 1.27 to Oschersleben 0.76).
- Done: `dnf_modifier` and `overtaking_difficulty`, fitted in two simulator
  rounds (`venue_stats.py --sim ... --fit`) to the 2012–2013 retirements and
  grid-to-finish swaps per venue. The game rolls failures every lap, so long
  races need low values (Brands Hatch 0.33, Moscow 0.58) and short ones high
  (Hockenheim 1.78). Six rounds (`build/sim/dtm-2013/venues-fit1` to `-fit6`;
  the game updated to build 45440200 between rounds one and two). Round six,
  40 races: 13.9% of starters retired (real 14.3%), 2.13 swaps per car (real
  2.32), about 2 stops everywhere. Per track the retirements scatter with 4
  races each; not refitted further.
- Overtaking: the aim was 15% more than real (2.67 swaps per car). Overtaking
  values below about 0.3 and a 40% stronger slipstream (round five) gave no
  more swaps: the field finishes close to its race-pace order. Accepted at
  about 2.2 (2026-11-15); the slipstream is back to the game default. More
  would need race-pace variance (driver consistency) or DRS, which touches
  the ratings and qualifying.
- Moscow: with the real pit loss the AI one-stopped (1.4 stops), so its
  `tyre_wear_mult` went from 0.59 to 0.75 (2.46 stops), now 0.68 (round six:
  2.2 stops).
- `pit_lane_loss_s`: Moscow 25.8 s from the official in-and-out time named on
  TV (29 s with the stop). The commentators' figures at the Nürburgring and
  Zandvoort match the specs and `tools/pit_lane.py`. At the Red Bull Ring the
  commentary says about 20 s with the stop (about 17 s lane loss): the model
  (23 s) runs high there, the spec keeps 19. Brands Hatch is still an estimate
  (model 14, spec 17).
- Open: `fuel_consumption` (120 L with no refuelling).

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

**Done:** five real 2013 series in `data/junior_series.json` (see the pack
README, "Feeder series"). The notes below are kept for other seasons.

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

- ~~Starting deals per team from the 2013 liveries~~ done: `sponsors` in
  `gen.json` (from `research/spotter_guide.csv`), swapped in by
  `build_pack.py` with the vanilla deals' money (see the pack README).
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
- **Menu music:** done. Four Kevin MacLeod tracks (CC BY 4.0, credited)
  replace the base playlist (`"vanilla_music": false` in `season.json`).
  Other candidates are in `private/music/candidates`, listed on the mod page.
- **Ambience:** a German-language PA and a crowd bed, if free recordings exist.
- `build_pack.py` copies the base audio. Make sure it puts ours over the
  base files and that no base file ends up in git.

## 6. Smaller items

- ~~**Staff:** named real technical staff instead of placeholders~~ done in
  v0.2, from [docs/staff](../staff/README.md).
- **Rule changes over time:** `change_control` / `scripted_changes` for
  2014 onwards (needs research on what changed). · P2
- **Part labels:** touring-car names in `car_parts.json` (🧪 whether the UI
  uses them). · P3
- **Events and radio quotes:** DTM-flavoured `events.json` and
  `radio_quotes.json`. · P3
- **Menu and dashboard art:** our own `title_bg.png`, `dashboard_bg*.png`. · P3
- **Engines:** all three makes have `factory: false` while every team is
  `works: true`. Check whether that's intended. · P2
- **Portraits:** Joey Hand still has a helmet card, and Wickens, Scheider
  and Priaulx have tight close-ups (bigger heads). Werner's photo is black
  and white with sunglasses. Look for better free photos of these five. · P3
- **Moscow length:** 2.555 vs 2.661 km still open.
- **Workshop description:** write it before the first upload. It must
  credit the car images to Pappydhorn12 (used with permission, rights stay
  with the artist) and list the photo, logo and map credits from
  `credits.txt`. · P1

## 7. Still to check in-game

From the README: top speeds after the refit, the Nürburgring lap with the
F1 chicane, two stops at the long races.
