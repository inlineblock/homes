"""Reopened-geometry checks. Does not certify construction or commercial systems."""
import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'tools')]
from design import *
F=.3048;s=bpy.context.scene;HOME=ROOT/'homes'/SLUG

def bounds(o):
    pts=[o.matrix_world@Vector(v) for v in o.bound_box]
    return tuple(min(getattr(p,a)/F for p in pts) for a in 'xyz')+tuple(max(getattr(p,a)/F for p in pts) for a in 'xyz')
def intersects(a,b,tol=.002):return all(min(a[i+3],b[i+3])-max(a[i],b[i])>tol for i in range(3))
links=[]
for lib in bpy.data.libraries:
    assert lib.filepath.startswith('//'),lib.filepath
    p=Path(bpy.path.abspath(lib.filepath)).resolve();assert p.is_file() and p.is_relative_to(ROOT);links.append(lib.filepath)
assert len(links)>=15
floor=bpy.data.objects['Gross enclosed floor'];area=floor.dimensions.x*floor.dimensions.y/F**2;assert abs(area-AREA)<.02
assert len([o for o in s.objects if ' bed frame' in o.name])==3
# Verify the widened entry from actual wall extents, including the shorter east enclosure.
east=[bounds(o) for o in s.objects if o.name.startswith('Entry east') and 'leaf' not in o.name]
west=[bounds(o) for o in s.objects if o.name.startswith('Primary east') and 'leaf' not in o.name]
entry_clear=min(v[0] for v in east)-max(v[3] for v in west)
assert entry_clear>=7.6 and max(v[4] for v in east)<=12.01
assert len([o for o in s.objects if o.type=='EMPTY' and 'oak wardrobe' in o.name])==6
assert len([o for o in s.objects if o.name.startswith('Primary WC west') and o.type=='MESH'])>=4
assert any(o.name.startswith('Primary WC rear') for o in s.objects)
# Test every panel component against actual pocket/wall solids through its travel.
statics=[o for o in s.objects if o.type=='MESH' and o.get('ifc_class')=='IfcWall']
panels=[o for o in s.objects if o.get('opening_system')]
checks=0
for f in [1,20,40,60,80,100,120]:
    s.frame_set(f);bpy.context.view_layer.update()
    for o in panels:
        a=bounds(o)
        for other in statics:
            assert not intersects(a,bounds(other)),(f,o.name,other.name,'panel/wall collision')
        checks+=1
s.frame_set(120);bpy.context.view_layer.update()
for name,spec in [('Great room',DOOR),('Serving window',WINDOW)]:
    group=[bounds(o) for o in panels if o['opening_system']==name]
    if spec['pocket_center']<spec['start']:assert max(bb[3] for bb in group)<spec['start']-.10
    else:assert min(bb[0] for bb in group)>spec['end']+.05
# Swept concept routes include actual evaluated collection-instance geometry.
# Bounds are conservative: passing is not a code or accessibility finding.
def instance_bounds(inst):
    # Curve control handles can have oversized bounds; check tessellated visible geometry.
    if inst.object.type == 'CURVE':
        mesh=inst.object.to_mesh()
        pts=[inst.matrix_world@v.co for v in mesh.vertices]
        inst.object.to_mesh_clear()
    else:
        pts=[inst.matrix_world@Vector(v) for v in inst.object.bound_box]
    return tuple(min(getattr(p,a)/F for p in pts) for a in 'xyz')+tuple(max(getattr(p,a)/F for p in pts) for a in 'xyz')

def pedestrian_height(bb):
    return bb[2]<6 and bb[5]>.30

linked_obstacles=[]
linked_parent_names=set()
for inst in bpy.context.evaluated_depsgraph_get().object_instances:
    if not inst.is_instance or not inst.parent or inst.object.type not in {'MESH','CURVE'}:continue
    if inst.object.hide_render or inst.parent.hide_render:continue
    bb=instance_bounds(inst)
    if pedestrian_height(bb):
        linked_obstacles.append((inst.parent.name+' '+inst.object.name,bb))
        linked_parent_names.add(inst.parent.name)
