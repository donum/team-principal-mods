# DTM 2010: Season Pack

Status: **v0.1, generated and builds, not yet tested in-game.** Lap times
and tyre wear are first guesses, not simulated. The data was generated with
`tools/season_from_research.py` from `research/`, configured in `gen.json`.
For the sourced facts, see [research/season.md](research/season.md). What
is still open is in the [backlog](../../docs/plans/DTM2010_BACKLOG.md);
era-wide items are in the [2003 backlog](../../docs/plans/DTM2003_BACKLOG.md).

**Era base:** 2010 builds on [`bases/dtm-era3`](../../bases/dtm-era3),
set up on 2003 (the era's mother template). It inherits the rules, the
Dunlop tyre, the engines and the era's engine sounds (none collected yet:
vanilla sounds for now). 2010 changes the car profiles (Audi A4, AMG
C-Klasse W204) and the weight. It was Dunlop's last DTM season.

## How it's built

- **Teams and drivers:** 9 teams, 18 seats and 19 drivers from
  `research/entries.csv`.
  - HWA: Salzgitter/Mercedes-Benz Bank (#3, #4) and Laureus (#7, #8).
  - Persson runs three cars as one team (Green, Stoddart and Cheng's Stern
    car #21).
  - The Audi Sport Rookie Team Abt is a one-car team (Molina).
  - Phoenix: Prémat has the seat, O'Young (Shanghai only) is a reserve.
- **Car generations:** HWA and the two Abt works teams ran 2009 cars,
  everyone else 2008 cars. The 2008 teams get `potential: 3` (wishlist C4,
  D7). All cars weigh 1,050 kg; the lighter older cars in ru.wiki are
  unverified and not used.
- **Ratings:** average points per car over 54–57.5; driver skill 11–18.
- **Previous position:** the 2009 teams' standing.
- **Colours:** first estimates, not checked against photos.
- O'Young is Chinese in the pack (de.wiki); en.wiki says Hong Kong.

## Rules

| Rule | 2010 | Pack |
|---|---|---|
| Points | 10-8-6-5-4-3-2-1 | `dtm_top8` (base) |
| Qualifying | knockout in 4 parts, Q4 a single-lap shootout of the top 4 | `knockout` (3 parts) |
| Pit stops | 2 mandatory, with tyres | tyre wear makes two stops normal |
| Refuelling | allowed | allowed, 60 kg tank |
| Tyres | Dunlop SP Sport Maxx control tyre | one dry compound |
| Weight | 1,050 kg incl. driver | 905 kg chassis + 145 kg engine (season patch) |
| Race | 160–190 km, with a time limit | full lap count |

## Tracks

Hockenheim GP, Valencia, Lausitz, Norisring, Nürburgring short, Zandvoort,
Brands Hatch Indy and Oschersleben use the era 4 traces. Adria (`adria`)
is traced in the era base, with 2010's laps and tyre wear in `gen.json`.
**Placeholders:** the 3.736 km Hockenheim layout (`hockenheim10`, on the GP
trace: OSM's only short layout, the Kleiner Kurs, is about 2.6 km, so the
3.736 km figure needs a source first) and the Shanghai street circuit
(`shanghai`, on the Norisring: a temporary 2010 circuit that OSM doesn't
have).

## Simplifications

See the [wish list](../../docs/DEVELOPER_WISHLIST.md):
- **A5, A6:** no four-part knockout with a Q4 single-lap shootout.
- **A3:** races ran to a time limit; the game runs the full lap count.
- **B5:** two mandatory stops can't be required.
- **B7:** one spec dry tyre.
- **C2:** O'Young's single round is not modelled (reserve).
- **C4, D7:** 2008 cars are a rating, not real older cars; the
  development freeze isn't modelled.
- Also D1, D3, E1, E2, E8.

## Gaps

- The short Hockenheim and Shanghai are placeholders; Adria is traced but not calibrated.
- No car images, team logos, portraits or sponsors.
- Lap times and tyre wear not simulated.

## Rebuild

```bash
python tools/season_from_research.py seasons/dtm-2010
```

```bash
python tools/build_pack.py seasons/dtm-2010
```
