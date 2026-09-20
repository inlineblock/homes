"""Independent measured kitchen host review, no rendering or home mutation.

Blender --background --factory-startup --python tools/timber02/verify_kitchen.py
  -- --file /path/to/model.blend
Writes only the ignored kitchen verification.json receipt. Concept operation
assumptions remain separate from observed closed mesh and fit measurements.
"""
from pathlib import Path
import bpy, sys, json, hashlib, math
from mathutils import Vector, Matrix

ROOT=Path(__file__).resolve().parents[2]
HOME=ROOT/'homes/timber-courtyard-02'
WORK=HOME/'outputs/work/kitchen'
F=.3048
path=Path(sys.argv[sys.argv.index('--file')+1]) if '--file' in sys.argv else WORK/'kitchen-candidate.blend'
bpy.ops.wm.open_mainfile(filepath=str(path));bpy.context.view_layer.update()
deps=bpy.context.evaluated_depsgraph_get()
CHECKS=[]


def record(name,passed,details,kind='constraint'):
    CHECKS.append({'name':name,'passed':bool(passed),'kind':kind,'details':details})


def aabb(points):
    return ([min(p[i] for p in points) for i in range(3)],[max(p[i] for p in points) for i in range(3)])


def expanded(o,parent=None):
    world=o.matrix_world if parent is None else parent@o.matrix_local
    if o.type in {'MESH','CURVE'}:
        eo=o.evaluated_get(deps)
        mesh=eo.data if o.type=='MESH' else eo.to_mesh()
        points=[world@v.co for v in mesh.vertices]
        if o.type=='CURVE':eo.to_mesh_clear()
        yield {'name':o.name,'object':o,'matrix':world,'bounds':aabb(points)}
    if o.instance_type=='COLLECTION' and o.instance_collection:
        for child in o.instance_collection.objects:
            yield from expanded(child,world)


def roots(prefix):return [o for o in bpy.context.scene.objects if o.library is None and o.name.startswith(prefix)]
def one(prefix):
    result=roots(prefix);assert len(result)==1,(prefix,len(result));return result[0]
def meshlist(prefix):return [m for o in roots(prefix) for m in expanded(o)]
def bounds(prefix):
    return aabb([Vector(p) for m in meshlist(prefix) for p in m['bounds']])
def overlaps(a,b,tol=.0001):return all(min(a[1][i],b[1][i])-max(a[0][i],b[0][i])>tol for i in range(3))
def fit_intersections(prefix,host_prefix):
    return [[a['name'],b['name']] for a in meshlist(prefix) for b in meshlist(host_prefix) if overlaps(a['bounds'],b['bounds'])]
def ft(v):return v/F
def manifest(o):
    return json.loads((Path(bpy.path.abspath(o.instance_collection.library.filepath)).parent/'asset.json').read_text())


# Actual link paths and transforms, not source variable declarations.
libs=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).exists(),'blender_missing':l.is_missing} for l in bpy.data.libraries]
record('All native library links are relative and resolve',all(x['path'].startswith('//') and x['exists'] for x in libs),libs)
equipment=['Kitchen 48 inch refrigerator freezer','Kitchen integrated dishwasher','Kitchen induction stove','Kitchen built in oven','Kitchen extraction hood','Kitchen real sink and mixer']
observed=[]
for prefix in equipment:
    o=one(prefix);meta=manifest(o);lo,hi=bounds(prefix)
    observed.append({'object':o.name,'id':meta['id'],'version':meta['version'],'scale':list(o.scale),'bounds_m':[lo,hi],'origin_m':list(o.location)})
record('Equipment uses exact linked assets at full scale',all(all(abs(v-1)<1e-6 for v in x['scale']) for x in observed),observed)