# Keep local architectural/furniture checks, plus every linked object in the
# house or furnishing region. Rugs and paving fall below the height filter.
obstacles=[]
for o in s.objects:
    if o.type!='MESH' or o.hide_render:continue
    groups=[c.name for c in o.users_collection]
    if not any(c.startswith(('01 Architecture','03 Kitchen','04 Furnishings','09 Roof')) for c in groups):continue
    bb=bounds(o)
    if pedestrian_height(bb):obstacles.append((o.name,bb))
obstacles.extend(linked_obstacles)
assert any('Living shared linen sofa' in n for n in linked_parent_names),'linked living sofa absent from route geometry'
assert any('Living shared oak coffee table' in n for n in linked_parent_names),'linked coffee table absent from route geometry'
assert any('Dining shared eight foot oak table' in n for n in linked_parent_names),'linked dining table absent from route geometry'
assert sum('Dining shared oak chair' in n for n in linked_parent_names)==6,'all six dining chairs must enter route geometry'

def check_routes(route_map, solids, radius, step, message):
    checks=0;closest=None
    for name,points in route_map.items():
        for a,b in zip(points,points[1:]):
            # Broad phase only removes objects that cannot meet this segment.
            candidates=[(obj,bb) for obj,bb in solids
                        if bb[3]>=min(a[0],b[0])-radius and bb[0]<=max(a[0],b[0])+radius
                        and bb[4]>=min(a[1],b[1])-radius and bb[1]<=max(a[1],b[1])+radius]
            n=max(1,math.ceil(math.dist(a,b)/step))
            for i in range(n+1):
                x=a[0]+(b[0]-a[0])*i/n;y=a[1]+(b[1]-a[1])*i/n
                for obj,bb in candidates:
                    dx=max(bb[0]-x,0,x-bb[3]);dy=max(bb[1]-y,0,y-bb[4])
                    distance=math.hypot(dx,dy);checks+=1
                    if closest is None or distance<closest:closest=distance
                    assert distance>=radius-.02,(name,obj,round(x,2),round(y,2),message)
    return {'sampled_object_distance_checks':checks,'nearest_candidate_distance_ft':round(closest,3) if closest is not None else None}
