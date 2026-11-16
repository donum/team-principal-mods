# Questions to other mod authors

- **Context:** the Workshop mods use a few files and fields that vanilla
  doesn't have and the modding guide doesn't mention. Before we copy any of
  them, we want to know if the game reads them.
- **Checked** on 2026-11-16 against `data/default22` to `default26`,
  `data/oval/default`, `MODDING_GUIDE.md` and the 0.99.6 update notes. The game
  code is packed, so a text search of the exe can't answer this.
- **Already vanilla, our own gaps (no question needed):**
  - `sponsors.json` `"type": "title"`: vanilla has 12 title sponsors. Ours
    have no type.
  - `driverslicense.json` `practicepoint`: vanilla sets 1. Ours leaves it out.
  - `events.json` entries with a `team`: vanilla has 11 of them.
  - `series.json`: vanilla has it, but only for Oval (`data/oval/default`).

## 2010 mod and 2016 mod
Workshop items 3821355108 and 3821763947.
<https://steamcommunity.com/sharedfiles/filedetails/?id=3821355108>
<https://steamcommunity.com/sharedfiles/filedetails/?id=3821763947>

Hey! Quick questions about your mods:

- You ship a `tyre_upgrades.json` with costs for pace and durability per
  compound. Does the game read it? Where does it show up?
- Your teams have `negotiation_points` (6 to 8). What does it change? Did
  you see a difference in game?

Thanks! Dan

## F1 1989
Workshop item 3824621250.
<https://steamcommunity.com/sharedfiles/filedetails/?id=3824621250>

Hey! Your mod has a `preseasonfocus.json` with five choices (Aerodynamics,
Chassis, Internals, Qualifying, Speed).

- Does the game offer these choices before the season? Or is it for a
  feature that's coming?
- Your teams have `negotiation_points: 0`. Is 0 on purpose?

Thanks! Dan

## F1 2003
Workshop item 3830822994.
<https://steamcommunity.com/sharedfiles/filedetails/?id=3830822994>

Hey! You ship a `sponsors_min.json` next to `sponsors.json`, with the
tobacco title sponsors. Does the game load it? Is it a backup or a second
pool?

Thanks! Dan

## 2015 IndyCar
Workshop item 3837950934.
<https://steamcommunity.com/sharedfiles/filedetails/?id=3837950934>

Hey! Questions about your Oval pack:

- `rules.json` (`technical_development_enabled`, `reuse_formula_*`) isn't in
  the vanilla Oval data. Does the game read it?
- Your notes say "in_game_tested: false". Did you get a chance to test it
  since?

Thanks! Dan

## Developer
- Is `spectator_god_mode` in `options.json` a real option? The name is in
  the game, but vanilla doesn't set it. Four mods do.
- Could the modding guide list every file the game reads, so we can tell
  real fields from leftovers?
