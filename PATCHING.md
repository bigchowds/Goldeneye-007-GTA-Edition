# Installing GoldenEye: GTA Edition — v21 Beta

The playable release is a **single xdelta patch** applied to a **clean GoldenEye 007 USA / NTSC-U ROM in `.z64` format**. It includes the GTA Edition changes and the existing third-person functionality and options. No separate third-person patch is required.

No original or modified game ROM is included in the download.

## Download

Get `GoldenEye-GTA-Edition-v21-beta-release.zip` from the [v21 beta release](https://github.com/bigchowds/Goldeneye-007-GTA-Edition/releases/tag/v21-beta), then extract it. Use the attached release download rather than GitHub's automatic **Source code** archive.

Patch filename: `GoldenEye-GTA-Edition-v21-beta-clean-USA.xdelta`

## Required original ROM

Use your own legally obtained, unmodified **USA / NTSC-U `.z64`** dump with these fingerprints:

| Check | Required value |
| --- | --- |
| Size | 12,582,912 bytes (12 MiB) |
| SHA-256 | `2cdcec8a9f0cb6e36337f3ee39d8ad105dc8afa6ba1c02d466e8f5b771f9a162` |
| SHA-1 | `abe01e4aeb033b6c0836819f549c791b26cfde83` |
| MD5 | `70c525880240c1e838b8b1be35666c3b` |

The required SHA-1 also matches the NTSC-U baseline recorded by [GoldenEye 007 Plus](https://github.com/Joshua-1248/GoldenEye-007-Plus/blob/main/ge007.u.sha1).

PAL, Japanese, byte-swapped `.n64` / `.v64`, already patched and padded dumps do not have the required fingerprint. Renaming a file to `.z64` does not convert its byte order.

## Apply with a graphical patcher

Use an xdelta-compatible patcher, for example [xdelta-wasm](https://kotcrab.github.io/xdelta-wasm/) or xdeltaUI.

1. Select the **clean USA `.z64` ROM** as the original/source file.
2. Select `GoldenEye-GTA-Edition-v21-beta-clean-USA.xdelta` as the patch.
3. Choose a new output name, such as `GoldenEye-GTA-Edition-v21.z64`. Keep your original ROM.
4. Apply the patch. If the source is rejected or a checksum error appears, check the original ROM hash rather than forcing the patch.
5. Open the resulting `.z64` in your emulator and start a mission fresh.

For testing, use **8 MiB / Expansion Pak RAM** if your emulator offers a RAM-size setting; the recorded focused runtime checks used that configuration. Manual gameplay testing was carried out in Project64.

This package was verified with xdelta3. The named graphical frontends are convenience options and have not been separately tested with this release.

## Apply with xdelta3

[Download xdelta3 from its official releases](https://github.com/jmacd/xdelta/releases). From a folder containing the patch and your original ROM:

```sh
xdelta3 -d -s "Goldeneye 007 Clean USA.z64" "GoldenEye-GTA-Edition-v21-beta-clean-USA.xdelta" "GoldenEye-GTA-Edition-v21.z64"
```

On Windows, use `xdelta3.exe` in place of `xdelta3`. Substitute your actual source filename if it differs.

## Verify the result

| File | Size | SHA-256 |
| --- | --- | --- |
| Patch | 9,399,950 bytes | `1e7c08c72e0a6d0bd1e7b7e9a495058c0b566f15c63a962a389af69af5bade91` |
| Patched ROM | 33,554,432 bytes (32 MiB) | `f65aa6b848f3b5ca0deefcbf99d58787f5adca572a915b2b93adc9d403117613` |

In Windows PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath ".\Goldeneye 007 Clean USA.z64"
Get-FileHash -Algorithm SHA256 -LiteralPath ".\GoldenEye-GTA-Edition-v21.z64"
```

The clean-ROM patch was decoded and the result matched the tested v21 development ROM **byte for byte**. Its report is in [validation/v21-clean-USA-patch.json](validation/v21-clean-USA-patch.json).

## Beta notes

- Main campaign manually tested through **Cradle**.
- **Streets:** known freeze risk around the Valentin sequence.
- Some original GoldenEye dialogue remains.
- **Aztec** and **Egyptian** are untested.
- Start missions fresh. Save states made with an older ROM can retain the older scene state.

This release package preserves the existing v21 game build; it does not resolve these beta limitations. See [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

## Earlier development patch

An earlier file named `GoldenEye-GTA-Edition-v21-beta.xdelta` required the exact Third Person development base. It is a different patch. For this release, use **`GoldenEye-GTA-Edition-v21-beta-clean-USA.xdelta` with the clean original USA ROM**.
