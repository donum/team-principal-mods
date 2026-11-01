# Team Principal Mods

Community season packs for
[Team Principal: A Racing Manager](https://store.steampowered.com/app/4340600/Team_Principal_A_Racing_Manager/),
published via the Steam Workshop.

The first goal is **historic DTM** (Deutsche Tourenwagen-Meisterschaft) seasons,
starting with **1991**.

| Season | Status | Folder |
|---|---|---|
| DTM 1990 | 🚧 generated and playable, not yet tested in-game | [`seasons/dtm-1990`](seasons/dtm-1990) |
| DTM 1991 | ✅ playable; lap times need calibrating | [`seasons/dtm-1991`](seasons/dtm-1991) |
| DTM 1992 | 🚧 generated and playable, not yet tested in-game | [`seasons/dtm-1992`](seasons/dtm-1992) |
| DTM 2013 | 🚧 generated and playable, not yet tested in-game | [`seasons/dtm-2013`](seasons/dtm-2013) |
| DTM 1984–2026 | 📚 research data ([season archive](tools/build_browser.py)) | `seasons/*/research` |

## How it works

The repo only contains **our own content**. A pack is assembled from:

1. a **base pack** taken from your local game install (e.g. `data/default26`),
   which supplies the engine files we don't touch (constants, audio, tyre
   model...), and
2. our **season overlay**: teams, drivers, staff, engines, tyres, calendar,
   regulation patches, traced tracks and our own artwork.

```bash
python tools/build_pack.py seasons/dtm-1991
```

```bash
python tools/build_pack.py seasons/dtm-1991 --install
```

`--install` copies the pack into `<game>/data/<pack_folder>`. Set your game
path with `--game`, or in a `local.json` file (gitignored):

```json
{ "game_path": "X:/SteamLibrary/steamapps/common/Team Principal A Racing Manager" }
```

The build validates cross-references: teams ↔ drivers ↔ engines ↔ tyres ↔
calendar ↔ tracks. Placeholder geometry is used for venues we haven't traced
yet, and is reported in the output.

## Docs

- [Modding capabilities and limits](docs/CAPABILITIES.md): what the game
  lets us change, what has to be approximated, and the open questions.
- [Wish list for the game developer](docs/DEVELOPER_WISHLIST.md): what the
  game would need for full historical accuracy.
- [DTM eras](docs/ERAS.md): the six eras from 1984 to today, and how each
  maps to the game.
- [DTM 1991 season dossier](seasons/dtm-1991/README.md): sourced facts behind
  the data.

## License

- Tooling: [MIT](LICENSE)
- Content (season data, research, art): [CC BY-NC-SA 4.0](LICENSE-CONTENT.md)

This is unofficial community content. It is not affiliated with the game's
publisher, the DTM, or any manufacturer. Real names are used for historical
description only. No official logos or third-party mod files are included.
