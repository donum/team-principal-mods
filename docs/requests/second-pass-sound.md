# Back-straight pass-bys

- **Status:** draft, not posted
- **Wishlist:** E22 (and E11 for the car count on the main straight)
- **Attach:** `img/second-pass/all.png` (18 tracks with a second pass),
  `img/second-pass/counter.png` (5 without)
- **Length:** about 1,195 characters (Discord limit 2,000)

---

## Feature request: pass-bys on the back straight

Hey! A small idea for more immersion.

On many tracks you hear the cars twice per lap. Once on the main straight, and again when they come back on the back straight (in German we say *Gegengerade*). Brands Hatch, Monaco, Suzuka, Sepang, Hungaroring, Singapore and many more. Right now we only hear them at the finish line, and then it's quiet.

Idea: an optional list of extra pass-by points per track:
```json
"flyby_points": [ { "progress": 0.58 } ]
```
When a car passes there, the game plays a pass-by. The game knows the track layout, so it could set the volume by itself: further away from the start line = quieter. An optional `"volume"` could override it.

Bonus: a pool of far pass-bys in `hotlap_flybys.json`, recorded from across the track:
```json
"far_passby": ["far_1", "far_2"]
```
If there is none, just play the normal pass-by quieter.

Also, when a big group comes down the main straight, I often hear fewer pass-bys than there are cars.

Tracks without the list sound like now. I attached 18 tracks where this happens (blue) and 5 where it doesn't (Monza, Imola...).

Happy to record and test far pass-bys for the DTM packs!

---

## Notes

- The layouts and numbers come from `tools/second_pass_maps.py`
  (vanilla Monaco, Suzuka, Abu Dhabi and Melbourne; F1 workshop packs;
  BTCC 1991; DTM 2010, 2013 and 2018). The full table with lap progress
  is in wishlist E22. Rerun the tool to redraw them.
- The JSON keys are made up. The progress value is the lap fraction, as in
  `drs_zones`.
- Suzuka also crosses itself at the bridge. A listening point there would
  hear the cars twice too, but it is far from the line.