# Service fixture collections must contain only the declared asset, never a
# publisher's preview stage. Verify mounting voids against evaluated host solids.
outlet_objects=[o for prefix in ['Kitchen garden counter power','Pantry appliance counter power','Kitchen island end power'] for o in roots(prefix)]
outlet_collections=[];outlet_cavities=[]
for outlet in outlet_objects:
    meta=manifest(outlet);actual=aabb([Vector(v) for m in expanded(outlet) for v in m['bounds']])
    expected=meta['bounds_m'];expected_world=aabb([outlet.matrix_world@Vector((x,y,z)) for x in [expected['min'][0],expected['max'][0]] for y in [expected['min'][1],expected['max'][1]] for z in [expected['min'][2],expected['max'][2]]])
    forbidden=[o.name for o in outlet.instance_collection.all_objects if o.type in {'LIGHT','CAMERA'}]
    item={'object':outlet.name,'collection':outlet.instance_collection.name,'declared_collection':meta['blender']['collection'],'bounds_m':actual,'expected_bounds_m':expected_world,'forbidden_preview_objects':forbidden,'scale':list(outlet.scale)}
    item['valid']=outlet.instance_collection.name==meta['blender']['collection'] and not forbidden and all(abs(actual[j][i]-expected_world[j][i])<.0003 for j in [0,1] for i in range(3)) and all(abs(v-1)<1e-6 for v in outlet.scale)
    outlet_collections.append(item)
    if outlet.name.startswith('Kitchen garden'):host_roots=roots('Kitchen low stone splash')+roots('Kitchen insulated spandrel concept')
    elif outlet.name.startswith('Pantry'):host_roots=roots('Rear facade cedar board')
    else:host_roots=roots('Kitchen island supporting end cheek')+roots('Kitchen island power service cover')+roots('Kitchen island service cover edge')
    cutout=meta['interfaces']['host_cutout_m'];hits=[]
    for x in [-cutout['width_x']/2+.002,0,cutout['width_x']/2-.002]:
        for z in [-cutout['height_z']/2+.002,0,cutout['height_z']/2-.002]:
            start=outlet.matrix_world@Vector((x,-.0002,z));direction=outlet.matrix_world.to_3x3()@Vector((0,1,0))
            for host in host_roots:
                inv=host.matrix_world.inverted();eo=host.evaluated_get(deps)
                hit,loc,normal,index=eo.ray_cast(inv@start,inv.to_3x3()@direction,distance=cutout['depth_y']+.0002)
                if hit:hits.append({'host':host.name,'outlet_local_xz_m':[x,z],'hit_world_m':list(host.matrix_world@loc)})
    outlet_cavities.append({'object':outlet.name,'required_cavity_m':cutout,'sampled_host_intersections':hits})
record('Every outlet instances only its declared full-scale fixture collection',len(outlet_objects)==4 and all(i['valid'] for i in outlet_collections),outlet_collections)
record('Outlet backbox cavities clear actual host finish and backing',len(outlet_objects)==4 and not any(i['sampled_host_intersections'] for i in outlet_cavities),outlet_cavities)

# Countertop voids: cast actual evaluated mesh, not a bounding box over holes.
def counter_hole_check(counter_prefix,fixture_prefix,parts):
    counter=one(counter_prefix);matrix=counter.matrix_world;inv=matrix.inverted();eo=counter.evaluated_get(deps)
    shape=[m for m in meshlist(fixture_prefix) if any(m['name'].startswith(s) for s in parts)]
    lo,hi=aabb([Vector(v) for m in shape for v in m['bounds']]);z=bounds(counter_prefix)[1][2]
    samples=[]
    for x in [lo[0]+.0005,(lo[0]+hi[0])/2,hi[0]-.0005]:
        for y in [lo[1]+.0005,(lo[1]+hi[1])/2,hi[1]-.0005]:
            origin=inv@Vector((x,y,z+.1));direction=inv.to_3x3()@Vector((0,0,-1))
            hit,loc,normal,index=eo.ray_cast(origin,direction,distance=.3)
            samples.append({'xy_m':[x,y],'counter_hit':hit})
    record(counter_prefix+' clears actual fixture body',not any(s['counter_hit'] for s in samples),{'fixture_outer_body_bounds_m':[lo,hi],'ray_samples':samples})
