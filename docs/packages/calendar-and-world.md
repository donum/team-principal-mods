# Package: Calendar, Weather and the Wider World

Dates, weather, feeder series, money and history. Part of the
[feature packages](README.md).

- **Wishlist items:** [A4](../DEVELOPER_WISHLIST.md#a4-more-than-one-event-per-week--p3),
  [C7](../DEVELOPER_WISHLIST.md#c7-feeder-series-with-real-race-weekends--p2),
  [D4](../DEVELOPER_WISHLIST.md#d4-weather-realism--p3),
  [E6](../DEVELOPER_WISHLIST.md#e6-currency-and-economy-per-pack--p3),
  [E7](../DEVELOPER_WISHLIST.md#e7-historical-start-state--p3).
- **Modes:** all three.
- **Status:** outline.

## 1. What the game has today

- A calendar of week slots; `calendar` regulations add, remove, move and
  replace races; scripted test weeks.
- Rain chance per track (`wet_weather_probability_multiplier`), the same
  for every visit.
- Junior series with one race per week and one points table.
- One currency and economy scale for every pack.

## 2. Every need we know

| Seasons | Need |
|---|---|
| DTM 1991 | A double-header at one venue; real dates for news |
| DTM 2013 | Different rain chances for the May and October Hockenheim rounds |
| DTM 2013 | Feeder series with 2 or 3 races per weekend and their own points |
| DTM 1991 | Budgets in Deutsche Mark, much smaller than F1 |
| DTM 1991 | Previous-season standings to set prestige and form |

## 3. The building blocks

- **A real date** for each schedule week (day of year), several events per
  week.
- **Weather by date and region**, through the day (for endurance).
- **Junior weekends** use the same weekend block as the main series
  ([Weekend format](weekend-format.md)).
- **Economy:** a currency label and global scale factors.
- **History:** previous standings as data.

## 4. Fits the existing options

- `schedule.json` weeks stay; a `date` field is optional.
- The `calendar` regulation rows and `scripted_changes` keep working;
  with dates, a change can say "from 15 September".

## 5. Overlaps

| Shared block | Package |
|---|---|
| Dates for mid-season changes | [Balance](balance-and-homologation.md) (B2) |
| Junior points | [Points](points-and-championships.md) |
| Junior eligibility | [Entries](entries-and-crews.md) |
| Weather for red flags | [Race control](race-control.md) |

## 6. Endurance

- Weather and track temperature that change through 24 hours.
- Day and night by real date and place.
- Support races and endurance cups on the same weekend.

## Evidence log

| Item | Season | Need | Source | Status |
|---|---|---|---|---|
| C7 | DTM 2013 | Five feeder series | `seasons/dtm-2013/research` | Checked |
| D4 | DTM 2013 | Rain by date | `seasons/dtm-2013/research/season.md` | Checked |
