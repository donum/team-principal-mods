# DTM Eras and How They Map to Team Principal

German touring-car racing falls into six eras, each defined by its technical
rules. One season pack per year fits best, with shared car and rule
templates per era: an era base in [`bases/`](../bases/README.md) (era 4 is
`bases/dtm-era4`). The research data for every season is in
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

## Series logo by era (for in-game branding)

From 2000 to October 2024 the DTM kept one wordmark: heavy italic capitals
"DTM". Only its colours and finish changed. ADAC's Thomas Voss said it ran
"über 20 Jahre, nur ab und zu in der Farbe verändert". Years below come from
archived dtm.de / dtm.com pages (Wayback Machine) and the Commons files listed.

| Years | Look | Reference |
|---|---|---|
| 1984–85 (DPM), 1986–96 (DTM, ITC) | **Not verified.** No source found yet. Don't reuse a Masters-era logo here; use a plain "DTM" text title until a period source turns up. | — |
| 2000–2004 | Italic "DTM" in chrome / silver gradient on navy blue, with "DEUTSCHE TOURENWAGEN MASTERS" stacked beside it (dtm.de, April 2002). | Wayback dtm.de 2002 |
| 2005–2014 | Same chrome-on-navy italic "DTM", now without the long name: from 2005 "DTM" is a brand, not an abbreviation. Seen on dtm.com 2008, 2013 and 2014. | de.wikipedia `Dtm logo.png` (2006, "Das aktuelle DTM-Logo") |
| 2015–2018 | Flat version: solid italic "DTM", black on white or white on navy, no gradient (dtm.com from June 2015). | Commons `DTM Blue and White logo.svg` (used on the 2017 and 2018 season pages), `Deutsche Tourenwagen Masters (logo).png` |
| 2019–2022 | Same letters in neon yellow-green on navy blue (dtm.com 2019). | Commons `DTM logo.svg` |
| 2023 – Oct 2024 | ADAC takes over: same letters in yellow on black (ADAC colours). The 2024 season also used a "DTM 40" anniversary badge (yellow box, black text). | Commons `DTM logo 2023.svg`, `DTM 40 Years.jpg` |
| Oct 2024 – today (2025 season on) | New design by UnitedSenses (Munich): new italic capital typeface with notches cut into all three letters, yellow on a black rounded box. First shown at the Hockenheim finale 2024. | Commons `Deutsche Tourenwagen Masters - Logo 2025.png`, de.wikipedia `DTM 2024 logo.svg` |

Era mapping: era 1 and era 2 are open (see first row). Era 3 is chrome on
navy. Era 4 is chrome on navy for 2012–2014, then flat for 2015–2018.
Era 5 is neon on navy. Era 6 is neon (2021–22), then yellow on black (2023–24),
then the notched 2025 logo. Text-only logos count as public domain on Commons
(below the threshold of originality), which is why we can ship them.

## What changes between eras (game view)

**Era 1: Production and Group A**
- **Weekend:** one race per round until 1987. Two ~100 km heats per round from 1988, with a qualification race from 1989.
- **Pit stops:** none (sprint races, no refuelling).
- **Driver aids:** none, apart from ABS on some cars from 1991.
- **Tyres:** open tyre war (Yokohama, Pirelli, Dunlop, Michelin, Bridgestone).
- **Balance:** displacement-based weights plus success ballast. Not supported in the game: see the wish list.
- **Game fit:** works now (see `seasons/dtm-1991`), but heats and ballast are approximated.
- **Packs:** 1987, 1990, 1991 and 1992 share the 1991 template (`"template": "dtm-1991"`), which is the era's mother season. No engine sounds collected yet (vanilla).

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
- **Packs:** era base `bases/dtm-era3`, tuned on its mother season 2003; 2006 and 2010 build on it. No engine sounds collected yet (vanilla).

**Era 4: New DTM / Class One**
- **Weekend:** two races from 2015.
- **Driver aids:** DRS from 2013, which the game supports directly (`drs_policy`).
- **Tyres:** option and prime tyres from 2013, which map to compound rules.
- **Balance:** performance weights until 2017.
- **Points:** for qualifying from 2017.
- **Game fit:** very good. Two races a weekend become two game weeks (`races_per_round`), each with its own qualifying, as raced from 2017.
- **Packs:** era base `bases/dtm-era4`, mother season 2013 (sounds from 2012 and 2013 cars); 2012 and 2018 build on it.

**Era 5: Class One turbo**
- **Driver aids:** push-to-pass, modelled with the game's spec ERS (`ers_policy: spec`), and DRS.
- **Game fit:** very good.
- **Packs:** era base `bases/dtm-era5` on top of `bases/dtm-era4` (same chassis family, so it inherits tracks and tyres), tuned on its mother season 2020. Its own sound overlay replaces era 4's V8 sounds; none collected yet (vanilla).

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
matrix. Its Tracks section (`tools/track_inventory.py`) has one card per
venue: every race held there, the layouts by length, our generated tracks and
the rounds that use them, results files, the race-tracks layout history and the
photo research. Its "Build next" line names the most raced venues without a
game track. Modern venues such as Lausitzring, Oschersleben, Red Bull Ring,
Zandvoort, Brands Hatch and Assen still exist in OpenStreetMap, so the raceway
loop mode of `tools/osm_track.py` will cover most of them.
