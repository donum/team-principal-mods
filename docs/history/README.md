# Rules history

How the racing rules of F1 (1950 to 2026), DTM (1984 to 2026), IndyCar
(1979 to 2026), endurance racing (1953 to 2026), the BTCC (1958 to 2026),
NASCAR (1949 to 2026), Super GT (1993 to 2026), IMSA (1971 to 2026) and
Formula E (2014 to 2026) changed,
one topic per file. Each file has a table, its sources, and a Discord post
that is ready to paste. The table image for Discord is in
`docs/packages/img/png/<file name>.png`.

To make an image again after an edit:

```bash
python -I tools/history_table.py docs/history/f1-qualifying.md
```

`(?)` marks a detail the sources did not confirm. "Open" below is the
number of `(?)` in the tables. Check them, and the conflicts listed under
Sources in each file, before posting.

Every file ends with an **In the game today** table: for each rule,
whether Team Principal (0.99.5 and the 0.99.6 beta) can do it (`Yes`), only
with a stand-in (`Partly`) or not at all (`No`), with the item in
`docs/DEVELOPER_WISHLIST.md`. Over all 37 files: 83 yes, 57 partly,
139 no. Checked against the 0.99.6 beta game code.

Status: `draft` (not posted yet), `posted` (add the date and link),
`answered`.

## Coverage explorer

[coverage.html](coverage.html) is one self-contained page with three views:

- **Coverage:** which game features each of the 469 seasons of the nine
  series needs, and how many seasons become playable as they were when you
  switch features on.
- **Rules history:** every table below, per series, with what the game can
  do today.
- **A page per series:** a gap matrix like `docs/dtm_rules.html`, and every
  season with its needs, its rules from the tables and, for DTM, the full
  rulebook rows.

Published as an artifact: https://claude.ai/artifact/W9A1EGxwUBCjp6AQSVXM3Z.
Links to a view: `#share` (screenshot view), `#rules-f1`, `#dtm` and so on.
The page rebuilds itself from these Markdown files: run
`python -I tools/coverage_data.py` after changing a history file,
`tools/coverage_data.py` or `tools/coverage_template.html`.

## F1, 1950 to 2026

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Qualifying | [f1-qualifying.md](f1-qualifying.md) | 1,408 | 10 | draft |
| 2 | Points | [f1-points.md](f1-points.md) | 1,370 | 7 | draft |
| 3 | Tyres | [f1-tyres.md](f1-tyres.md) | 1,311 | 12 | draft |
| 4 | Pit stops | [f1-pit-stops.md](f1-pit-stops.md) | 1,394 | 12 | draft |
| 5 | Race format and starts | [f1-race-format.md](f1-race-format.md) | 1,346 | 16 | draft |
| 6 | Safety car and red flags | [f1-safety-car.md](f1-safety-car.md) | 1,221 | 11 | draft |
| 7 | Overtaking aids | [f1-overtaking-aids.md](f1-overtaking-aids.md) | 1,252 | 8 | draft |
| 8 | Engines and grid penalties | [f1-engines.md](f1-engines.md) | 1,265 | 11 | draft |
| 9 | Parc fermé and minimum weight | [f1-parc-ferme-weight.md](f1-parc-ferme-weight.md) | 1,282 | 21 | draft |
| 10 | Money and testing | [f1-money-testing.md](f1-money-testing.md) | 1,346 | 12 | draft |
| 11 | Entries and drivers | [f1-entries-drivers.md](f1-entries-drivers.md) | 1,282 | 4 | draft |
| 12 | Team orders | [f1-team-orders.md](f1-team-orders.md) | 1,226 | 3 | draft |
| 13 | Weekend schedule and calendar | [f1-weekend-calendar.md](f1-weekend-calendar.md) | 1,262 | 14 | draft |

## DTM, 1984 to 2026

Made from the season research in `seasons/<id>/research/` and
`docs/dtm_rules.html`, not from new web research.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Qualifying | [dtm-qualifying.md](dtm-qualifying.md) | 1,136 | 3 | draft |
| 2 | Race format | [dtm-race-format.md](dtm-race-format.md) | 1,223 | 9 | draft |
| 3 | Pit stops and tyres | [dtm-pit-stops-tyres.md](dtm-pit-stops-tyres.md) | 1,321 | 0 | draft |
| 4 | Points | [dtm-points.md](dtm-points.md) | 1,179 | 0 | draft |
| 5 | Weight balancing | [dtm-weight-balancing.md](dtm-weight-balancing.md) | 1,338 | 5 | draft |

