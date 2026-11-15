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

## Cars and race notes from TCR (2026-11-15)
From the 1991 Cars page (http://touringcarracing.net/Pages/1991%20Cars.html)
and the 1991 race pages (`/Races/1991%20<venue>.html`). The cars page
has spec boxes for five BTCC cars only; Ford, Mitsubishi and the
privateer cars have none. The 1991 BTCC Class page is only the points
table (already used above).
- **BMW M3, Prodrive (Mobil BMW Team):** BMW S14 inline-4, bore and stroke
  93.4 x 72.9 mm, 1998 cc, two overhead cams, four valves per cylinder,
  about 270 hp, BMW Motorsport six-speed gearbox, 1050 kg, discs all round,
  Pirelli tyres.
- **BMW M3, Vic Lee Motorsport:** same, with a Eurotech-BMW S14 engine, no
  power figure, Yokohama tyres.
- **Nissan Primera ZX, Janspeed Engineering:** Nissan inline-4, 2000 cc,
  two cams, four valves, 265 hp, Jack Knight six-speed gearbox, 950 kg,
  Dunlop.
- **Toyota Carina II, "Rouse Sport":** Toyota inline-4, 1998 cc, two cams,
  four valves, no power figure, Xtrac six-speed gearbox, 950 kg, Yokohama.
- **Vauxhall Cavalier GSi, Dave Cook Racing Services (Swindon):** Opel
  inline-4, 2000 cc, two cams, four valves, no power figure, Xtrac six-speed
  gearbox, 950 kg, Dunlop. TCR's entrant column reads "Dave Cook Racing
  Services / Vauxhall Dealer Sport"; Mitsubishi's reads "John Maguire
  Racing / Mitsubishi Motors with Firestone".
- **Season summary** (1991 BTCC page): works or semi-works teams were Ford
  (Trakstar, Gravett, a non-turbo four-door Sierra), BMW (Prodrive two
  cars, Vic Lee four), Toyota (Rouse, two cars), Vauxhall (two or three
  cars), Nissan (one or two Janspeed cars) and Mitsubishi (one car, Hales).
  Best privateers: Sytner (M3) and Middlehurst (non-turbo three-door
  Sierra). The Toyota was new for 1991; the M3 and Cavalier had raced in
  1990. Prodrive is called "semi works".
- **Race notes** (facts not in the tables):
  - Round 1 Silverstone: Palmer hit Rouse at the start; Soper pitted with
    gearbox trouble.
  - Round 3 Donington: Hoy pitted on lap 2 with the cockpit full of smoke
    and a small fire under the bonnet, after the noise changes to the
    exhaust. Bellm stopped just before the line so as not to be classified
    and face the noise check.
  - Round 5 Silverstone (void): only Sytner, Ayles and Middlehurst started
    on wet tyres; Cleland was "winner" on the count-back despite a big off
    on the last lap.
  - Round 6 Brands Hatch Indy: 17 starters; Sugden hit Hoy's left rear to
    take the lead; Gravett stalled at the start.
  - Round 8 Donington double header: Cleland on pole on new Dunlop radials.
    Race 1: Ayles and Allam tangled. Race 2: red flag after 7 laps when
    Whale's oil at McLeans put Whale, Hales, Allam, Cleland and Bellm off;
    restarted over 12 laps, result on aggregate. Bellm raced Yokohamas meant
    for Hoy, who was out with gearbox and over-rev trouble.
  - Round 9 Oulton Park: Ayles broke his suspension after a jump over the
    grass; Bristow had a big off on the last lap.
  - Round 10 Brands Hatch double header: Ayles hit Sytner on the warm-up
    lap and was out of race 2.
  - Round 12 Thruxton: the first six on the grid within 0.2 s. Palmer hit
    Hoy; Hoy and Cleland then collided at the Complex, and Hoy retired.
    Harvey broke down on the last lap.
  - Round 13 Silverstone: wet practice, dry race. Wilson rolled his
    Vauxhall after a nudge from Hall. Hoy fifth and champion. TCR heads
    this page "Silverstone National Circuit"; `calendar.csv` has the GP
    circuit (no AS scan for this round). The season review's commentary
    names the GP corners, so TCR's heading looks wrong (open questions).
  - Round 8 race 2: 7 laps plus the 12-lap restart give the 19 laps in
    `calendar.csv`.

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

## From the official season review (2026-11-15)
"1991 BTCC (British Touring Car Championship) - Full Season Review", 88 min,
a BHP Sport production "© 1991" (later sold on DVD by Duke), Rumble copy in
`Videos/yt/BTCC/1991/Singles`. Murray Walker commentates most races, Frank
Sytner co-commentates Oulton Park. Transcript (private):
`private/tv_coverage/transcripts/btcc/1991/Singles__1991 BTCC ... Full Season Review.txt`.
Times are video times [Review h:mm:ss].
- **Format:** in two seasons the RAC MSA cut the championship from four
  classes to one [0:01:50]. 1990 was the last year of the 500 hp Sierra
  Cosworths [0:01:22]. The caption card: 2000 cc / 8,500 rpm, unleaded fuel,
  six slick tyres per meeting [0:01:55].
- **Power:** Rouse's Carina "that 285 horsepower Toyota" [0:55:50] (the first
  Toyota figure we have; TCR has none).
- **Drive side:** Soper's, Palmer's and Harvey's BMWs were left-hand drive
  [0:25:31, 0:31:21, 0:45:47, 0:53:04]; Rouse's Toyota right-hand drive
  [0:53:09].
- **Engines:** Gravett's Sapphire ran 1990's turbo engine with the turbo
  taken off, so the engine was all new [0:58:10]. Middlehurst's Sierra "looks
  like a turbocharged Cosworth" but has a two-litre atmospheric engine built
  by Graham Goode [1:17:20].
