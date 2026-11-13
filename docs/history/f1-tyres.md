# F1 tyre rules, 1950 to 2026

Part of a series on how F1 rules changed (qualifying, points, tyres, pit
stops). Each file has the table, the sources and a Discord post. The table
image is made with `python -I tools/history_table.py docs/history/f1-tyres.md`.

`(?)` marks a detail that the sources we read did not confirm. Check it
before you rely on it.

## Table

| Years | Suppliers | Tyres | Rules per weekend | Quirks |
|---|---|---|---|---|
| 1950 to 1958 | Pirelli, Firestone, Englebert, Continental, Avon, Dunlop. Firestone only at Indianapolis. | Treaded road-style tyres, cross-ply. | No limits. Change tyres whenever you want. | Several makes in one field, each team picks. |
| 1959 to 1970 | Dunlop (alone 1960 to 1963), then Goodyear from 1964 and Firestone. | Nylon casings, lower and wider every year. | No limits. | Tyre war Goodyear vs Firestone from the mid 1960s. |
| 1971 to 1976 | Goodyear and Firestone (Firestone to 1974 (?)), then Goodyear. | Slicks from the 1971 Spanish GP (Firestone). | No limits. Special qualifying tyres start to appear (?). | Slicks plus wings: grip jumps. |
| 1977 to 1986 | Goodyear vs Michelin (1977 to 1984), Pirelli (1981 to 1986), Avon (1981 to 1982). | Radial tyres arrive with Michelin. Qualifying tyres that last one or two laps (?). | Few limits. Qualifying tyre sets limited per driver in the 1980s (?). | Three makes at once in the early 1980s. A team on the "wrong" tyre has no chance. |
| 1987 to 1996 | Goodyear, with Pirelli again 1989 to 1991. Goodyear alone 1987 to 1988 and 1992 to 1996. | Rear tyres narrower from 1993 (18 to 15 inch rim width). Qualifying tyres end in the early 1990s (?). | Set limits per weekend (?). | Goodyear wins almost every race for ten years. |
| 1997 to 1998 | Goodyear vs Bridgestone. Goodyear leaves after 1998. | 1998: grooved tyres, 3 grooves front, 4 rear, to cut grip. | Set limits per weekend (?). | Bridgestone wins the title in its second year. |
| 1999 to 2000 | Bridgestone alone. | Four grooves front and rear. | Two compounds per race, team picks one (?). | |
| 2001 to 2006 | Bridgestone vs Michelin. | Grooved. Each maker brings tyres made for each team. | 2005: one set for qualifying and the whole race, no changes unless damaged or wet. 2006: changes allowed again, 14 sets per weekend (7 dry). | USA 2005: Michelin tyres were unsafe in the banked turn. Michelin teams pulled out after the formation lap, only 6 cars raced. |
| 2007 to 2008 | Bridgestone alone. | Grooved. Four dry compounds in the range, two per race. | Both dry compounds must be used in the race, unless it is wet. Softer tyre marked with a white stripe in a groove. | First race of 2007: the soft tyre had a small dot, nobody could see it. Japan 2008: green grooves for an environment campaign. |
| 2009 to 2010 | Bridgestone alone. Leaves after 2010. | Slicks again. Soft tyre has green sidewalls. 2010: front 270 to 245 mm. | 2009: 14 sets. 2010: 11 sets. Top 10 start on their Q3 tyres (2010). | Refuelling banned in 2010, so tyres decide strategy. |
| 2011 to 2015 | Pirelli alone. | 13-inch. Coloured lettering per compound (hard silver, medium white, soft yellow, supersoft red). | 11 dry sets. Two compounds per race, both used in the dry. Top 10 start on Q3 tyres, later Q2 tyres (?). | Pirelli asked to make tyres that wear fast, to force stops. Silverstone 2013: several rear tyres failed, new tyres from Hungary (?). |
| 2016 | Pirelli alone. | Ultrasoft added (purple). | Three compounds per race, 13 sets. Pirelli fixes 2 race sets and 1 soft set for Q3, teams pick the other 10, weeks in advance. Top 10 start on Q2 tyres. Minimum pressures set by Pirelli (?). | Teams pick different sets, so tyre counts differ per car. |
| 2017 to 2018 | Pirelli alone. | Much wider tyres. 2018: hypersoft (pink) and superhard (orange), seven compounds. | Same as 2016. | Seven compounds and many colours, hard to follow on TV. |
| 2019 to 2021 | Pirelli alone. | Five dry compounds C1 to C5. Per race always called hard, medium, soft: white, yellow, red. | Three compounds per race, 13 sets. Top 10 start on Q2 tyres (to 2021). | A "soft" is a different tyre at every track. |
| 2022 to 2024 | Pirelli alone. | 18-inch wheels, 720 mm. 2023: C0 added, 2024: dropped. | Free start tyre. 2023 Hungary and Monza: 11 sets, hard/medium/soft for Q1/Q2/Q3. Blanket temperatures limited, a ban was planned and dropped (?). | Low-profile tyres, cars look different. |
| 2025 | Pirelli alone. | C6 added, C1 to C6. | Monaco: at least two stops (three sets) in the race. | The Monaco rule was dropped again for 2026. |
| 2026 | Pirelli alone, contract to 2028. | Narrower: 280 front, 375 rear. Five dry compounds C1 to C5, intermediate green, full wet blue. | Three dry compounds per race, at least two used unless it is wet. | |

