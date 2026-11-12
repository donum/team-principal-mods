# Package: Car Model

Parts, drivetrain, speed and damage for cars that aren't open-wheelers.
Part of the [feature packages](README.md).

- **Wishlist items:** [D1](../DEVELOPER_WISHLIST.md#d1-touring-car-part-set--p1),
  [D2](../DEVELOPER_WISHLIST.md#d2-drivetrain--p2),
  [D3](../DEVELOPER_WISHLIST.md#d3-documented-lap-time-controls--p1),
  [D5](../DEVELOPER_WISHLIST.md#d5-wider-car-profile-range--p2).
  D6 (damage repair) lives in [Tyres and pit stops](tyres-and-stops.md)
  as a stop service.
- **Modes:** formula (touring and GT packs), endurance (prototypes and GT).
- **Status:** outline.

## 1. What the game has today

- Open-wheel part categories; a pack can relabel the six slots in
  `car_parts.json`, but drawings and setup screens stay open-wheel.
- `car_profile` multipliers within 0.5 to 1.5.
- `lap_modifier` sets the number of laps; lap time follows micro-sector
  speeds and `car_profile`.
- Part damage from contact, swapped F1-style at the next stop.

## 2. Every need we know

| Seasons | Need |
|---|---|
| All DTM | Splitter, rear wing, suspension, brakes, gearbox instead of open-wheel parts |
| DTM 1991 | 4WD Audi strong in the wet |
| DTM 2012, 2013 | About 480 hp, 1,110 kg, lots of drag: beyond the profile range |
| DTM 2013 | Body damage carried to the end, not swapped |
| Endurance | Prototypes and GT cars in one race, very different speeds |

## 3. The building blocks

- Part categories as data, with labels, effects and drawings from the
  pack.
- `drivetrain` per car with traction and wet effects.
- A car profile from physical values (hp, mass, drag area, downforce)
  instead of multipliers, **per class**.
- A per-track lap-time multiplier and a calibration helper.

## 4. Fits the existing options

- `car_profile` stays; a profile can carry physical values instead of
  multipliers, and the multipliers keep working.
- `car_parts.json` keeps its format; categories become a list instead of
  fixed keys.

## 5. Overlaps

| Shared block | Package |
|---|---|
| Profiles per class | [Entries](entries-and-crews.md) (class tag), [Balance](balance-and-homologation.md) (BoP) |
| Frozen part categories | [Balance](balance-and-homologation.md) (D7) |
| Part drawings, setup screen art | [Presentation](presentation.md) |
| Repair as a stop service | [Tyres and pit stops](tyres-and-stops.md) |

## 6. Endurance

- Several car profiles in one race (classes).
- Wear and reliability over 6 to 24 hours; brake changes; garage repairs.
- Headlights and night pace.

## Evidence log

| Item | Season | Need | Source | Status |
|---|---|---|---|---|
| D5 | DTM 2013 | Profile limits | `tools/calibrate.py` runs | Checked |
| D2 | DTM 1991 | Audi in the wet | `seasons/dtm-1991/research` | Checked |
