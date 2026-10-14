"""Clear frozen dialogue exactly when the existing helicopter reward starts."""
import struct
from transfer_cj_to_plus import u32

RESET_ROM = 0xEF6E0
RESET_RAM = 0x806BABB0
RESET_CODE = bytes.fromhex('240effff 3c018003 ac2e7520 3c018003 ac20751c 3c018003 ac207518 3c018003 03e00008 ac207524')


def caption_reset_stub(base, voice):
    assert base[RESET_ROM:RESET_ROM+len(RESET_CODE)] == RESET_CODE
    # This is the existing Plus physical game mapping, confirmed by its
    # native caller and neighboring clear/set-upper-text leaf functions.
    assert RESET_RAM == 0x80600000+RESET_ROM-0x34B30
    call = 0x0c000000 | ((RESET_RAM>>2)&0x3ffffff)
    assert u32(base,0x3E2A0) == call
    at = voice['control_rom_start']+voice['respect_music_stub_offset']
    space = voice['ending_volume_stub_offset']-voice['respect_music_stub_offset']
    assert space == 224
    old = base[at:at+space];words = list(struct.unpack('>56I',old))
    assert words[:3] == [0x24080128,0x14a8000a,0]
    assert words[12:15] == [0x24080128,0x14a80022,0]
    assert words[15:21] == [0x27bdffd8,0xafbf0024,0xafa40020,0xafa5001c,0xafa60018,0xafa70014]
    assert words[48:53] == [0x27bdff80,0x3c0f8002,0x81ef43f8,0xafb1001c,0x00058c00]
    assert words[55] == 0
    # Remove the redundant second sound-ID test. Save the caller's registers,
    # call the game's own queue reset, then run the same music mute and audio.
    updated = words[:12]+words[15:21]+[call,0]+words[21:55]
    native = updated.index(0x27bdff80)
    updated[1] = 0x14a80000 | (native-2)
    updated += [0]*(56-len(updated))
    assert len(updated) == 56 and native == 47
    assert updated[18:20] == [call,0]
    blob = struct.pack('>56I',*updated)
    return blob, {'sound_id':296,'when':'Existing reward cue at the start of CJ helicopter escape',
        'native_reset_function_rom':f'{RESET_ROM:08X}','native_reset_function_ram':f'{RESET_RAM:08X}',
        'clear_both_queued_dialogue_lines_before_respect':True,
        'For_Grove_and_CJ_reply_captions_retained_before_ending':True,
        'controls_jump_and_falling_audio_unchanged':True,
        'reserved_stub_bytes':space,'audio_heap_growth_bytes':0}
