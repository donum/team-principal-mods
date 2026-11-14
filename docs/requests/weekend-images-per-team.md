# Weekend images per team

- **Status:** draft, not posted
- **Wishlist:** E19 (builds on E17)
- **Post after:** [Weekend images: track, session and result](weekend-images.md). This one only makes sense once that idea is known.
- **Attach:** `img/weekend-journey/01g-start-race-start.jpg`, `img/weekend-journey/06-qualifying.jpg`
- **Length:** about 1,300 characters (Discord limit 2,000)

---

## Feature request: weekend images per team

Hey! A small follow-up to the weekend images idea.

You play one team for a whole season. A photo of **your own cars** at this track makes the weekend feel like yours, much more than a general track photo. Teams also have their own pictures: the crew, the garage, their cars on the grid. Packs often have these with the team's permission.

So my idea: **a team can replace the pack's weekend pictures.** If you play BMW Team MTEK, you see MTEK photos. Every other team sees the pack's track photos.

The game looks for a picture in this order:
1. your team, this track, this session
2. your team, this session (any track)
3. this track, this session
4. the pack, this session
5. today's screen without a picture

This would work for the session screens, the start of the weekend, the result pictures (win, podium, points, no points, retired) and the dashboard background. Several pictures per entry, the game picks one. A team without its own pictures sees the pack's, so nothing changes for packs that don't use it.

```json
"weekend_images": {
  "race": ["race.jpg"],
  "teams": {
    "bmw_mtek": {
      "dashboard": ["mtek_garage.jpg"],
      "race": ["mtek_grid.jpg"],
      "results": { "win": ["mtek_win.jpg"] }
    }
  }
}
```

Two screens from the 2013 mock-ups are attached. What do you think?

---

## Notes

- The attached qualifying screen uses a BMW press photo from the real qualifying day (17 Aug 2013): Wittmann's MTEK car from behind. With this idea, a pack could show it to MTEK players only and a neutral track photo to everyone else.
- Team ids in the example follow the pack's team ids. The real key would be whatever the game uses for teams.
