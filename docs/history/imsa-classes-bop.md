# IMSA classes and balancing, 1971 to 2026

Part of the IMSA rules history (classes and balancing, race format and
points). IMSA GT Championship 1971 to 1998, American Le Mans Series 1999
to 2013 (and Grand-Am 2000 to 2013), WeatherTech SportsCar Championship
from 2014. The table image is made with
`python -I tools/history_table.py docs/history/imsa-classes-bop.md`.

`(?)` marks a detail that the sources we read did not confirm.

## Table

| Years | Top class | Other classes | Balancing | Quirks |
|---|---|---|---|---|
| 1971 to 1980 | GTO and GTU. GTX from 1977 (Group 5). | Touring TO and TU (to 1977 and 1976). AAGT from 1975. | Classes by engine size. | Turbos allowed from mid 1977. |
| 1981 to 1993 | GTP prototypes (from 1981, first champion Redman in 1981). | Lights (from 1985), GTO, GTU, GTS from 1992 (GTO renamed). | GT classes: engine size against minimum weight: 3.0 L at 1,900 lb up to 6.0 L at 2,700 lb, turbos 15 to 20% heavier. | GTP had no fuel limit, unlike Group C. Last GTP race October 1993. |
| 1994 to 1998 | WSC: open-top, flat-bottom, production engines. | GTS-1, GTS-2 (1995), GTS-3 (1997). 1998: GT1, GT2, GT3. | Air restrictors, weight and rev limits per engine type. 1995: turbo WSC cars get smaller restrictors and more weight. | Mazda RX-7 won its class at Daytona ten years in a row from 1982. |
| 1999 to 2013 | ALMS: LMP1, later P1. Grand-Am: Daytona Prototypes from 2003. | ALMS: LMP2, GT1 (to 2009), GT2/GT, Challenge classes (PC, GTC). Grand-Am: GT, GX. | ALMS: ACO class rules, plus IMSA performance adjustments in GT (2010). Grand-Am: DP engine sizes changed to level the field, standard ECU from 2007. | Two rival series. Grand-Am ran GT on Saturday and prototypes on Sunday at short tracks. |
| 2014 to 2016 | P: Daytona Prototypes, LMP2, DeltaWing together. | PC (one-make), GTLM (GTE rules), GTD (full GT3 rules from 2016). | Balance of performance, also between DP and LMP2. | United SportsCar Championship, WeatherTech from 2016. |
| 2017 to 2022 | DPi (own class from 2019). | LMP2, LMP3 (2021 to 2023), PC (2017), GTLM (to 2021), GTD Pro (from 2022, GT3), GTD. | BoP. | DPi was based on the 2017 LMP2 cars. |
| 2023 to 2026 | GTP: LMDh and Le Mans Hypercar cars. | LMP2, GTD Pro, GTD. | BoP. | GTP, LMP2 and GTD cars can also race at Le Mans. |

## In the game today

Game support in Team Principal 0.99.5 and the 0.99.6 beta. Yes: set in pack data. Partly: a stand-in that behaves differently. No: not possible today. IDs such as A1 are items in `docs/DEVELOPER_WISHLIST.md`.

| Rule | Game | How |
|---|---|---|
| Several classes in one race | No | B4 |
| Weight by engine size, balance of performance | No | B2 |
| Different car types in one class | No | C9 |
| Hybrid and non-hybrid side by side | Partly | `ers_policy` open development |
| One minimum weight | Yes | `chassis_minimum_weight` |

## Sources

- Wikipedia, "IMSA GT Championship" (classes 1971 to 1998, weight
  formula, GTP), "American Le Mans Series", "Rolex Sports Car Series",
  "IMSA SportsCar Championship" (classes 2014 to 2026).
- Racer, Motorsport.com, Sportscar365 2014 reports (BoP between DP and
  LMP2 from the 2014 Rolex 24).
- Motor Sport, March 1995, "The hares and the tortoise" (1995 restrictor,
  weight and rev changes), Motor Sport 1993 (WSC power set by air
  restrictors).
- Wikipedia, "Daytona Prototype" (engine sizes changed to level the field,
  standard ECU 2007), Grand-Am "Grand-Am 101: the Daytona Prototype
  class" (2012). Autoracing1, "IMSA revises performance balancing rules
  for ALMS", Corvette Blogger 2010 (ALMS GT adjustments).
- Wikipedia, "1998 IMSA GT Championship" and "1998 12 Hours of Sebring"
  (1998 classes WSC, GT1, GT2, GT3).
- Sportscar365 (GTD moves to full FIA GT3 rules in 2016). GTD itself
  starts in 2014, so the old "since 2016" note meant the GT3 rules.
- The weight formula sits in the GT section of "IMSA GT Championship",
  not in the GTP section.

## Discord post

=== post | IMSA classes history | imsa-classes-bop
## IMSA classes and balancing, 1971 to 2026

North America's sports car racing, as a second test for classes in one race. The table is below. What stood out to me:

- **Always several classes in one race,** from GTO and GTU (1971) to GTP, LMP2, GTD Pro and GTD today.
- **Balancing by engine size and weight in the 1980s GT classes:** a 3.0 L car at 1,900 lb, a 6.0 L car at 2,700 lb, turbos 15 to 20% heavier.
- **Two rival series** from 1999 to 2013 (ALMS and Grand-Am), merged in 2014.
- **Different car types in one class:** Daytona Prototypes, LMP2 and the DeltaWing together (2014), now LMDh and Le Mans Hypercar cars in GTP.
- **Pro-am rules by driver rating** in LMP2 and GTD (see part two).

For the game this is the same as endurance: classes with their own results, a balance per class and car type, and different car types racing for the same class win.

The last table in the picture shows what the game can do today: yes, partly or no.

Mistakes? Tell me!
