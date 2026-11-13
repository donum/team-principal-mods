# American open-wheel cars, engines and push-to-pass, 1979 to 2026

Part of the IndyCar rules history (points, qualifying and race, pit stops
fuel and tyres, cars and engines). Covers CART (1979 to 2003), Champ Car
World Series (2004 to 2007) and IRL / IndyCar (1996 to 2026). The table
image is made with
`python -I tools/history_table.py docs/history/indycar-cars-engines.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Chassis | Engines | Overtaking aid | Quirks |
|---|---|---|---|---|
| 1979 to 1995 | Open market: teams buy from several makers (March, Lola, Penske, Reynard and others). | Turbo engines, the standard at Indianapolis since the late 1960s. 2.65 L turbo V8 in CART. | None. | 1994: the split between CART and Tony George begins. |
| 1996 | IRL: 1992 to 1995 CART chassis by Lola and Reynard. | Turbo V8 at 45 inHg boost. Buick "stock block" V6 at 55 inHg. | None. | Two engine types with different boost. |
| 1997 to 2002 | IRL: Dallara, G-Force, Riley & Scott (to 2000). | 4.0 L V8 without turbo, 10,000 rpm, about 650 hp. Oldsmobile (Chevrolet from 2002), Nissan/Infiniti. | None. | Cheaper "production-based" engines. |
| 2000 to 2005 | Panoz bought G-Force (2002). New makers need approval from 2003. | 3.5 L, then 3.0 L from the 2004 Indy 500 after crashes. Toyota and Honda come over from CART (2003). | None. | |
| 2004 to 2007 | Champ Car: Lola (2004 to 2006), Panoz DP01 (2007). | Ford-Cosworth 2.65 L turbo V8, about 750 hp, leased to all teams. | Push-to-pass from 2004: about 50 hp for a set time per race. | 2008: the IRL buys Champ Car's assets for 6 million USD and the series merge. |
| 2006 to 2011 | IndyCar: Dallara only from about 2008. | Honda alone. 3.5 L from 2007, 10,300 rpm, about 650 hp, 1,200 miles between rebuilds. | Push-to-pass from mid-2009: 10,500 rpm, about 690 hp. | A full engine lease cost 935,000 USD per car (2010). |
| 2012 to 2014 | Dallara DW12, safety cell price capped. | 2.2 L twin-turbo V6: Chevrolet, Honda (single turbo to 2013), Lotus (2012 only). 12,000 rpm. Boost 1.3 to 1.6 bar by track. | Push-to-pass: about 60 hp for 6 to 200 s per race by track (from Toronto 2012). | |
| 2015 to 2017 | DW12 with aero kits by Chevrolet and Honda. Frozen 2017. | Same. | Same. | Two makers, two looks. |
| 2018 to 2019 | DW12 with one universal aero kit for all. Front protection from Indy 2019. | Same. | Same. | |
| 2020 to 2023 | DW12 with aeroscreen. | Chevrolet and Honda. | Same. | |
| 2024 to 2026 | DW12. New car delayed from 2027 to 2028. | Same plus hybrid (about 60 hp, from Mid-Ohio 2024). | 150 to 200 s per race on road courses, at most 20 s per use. | The DW12 races for more than 14 seasons. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| One chassis for everyone | Partly | teams build their own, ratings can be set level |
| Buying a chassis from a maker | No | C4 |
| Engine makers | Yes | `engines.json` |
| Boost per track type | No |  |
| Push-to-pass as seconds per race | Partly | ERS spec stands in (B13) |
| Aero kits per maker | No | C9 |

## Sources

- Wikipedia, "IndyCar Series" (chassis and engines from 1996, boost,
  push-to-pass from 2009 and 2012, merger), "Champ Car World Series"
  (Lola, Panoz, Cosworth, 2008 sale), "Dallara DW12" (hybrid 2024, delay to
  2028), "Push-to-pass" (150 to 200 s, 20 s per use).
- Fact check: Autosport and Crash.net 2004 (Champ Car push-to-pass, 41.5
  to 44 inHg, about 50 hp), heraldnet and vindyarchives 2008 (6 million
  USD for Champ Car's assets, plus 2 million each to the two owners; one
  later report says about 10 million in total), "1968 Indianapolis 500" (first win
  for a turbo engine).
- Conflicts: push-to-pass power, 50 or 60 hp. Merger price, 6 or 10
  million USD depending on what is counted.

## Discord post

=== post | IndyCar cars and engines history | indycar-cars-engines
## IndyCar cars, engines and push-to-pass, 1979 to 2026

Part four and the last of the IndyCar rules history. The table is below. What stood out to me:

- **Open market until the 2000s:** teams bought chassis from Lola, Reynard, Dallara, G-Force and others. Since about 2008 one Dallara for everyone, the DW12 since 2012, racing into 2027.
- **Engines by era:** turbo V8, then a 4.0 L without turbo in the IRL (1997), 3.5 and 3.0 L, Honda alone (2006 to 2011), then a 2.2 L twin-turbo V6 from Chevrolet and Honda, with hybrid since 2024.
- **Two engine types with different boost** in 1996, a lot like DTM's weights per make.
- **Aero kits per maker** (2015 to 2017), then one kit for all.
- **Push-to-pass** as a time budget: 150 to 200 seconds per race, at most 20 seconds per use.
- **Two rival series** from 1996 to 2007, merged in 2008.

For the game: a spec chassis vs an open chassis market, engine makers per team, boost or power per track type, and push-to-pass as a budget in seconds. DTM's push-to-pass counted uses per race, so the setting should allow both.

The last table in the picture shows what the game can do today: yes, partly or no.

That's the IndyCar series. Mistakes? Tell me!
