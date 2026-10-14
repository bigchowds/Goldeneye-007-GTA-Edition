# Changelog

## v21 Beta

### Cradle

- Fixed old confrontation captions carrying into the helicopter escape sequence.
- Clears the upper dialogue queue immediately before the existing reward cue.
- Preserves the prior falling sequence, camera timing, helicopter transition and audio behaviour.
- Keeps the confrontation dialogue available before the ending transition.

### Facility

- Reworked the post-shot speech trigger so it no longer relies on a second scripted damage step that may be skipped.
- Tracks the relevant Tenpenny shot event and waits for Smoke to be dying, dead or absent before playback.
- Prevents duplicate playback.
- Restores music after the voice window without resetting the native scene timer.

### Validation

- Added focused runtime fixtures for Cradle caption sequencing.
- Added positive and negative Facility post-shot voice fixtures.
- Added binary/resource validation report for the v21 output.

### Known limitations

- Streets can freeze around the Valentin sequence.
- Dialogue conversion remains partial.
- Aztec and Egyptian are untested in this beta.
