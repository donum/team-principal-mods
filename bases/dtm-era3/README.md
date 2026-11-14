# Era base: DTM 2000–2011 (era 3)

V8 silhouettes: Abt-Audi TT-R and Audi A4, AMG-Mercedes CLK and C-Klasse,
Opel Astra V8 Coupé and Vectra GTS V8 (until 2005). 4.0 V8s with
restrictors, Dunlop control tyre, two mandatory stops and refuelling.
See [bases/README.md](../README.md) for how bases and seasons layer.

**Mother template: 2003.** It was the first era-3 season built, so the
base was set up on it, and the era's engine sounds will be recorded from its
cars (`base.json` `"audio"`: overlay `dtm-era3`, `recording_years: [2003]`,
`research_season: dtm-2003`). Every later era-3 season inherits them. None
are collected yet, so `in_pack` is false and the packs keep vanilla sounds.

Seasons on it: [2003](../../seasons/dtm-2003), [2006](../../seasons/dtm-2006),
[2010](../../seasons/dtm-2010).

| File | Holds |
|---|---|
| `base.json` | era constants (top-8 points), shared tracks from `dtm-era4` and the 1991 Norisring, their tyre wear, the sound overlay |
| `gen.json` | rating ranges, car profiles (TT-R, A4, CLK, C-Klasse, Astra, Vectra), engines, chassis names 2000–2011, the Dunlop tyre |
| `patches/regulations.json` | top-8 points, car profile `dtm_v8_silhouette` (uncalibrated), 1,080 kg, refuelling, one dry compound, knockout qualifying, up to three cars a team |
| `data/` | one-dry-compound tyre model (2012 style), touring-car part names, damage and radio texts as in era 4 |
| `assets/engines/` | Audi and Mercedes-Benz logos (copied from era 4); Opel has none yet |

Era 3's own traces (`track_specs/`, `tracks/`, `tools/osm_track.py`):
`adria`, `donington`, `lausitzring03` (2003), `catalunya_national`,
`lemans` (2006). Each spec carries its first season's laps and tyre wear;
a later season sets its own in `track_overrides`. All use `speed_scale` 1.0
(uncalibrated). Other venues use the era 4 traces; 2010's short Hockenheim
and Shanghai are still placeholders in that season's `gen.json`. Open items:
[docs/plans/DTM2003_BACKLOG.md](../../docs/plans/DTM2003_BACKLOG.md).
