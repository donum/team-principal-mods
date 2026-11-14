# Dashboard images in random order

- **Status:** draft, not posted
- **Wishlist:** E20
- **Attach:** nothing needed
- **Length:** about 700 characters (Discord limit 2,000)

---

## Feature request: dashboard images in random order

Hey! A small one this time.

A pack (or a team) can have several dashboard pictures, which is great. But the dashboard always starts with image 1, so that's the one I see most of the time. Over a long career it gets a bit dull, and the other pictures hardly show up.

My idea: **an optional setting to show them in random order.**

```json
"dashboard_order": "random"
```

The game would start with a random image, or shuffle the whole set. Either works for me. It would apply to `dashboard_bg<N>.png` and to the team sets in `assets/dashboard_bgs/`. Without the setting, everything stays as it is now.

What do you think?

---

## Notes

- How it works today is in `docs/CAPABILITIES.md` (dashboard rows): the game moves through the images in number order.
- A follow-up could be the same for `title_bg` (several title screens, one picked at start). Left out to keep this post short.
