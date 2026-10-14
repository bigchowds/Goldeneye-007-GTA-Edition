# Testing Status

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
