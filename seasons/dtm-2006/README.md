# DTM 2006: Season Pack

Status: **v0.1, generated and builds, not yet tested in-game.** Lap times
and tyre wear are first guesses, not simulated. The data was generated with
`tools/season_from_research.py` from `research/`, configured in `gen.json`.
For the sourced facts, see [research/season.md](research/season.md). What
is still open is in the [backlog](../../docs/plans/DTM2006_BACKLOG.md);
era-wide items are in the [2003 backlog](../../docs/plans/DTM2003_BACKLOG.md).

**Era base:** 2006 builds on [`bases/dtm-era3`](../../bases/dtm-era3),
set up on 2003 (the era's mother template). It inherits the rules, the
Dunlop tyre, the engines and the era's engine sounds (none collected yet:
vanilla sounds for now). 2006 changes the car profiles (Audi A4, AMG
C-Klasse W203), the weights and the knockout qualifying.

## How it's built

- **Teams and drivers:** 10 teams, 19 seats and 23 drivers from
  `research/entries.csv`. Single-car Mercedes entries are paired as in the
  teams' standings: Vodafone/Salzgitter and DaimlerChrysler Bank (HWA),
  Stern/Easy Rent (Persson), TV-Spielfilm/TrekStor (Mücke) and
  AutoScout24/Junge Gebrauchte (#21 Persson, #22 Mücke).
- **Car generations:** each make ran 4 new, 4 one-year-old (2005) and 2
  two-year-old (2004) cars. Older cars weigh 890 kg (1,035 kg real) against
  905 kg (1,050 kg), and get `potential` 3 (2005 cars) or 2 (2004 cars)
  instead of 6 (wishlist C4, D7). The 2004 cars' real weight is not known.
- **Futurecom TME** runs one seat (Ickx). Its #19 car had four drivers, none
  for half the season, so the generator seats none of them (see Gaps).
- **Ratings:** average points per car over 53–57.5; driver skill 11–18.
- **Previous position:** the 2005 teams' standing, with Phoenix, Rosberg and
  the new teams placed after it.
- **Colours:** first estimates, not checked against photos.

## Rules

| Rule | 2006 | Pack |
|---|---|---|
| Points | 10-8-6-5-4-3-2-1 | `dtm_top8` (base) |
| Qualifying | knockout in 3 parts, slowest 6 out per part | `knockout` (base) |
| Pit stops | 2 mandatory, with tyres | tyre wear makes two stops normal |
| Refuelling | allowed, 70 L | allowed, 60 kg tank |
| Tyres | Dunlop, 7 sets per weekend | one dry compound, `light` allocation |
| Weight | 1,050 kg new, 1,035 kg older | 905 / 890 kg chassis (season patch) |
| Success ballast | ±10 kg per make, max ±20 | not modelled |

## Tracks

Hockenheim, Lausitz (3.442 km), Oschersleben, Brands Hatch Indy, Norisring,
Nürburgring short and Zandvoort use the era 4 traces. Barcelona national
circuit (`catalunya_national`, 2,872 m against 2,949 m, routed over the
link after turn 2) and Le Mans Bugatti (`lemans`, 4,112 m against 4,180 m)
are traced in the era base. Both are uncalibrated (`speed_scale` 1.0).

## Simplifications

See the [wish list](../../docs/DEVELOPER_WISHLIST.md):
- **A6:** the knockout can't drop six per part.
- **B1, B2:** no manufacturer success ballast.
- **B5:** two mandatory stops can't be required.
- **B7:** one spec dry tyre; the 7-set allocation is the game's 15-set
  `light` rule.
- **B10:** the smaller pit crews of 2006 aren't modelled.
- **C2:** the #19 Futurecom car's four drivers can't share one seat.
- **C4, D7:** older car generations are a weight and a rating, not real
  older cars; the development freeze isn't modelled.
- Also D1, D3, E1, E2, E8.

## Gaps

- Futurecom TME has one car instead of two (tool gap: seats per car number).
- Barcelona and Le Mans are traced but not calibrated; the Barcelona stadium section follows today's ways.
- No car images, team logos, portraits or sponsors.
- Lap times and tyre wear not simulated.

## Rebuild

```bash
python tools/season_from_research.py seasons/dtm-2006
```

```bash
python tools/build_pack.py seasons/dtm-2006
```