# Centerline paths deliberately continue into the room, not just to a wall label.
routes={
 'entry to dining terrace':[(20,-2),(20,18.7),(25,18.7),(42,18.7),(42,34),(36,36),(36,42),(39,46)],
 'primary bedroom':[(20,10.3),(11.5,10.3),(11.5,6)],
 'primary bath':[(11.5,10.3),(9.65,10.3),(9.65,15.9),(11,17),(12,20),(13.8,21),(13.8,24)],
 'primary dressing':[(9.65,15.9),(8,14),(5,14),(4.5,14.25),(3.4,14.25)],
 'primary shower':[(11,17),(8,20.25),(4,20.25)],
 'primary WC':[(11,17),(12,13.85),(16,13.85)],
 'bedroom 02':[(22,10),(22,7.05),(28.5,7.05)],
 'bedroom 02 closet':[(22,10),(22,7.05),(28.5,7.05),(28.5,10.25),(37.2,10.25),(37.2,5)],
 'bedroom 03 closet':[(44.65,18.7),(44.65,12),(52.7,12)],
 'bedroom 03':[(44.65,18.7),(44.65,14),(44.65,12)],
 'guest bath':[(58,18.7),(58,2.25),(62,2.25)],
 'guest WC':[(62,2.25),(63.55,3.3)],
 'guest shower':[(62,2.25),(63.6,3.3),(63.6,6.1)],
 'guest vanity':[(63.6,6.1),(64.05,6.5)],
 'laundry':[(58,18.7),(58,11.65),(62,11.65)],
 'kitchen work aisle':[(42,34),(47,34),(62,34),(62,29)],
 'coat storage':[(22,7),(22,10.9)],
 'linen storage':[(58,11.65),(62,11.65),(64,11.65),(64,11.7)],
 'mechanical service':[(58,18.7),(64,18.7)],
 'fireplace front service':[(20,37),(12,37),(7.25,36.78)],
}
interior_route_evidence=check_routes(routes,obstacles,1.25,.12,'30 inch walking route obstructed')
# Counter continuity and serving aperture remain separate from stone.
bridge=bounds(bpy.data.objects['Continuous stone sill serving bridge']);s.frame_set(1);bpy.context.view_layer.update()
windowbottom=min(bounds(o)[2] for o in panels if o['opening_system']=='Serving window')
assert windowbottom>bridge[5]
outer_top=bounds(bpy.data.objects['Exterior serving stone counter'])
outer_front=max(bounds(o)[4] for o in s.objects if o.name.startswith('Exterior serving drawer front'))
overhang=outer_top[4]-outer_front
assert overhang>=1.0,('insufficient counter knee overhang',overhang)
# Independent site checks include new columns/screens, local terrace furniture,
# evaluated linked conversation furniture/stools, and actual plant meshes.
s.frame_set(120);bpy.context.view_layer.update()
arrival_obstacles=[]
for o in s.objects:
    if o.type!='MESH' or o.hide_render:continue
    groups=[c.name for c in o.users_collection]
    if not any(c.startswith(('01 Architecture','03 Kitchen','04 Furnishings','06 Landscape','09 Roof','12 Arrival','13 Carport','14 Verandah')) for c in groups):continue
    if o.name.startswith(('Illustrative dune ground','Soft original coastal dune topography','Illustrative ocean')):continue
    bb=bounds(o)
    if pedestrian_height(bb):arrival_obstacles.append((o.name,bb))
arrival_obstacles.extend(linked_obstacles)
assert any('Shared terrace dining table' in n for n in linked_parent_names),'linked outdoor dining table absent from route geometry'
assert sum('Shared terrace dining chair' in n for n in linked_parent_names)==6,'all six outdoor dining chairs must enter route geometry'
assert any('Shared west terrace sofa' in n for n in linked_parent_names),'linked outdoor sofa absent from route geometry'
assert any('| shared grass' in n for n in linked_parent_names),'linked planting absent from route geometry'
arrival_routes={'parking to front entry':[(86,-15),(86,-2.25),(20,-2.25),(20,2)],'road to front entry':[(20,-44),(20,2)]}
arrival_route_evidence=check_routes(arrival_routes,arrival_obstacles,1.5,.15,'36 inch arrival route blocked')
driver_routes={'left car driver to crosswalk':[(75,-15),(75,-2.25),(20,-2.25)],'right car driver to crosswalk':[(88,-15),(86,-15),(86,-2.25),(20,-2.25)]}
driver_route_evidence=check_routes(driver_routes,arrival_obstacles,1.25,.15,'30 inch driver approach blocked')
# Stop beside seating/dining rather than sweeping into a chair/table footprint.
terrace_routes={
 'slider to outdoor dining':[(36,42),(39,46.5),(39,51.5)],
 'slider to seaward terrace edge':[(36,42),(39,46.5),(39,57)],
 'slider to serving counter approach':[(36,42),(39,46.5),(46,46.5),(46,48.3),(65,48.3),(65,45)],
 'slider to western conversation':[(36,42),(36,45.5),(20.7,45.5),(20.7,51.5),(17.5,51.5)],
}
terrace_route_evidence=check_routes(terrace_routes,arrival_obstacles,1.5,.12,'36 inch terrace route blocked')
# Measure real support geometry; constants identify the intended design only.
from verandah import (PERGOLA_BOUNDS,PERGOLA_POSTS,PERGOLA_POST_WIDTH,PERGOLA_BEAM_BOTTOM,PERGOLA_BEAM_TOP,
    PERGOLA_LEDGER_BOTTOM,PERGOLA_LEDGER_TOP,PERGOLA_SLAT_TOP,PERGOLA_SLAT_COUNT,SCREEN_HEIGHT,ENTRY_CANOPY_POSTS)
