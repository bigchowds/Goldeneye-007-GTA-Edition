"""Focused worst-case subtitle and post-shot speech fixtures."""
from pathlib import Path
import sys,json,struct,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import tec9_model_v18
from transfer_cj_to_plus import *
from cast_missions_v5 import Editor,lists,LENGTHS
from dam_patch import instructions
from scene_missions_v10 import intro_records


def make(version,stage,kind,marked=True):
    base=(ROOT/f'CJ_Scene_Audio_v{version}.z64').read_bytes();data,_=decode_cdata(base);_,table=read_table(data,0x261d4)
    out=bytearray(base);meta=bytearray(data);put32(meta,0x241a8-0x20d90,stage)
    name='UsetupcradZ' if kind=='captions' else 'UsetuparkZ'
    e=next(x for x in table if x['name']==name);end=table[e['id']+1]['address'];raw=rz_decode(base[e['address']:end]);ed=Editor(raw);ais,term=lists(raw)
    wait=bytes.fromhex('ec ae 02e0 03 b40001e0e1 01e0 02e1')
    if kind=='captions':
        report=json.loads((ROOT/'CJ_Scene_Audio_v10_Validation.json').read_text());ai=int(report['mission_changes']['UsetupcradZ']['retained_v9_changes']['cradle_intro']['audio_watcher_ai'],16)
        c=list(instructions(raw,ais[ai][1],LENGTHS));wrapper=wait+bytes.fromhex('c32417 c32418 05fd041d 04')
        ed.replace(c[0][0],c[-1][0]+1,wrapper,'Queue both final captions immediately before native falling cinema')
    else:
        for p,t,c in intro_records(raw):
            if t in (3,4,6):ed.replace(p,p+len(c),b'','Omit intro camera in controlled speech fixture')
            elif t==0:put32(ed.work,p+4,125)
        off=u32(raw,24)+125*44;struct.pack_into('>3f',ed.work,off+24,-1,0,0)
        c=list(instructions(raw,ais[0x417][1],LENGTHS))
        ed.replace(c[0][0],c[-1][0]+1,bytes.fromhex('05fd0001 04'),'Isolate watcher from native Tenpenny staging for controlled death fixture')
        code=wait+bytes.fromhex('18430806')+(bytes.fromhex('9a00040000') if marked else b'')
        code+=bytes.fromhex('03 18430806 05fd0001 04')
        ai=next(i for i in range(0x1000,0x1100) if i not in ais);at=u32(raw,20)
        ed.insert(at,code,'Controlled native shot and optional Tenpenny-shot marker')
        ed.insert(term,struct.pack('>II',0,ai),'Controlled fixture background entry')
    modified=bytearray(ed.finish())
    if kind!='captions':put32(modified,ed.mapped(term)-8,ed.before_insert(at))
    packed=rz_encode(modified);assert len(packed)<=end-e['address']
    out[e['address']:end]=packed+bytes(end-e['address']-len(packed))
    packed=rz_encode(meta,dense=True);assert len(packed)<=INFLATE_ROM-CDATA_ROM
    out[CDATA_ROM:INFLATE_ROM]=packed+bytes(INFLATE_ROM-CDATA_ROM-len(packed));crc=n64_crc(out);put32(out,16,crc[0]);put32(out,20,crc[1])
    path=ROOT/'boot-v6-research'/f'{kind}_{"marked" if marked else "unmarked"}_Probe_v{version}.z64';path.write_bytes(out)
    return {'path':str(path),'production_sha256':hashlib.sha256(base).hexdigest(),'probe_sha256':hashlib.sha256(out).hexdigest()}


if __name__=='__main__':
    results=[make(20,41,'captions'),make(21,41,'captions'),make(21,34,'facility'),make(21,34,'facility',False)]
    (ROOT/'boot-v6-research/final-probes-v21.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
