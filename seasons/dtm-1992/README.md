# DTM 1992: Season Pack

Status: **v0.1, generated.** The data was generated with
`tools/season_from_research.py` from `research/`, configured in `gen.json`.
For the sourced facts behind it (calendar, entry list, standings, rules,
sources and unverified points), see [research/season.md](research/season.md).

## How it's built

- **Teams and drivers:**
  - Built from `research/entries.csv`.
  - Drivers who entered at least half the rounds get race seats, up to 3 per
    team. Everyone else is a reserve driver.
  - One-off teams listed with `"skip"` in `gen.json` aren't included.
- **Ratings, skills and salaries:** estimated from the final 1992 standings.
  These are estimates, not history.
- **Rules, engines, tyres and car profiles:** shared with DTM 1991
  (`template` in `gen.json`).
- **Tracks:**
  - Shared with other seasons where the layout is the same (`shared_tracks`).
  - The season's own lap length and race laps come from `track_overrides`.
  - Venues new for this season are in `track_specs/`.
- **Art:**
  - Cars are plain team-colour liveries (`art/cars.json`).
  - Team logos are reused from 1991 where the team existed then; the rest are
    crests (`art/logos.json`).

## Simplifications

- Audi (SMS, AZR) withdrew after round 6 when the ONS appeal court ruled its
  crankshaft illegal. In the game the Audis race the whole season.
- AMG ran 4 cars (Ludwig, Schneider, Rosberg, Lohr). The game allows 3, so
  Lohr is a reserve driver.
- BMW got a bigger front splitter and a higher rear wing from the Nordschleife
  round on. That isn't modelled.
- One race per round at heat distance, as in the 1991 pack.

## Rebuild

```bash
python tools/season_from_research.py seasons/dtm-1992
```

```bash
python tools/osm_track.py seasons/dtm-1992/track_specs/*.json
```

```bash
python tools/car_art.py seasons/dtm-1992
```

```bash
python tools/logo_art.py seasons/dtm-1992
```

```bash
python tools/build_pack.py seasons/dtm-1992 --install
```