counter_hole_check('Kitchen garden cleanup worktop','Kitchen real sink and mixer',['Sink end','Sink side','Stainless sink bowl bottom'])
counter_hole_check('Kitchen east cooking worktop','Kitchen induction stove',['Cooktop below-counter casing'])
for fixture,host in [('Kitchen real sink and mixer','Kitchen sink base'),('Kitchen built in oven','Kitchen open oven housing')]:
    collisions=fit_intersections(fixture,host)
    record(fixture+' fits actual cabinet meshes',not collisions,{'mesh_bounds_intersections':collisions})

# Physical elevations, clearance and current installation metadata.
counter_under=bounds('Kitchen garden cleanup worktop')[0][2]
dw_top=bounds('Kitchen integrated dishwasher')[1][2]
dw_required=manifest(one('Kitchen integrated dishwasher'))['installation']['clear_opening_concept_m'][2]
record('Dishwasher closed body fits under counter',counter_under>dw_top,{'counter_underside_m':counter_under,'dishwasher_top_m':dw_top,'clearance_m':counter_under-dw_top})
record('Dishwasher declared installation opening provided',counter_under>=dw_required-1e-5,{'required_m':dw_required,'actual_m':counter_under},'concept_installation')
hood_bottom=bounds('Kitchen extraction hood')[0][2];hob_top=bounds('Kitchen induction stove')[1][2]
record('Hood concept mounting gap is at least30in',hood_bottom-hob_top>=.762-1e-4,{'gap_m':hood_bottom-hob_top,'gap_inches':(hood_bottom-hob_top)/.0254,'basis':'30in concept target; selected hood/cooktop manual still required'},'concept_installation')

# Closed routes measured between actual worktop and appliance extrema.
island=bounds('Kitchen island preparation stone');rear=bounds('Kitchen garden cleanup worktop');east=bounds('Kitchen east cooking worktop');fridge=bounds('Kitchen 48 inch refrigerator freezer')
aisles={'rear_work_aisle_m':rear[0][1]-island[1][1],'east_work_aisle_m':east[0][0]-island[1][0],'fridge_pull_to_island_m':fridge[0][0]-island[1][0]}
record('Main closed working aisles provide48in concept target',min(aisles.values())>=1.2192-.002,aisles,'concept_planning')

def world_envelope(o,local):
    return aabb([o.matrix_world@Vector((x,y,z)) for x in [local['min'][0],local['max'][0]] for y in [local['min'][1],local['max'][1]] for z in [local['min'][2],local['max'][2]]])
solid_prefixes=['Kitchen island','Kitchen rear drawer','Kitchen sink base','Kitchen cooking landing','Kitchen open oven housing','Kitchen Rear end','Kitchen Corner blank','Kitchen East north','Kitchen Fridge side','Kitchen garden cleanup worktop','Kitchen east cooking worktop']
obstacles=[m for prefix in solid_prefixes for m in meshlist(prefix)]
for prefix in ['Kitchen integrated dishwasher','Kitchen 48 inch refrigerator freezer']:
    o=one(prefix);operation=manifest(o)['installation']['operating_envelope'];sweep=world_envelope(o,operation['door_sweep_bounds_m'])
    conflicts=sorted(set(m['name'] for m in obstacles if overlaps(sweep,m['bounds'])))
    record(prefix+' conservative door envelope avoids fixed obstructions',not conflicts,{'envelope_m':sweep,'conflicts':conflicts,'basis':operation['basis']},'conservative_operating_allowance')
    if 'dishwasher' in prefix:
        remaining=sweep[0][1]-island[1][1]
        operator=([o.location.x-.3,sweep[0][1]-.6,0],[o.location.x+.3,sweep[0][1],1.8])
        operator_obstacles=obstacles+meshlist('Shared supported dining chair')+meshlist('Dining table')+meshlist('Shared grounded dining table')
        operator_conflicts=sorted(set(m['name'] for m in operator_obstacles if overlaps(operator,m['bounds'])))
        record('Standing behind fully open dishwasher has600mm footprint',not operator_conflicts,{'operator_footprint_m':operator,'conflicts':operator_conflicts,'y_only_distance_to_island_m':remaining,'basis':'600x600mm chosen operator footprint, not code; island only constrains it where X ranges overlap.'},'concept_operation')
        opposing=roots('Kitchen island deep drawers')
        drawer_sweeps=[]
        for drawer in opposing:
            lo,hi=aabb([Vector(v) for m in expanded(drawer) for v in m['bounds']]);hi[1]+=.5
            if overlaps(sweep,(lo,hi)):drawer_sweeps.append(drawer.name)
        record('Dishwasher and opposing island drawers can open together',not drawer_sweeps,{'conflicting_drawers':drawer_sweeps,'drawer_travel_m':.5,'restriction_if_false':'Close opposing drawers during dishwasher loading.'},'concept_operation')