columns=[o for o in s.objects if o.name.startswith('Verandah timber column')]
assert len(columns)==2,('attached pergola requires only two seaward supports',len(columns))
measured_posts=[]
for target in PERGOLA_POSTS:
    matches=[o for o in columns if math.hypot((bounds(o)[0]+bounds(o)[3])/2-target[0],(bounds(o)[1]+bounds(o)[4])/2-target[1])<.01]
    assert len(matches)==1,('missing seaward pergola support',target)
    bb=bounds(matches[0]);assert abs(bb[3]-bb[0]-PERGOLA_POST_WIDTH)<.01 and bb[2]<=.19 and abs(bb[5]-PERGOLA_BEAM_BOTTOM)<.01
    assert bb[1]>PERGOLA_BOUNDS[2]+10, 'house-side pergola column is forbidden'
    measured_posts.append({'center_ft':list(target),'bottom_ft':round(bb[2],3),'top_ft':round(bb[5],3),'width_ft':round(bb[3]-bb[0],3)})
outer=bounds(bpy.data.objects['Verandah timber-clad steel outer beam'])
ledger=bounds(bpy.data.objects['Verandah attached structural header ledger'])
assert abs(outer[2]-PERGOLA_BEAM_BOTTOM)<.01 and abs(outer[5]-PERGOLA_BEAM_TOP)<.01
assert abs(ledger[2]-PERGOLA_LEDGER_BOTTOM)<.01 and abs(ledger[5]-PERGOLA_LEDGER_TOP)<.01
assert ledger[0]<DOOR['start'] and ledger[3]>DOOR['end'],'ledger must cover the whole sliding wall'
header=bounds(bpy.data.objects['Great room structural header concept'])
assert ledger[1]<=header[4]+.001 and ledger[4]>header[4] and min(ledger[5],header[5])>max(ledger[2],header[2]),'ledger must meet actual structural header face without floating gap'
assert ledger[2]>DOOR['head']+.10,'ledger below required slider head clearance'
beams=[outer,ledger]+[bounds(o) for o in s.objects if o.name.startswith('Verandah side beam')]
assert len(beams)==4
slats=[bounds(o) for o in s.objects if o.name.startswith('Verandah open shade slat')]
assert len(slats)==PERGOLA_SLAT_COUNT and all(abs(bb[2]-PERGOLA_BEAM_TOP)<.01 and abs(bb[5]-PERGOLA_SLAT_TOP)<.01 for bb in slats)
soffit=[bounds(o) for o in s.objects if o.name.startswith(('Pavilion deep timber eave 02','Pavilion deep timber eave 03'))]
assert soffit and max(bb[5] for bb in slats)<min(bb[2] for bb in soffit),'pergola intersects main roof soffit'
for o in columns:
    bb=bounds(o)
    assert min(bb[3],outer[3])>max(bb[0],outer[0]) and min(bb[4],outer[4])>max(bb[1],outer[1]) and abs(bb[5]-outer[2])<.01,('column does not meet seaward beam',o.name)
