# Rules history

How the racing rules of F1 (1950 to 2026) and DTM (1984 to 2026) changed,
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

Status: `draft` (not posted yet), `posted` (add the date and link),
`answered`.

## F1, 1950 to 2026

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Qualifying | [f1-qualifying.md](f1-qualifying.md) | 1,324 | 10 | draft |
| 2 | Points | [f1-points.md](f1-points.md) | 1,286 | 7 | draft |
| 3 | Tyres | [f1-tyres.md](f1-tyres.md) | 1,227 | 12 | draft |
| 4 | Pit stops | [f1-pit-stops.md](f1-pit-stops.md) | 1,310 | 12 | draft |
| 5 | Race format and starts | [f1-race-format.md](f1-race-format.md) | 1,262 | 16 | draft |
| 6 | Safety car and red flags | [f1-safety-car.md](f1-safety-car.md) | 1,137 | 11 | draft |
| 7 | Overtaking aids | [f1-overtaking-aids.md](f1-overtaking-aids.md) | 1,168 | 8 | draft |
| 8 | Engines and grid penalties | [f1-engines.md](f1-engines.md) | 1,181 | 11 | draft |
| 9 | Parc fermé and minimum weight | [f1-parc-ferme-weight.md](f1-parc-ferme-weight.md) | 1,198 | 21 | draft |
| 10 | Money and testing | [f1-money-testing.md](f1-money-testing.md) | 1,262 | 12 | draft |
| 11 | Entries and drivers | [f1-entries-drivers.md](f1-entries-drivers.md) | 1,198 | 4 | draft |
| 12 | Team orders | [f1-team-orders.md](f1-team-orders.md) | 1,142 | 3 | draft |
| 13 | Weekend schedule and calendar | [f1-weekend-calendar.md](f1-weekend-calendar.md) | 1,178 | 14 | draft |

## DTM, 1984 to 2026

Made from the season research in `seasons/<id>/research/` and
`docs/dtm_rules.html`, not from new web research.

| # | Topic | File | Post length | Open | Status |
|---|---|---|---|---|---|
| 1 | Qualifying | [dtm-qualifying.md](dtm-qualifying.md) | 1,052 | 3 | draft |
| 2 | Race format | [dtm-race-format.md](dtm-race-format.md) | 1,139 | 9 | draft |
| 3 | Pit stops and tyres | [dtm-pit-stops-tyres.md](dtm-pit-stops-tyres.md) | 1,237 | 0 | draft |
| 4 | Points | [dtm-points.md](dtm-points.md) | 1,095 | 0 | draft |
| 5 | Weight balancing | [dtm-weight-balancing.md](dtm-weight-balancing.md) | 1,254 | 5 | draft |

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
