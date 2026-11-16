# Responsive images, safe areas and a pack logo

- **Status:** draft, not posted
- **Wishlist:** E21, E5 (map aspect ratio, safe area)
- **Attach:** from `img/responsive/`: main-menu, race-hockenheim (and
  dashboard for part 4)
- **Length:** intro about 500 characters, each part 500 to 900 (Discord
  limit 2,000). Post the intro with all parts in one go, or the intro with
  part 1 and the rest one by one as replies.

---

## Intro

### Feature request: images that fit any window

Hey! Something I noticed playing our DTM 2013 pack on a wide window (about 21:9, 2000 × 857).

Pack images are made for 16:9. On a wider window the game fills the screen and cuts off what doesn't fit. Most screens cope well, but two places lose important parts: the main menu (our "DTM 2013" logo is cut in half) and the race map (the track is squashed).

I have a few small ideas, each useful on its own. Screenshots attached.

---

## Part 1: a focus point for background images

The menu photo is scaled to fill the window and the middle is kept. On a wide window the top and bottom are cut, and that's where the important bits often are.

My idea: **a pack can say which point of the image must stay in view.**

```json
"title_bg_focus": [0.75, 0.6]
```

The numbers are fractions of the image (across, down). The game crops around that point instead of the middle. The same would work for the dashboard backgrounds. Without it, the middle is kept, as now.

Optional extra: a second image for very wide windows (`title_bg_wide.png`), used when the window is wider than about 2:1.

---

## Part 2: a pack logo on the main menu

Right now a pack can't show its own logo, so we draw ours into the menu photo. That's exactly what gets cut off on a wide window (see screenshot: only half of "DTM" is left).

My idea: **an optional `assets/pack_logo.png`, drawn as its own layer**, top right of the main menu. Sized and placed like the game's own logo, so it always fits.

Optionally the same logo small on the loading screens or the dashboard header. A pack without the file looks as today.

---

## Part 3: keep the race map's shape

On the race screen the track image is stretched to the map panel, across and down separately. On a wide, short window the track gets squashed: Hockenheim at 976 × 423 px is scaled 0.94 across but 0.39 down, so the corners lose their shape (screenshot).

My idea: **keep the aspect ratio** and fill the rest of the panel with the background colour (letterbox), like the non-raw track mode already does.

---

## Part 4: document the safe areas

When we make art, we guess which part of a screen stays visible and clear of the interface. What we found so far:

- **Main menu:** the buttons and logo take the left 40 %.
- **Dashboard:** the photo shows between the sidebar (from 19 % across) and between the info cards and the button bar (47 % to 86 % down).
- **Race map:** the session header can wrap to two lines (about 82 px) and hides the top of the map; the bottom is behind the driver cards.

My idea: **a short note in the modding guide** with the safe area of each screen, ideally for 16:9 and 21:9. Then every pack can place its cars and tracks where they stay visible.

What do you think?

---

## Notes

- How the game draws the menu: `ui/main_menu` scales `assets/title_bg.png`
  and takes a subsurface; the game logo (`title_logo.png`) is a separate
  layer (game code 0.99.6).
- Our menu art: `tools/menu_art.py`, the wordmark is the `"logo"` overlay
  in `seasons/dtm-2013/art/menu.json`.
- The map numbers come from wishlist E5. The dashboard and menu bands are
  from `docs/plans/DTM2012_BACKLOG.md` (photo briefs).
- Screenshots: DTM 2013 pack, game 0.99.6, window 2000 × 857.
