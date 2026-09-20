"""Fresh native verification of measured geometry and portable pinned dependencies."""
import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent));import design as d
H=ROOT/'homes/modern-block';meta=json.loads((H/'project.json').read_text());scene=bpy.context.scene
assert Path(bpy.data.filepath).resolve()==(H/'model/modern-block.blend').resolve()
bpy.context.view_layer.update()
def world_bounds(obj):
 return [obj.matrix_world @ Vector(p) for p in obj.bound_box]
def bottom_z(obj):
 return min(p.z for p in world_bounds(obj))
def top_z(obj):
 return max(p.z for p in world_bounds(obj))
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
lower_stairs=[o for o in stairs if o.name.startswith('Lower stair oak tread')]
upper_stairs=[o for o in stairs if o.name.startswith('Upper stair oak tread')]
assert len(lower_stairs)==11 and len(upper_stairs)==11
riser=(d.UPPER-d.GROUND)/24
half_landing=bpy.data.objects['Stair half landing']
half_landing_top=top_z(half_landing)
assert abs(half_landing_top-(d.GROUND+d.UPPER)/2)<.001
tread_tops=sorted(top_z(o) for o in stairs)
expected_tops=[d.GROUND+i*riser for i in list(range(1,12))+list(range(13,24))]
assert all(abs(actual-expected)<.001 for actual,expected in zip(tread_tops,expected_tops)),tread_tops
assert abs(max(tread_tops)-(d.UPPER-riser))<.001
# The half landing and upper occupied floor form the twelfth and final rises;
# they are not extra duplicate treads at the same elevation.
rise_levels=sorted([d.GROUND]+tread_tops+[half_landing_top,d.UPPER])
assert len(rise_levels)==25 and all(abs(b-a-riser)<.001 for a,b in zip(rise_levels,rise_levels[1:]))
assert d.STAIR_VOID[1]==8.2 and d.STAIR_VOID[3]==12.5
# Measure the occupied projection and selected finished ceiling undersides.
upper_slab=bpy.data.objects['Upper occupied slab']
upper_slab_bounds=world_bounds(upper_slab)
upper_floor_top=max(p.z for p in upper_slab_bounds)
upper_front=min(p.y for p in upper_slab_bounds)
assert abs(upper_floor_top-d.UPPER)<.001
assert abs(upper_front-d.UPPER_FRONT)<.001
main_ceiling_bottom=bottom_z(bpy.data.objects['Main ceiling below upper'])
assert abs(main_ceiling_bottom-(d.GROUND+d.GROUND_CLEAR))<.001
kitchen_slats=[o for o in scene.objects if o.name.startswith('Kitchen oak ceiling slat')]
assert kitchen_slats
kitchen_slat_bottoms=[bottom_z(o) for o in kitchen_slats]
assert all(abs(z-(d.GROUND+d.GROUND_CLEAR))<.001 for z in kitchen_slat_bottoms),kitchen_slat_bottoms
upper_ceiling_bottom=bottom_z(bpy.data.objects['Cedar upper bar ceiling'])
assert abs(upper_ceiling_bottom-(d.UPPER+d.UPPER_CLEAR))<.001
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
 assert abs(obj.location.y-(d.UPPER_FRONT-.6))<.0001 and obj['service_gap_m']>=.3
 bounds=[obj.matrix_world @ child.matrix_world @ Vector(p) for child in obj.instance_collection.all_objects if child.type=='MESH' for p in child.bound_box]
 assert abs(max(p.y for p in bounds)-(d.UPPER_FRONT-.45))<.0001
 assert abs(max(p.z for p in bounds)-(d.UPPER+2.85))<.0001