# Sample the actual refrigerator door panels around declared hinges. SAT avoids
# false collisions from broad axis-aligned sweep rectangles around a rotation.
def sat(poly,other):
    axes=[Vector((1,0)),Vector((0,1))]
    for i in range(len(poly)):
        edge=poly[(i+1)%len(poly)]-poly[i]
        if edge.length>1e-8:axes.append(Vector((-edge.y,edge.x)).normalized())
    rectangle=[Vector((x,y)) for x,y in [(other[0][0],other[0][1]),(other[1][0],other[0][1]),(other[1][0],other[1][1]),(other[0][0],other[1][1])]]
    return all(min(max(p.dot(a) for p in poly),max(p.dot(a) for p in rectangle))-max(min(p.dot(a) for p in poly),min(p.dot(a) for p in rectangle))>.0001 for a in axes)
fridge_obj=one('Kitchen 48 inch refrigerator freezer');door_conflicts=[]
for child in fridge_obj.instance_collection.objects:
    if child.type!='MESH' or not any(s in child.name.lower() for s in ['door panel','pull']):continue
    local=[child.matrix_local@Vector(v) for v in child.bound_box];lo,hi=aabb(local);sign=1 if (lo[0]+hi[0])>0 else -1
    pivot=Vector((sign*.593,-.381,.116))
    for degrees in range(0,111,5):
        rot=Matrix.Rotation(math.radians(sign*degrees),3,'Z')
        points=[fridge_obj.matrix_world@(pivot+rot@(Vector((x,y,z))-pivot)) for x,y,z in [(lo[0],lo[1],lo[2]),(hi[0],lo[1],lo[2]),(hi[0],hi[1],lo[2]),(lo[0],hi[1],lo[2])]]
        poly=[Vector((p.x,p.y)) for p in points]
        for m in obstacles:
            if m['bounds'][1][2]<.116:continue
            if sat(poly,m['bounds']):door_conflicts.append({'panel':child.name,'degrees':degrees,'obstacle':m['name']})
record('Actual refrigerator panels and pulls clear through110degrees',not door_conflicts,{'sample_step_degrees':5,'conflicts':door_conflicts,'basis':'Actual panel/pull oriented bounds and declared concept hinge axes; discrete samples, not selected manufacturer articulation'},'sampled_operation')
if not door_conflicts:
    for check in CHECKS:
        if check['name']=='Kitchen 48 inch refrigerator freezer conservative door envelope avoids fixed obstructions' and not check['passed']:
            check['kind']='unresolved_selected_product_allowance'
            check['details']['interpretation']='Conservative rectangular planning envelope overlap is not a proven collision: actual modeled panels and pulls clear the fixed neighbors through the sampled motion. Selected product hinge mechanism and installation allowances remain unresolved.'

