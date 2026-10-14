# Testing Status

## Clean-ROM release patch

The clean-USA-ROM patch was encoded with xdelta3 3.2.2 in raw VCDIFF format, with armor and secondary compression disabled. Decoding it against the supplied 12 MiB NTSC-U `.z64` produced the tested 32 MiB v21 target byte for byte.

- Required source SHA-256: `2cdcec8a9f0cb6e36337f3ee39d8ad105dc8afa6ba1c02d466e8f5b771f9a162`
- Patch SHA-256: `1e7c08c72e0a6d0bd1e7b7e9a495058c0b566f15c63a962a389af69af5bade91`
- Output SHA-256: `f65aa6b848f3b5ca0deefcbf99d58787f5adca572a915b2b93adc9d403117613`

See [validation/v21-clean-USA-patch.json](validation/v21-clean-USA-patch.json). This is packaging verification, not a new gameplay regression test. The graphical patcher frontends linked in the installation guide were not separately exercised.

## Manual campaign testing

The current v21 beta has been manually played through the main campaign **up to and including Cradle**.

Known exception:

- **Streets:** a freeze can occur around the Valentin sequence.

Not yet tested:

- **Aztec**
- **Egyptian**

## Focused v21 runtime validation

The final v21 scene changes were also exercised with controlled Mupen64Plus runtime tests using 8 MiB RAM, audio enabled and the dynamic recompiler.

The included `validation/v21_validation.json` records these focused checks.

### Cradle

The test reproduced the previous caption spill in the earlier build and confirmed that v21 clears the queued confrontation captions before the `+RESPECT` reward/escape presentation.

### Facility

The positive fixture confirmed a single continuous playback of the intended post-shot voice after the relevant shot/death state. A negative fixture without the Tenpenny-shot marker confirmed that the voice did not play.

## Scope

These tests are deliberately narrow. They validate the targeted v21 fixes and do not replace a complete campaign regression test.
