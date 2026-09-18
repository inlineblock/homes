"""Render current Mountain cameras into ignored review outputs, never save view state."""
import bpy,sys,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from design import VIEWS
s=bpy.context.scene;p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';sample_override=os.environ.get('MOUNTAIN_SAMPLES');s.render.resolution_percentage=int(os.environ.get('MOUNTAIN_PERCENT',100))
out=Path(__file__).resolve().parents[2]/'homes/mountain-house/outputs/work';out.mkdir(parents=True,exist_ok=True)
requested=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
for cam,name in VIEWS:
    if requested and name not in requested:continue
    s.cycles.samples=int(sample_override) if sample_override else (256 if name[:2] in {'01','02','03','04','05'} else 512)
    for n in s.world.node_tree.nodes:
        if n.type=='TEX_SKY':n.sun_rotation=__import__('math').radians(205 if name=='02-road-arrival' else 65)
    s.camera=bpy.data.objects[cam];s.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('MOUNTAIN_RENDERED',name,flush=True)
