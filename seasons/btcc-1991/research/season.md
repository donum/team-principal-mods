# BTCC 1991: research dossier

The 34th British Touring Car Championship, and the first season of Super
Touring. 13 meetings and 15 races, all in the UK, from 1 April (Silverstone)
to 6 October (Silverstone). Will Hoy won the title (BMW M3, BMW Team
Listerine / Vic Lee Racing) with 155 points, ahead of John Cleland (132,
Vauxhall Cavalier) and Andy Rouse (115, Toyota Carina). BMW won the
manufacturers' title.

Sources (checked 2026-11-15):
- **en.wiki:** "1991 British Touring Car Championship" (wikitext read
  2026-11-13), the first source; tagged "sources needed".
- **AS:** the period Autosport results boxes, scanned on 1990sbtcc.com
  (https://1990sbtcc.com/as9101/ to /as9112/, linked from
  https://1990sbtcc.com/1991-race-reports/), meetings 1-12. The race
  archive https://1990sbtcc.com/race-archive/ has the qualifying and race
  tables per round.
- **TCN:** touringcars.net database
  (https://www.touringcars.net/database/season.php?series=BTCC&year=1991,
  race.php?id=759 to 793, standings.php).
- **TCR:** touringcarracing.net
  (http://touringcarracing.net/Pages/1991%20BTCC.html, its points table and
  1991 Cars page).
- **Regs:** https://1990sbtcc.com/btcc-regulations/ and the Motor Sport
  preview, March 1991
  (https://www.motorsportmagazine.com/archive/article/march-1991/25/british-touring-car-championship-3/).

Checked against AS and TCN: every date, venue, layout, winner, pole and
fastest lap in `calendar.csv`, every finishing position in
`race_results.csv` (all 15 races; one fix, Baird at Snetterton) and every
total in `standings.csv`.

## Regulations
- **Class:** one class of Super Touring cars, grown from Group A's
  Division II (two-litre) cars. Group A cars could still enter, restricted
  to Super Touring speed (Middlehurst's and Leech's Sierra RS Cosworths,
  Brodie's Sapphire 4x4) [en.wiki].
- **Points:** 24-18-12-10-8-6-4-3-2-1 per race. The races at the two
  double-header meetings (Donington National, Brands Hatch Indy in August)
  paid half points to the top eight (12-9-6-5-4-3-2-1). No dropped scores,
  no points for pole or fastest lap [Regs, Motor Sport, TCR table]. With
  round 5 void and Harvey's -48 this gives all 41 totals in
  `standings.csv` exactly (checked by script). Manufacturers: 10-9-8-...-1
  for each make's best car per race, full points at the double headers:
  BMW 134, Vauxhall 116, Toyota 111, Ford 102, Nissan 53, Mitsubishi 45
  [TCR]. The game pays the same points in every race, so the double-header
  races pay full points in the pack (wishlist A1).
- **Penalty:** Tim Harvey was disqualified at round 3 and docked 48 points for
  breaking the noise limit.
- **Void race:** round 5 (Silverstone) was stopped after 10 laps for heavy
  rain, not restarted, and paid no points.
- **Weights:** 950 kg for front-wheel drive cars, 1050 kg for rear- and
  four-wheel drive cars (BMW M3, Ford Sierra and Sapphire) [Regs; TCR cars
  page]. Rev limit 8,500 rpm, six slicks per meeting [Regs; AS round 1].
- **Tyres** (AS tyre column, legend in AS round 10): Yokohama (Vic Lee's
  BMWs, Toyota, Trakstar, Graham Goode, Pyramid, Team Sweden, Judge, R&D),
  Pirelli (Prodrive, Techspeed, Drambuie), Dunlop (Vauxhall, Nissan, HWR,
  Mackenzie), Firestone (Mitsubishi). Motor Sport, Nov 1991, agrees for Vic
  Lee, Vauxhall and Prodrive. In `entries.csv` "tyres".
- **Race distances:** laps and lap lengths per race in `calendar.csv`, from
  the AS headers (miles) and TCN.
- **Engines** [TCR cars page]: BMW M3 S14 2.0 inline-4 (1998 cc, about
  270 hp; Vic Lee's built by Eurotech), Nissan 2.0 L4 265 hp; Toyota,
  Vauxhall (Opel unit) and Ford 2.0 L4 without a figure. Only Leech's RS500
  was a turbo; Middlehurst's Sierra and Gravett's Sapphire were 2.0
  non-turbo [AS round 1].

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

Team names are the 1991 ones from the Autosport "Entrant/Sponsor" column
[AS], since 2026-11-15. Where the entrant is the runner's initials or a
person (VLM, Prodrive, Maguire, Forrest, Leech, Janspeed) the pack uses the
sponsor name; where it is a team name it keeps that. As printed: "VLM/Team
Securicor + Listerine" (Hoy, Bellm; Hoy's car in Securicor Omega Express
colours), "VLM/Team Labatt's", "Prodrive/The Mobil BMW Team" (later
"Prodrive/Mobil BMW Team"), "Vauxhall Dealersport", "Kaliber ICS Team
Toyota", "Shell Team Trakstar Ford", "Castrol Racing with Janspeed" (later
"Janspeed/Nissan Racing with Castrol"; the pack uses the later name),
"Maguire/Mitsubishi Motors+Firestone", "Pyramid Motorsport/Mobil", "BMW
Team Sweden" (later "BMW Dealer Team Sweden"), "Techspeed/Midland Auto
Trader(+Mobil)", "Forrest/Drambuie+Lazerprinz", "Leech/Judge
Developments+Partservice", "HWR Motorsport/Bristol Street Motors",
"BRR/100+ Wheels + British Gas Resource" (Neal), "Graham Goode Racing",
"R&D Motorsport". Cars: Vauxhall Cavalier GSi, Nissan Primera ZX then eZX,
Mitsubishi Lancer GTi then Galant. The en.wiki names were "BMW Team
Listerine", "BMW Team Labatt's", "BMW Team Finance", "Vauxhall Sport",
"Trakstar Motorsport", "Nissan Janspeed Racing", "John Maguire Racing",
"Auto Trader Techspeed Team", "Drambuie Racing", "Judge Developments".

Left out of the pack (`gen.json` "skip"): Sean Walker Racing (one entry, did
not start), Moto-Build (Rover 216GTi, one start) and Andrew Mackenzie Racing
(Peugeot 405, two entries, one start; en.wiki has it as ACE Motorsport).

## From the TV coverage (transcripts, 2026-11-15)
The 18 broadcasts in the video archive (`Videos/yt/BTCC/1991`) were
transcribed (private, `private/tv_coverage/transcripts/btcc/1991`). Facts
read from them, with video and time:
- **Rules:** two-litre engines, at most six cylinders, 8,500 rpm limit,
  unleaded fuel [Round 1 race archive 0:01:00]; six tyres per car for
  practice and race [Will Butler Round 4 Pt 1 0:00:11]; exhaust noise under
  110 dB [Round 3 race archive 0:00:28].
- **Noise at Donington (round 3):** four cars started from the back with a
  ten-second penalty for breaking the noise rule, Harvey last [Round 3 race
  archive 0:06:42, 0:16:15]; Bellm, Harvey and Bristow faced a noise check
  after the race [0:18:36]. Harvey's 48-point penalty followed.
- **Power:** "about 280 horsepower" for the BMW M3 and the Cavalier [Round 1
  race archive 0:04:30, 0:13:17], "some 250 horsepower" in a later report
  [Will Butler Round 4 Pt 1 0:01:54]. The front-wheel drive Vauxhalls had
  "a slight weight advantage" [Snetterton 14 Apr 1991 0:09:01].
- **Ages** agree with the birth dates in `entries.csv`: Ayles 26 [Round 3
  0:09:36], Middlehurst 28 [Round 1 Pt 1 0:10:08; pt4 Round 15 0:04:23],
  Allam 36 and Cleland 38 [Snetterton 14 Apr 1991 0:09:45]. Hometowns:
  Ayles Maidstone, Middlehurst St Helens, Cleland Peebles.
- **Colours:** Middlehurst's Sierra was grey and blue [pt4 Round 15 0:04:23].

## Corrections from the second sources (2026-11-15)
- Points scale (above), weights, tyres, race laps and lap lengths.
- Nick Baird did not start at Snetterton (not in AS or TCN; en.wiki: Ret).
- At Snetterton Gary Ayles was the driver disqualified (missing wiper arm);
  the chequered flag was waved early [AS].
- Spellings: Kieth O'Dor (the period spelling, AS and 1990sbtcc.com; en.wiki
  is right), Alastair Fenwick and Alastair Lyall, Andrew Mackenzie.
- Brands Hatch Indy was about 1.936 km in 1991, not 1.929 km.
- Birth dates from racingsportscars.com (driver pages); O'Dor's from
  en.wiki only.

## Per-race results
`results/NN-<track>-race.csv` and `-qualifying.csv` for all 15 races, for
`tools/simulate.py`: order, laps, times and best laps from touringcars.net
(race.php and qualifying.php pages), entrant, car and tyres as printed in the
Autosport tables (race 15 from touringcars.net only; races 9 and 12 take
the entrants and tyres of races 8 and 11). Checked: finishing order equals
`race_results.csv` in every race, pole equals the grid-1 driver, race 7
spot-checked against the Autosport table. Odd tyre codes are kept as
printed (Palmer "Y" at round 1, Allam "P" at round 7, "A" probably Avon).

## Open questions
- Birth dates still missing: Gravett, Baird, Forrest, Leech, Llewellyn,
  Lindgren, Andersson (they are aged 30 in the pack).
- Engine outputs for Toyota, Vauxhall and Ford.
- The Silverstone finale (round 13) has no AS scan; its result is from TCN.
- Team names: the pack keeps the en.wiki names; the period names are above.
- Team colours are first guesses, not checked against photos.
- The Wikipedia entry table gives Kaliber ICS Team Toyota a Japanese flag and
  ACE Motorsport an Italian one; both look like the car maker's or a typo.
