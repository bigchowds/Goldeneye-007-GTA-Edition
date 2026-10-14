"""Verify the final caption reset and post-shot voice without other changes."""
from pathlib import Path
import hashlib,json
import tec9_model_v18
from transfer_cj_to_plus import *
from cast_missions_v5 import lists,LENGTHS
from dam_patch import instructions
from build_cast_v1 import props,PROP_WORDS
from scene_missions_v21 import OLD_GATE,SHOT_FLAG
from ending_caption_v21 import caption_reset_stub
from build_scene_audio_v14 import IMAGE_BASE,TEXTURE_TABLE
import menu_audio
ROOT=Path(__file__).resolve().parent


def main():
    old=(ROOT/'CJ_Scene_Audio_v20.z64').read_bytes();new=(ROOT/'CJ_Scene_Audio_v21.z64').read_bytes()
    path=ROOT/'CJ_Scene_Audio_v21_Validation.json';report=json.loads(path.read_text())
    prior=json.loads((ROOT/'CJ_Scene_Audio_v20_Validation.json').read_text())
    assert hashlib.sha256(old).hexdigest()==report['base_sha256']
    assert hashlib.sha256(new).hexdigest()==report['output_sha256']
    assert len(old)==len(new)==0x2000000 and n64_crc(new)==(u32(new,16),u32(new,20))
    od,_=decode_cdata(old);nd,_=decode_cdata(new);tb,ot=read_table(od,0x261d4);_,nt=read_table(nd,0x261d4)
    assert [x['name'] for x in ot]==[x['name'] for x in nt]
    unchanged=0
    for a,b,an,bn in zip(ot[1:-1],nt[1:-1],ot[2:],nt[2:]):
        x=old[a['address']:an['address']];y=new[b['address']:bn['address']]
        if a['name']!='UsetuparkZ':assert x==y,a['name'];unchanged+=1
        else:before,after=rz_decode(x),rz_decode(y)
    oa,na=lists(before)[0],lists(after)[0];watch=int(report['Facility_post_shot_voice']['new_background_ai'],16)
    assert set(na)==set(oa)|{watch} and watch>=0x1000
    gate=before.index(OLD_GATE);marker=b'\x9a'+SHOT_FLAG.to_bytes(4,'big')
    for identity in oa:
        want=[]
        for p,c in instructions(before,oa[identity][1],LENGTHS):
            if identity==0x417 and gate<=p<gate+len(OLD_GATE):continue
            want.append(c)
            if identity==0x417 and c==bytes.fromhex('18430806'):want.append(marker)
        assert [c for _,c in instructions(after,na[identity][1],LENGTHS)]==want,hex(identity)
    w=[c for _,c in instructions(after,na[watch][1],LENGTHS)]
    assert w.count(bytes.fromhex('c4010aff'))==1
    assert b'\x9c'+SHOT_FLAG.to_bytes(4,'big')+b'\xe1' in w
    assert bytes.fromhex('3043e2') in w and bytes.fromhex('3143e2') in w
    assert w[-2:]==[bytes.fromhex('05fd0001'),b'\x04']
    assert sum(c==bytes.fromhex('c4010aff') for _,s in na.values() for _,c in instructions(after,s,LENGTHS))==1
    op,np_=list(props(before)),list(props(after));assert len(op)==len(np_)
    for (p,t),(q,ty) in zip(op,np_):assert t==ty and before[p:p+4*PROP_WORDS[t]]==after[q:q+4*PROP_WORDS[t]]
    permitted={tb+12*i+j for i in range(1,len(ot)) for j in range(8,12)}
    assert all(i in permitted for i,(a,b) in enumerate(zip(od,nd)) if a!=b)
    p=q=IMAGE_BASE
    for i in range(2732):
        a=u32(od,TEXTURE_TABLE+i*8)&0xffffff;b=u32(nd,TEXTURE_TABLE+i*8)&0xffffff
        assert a==b and old[p:p+a]==new[q:q+b];p+=a;q+=b
    m,v=prior['music_audio'],prior['voice_audio'];delta=report['audio_relocation_bytes_from_v20']
    a=bytearray(old[m['control_rom_start']:v['appended_region_end']])
    b=bytearray(new[m['control_rom_start']+delta:v['appended_region_end']+delta])
    for rec in v['voice_records']+v['enemy_hurt_records']+[v['new_native_gunshot_record']]:
        at=v['control_rom_start']-m['control_rom_start']+rec['wave_offset'];assert u32(b,at)==u32(a,at)+delta;b[at:at+4]=a[at:at+4]
    offset=v['control_rom_start']-m['control_rom_start']+v['respect_music_stub_offset']
    expected,_=caption_reset_stub(old,v);assert b[offset:offset+224]==expected
    b[offset:offset+224]=a[offset:offset+224];assert a==b
    assert report['voice_audio']['control_rom_end']-report['voice_audio']['control_rom_start']==v['control_rom_end']-v['control_rom_start']
    allowed=set(range(16,24))|set(range(CDATA_ROM,INFLATE_ROM))
    for p in (0x76b4,0x76bc,0x76ec,0x76f4,0x76b0,0x76c0,0x7704,0x7708,
              0x7658,0x765c,0x7654,0x7660,0x7684,0x768c,menu_audio.MUSIC_TABLE+4+23*8):allowed.update(range(p,p+4))
    assert all(i in allowed for i,(a,b) in enumerate(zip(old[:IMAGE_BASE],new[:IMAGE_BASE])) if a!=b)
    report['focused_validation']={'valid_N64_checksum_and_32MiB_size':True,
        'Cradle_setup_and_all_cutscene_timing_byte_exact_v20':True,
        'native_queue_reset_before_reward':True,'caption_reset_only_for_sound_296':True,
        'caption_wrapper_fits_same_224_byte_reservation':True,'no_audio_heap_growth':True,
        'Tenpenny_recording_retained':True,'both_native_shots_latch_marker':True,
        'voice_requires_marker_and_Smoke_death':True,'voice_once_in_new_watcher':True,
        'native_Facility_AI_other_than_voice_marker_edits_preserved':True,
        'all_character_and_weapon_props_preserved':True,'all_2732_textures_byte_exact':True,
        'all_recorded_samples_and_other_audio_code_preserved':True,
        'other_resource_chunks_byte_exact':unchanged,'Streets_setup_byte_exact':True}
    path.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['focused_validation'],indent=2))


if __name__=='__main__':main()