screen=[bounds(o) for o in s.objects if o.name.startswith('Verandah low')]
assert screen and max(bb[5] for bb in screen)<=SCREEN_HEIGHT+.01
entry_posts=[bounds(o) for o in s.objects if o.name.startswith('Entry canopy timber column')]
assert len(entry_posts)==len(ENTRY_CANOPY_POSTS)
verandah_evidence={'seaward_supports':measured_posts,'house_side_columns':0,'ledger_bottom_ft':round(ledger[2],3),'ledger_top_ft':round(ledger[5],3),'ledger_meets_header_face':True,'sliding_wall_width_covered_ft':DOOR['end']-DOOR['start'],'slat_to_soffit_clearance_ft':round(min(bb[2] for bb in soffit)-max(bb[5] for bb in slats),3),'perimeter_beams':len(beams),'beam_underside_ft':round(min(bb[2] for bb in beams),3),'open_shade_slats':len(slats),'slat_top_ft':round(max(bb[5] for bb in slats),3),'west_screen_height_ft':round(max(bb[5] for bb in screen),3),'entry_canopy_supports':len(entry_posts),'limits':'Geometric support contact and pedestrian routes only; no structural sizing, wind restraint, foundation, waterproofing or compliance approval. Pergola is open shade, not a rain roof.'}
for prefix,center in [('Pearl coastal coupe',79.5),('Graphite coastal coupe',92.5)]:
    bb=[bounds(o) for o in s.objects if o.name.startswith(prefix)]
    assert min(v[0] for v in bb)>center-6 and max(v[3] for v in bb)<center+6
    assert min(v[1] for v in bb)>-27 and max(v[4] for v in bb)<-3
from pavilion_roof import verify_geometry as verify_roof
roof_evidence=verify_roof(s)
report={'native_model_reopened':True,'gross_enclosed_area_sqft':round(area,2),'modeled_beds':3,'relative_libraries':links,'opening_travel':{'sampled_frames':[1,20,40,60,80,100,120],'panel_component_checks':checks,'no_panel_wall_collisions':True,'both_clear_openings_unobstructed_by_panels':True},'entry':{'clear_width_ft':round(entry_clear,2),'east_enclosure_length_ft':12,'guest_wardrobe_bays':6,'wardrobe_bay_width_ft':2,'wardrobe_depth_ft':2},'circulation':{'swept_diameter_inches':30,'routes':list(routes),'actual_geometry_checked':True},'counter':{'stone_top_ft':round(bridge[5],3),'closed_window_bottom_ft':round(windowbottom,3),'no_glass_stone_intersection':True,'outdoor_knee_overhang_inches':round(overhang*12,2)},'arrival':{'carport_ft':[26,24],'cars':2,'routes':list(arrival_routes),'swept_route_diameter_inches':36,'driver_approach_diameter_inches':30,'driver_routes':list(driver_routes),'actual_geometry_checked':True,'limits':'Parked envelope and walking path only; no turning simulation or full car-door sweep.'},'roof':roof_evidence,'limits':'Concept geometry only. No weatherproofing, thermal, structural, impact/flood or accessibility approval.'}
report['circulation'].update({'linked_instance_parents_checked':len(linked_parent_names),'distance_checks':interior_route_evidence})
report['arrival'].update({'includes_linked_furniture_and_plant_geometry':True,'distance_checks':arrival_route_evidence,'driver_distance_checks':driver_route_evidence})
report['terrace_circulation']={'swept_route_diameter_inches':36,'routes':terrace_routes,'actual_geometry_checked':True,'distance_checks':terrace_route_evidence,'limits':'Static furniture only; no occupied seating, moving chair, mobility-device or terrain-grade approval.'}
report['verandah']=verandah_evidence
from lighting_hardware import verify_saved
lighting_evidence=verify_saved(s)
(HOME/'model/lighting-validation.json').write_text(json.dumps(lighting_evidence,indent=2)+'\n')
# Check the actual linked insert and surround against the pocket and furniture.
from fireplace import INSERT_FRONT, INSERT_BOTTOM, INSERT_WIDTH, INSERT_HEIGHT
insert_parts=[bb for name,bb in linked_obstacles if name.startswith('Living shared electric fireplace ')]
assert insert_parts, 'Linked fireplace missing from evaluated scene'
insert_bb=tuple(min(b[i] for b in insert_parts) for i in range(3))+tuple(max(b[i+3] for b in insert_parts) for i in range(3))
surround=[o for o in s.objects if o.get('fireplace_surround')]
assert len(surround)==5
for bb in insert_parts:
    for obj in surround:assert not intersects(bb,bounds(obj)),('Fireplace insert buried in surround',obj.name)
