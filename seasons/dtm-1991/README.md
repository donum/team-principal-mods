# DTM 1991: Season Dossier

Status: **v0.2, playable.** All 8 tracks are generated from OpenStreetMap, all 22
cars and logos are done, and race distances are the real 1991 heat lengths.
Lap times are still waiting for in-game calibration. See [Roadmap](#roadmap).

This file records **what we know, where it comes from, and what's a game-design
estimate**. Corrections with a source are very welcome.

## Sources

| Id | Source |
|---|---|
| S1 | touringcarracing.net season page: <http://touringcarracing.net/Pages/1991%20DTM.html> |
| S2 | touringcarracing.net classifications: <http://touringcarracing.net/Pages/1991%20DTM%20Class.html> |
| S3 | touringcarracing.net race pages: `http://touringcarracing.net/Races/1991%20<Venue>.html` |
| S4 | touringcarracing.net car sheet: <http://touringcarracing.net/Pages/1991%20Cars.html> |
| S5 | de.wikipedia "Deutsche Tourenwagen-Meisterschaft 1991" |
| S6 | en.wikipedia "1991 Deutsche Tourenwagen Meisterschaft" |
| S7 | de.wikipedia "Audi V8 quattro DTM" |
| S8 | Wikidata (dates of birth) |

The Automobilista 2 "DTM 1991" mod (v1.41): its 1991 livery artwork is used
in the car images and team decals, with the livery author's permission. Its numbers, drivers and colours matched our sources, except that it
gives Ludwig #7 in its XML while his car is painted #8.

## Calendar: 10 DTM rounds (`data/schedule.json`)

| Wk | Date | Venue | Track id | Length | Type | Heat winners [S5/S6] |
|---|---|---|---|---|---|---|
| 13 | 31 Mar | Zolder (BEL) | `zolder` | 4.194 km | permanent | Cecotto / Cecotto |
| 15 | 14 Apr | Hockenheimring | `hockenheim` | 6.797 km | permanent | Soper / Soper |
| 16 | 21 Apr | Nürburgring GP | `nuerburgring` | 4.542 km | permanent | Ludwig / Ludwig |
| 18 | 5 May | AVUS, Berlin | `avus` | 4.880 km | street/autobahn | Stuck / Biela |
| 23 | 9 Jun | Wunstorf | `wunstorf` | 5.050 km | airfield | Winkelhock / Cecotto |
| 26 | 30 Jun | Norisring | `norisring` | 2.300 km | street | Thiim / Stuck |
| 31 | 4 Aug | Diepholz | `diepholz` | 2.690 km | airfield | Stuck / Soper |
| 36 | 8 Sep | Nürburgring GP | `nuerburgring` | 4.542 km | permanent | Ludwig / Ludwig |
| 37 | 15 Sep | Alemannenring, Singen | `alemannenring` | 2.800 km | street (new) | Biela / Stuck |
| 39 | 29 Sep | Hockenheimring | `hockenheim` | 6.802 km | permanent | Biela / Biela |

**Not included:**

- **Brno** (6 Oct) and **Donington** (20 Oct). These were ITR Cup rounds and
  scored no DTM points [S1, S2, S5].
- The Kyalami and Macau invitation races.

**The 1991 weekend format** (sources: touringcarracing.net round pages, de.wikipedia):
- **Qualifying** (two sessions) set grid places 1–16. Everyone else ran a
  roughly 50 km qualification race for places 17 and lower. Heat fields had
  32–40 cars.
- **Two heats of about 100 km each.** Both paid full points
  (20-15-12-10-8-6-4-3-2-1). The heat-2 grid was the heat-1 finishing order.
- **No planned pit stops and no refuelling.** Cars stopped only for damage
  or penalties.
- **Success ballast** went up to 50 kg. Drivers new to the series started on
  the maximum. The per-position scale is unknown.
- **No Nordschleife in 1991.** The DTM raced it in 1988–90 and 1992–93,
  always 2 × 4 laps.

**What the game can model:**
- **One race per round** at the real heat distance (`race_laps`). Two heats
  per weekend aren't possible.
- **Grid limit 40,** so the whole field starts.
- **No forced stops:** tyre wear is tuned so a heat runs without one.
- **Not modelled:** the qualification race and success ballast.

## Rules (`patches/regulations.json`, `season.json` → constants)

| Rule | 1991 reality | In game |
|---|---|---|
| Points | 20-15-12-10-8-6-4-3-2-1 per heat, all results count [S5, S6] | `points_system: dtm_1991`, `POINTS_TOP10` |
| Car base | FIA Group A + ONS rules, Evo homologations | `car_profile: group_a_touring` (multipliers **to calibrate**) |
| Weight | Displacement-based. BMW/Merc 980–990 kg, Opel 1130 kg (−50 kg after round 2), Audi 1290 kg (−40 kg from Wunstorf), Mustang 1160 kg [S3, S4] | Team `car_mass_kg` = car minus engine `mass_kg` (assumption 🧪) |
| Success ballast | Up to 50 kg; newcomers start on maximum [S3] | ❌ not modelled |
| Tyres | Open tyre war [S3] | Five suppliers; see team table |
| Refuelling, DRS, ERS | none | banned / disabled |
| Grid | ~16 direct qualifiers plus a qualification race | `QUALI_GRID_LIMIT = 30` |

## Entrants (`data/teams.json`, `data/drivers.json`)

**Legend:**
- **P** = partner (works-supported) engine deal, **C** = customer engine deal.
- **(R)** = reserve or guest driver.
- Tyres marked † are **unverified** assignments.

| Team | Car / engine | Tyres | Drivers (#) |
|---|---|---|---|
| SMS Schmidt Motorsport | Audi V8 quattro (P) | Dunlop | Stuck 1, Haupt 2, (R) Röhrl 46 |
| AZR Audi Zentrum Reutlingen | Audi V8 quattro (P) | Dunlop | Jelinski 44, Biela 45 |
| BMW M Team Schnitzer | BMW M3 Evo (P) | Yokohama | Cecotto 3, Winkelhock 4, Nissen 5 |
| BMW M Team Bigazzi | BMW M3 Evo (P) | Pirelli † | Soper 11, Hahne 12 |
| AMG Mercedes | 190E Evo II (P) | Bridgestone | Thiim 7, Ludwig 8, Lohr 78, (R) Kreutzpointner 87 |
| Zakspeed Racing | 190E Evo II (P) | Pirelli † | Giroix 18, Asch 19, (R) B. Schneider 88, (R) M. Schumacher 20 |
| Snobeck Racing | 190E Evo II (P) | Michelin † | Cudini 9, Laffite 10 |
| MS-Jet Racing | 190E Evo II (P) | Pirelli † | Schmickler 22, van Ommen 23, (R) Mass 24 |
| Linder M Team | BMW M3 Evo (C) | Yokohama † | Quester 15, Heger 16, Meeuvissen 17, (R) Menu 65 |
| MM Diebels Alt | BMW M3 Evo (C) | Michelin † | Danner 31, Rensing 32, (R) Murmann 33 |
| Unitron Sports | BMW M3 Evo (C) | Yokohama † | Zakowski 13, Kelleners 14 |
| BMW Team Isert | BMW M3 Evo (C) | Yokohama † | Leopold von Bayern 30, (R) Oestreich 29 |
| Tic Tac Tauber Team | BMW M3 Evo (C) | Yokohama † | Berg 43 |
| Auto Maass Climair Team | BMW M3 Evo (C) | Yokohama † | K. König 28 |
| Valier Motorsport | BMW M3 Evo (C) | Pirelli † | Maggiorelli 34 |
| Marlboro BMW Dealer Team | BMW M3 Evo (C) | Yokohama † | Euser 42 |
| Team Vanicek | BMW M3 Evo (C) | Yokohama † | H. Becker 55 |
| BAS Reifendienst | 190E Evo II (C) | Pirelli † | Bernhard 50 |
| Opel Team Eggenberger | Omega 3000 Evo 500 (P) | Michelin | Niedzwiedz 25, Ferté 26 |
| Opel Team Irmscher | Omega 3000 Evo 500 (P) | Michelin † | Engstler 36, Strycek 37 |
| Opel Team Schübel | Omega 3000 Evo 500 (C) | Pirelli † | Oberndorfer 66, (R) Reuter 99 |
| Gerd Ruch Motorsport | Ford Mustang 5.0 GT (C) | Dunlop | G. Ruch 40 |

**How the roster was simplified for the game:**

- **AMG ran four cars**, but the game allows at most three entries per team, so
  Kreutzpointner is a reserve.
- **Part-time and guest drivers are reserves.** This covers Röhrl, B. Schneider,
  M. Schumacher, Mass, Reuter, Menu, Murmann and Oestreich.
- **Left out:** one-off entries such as Ickenstein, Dufter, J. Ruch, Räker,
  Heinz Becker (Gronemeyer), Haider and Venc. Their data is incomplete.
- Schmickler's two late-season Irmscher Opel drives are not modelled.

**What's sourced and what's estimated:**

| Category | Status | Notes |
|---|---|---|
| Names, numbers, entrants, nationalities, birth dates | **Sourced** [S3, S5, S6, S8] | Ages are taken at season start. |
| Luca Maggiorelli's age | **Unknown** | Set to 30 as a placeholder. |
| Driver titles | Background knowledge, **to verify** | Stuck 1990, Ludwig 1988, Strycek 1984. |
| Team titles | Background knowledge, **to verify** | Schnitzer 1989 (Ravaglia), SMS 1990 (Stuck). |
| Driver skills, talent, traits, personalities, salaries | **Estimates** | Calibrated on the 1991 standings: Biela 174, Ludwig 166, Stuck 158, Cecotto 147, Soper 133, Cudini 106... [S5, S6]. |
| Team ratings, finances, HQ levels | **Estimates** | |
| Staff | **Generated placeholders** | Real 1991 engineers are mostly undocumented. |

## Engines (`data/engines.json`)

| Supplier | Engine | 1991 data [S4, S7] | Game estimate |
|---|---|---|---|
| Audi | 3.6 V8 32V, quattro 4WD | ~460 hp (rivals claimed 500+) | power 60, heavy (190 kg) |
| BMW | S14 2.5 16V | 382 hp @ 8750 | power 52, reliable |
| Mercedes-Benz | 2.5-16 (AMG-built) | ~340–360 hp | power 50, most reliable |
| Opel | 3.0 24V straight-six | 385 hp, heavy car | power 51, fragile |
| Ford | 5.0 V8 (Mustang) | 520 hp, 1160 kg | power 62, very fragile |

## Roadmap

1. **In-game smoke test.** Load the pack, start a career, and run a weekend.
   Answer the open questions in [CAPABILITIES §6](../../docs/CAPABILITIES.md#6-open-questions-to-verify-in-game).
2. **Calibrate lap times.** Tune `car_profile` and track `micro_sectors`
   against real 1991 pole times (e.g. Norisring ~50 s, Hockenheim ~2:15).
3. ✅ **Real tracks.** All 8 venues are generated from OpenStreetMap with
   `tools/osm_track.py` (specs in `track_specs/`). The status, confidence
   and open questions for each venue are in
   [docs/TRACKS.md](../../docs/TRACKS.md). The weak spots are the AVUS
   south turn and the Wunstorf perimeter road.
4. **Car images: polish.** All 22 cars are done (`tools/car_art.py`).
   Still to fix:
   - Leftover marks from the 1993 reference liveries, such as rear-wing logos.
   - The traced Audi body has less detail than the Pohlmann drawings.
5. **Logos and menu art.** ✅ Team and engine logos are done
   (`tools/logo_art.py`). Still to do:
   - Look for real 1991 logos for the 11 teams that use plain crests: AMG,
     Bigazzi, Linder, Isert, Climair, Valier, Vanicek, BAS, Eggenberger,
     Schübel and Ruch.
   - DTM-style menu and dashboard backgrounds.
6. **Sponsors.** Build a period sponsor pool and starting sponsors (cloned
   placeholders for now).
7. **Junior series.** Add the 1991 German F3 and Formel Opel Lotus
   (currently base-game placeholders).
8. **Economy.** Rescale salaries, costs and prize money from F1 scale to DTM
   scale.
9. **Follow-up seasons.** 1992 (Audi's twisted-crankshaft dispute and
   withdrawal), 1993 (Class 1 regulations).
