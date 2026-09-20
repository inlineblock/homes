"""Derive a closed, genuinely shelved linen cupboard from published oak wardrobe.

blender -b --factory-startup --python tools/library/publish_oak_linen_cabinet.py
blender -b --factory-startup --python tools/library/publish_oak_linen_cabinet.py -- --verify --render
"""
from pathlib import Path
import bpy, hashlib, json, math, sys
from mathutils import Matrix, Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'tools/library'))
from common import geometry as g
from publish_modern_block import bounds, linked_mat, box
SLUG='oak-linen-cabinet-2ft';ID='cabinetry/'+SLUG;NAME='Closed oak linen cabinet 2ft | v001'
FOLDER=ROOT/'library'/ID/'v001';NATIVE=FOLDER/(SLUG+'.blend')
PARENT=ROOT/'library/cabinetry/oak-wardrobe-2ft/v001/oak-wardrobe-2ft.blend'
GEN='tools/library/publish_oak_linen_cabinet.py'
SHELF_Z=[.46,.85,1.24,1.63]

def publish():
 if NATIVE.exists():print('PRESERVE existing immutable asset');return
 bpy.ops.wm.read_factory_settings(use_empty=True)
 with bpy.data.libraries.load(str(PARENT),link=False) as (src,dst):
  candidates=[x for x in src.collections if not any(y in x.lower() for y in ('preview','studio'))]
  assert len(candidates)==1,candidates;dst.collections=candidates
 c=dst.collections[0];c.name=NAME;bpy.context.scene.collection.children.link(c);g.ACTIVE=c
 c['asset_id']=ID;c['asset_version']='v001';c['derived_from']='cabinetry/oak-wardrobe-2ft/v001'
 oak=linked_mat('coastal-white-oak','v001')
 removed=[]
 for ob in list(c.all_objects):
  if 'hanging rail' in ob.name.lower():removed.append(ob.name);bpy.data.objects.remove(ob,do_unlink=True);continue
  if ob.type=='MESH' and any('oak' in m.name.lower() for m in ob.data.materials if m):
   ob.data.materials.clear();ob.data.materials.append(oak)
  if 'upper shelf' in ob.name:ob.name='Linen retained upper shelf'
 for i,z in enumerate(SHELF_Z):
  box('Linen added shelf %d'%(i+1),(0,.018288,z),(.573024,.54864,.019812),oak,.0018288)
 assert len(removed)==1,removed
 lo,hi=bounds(c);FOLDER.mkdir(parents=True,exist_ok=True)
 bpy.data.libraries.write(str(NATIVE),{c},fake_user=True,path_remap='RELATIVE_ALL')
 meta={'schema_version':1,'id':ID,'version':'v001','name':NAME,'units':'meters','dimensions_m':[hi[i]-lo[i] for i in range(3)],'bounds_m':{'min':lo,'max':hi},'blender':{'collection':NAME},'placement':{'origin':'Floor center of nominal 24x24 inch carcass at Z=0','front_direction':'-Y; width X; Z up','allowed_scaling':'Rigid placement and rotation only; no scaling'},'nominal_dimensions_inches':[24,24,96],'modeled_state':'Closed pair of individually editable oak doors, five actual internal shelves above bottom floor; no hanging rail. Shelves are fixed in visualization; selected hardware remains unspecified.','internal_storage':{'added_shelf_centers_z_m':SHELF_Z,'retained_upper_shelf_center_z_m':6.65*g.F,'shelf_thickness_m':.019812,'shelf_width_m':.573024,'shelf_depth_m':.54864,'bottom_deck_top_z_m':.33*g.F,'shelf_count':5,'top_linen_compartment_note':'Upper compartment remains storage, not a wardrobe rail space.'},'installation':{'mounting':'Level floor plus host wall anti-tip fixing; cabinet is not a wall-mounted unit. Host supplies finish tolerance and moisture-compatible product selection.','operating_envelope':{'modeled_state':'Closed','intended_open_angle_degrees':90,'hinges_m':[[-.955*g.F,-.965*g.F,0],[.955*g.F,-.965*g.F,0]],'door_leaf_width_m':.95*g.F,'conservative_front_projection_m':.34,'front_operator_space_beyond_swing_m':.60,'basis':'Original concept leaf dimensions plus pulls; approximate planning envelope, not a manufacturer hinge specification.','host_open_state_checked':False},'service_requirements':['Locate inside bathroom with dry access away from shower spray','Reserve floor and door clearance; anti-tip support and shelf capacity require actual specification']},'derived_from':{'id':'cabinetry/oak-wardrobe-2ft','version':'v001','path':'../../oak-wardrobe-2ft/v001/oak-wardrobe-2ft.blend','sha256':hashlib.sha256(PARENT.read_bytes()).hexdigest(),'method':'Append actual published collection; retain original carcass, toe kick, closed doors and pulls. Remove hanging rail and add four shelves below retained upper shelf. Relink original coastal-white-oak material.'},'dependencies':[{'id':'materials/coastal-white-oak','version':'v001','path':'../../../materials/coastal-white-oak/v001/coastal-white-oak.blend'}],'source':{'kind':'original derivative','generator':GEN,'command':'blender -b --factory-startup --python '+GEN},'software':{'blender':bpy.app.version_string},'license':'CC-BY-4.0','rights':'Original Homes project contributors geometry and procedural material; retain attribution. No manufacturer or third-party CAD.','files':{'blender':NATIVE.name,'preview':'preview.png','open_preview':'open-preview.png','validation':'validation.json'},'limitations':'Original linen-storage visualization. Doors have editable geometry but no selected hinge hardware; shelf loads, moist-room suitability and installation remain unresolved.'}
 (FOLDER/'asset.json').write_text(json.dumps(meta,indent=2)+'\n');print('PUBLISHED',ID,meta['dimensions_m'],flush=True)

