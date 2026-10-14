"""Play Tenpenny's retained recording after his scripted shot kills Smoke."""
import struct
from cast_missions_v5 import Editor, lists, LENGTHS
from dam_patch import instructions
from transfer_cj_to_plus import u32

SHOT_FLAG = 0x00040000
OLD_GATE = bytes.fromhex('9680e0 c4010aff ae 025a 03 b40000b45b 015a 025b f400ffff 9480 02e0')


def fix_facility_voice(raw):
    ais, terminator = lists(raw)
    codes = {ai:list(instructions(raw,start,LENGTHS)) for ai,(_,start) in ais.items()}
    used = 0
    for code in codes.values():
        for _,c in code:
            if c[0] in (0x9a,0x9b,0x9c): used |= int.from_bytes(c[1:5],'big')
    assert not used & SHOT_FLAG
    start = raw.find(OLD_GATE)
    assert start >= 0 and raw.find(OLD_GATE,start+1) < 0
    shots = [p for p,c in codes[0x417] if c == bytes.fromhex('18430806')]
    assert len(shots) == 2 and start == shots[1]+4
    assert sum(c==bytes.fromhex('c4010aff') for code in codes.values() for _,c in code) == 1
    editor = Editor(raw)
    editor.replace(start,start+len(OLD_GATE),b'',
        'Remove the skippable second-shot speech gate and its foreground timer reset')
    marker = b'\x9a'+struct.pack('>I',SHOT_FLAG)
    for p in shots:
        editor.insert(p+4,marker,'Latch that Tenpenny applied his scripted shot to Smoke')
    identity = next(i for i in range(0x1000,0x1100) if i not in ais)
    # A separate timer restores music without resetting Tenpenny's native AI.
    code = bytes.fromhex('02e0 03')+b'\x9c'+struct.pack('>I',SHOT_FLAG)+b'\xe1'
    code += bytes.fromhex('01e0 02e1 3043e2 3143e2 01e0 02e2 c4010aff ae 02e3 03 b40000b3e4 01e3 02e4 f400ffff 05fd0001 04')
    table = u32(raw,20)
    editor.insert(table,code,'One-shot watcher: Tenpenny shot marker plus Smoke dying/dead/absent')
    editor.insert(terminator,struct.pack('>II',0,identity),'Facility post-shot speech watcher table entry')
    out = bytearray(editor.finish())
    from transfer_cj_to_plus import put32
    put32(out,editor.mapped(terminator)-8,editor.before_insert(table))
    assert identity in lists(out)[0]
    return bytes(out), {'new_background_ai':f'{identity:04X}','Tenpenny_ai':'0417',
        'Smoke_character':67,'private_shot_flag':f'{SHOT_FLAG:08X}',
        'marker_after_both_native_Tenpenny_damage_commands':True,
        'requires_Tenpenny_shot_and_Smoke_dying_dead_or_absent':True,
        'sound_id':266,'recording':'Tenpenny Swear At Carl(1).wav',
        'plays_once':True,'music_restore_after_seconds':3.0,
        'native_Tenpenny_timer_no_longer_reset_by_speech':True,
        'recording_bytes_unchanged':True}