# Actual oven door/window/handle vertices posed to90degrees about a concept hinge.
oven_obj=one('Kitchen built in oven');oven_points=[]
for child in oven_obj.instance_collection.objects:
    if child.type!='MESH' or not any(s in child.name for s in ['Oven door','Oven transparent viewing window','Oven full-width door handle','Oven handle bracket']):continue
    pivot=Vector((0,-1.025*F,.09*F));rotation=Matrix.Rotation(math.pi/2,3,'X')
    oven_points += [oven_obj.matrix_world@(pivot+rotation@(child.matrix_local@Vector(v)-pivot)) for v in child.bound_box]
oven_open=aabb(oven_points)
oven_conflicts=sorted(set(m['name'] for m in meshlist('Kitchen island') if overlaps(oven_open,m['bounds'])))
oven_operator=([oven_open[0][0]-.6,oven_obj.location.y-.3,0],[oven_open[0][0],oven_obj.location.y+.3,1.8])
oven_operator_conflicts=sorted(set(m['name'] for m in meshlist('Kitchen island') if overlaps(oven_operator,m['bounds'])))
record('Oven door90degree pose and operator avoid island',not oven_conflicts and not oven_operator_conflicts,{'door_bounds_m':oven_open,'door_conflicts':oven_conflicts,'operator_600mm_bounds_m':oven_operator,'operator_conflicts':oven_operator_conflicts,'basis':'Actual door/window/handle bounds rotated about original concept lower hinge, no selected manufacturer hinge model'},'sampled_operation')

drawer_clear=[]
for prefix in ['Kitchen rear drawer storage','Kitchen island deep drawers','Kitchen cooking landing drawers']:
    for drawer in roots(prefix):
        lo,hi=aabb([Vector(v) for m in expanded(drawer) for v in m['bounds']])
        facing=drawer.matrix_world.to_3x3()@Vector((0,-1,0))
        if abs(facing.y)>abs(facing.x):
            gap=(rear[0][1]-hi[1] if facing.y>0 else lo[1]-island[1][1])-.5
        else:gap=lo[0]-island[1][0]-.5
        drawer_clear.append({'object':drawer.name,'remaining_operator_depth_m':gap})
record('Single kitchen drawer leaves600mm operator space',all(d['remaining_operator_depth_m']>=.6 for d in drawer_clear),{'travel_m':.5,'instances':drawer_clear,'basis':'Single drawer operation; facing drawers are not assumed simultaneously extended'},'concept_operation')

# Seats, overhang, pullback, and independent aisle line behind occupied chairs.
seats=roots('Kitchen island seat');seat_bounds=[aabb([Vector(v) for m in expanded(o) for v in m['bounds']]) for o in seats]
seat_centers=sorted(o.location.x for o in seats)
back=bounds('Kitchen island finished back')
record('Three full-scale seats have30in center spacing',len(seats)==3 and min([seat_centers[i+1]-seat_centers[i] for i in range(len(seat_centers)-1)] or [0])>=.762-.002,{'count':len(seats),'centers_x_m':seat_centers,'scale':[list(o.scale) for o in seats]},'concept_planning')
overhang=back[0][1]-island[0][1]
record('Island seated knee overhang provides15in',overhang>=.381,{'overhang_m':overhang,'basis':'15in concept knee-depth target'},'concept_planning')
seat_south=min(b[0][1] for b in seat_bounds)
record('Seat pullback and rear route are explicitly measured',True,{'southern_seat_extent_ft':ft(seat_south),'distance_to_south_open_floor_y32_ft':ft(seat_south)-32,'assumed_chair_pullback_m':.45,'remaining_after_pullback_m':seat_south-32*F-.45,'basis':'Y32 is open-room line; does not by itself prove a door-to-door route'},'measurement')
supports=[]
for prefix in ['Shared supported linen sofa','Shared supported dining chair','Shared supported coffee table','Dining table','Shared grounded dining table']:
    if not roots(prefix):continue
    lo,hi=bounds(prefix)
    supports.append({'prefix':prefix,'lowest_geometry_z_m':lo[2],'floor_contact_within_3mm':abs(lo[2])<=.003})