def open_doors(c):
 for ob in c.all_objects:
  if not any(t in ob.name for t in ('hinged oak door','door pull','pull mount')):continue
  side=-1 if ob.location.x<0 else 1
  hinge=Vector((side*.955*g.F,-.965*g.F,0))
  angle=side*math.pi/2
  ob.matrix_world=Matrix.Translation(hinge)@Matrix.Rotation(angle,4,'Z')@Matrix.Translation(-hinge)@ob.matrix_world
 bpy.context.view_layer.update()

def preview(c):
 g.collection('Linen preview studio only');floor=g.material('Linen neutral ground',(.24,.25,.23),.9)
 box('Preview floor',(0,0,-.025),(200,200,.04),floor)
 s=bpy.context.scene;target=Vector((0,-.06,1.22));s.camera=g.camera('Linen cabinet native preview',Vector((2.0,-4.7,2.9))/g.F,target/g.F,58)
 g.area('Soft key',Vector((-2,-3,5))/g.F,target/g.F,850,3/g.F,(1,.98,.94));g.area('Soft fill',Vector((3,-1,3))/g.F,target/g.F,500,2/g.F,(.94,.97,1))
 s.world=bpy.data.worlds.new('Linen neutral world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=3
 s.render.resolution_x=720;s.render.resolution_y=960;s.render.resolution_percentage=100;s.view_settings.view_transform='AgX';s.render.image_settings.file_format='PNG'
 s.render.filepath=str(FOLDER/'preview.png');bpy.ops.render.render(write_still=True)
 open_doors(c);s.render.filepath=str(FOLDER/'open-preview.png');bpy.ops.render.render(write_still=True)

def verify(render):
 sha=hashlib.sha256(NATIVE.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(NATIVE));assert all(l.filepath.startswith('//') for l in bpy.data.libraries)
 bpy.ops.wm.read_factory_settings(use_empty=True)
 with bpy.data.libraries.load(str(NATIVE),link=True) as (src,dst):assert NAME in src.collections;dst.collections=[NAME]
 c=dst.collections[0];bpy.context.scene.collection.children.link(c);lo,hi=bounds(c)
 assert all(abs(hi[i]-lo[i]-v)<1e-5 for i,v in enumerate([.6096,.6382512,2.4384]))
 assert len([o for o in c.all_objects if 'shelf' in o.name.lower()])==5
 assert not any('hanging rail' in o.name.lower() for o in c.all_objects)
 assert len([o for o in c.all_objects if 'hinged oak door' in o.name])==2
 assert all(Path(bpy.path.abspath(l.filepath,library=l.parent)).exists() for l in bpy.data.libraries)
 shelf_tops=sorted(o.location.z+o.dimensions.z/2 for o in c.all_objects if 'shelf' in o.name.lower())
 if render:
  bpy.ops.wm.read_factory_settings(use_empty=True)
  with bpy.data.libraries.load(str(NATIVE),link=False) as (src,dst):dst.collections=[NAME]
  c=dst.collections[0];bpy.context.scene.collection.children.link(c);preview(c)
 assert hashlib.sha256(NATIVE.read_bytes()).hexdigest()==sha
 report={'fresh_native_open':True,'fresh_link':True,'relative_dependencies_resolve':True,'native_sha256':sha,'native_preserved_by_review':True,'actual_dimensions_m':[hi[i]-lo[i] for i in range(3)],'retained_editable_doors':2,'shelves':5,'shelf_tops_z_m':shelf_tops,'hanging_rails':0,'preview_rendered':(FOLDER/'preview.png').exists(),'open_preview_rendered':(FOLDER/'open-preview.png').exists(),'host_integration_checked':False}
 for key,file in [('preview_sha256','preview.png'),('open_preview_sha256','open-preview.png')]:
  if (FOLDER/file).exists():report[key]=hashlib.sha256((FOLDER/file).read_bytes()).hexdigest()
 (FOLDER/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('VERIFIED',ID,flush=True)
if __name__=='__main__':
 if '--verify' in sys.argv:verify('--render' in sys.argv)
 else:publish()
