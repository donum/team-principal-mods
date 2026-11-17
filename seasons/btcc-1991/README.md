# BTCC 1991: Season Pack

Status: **v0.1, generated and builds; research checked against period sources (2026-11-15).**
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
  (`shared_tracks`). The other six circuits are traced in `track_specs/` from
  the 1991 layouts of the race-tracks repo (`tools/race_tracks.py`,
  `tools/osm_track.py`): Silverstone National and GP 1991, Snetterton 1990,
  Donington Park GP and National, Oulton Park International 1975, Thruxton.
- **Staff and team principals:** real people from
  `docs/staff/btcc_staff.csv` (25 rows, `"staff_reference": "btcc-1991"`),
  made-up period names from `btcc_staff_fictional.csv` for every other
  role. Team facts behind them: [research/team_facts.md](research/team_facts.md).
- **Sponsors:** the real 1991 backers from `docs/teams/btcc_sponsors.csv`
  (`sponsors` in `gen.json`). Teams without a known sponsor keep the base
  game's fictional ones.
- **After 1991:** `real_history` in `gen.json` plays the real grid of 1992
  to 2000 from `docs/teams/btcc_game_events.csv`: 27 teams join (Peugeot,
  Mazda, Renault, Volvo, Alfa Romeo, Honda and Audi arrive as makes), the
  1991 teams leave when they really did. Pay drivers: Ray Bellm, Laurence
  Bristow, Matt Neal, Ian Forrest (amounts are our estimates). No 1992 seat
  was announced before the 1991 finale, so there are no future contracts.
  Debut liveries of the later teams: [research/later_team_liveries.md](research/later_team_liveries.md).

## Series logo

The series was the "Esso RAC British Touring Car Championship" in 1991.
Logo reference: the cover of the official 1991 season review (Duke Video),
kept outside the repo as
`Pictures/mods/btcc-1991/reference/btcc-1991-season-review-cover.png`
(Duke's artwork, reference only, not for the pack). It shows a large
teal "BTCC" wordmark (heavy upright sans-serif capitals) on a dark grey top band,
then a teal band with "1991" and "BRITISH TOURING CAR CHAMPIONSHIP" in black
capitals (two lines). At the foot of the cover is a small italic "BTCC" badge
with a chequered pattern, next to the Dunlop and Duke logos. The cover is a
later DVD design, so the big teal wordmark may be Duke's styling, not the
1991 series logo; the small chequered badge is the better candidate for the
period logo.

Period evidence from the 1991 season review itself (a BHP Sport production,
"© 1991", in `Videos/yt/BTCC/1991/Singles`): the podium backdrop at the
Silverstone finale [1:27:53] has a red "ESSO" box next to "British Touring
Car Championship" in dark blue bold upright letters (title case) on white.
The cars' number panels read "ESSO" over "British Touring Car Championship"
with a small chequered-flag mark. The review's own captions title the series
"ESSO BRITISH TOURING CAR CHAMPIONSHIP" in white italic capitals. No
"BTCC" wordmark showed up in a scan of the review (one frame every 12 s). Until a programme or poster
turns up, use a plain text title in game ("British Touring Car
Championship" or "BTCC"), as the DTM packs do for unverified years
(`docs/ERAS.md`).

## Simplifications

- Every race pays 24-18-12-10-8-6-4-3-2-1. In 1991 the four races at the two
  double-header meetings paid half points to the top eight; the game has
  one points scale for all races (wishlist A1).
- One minimum weight of 950 kg; the BMW M3 and Ford Sierra carry their
  1050 kg as car mass.
- No team logos yet.
- Portraits are painted illustrations in 1991 style, made with ChatGPT
  (OpenAI). They are not photos and the likeness is approximate. Free
  photos from 1991 barely exist; see
  [research/portrait_drawings.md](research/portrait_drawings.md).
- Sounds are the game's own.
- A team that changed make (Rouse, RML, Prodrive, WSR, Schnitzer's return)
  is a new team in the game (wishlist C12). The game keeps 10 teams, so
  four teams that left after 1999 stay (wishlist C10).
- Later teams have no car images yet; their colours are mostly unchecked
  (see `research/later_team_liveries.md`).
