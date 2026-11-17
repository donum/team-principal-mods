# BTCC 1991 portrait drawings

**Status 2026-11-17:** 26 drivers have an AI-generated portrait made with
ChatGPT (OpenAI) from the round of 11:30, only for the drivers with a 1991
TV still or web photo as reference. The 12 without a reference (Berridge,
Fenwick, Godfrey Hall, Leech, Baird, Llewellyn, Hales, Lyall, MacKay,
Jeff Wilson, Bardy, Forrest) are pinned to helmet cards. Originals in
`~/Pictures/mods/btcc-1991/portraits/drawn/`; the earlier painted round is
kept in `drawn/round1_paintings/` and is not used.
A hand drawing by a friend can still replace any of them (below).

The pack's portraits come from two places:

1. **Commons photos** (`tools/portrait_art.py`), but only where a free photo
   shows the driver close to 1991. Most free photos are from 2009 or later.
2. **Drawn portraits** by a friend, using our private 1991 TV frames as
   reference (`~/Pictures/mods/btcc-1991/portraits`, see its README). The
   frames themselves never go in the pack or git. Only the drawing does.

Everyone else keeps a helmet card in team colours.

Commons run of 2026-11-17: only Christian Danner (1995, Donington) is
close enough and shows his face. The others found were from 2004 to 2023,
showed a helmet, or showed the wrong thing (David Leslie: a tombstone), so
they are pinned to helmet cards in `art/portraits.json`.

## Message to the artist

> Hey!
>
> I'm building a BTCC 1991 season for Team Principal and I'd love driver
> portraits that look like the drivers did back then. There are almost no
> free photos from 1991, but I have stills from the old BBC coverage.
>
> Would you be up for drawing some of them? I can send you the stills as
> reference.
>
> - Format: 683 x 1024 px, head and shoulders, face a bit above the middle
> - Your own drawing please, not a traced or painted-over still
> - Any style you like, as long as it is the same for all of them
> - I'll credit you by name in the mod and on the Workshop page
>
> The top 15 drivers have good stills, so those would be first (list
> below). No rush at all.
>
> Thanks!
> Dan

## Drivers with good 1991 stills (first batch)

Robb Gravett, Andy Rouse, Gary Ayles, Tim Harvey, Laurence Bristow,
John Cleland, Jeff Allam, Will Hoy, Ray Bellm, Jonathan Palmer,
Steve Soper, Tim Sugden, Christian Danner, Keith Odor, Frank Sytner.

The best still per driver is listed in the private README. Send the artist
the `_crop.jpg` files, plus `overview.jpg` for the whole grid.

## When a drawing arrives

1. Save it as `~/Pictures/mods/btcc-1991/portraits/drawn/<Driver>.png`
   (outside git, like the car images).
2. Pin it in `seasons/btcc-1991/art/portraits.json`:

   ```json
   "Will Hoy": {"source": "drawing", "pinned": true,
                "image": "~/Pictures/mods/btcc-1991/portraits/drawn/Will Hoy.png",
                "author": "<artist name>", "license": "used with permission"}
   ```

3. Run `python tools/portrait_art.py seasons/btcc-1991 --only "Will Hoy"`
   and then `python tools/build_pack.py seasons/btcc-1991 --install`.
   The drawing goes to `assets/portraits/` and its credit to `credits.txt`.
