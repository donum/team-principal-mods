# BTCC 1991: research dossier

The 34th British Touring Car Championship, and the first season of Super
Touring. 13 meetings and 15 races, all in the UK, from 1 April (Silverstone)
to 6 October (Silverstone). Will Hoy won the title (BMW M3, BMW Team
Listerine / Vic Lee Racing) with 155 points, ahead of John Cleland (132,
Vauxhall Cavalier) and Andy Rouse (115, Toyota Carina). BMW won the
manufacturers' title.

Source for everything here unless marked: en.wikipedia "1991 British Touring
Car Championship" (wikitext read 2026-11-13). The page carries a "sources
needed" tag, so all of it should be checked against a second source.

## Regulations
- **Class:** one class of Super Touring cars, grown from Group A's
  Division II (two-litre) cars. Group A cars could still enter, restricted
  to Super Touring speed (Middlehurst's and Leech's Sierra RS Cosworths,
  Brodie's Sapphire 4x4) [en.wiki].
- **Points:** not stated on the page. 20-15-12-10-8-6-4-3-2-1 per race
  matches about half the drivers exactly (Allam, Hahne, Leslie, Danner and
  most of the back markers) but not the top: Hoy +3, Cleland -3, Rouse -21,
  Palmer -13, Gravett -17. Dropped scores and fastest-lap points would
  explain most of it. Open.
- **Penalty:** Tim Harvey was disqualified at round 3 and docked 48 points for
  breaking the noise limit.
- **Void race:** round 5 (Silverstone) was stopped after 10 laps for heavy
  rain, not restarted, and paid no points.
- **Weights, tyres, race distances:** unknown.

## Weekend format
One race per meeting, except Donington National (round 8) and Brands Hatch
Indy (round 10), which had two. `entries.csv` "rounds" count meetings (1-13),
as the Wikipedia entry table does; `race_results.csv` has one column per race
(r1-r15).

## Teams
Manufacturer entries: BMW (Prodrive as "BMW Team Finance", Vic Lee Racing as
"BMW Team Listerine" and "BMW Team Labatt's"), Vauxhall (Dave Cook Racing as
"Vauxhall Sport"), Toyota (Andy Rouse as "Kaliber ICS Team Toyota"), Ford
(Trakstar, Robb Gravett only), Nissan (Janspeed, from round 2) and
Mitsubishi (John Maguire Racing, Lancer then Galant). The independents ran
mostly BMW M3s.

Left out of the pack (`gen.json` "skip"): Sean Walker Racing (one entry, did
not start), Moto-Build (Rover 216GTi, one start) and ACE Motorsport
(Peugeot 405, two entries, one start).

## Open questions
- Points scale, dropped scores, fastest-lap points.
- Minimum weight and tyre supplier(s). The pack uses 950 kg and Dunlop for
  every team as placeholders.
- Circuit lengths and race laps. Only Donington GP (4.023 km) and Brands
  Hatch Indy (1.929 km, our traced track) are filled in.
- Driver birth dates (none filled in yet, so every driver is aged 30).
- Engine names and outputs. `entries.csv` lists generic "2.0 L4" engines.
- Team colours are first guesses, not checked against photos.
- The Wikipedia entry table gives Kaliber ICS Team Toyota a Japanese flag and
  ACE Motorsport an Italian one; both look like the car maker's or a typo.
- Keith O'Dor is spelt "Kieth O'dor" in the Wikipedia tables.
