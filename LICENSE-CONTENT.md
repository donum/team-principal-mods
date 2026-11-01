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

## Car images: CC BY-SA 4.0

The team car images (`seasons/*/assets/Cars/*.png`, made with
`tools/car_art.py`) build on two sources:

- **Outlines:** adapted from Oliver Pohlmann's DTM side-view illustrations
  on Wikimedia Commons (CC BY-SA 3.0 DE). The Audi V8 outline is traced from
  a photo by Matthew Lamb (Wikimedia Commons, CC BY-SA 2.0). The reference
  for each car model is listed in `seasons/*/art/cars.json`.
- **1991 liveries:** taken from the Automobilista 2 "DTM 1991" mod, used with
  the livery author's permission.

Because of ShareAlike, these images are licensed **CC BY-SA 4.0**
(<https://creativecommons.org/licenses/by-sa/4.0/>), not CC BY-NC-SA. The
credits are in each pack's `credits.txt`. The liveries show real sponsor
trademarks, which belong to their owners.

## Logos

Team and engine logos (`seasons/*/assets/logos`, `seasons/*/assets/engines`,
made with `tools/logo_art.py` from `seasons/*/art/logos.json`) come from three
places:
- **1991 team decals** from the AMS2 liveries, used with the livery author's
  permission.
- **Public-domain period logos** from Wikimedia Commons. The file for each
  logo is listed in `logos.json`.
- **Plain text crests** made for this pack (CC BY-NC-SA 4.0).

The logos are trademarks of their owners and are used here only to depict the
1991 season.

## What this license does NOT cover

- **The game's own files.** `constants.py`, default audio, dashboard
  backgrounds and other base-game data belong to the Team Principal publisher.
  This repository does not include them. The build tool copies them from your
  local install at build time (EULA §4.3).
- **Third-party trademarks and likenesses.** Names and logos of manufacturers,
  teams, sponsors and drivers (for example BMW, Mercedes-Benz, Audi, Opel,
  Warsteiner, Jägermeister, DTM) belong to their owners. This license does not
  grant any right to them, and their use here is descriptive and historical.
  Real team and sponsor logos appear only in the car images and logos described above.
- **Third-party mods.** Other Workshop packs are not used. The Automobilista 2
  "DTM 1991" mod's livery artwork is used only with its author's permission,
  only inside the car images, and the mod's files are not in this
  repository: the tool reads them from a local install.

This project is unofficial community content. It is not affiliated with or
endorsed by the Team Principal publisher, ITR e.V./DTM, or any manufacturer.
