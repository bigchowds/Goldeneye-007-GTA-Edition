# GoldenEye: GTA Edition — v21 Beta

Play GoldenEye 007 as **00 CJ**, with GTA: San Andreas-themed characters, custom voice lines, mission scenes and ending changes. The existing third-person functionality and options are included.

## Download and install

Download the attached **`GoldenEye-GTA-Edition-v21-beta-release.zip`** and extract it. Apply **`GoldenEye-GTA-Edition-v21-beta-clean-USA.xdelta`** to your own clean **GoldenEye 007 USA / NTSC-U `.z64` ROM**.

**No separate third-person patch is needed. No game ROM is included.** GitHub's automatic **Source code** downloads are the development snapshot rather than the playable patch.

**[Full installation guide](https://github.com/bigchowds/Goldeneye-007-GTA-Edition/blob/main/PATCHING.md)**

Required original ROM: **12,582,912 bytes (12 MiB)**

```text
Source SHA-256: 2cdcec8a9f0cb6e36337f3ee39d8ad105dc8afa6ba1c02d466e8f5b771f9a162
Patch SHA-256:  1e7c08c72e0a6d0bd1e7b7e9a495058c0b566f15c63a962a389af69af5bade91
Output SHA-256: f65aa6b848f3b5ca0deefcbf99d58787f5adca572a915b2b93adc9d403117613
```

## Included in this beta

- CJ-themed playable character and **00 CJ** presentation.
- GTA-inspired character replacements, dialogue and custom audio.
- Modified mission scenes, event timing and voice playback.
- Existing third-person functionality retained from the development base.
- Cradle ending caption cleanup while preserving the falling voice and helicopter sequence.
- Facility post-shot dialogue trigger fix.

## Test status and known issues

- Main campaign manually tested through **Cradle**.
- **Streets:** can freeze around the Valentin sequence.
- Some original GoldenEye dialogue remains.
- **Aztec and Egyptian:** untested.
- Start missions fresh rather than loading save states from an older ROM.

The clean-ROM patch was decoded with xdelta3 and verified **byte for byte** against the tested v21 build. This is a packaging change with the same game content, not a new fix for the known beta issues.

## Credits

GTA Edition project by **[BigChowds](https://www.youtube.com/@BigChowds)**. Third-person foundation: **[GoldenEye 007 Plus by Joshua-1248](https://github.com/Joshua-1248/GoldenEye-007-Plus)**, built on the GoldenEye decompilation project. See the repository [credits](https://github.com/bigchowds/Goldeneye-007-GTA-Edition/blob/main/CREDITS.md) and [fan project notice](https://github.com/bigchowds/Goldeneye-007-GTA-Edition/blob/main/NOTICE.md).

The public source is an incremental v21 snapshot; cloning it alone does not provide a complete standalone build environment.
