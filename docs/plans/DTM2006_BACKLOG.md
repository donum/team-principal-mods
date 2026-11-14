# Backlog: DTM 2006 pack

Everything still open for the 2006 pack, as of 13 November 2026. Era-wide
items (lap-time calibration, two stops, engine sounds, tracks to trace,
logos) are in the [2003 backlog](DTM2003_BACKLOG.md), since 2006 builds on
`bases/dtm-era3` with 2003 as the mother template. Game limits are in
[DEVELOPER_WISHLIST.md](../DEVELOPER_WISHLIST.md).

Priority: **P1** = changes how the game plays, **P2** = more of the real
season, **P3** = presentation.

- **Futurecom TME second car** · P1: the #19 car had four drivers
  (Tielemans, Bleekemolen, Kiesa, Björk), none for half the season, so
  `season_from_research.py` seats none of them and TME runs one car. Needs
  a generator option to seat by car number or a per-team seat count.
- **Tracks** · P2: Barcelona national and Le Mans Bugatti are traced into
  the base; calibrate their `speed_scale` (see the 2003 backlog).
- **2004 cars' weight** · P2: not found; they use the 2005 cars' 1,035 kg.
- **Success ballast** · P2: ±10 kg per make after each round, not possible
  (wishlist B1, B2). Could be approximated with a lower rating for Mercedes.
- **Sponsors, colours, car images, logos, portraits** · P3: as for 2003.
- **Unverified laps** · P2: most laps derived from distance; Brands Hatch
  82 or 85 laps (`research/season.md`).
