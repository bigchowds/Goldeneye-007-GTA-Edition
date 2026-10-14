# Build Notes

## Important

The files under `src/incremental-v21/` are the **latest incremental v21 changes**, not a complete standalone source tree.

The original development build used an earlier source pack and the exact v20 build as inputs. Those files are not included here.

## Known source dependencies

The v21 scripts reference earlier development modules such as:

- `tec9_model_v18`
- `transfer_cj_to_plus`
- `cast_missions_v5`
- `dam_patch`
- `scene_missions_v10`
- `build_scene_audio_v14`
- `menu_audio`
- `build_cast_v1`
- `runtime_helpers_v12`

The main v21 builder also expects the exact previous v20 ROM/build report used during development.

## Why the repository is structured this way

The aim of this public beta snapshot is to preserve and document the latest technical changes without publishing a retail game ROM or pretending that an incomplete historical source snapshot is a reproducible build.

A future cleanup can consolidate the historical modules into a full source tree. The playable beta is distributed separately as a verified clean-ROM patch; applying that release patch does not depend on rebuilding this incremental source snapshot. See [PATCHING.md](../PATCHING.md).

## Current v21 output fingerprint

The development v21 output recorded in the validation report has SHA-256:

`f65aa6b848f3b5ca0deefcbf99d58787f5adca572a915b2b93adc9d403117613`

This hash identifies the tested development build. The ROM itself is not included.
