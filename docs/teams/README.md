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
| `dtm_game_events.csv` | The build step `tools/real_history.py`: joins, leaves and engine makers per real year, with names, colours, history text and team principal for teams that join. A pack maps the keys to its own teams in `gen.json` `real_history.operators`. |
| `dtm_liveries.csv` | Car images of teams that join later: colours, sponsors and layout per car in its first season, with photo links. Drafts in `seasons/dtm-2013/art/cars.json` (cars with a `season`), brief for the artist in `seasons/dtm-2013/research/later_team_liveries.md`. |
| `dtm_driver_backing.csv` | `drivers.json` `pay_driver_amount_m` (part A), `future_contract` (part B, only for deals announced before the pack's season starts) |

## Columns

- `dtm_team_changes.csv`: `year` is the first season affected. For a
  leave, that is the first season without the team; the last season raced
  is in `detail`. `change` is one of `team_join`, `team_leave`,
  `operator_change`, `make_join`, `make_leave`, `car_count`.
- `dtm_sponsors.csv`: one row per car (or per team when `driver` is blank).
  `in_team_name=yes` means the sponsor was in the official entrant name.
- `dtm_game_events.csv`: for a `team_join`, `history` is the in-game team
  text, written as of the debut year. `principal` is a real person from
  `docs/staff` (the debut season's row), with `principal_nationality` and,
  when known, `principal_born`. `tools/build_pack.py` adds that principal
  to `teamprincipals.json` for the inactive team, as the vanilla packs do.
  When the column is empty, or the person already leads a team on the
  pack's grid, the build uses a made-up name. A principal with no known
  birth year is kept inside the usual age range in the debut year.
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
- Joining teams (2015 to 2020) have a history text and a real principal,
  except BMW Team RMR: Stefan Reinhold and Bart Mampaey shared it and
  already lead RMG and RBM, so it gets a made-up name. Andreas Bänziger,
  R-Motorsport's co-owner, stands in for R-Motorsport 2 (no separate
  principal found). No birth years yet except Frédéric Vasseur (1968).
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

## BTCC

The same files for the BTCC, with the prefix `btcc_`:

| File | Notes |
|---|---|
| `btcc_team_changes.csv` | 1992 to 2000, same columns as the DTM file |
| `btcc_game_events.csv` | Read by `tools/real_history.py`; keys of the 1991 teams in `seasons/btcc-1991/gen.json` |
| `btcc_sponsors.csv` | 1991 only. Extra columns `source_industry`, `country` (from the sources) and `game_industry`, `game_nationality` (the game's lists) |
| `btcc_driver_backing.csv` | Same columns as the DTM file |

Status (2026-11-16):

- Joins and leaves of every 1991 team and every works team to 2000.
- No `principal` column yet, so the joining teams get made-up principals. A team
  that changed make is a leave plus a join under a new key (wishlist C12).
  Two names were changed by us so they stay unique: BMW Team Motorsport
  (1995) and Honda Team WSR (1999).
- Colours of the joining teams are mostly from memory, five are
  placeholders. Unclear: who ran BMW (1995) and Toyota (1995), Renault
  Dealer Racing's operating company, the link between Team DCRS (1997) and
  Dave Cook. Several exit years only come from Wikipedia.
- Sponsors: Castrol (Nissan), Firestone (Mitsubishi), Lazerprinz and
  Partservice could not be found for 1991. BMW Team Finance and Mobil 1 on
  the Prodrive cars are weak.
- No 1992 seat was announced before the 1991 finale (6 Oct 1991); the first
  was Will Hoy to Toyota on 4 Dec 1991.