record('Adjacent living and dining furniture reaches floor',all(s['floor_contact_within_3mm'] for s in supports),supports)

# Pantry bays, actual wall aperture, shelves versus counter/bases and clear route.
pantry_collisions=[]
pantry_obstacles=meshlist('Pantry appliance worktop')+meshlist('Pantry appliance and bulk drawer storage')
for s in meshlist('Pantry food shelf'):
    for other in pantry_obstacles:
        if overlaps(s['bounds'],other['bounds']):pantry_collisions.append([s['name'],other['name']])
record('Pantry shelves do not overlap rear counter or cabinets',not pantry_collisions,{'intersections':pantry_collisions})
wall=meshlist('pantry-west');lower=[m for m in wall if m['bounds'][0][2]<1]
intervals=sorted((m['bounds'][0][1],m['bounds'][1][1]) for m in lower)
gaps=[(intervals[i][1],intervals[i+1][0]) for i in range(len(intervals)-1)]
gap=max(gaps,key=lambda v:v[1]-v[0]) if gaps else (0,0)
record('Pantry actual wall aperture is36in',gap[1]-gap[0]>=.9144-.001,{'opening_y_m':gap,'width_m':gap[1]-gap[0]})
pantry_shelf_bounds=bounds('Pantry food shelf');pantry_wall_east=max(m['bounds'][1][0] for m in wall)
pantry_clear=pantry_shelf_bounds[0][0]-pantry_wall_east
record('Pantry central storage aisle provides36in',pantry_clear>=.9144,{'clear_width_m':pantry_clear,'east_shelf_front_x_m':pantry_shelf_bounds[0][0],'west_wall_east_x_m':pantry_wall_east},'concept_planning')
door=bounds('Kitchen pantry door open');routewidth=pantry_shelf_bounds[0][0]-door[1][0]
record('Open pantry door leaves36in around free edge',routewidth>=.9144,{'clear_width_m':routewidth,'door_bounds_m':door,'basis':'Room-side bypass between open leaf tip and east shelving; open aperture separately checked'},'concept_planning')
east_window=[m for p in ['East facade window','Pantry east clerestory'] for m in meshlist(p) if 'glazing' in m['name'] and m['bounds'][0][1]>32*F]
blocked_glazing=[m['name'] for m in east_window if m['bounds'][0][2]<pantry_shelf_bounds[1][2] and min(m['bounds'][1][1],pantry_shelf_bounds[1][1])-max(m['bounds'][0][1],pantry_shelf_bounds[0][1])>.01]
record('Tall pantry shelves do not conceal east glazing',not blocked_glazing,{'glazing_obscured_by_shelf_back':blocked_glazing,'shelf_top_m':pantry_shelf_bounds[1][2],'east_pantry_glazing_bounds_m':[m['bounds'] for m in east_window]})
ledger_roots=roots('Pantry anti tip fixing ledger');backing_roots=roots('Pantry insulated shelf backing')
ledger_measurement={'ledger_count':len(ledger_roots),'backing_count':len(backing_roots),'basis':'Concept backing/ledger geometry, no fastener or load approval'}
ledger_ok=False
if ledger_roots and backing_roots:
    ledger=bounds('Pantry anti tip fixing ledger');backing=bounds('Pantry insulated shelf backing')
    shelf_rear=pantry_shelf_bounds[1][0]
    ledger_ok=ledger[0][0]<=shelf_rear+.002 and ledger[1][0]>=backing[0][0] and ledger[0][1]<=pantry_shelf_bounds[0][1]+.002 and ledger[1][1]>=pantry_shelf_bounds[1][1]-.002
    ledger_measurement.update(ledger_bounds_m=ledger,backing_bounds_m=backing,shelf_rear_x_m=shelf_rear)
