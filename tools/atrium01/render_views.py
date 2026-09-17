"""Render selected views from the saved scene without overwriting its camera state."""
import bpy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HOME=ROOT/'homes/atrium-01';s=bpy.context.scene
try:
    p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
    for d in p.devices:d.use=d.type=='METAL'
    s.cycles.device='GPU'
except Exception:pass
s.cycles.samples=96;s.render.resolution_x=1800;s.render.resolution_y=1238;s.render.resolution_percentage=100
views=[('02 Kitchen courtyard','02-kitchen-courtyard',False),('03 Atrium exterior','03-exterior',False),('04 Whole-home cutaway','04-cutaway',True)]
for name,file,cutaway in views:
    s.camera=bpy.data.objects[name]
    bpy.data.collections['09 Roof | hide for cutaway'].hide_render=cutaway
    bpy.data.collections['08 Structure | exposed fir'].hide_render=cutaway
    s.render.filepath=str(HOME/'renders'/f'{file}.png');bpy.ops.render.render(write_still=True)
    print('RENDER_SAVED',file,flush=True)
