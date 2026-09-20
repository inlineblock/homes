"""Render reviewed-candidate cameras only; never overwrite canonical model."""
import argparse,sys,os,math,json,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from design import VIEWS,SLUG
p=argparse.ArgumentParser();p.add_argument('views',nargs='*');p.add_argument('--samples',type=int,default=128);p.add_argument('--width',type=int,default=1800);p.add_argument('--cpu',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
s=bpy.context.scene
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='METAL'
 s.cycles.device='GPU'
except Exception:s.cycles.device='CPU'
if a.cpu:s.cycles.device='CPU';s.render.threads_mode='FIXED';s.render.threads=8
s.render.resolution_x=a.width;s.render.resolution_y=round(a.width*2/3);s.render.resolution_percentage=100;s.cycles.samples=a.samples
out=Path(__file__).resolve().parents[2]/'homes'/SLUG/'outputs/work';out.mkdir(parents=True,exist_ok=True)
receipt_path=out/'render-receipt.json'
receipt=json.loads(receipt_path.read_text()) if receipt_path.exists() else {'views':{}}
digest=lambda path:hashlib.sha256(Path(path).read_bytes()).hexdigest()
for name in a.views or VIEWS:
 if name not in VIEWS:raise ValueError(name)
 originals={}
 if name in {'08-primary-bath','12-east-bath'}:
  prefix='West' if name=='08-primary-bath' else 'East'
  for door in s.objects:
   if door.name.startswith(prefix+' bedroom services open door') and 'hinge_xy_ft' in door and door['hinge_xy_ft'][0]>(8 if prefix=='West' else 56):
    old=door.matrix_world.copy();originals[door.name]=old;hx,hy=door['hinge_xy_ft'];a=door['closed_angle'];w=door['door_width_ft']
    door.rotation_euler.z=a;door.location.x=(hx+math.cos(a)*w/2)*.3048;door.location.y=(hy+math.sin(a)*w/2)*.3048
    bpy.context.view_layer.update();delta=door.matrix_world@old.inverted()
    # Existing frozen native has tagged levers but an untagged bespoke spindle.
    # Move the complete latch assembly for this photographic door state.
    door_base,door_suffix=door.name.split(' open door',1)
    spindle_name=door_base+' conceptual latch spindle'+door_suffix
    for handle in [h for h in s.objects if h.get('door_owner')==door.name or h.name==spindle_name]:
     originals[handle.name]=handle.matrix_world.copy();handle.matrix_world=delta@handle.matrix_world
 s.camera=bpy.data.objects[name]
 if name=='13-dressing':
  # Photographic position beyond the open entry leaf; canonical camera stays saved.
  originals[s.camera.name]=s.camera.matrix_world.copy()
  s.camera.location=Vector((4.05,18.2,5.5))*.3048
  s.camera.rotation_euler=(Vector((4.05,27,4.6))*.3048-s.camera.location).to_track_quat('-Z','Y').to_euler()
 s.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
 bpy.context.view_layer.update()
 receipt['views'][name]={'native_sha256':digest(bpy.data.filepath),'render_script_sha256':digest(__file__),'image_sha256':digest(s.render.filepath),'camera_matrix_world_m':[list(row) for row in s.camera.matrix_world],'camera_lens_mm':s.camera.data.lens,'samples':s.cycles.samples,'resolution':[s.render.resolution_x,s.render.resolution_y],'transient_camera_override':name=='13-dressing','transient_closed_bath_door':name in {'08-primary-bath','12-east-bath'},'native_saved':False}
 receipt_path.write_text(json.dumps(receipt,indent=2)+'\n')
 for key,transform in originals.items():bpy.data.objects[key].matrix_world=transform
 print('TWIN_RENDER_READY',name,flush=True)
