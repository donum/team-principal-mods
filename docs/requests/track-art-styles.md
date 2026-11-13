# Track art styles the player picks

- **Status:** draft, not posted
- **Wishlist:** E16
- **Attach:** `docs/packages/img/png/track-art-styles.png`
- **Length:** about 1,700 characters (Discord limit 2,000)

---

## Feature request: let the player pick the track art style

Hey! Another one from the DTM packs.

For DTM 2013 I redid all nine tracks as illustrated race-day images. I made them with an AI image tool, then checked each one against the real lap so the cars stay on the track. I'm happy with how they look, but I know AI art isn't for everyone. Some players would rather not see it, and that's fine.

So my idea: **a pack can ship more than one track art style, and the player picks one.**

- the pack author defines the styles (e.g. `map`, `illustrated`, `minimal`, `satellite`) and which one is the default
- the player picks a style in the settings, for this pack or for all packs that have it
- every style uses the same frame as the track file. Only the background image changes, so the racing line, pits and cars all stay the same
- if a pack doesn't have the chosen style, it falls back to the default
- optional: a small "AI" tag on a style, so players know what they're picking

Example in the pack:
```json
"track_art": {
  "default": "illustrated",
  "styles": {
    "map":         { "name": "Map",         "folder": "assets/tracks/map",         "ai": false },
    "illustrated": { "name": "Illustrated", "folder": "assets/tracks/illustrated", "ai": true },
    "minimal":     { "name": "Minimal",     "folder": "assets/tracks/minimal",     "ai": false }
  }
}
```
Today it's always `assets/tracks/<id>.png`, so a pack without `track_art` plays exactly like now.

The picture shows how it could look. All three are the same Hockenheim lap at the same size.

It would help other modders too. Someone could make a hand-drawn set for an existing pack without replacing anybody's work. Happy to test it!

---

## Notes (not for the post)

- Mockup images: "Map" is `bases/dtm-era4/assets/tracks/hockenheim13.png`
  (OpenStreetMap), "Illustrated" is the 2013 art, "Minimal" is the track
  line cut out of the map image.
- "Satellite" is only an example name. Google, Bing and Esri imagery can't
  ship in a pack; free Sentinel-2 imagery is too coarse for a track.
