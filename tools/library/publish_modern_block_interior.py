"""Publish two original interior variations, preserving their pinned source assets.

Blender -b --factory-startup --python tools/library/publish_modern_block_interior.py
Blender -b --factory-startup --python tools/library/publish_modern_block_interior.py -- --verify --render
"""
from pathlib import Path
import bpy,json,sys,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
from common.timber_materials import grain_uv
GEN='tools/library/publish_modern_block_interior.py'
ASSETS={
 'shower-tray-screen-1500x1200':('fixtures','Shower tray screen 1500x1200 | shared v001','fixtures/shower-tray-screen-900'),
 'oak-shelving-2ft':('cabinetry','Oak shelving 2ft | shared v001','cabinetry/oak-wardrobe-2ft'),
}
def folder(slug):return ROOT/'library'/ASSETS[slug][0]/slug/'v001'
def bounds(c):
 bpy.context.view_layer.update();p=[o.matrix_world@Vector(v) for o in c.all_objects if o.type=='MESH' for v in o.bound_box];return [min(q[i] for q in p) for i in range(3)],[max(q[i] for q in p) for i in range(3)]
def source_collection(id,name):
 path=ROOT/'library'/id/'v001'/(id.split('/')[-1]+'.blend')
 with bpy.data.libraries.load(str(path),link=False) as (a,b):b.collections=[a.collections[0]]
 c=b.collections[0];c.name=name;bpy.context.scene.collection.children.link(c);g.ACTIVE=c;return c

def shower(c):
 for o in c.all_objects:
  n=o.name
  if n=='Shower tray':o.dimensions=(1.5,1.2,.05)
  elif n=='Shower recessed drainage slot':o.location.y=.51
  elif n=='Fixed left shower screen':o.location.x=-.74;o.dimensions=(.009,1.19,2.0)
  elif n=='Shower screen post':o.location.x=-.74;o.location.y=-.59
  elif n in ['Shower rail','Shower head arm','Rain shower head','Mixer plate']:o.location.y+=.15
  bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.select_set(False)
 return {'dependencies':[], 'derived_from':{'id':'fixtures/shower-tray-screen-900','version':'v001','changes':'Dedicated 1500x1200mm tray and 1190mm fixed side screen; repositioned original-size controls, head, riser, drain and screen post. All original material appearances and hardware proportions retained.'},'placement':{'origin':'Centered nominal tray XY at floor Z=0','front_direction':'Open front -Y; plumbing wall +Y; fixed glass -X; Z up','allowed_scaling':'Rigid placement and Z rotation only; no nonuniform scale'},'installation':{'mounting':'Continuous supported waterproof floor beneath 1.5x1.2m tray. Host supplies +Y plumbing wall, drain, screen anchorage and adjacent waterproof surfaces.','operating_envelope':{'modeled_state':'Fixed left glass screen and open front; no swinging glass door','reserve_front_approach_depth_m':.9,'basis':'Original concept geometry and approach allowance','host_open_state_checked':False},'service_requirements':['Resolve actual waterproofing, sloped drainage, threshold and splash containment.','Select tested safety glazing, anchorage, slip resistance, controls and ventilation.']},'product_status':'Original concept shower assembly; enlarged fixed tray geometry, not a specified commercial product or accessibility certification'}

def shelves(c):
 # Actual source carcass retained; pantry variant intentionally has open access.
 for o in list(c.all_objects):
  if any(t in o.name for t in ['hanging rail','hinged oak door','door pull','pull mount']):bpy.data.objects.remove(o,do_unlink=True)
 oak=next(o.data.materials[0] for o in c.all_objects if 'side panel' in o.name)
 for i,z in enumerate([1.55,2.80,4.05,5.30]):
  o=g.box('Pantry full-depth shelf %02d'%(i+1),(0,.06,z),(1.88,1.80,.065),oak,.006)
  # Parent oak uses its own physical shader; no new private material variant.
  grain_uv(o)
 for o in c.all_objects:o.name=o.name.replace('Wardrobe','Pantry')
 return {'dependencies':[{'id':'materials/coastal-white-oak','version':'v001','path':'../../../materials/coastal-white-oak/v001/coastal-white-oak.blend'}], 'derived_from':{'id':'cabinetry/oak-wardrobe-2ft','version':'v001','changes':'Retained exact two-foot carcass, back, top/bottom, toe kick and upper shelf. Removed hanging rail, both doors and all pulls; added four full-depth shelf decks for open pantry storage.'},'placement':{'origin':'Floor-center nominal carcass footprint XY; base Z=0','front_direction':'Open shelf access -Y; Z up','allowed_scaling':'Rigid placement and Z rotation only; no nonuniform scale'},'installation':{'mounting':'Level supported floor plus host-designed wall anti-tip anchorage; nominal carcass 2x2x8ft.','operating_envelope':{'modeled_state':'Open-front fixed shelving; no cabinet door or moving rail','reserve_front_access_depth_m':.90,'shelf_deck_elevations_m':[round(z*g.F,4) for z in [.3,1.55,2.80,4.05,5.30,6.65]],'internal_clear_width_m':1.88*g.F,'shelf_depth_m':1.8*g.F,'basis':'Modeled geometry and concept standing allowance','host_open_state_checked':False},'service_requirements':['Host must preserve pantry room door clearance, circulation and access to high shelves.','Select shelving load capacities, wall fixings and moisture-cleaning requirements; no engineered load rating supplied.']},'product_status':'Original open pantry shelving variation; no wardrobe hanging-storage claim or commercial product specification'}

