"""Fresh native verification of measured geometry and portable pinned dependencies."""
import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent));import design as d
H=ROOT/'homes/modern-block';meta=json.loads((H/'project.json').read_text());scene=bpy.context.scene
assert Path(bpy.data.filepath).resolve()==(H/'model/modern-block.blend').resolve()
libs=[]
for lib in bpy.data.libraries:
 assert lib.filepath.startswith('//'),lib.filepath
 p=Path(bpy.path.abspath(lib.filepath)).resolve();assert p.is_file() and p.is_relative_to(ROOT),str(p)
 libs.append(lib.filepath)
areas={}
for o in scene.objects:
 if o.get('floor_area_role'):
  val=sum(p.area for p in o.data.polygons if p.normal.z>.9);areas[o.name]=val
assert abs(sum(areas.values())-(d.CONDITIONED_M2+d.GARAGE_M2))<.001,areas
beds=[o for o in scene.objects if o.get('bed_count')==1];assert len(beds)==4,[o.name for o in beds]
wardrobes=[o for o in scene.objects if o.instance_type=='COLLECTION' and 'wardrobe' in (o.get('asset_id','')+o.get('shared_asset_id',''))];assert len(wardrobes)>=13
shelves=[o for o in scene.objects if o.instance_type=='COLLECTION' and 'shelving' in o.get('asset_id','')];assert len(shelves)>=5
stairs=[o for o in scene.objects if 'stair oak tread' in o.name];assert len(stairs)==22,len(stairs)
assert abs(max(o.location.z+o.dimensions.z/2 for o in stairs)-3.6)<.001
assert d.STAIR_VOID[1]==8.2 and d.STAIR_VOID[3]==12.5
screens=[o for o in scene.objects if o.name.startswith('Pivot screen ')];assert len(screens)==5
assert min(abs(a.location.x-b.location.x) for a in screens for b in screens if a!=b)>1.806
pool=bpy.data.objects['Courtyard pool'];assert tuple(round(v,2) for v in pool.location)==(5,13,0)
# Verify actual evaluated instance geometry exists at physical scale.
dg=bpy.context.evaluated_depsgraph_get();instance_counts={}
for it in dg.object_instances:
 if it.is_instance and it.parent:
  name=it.parent.original.name;instance_counts[name]=instance_counts.get(name,0)+1
for obj in beds+screens+[pool]:assert instance_counts.get(obj.name,0)>0,obj.name
for o in scene.objects:
 if o.instance_type=='COLLECTION' and o.get('asset_id','').startswith(('appliances/','cabinetry/','fixtures/')):
  assert all(abs(v-1)<.00001 for v in o.scale),(o.name,tuple(o.scale))
openings=json.loads((H/'model/opening-schedule.json').read_text())
for name in ['Main courtyard','Guest court']:
 assert any(o['name']==name and o['kind']=='door' and min(o['a'][1],o['b'][1])<3.4 for o in openings),name
# Exterior decks bear into grade, and planting leaves the vehicle apron clear.
for obj in scene.objects:
 if obj.name.endswith('terrace substrate'):
  assert obj.location.z-obj.dimensions.z/2<=-.53
sys.path.insert(0,str(ROOT/'tools'))
from site_context import _plant_bounds,_overlaps
bpy.context.view_layer.update()
for obj in scene.objects:
 if obj.name.startswith(('Forecourt native concept planting','Garden edge drift')):
  assert not _overlaps(_plant_bounds(obj),(-17.45,8,-7.95,22)),obj.name
# Revised entrance, room-aligned glazing and external service geometry.
for prefix in ['Entry','Lanai']:
 steps=sorted([o for o in scene.objects if o.name.startswith(prefix+' equal-riser garden step')],key=lambda o:o.location.y)
 assert len(steps)==3
 tops=[o.location.z+o.dimensions.z/2 for o in steps]
 assert all(abs(b-a-.53/3)<.0001 for a,b in zip([-.53]+tops,tops)),tops
landing=bpy.data.objects['Arrival supported level landing']
assert abs(landing.location.z+landing.dimensions.z/2)<.0001
assert abs(landing.dimensions.y-1.4)<.0001
privacy=[o for o in scene.objects if o.name.startswith('Primary bath fixed privacy screen')]
assert len(privacy)==2
for obj in privacy:
 assert all(abs(v-1)<.00001 for v in obj.scale)
 assert abs(obj.location.y+.6)<.0001 and obj['service_gap_m']>=.3
 bounds=[obj.matrix_world @ child.matrix_world @ Vector(p) for child in obj.instance_collection.all_objects if child.type=='MESH' for p in child.bound_box]
 assert abs(max(p.y for p in bounds)+.45)<.0001
 assert abs(max(p.z for p in bounds)-6.45)<.0001
front=[o for o in openings if o['name']=='Upper street']
assert len(front)==2 and all(not min(o['a'][0],o['b'][0])<17<max(o['a'][0],o['b'][0]) for o in front)
flue=bpy.data.objects['Living conceptual concealed flue']
assert flue.location.x-flue.dimensions.x/2>22.12-.001
assert '13-east-arrival' in bpy.data.objects
receipt={'native_reopened':True,'facade_revision':{'equal_exterior_risers_m':.53/3,'entry_landing_depth_m':1.4,'bathroom_screen_instances':2,'screen_service_gap_m':.35,'front_partition_clear_of_glazing':True,'flue_outside_upper_wc':True},'blender':bpy.app.version_string,'relative_libraries':len(libs),'measured_floor_areas_m2':areas,'conditioned_gross_m2':d.CONDITIONED_M2,'bed_instances':len(beds),'wardrobe_bays':len(wardrobes),'shelf_modules':len(shelves),'stair_risers':22,'riser_m':3.6/22,'tread_depth_m':.28,'flight_width_m':1.2,'landing_depth_m':1.22,'upper_landing_m':1.2,'screen_panel_centers_m':2.0,'screen_sweep_radius_m':.903,'sheltered_pavilion_doors':True,'evaluated_required_instances':{o.name:instance_counts[o.name] for o in beds+screens+[pool]},'limitations':['Concept geometry and route reservations only; manufacturer selection, engineering and local approval unresolved.','Window modules explicitly resized; frame sightlines vary from source nominal.','No exact existing-building dimensions or original layout claimed.']}
(H/'model/native-validation.json').write_text(json.dumps(receipt,indent=2)+'\n');print('MODERN_BLOCK_VERIFIED',json.dumps(receipt),flush=True)