- **Noise (round 3):** limit 110 dB; Vic Lee's cars had side exhausts and a
  high-pitched resonance; the team aimed for 106 dB with a deflector plate and
  extra baffling. Failing a check after the race could cost all points so
  far [0:14:49-0:16:50]. Hoy's practice times were disallowed, he started
  from the back and retired on lap 2 with smoke and a small fire [0:16:59].
- **Crowds:** over 20,000 at the Silverstone opener [0:03:03]; Grand Prix day
  at Silverstone (round 7) had the biggest crowd of the season [0:23:16].
- **Round 1:** Sytner had engine failure in qualifying and did not race
  [0:03:28]. Palmer hit Rouse at Becketts on lap 1; Rouse rejoined almost
  last (19th) and finished fourth [0:04:19, 0:09:12]. Hoy fastest lap
  1:47.5, 91.7 mph, and won by about 10 s [0:08:08]. Soper lived in Monaco
  [0:05:09]. Rouse on learning front-wheel drive: the reaction to a slide is
  the opposite of a rear-wheel drive car [0:10:08].
- **Round 2 Snetterton:** Palmer hit Lindgren at Russell and both retired
  [0:12:08]. The Vic Lee BMWs were on Yokohama, the Vauxhalls on Dunlop, and
  the Vauxhalls' tyres faded [0:13:58]; Vic Lee one-two, Hoy from Bellm.
- **Round 5 Silverstone (void):** most of the field gambled on slicks;
  Sytner on wet tyres was the "moral victor" [0:21:45].
- **Round 6 Brands Hatch:** Hoy carried a rear-facing camera; Sugden started
  from pole and passed Hoy with light contact at Surtees on lap 15 [0:22:45].
- **Round 7 Silverstone GP:** Sytner hit Ayles' Toyota and spun it; Ayles
  then retired with a split radiator [0:30:09, 0:30:57]. Mackenzie's Peugeot
  went off [0:27:08].
- **Round 8 Donington double header:** two races of 25 laps with only a
  10-minute break (TCR says 15 minutes) [0:32:48, 0:35:29]. Hoy missed a gear
  and blew his engine [0:32:58]. Rouse's first Toyota win, fastest lap
  92.2 mph [0:35:04]. Race 2 had 15 starters (Ayles, Hoy, Sytner out)
  [0:36:52]; Hales' first drive in the new Galant [0:42:40]. After the red
  flag, 10 cars restarted, Cleland among the three from the pit lane, result
  on aggregate [0:44:51]. Soper retired with a fuel pump problem that
  damaged the engine [0:48:08]. Gravett third, his best result so far
  [0:49:25]. Prodrive's boss is Dave Richards [0:43:49].
- **Round 9 Oulton Park:** Hoy raced with flu [0:50:32]. Ayles fastest lap
  96.5 mph [0:51:38].
- **Round 10 Brands Hatch:** Rouse had to avoid Forrest's BMW broadside
  across the track, which let Hoy by [0:55:23].
- **Privateers:** O'Dor's Janspeed Primera became a top-ten runner, with
  Bailey joining as team-mate [0:58:37]. Hales drove an "overweight" Starion
  in 1990, the Lancer in the first half of 1991 and the larger Galant in the
  second half [0:58:51].
- **Round 12 Thruxton:** Palmer's first pole, Soper alongside; Hahne replaced
  Bristow; the first six within 0.2 s [1:00:56]. Palmer hit Hoy and spun him;
  later Hoy and Cleland touched twice, the first time Hoy's front spoiler
  rubbed the left front tyre [1:05:51, 1:07:48]. Cleland finished ninth
  [1:11:47]. Hoy went to the final 17 points ahead [1:12:28]. Vic Lee was
  Hoy's team boss [1:04:09].
- **Round 13 Silverstone:** front row Rouse and Cleland, Hoy and Harvey row
  two [1:13:23]. Palmer held back to protect Hoy ("BMW teamwork") [1:23:20].
  Hall (#18 BMW) nudged Jeff Wilson's Vauxhall "Belmont" into a double roll;
  Wilson walked away [1:24:46, 1:25:01]. Leslie drove Sytner's black #2 BMW
  [1:23:29]. Sugden had been in the BMW Junior team in 1990 [1:20:14].
- **Season:** Hoy, Cleland, Rouse and Soper won three races each, Harvey
  the last one [1:27:39].
- **Colours named on air:** Harvey's car "dark blue" [1:08:45], Rouse's
  Toyota "dark blue and white" [1:09:24], Gravett's Ford "red and yellow"
  [1:10:39], Middlehurst's Sierra "grey and blue" [1:16:42] (it looks white
  on screen), Bellm's BMW "light blue" [0:39:30].
- **Ages:** Middlehurst 28, eleven years of racing [1:16:42, 1:18:52].

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
- Engine outputs for Vauxhall and Ford (Toyota: 285 hp on air in the
  season review; BMW and Cavalier "about 280" and "some 250" in the TV
  coverage, about 270 at TCR).
- Round 13 layout: Silverstone GP in `calendar.csv`, "National" at TCR. The
  season review names Copse, Maggotts, Becketts, Chapel, Hangar Straight,
  Stowe, Vale, Club, Abbey, Bridge, Priory, Brooklands and Luffield
  [1:13:40-1:15:34], which is the GP circuit.
- The Silverstone finale (round 13) has no AS scan; its result is from TCN.
- Team names: the pack keeps the en.wiki names; the period names are above.
- Team colours are first guesses, not checked against photos.
- The Wikipedia entry table gives Kaliber ICS Team Toyota a Japanese flag and
  ACE Motorsport an Italian one; both look like the car maker's or a typo.
