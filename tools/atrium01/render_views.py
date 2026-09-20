"""Render stable camera names into ignored work; never save temporary view states."""
import bpy,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HOME=ROOT/'homes/atrium-01';s=bpy.context.scene
out=HOME/'outputs/work';out.mkdir(parents=True,exist_ok=True)
try:
    p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
    for d in p.devices:d.use=d.type=='METAL'
    s.cycles.device='GPU'
except Exception:pass
s.cycles.samples=int(os.getenv('ATRIUM_SAMPLES','64'))
s.render.resolution_x=1600;s.render.resolution_y=1100;s.render.resolution_percentage=int(os.getenv('ATRIUM_PERCENT','100'))
views=sorted(o.name for o in s.objects if o.type=='CAMERA')
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if args:views=args
for name in views:
    s.camera=bpy.data.objects[name]
    cutaway=name=='04-cutaway'
    for coll in bpy.data.collections:
        if coll.name.startswith(('09 Roof','08 Structure')):coll.hide_render=cutaway
    for obj in s.objects:
        if obj.get('shade_state')=='open':obj.hide_render=name=='14-primary-privacy'
        elif obj.get('shade_state')=='closed':
            obj.hide_render=name!='14-primary-privacy';obj.hide_viewport=name!='14-primary-privacy'
    s.render.filepath=str(out/f'{name}.png');bpy.ops.render.render(write_still=True)
    print('RENDER_SAVED',name,flush=True)
