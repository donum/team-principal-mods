# Sportscar classes and balance of performance, 1953 to 2026

Part of the endurance rules history (classes and BoP, drivers and pit
stops, race format and points). Covers the World Sportscar Championship
(1953 to 1992), Le Mans, and the FIA WEC (2012 to 2026). The table image
is made with
`python -I tools/history_table.py docs/history/wec-classes-bop.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Top class | Other classes | How cars are balanced | Quirks |
|---|---|---|---|---|
| 1953 to 1961 | Sports cars. | GT. Both split by engine size. | Engine size classes. From 1958 sports cars limited to 3 L. | World Sportscar Championship for makes. Mille Miglia (to 1957), Carrera Panamericana (1953, 1954) and Targa Florio (from 1955) count. |
| 1962 to 1971 | GT title, with a sports car cup (1962) and a prototype trophy (1963 to 1965) next to it. | GT under 1 L, under 2 L and over 2 L. From 1968: 5 L sports cars and 3 L prototypes. | Engine size. | The title name changes almost every few years. |
| 1972 to 1981 | 3.0 L sports cars (to 1977), then Group 5 "special production" cars. | Group 4 GT. | Engine size. | 1975: Le Mans fuel rule, at least 20 laps between fuel stops. 1976: Le Mans adds its own GTP class (closed cars, at least 850 kg). |
| 1982 to 1990 | Group C: closed prototypes, at least 800 kg, 100 L tank, five fuel stops per 1000 km. | Group C Junior / C2 (from 1983): 700 kg, 55 L tank. GT (1983 to 1984). | Fuel: about 600 L per 1000 km for C1, about 330 L for C2. Any engine. | A fuel formula instead of an engine formula. 1990: chicanes on the Mulsanne straight after 407 km/h in 1988. |
| 1991 to 1992 | 3.5 L engines without turbo, 750 kg. | Older Group C cars, held back by weight and fuel (1991). Le Mans 1992 added classes for older and small cars. | Weight and fuel for the old cars. | The championship ends, 1993 is cancelled before the first race. |
| 1994 to 2010 | Le Mans prototypes (LMP), with GT1 cars racing for the win in the 1990s. | GT1 and GT2 (to 1998), GTS and GT (1999 to 2004), GT1 and GT2 again (2005 to 2010). LMP675 for a short time. | Class rules with air restrictors, boost and weight. The ACO changes them between diesel and petrol LMP1 (2009, 2010). | 1994: a Porsche 962 "road car" wins in GT1. 2005: GT3 rules bring the term "balance of performance". 2006: Audi diesel wins Le Mans. |
| 2011 | LMP1. | LMP2, GTE (GT2 renamed). | The organisers may change GTE weight, engine or aero at any time. | GT1 dropped. |
| 2012 to 2020 | LMP1, hybrid and non-hybrid side by side. | LMP2, GTE Pro, GTE Am. Four classes. | GTE: balance of performance. LMP1: "Equivalence of Technology" between hybrid and non-hybrid. | 2014: all LMP1 cars closed. 2017: LMP2 limited to four chassis makers, one engine. |
| 2021 to 2023 | Hypercar: 1030 kg, 500 kW. LMDh cars allowed from 2023. Old LMP1 cars allowed in 2021 and 2022. | LMP2 (950 kg, less power), GTE Pro (to 2022), GTE Am (to 2023). | Balance of performance for Hypercars, the hybrid speed limit is set in the BoP table. | Cars built to two different rule sets (Le Mans Hypercar and LMDh) race for the same win. |
| 2024 to 2026 | Hypercar. | LMGT3 (GT3 cars with a kit). LMP2 only at Le Mans, at least 15 places. | BoP for Hypercar and LMGT3. | Le Mans: 62 cars since 2019 (59 in 2020), three classes. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Several classes in one race | No | B4 |
| Balance of performance | No | B2 |
| Fuel formula (Group C) | Partly | `formula_fuel_tank` tank size, no fuel limit per race |
| Hybrid and non-hybrid side by side | Partly | `ers_policy` open development |
| One minimum weight | Yes | `chassis_minimum_weight` |
| Big fields (62 cars) | Partly | grid limit, at most 3 cars per team (C1) |

## Sources

- Wikipedia, "World Sportscar Championship" (classes and names by era,
  Le Mans in or out, 1991 and 1992 rules, 1993), "Group C" (fuel formula,
  weights), "Le Mans Prototype" (LMP1, LMP2, LMP3 rules), "LM GTE" (GTE
  rules and BoP rights), "Le Mans Hypercar" (2018 to 2021 rules), "Balance
  of Performance" (GT3 2005, EoT), "24 Hours of Le Mans", "FIA World
  Endurance Championship".
- Wikipedia, "1958 World Sportscar Championship" (3 L limit) and "1968
  World Sportscar Championship" (3 L prototypes from 1968, after the 7 L
  Fords of 1967), "2020 24 Hours of Le Mans" (59 entries), FIA LMP2
  technical updates 2021 to 2025 (LMP2 at 950 kg).
- Wikipedia, "1975 24 Hours of Le Mans" and Motor Sport, July 1975 (20 laps
  between fuel stops), "1976 24 Hours of Le Mans" and motor.es history of
  Le Mans 1975 to 1980 (the new GTP class).
- Wikipedia, "1999 24 Hours of Le Mans" (GT1 and GT2 renamed GTP and GTS)
  and "2005 24 Hours of Le Mans" (GTS and GT renamed GT1 and GT2).
- Autosport, "ACO changes engine rules for 2009" and "ACO publishes 2010 Le
  Mans rules", Autoblog 2009 (restrictor, boost and weight changes between
  diesel and petrol).
- Jalopnik and Motorsport Week (GTE Pro ended 2022, GTE Am 2023).
- Conflict: the "World Sportscar Championship" overview puts the 5 L and
  3 L classes in 1966, the 1968 season article in 1968. The table uses 1968.
- Conflict: one 1976 source says GTP cars had a fuel limit, others say all
  fuel limits were dropped in 1976. The table leaves the fuel limit out.
- Wikipedia, "1953" and "1962 World Sportscar Championship" (races,
  1962 titles). Wikipedia, "1975" and "1976 24 Hours of Le Mans".
- ACO 2012 announcement via 24h-lemans.com and Autosport, "ACO confirms
  2014 LMP1 regulations" (closed LMP1 cars from 2014). Motorsport.com,
  "Alpine WEC LMP1 car granted extra year of homologation" (old LMP1 cars
  in 2021 and 2022).
- Left out: the LMP2 engine size, the sources differ.

## Discord post

=== post | Sportscar classes and BoP history | wec-classes-bop
## Sportscar classes and balance of performance, 1953 to 2026

Part one of the endurance rules history (World Sportscar Championship, Le Mans, WEC), with the endurance mode in mind. The table is below. What stood out to me:

- **Classes by engine size** for the first 30 years: under 1 L, under 2 L, over 2 L, then 3 L and 5 L.
- **Group C (1982 to 1990) used fuel, not engine size:** at least 800 kg, a 100 L tank, five fuel stops per 1000 km. Any engine you like, but only about 600 L per 1000 km.
- **Different car types racing for the same win:** GT1 against prototypes in the 1990s, hybrid against non-hybrid LMP1 ("Equivalence of Technology"), Le Mans Hypercar against LMDh since 2023.
- **Balance of performance:** the term comes from GT3 in 2005. The organisers can change weight, power and aero during a season.
- **Classes in one race:** two to four, today Hypercar, LMGT3 and at Le Mans LMP2. 62 cars at Le Mans.

For the game this is: classes in one race with their own results, a rule set per class (weight, power, fuel or energy), and a BoP that changes per track. The same thing as DTM's weights per make, just bigger.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
