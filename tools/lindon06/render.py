"""Render named cameras from saved current geometry into ignored QA work."""
import bpy,sys,argparse
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--views',nargs='+');parser.add_argument('--draft',action='store_true');parser.add_argument('--samples',type=int,default=128)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
home=Path(__file__).resolve().parents[2]/'homes/lindon-brick-house';scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.samples=24 if args.draft else args.samples;scene.cycles.use_denoising=True
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
    prefs.compute_device_type='METAL';prefs.get_devices()
    for d in prefs.devices:d.use=d.type=='METAL'
    scene.cycles.device='GPU'
except Exception:scene.cycles.device='CPU'
scene.render.resolution_percentage=50 if args.draft else 100
views=args.views or sorted(o.name for o in scene.objects if o.type=='CAMERA' and o.name[:2].isdigit())
for view in views:
    scene.camera=bpy.data.objects[view]
    scene.render.filepath=str(home/'outputs/work'/f'{view}.png')
    bpy.ops.render.render(write_still=True)
    print('LINDON_RENDERED',view,flush=True)
