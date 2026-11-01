# 1995 DTM + International Touring Car Series (ITC): research dossier

## Overview
- Two parallel championships with the same cars, teams, drivers and rules: **DTM** (7 German weekends) and the FIA **International Touring Car Series** (5 weekends abroad). Points were kept separately.
- 12 weekends × 2 heats = 24 races. The AVUS heat 2 was annulled, so 23 races counted.
- DTM rounds: 1 Hockenheim, 2 AVUS, 5 Norisring, 7 Diepholz, 9 Nürburgring, 10 Alemannenring, 12 Hockenheim.
- ITC rounds: 3 Mugello, 4 Helsinki, 6 Donington, 8 Estoril, 11 Magny-Cours.
- Champion of both: **Bernd Schneider** (D2 AMG-Mercedes C-Klasse), with 138 DTM points and 155 ITC points. Mercedes-Benz won both manufacturer standings.
- This was the last season under the DTM name until 2000.

## Class 1 regulations (FIA Class 1, 1993–96)
- Engine: at most 6 cylinders, 2.5 litres, 4 valves per cylinder, naturally aspirated. The engine had to be derived from a production engine of the same manufacturer.
- Permitted: four-wheel drive, traction control, ABS and electronically controlled differentials. Aero was free below the wheel centreline. From 1995 the suspension could be purpose-built (Automobile Year 1995/96, via en.wiki "Class 1 Touring Cars").
- 1995 changes (ja.wiki "クラス1", citing Racing On No. 485):
  - 12,000 rpm rev limit
  - Minimum weight 1,020 kg for 2WD and 1,060 kg for 4WD (1993: 1,000 / 1,040 kg)
  - Semi-automatic gearboxes with up to 6 speeds allowed
  - Free suspension layout
  - Flat bottom allowed
  - Rear tank limited to 70 L
- Drivetrains:
  - Alfa Romeo 155 V6 TI: 4WD
  - Opel Calibra V6 4x4: 4WD, with a Cosworth-built V6 ("Phase 3" engine)
  - AMG-Mercedes C-Klasse: rear-wheel drive. de.wiki gives about 375 kW for 1995.
- Electronics: semi-automatic gearboxes, active or adjustable suspension, and Mercedes' movable ballast "weight shuttle" (motorsportretro; de.wiki ITC).

## Points and format
- Points per heat for positions 1–10: 20-15-12-10-8-6-4-3-2-1, in both DTM and ITC.
- Manufacturer points went only to the best-placed car of each make.
- Weekend: qualifying, then two heats of about 100 km on the same day (motorsportretro: "two races on Sundays, with a 30-minute gap"; crews had 22 minutes to repair cars between heats).
- Heat 2 grid: in 1996 it was the heat 1 finishing order (en.wiki round tables). This is assumed for 1995 but not verified.
- **Mandatory pit stops:** I found no source saying they existed. Heats were about 100 km sprints and the race reports mention no compulsory stops. This is unverified.
- **Qualifying race:** not documented for 1995. The `qual_race` column is left empty.

## Calendar notes
- For the first time, the season did not open at Zolder; Hockenheim hosted the opener on 23 April, about three weeks later than usual.
- Planned ITC rounds that were cancelled:
  - Barcelona (Circuit de Catalunya), planned as the final, clashed with the motorcycle GP.
  - Spa: the circuit owner, Ecclestone, said there was too little time to promote it.
- There were no overseas rounds in 1995. Interlagos and Suzuka came in 1996.
- Lap counts in calendar.csv are derived from the de.wiki distances divided by the circuit length. Every lap count is a whole number, which supports the lengths used.

