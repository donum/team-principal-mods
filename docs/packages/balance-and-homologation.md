# Package: Balance and Homologation

Weight, ballast, performance balance and how far teams may develop their
cars. Part of the [feature packages](README.md).

- **Wishlist items:** [B1](../DEVELOPER_WISHLIST.md#b1-success-ballast--p1),
  [B2](../DEVELOPER_WISHLIST.md#b2-mid-season-balance-changes-on-a-date--p1),
  [C4](../DEVELOPER_WISHLIST.md#c4-customer-cars-and-homologation--p2),
  [D7](../DEVELOPER_WISHLIST.md#d7-development-freeze-and-homologation--p2).
- **Modes:** formula, endurance (BoP is central there), oval (spec cars).
- **Status:** outline.

## 1. What the game has today

- `chassis_minimum_weight` (one value for the grid) and `car_mass_kg` per
  team in `teams.json`.
- `scripted_changes` rows with `key`, `effective_season`,
  `new_regulation` (per season, not per week or per make).
- `technical_regulation_era` gives bonuses or penalties to car concepts.
- Teams design and build every part all season.

## 2. Every need we know

| Seasons | Need |
|---|---|
| DTM 1990, 1991 | Success ballast up to 50 or 100 kg, taken off again after poor results, newcomers on the maximum |
| DTM 1990 to 1992 | Mid-season changes for one make on a date (Audi -40 kg from Wunstorf 1991, BMW's new wing from the Nordschleife 1992) |
| DTM 1991 | Minimum weight by displacement and drivetrain |
| DTM 1991 | Customer cars: privateers buy the Evo car, the maker develops it |
| DTM 2012, 2013 | Cars homologated before the season, aero frozen during it |
| DTM 2014 to 2018 | Success ballast again (by result), later "performance weights" |
| DTM 2021 on | GT3 BoP per car model and per track |
| Super GT | Ballast from championship points, taken off near the end of the season |
| WTCR, TCR | Compensation weight per car model, recalculated every few rounds |
| F1 2017 to 2021 | Engine development tokens |

## 3. The building blocks

- **A balance block** with rows like
  `{"filter": {"engine": "Audi"}, "mass_kg": -40, "from": {"season": 1, "week": 23}}`.
  Filters: engine, team, car model, class, entry. Values: mass, power,
  drag, ride height, fuel or energy per stint.
- **Ballast rules:** by result (`per_position: [30, 20, 10]`), by points
  (`kg_per_point: 2`), with a `max_kg`, a removal rule and a value for
  newcomers.
- **Homologation:** a part category can be `open`, `tokens: N`, or `frozen`
  after a date; Evo kits as dated rows.
- **Customer cars:** a chassis contract like an engine contract. The
  customer gets the supplier's homologated parts.

## 4. Fits the existing options

- Balance rows are `scripted_changes` with a week and a filter. The system
  and the voting stay.
- `chassis_minimum_weight` stays the default; rows override per make or
  car model.
- Customer chassis use the same works, partner and customer prices as
  engines and tyres today.

## 5. Overlaps

| Shared block | Package |
|---|---|
| Ballast reads results and points | [Points](points-and-championships.md) |
| Real dates for weeks | [Calendar and world](calendar-and-world.md) |
| Classes and car models are entry tags | [Entries](entries-and-crews.md) |
| Supplier contracts | [Tyres](tyres-and-stops.md) (D9) |
| Part categories as data | [Car model](car-model.md) (D1) |

## 6. Endurance

- BoP per class, per car model and per event, with a published table.
- Energy or fuel per stint and minimum pit time as BoP values.
- Success ballast in some championships (Super GT, IMSA in the past).

## Evidence log

| Item | Season | Need | Source | Status |
|---|---|---|---|---|
| B1 | DTM 1990, 1991 | Success ballast | `seasons/dtm-199*/research` | Checked |
| B2 | DTM 1990 to 1992 | Dated make-specific changes | `seasons/dtm-199*/research` | Checked |
| D7 | DTM 2012, 2013 | Aero freeze | `seasons/dtm-2013/research/season.md` | Checked |
| B1 | DTM 2014 to 2018 | Success ballast and performance weights | [dtm_rules.html](../dtm_rules.html) | Checked |

## Open questions

- DTM 2014 to 2018: the exact weight tables.