front=[o for o in openings if o['name']=='Upper street']
assert len(front)==2 and all(not min(o['a'][0],o['b'][0])<17<max(o['a'][0],o['b'][0]) for o in front)
flue=bpy.data.objects['Living conceptual concealed flue']
assert flue.location.x-flue.dimensions.x/2>22.12-.001
assert '13-east-arrival' in bpy.data.objects
# The rotated shower's controls need a real host face, not open space behind
# an otherwise complete linked fixture. Measure the wall and actual hardware.
shower_wall=bpy.data.objects['Primary shower stone service wall']
shower_wall_bounds=world_bounds(shower_wall)
wall_xy=(min(p.x for p in shower_wall_bounds),min(p.y for p in shower_wall_bounds),max(p.x for p in shower_wall_bounds),max(p.y for p in shower_wall_bounds))
assert all(abs(actual-expected)<.0001 for actual,expected in zip(wall_xy,d.SHOWER_SERVICE_WALL)),wall_xy
assert abs(bottom_z(shower_wall)-d.UPPER)<.0001
assert abs(top_z(shower_wall)-(d.UPPER+d.SHOWER_SERVICE_HEIGHT))<.0001
shower=bpy.data.objects['Primary separate shower']
assert shower.instance_collection is not None
shower_control_gaps={}
for label in ('Mixer plate','Shower rail'):
 parts=[child for child in shower.instance_collection.all_objects if child.type=='MESH' and child.name.split('.')[0]==label]
 assert len(parts)==1,(label,[child.name for child in parts])
 part=parts[0]
 bounds=[shower.matrix_world @ part.matrix_world @ Vector(p) for p in part.bound_box]
 assert min(p.x for p in bounds)>=wall_xy[0]-.0001 and max(p.x for p in bounds)<=wall_xy[2]+.0001,label
 assert min(p.z for p in bounds)>=bottom_z(shower_wall)-.0001 and max(p.z for p in bounds)<=top_z(shower_wall)+.0001,label
 # Up to 5 mm engagement is allowed for a mounting plate; a positive gap
 # greater than 60 mm indicates that the host backing is absent/misaligned.
 gap=min(p.y for p in bounds)-wall_xy[3]
 assert -.005<=gap<=.06,(label,gap)
 shower_control_gaps[label]=gap
receipt={'native_reopened':True,'facade_revision':{'equal_exterior_risers_m':.53/3,'entry_landing_depth_m':1.4,'bathroom_screen_instances':2,'screen_service_gap_m':.35,'front_partition_clear_of_glazing':True,'flue_outside_upper_wc':True},'measured_section_m':{'upper_floor_top':upper_floor_top,'occupied_upper_front_y':upper_front,'occupied_front_projection':d.MAIN[1]-upper_front,'main_ceiling_underside':main_ceiling_bottom,'main_clear_height':main_ceiling_bottom-d.GROUND,'kitchen_slat_bottom_min':min(kitchen_slat_bottoms),'kitchen_slat_bottom_max':max(kitchen_slat_bottoms),'upper_ceiling_underside':upper_ceiling_bottom,'upper_clear_height':upper_ceiling_bottom-upper_floor_top},'blender':bpy.app.version_string,'relative_libraries':len(libs),'measured_floor_areas_m2':areas,'conditioned_gross_m2':d.CONDITIONED_M2,'bed_instances':len(beds),'wardrobe_bays':len(wardrobes),'shelf_modules':len(shelves),'stair_risers':24,'stair_treads':22,'treads_per_flight':[len(lower_stairs),len(upper_stairs)],'riser_m':riser,'half_landing_elevation_m':half_landing_top,'highest_tread_elevation_m':max(tread_tops),'stair_convention':'24 equal rises; 11 separate treads per flight, with half landing and upper floor completing each flight.','tread_depth_m':.28,'flight_width_m':1.2,'landing_depth_m':1.22,'upper_landing_m':1.2,'screen_panel_centers_m':2.0,'screen_sweep_radius_m':.903,'sheltered_pavilion_doors':True,'evaluated_required_instances':{o.name:instance_counts[o.name] for o in beds+screens+[pool]},'limitations':['Concept geometry and route reservations only; manufacturer selection, engineering and local approval unresolved.','Structural calculations and support capacity for the occupied projection are not verified.','Ceiling checks measure the selected main, kitchen slat and upper-bar undersides; they do not certify every local soffit or equipment clearance.','Window modules explicitly resized; frame sightlines vary from source nominal.','No exact existing-building dimensions or original layout claimed.']}
receipt['shower_host_support']={'wall_bounds_xy_m':wall_xy,'wall_bottom_m':bottom_z(shower_wall),'wall_top_m':top_z(shower_wall),'wall_height_m':top_z(shower_wall)-bottom_z(shower_wall),'controls_back_to_wall_face_m':shower_control_gaps,'scope':'Geometric host backing only; waterproofing, anchorage and plumbing installation are not certified.'}
(H/'model/native-validation.json').write_text(json.dumps(receipt,indent=2)+'\n');print('MODERN_BLOCK_VERIFIED',json.dumps(receipt),flush=True)
