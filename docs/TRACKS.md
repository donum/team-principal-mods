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
| **Via route** | Street circuits, airfields, old or changed layouts | `route_ways` (tag filters) and/or `route_relation` (an OSM `type=circuit` relation), `via` (points in driving order), `exclude_way_ids`, `bridges` (missing links; more than 2 points = a hand-placed polyline), `start`, `bbox_tiles` (extra download boxes for dense cities) |

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
| Hockenheim | 6.797 km | Via over today's raceway plus the 1932–2001 `abandoned:highway=raceway` forest loop, and 1 bridge (Nordkurve exit). Has all three 1991 chicanes. | 6,895 m (+1.4%) | High |
| Nürburgring GP | 4.542 km | Via. Today's GP with the "Variante 24h-Rennen" in place of the 2002 Mercedes Arena. | 4,548 m (+0.1%) | High |
| Norisring | 2.300 km | Via over OSM circuit relation 1889538, counter-clockwise. Unchanged since 1972. | 2,207 m (−4%) | High |
| Alemannenring (Singen) | 2.800 km | Via over 6 named streets, clockwise. 3 bridges (an underpass junction and the hairpin across the central reservation). | 2,817 m (+0.6%) | High for the streets. The hairpin position is unverified. |
| AVUS | 4.880 km | Via over the A115 carriageways (OSM tags them `abandoned:highway=raceway`) and the Nordkurve, counter-clockwise. The south turn is a bridge. | 4,872 m (−0.2%) | **Low for the south turn.** Its 1991 position is undocumented, so it is placed where the lap measures 4.880 km. The 1991 chicane isn't modelled. |
| Diepholz | 2.690 km | Via over runway 08/26 and the northern taxiway, counter-clockwise | 2,665 m (−0.9%) | Medium. The chicanes aren't modelled. |
| Wunstorf | 5.050 km | Via over runways 03/21 and 08/26. The west perimeter road is a multi-point bridge, mapped from the 1993 Commons diagram (which has a north arrow) by an affine fit to the runway ends. | 4,554 m (−10%) | **Low to medium.** Direction comes from one diagram arrow. The perimeter road and the 1991 sweeper are approximate. |

### Open questions

- **AVUS:** where was the 1991 south turn, and where was the chicane? A
  1989–91 Avusrennen programme or an ADAC map would settle both.
- **Wunstorf:** what was the exact 1991 route back onto 03/21 (sweeper vs.
  hairpin), and what is the true scale of the west perimeter road?
- **Diepholz and Wunstorf:** where were the 1991 chicanes?

## Rules of thumb

- **Use the 1991 length** for `length_km`. Record the difference from the
  traced length in `notes`.
- **Exclude later additions** (chicanes added after 1991, new sections) by
  way ID, and say why in `notes`.
- **Bridges are a last resort.** Each one is a straight line, so keep them
  short and document them.
- **Airfields and street circuits** need `width_m` matching the real course,
  about 12–15 m. Use `overtaking_difficulty` for how hard passing is.
- **Lap-time calibration happens later and for all tracks at once.** The
  micro-sector speeds use the base game's reference scale, and the
  `car_profile` regulation scales them.