## Rules across all years

- Wet tyres (intermediate and full wet) are not limited by the two-compound
  rule: once a race is wet, any choice is fine.
- One supplier for everyone since 2007. Before that, tyre wars decided
  titles: 1998 Bridgestone, 2005 Michelin.

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Several tyre makers, tyre wars | Yes | `tyre_suppliers.json`, a supplier per team |
| Own grip and wear per tyre maker | Partly | ratings per compound, wet included, no warm-up per maker (D9) |
| Two dry compounds must be used | Yes | `formula_compound_usage` |
| Sets per weekend | Yes | `weekend_tyre_allocation`: any number of dry, inter and wet sets |
| Own compound names and colours (C1 to C5, option) | Partly | names from `tyremodel.json`, colours fixed by the first letter (D8) |
| One set for qualifying and race (2005) | No | B12 |
| Top 10 start on their qualifying tyres | No | B12 |
| Tyre warmer limits or bans | No | B12 |
| Wet and intermediate tyres | Yes | weather and wet tyres built in |

## Sources

- Wikipedia, "Formula One tyres" (supplier table, groove and size rules,
  2005 to 2026 rules), "Bridgestone" (F1 part, via summary).
- From earlier reads: Wikipedia "Formula One race weekend" and season
  articles (2006 and 2010 set counts, 2023 tyre trial, 2025 Monaco).
- Not confirmed, marked `(?)`: qualifying tyres and when they ended, set
  limits before 2005, 2011 to 2015 top 10 rule, Silverstone 2013, minimum
  pressures, tyre blankets, Firestone's last year.

## Discord post

=== post | F1 tyres history | f1-tyres
## F1 tyre rules, 1950 to 2026

Part three of the rules history (after qualifying and points). The table is below. What stood out to me:

- **Free for 25 years.** Until the late 1970s any number of sets, any make. Several tyre makers in one field.
- **Tyre wars decided titles.** Goodyear vs Firestone, then Michelin, Pirelli, Bridgestone. USA 2005: the Michelin teams pulled out, only 6 cars raced.
- **Grooves to slow cars down** (1998 to 2008), then slicks again in 2009.
- **2005: one set for qualifying and the whole race.** Changes only for damage or rain.
- **2007 on: two dry compounds per race, both must be used.** That rule is still there.
- **2016: teams pick their own sets** weeks before the race, from three compounds.
- **Names vs compounds:** since 2019 "soft" just means the softest of the three brought to that track (C1 to C5/C6).

For the game this is: a compound range per season, which compounds come to each race, sets per weekend (who picks them), must-use rules (both compounds, a minimum number of stops like Monaco 2025, top 10 start tyre), and tyre makers with their own grip and wear. Most of these already fit the rules-as-rows idea from my earlier posts.

The last table in the picture shows what the game can do today: yes, partly or no.

Last one: pit stops. Mistakes? Tell me!
