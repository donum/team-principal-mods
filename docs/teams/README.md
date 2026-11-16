# DTM teams, sponsors and driver backing by real year

These files list what really happened to DTM teams, sponsors and driver
deals. Every row uses the real calendar year, not a pack, so any DTM pack
can read them. A pack for year P maps real year Y to career season
`Y - P + 1`. For example, the 2013 pack sees Mercedes leave before season 7 (2019).

Uses in the game:

| File | Game keys it feeds |
|---|---|
| `dtm_team_changes.csv` | `events.json` (`team_join`, `team_leave` with `team`, `first_season`, `chance`), `teams.json` (`first_active_season`, `engine_units_per_season`), `team_buyouts.json` (operator change, rename) |
| `dtm_sponsors.csv` | `starting_sponsors.json`, renames in later years. Rows with `in_team_name=yes` are title sponsors in real life, but we don't set `"type": "title"`: the game would put the name in front of a team name that already holds it (wishlist C11). |
| `dtm_game_events.csv` | The build step `tools/real_history.py`: joins, leaves and engine makers per real year, with names, colours and history text for teams that join. A pack maps the keys to its own teams in `gen.json` `real_history.operators`. |
| `dtm_liveries.csv` | Car images of teams that join later: colours, sponsors and layout per car in its first season, with photo links. Drafts in `seasons/dtm-2013/art/cars.json` (cars with a `season`), brief for the artist in `seasons/dtm-2013/research/later_team_liveries.md`. |
| `dtm_driver_backing.csv` | `drivers.json` `pay_driver_amount_m` (part A), `future_contract` (part B, only for deals announced before the pack's season starts) |

## Columns

- `dtm_team_changes.csv`: `year` is the first season affected. For a
  leave, that is the first season without the team; the last season raced
  is in `detail`. `change` is one of `team_join`, `team_leave`,
  `operator_change`, `make_join`, `make_leave`, `car_count`.
- `dtm_sponsors.csv`: one row per car (or per team when `driver` is blank).
  `in_team_name=yes` means the sponsor was in the official entrant name.
- `dtm_driver_backing.csv`: `part` A = drivers who brought money or were
  funded juniors, B = when next-season deals were announced. `amount_m` is
  blank unless a source gives a figure.

## Into a pack

1. In the season's `gen.json`, add `real_history` with `events`
   (`docs/teams/dtm_game_events.csv`), `operators` (key in the CSV to the
   pack's team name, for every team on its grid) and optional
   `pay_drivers` (name to amount in millions).
2. Run `tools/season_from_research.py` (copies it to `season.json`) and
   `tools/build_pack.py`. The build prints every team that joins later,
   and every leave the game would skip (it keeps at least 10 teams).
3. Rows for years up to the pack's own year are skipped. A join whose key
   is already in `operators` is skipped too, so a 2016 pack that has ART
   on its grid just maps `ART-Mercedes` to its team.

## Status (2026-11-16)

- Covered: 2013 to 2020 (end of Class 1). Older eras are still to do.
- Not in `dtm_game_events.csv` yet: team renames (`team_buyouts.json`
  `identity_rebrand`), the 2014 7th Mercedes car, WRT's 3rd car in 2020,
  and Audi and BMW leaving after 2020 (the DTM moved to GT3; the grid
  would empty).
- No 2014 seat was announced before the 2013 finale (20 Oct 2013). The
  first was 6 Dec 2013, so the 2013 pack gets no future contracts.
- Only Mercedes (and Orlen Team ART in 2020) put sponsors in team names.
  Audi and BMW sponsors were on the car name only.
- Rows checked only on Wikipedia or in search snippets say so in the
  `detail` or `note` column. Unclear points: BMW's exact exit date, some
  2013 and 2016 car sponsors, the 2019 BMW team split, the 2020 WRT cars.

When you add facts, keep the source URL in each row and update this list.
