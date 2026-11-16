# Ambience per track and drive-by pools

- **Status:** answered 16 Nov 2026: both implemented, expected in the next version
- **Wishlist:** E9 (ambience per track), E11 (drive-by pools, its second request)
- **Attach:** nothing needed
- **Length:** about 1,000 characters (Discord limit 2,000)

---

## Feature request: ambience per track + drive-by pools

Hey! Two small audio wishes that would add a lot of variety.

**Ambience per track**
Right now every round plays the same crowd and track sound. But Monaco between the walls sounds nothing like the open spaces of Monza. A track announcer who speaks the local language would make it even more authentic.

An optional per-track set in `session_layers.json` would be nice, falling back to the default set:
```json
"tracks": {
  "monaco": { "crowd": ["monaco_crowd.ogg"], "announcer": ["monaco_pa_fr.ogg"] }
}
```

**Drive-by pools**
`passby_audio` takes one clip per engine supplier. So every car of that make sounds exactly the same, and two of them close together sound like one car. A list of clips per supplier, picked at random per car, would fix that:
```json
"passby_audio": ["audi_passby_1", "audi_passby_2", "audi_passby_3"]
```

Both are optional, so packs without them sound like now. Happy to record and test sets for the DTM packs!

---

## Notes

- Monaco and Monza are the examples because the developer knows the F1 tracks. The DTM case (Norisring vs. Lausitzring) is in E9.
- The JSON keys in the ambience example are made up. The real layer names come from `session_layers.json`.
- Ideas dropped from this post, maybe for a later one: dashboard images in random order (E20), more than one title screen, photo credits on screen, track facts at the start of the weekend, pack tips while loading, a season intro.

## Answer (Joe [TPRM], 16 Nov 2026)

"Implemented", both parts, optional. The format differs a bit from our guess:

```json
"tracks": {
  "monaco": {
    "crowd": {"file": "monaco_crowd.ogg", "gain": 0.9},
    "pa": {"file": "monaco_pa_fr.ogg"}
  }
}
```

- One `file` per layer (not a list), with an optional `gain`. The layer is `pa`, not `announcer`.
- Drive-by pools as asked: `"passby_audio": ["audi_passby_1", "audi_passby_2", "audi_passby_3"]`.
- To check in the next version: which file holds `tracks` (we assume `session_layers.json`), whether other layers (track bed) can be overridden, and whether the pass-by pick is per car or per pass.
