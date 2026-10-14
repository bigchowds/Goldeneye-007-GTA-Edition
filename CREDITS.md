# Credits

## GTA Edition project

**[BigChowds](https://www.youtube.com/@BigChowds)** — project concept, creative direction, GTA-themed character and dialogue decisions, integration work, feedback-driven iteration and manual gameplay testing.

This repository preserves the incremental Python changes for the final v21 scene fixes and their focused validation material.

## Third-person foundation

**[Joshua-1248 — GoldenEye 007 Plus](https://github.com/Joshua-1248/GoldenEye-007-Plus)** — the enhanced GoldenEye foundation used for this project, including its third-person functionality and options.

The supplied development base identifies itself as GoldenEye 007 Plus. Its exact SHA-256 is `981bb761d55c959c8735807d1acf3a2a0bcfecdde136e99854f4bbf98662cc8a`. The GTA Edition patch preserves the functionality of that supplied base; it does not claim to include every feature in the current upstream version.

**[KholdFuzion and the GoldenEye decompilation contributors](https://gitlab.com/kholdfuzion/goldeneye_src)** — the decompilation foundation identified by GoldenEye 007 Plus. Further upstream contributors and notices are listed in the [Plus credits](https://github.com/Joshua-1248/GoldenEye-007-Plus/blob/main/CREDITS.txt) and [upstream notices](https://github.com/Joshua-1248/GoldenEye-007-Plus/blob/main/LICENSES_AND_NOTICES.txt).

Snapshots of the public upstream [credits](docs/upstream/GoldenEye-007-Plus-CREDITS.txt) and [licensing notices](docs/upstream/GoldenEye-007-Plus-LICENSES_AND_NOTICES.txt), retrieved on 14 October 2026, are also included. These preserve upstream attribution and notices, including the Perfect Dark MIT notice; they are not a claim that this mod contains every feature listed in the current upstream credits.

## Original games and assets

- **Rare / Nintendo and the relevant GoldenEye rights holders** — GoldenEye 007 and its original game material.
- **Rockstar Games and the relevant Grand Theft Auto rights holders** — Grand Theft Auto: San Andreas characters, dialogue, audio and other original game material used by the fan modification.

Original game material remains the property of its respective rights holders. Project attribution is not a claim of ownership of those assets or permission to redistribute them. See [NOTICE.md](NOTICE.md).

## Tools and testing

- **[xdelta / Joshua MacDonald](https://github.com/jmacd/xdelta)** — binary patch encoding and decoding. The release patch was encoded with xdelta3 3.2.2 as raw VCDIFF, with armor and secondary compression disabled.
- **Project64** — manual gameplay testing during development.
- **Mupen64Plus** — the focused Facility and Cradle runtime checks recorded in the existing validation report.
