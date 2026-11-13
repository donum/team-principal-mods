# MotoGP bikes, engines and tyres, 1949 to 2026

Part of the MotoGP rules history (bikes and tyres, race format and
points). The premier class: 500cc from 1949 to 2001, MotoGP from 2002. The
table image is made with
`python -I tools/history_table.py docs/history/motogp-bikes-tyres.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Engine | Weight and fuel | Tyres | Quirks |
|---|---|---|---|---|
| 1949 to 1968 | 500cc, four-strokes dominate. Unlimited cylinders and gears until 1968. | Not stated (?). | | MV Agusta wins riders' and constructors' titles in all four solo classes 1958 to 1960. |
| 1969 to 2001 | 500cc, at most four cylinders and six gears. Two-strokes take over by the mid 1970s. | Minimum weight raised from 115 kg to 130 kg in 1991. Fuel limit not stated (?). | Michelin radials from 1984. | Push starts end in 1987. Carbon brakes from 1988. Unleaded fuel 1998. |
| 2002 to 2006 | 990cc four-stroke, or 500cc two-stroke (gone by 2003). Any number of cylinders. | Minimum weight by cylinders: 135 kg (2 or 3) up to 155 kg (6). Fuel 24 L, 22 L from 2005. | Bridgestone arrives, Dunlop returns, tyre war. | Three-, four- and five-cylinder bikes race each other. |
| 2007 to 2011 | 800cc four-stroke. | Weight by cylinders, 21 L of fuel. | 2007: 31 tyres per rider a weekend, 2008: 40. Bridgestone alone from 2009, given out at random. | 2009: qualifying tyres, launch control and active suspension banned. Rookies may not join factory teams (2010 to 2012). |
| 2012 to 2015 | 1000cc, at most four cylinders, 81 mm bore. Claiming Rule Teams (2012, 2013): cheaper bikes with more engines and fuel, a factory can buy their engines. | 160 kg (2013), 158 kg (2015). Factory 20 L, Open class 24 L (2014). | Bridgestone. | Open class (2014, 2015): standard ECU software in return for more fuel and engines. |
| 2016 to 2026 | 1000cc, standard ECU and software for all. | 22 L for all. 40% sustainable fuel from 2024. | Michelin alone from 2016. | Concessions for weaker makes (testing, engines, wildcards), ranked A to D from 2024. Satellite teams get factory bikes from 2018. Front ride-height devices banned 2023. |
| 2027 | 850cc, 6 engines per rider (from 7). | 20 L, 100% sustainable fuel. | Pirelli alone. | All ride-height devices banned, aero tighter, every make starts in concession group B. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Motorcycles | No | the game models cars (N9) |
| Weight by number of cylinders | No | B2 |
| Engines per season with penalties | Yes | `seasonal_component_allocation_rule` |
| Fuel per race | Partly | `formula_fuel_tank` only with refuelling |
| Concessions for weaker makes | No | B2, D7 |
| Claiming rule and cheaper teams with more engines | No | C4 |
| One tyre maker, tyres per weekend | Yes | `tyre_suppliers.json`, `weekend_tyre_allocation` |
| Standard ECU, banned devices | Partly | `driver_aid_restrictions` |

## Sources

- Wikipedia, "Grand Prix motorcycle racing" (engine and cylinder rules,
  weights, fuel, tyre suppliers and allocations, ECU, CRT and Open class,
  2027 rules, 1969 cylinder and gear limits, 2018 satellite bikes).
- Bennetts BikeSocial (1969: six gears, four cylinders for 500s). Crash.net,
  Autosport and Roadracing World, May 2024 (2027 rules). Cycle News, 1991
  preview (253 lb to 286 lb).
- Crash.net and Autosport, 2024 MotoGP concession system (ranks A to D).
- NSR World (Honda NSR500 history) and Motor Sport, "The day MotoGP nearly
  died" (500cc minimum weight raised from 115 kg to 130 kg, 1991).
- FIM press release, April 2000, on Sportcal and Silverbullet (24 L for 2002
  and 2003, weights by cylinders). Crash.net, Roadracing World and the
  2005 season article (24 L kept for 2004, 22 L from 2005). The 26 L in the
  main article is not supported.
- Not confirmed, marked `(?)`: weights and fuel before 1991, fuel limit
  before 2002.

## Discord post

=== post | MotoGP bikes history | motogp-bikes-tyres
## MotoGP bikes, engines and tyres, 1949 to 2026

Two wheels for a change. The game is about cars, so this is mostly to show which rules carry over. The table is below. What stood out to me:

- **Weight by number of cylinders** (2002 to 2011): a two-cylinder bike could be 20 kg lighter than a six. A balancing rule like DTM's weights per make.
- **Engines per rider per season,** 7 today, 6 from 2027, with penalties for more.
- **Cheaper teams with more allowances:** Claiming Rule Teams (2012, 2013), the Open class (2014, 2015), and concessions for weaker makes since then.
- **Tyres:** a tyre war, then Bridgestone given out at random (2009), Michelin (2016), Pirelli (2027).
- **Fuel per race:** 24 L down to 20 L.

For the game: engine limits and one tyre maker already work. Weights by engine type and concessions for weaker makes are the same requests as for the car series.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
