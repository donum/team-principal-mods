# Rules history

How the racing rules of F1 (1950 to 2026), DTM (1984 to 2026), IndyCar
(1979 to 2026), endurance racing (1953 to 2026), the BTCC (1958 to 2026),
NASCAR (1949 to 2026), Super GT (1993 to 2026), IMSA (1971 to 2026),
Formula E (2014 to 2026), MotoGP (1949 to 2026), the WRC (1973 to 2026), the
NLS (1977 to 2026), GT World Challenge (1997 to 2026), the Dakar (1979 to
2026), World Rallycross (2014 to 2025) and the Race of Champions (1988 to
2025) changed,
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
`docs/DEVELOPER_WISHLIST.md`. Over all 50 files: 93 yes, 63 partly,
197 no. Checked against the 0.99.6 beta game code.

Status: `draft` (not posted yet), `posted` (add the date and link),
`answered`.

## Coverage explorer

[coverage.html](coverage.html) is one self-contained page with three views:

- **Coverage:** which game features each season of the sixteen
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
| 1 | Qualifying | [f1-qualifying.md](f1-qualifying.md) | 1,408 | 1 | draft |
| 2 | Points | [f1-points.md](f1-points.md) | 1,370 | 0 | draft |
| 3 | Tyres | [f1-tyres.md](f1-tyres.md) | 1,311 | 8 | draft |
| 4 | Pit stops | [f1-pit-stops.md](f1-pit-stops.md) | 1,394 | 4 | draft |
| 5 | Race format and starts | [f1-race-format.md](f1-race-format.md) | 1,344 | 7 | draft |
| 6 | Safety car and red flags | [f1-safety-car.md](f1-safety-car.md) | 1,221 | 2 | draft |
| 7 | Overtaking aids | [f1-overtaking-aids.md](f1-overtaking-aids.md) | 1,252 | 4 | draft |
| 8 | Engines and grid penalties | [f1-engines.md](f1-engines.md) | 1,283 | 2 | draft |
| 9 | Parc fermé and minimum weight | [f1-parc-ferme-weight.md](f1-parc-ferme-weight.md) | 1,300 | 2 | draft |
| 10 | Money and testing | [f1-money-testing.md](f1-money-testing.md) | 1,346 | 6 | draft |
| 11 | Entries and drivers | [f1-entries-drivers.md](f1-entries-drivers.md) | 1,282 | 0 | draft |
| 12 | Team orders | [f1-team-orders.md](f1-team-orders.md) | 1,226 | 1 | draft |
| 13 | Weekend schedule and calendar | [f1-weekend-calendar.md](f1-weekend-calendar.md) | 1,285 | 11 | draft |

## DTM, 1984 to 2026

Made from the season research in `seasons/<id>/research/` and
`docs/dtm_rules.html`, not from new web research.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Qualifying | [dtm-qualifying.md](dtm-qualifying.md) | 1,143 | 5 | draft |
| 2 | Race format | [dtm-race-format.md](dtm-race-format.md) | 1,225 | 2 | draft |
| 3 | Pit stops and tyres | [dtm-pit-stops-tyres.md](dtm-pit-stops-tyres.md) | 1,331 | 1 | draft |
| 4 | Points | [dtm-points.md](dtm-points.md) | 1,194 | 1 | draft |
| 5 | Weight balancing | [dtm-weight-balancing.md](dtm-weight-balancing.md) | 1,338 | 5 | draft |
| 6 | Munich stadium show event | [dtm-munich-show.md](dtm-munich-show.md) | 588 | 0 | draft |

## IndyCar, 1979 to 2026

CART (1979 to 2003), Champ Car World Series (2004 to 2007) and IRL /
IndyCar (1996 to 2026). Qualifying and race format share one file because
the sources were thin.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Points | [indycar-points.md](indycar-points.md) | 1,274 | 1 | draft |
| 2 | Qualifying and race format | [indycar-qualifying-race.md](indycar-qualifying-race.md) | 1,251 | 6 | draft |
| 3 | Pit stops, fuel and tyres | [indycar-pit-fuel-tyres.md](indycar-pit-fuel-tyres.md) | 1,207 | 4 | draft |
| 4 | Cars, engines and push-to-pass | [indycar-cars-engines.md](indycar-cars-engines.md) | 1,201 | 0 | draft |

## Endurance: World Sportscar Championship, Le Mans and WEC, 1953 to 2026

