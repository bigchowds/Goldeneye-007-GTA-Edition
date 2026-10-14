#!/usr/bin/env python3
"""Compare full-ROM startup with Mupen64Plus using its bundled C API."""
from pathlib import Path
import argparse, ctypes as C, json, threading, time, hashlib

ROOT=Path(__file__).resolve().parents[1]
BUNDLE=ROOT/'emulator-research/mupen64plus-bundle-mupen64plus-bundle-linux64-ubuntu22'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('rom');ap.add_argument('--seconds',type=float,default=8)
    ap.add_argument('--memory',type=int,choices=(4,8),default=8);ap.add_argument('--mode',type=int,default=2)
    ap.add_argument('--video',action='store_true')
    ap.add_argument('--input',action='store_true')
    ap.add_argument('--start',action='store_true')
    ap.add_argument('--test-input',action='store_true')
    ap.add_argument('--events',type=Path)
    ap.add_argument('--load',type=Path)
    ap.add_argument('--tag',default='scene-test')
    ap.add_argument('--facility',action='store_true')
    ap.add_argument('--audio',action='store_true')
    ap.add_argument('--capture-every',type=int,default=300)
    ap.add_argument('--checkpoints',default='')
    args=ap.parse_args();rom=Path(args.rom).resolve()
    folder=Path(__file__).resolve().parent/(args.tag+f'-{args.memory}MB-mode{args.mode}'+('-video' if args.video else '')+('-input' if args.input else '')+('-start' if args.start else ''))
    folder.mkdir(exist_ok=True);config=folder/'config';config.mkdir(exist_ok=True)
    record={'rom':rom.name,'sha256':hashlib.sha256(rom.read_bytes()).hexdigest(),
            'rdram_mb':args.memory,'cpu_mode':args.mode,'messages':[],'states':[],'frames':0,'scene_audit':[]}
    save_done=threading.Event()
    events=json.loads(args.events.read_text()) if args.events else {}
    checkpoints={int(x) for x in args.checkpoints.split(',') if x}
    record['checkpoints']=[]
    LOG=C.CFUNCTYPE(None,C.c_void_p,C.c_int,C.c_char_p)
    STATE=C.CFUNCTYPE(None,C.c_void_p,C.c_int,C.c_int)
    FRAME=C.CFUNCTYPE(None,C.c_uint)
    @LOG
    def log(ctx,level,msg):
        text=msg.decode(errors='replace');record['messages'].append([level,text])
        if level<=3:print(level,text,flush=True)
    @STATE
    def state(ctx,param,value):
        record['states'].append([param,value])
        if param==11:save_done.set()
    @FRAME
    def frame(index):
        record['frames']=int(index)
        if gfx is not None and int(index)%15==0:
            try:
                import array,sys,struct
                sys.path.insert(0,str(ROOT))
                from runtime_helpers_v12 import voices
                from transfer_cj_to_plus import u32
                pointer=lib.DebugMemGetPointer(1)
                if pointer:
                    values=array.array('I');values.frombytes(C.string_at(pointer,0x800000));values.byteswap();ram=values.tobytes()
                    active=voices(ram)
                    entry={'frame':int(index),'clock':u32(ram,0x492bc),'stage':u32(ram,0x241a8),'top_queue':u32(ram,0x3751c),'top_timer':struct.unpack_from('>i',ram,0x37520)[0],'top_flags':u32(ram,0x37524),'sounds':[v for v in active if v['sound_id'] in (266,282,296)]}
                    actors_base=u32(ram,0x2d8b4)&0x7fffff;actors_count=u32(ram,0x2d8b8)
                    if 0<actors_count<400:
                        for i in range(actors_count):
                            q=actors_base+i*0x1dc
                            if struct.unpack_from('>h',ram,q)[0]==67:
                                entry['Smoke_action']=ram[q+7]
                    record['scene_audit'].append(entry)
            except Exception as error:
                if 'scene_audit_initial_note' not in record:record['scene_audit_initial_note']=str(error)
        if args.facility and int(index)==1800:
            C.c_uint32.from_address(C.c_void_p.in_dll(gfx, 'g_pRDRAM').value+0x24304).value = 0x22
            print('FORCE FACILITY stage transition',flush=True)
        if args.test_input and str(index) in events:
            inp.TestSetKeys(events[str(index)])
            print('INPUT',index,events[str(index)],flush=True)
        if args.start:
            if int(index) in (90,300,600,1200,1800,2400,3000):lib.CoreDoCommand(13,13,None)
            if int(index) in (96,306,606,1206,1806,2406,3006):lib.CoreDoCommand(14,13,None)
        if int(index) in checkpoints:
            filename=C.create_string_buffer(str(folder/f'checkpoint-{index}.st').encode())
            result=lib.CoreDoCommand(11,1,filename)
            record['checkpoints'].append({'frame':int(index),'save_return':result})
        if int(index)%args.capture_every==0 and gfx is not None:
            width,height=C.c_int(),C.c_int()
            gfx.ReadScreen2(None,C.byref(width),C.byref(height),0)
            if width.value>0 and height.value>0:
                pixels=C.create_string_buffer(width.value*height.value*3)
                gfx.ReadScreen2(pixels,C.byref(width),C.byref(height),0)
                from PIL import Image
                captured=Image.frombytes('RGB',(width.value,height.value),pixels.raw).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                captured.save(folder/f'frame-{index}.png')
                record['frame_capture']=int(index)
    lib=C.CDLL(str(BUNDLE/'libmupen64plus.so.2.0.0'),mode=C.RTLD_GLOBAL)
    lib.CoreStartup.argtypes=[C.c_int,C.c_char_p,C.c_char_p,C.c_void_p,LOG,C.c_void_p,STATE]
    lib.CoreDoCommand.argtypes=[C.c_int,C.c_int,C.c_void_p]
    lib.DebugMemWrite32.argtypes=[C.c_uint,C.c_uint]
    lib.DebugMemGetPointer.argtypes=[C.c_int]
    lib.DebugMemGetPointer.restype=C.c_void_p
    lib.ConfigOpenSection.argtypes=[C.c_char_p,C.POINTER(C.c_void_p)]
    lib.ConfigSetParameter.argtypes=[C.c_void_p,C.c_char_p,C.c_int,C.c_void_p]
    lib.CoreAttachPlugin.argtypes=[C.c_int,C.c_void_p]
    def check(code,what):
        if code:raise RuntimeError(f'{what}: {code}')
    check(lib.CoreStartup(0x020001,str(config).encode(),str(BUNDLE).encode(),None,log,None,state),'startup')
    handle=C.c_void_p();check(lib.ConfigOpenSection(b'Core',C.byref(handle)),'config open')
    for key,kind,value in [('R4300Emulator',1,args.mode),('DisableExtraMem',3,int(args.memory==4)),
                           ('EnableDebugger',3,0),('CountPerOp',1,2)]:
        v=C.c_int(value);check(lib.ConfigSetParameter(handle,key.encode(),kind,C.byref(v)),key)
    image=C.create_string_buffer(rom.read_bytes());check(lib.CoreDoCommand(1,len(image)-1,image),'ROM open')
    rsp=C.CDLL(str(BUNDLE/'mupen64plus-rsp-hle.so'))
    rsp.PluginStartup.argtypes=[C.c_void_p,C.c_void_p,LOG]
    check(rsp.PluginStartup(C.c_void_p(lib._handle),None,log),'RSP startup')
    gfx=None
    if args.video:
        gfx=C.CDLL(str(BUNDLE/'mupen64plus-video-glide64mk2.so'))
        gfx.PluginStartup.argtypes=[C.c_void_p,C.c_void_p,LOG]
        gfx.ReadScreen2.argtypes=[C.c_void_p,C.POINTER(C.c_int),C.POINTER(C.c_int),C.c_int]
        check(gfx.PluginStartup(C.c_void_p(lib._handle),None,log),'graphics startup')
        check(lib.CoreAttachPlugin(2,C.c_void_p(gfx._handle)),'attach graphics')
    aud=None
    if args.audio:
        aud=C.CDLL(str(BUNDLE/'mupen64plus-audio-sdl.so'))
        aud.PluginStartup.argtypes=[C.c_void_p,C.c_void_p,LOG]
        check(aud.PluginStartup(C.c_void_p(lib._handle),None,log),'audio startup')
        check(lib.CoreAttachPlugin(3,C.c_void_p(aud._handle)),'attach audio')
    inp=None
    if args.input:
        inp=C.CDLL(str(Path(__file__).resolve().parent/'test_input.so' if args.test_input else BUNDLE/'mupen64plus-input-sdl.so'))
        inp.PluginStartup.argtypes=[C.c_void_p,C.c_void_p,LOG]
        check(inp.PluginStartup(C.c_void_p(lib._handle),None,log),'input startup')
        check(lib.CoreAttachPlugin(4,C.c_void_p(inp._handle)),'attach input')
    check(lib.CoreAttachPlugin(1,C.c_void_p(rsp._handle)),'attach RSP')
    check(lib.CoreDoCommand(15,0,C.cast(frame,C.c_void_p)),'frame callback')
    if args.load:
        name=C.create_string_buffer(str(args.load.resolve()).encode())
        check(lib.CoreDoCommand(10,0,name),'load state')
    execution={}
    def execute():execution['return']=lib.CoreDoCommand(5,0,None)
    worker=threading.Thread(target=execute);worker.start()
    time.sleep(.2)
    if inp is not None and not args.test_input:
        ih=C.c_void_p();lib.ConfigOpenSection(b'Input-SDL-Control1',C.byref(ih))
        lib.ConfigGetParamString.argtypes=[C.c_void_p,C.c_char_p];lib.ConfigGetParamString.restype=C.c_char_p
        record['start_binding']=lib.ConfigGetParamString(ih,b'Start').decode(errors='replace')
    limiter=C.c_int(0);lib.CoreDoCommand(17,5,C.byref(limiter))
    deadline=time.monotonic()+args.seconds
    while time.monotonic()<deadline and worker.is_alive():time.sleep(.1)
    saved=folder/'startup.st';saved_name=C.create_string_buffer(str(saved).encode())
    if worker.is_alive():
        save_done.clear()
        record['save_request_return']=lib.CoreDoCommand(11,1,saved_name)
        save_done.wait(4)
        record['save_complete']=save_done.is_set()
        if gfx is not None and save_done.is_set():
            gfx.ReadScreen2.argtypes=[C.c_void_p,C.POINTER(C.c_int),C.POINTER(C.c_int),C.c_int]
            width,height=C.c_int(),C.c_int();gfx.ReadScreen2(None,C.byref(width),C.byref(height),0)
            record['screen_size']=[width.value,height.value]
            if width.value>0 and height.value>0:
                pixels=C.create_string_buffer(width.value*height.value*3)
                gfx.ReadScreen2(pixels,C.byref(width),C.byref(height),0)
                from PIL import Image
                image=Image.frombytes('RGB',(width.value,height.value),pixels.raw).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                image.save(folder/'startup.png')
        record['stop_return']=lib.CoreDoCommand(6,0,None)
        worker.join(4)
    record['execution']=execution;record['worker_alive']=worker.is_alive()
    record['saved_bytes']=saved.stat().st_size if saved.exists() else 0
    (folder/'run.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:record[k] for k in ('rom','rdram_mb','frames','execution','saved_bytes','worker_alive')},indent=2))
    if worker.is_alive():
        import os
        os._exit(3)
    if saved.exists():
        import gzip,array
        try:
            raw=gzip.decompress(saved.read_bytes())
        except (EOFError, OSError) as error:
            record['savestate_parse_note']=f'Asynchronous save incomplete at shutdown: {error}'
        else:
            ram=array.array('I'); ram.frombytes(raw[0x1bc:0x1bc+0x800000]); ram.byteswap()
            (folder/'ram.bin').write_bytes(ram.tobytes())
    lib.CoreDoCommand(2,0,None);lib.CoreDetachPlugin(1);rsp.PluginShutdown()
    if gfx is not None:lib.CoreDetachPlugin(2);gfx.PluginShutdown()
    if inp is not None:lib.CoreDetachPlugin(4);inp.PluginShutdown()
    if aud is not None:lib.CoreDetachPlugin(3);aud.PluginShutdown()
    lib.CoreShutdown()

if __name__=='__main__':main()
