# DTM Eras and How They Map to Team Principal

German touring-car racing falls into six eras, each defined by its technical
rules. One season pack per year fits best, with shared car and rule
templates per era. The research data for every season is in
`seasons/<id>/research/`; browse it in the season archive
(`tools/build_browser.py`).

| Era | Years | Cars | Champions |
|---|---|---|---|
| **1. Production and Group A** | DPM 1984–85, DTM 1986–92 | BMW 635 / M3, Volvo 240T, Rover Vitesse, Ford Sierra, Mercedes 190E, Audi V8, Opel Omega | Strycek, Stureson, Thiim, van de Poele, Ludwig ×2, Ravaglia, Stuck, Biela |
| **2. Class 1** | DTM 1993–95, ITC 1995–96 | Alfa 155 V6 TI, Mercedes 190E / C-Class, Opel Calibra | Larini, Ludwig, Schneider, Reuter |
| — | 1997–99 | *no series* | |
| **3. Masters, V8 silhouettes** | 2000–2011 | Audi TT-R / A4, Mercedes CLK / C-Class, Opel Astra / Vectra (until 2005) | Schneider ×4, Aïello, Ekström ×2, Paffett, Scheider ×2, di Resta, Tomczyk |
| **4. New DTM / Class One** | 2012–2018 | Audi A5 / RS5, BMW M3 / M4, Mercedes C-Coupé / C63 | Spengler, Rockenfeller, Wittmann ×2, Wehrlein, Rast, Paffett |
| **5. Class One turbo** | 2019–2020 | 2.0 turbo four-cylinder: Audi RS5, BMW M4, Aston Martin Vantage (2019) | Rast ×2 |
| **6. GT3** | 2021–today | Customer GT3: Audi, BMW, Mercedes-AMG, Ferrari, Lamborghini, Porsche, McLaren, Ford Mustang… | Götz, van der Linde, Preining ×2, Bortolotti, Güven |

## What changes between eras (game view)

**Era 1: Production and Group A**
- **Weekend:** one race per round until 1987. Two ~100 km heats per round from 1988, with a qualification race from 1989.
- **Pit stops:** none (sprint races, no refuelling).
- **Driver aids:** none, apart from ABS on some cars from 1991.
- **Tyres:** open tyre war (Yokohama, Pirelli, Dunlop, Michelin, Bridgestone).
- **Balance:** displacement-based weights plus success ballast. Not supported in the game: see the wish list.
- **Game fit:** works now (see `seasons/dtm-1991`), but heats and ballast are approximated.

**Era 2: Class 1**
- **Weekend:** two heats.
- **Pit stops:** none mandated, as far as the sources show.
- **Cars:** 4WD (Alfa, Opel), active electronics, traction control and ABS allowed.
- **Game fit:** works; use the `driver_aid_restrictions` options to allow aids.

**Era 3: Masters, V8 silhouettes**
- **Weekend:** from 2001, a qualifying race plus a main race. From 2003, single ~60-minute races.
- **Pit stops:** mandatory from 2001, with a tyre change. Refuelling in 2003.
- **Driver aids:** none.
- **Balance:** weight rules by car generation (year-old cars), success ballast in some years.
- **Tyres:** Dunlop, then Hankook from 2011.
- **Game fit:** good. Mandatory stops, refuelling and compound rules exist in `regulations.json`.

**Era 4: New DTM / Class One**
- **Weekend:** two races from 2015.
- **Driver aids:** DRS from 2013, which the game supports directly (`drs_policy`).
- **Tyres:** option and prime tyres from 2013, which map to compound rules.
- **Balance:** performance weights until 2017.
- **Points:** for qualifying from 2017.
- **Game fit:** very good.

**Era 5: Class One turbo**
- **Driver aids:** push-to-pass, which could be modelled with the game's spec ERS (`ers_policy: spec`), and DRS.
- **Game fit:** very good.

**Era 6: GT3**
- **Weekend:** two races per weekend.
- **Race length:** time-limited (55–60 minutes + 1 lap).
- **Pit stops:** mandatory pit windows, two stops on Sundays in 2025.
- **Tyres:** a tyre-set pool.
- **Balance:** balance of performance plus success ballast (25/15/5 kg in 2022, 20/10/5 kg from 2023).
- **Points:** 3-2-1 for qualifying.
- **Entries:** many makes, customer teams on GT3 cars.
- **Game fit:**
  - Time-limited races need laps worked out from typical lap times.
  - Balance of performance and ballast aren't supported (wish list items B1 and B2).
  - Customer cars fit wish list item C4.

## Suggested build order

1. **1991**: playable now.
2. **1990 and 1992**: same cars and venues as 1991, so the car models and tracks mostly carry over.
3. **One modern showcase:**
   - **2013 (era 4):** DRS and option tyres show off the game's modern features.
   - **2023 (era 6):** many makes, pit windows.
4. **Fill in the remaining seasons era by era**, reusing that era's car models, rule templates and tracks.

Tracks needed across all eras are listed in the season archive's venue
matrix. Modern venues such as Lausitzring, Oschersleben, Red Bull Ring,
Zandvoort, Brands Hatch and Assen still exist in OpenStreetMap, so the raceway
loop mode of `tools/osm_track.py` will cover most of them.
