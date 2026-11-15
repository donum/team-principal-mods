# Venues: per-track facts for every pack

What a pack needs to know about a circuit beyond its shape: pit-lane loss,
retirements, overtaking, grid side, weather. Every series and season shares
this folder, so a fact found for DTM 2013 also serves 2012, 2014 or an F1
pack at the same venue. The track specs (`track_specs/*.json`) take their
values from here; the season browser shows them in its Tracks section.

Venue names are the keys of `tools/track_inventory.py` (`venue_key()`), the
same ones the season browser uses: "Hockenheim", "Red Bull Ring (A1-Ring)",
"Nürburgring GP"...

## Files

| File | What | Built by |
|---|---|---|
| [race_stats.csv](race_stats.csv) | One row per race with results in `seasons/*/research/results/`: starters, retirements by cause, grid-to-finish swaps, safety car and rain in the notes | `python -I tools/venue_stats.py` (generated, don't edit) |
| [venue_facts.csv](venue_facts.csv) | Sourced facts, one per row: pit speed limit, pit-lane length, published pit loss, grid side, climate, wet races | By hand and by the tools below; keep the source |

### venue_facts.csv columns

| Column | Meaning |
|---|---|
| `venue` | Venue key (see above) |
| `track` | Our track id when the fact is about one layout (`brandshatch` vs `brandshatch_gp`); empty = the whole venue |
| `field` | `pit_speed_limit_kmh`, `pit_lane_length_m` (pit-in to pit-out line, the speed-limit zone), `osm_pit_lane_m` (the whole lane as mapped), `pit_loss_s`, `pole_side`, `rain_days_<mon>` (days with ≥ 1 mm), `precip_mm_<mon>`, `weather_station`, `wet_race` |
| `value`, `unit` | The value |
| `applies_to` | Years or series it holds for ("DTM 2013", "2000-2018", "climate 1991-2020") |
| `status` | `verified`: a source states it. `derived`: measured or computed by our tools. `estimate`: an inference, reason in `note` |
| `source` | URL, a repo file, or a TV moment as `tv: <video path under the archive> @ h:mm:ss` |
| `note` | How it was read, caveats |

Later rows win over earlier ones for the same venue, track and field.

## From facts to game values

The game reads these track fields (checked in the game code, build 44328799):

| Track field | What the game does with it | Where our value comes from |
|---|---|---|
| `pit_lane_loss_s` | Time lost driving through the pit lane (default 18.5 s). The tyre service time is rolled on top | Published loss (`pit_loss_s`) if there is one, else `tools/pit_lane.py` (OSM pit lane, speed limit, lap speed) |
| `dnf_modifier` | Multiplies both the crash and the mechanical failure chance, rolled every lap (default 1.0) | Fitted with `tools/simulate.py` runs to the venue's real retirements per starter (pulled towards the series mean when there are few races). Long races need a low value: at 1.0 Brands Hatch (98 laps) loses 30% of the field |
| `overtaking_difficulty` | Multiplies the time lost in dirty air behind another car (default 1.0); higher = harder to pass | Fitted the same way to the real grid-to-finish swaps per car |
| `starting_grid.pole_side` | Which side pole starts on | `pole_side`, read off the TV start |
| `wet_weather_probability_multiplier` | Scales the game's chance of rain | Rain days in the race month over the calendar mean |
| `fuel_consumption` | Fuel burn per lap | Unchanged; DTM had no refuelling and a 120 L tank |

`python -I tools/venue_stats.py --pack seasons/dtm-2013 --years 2012-2013`
prints the suggestions next to the values now in the specs.

`--apply` writes what is sourced, not what is estimated: `pole_side` and a
published `pit_loss_s`, from facts whose `applies_to` names the pack's series
(a GT4 or F1 pit delta stays out of a DTM pack), and the rain multiplier from
the climate rows. It edits the spec the pack builds from and keeps its layout;
a track borrowed from another season (the 2013 Norisring comes from 1991) gets
the value in the base's `track_overrides` instead. Then rebuild the track
files (`tools/art_track.py` or `tools/osm_track.py`) and the pack.
`dnf_modifier` and `overtaking_difficulty` come from the simulator, like the
lap times from `tools/calibrate.py`:

```bash
python tools/simulate.py dtm-2013 --runs 4 --out build/sim/dtm-2013/venues-fit1
```
```bash
python -I tools/venue_stats.py --pack seasons/dtm-2013 --years 2012-2013 --sim build/sim/dtm-2013/venues-fit1 --fit
```

`--sim` pools the runs (all made with the track values now in `dist/`),
counts retirements and swaps per track the same way as for the real races,
and moves each value by target / simulated. `--fit` writes them. Rebuild the
pack and simulate again until the two agree.

`python -I tools/pit_lane.py <specs>` prints the pit-lane estimate per track.
With `--csv` it prints `osm_pit_lane_m` rows for this file.

## What we have (2026-11-15)

- **Grid side:** DTM 2013, read off the TV start at 8 of 9 venues (the wet
  Nürburgring race started behind the safety car). Five specs were wrong
  (Lausitzring, Moscow, Norisring, Oschersleben right; Zandvoort left).
- **Climate:** rain days and precipitation per month for the 12 DTM 2012–2018
  venues. Wikipedia's German climate tables count days with ≥ 0.1 mm under a
  "≥ 1 mm" label; the German rows here are counted from DWD daily data instead.
- **Pit lane:** 60 km/h for the whole DTM event (2017 regulations; 2012–2014
  assumed the same). Limit-zone lengths for Hockenheim, Nürburgring, Red Bull
  Ring, Zandvoort (post-2020), Misano, Valencia from SRO briefings. No DTM pit
  loss is published; the GT4 and F1 figures are kept for reference only.
- **Race stats:** DTM 1991, 2012, 2013 and F1 2010–2013 (the seasons with
  results files). Two DTM races per venue is a thin base: more seasons'
  results make the suggestions firmer.

## TV coverage

The downloaded broadcasts (see `tools/tv_coverage/`) are a source too:

- `transcribe.py` turns the commentary into timestamped text
  (`private/tv_coverage/transcripts/`, private: it belongs to the broadcaster);
- `frames.py` makes stills and contact sheets to read the grid, the timing
  graphics and the weather.

Only the facts go into this folder, with the video and time as the source.
