# Era base: DTM 2019–2020 (Class One turbo)

Builds on [`bases/dtm-era4`](../dtm-era4) (`"base": "dtm-era4"`): the Class
One chassis carried over from 2018, so the traced tracks, tyre model,
damage, car parts, car profiles and the Hankook tyre come from there.

This base changes only:
- `gen.json`: the 2.0 turbo engines (Audi RC8 2.0 TFSI, BMW P48 Turbo),
  1,070 kg with driver and fuel, chassis names for 2019 and 2020.
- `patches/regulations.json` (applied after era 4's): car profile
  `dtm_class1_turbo`, minimum weight, push-to-pass as spec ERS, one open
  qualifying session per race, a pole point.
- `tracks/`, `track_specs/`: the venues era 4 doesn't have, traced from
  OpenStreetMap: Assen (`assen`) and today's Zolder (`zolder20`).
- `base.json` `"audio"`: its own sound overlay `dtm-era5`, off for now
  (`in_pack: false`), so the era 4 V8 sounds are not used and the packs keep
  the game's vanilla sounds.

**Mother season: 2020.** It was the first season built on this base, so the
turbo sounds will be collected from 2020 cars (`recording_years`,
`research_season`) and 2019 inherits them. Open era-wide work is in
[docs/plans/DTM2020_BACKLOG.md](../../docs/plans/DTM2020_BACKLOG.md).

For 2019, add the Aston Martin Vantage DTM (HWA AFR Turbo 2.0 I4, R-Motorsport)
to `gen.json` `engines` and `chassis` in the season's own `gen.json`.