def publish():
 for slug,(cat,name,parent) in ASSETS.items():
  f=folder(slug);path=f/(slug+'.blend')
  if path.exists():continue
  bpy.ops.wm.read_factory_settings(use_empty=True);c=source_collection(parent,name);c['asset_id']=cat+'/'+slug;c['asset_version']='v001';meta=(shower if cat=='fixtures' else shelves)(c);lo,hi=bounds(c);f.mkdir(parents=True,exist_ok=True)
  # Append preserves native original source proportions; relink shared oak to pin dependency.
  if cat=='cabinetry':
   oakpath=ROOT/'library/materials/coastal-white-oak/v001/coastal-white-oak.blend'
   with bpy.data.libraries.load(str(oakpath),link=True) as (a,b):b.materials=[a.materials[0]]
   oak=b.materials[0]
   for o in c.all_objects:
    if o.type=='MESH':
     for slot in o.material_slots:
      if slot.material and ('oak' in slot.material.name.lower()):slot.material=oak
  bpy.data.libraries.write(str(path),{c},fake_user=True,path_remap='RELATIVE_ALL')
  meta.update(schema_version=1,id=cat+'/'+slug,version='v001',name=name,units='meters',dimensions_m=[hi[i]-lo[i] for i in range(3)],bounds_m={'min':lo,'max':hi},blender={'collection':name},license='CC-BY-4.0',rights='Original Homes project contributor geometry derived from existing original shared assets; attribution Homes project contributors.',source={'kind':'original-variation','generator':GEN,'command':'blender -b --factory-startup --python '+GEN},software={'blender':bpy.app.version_string},files={'blender':path.name,'preview':'preview.png','validation':'validation.json'})
  (f/'asset.json').write_text(json.dumps(meta,indent=2)+'\n');print('PUBLISHED',slug,meta['dimensions_m'],flush=True)

def preview(c,f,lo,hi):
 g.collection('Neutral native asset preview');s=bpy.context.scene;target=Vector((0,0,1.15));campos=Vector((2.8,-4.3,2.7));span=2.5
 if f.parent.name.startswith('shower'):campos=Vector((3.4,-4.3,3.0));target.z=.9
 cam=g.camera('Native asset camera',campos/g.F,target/g.F,52);s.camera=cam
 mat=g.material('Neutral preview floor',(.42,.43,.41),.92);g.box('Ground',(0,0,-.03/g.F),(100/g.F,100/g.F,.05/g.F),mat)
 g.area('Broad key',Vector((-3,-2,5))/g.F,target/g.F,1350,3/g.F,(1,.97,.92));g.area('Soft fill',Vector((2,1,3))/g.F,target/g.F,500,2/g.F,(.90,.95,1))
 s.world=bpy.data.worlds.new('Neutral studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.58,.61,.65,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.50
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=650;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(f/'preview.png');s.view_settings.view_transform='AgX';s.view_settings.exposure=0;bpy.ops.render.render(write_still=True)

def verify(render):
 for slug,(cat,name,parent) in ASSETS.items():
  f=folder(slug);path=f/(slug+'.blend');bpy.ops.wm.open_mainfile(filepath=str(path));assert all(l.filepath.startswith('//') for l in bpy.data.libraries)
  bpy.ops.wm.read_factory_settings(use_empty=True)
  with bpy.data.libraries.load(str(path),link=True) as (a,b):b.collections=[name]
  c=b.collections[0];bpy.context.scene.collection.children.link(c);lo,hi=bounds(c);m=json.loads((f/'asset.json').read_text());assert all(abs(hi[i]-lo[i]-m['dimensions_m'][i])<1e-5 for i in range(3));assert all(Path(bpy.path.abspath(l.filepath,library=l.parent)).exists() for l in bpy.data.libraries)
  if cat=='cabinetry':
   assert not any('rail' in o.name.lower() or 'door' in o.name.lower() for o in c.all_objects);assert len([o for o in c.all_objects if 'shelf' in o.name])==5
  if render:preview(c,f,lo,hi)
  (f/'validation.json').write_text(json.dumps({'fresh_native_open':True,'fresh_link':True,'relative_dependencies_resolve':True,'bounds_m':{'min':lo,'max':hi},'objects':len(c.all_objects),'preview_rendered':(f/'preview.png').exists(),'preview_settings':{'renderer':'Cycles CPU','threads':4,'samples':24},'host_integration_checked':False},indent=2)+'\n');print('VERIFIED',slug,flush=True)
if __name__=='__main__':
 if '--verify' in sys.argv:verify('--render' in sys.argv)
 else:publish()
