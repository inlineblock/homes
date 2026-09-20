"""Render saved cameras into ignored review work, preserving the canonical native file."""
import bpy,sys,argparse,math,json
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
root=home.parent.parent
closed={o.name:o.instance_collection for o in s.objects if o.instance_type=='COLLECTION' and o.get('asset_id')}
open_cache={}
def operation_state(obj, opened):
 if not opened:
  obj.instance_collection=closed[obj.name]
  return
 asset_id=obj['asset_id'];version=obj.get('asset_version','v001')
 if asset_id not in open_cache:
  folder=root/'library'/asset_id/version
  meta=json.loads((folder/'asset.json').read_text())
  coll=meta['blender']['operating_collections']['open']
  with bpy.data.libraries.load(str(folder/meta['files']['blender']),link=True) as (source,target):
   assert coll in source.collections,(asset_id,coll)
   target.collections=[coll]
  open_cache[asset_id]=target.collections[0]
 obj.instance_collection=open_cache[asset_id]
for v in a.views or sorted(o.name for o in s.objects if o.type=='CAMERA'):
 for o in s.objects:
  if o.name.startswith('Pivot screen '):o.rotation_euler.z=0 if v=='09-lanai-closed' else math.radians(75)
  if o.name in closed:
   opened=(v=='15-kitchen-open' and o.name.startswith(('Kitchen concealed dishwasher','Kitchen concealed refrigeration','Kitchen cream brass range')))
   opened=opened or (v=='16-kitchen-island' and o.name in ('Kitchen island microwave','Kitchen island waste and recycling'))
   opened=opened or (v=='17-pantry-open' and o.name in ('Pantry appliance garage','Pantry enclosed food storage'))
   operation_state(o,opened)
 s.view_settings.exposure=1.65 if v=='11-stair-gallery' else 0
 s.camera=bpy.data.objects[v];s.render.filepath=str(home/'outputs/work'/f'{v}.png');bpy.ops.render.render(write_still=True);print('RENDERED',v,flush=True)