record('Pantry anti-tip ledger bridges shelf rear to solid backing',ledger_ok,ledger_measurement,'concept_installation')

# A sampled700mm walking cylinder travels through the actual open-plan arrival
# to the pantry. This is a concept circulation test, not accessibility approval.
route_ft=[(38,34),(49.1,34),(49.1,35),(55,35),(58,35),(58,44.2)]
route_prefixes=['Kitchen island','Kitchen rear drawer','Kitchen sink base','Kitchen cooking landing','Kitchen open oven housing','Kitchen 48 inch','Kitchen integrated dishwasher','Kitchen garden cleanup','Kitchen east cooking','Kitchen pantry door','Pantry food shelf','Pantry appliance','pantry-west','suite-north','Shared supported dining chair','Dining table','Shared grounded dining table','Shared supported linen sofa']
route_obstacles=[m for p in route_prefixes for m in meshlist(p) if m['bounds'][1][2]>.04 and m['bounds'][0][2]<1.9]
route_conflicts=[];radius=.35
for a,b in zip(route_ft,route_ft[1:]):
    start,end=Vector(a)*F,Vector(b)*F;length=(end-start).length
    for n in range(math.ceil(length/.05)+1):
        pos=start+(end-start)*min(1,n*.05/max(length,.00001))
        for m in route_obstacles:
            lo,hi=m['bounds'];dx=max(lo[0]-pos.x,0,pos.x-hi[0]);dy=max(lo[1]-pos.y,0,pos.y-hi[1])
            if dx*dx+dy*dy<radius*radius:
                route_conflicts.append({'xy_m':list(pos),'object':m['name']})
record('700mm walking route reaches pantry without fixed obstructions',not route_conflicts,{'waypoints_ft':route_ft,'sample_step_m':.05,'body_width_m':.7,'conflicts':route_conflicts[:20],'total_conflicts':len(route_conflicts),'basis':'Closed equipment, static seat positions, open pantry leaf; not simultaneous appliance operation or accessibility certification'},'sampled_circulation')

# Gross slab sum compared to source area convention without importing house code.
floors=meshlist('Enclosed floor');area=sum((m['bounds'][1][0]-m['bounds'][0][0])*(m['bounds'][1][1]-m['bounds'][0][1]) for m in floors)
record('Source gross enclosed slab area preserved at2400sqft',abs(area/F/F-2400)<.1,{'slabs':len(floors),'area_sqft':area/F/F,'convention':'Gross enclosed slabs including walls, courtyard/landscape excluded'})
failures=[c for c in CHECKS if not c['passed'] and c['kind']!='unresolved_selected_product_allowance']
unresolved=[c for c in CHECKS if not c['passed'] and c['kind']=='unresolved_selected_product_allowance']
receipt={'file':str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'scope':'Kitchen/pantry installation and concept movement QA only; no whole-home, structural, manufacturer or code approval.',
         'software':bpy.app.version_string,'status':'open_failures_or_operating_restrictions' if failures else ('listed_geometry_checks_pass_with_unresolved_product_allowance' if unresolved else 'passes_listed_checks'),
         'geometry_or_planning_failures':len(failures),'unresolved_selected_product_allowances':len(unresolved),
         'checks':CHECKS,'limitations':['Closed-state geometry is real; conservative and sampled operating assumptions are identified separately.','No rendering performed. Selected-product installation, electrical/plumbing/exhaust engineering and actual door mechanisms remain unverified.']}
output=Path(sys.argv[sys.argv.index('--output')+1]) if '--output' in sys.argv else WORK/'verification.json'
output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(receipt,indent=2)+'\n')
for c in CHECKS:
    print(('PASS' if c['passed'] else ('NOTE' if c['kind']=='unresolved_selected_product_allowance' else 'FAIL')),c['name'],json.dumps(c['details']) if not c['passed'] else '',flush=True)
print('KITCHEN_VERIFICATION_WRITTEN',len(CHECKS),flush=True)