## IndyCar, 1979 to 2026

CART (1979 to 2003), Champ Car World Series (2004 to 2007) and IRL /
IndyCar (1996 to 2026). Qualifying and race format share one file because
the sources were thin.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Points | [indycar-points.md](indycar-points.md) | 1,255 | 2 | draft |
| 2 | Qualifying and race format | [indycar-qualifying-race.md](indycar-qualifying-race.md) | 1,251 | 11 | draft |
| 3 | Pit stops, fuel and tyres | [indycar-pit-fuel-tyres.md](indycar-pit-fuel-tyres.md) | 1,207 | 4 | draft |
| 4 | Cars, engines and push-to-pass | [indycar-cars-engines.md](indycar-cars-engines.md) | 1,201 | 2 | draft |

## Endurance: World Sportscar Championship, Le Mans and WEC, 1953 to 2026

Three topics, because the sources were thin on pit stops and points.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Classes and balance of performance | [wec-classes-bop.md](wec-classes-bop.md) | 1,237 | 1 | draft |
| 2 | Drivers, crews and pit stops | [wec-drivers-pit-stops.md](wec-drivers-pit-stops.md) | 1,232 | 5 | draft |
| 3 | Race format and points | [wec-race-format-points.md](wec-race-format-points.md) | 1,217 | 6 | draft |

## BTCC, 1958 to 2026

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Weekend format | [btcc-weekend-format.md](btcc-weekend-format.md) | 1,210 | 4 | draft |
| 2 | Points and titles | [btcc-points-titles.md](btcc-points-titles.md) | 1,194 | 3 | draft |
| 3 | Cars, classes and balancing | [btcc-cars-balancing.md](btcc-cars-balancing.md) | 1,274 | 7 | draft |

## NASCAR Cup, 1949 to 2026

Rated as an oval pack: the oval mode already has stages, a chase, charters,
the free pass and green-white-checker.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Points and playoffs | [nascar-points-playoffs.md](nascar-points-playoffs.md) | 1,118 | 2 | draft |
| 2 | Race format, qualifying and cautions | [nascar-race-format.md](nascar-race-format.md) | 1,104 | 4 | draft |
| 3 | Cars, engines and entries | [nascar-cars-entries.md](nascar-cars-entries.md) | 953 | 3 | draft |

## Super GT and JGTC, 1993 to 2026

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Classes, balancing and tyres | [supergt-classes-balancing.md](supergt-classes-balancing.md) | 1,031 | 1 | draft |
| 2 | Race format, drivers and points | [supergt-race-format-points.md](supergt-race-format-points.md) | 1,024 | 6 | draft |

## IMSA, 1971 to 2026

IMSA GT 1971 to 1998, ALMS 1999 to 2013, WeatherTech from 2014.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Classes and balancing | [imsa-classes-bop.md](imsa-classes-bop.md) | 962 | 5 | draft |
| 2 | Race format, drivers and points | [imsa-race-format-points.md](imsa-race-format-points.md) | 1,029 | 5 | draft |

## Formula E, 2014-15 to 2026-27

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Cars, energy and boosts | [fe-cars-energy.md](fe-cars-energy.md) | 1,037 | 1 | draft |
| 2 | Race format, qualifying and points | [fe-race-format-points.md](fe-race-format-points.md) | 1,172 | 2 | draft |

## Worth checking first

These are the points readers are most likely to notice:

- F1 qualifying: when the 107% rule ended (Japan 2002 or 2003), when Q1
  went to 18 minutes (2010 or 2014), when the top 10 started on Q2 tyres
  (2014 or 2016).
- F1 minimum weights before 2009 and from 2013, and 2026 (724 or 768 kg).
- F1 cost caps for 2022 to 2025.
- DTM 2026 success ballast and BoP, still assumed.

Single feature requests are in `docs/requests/`, the big multi-post
request in `docs/packages/discord_posts.md`.
