# Content License: CC BY-NC-SA 4.0

All mod content in this repository is licensed under the
**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International**
license (CC BY-NC-SA 4.0). This covers season data, research dossiers, track
traces, graphics and other creative assets, mainly under `seasons/` and `docs/`.

Full legal code: <https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode>

In short, you may share and adapt this content if you:

- **Attribute.** Credit "Team Principal Mods by Daniel Raude", link to this
  repository, and say what you changed.
- **Stay non-commercial.** This also matches the Team Principal EULA (§4.2),
  which only allows free, non-commercial mods.
- **Share alike.** Release your adaptations under the same license.

Tooling (`tools/`) is MIT licensed. See `LICENSE`.

## Why this license

- The game's EULA only permits **free, non-commercial** mods, so the NC clause
  matches what the platform requires anyway.
- **ShareAlike** keeps community improvements (corrected entry lists, better
  track traces, new liveries) open for everyone, which is common for
  historic-racing mods.
- Attribution keeps the research credit attached when packs get reused or
  split up on the Workshop.

## OpenStreetMap-derived tracks

Track geometry (`seasons/*/tracks/*.json`) and track overview maps
(`seasons/*/assets/tracks/*.png`) produced by `tools/osm_track.py` are derived
from OpenStreetMap data:

> Map data © OpenStreetMap contributors, available under the Open Database
> License (ODbL) 1.0. <https://www.openstreetmap.org/copyright>

That attribution must be kept wherever these files are redistributed,
including Workshop uploads. Each pack ships it in `credits.txt`, and each
track JSON carries it in its `source` field. The rendered maps are Produced
Works under ODbL. Any track geometry that counts as extracted data stays under
the ODbL as well.

## What this license does NOT cover

- **The game's own files.** `constants.py`, default audio, dashboard
  backgrounds and other base-game data belong to the Team Principal publisher.
  This repository does not include them. The build tool copies them from your
  local install at build time (EULA §4.3).
- **Third-party trademarks and likenesses.** Names and logos of manufacturers,
  teams, sponsors and drivers (for example BMW, Mercedes-Benz, Audi, Opel,
  Warsteiner, Jägermeister, DTM) belong to their owners. This license does not
  grant any right to them, and their use here is descriptive and historical.
  Real sponsor or manufacturer logos are never committed to this repository.
- **Third-party mods.** Other Workshop packs or sim-racing mods (for example
  the Automobilista 2 "DTM 1991" mod) are used for **reference and inspiration
  only**. None of their files are copied here.

This project is unofficial community content. It is not affiliated with or
endorsed by the Team Principal publisher, ITR e.V./DTM, or any manufacturer.
