# Package: Modding Format and Tools

How packs are built, loaded and checked. This package makes every other
one cheaper. Part of the [feature packages](README.md).

- **Wishlist items:** [E1](../DEVELOPER_WISHLIST.md#e1-overlay-partial-packs--p1),
  [E2](../DEVELOPER_WISHLIST.md#e2-settings-as-data-not-python--p1),
  [E3](../DEVELOPER_WISHLIST.md#e3-published-schema-and-validation--p2),
  [E5](../DEVELOPER_WISHLIST.md#e5-track-editor-features--p2),
  [E13](../DEVELOPER_WISHLIST.md#e13-translated-pack-texts--p3).
- **Modes:** all three.
- **Status:** outline.

## 1. What the game has today

- A pack is a full copy of about 30 files plus art and audio.
- Workshop packs read `constants.py` as safe data since 0.99.6; local
  packs still run it as Python.
- A modding guide, but no schema and no load-time validation.
- Track editors for formula and oval tracks.

## 2. Why it matters for the other packages

- Every new block (stage lists, rule rows, points schemes, balance rows)
  is more data. Without a schema and validation, a typo silently falls
  back to a default.
- Overlay packs let a season pack ship only its own blocks, so a game
  update reaches it.
- A shared block library (presets) lets packs reuse
  `dtm_2013_q4` or `f1_2010_tyres` by id.

## 3. The building blocks

- `base_pack` in `workshop.json`, merged at load time.
- `constants.json`, read the same way for local and Workshop packs.
- A JSON schema per file, a validation report at load, a list of fields
  that refer to team names.
- Language maps for pack texts.

## 4. Endurance

- Endurance packs will be the biggest (classes, crews, BoP tables);
  overlays and validation matter most there.

## Evidence log

| Item | Season | Need | Source | Status |
|---|---|---|---|---|
| E2 | 0.99.6 | Safe constants for Workshop packs only | Game code, `workshop_manager` | Checked |
