"""v21: clear old ending captions and repair the Facility post-shot voice."""
from pathlib import Path
import hashlib
import json
import tec9_model_v18  # Existing source-pack import compatibility.
from scene_missions_v21 import fix_facility_voice
from ending_caption_v21 import caption_reset_stub
from transfer_cj_to_plus import CDATA_ROM, INFLATE_ROM, decode_cdata, n64_crc, put32, read_table, rz_decode, rz_encode, u32
from build_scene_audio_v14 import IMAGE_BASE, TEXTURE_TABLE
import menu_audio

ROOT = Path(__file__).resolve().parent
BASE_SHA = '7131514668c20a36216ee2fc2dec12117873c6b7c9593fb3b938f685ffccd6b9'


def resource(rom, table, name):
    entry = next(e for e in table if e['name'] == name)
    return rz_decode(rom[entry['address']:table[entry['id']+1]['address']])


def main():
    base = (ROOT/'CJ_Scene_Audio_v20.z64').read_bytes()
    assert hashlib.sha256(base).hexdigest() == BASE_SHA
    prior = json.loads((ROOT/'CJ_Scene_Audio_v20_Validation.json').read_text())
    data, _ = decode_cdata(base); table_base, table = read_table(data, 0x261d4)
    meta = bytearray(data)
    scene, scene_report = fix_facility_voice(resource(base, table, 'UsetuparkZ'))
    replacements = {'UsetuparkZ': scene}
    caption_stub, caption_report = caption_reset_stub(base,prior['voice_audio'])
    images = []; cursor = IMAGE_BASE
    for i in range(2732):
        size = u32(data, TEXTURE_TABLE+8*i)&0xffffff
        blob = base[cursor:cursor+size]; cursor += size
        images.append(blob)
    images_blob = b''.join(images); bank_start = menu_audio.align(IMAGE_BASE+len(images_blob))
    bank = bytearray()
    for item, nxt in zip(table[1:-1], table[2:]):
        put32(meta, table_base+12*item['id']+8, bank_start+len(bank))
        if item['name'] in replacements:
            part = rz_encode(replacements[item['name']]); part += b'\0'*(-len(part)%16)
        else: part = base[item['address']:nxt['address']]
        bank.extend(part)
    bank_end = bank_start+len(bank)
    put32(meta, table_base+12*table[-1]['id']+8, bank_end)
    music_old, voice_old = prior['music_audio'], prior['voice_audio']
    dest = menu_audio.align(bank_end); delta = dest-music_old['control_rom_start']
    audio = bytearray(base[music_old['control_rom_start']:voice_old['appended_region_end']])
    stub_at = voice_old['control_rom_start']-music_old['control_rom_start']+voice_old['respect_music_stub_offset']
    audio[stub_at:stub_at+len(caption_stub)] = caption_stub
    assert dest+len(audio) < len(base)
    out = bytearray(base); out[IMAGE_BASE:] = b'\xff'*(len(out)-IMAGE_BASE)
    out[IMAGE_BASE:IMAGE_BASE+len(images_blob)] = images_blob
    out[bank_start:bank_end] = bank; out[dest:dest+len(audio)] = audio
    for hi, lo, key in ((0x76b4,0x76bc,'control_rom_start'),(0x76ec,0x76f4,'control_rom_start'),
            (0x76b0,0x76c0,'sample_table_rom_start'),(0x7704,0x7708,'sample_table_rom_start')):
        menu_audio.patch_address(out, hi, lo, music_old[key], music_old[key]+delta)
    seq = menu_audio.MUSIC_TABLE+4+23*8; put32(out,seq,u32(base,seq)+delta)
    for hi, lo, key in ((0x7658,0x765c,'control_rom_start'),(0x7654,0x7660,'control_rom_end'),
            (0x7684,0x768c,'control_rom_start')):
        menu_audio.patch_address(out,hi,lo,voice_old[key],voice_old[key]+delta)
    voice = json.loads(json.dumps(voice_old)); control = voice_old['control_rom_start']+delta
    for rec in voice['voice_records']+voice['enemy_hurt_records']+[voice['new_native_gunshot_record']]:
        at = control+rec['wave_offset']; put32(out,at,u32(out,at)+delta)
        rec['sample_rom_start'] += delta; rec['sample_rom_end'] += delta
    for key in ('control_rom_start','control_rom_end','appended_region_end'): voice[key] += delta
    music = json.loads(json.dumps(music_old))
    for key in ('control_rom_start','control_rom_end','sample_table_rom_start','new_sample_rom_start',
            'new_sample_rom_end','sequence_rom_start','appended_region_end'):
        if key in music: music[key] += delta
    packed = rz_encode(meta,dense=True); assert len(packed) <= INFLATE_ROM-CDATA_ROM
    out[CDATA_ROM:INFLATE_ROM] = packed+b'\0'*(INFLATE_ROM-CDATA_ROM-len(packed))
    crc = n64_crc(out); put32(out,16,crc[0]); put32(out,20,crc[1])
    assert len(out) == 0x2000000 and decode_cdata(out)[0] == meta
    (ROOT/'CJ_Scene_Audio_v21.z64').write_bytes(out)
    report = {'base_rom':'CJ_Scene_Audio_v20.z64','base_sha256':BASE_SHA,
        'output_sha256':hashlib.sha256(out).hexdigest(),'crc1':f'{crc[0]:08X}','crc2':f'{crc[1]:08X}',
        'modified_resources':sorted(replacements),'modified_textures':[],
        'Facility_post_shot_voice':scene_report,'Cradle_caption_reset':caption_report,
        'audio_relocation_bytes_from_v20':delta,'music_audio':music,'voice_audio':voice,
        'native_ZMG_Phantom_changes_retained':True,'Streets_setup_untouched':True,
        'Project64_runtime_confirmation':'pending user test'}
    (ROOT/'CJ_Scene_Audio_v21_Validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('output_sha256','modified_resources','modified_textures','Facility_post_shot_voice','Cradle_caption_reset')},indent=2))


if __name__ == '__main__': main()