## Storylines
- BMW privateers had left, so the field was three works-backed makes: Mercedes, Alfa Romeo and Opel.
- Reigning champion Klaus Ludwig moved from AMG to Keke Rosberg's new Opel team (Team Rosberg, Neustadt/Weinstraße). Ludwig won both finale heats at Hockenheim.
- Mercedes used the late start to catch up and gave the newest V6 C-Klasse to five of its six works drivers at the start.
- Alfa Romeo lost development time through testing crashes, including a heavy one for Larini. Larini's and Nannini's new cars started the season untested.
- Opel kept swapping its new cars between drivers after crash damage, and Dalmas and Amorim were sidelined at times.
- Schneider won 11 heats. Other winners:
  - Thiim: 3
  - Danner: 2
  - Bartels: 2 (double at Diepholz)
  - Ludwig: 2
  - Franchitti, Larini, Magnussen: 1 each
- Keke Rosberg retired after the DTM finale.
- Young drivers who later reached F1 or Indy: Fisichella (Alfa Corse 2), Franchitti and Magnussen.

## Team managers / bosses (where documented)
| Role | Person | Source |
|---|---|---|
| Opel motorsport chief 1995 | Walter Treser | de.wiki Opel Calibra V6 4x4 |
| Team Rosberg owner | Keke Rosberg | |
| Joest Racing owner | Reinhold Joest | |
| Zakspeed | founder Erich Zakowski; son Peter Zakowski led international programmes | |
| Persson Motorsport team boss | Ingmar Persson | |
| Ruch Motorsport | owner-driver Gerd Ruch | |

Mercedes (Norbert Haug) and Alfa Corse management are not confirmed in the sources I fetched.

## Sources
- https://de.wikipedia.org/wiki/Deutsche_Tourenwagen-Meisterschaft_1995 (raw wikitext; main source for entries, calendar, distances and both standings tables)
- https://en.wikipedia.org/wiki/1995_Deutsche_Tourenwagen_Meisterschaft (entries, schedule, standings cross-check)
- https://de.wikipedia.org/wiki/International_Touring_Car_Championship (history, format)
- https://en.wikipedia.org/wiki/Class_1_Touring_Cars and https://ja.wikipedia.org/wiki/クラス1 (regulations, weights)
- https://de.wikipedia.org/wiki/Opel_Calibra_V6_4×4, https://de.wikipedia.org/wiki/DTM_AMG_Mercedes_C-Klasse, plus the de.wiki pages Team_Rosberg, Joest_Racing, Zakspeed and Persson_Motorsport (team bases and bosses)
- https://www.motorsportretro.com/2014/02/why-class-1-dtm-of-1995-and-1996-was-too-good-to-be-true/ (format, electronics)
- https://web.archive.org/web/20191118065046/https://www.dtm.com/de/historie/die-dtm-saison-1995 (summary only)
- Wikidata SPARQL for birth dates
- touringcarracing.net covers DTM only up to 1993 (no 1995 page). touringcars.net is behind a Cloudflare challenge, so I did not use it.

## Unverified / gaps
- **Tyre suppliers** per team: not found. The `tyres` column is empty.
- **Laps per heat** for all rounds: derived, not quoted.
- **Helsinki 1995 length** (3.41 km / 30 laps): assumed, because the 1996 layout is quoted as 3.180 km.
- **AVUS:** length 2.640 km is derived. The reason heat 2 was annulled is unknown.
- **Final round date:** 15 Oct (en.wiki; a Sunday) vs 16 Oct (de.wiki).
- **Hockenheim round 1 pole:** Franchitti or Larini.
- **Entry conflicts:**
  - Alén's rounds: 1 and 4, or 1 and 6.
  - Giovanardi's rounds: 5, or 5 and 12.
  - Entrant of Tarquini and Couceiro: Schübel or Alfa Corse 2.
- **Mandatory pit stops** and any **qualifying-race** format.
- **Missing team bases:** Alfa Corse, Schübel, Euroteam, Persson and Ruch.
- **Engine type designations:** Mercedes M106-based V6, Alfa "690" V6 and Opel/Cosworth KF are from ja.wiki only.
- **1995 weights** (1,020/1,060 kg) have a single source (ja.wiki / Racing On).
