# Track Generation Plan

Every venue is generated from OpenStreetMap with
[`tools/osm_track.py`](../tools/osm_track.py). Each one has a spec in
`seasons/<season>/track_specs/<id>.json`. The tool writes:

- `tracks/<id>.json`: points in raw canvas pixels
  (`use_raw_canvas_coordinates`), micro-sectors and sector splits.
- `assets/tracks/<id>.png`: a 1044×1080 overview map.

The racing line stays inside the area the race screen doesn't cover
(`SAFE_BOX`). The background map fills the whole image.

Map data © OpenStreetMap contributors, ODbL 1.0. See
[LICENSE-CONTENT.md](../LICENSE-CONTENT.md).

## Two ways to build a lap

| Mode | When | Spec keys |
|---|---|---|
| **Raceway loop** | The circuit exists today and is tagged as one-way `highway=raceway` | (none) The tool finds the loop. Optional `exclude_way_names`/`exclude_way_ids`. |
| **Raceway loop in a relation** | A layout that shares corners with a longer one (Brands Hatch Indy) | `loop_relation`: the loop is searched only among the members of that OSM `type=circuit` relation |
| **Via route** | Street circuits, airfields, old or changed layouts | `route_ways` (tag filters), `route_relation` (an OSM `type=circuit` relation) and/or `route_way_ids`, `via` (points in driving order), `exclude_way_ids`, `bridges` (missing links; more than 2 points = a hand-placed polyline), `start`, `bbox_tiles` (extra download boxes for dense cities) |

**DRS zones** (`drs_zones`): a list of explicit zones (`detection_progress`,
`start_progress`, `end_progress` as lap fractions), or
`{"longest_straights": k}` for one zone on each of the k longest straights.
The default is none, as in the 1991 tracks. Shared tracks can get zones
through `track_overrides`.

**Micro-sectors.** The game caps each sector's speed and does its own
acceleration and braking between the caps. So straights are uncapped
(370 km/h on the reference scale), and a bend counts as a corner only if it
slows the car: a kink the racing line can straighten (from its turning angle
and `width_m`), or one the reference car never reaches the cap in, is part of
the straight. Before November 2026 short straights were capped at the speed
reached at their end, and kinks stayed corners. Cars cruised at those caps or
braked mid-straight, so the field bunched and stretched on the straights.
The first sector also started before the start line whenever the line sat
inside it, so every corner came up late (225 m at the Norisring), and cars
braked on the straight after a hairpin. It is now split at the line.

In via mode the tool joins consecutive via points by the shortest path over
the allowed ways. It also closes small mapping gaps (`snap_gap_m`). Missing
sections, such as demolished track, become explicit `bridges`.

**How to check a venue:**
1. Compare the traced length with the 1991 length.
2. Look at the overview PNG against period layout maps.
3. Set `"debug": true` to print the length of each via leg. One overly long
   leg means a detour.

## Workflow per venue

1. **Research the 1991 layout:** direction, corner names, start/finish, which
   chicanes existed. Use Wikipedia, touringcarracing.net race pages and
   circuit databases.
2. **Download the area** (`bbox`) and render a diagnostic map of the
   race-relevant ways with their IDs.
3. **Write the spec:** route filters, via points along the 1991 line,
   exclusions for later layout changes, and bridges for vanished sections.
4. **Generate the track.** Check the traced length (within about 2%) and the
   overview picture.
5. **Rebuild and install the pack, then check in-game:** cars stay on the
   drawn line, nothing hidden behind overlays, sensible lap times.

## DTM 1991 venues

Confidence ratings are from the layout research. Sources are listed in each
spec's `notes` and in the season dossier.

| Venue | 1991 length | How it's built | Traced | Confidence |
|---|---|---|---|---|
| Zolder | 4.194 km | Raceway loop. Today's layout. | 3,953 m (−5.7%) | High. The 1991 chicane details may differ. |
| Hockenheim | 6.797 km | Via over today's Motodrom plus the 1932–2001 `abandoned:highway=raceway` forest loop. 2 bridges: the Nordkurve exit, and the Senna chicane exit to the Agip approach. Has all three 1991 chicanes. Today's Parabolika/Spitzkehre section is excluded. The overview draws the post-2002 clearings as forest (`historic_forest`), with a verge along the old track. | 6,716 m (−1.2%) | High |
| Nürburgring GP | 4.542 km | Via. Today's GP with the "Variante 24h-Rennen" in place of the 2002 Mercedes Arena. | 4,548 m (+0.1%) | High |
| Norisring | 2.300 km | Via over OSM circuit relation 1889538, counter-clockwise. Unchanged since 1972. | 2,207 m (−4%) | High |
| Alemannenring (Singen) | 2.800 km | Via over 6 named streets, clockwise. 3 bridges (an underpass junction and the hairpin across the central reservation). | 2,817 m (+0.6%) | High for the streets. The hairpin position is unverified. |
| AVUS | 4.880 km | Via over the A115 carriageways (OSM tags them `abandoned:highway=raceway`) and the Nordkurve, counter-clockwise. The south turn is a bridge. | 4,872 m (−0.2%) | **Low for the south turn.** Its 1991 position is undocumented, so it is placed where the lap measures 4.880 km. The 1991 chicane isn't modelled. |
| Diepholz | 2.690 km | Via over runway 08/26 and the northern taxiway, counter-clockwise | 2,665 m (−0.9%) | Medium. The chicanes aren't modelled. |
| Wunstorf | 5.050 km | Via over runways 03/21 and 08/26. The west perimeter road is a multi-point bridge, mapped from the 1993 Commons diagram (which has a north arrow) by an affine fit to the runway ends. | 4,554 m (−10%) | **Low to medium.** Direction comes from one diagram arrow. The perimeter road and the 1991 sweeper are approximate. |

