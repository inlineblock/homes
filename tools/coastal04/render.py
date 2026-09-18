"""Render named opening states to ignored review drafts. Never save transient state."""
import bpy,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
from design import VIEWS
s=bpy.context.scene
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.samples=int(os.environ.get('COASTAL_SAMPLES',s.cycles.samples));s.render.resolution_percentage=int(os.environ.get('COASTAL_PERCENT','100'))
out=ROOT/'homes/coastal-house/outputs/work';out.mkdir(parents=True,exist_ok=True)
requested=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
unknown=set(requested)-{v[1] for v in VIEWS}
if unknown:raise ValueError('Unknown Coastal render names: '+', '.join(sorted(unknown)))
views=[next(v for v in VIEWS if v[1]==name) for name in requested] if requested else VIEWS
for cam,file,frame in views:
    s.cycles.samples=int(os.environ.get('COASTAL_SAMPLES',256 if file in {'05-terrace-closed','06-front-arrival','07-roof-and-parking','08-west-garden'} else 512))
    s.frame_set(frame);s.camera=bpy.data.objects[cam];s.render.filepath=str(out/(file+'.png'));bpy.ops.render.render(write_still=True);print('COASTAL_RENDERED',file,flush=True)
