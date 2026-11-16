# DTM driver careers

Every driver's result in every DTM and ITC race from 1984 to 2026. Each DTM
pack reads its driver `history` from here: a driver's record before the
pack's season.

- **Built:** 2026-11-16 by `tools/driver_careers.py build`.
- **Size:** 16,047 race rows, 1,399 driver-seasons, 527 drivers, 40 seasons.
- **Page:** the private artifact "DTM Driver Database"
  (https://claude.ai/artifact/6yik2XS5df4K2MYhpiaDK7). It has the drivers,
  every season as a results grid, the history each pack gets and the source
  checks. Rebuild it with `python -I tools/driver_careers.py page <file>.html`
  and republish it to the same URL.

## Files

| File | One row per | Notes |
|---|---|---|
| [dtm_races.csv](dtm_races.csv) | driver and race | `kind`: `race`, `qr` (qualifying race 2001-2002), `nc` (non-championship), `annulled`. `started` is 0 for DNS, DNQ, withdrawn. `pole` and `fastest_lap` where a source has them. |
| [dtm_driver_seasons.csv](dtm_driver_seasons.csv) | driver and season | Starts, wins, podiums, poles, points, final position. Counts only `race` rows. |
| [dtm_drivers.csv](dtm_drivers.csv) | driver | Career totals, birth year, game nationality, and the fandom wiki's own career box for comparison. |
| [aliases.csv](aliases.csv) | other spelling | Maps a name in a pack or a source to the database name (Susie Stoddart → Susie Wolff). |
| [CHECKS.md](CHECKS.md) | disagreement | Written by `build`: where the sources disagree. |

## Sources

- **dtm.fandom.com (de)**, the season pages: results for 1984 to 1993 and
  1995 (DTM and ITC), make and guest flag for all years, a check for the rest.
- **en.wikipedia**, drivers' standings race by race (bold = pole, italics =
  fastest lap): results for 1994, 1996 and 2000 to 2026.
- **de.wikipedia**, the race list with pole sitter and winner: poles for
  1984 to 1993 and 1995, and a check on the winners.
- **Repo research**: `seasons/*/research/standings.csv` for points and final
  positions, `entries.csv` for birth years and nationality.

The raw pages are cached in `reference/driver_careers/` (gitignored).
`python -I tools/driver_careers.py fetch` refreshes them.

## Rules

- **History** = every championship race before the pack's year, DTM and ITC
  together. A season counts when the driver started at least one race. A
  title is a P1 finish in the DTM or ITC standings.
- **Not counted:** qualifying races (2001, 2002), non-championship rounds
  (Brno and Donington 1991, Donington 1993, the ITR Gold Cups at Mugello and
  Donington 1994, Shanghai 2004, Munich 2011 and 2012, Fuji 2019) and the
  annulled AVUS heat 2 in 1995.
- **Points** are each season's own totals, added up across different
  scoring systems, like the F1 Workshop packs do.
- **Retired drivers:** `apply` also adds every race winner and champion who
  is not in the pack and did not race that year, as `retired: true` with low
  skills, so the game's all-time statistics start with the real record
  holders. The file-level key `$career_retired` lists them, and the next
  `apply` replaces them.

## Commands

```
python -I tools/driver_careers.py build
python -I tools/driver_careers.py apply seasons/dtm-2013
python -I tools/driver_careers.py history 2013 "Mike Rockenfeller"
python -I tools/driver_careers.py page dtm_driver_database.html
```

`tools/season_from_research.py` calls `apply` at the end, so a regenerated
DTM pack keeps its history. Set `"career_history": false` in `gen.json` to
skip it.

## What the game does with it

From the game code (build 45440200): `GameState.load_data` reads `seasons`,
`championships`, `wins`, `podiums`, `poles`, and `starts` and `points` when
present. The numbers feed the statistics screen (all-time tables), the
driver negotiation history panel, news cards for career milestones (starts,
podiums, poles, seasons, dynasties), and driver mood after a weekend. The
game adds each new race to the same counters.

## Car drawings

All 1,162 SVGs of the fandom wiki are saved outside the repo in
`C:/Users/dan/Pictures/mods/dtm_fandom_svgs/` (2026-11-16): 1,009 car side
views in `<year>/` (one per driver and season, e.g.
`2013/Mike_Rockenfeller_2013.svg`), 63 make, tyre and team logos in `logos/`,
46 track maps in `tracks/` and 44 autographs in `autographs/`.
`SOURCES.csv` has the wiki page of each file and, for 993 cars, the number,
driver, make, team, car and tyres from the season's entry list. All were
drawn and uploaded by the wiki's admin, Byggxx. The image gallery
(`C:/Users/dan/Pictures/mods/gallery/`) shows them in its Drawings tab;
rebuild it with `python -I drawings_build.py` there.

- **Coverage:** strong for 1984 to 1989, 1995, 2000 to 2015 and 2020 to
  2023 (2013: all 22 cars). Thin for 1990 to 1994 (2 to 7 cars a year), and
  none for 2005, 2016 to 2018 and 2024 onwards.
- **Getting them again:** the image server (static.wikia.nocookie.net)
  answers scripts with a Cloudflare check, so they are saved by hand in a
  browser from `reference/driver_careers/svg_urls.txt` (all 1,162 URLs).
  `python -I tools/careers/sort_svgs.py` then files them from Downloads and
  writes `SOURCES.csv` and `MISSING.txt`. It knows the six files the wiki
  redirects to another name (Susie Stoddart → Wolff 2011 and others).
- **Use:** fan drawings under CC BY-SA (the fandom default). Credit Byggxx
  and dtm.fandom.com before using one in a pack.
