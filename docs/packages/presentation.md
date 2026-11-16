# Package: Presentation and Sound

How a pack looks and sounds: car images, portraits, sponsors, engines and
venues. Part of the [feature packages](README.md).

- **Wishlist items:** [E4](../DEVELOPER_WISHLIST.md#e4-documented-asset-names--p2),
  [E8](../DEVELOPER_WISHLIST.md#e8-engine-sounds-per-supplier-beyond-pass-bys--p3),
  [E9](../DEVELOPER_WISHLIST.md#e9-ambience-and-start-sounds-per-track--p3),
  [E10](../DEVELOPER_WISHLIST.md#e10-documented-start-sound-timing--p3),
  [E11](../DEVELOPER_WISHLIST.md#e11-a-full-field-crossing-the-line--p3),
  [E12](../DEVELOPER_WISHLIST.md#e12-a-sponsor-on-several-teams--p3),
  [E14](../DEVELOPER_WISHLIST.md#e14-pit-entry-sound--p3),
  [E15](../DEVELOPER_WISHLIST.md#e15-car-and-portrait-in-session-screens--p3),
  [E21](../DEVELOPER_WISHLIST.md#e21-backgrounds-that-fit-any-window-and-a-pack-logo--p2).
- **Modes:** all three.
- **Status:** outline.

## 1. What the game has today

- One car image per team, looked up by team name.
- `passby_audio` per engine supplier; other engine sounds are one shared
  bank; ambience is one set per pack.
- Session screens show names, positions and team colours.

## 2. The building blocks

- **Per-entry assets:** car image (optionally per round), portrait, code.
  Fallback: entry, then team, then today's art.
- **Per-supplier and per-track sound overrides**, with the pack-wide set
  as the fallback.
- **Pack-defined labels and colours** for tyres, parts and classes, used
  on every screen.
- **Make-wide sponsors** on several teams.

## 3. Overlaps

| Shared block | Package |
|---|---|
| The entry as the unit | [Entries](entries-and-crews.md) |
| Tyre names, colours, supplier logos | [Tyres and pit stops](tyres-and-stops.md) |
| Part drawings | [Car model](car-model.md) |

## 4. Endurance

- Class colours on timing and on cars (number panels).
- Crew portraits on the driver card, the current driver highlighted.
- Night and headlight visuals; per-track ambience through the day.

## Evidence log

| Item | Season | Need | Source | Status |
|---|---|---|---|---|
| E4 | DTM 1991, 2013 | Different liveries for team-mates | `seasons/dtm-2013/research` | Checked |
| E11 | DTM 2013 | Mix limits | `ui/audio_manager.py` | Checked |
