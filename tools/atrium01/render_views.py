"""Render named views into ignored work; review before promotion. Never save render states."""
import bpy,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HOME=ROOT/'homes/atrium-01';s=bpy.context.scene
out=HOME/'outputs/work';out.mkdir(parents=True,exist_ok=True)
try:
    p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
    for d in p.devices:d.use=d.type=='METAL'
    s.cycles.device='GPU'
except Exception:pass
s.cycles.samples=int(os.getenv('ATRIUM_SAMPLES','96'));s.render.resolution_x=1800;s.render.resolution_y=1238;s.render.resolution_percentage=int(os.getenv('ATRIUM_PERCENT','100'))
views=[('01 Kitchen hero','01-kitchen',False),('02 Kitchen courtyard','02-kitchen-courtyard',False),('03 Atrium exterior','03-exterior',False),('04 Whole-home cutaway','04-cutaway',True),('05 Rear terrace','05-rear-terrace',False),('06 West roof and atrium','06-west-roof-atrium',False),('07 Open-air atrium','07-open-air-atrium',False)]
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if args:
    byfile={v[1]:v for v in views};views=[byfile[a] for a in args]
for name,file,cutaway in views:
    s.camera=bpy.data.objects[name]
    bpy.data.collections['09 Roof | hide for cutaway'].hide_render=cutaway
    bpy.data.collections['08 Structure | exposed fir'].hide_render=cutaway
    s.render.filepath=str(out/f'{file}.png');bpy.ops.render.render(write_still=True)
    print('RENDER_SAVED',file,flush=True)
