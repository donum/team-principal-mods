# BTCC 1991: Season Pack

Status: **v0.1, generated and builds; not yet tested in-game or simulated.**
Our first British Touring Car Championship pack, and the first season of
Super Touring. The data was generated with `tools/season_from_research.py`
from `research/`, configured in `gen.json`. For the sourced facts behind it
(calendar, entry list, standings, rules, open questions), see
[research/season.md](research/season.md). What is still open is in
[docs/plans/BTCC1991_BACKLOG.md](../../docs/plans/BTCC1991_BACKLOG.md).

```bash
python tools/season_from_research.py seasons/btcc-1991
```

```bash
python tools/build_pack.py seasons/btcc-1991
```

The pack folder is `btcc1991`.

## How it's built

- **Template:** the DTM Group A season (`"template": "dtm-1991"`) gives the
  data layout and the vanilla base pack. Rules, engines, car profiles and
  tracks are the season's own (`"rules": "own"`, `patches/regulations.json`).
- **Teams and drivers:** from `research/entries.csv`. Drivers in at least
  half the meetings get race seats; everyone else is a reserve. Sean Walker
  Racing, Moto-Build and ACE Motorsport are left out (`"skip"`).
- **Makes:** read from the engine column (`"make_from": "engine"`): BMW,
  Vauxhall, Toyota, Ford, Nissan, Mitsubishi.
- **Ratings, skills and salaries:** estimated from the final standings, with
  Soper and Harvey set by hand (`drivers` in `gen.json`).
- **Calendar:** 13 meetings. Donington National (round 8) and Brands Hatch
  Indy (round 10) had two races, so each of those takes two game weeks.
- **Tracks:** Brands Hatch Indy is our traced track from the DTM era 4 base
  (`shared_tracks`). The other six British circuits are placeholders that
  borrow a DTM track's geometry (`track_placeholders`) until they are traced.

## Simplifications

- Every team runs Dunlop tyres and one 950 kg weight limit, until the real
  values are sourced.
- No car images, team logos or portraits yet.
- Sounds are the game's own.