pocket=[o for o in s.objects if o.name.startswith('Pocket removable cladding skin') and o.location.x/F<10]
assert len(pocket)==2
inner_skin=min(pocket,key=lambda o:o.location.y)
assert 'plaster' in inner_skin.data.materials[0].name.lower()
fire_back=max([insert_bb[4]]+[bounds(o)[4] for o in surround])
assert fire_back<bounds(inner_skin)[1], 'Fireplace occupies the sliding pocket'
hearth=bounds(bpy.data.objects['Living fireplace low hearth'])
chaise=max(bounds(o)[4] for o in s.objects if o.name.startswith(('Living chaise cushion','Living chaise base')))
assert hearth[1]-chaise>=3.-.002
# Front removal envelope spans the full insert, measured from its actual front.
service=(insert_bb[0],insert_bb[1]-3,0,insert_bb[3],insert_bb[1],6)
for name,bb in obstacles:
    if name.startswith(('Living fireplace','Living shared electric fireplace')):continue
    assert not intersects(service,bb),('Fireplace front removal blocked',name)
fire_checks=0
for f in [1,20,40,60,80,100,120]:
    s.frame_set(f);bpy.context.view_layer.update()
    for panel in panels:
        for bb in insert_parts+[bounds(o) for o in surround]:
            assert not intersects(bounds(panel),bb),(f,panel.name,'fireplace / sliding panel collision')
            fire_checks+=1
report['fireplace']={'type':'Original slim electric concept','linked_asset':'fixtures/slim-electric-fireplace-48in@v001',
 'evaluated_insert_bounds_ft':insert_bb,'surround_parts':len(surround),'clear_chaise_to_hearth_ft':round(hearth[1]-chaise,3),
 'front_removal_depth_ft':3,'front_removal_unobstructed':True,'pocket_skin_separation_ft':round(bounds(inner_skin)[1]-fire_back,3),
 'sampled_panel_fireplace_checks':fire_checks,'no_panel_collisions':True,
 'limits':'Concept geometry; product, electrical circuit, ventilation and thermal clearances unselected.'}
manifest=json.loads((HOME/'project.json').read_text())
full=[o for o in s.objects if o.name.startswith('Shared limestone facade full panel')]
cuts=[o for o in s.objects if o.name.startswith('Limestone facade bespoke perimeter cut')]
assert len(full)==manifest['facade_panel_schedule']['full_linked_panels']
assert len(cuts)==manifest['facade_panel_schedule']['bespoke_edge_cuts']
report['pocket_wall']={'exterior':'Matching pinned limestone facade panels with narrow service seam','interior':'Warm limestone plaster',
 'facade_full_panels':len(full),'facade_perimeter_cuts':len(cuts),'moving_cavity_retained':True}
report['lighting']={'actual_ceiling_openings':lighting_evidence['total_actual_ceiling_openings'],'regions':lighting_evidence['downlights'],'pendant_ceiling_contact_checked':True}
# Artistic bounce emitters remain wholly below their local ceiling, not through roofs.
for name in ['Daylight bounce living','Daylight bounce dining','Daylight bounce kitchen']:
    lamp=bpy.data.objects[name]
    assert (lamp.matrix_world.to_quaternion()@Vector((0,0,-1))-Vector((0,0,-1))).length<1e-6
    assert lamp.location.z/F < 10.45
    assert lamp.location.y/F + lamp.data.size/(2*F) < 39.5
    assert lamp.location.x/F - lamp.data.size/(2*F) > .5
    assert lamp.location.x/F + lamp.data.size/(2*F) < 67.5
s.frame_set(1);bpy.context.view_layer.update()
(HOME/'model/model-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('COASTAL_VERIFIED',json.dumps(report),flush=True)
# IFC exporter can follow this script: leave scene at closed frame, do not save blend.