### Added for 1990 and 1992

| Venue | Season | Length | How it's built | Traced |
|---|---|---|---|---|
| Nordschleife + GP | 1990, 1992 | 25.3 km | Via over the GP circuit and the Nordschleife, left at Hatzenbach, Hohenrain link back | 25,905 m (+2.4%) |
| Mainz-Finthen | 1990 | 2.250 km | Runway 07/25 and taxiways A and C, clockwise. The 1980s chicane step isn't modelled. | 2,135 m (−5%) |
| Brno | 1992 | 5.394 km | The "Masarykův okruh" ways, clockwise | 5,362 m (−0.6%) |
| AVUS (short) | 1992 | 2.640 km | The 1991 AVUS with the south turn moved north (position undocumented) | 2,620 m (−0.8%) |
| Hockenheim Motodrom | 1992 | 2.634 km | The short circuit over today's "Kleiner Kurs" link | 2,574 m (−2.3%) |
| Nürburgring Sprint | 1992 | 3.029 km | The 1984 GP circuit with the Kurzanbindung | 3,045 m (+0.5%) |

### Added for 2013

Eight modern venues, each with one DRS zone except Zandvoort. See
[the 2013 pack README](../seasons/dtm-2013/README.md#tracks) for how each one
is built and how its traced length compares.

Each season reuses the 1991 tracks through `shared_tracks`, and sets its own
lap lengths and race laps through `track_overrides`.

### Open questions

- **AVUS:** where was the 1991 south turn, and where was the chicane? A
  1989–91 Avusrennen programme or an ADAC map would settle both.
- **Wunstorf:** what was the exact 1991 route back onto 03/21 (sweeper vs.
  hairpin), and what is the true scale of the west perimeter road?
- **Diepholz and Wunstorf:** where were the 1991 chicanes?

## Race distance and lap-time calibration

**Race distance.** The game races `laps` (the pack's `options.json`, 50) ×
the track's `lap_modifier` laps. The track spec's `race_laps` sets this to the
real 1991 heat distance, about 100 km:

| Track | Laps |
|---|---|
| Zolder | 24 |
| Hockenheim | 15 |
| Nürburgring | 22 |
| AVUS | 21 |
| Wunstorf | 20 |
| Norisring | 44 |
| Diepholz | 37 |
| Alemannenring | 36 |

An earlier version misused `lap_modifier` as a lap-time knob, which gave
races of 45–56 laps.

**Lap time.** The spec's `speed_scale` multiplies every micro-sector target
speed. The real 1991 results for every session are in
`seasons/dtm-1991/research/results/` (from touringcarracing.net). After an
in-game qualifying session:

1. Run `python tools/calibrate.py seasons/dtm-1991 --observe-save "<game>/saves/<save>.json"`.
2. Run `python tools/calibrate.py seasons/dtm-1991 --apply`. This computes
   the new scale as old scale × game pole ÷ real pole.
3. Regenerate the tracks, then rebuild and install the pack.

**Starting values:**
- **Zolder:** 1.22, measured. The first build's in-game pole was 1:45.4
  against the real 1:42.7.
- **Hockenheim:** 0.98, from a practice time.
- **Other tracks:** estimates. They all need an in-game qualifying session.

**Pit stops.** The 1991 heats were ~100 km sprints with no planned stops,
only for damage or penalties, and no refuelling. Tyre wear is set (0.6× the
earlier values) so a heat runs without stopping. This still needs an
in-game check.

## Rules of thumb

- **Use the 1991 length** for `length_km`. Record the difference from the
  traced length in `notes`.
- **Exclude later additions** (chicanes added after 1991, new sections) by
  way ID, and say why in `notes`.
- **Bridges are a last resort.** Each one is a straight line, so keep them
  short and document them.
- **Airfields and street circuits** need `width_m` matching the real course,
  about 12–15 m. Use `overtaking_difficulty` for how hard passing is.
- **Don't hand-tune `lap_modifier`.** Micro-sector speeds use the base game's
  reference scale. Lap times are set only through the calibration loop above.
- **Re-check lap times whenever a track's geometry changes.** A new route or
  new corner speeds changes the lap.