Three topics, because the sources were thin on pit stops and points.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Classes and balance of performance | [wec-classes-bop.md](wec-classes-bop.md) | 1,237 | 2 | draft |
| 2 | Drivers, crews and pit stops | [wec-drivers-pit-stops.md](wec-drivers-pit-stops.md) | 1,258 | 4 | draft |
| 3 | Race format and points | [wec-race-format-points.md](wec-race-format-points.md) | 1,217 | 1 | draft |

## BTCC, 1958 to 2026

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Weekend format | [btcc-weekend-format.md](btcc-weekend-format.md) | 1,327 | 3 | draft |
| 2 | Points and titles | [btcc-points-titles.md](btcc-points-titles.md) | 1,288 | 6 | draft |
| 3 | Cars, classes and balancing | [btcc-cars-balancing.md](btcc-cars-balancing.md) | 1,253 | 2 | draft |

## NASCAR Cup, 1949 to 2026

Rated as an oval pack: the oval mode already has stages, a chase, charters,
the free pass and green-white-checker.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Points and playoffs | [nascar-points-playoffs.md](nascar-points-playoffs.md) | 1,155 | 1 | draft |
| 2 | Race format, qualifying and cautions | [nascar-race-format.md](nascar-race-format.md) | 1,168 | 2 | draft |
| 3 | Cars, engines and entries | [nascar-cars-entries.md](nascar-cars-entries.md) | 992 | 1 | draft |

## Super GT and JGTC, 1993 to 2026

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Classes, balancing and tyres | [supergt-classes-balancing.md](supergt-classes-balancing.md) | 1,080 | 1 | draft |
| 2 | Race format, drivers and points | [supergt-race-format-points.md](supergt-race-format-points.md) | 1,024 | 5 | draft |

## IMSA, 1971 to 2026

IMSA GT 1971 to 1998, ALMS 1999 to 2013, WeatherTech from 2014.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Classes and balancing | [imsa-classes-bop.md](imsa-classes-bop.md) | 969 | 2 | draft |
| 2 | Race format, drivers and points | [imsa-race-format-points.md](imsa-race-format-points.md) | 1,029 | 7 | draft |

## Formula E, 2014-15 to 2026-27

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Cars, energy and boosts | [fe-cars-energy.md](fe-cars-energy.md) | 1,051 | 0 | draft |
| 2 | Race format, qualifying and points | [fe-race-format-points.md](fe-race-format-points.md) | 1,202 | 0 | draft |

## MotoGP, 1949 to 2026

The premier class: 500cc to 2001, MotoGP from 2002. The game models cars, so
this shows which rules carry over.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Bikes, engines and tyres | [motogp-bikes-tyres.md](motogp-bikes-tyres.md) | 987 | 2 | draft |
| 2 | Race format, qualifying and points | [motogp-race-format-points.md](motogp-race-format-points.md) | 918 | 4 | draft |

## WRC, 1973 to 2026

Stage rallies, the series furthest from the game.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Cars, classes and tyres | [wrc-cars-classes.md](wrc-cars-classes.md) | 954 | 5 | draft |
| 2 | Event format and points | [wrc-format-points.md](wrc-format-points.md) | 1,078 | 2 | draft |

## NLS, 1977 to 2026

Nordschleife endurance races: Veedol, BFGoodrich, VLN, NLS.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Classes and points | [nls-classes-points.md](nls-classes-points.md) | 893 | 6 | draft |
| 2 | Race format, drivers and safety | [nls-race-format.md](nls-race-format.md) | 920 | 1 | draft |

## GT World Challenge, 1997 to 2026

FIA GT, GT1, Blancpain, GT World Challenge Europe.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Classes and balancing | [gtwc-classes-bop.md](gtwc-classes-bop.md) | 782 | 0 | draft |
| 2 | Race format and points | [gtwc-race-format-points.md](gtwc-race-format-points.md) | 976 | 4 | draft |

## Dakar, 1979 to 2026

Rally raid: bikes, cars and trucks over two weeks. Shows where the rule
system ends.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Classes and vehicles | [dakar-classes-vehicles.md](dakar-classes-vehicles.md) | 930 | 3 | draft |
| 2 | Format and routes | [dakar-format-routes.md](dakar-format-routes.md) | 961 | 1 | draft |

## World Rallycross, 2014 to 2025

Heats, semi-finals and a final on tarmac and gravel.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Format and cars | [wrx-format-cars.md](wrx-format-cars.md) | 837 | 3 | draft |

## Race of Champions, 1988 to 2025

A yearly show event in identical cars, as a proof of concept for
one-off events. See also the DTM Munich topic.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Format, venues and cars | [roc-format.md](roc-format.md) | 969 | 1 | draft |

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
