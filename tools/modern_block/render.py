"""Render saved cameras into ignored review work, preserving the canonical native file."""
import bpy,sys,argparse,math
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--views',nargs='+');p.add_argument('--draft',action='store_true');p.add_argument('--samples',type=int,default=96);a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=20 if a.draft else a.samples;s.cycles.use_denoising=True
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
 prefs.compute_device_type='METAL';prefs.get_devices()
 for dev in prefs.devices:dev.use=dev.type=='METAL'
 s.cycles.device='GPU'
except Exception:s.cycles.device='CPU'
s.render.resolution_percentage=50 if a.draft else 100
home=Path(bpy.data.filepath).parent.parent
for v in a.views or sorted(o.name for o in s.objects if o.type=='CAMERA'):
 for o in s.objects:
  if o.name.startswith('Pivot screen '):o.rotation_euler.z=0 if v=='09-lanai-closed' else math.radians(75)
 s.view_settings.exposure=1.65 if v=='11-stair-gallery' else 0
 s.camera=bpy.data.objects[v];s.render.filepath=str(home/'outputs/work'/f'{v}.png');bpy.ops.render.render(write_still=True);print('RENDERED',v,flush=True)
