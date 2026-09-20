"""Check the saved kitchen, actual linked meshes and explicit operating states.

Run with Blender -b homes/modern-block/model/modern-block.blend --python
tools/modern_block/verify_kitchen.py. This does not save or mutate the home file.
The JSON receipt reports failures as well as passes; an exception is not a pass.
"""
import hashlib
import json
import math
import sys
import traceback
from pathlib import Path

import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
import design as d
import kitchen_layout as k

HOME = ROOT / 'homes/modern-block'
TOL = .0006


def bounds(points):
    return tuple(min(p[i] for p in points) for i in range(3)) + tuple(
        max(p[i] for p in points) for i in range(3))


def union(parts):
    return tuple(min(p['bounds'][i] for p in parts) for i in range(3)) + tuple(
        max(p['bounds'][i] for p in parts) for i in range(3, 6))


def overlap(a, b, tolerance=TOL):
    return all(min(a[i+3], b[i+3])-max(a[i], b[i]) > tolerance for i in range(3))


def moving(obj):
    while obj:
        if obj.get('motion_kind'):
            return True
        obj = obj.parent
    return False


def part(obj, matrix, graph, owner, is_moving=False):
    evaluated = obj.evaluated_get(graph)
    mesh = evaluated.to_mesh()
    try:
        points = [matrix @ v.co for v in mesh.vertices]
        polygons = [tuple(p.vertices) for p in mesh.polygons]
    finally:
        evaluated.to_mesh_clear()
    if not points or not polygons:
        return None
    return {'name': obj.name, 'owner': owner, 'vertices': points,
            'polygons': polygons, 'bounds': bounds(points),
            'moving': is_moving, 'bvh': None}


def collection_parts(collection, transform, graph, owner, inherited=False):
    result = []
    transform = transform @ Matrix.Translation(-collection.instance_offset)
    for obj in collection.all_objects:
        matrix = transform @ obj.evaluated_get(graph).matrix_world
        motion = inherited or moving(obj)
        if obj.type == 'MESH':
            value = part(obj, matrix, graph, owner, motion)
            if value:
                result.append(value)
        elif obj.instance_type == 'COLLECTION' and obj.instance_collection:
            result += collection_parts(obj.instance_collection, matrix, graph, owner, motion)
    return result


def tree(p):
    if p['bvh'] is None:
        p['bvh'] = BVHTree.FromPolygons(p['vertices'], p['polygons'], all_triangles=False)
    return p['bvh']


def inside(point, p):
    """Parity ray for complete containment, separate from surface crossings."""
    direction = Vector((.87131, .39127, .28761)).normalized()
    start = point.copy()
    hits = 0
    for _ in range(128):
        location, normal, index, distance = tree(p).ray_cast(start, direction, 100)
        if location is None:
            return bool(hits % 2)
        if distance < TOL:
            return False  # A seated/contact surface is not penetration.
        hits += 1
        start = location + direction * .00001
    return False


def penetrates(a, b):
    if not overlap(a['bounds'], b['bounds']):
        return False
    if tree(a).overlap(tree(b)):
        return True
    # BVH surface overlap alone misses a solid wholly inside another solid.
    for source, target in [(a, b), (b, a)]:
        bb = target['bounds']
        for point in source['vertices'][::max(1, len(source['vertices'])//12)]:
            if all(bb[i]+TOL < point[i] < bb[i+3]-TOL for i in range(3)) and inside(point, target):
                return True
    return False


def serial_bounds(parts):
    b = union(parts)
    return {'min': list(b[:3]), 'max': list(b[3:])}


def transform_bounds(local, matrix):
    lo, hi = local['min'], local['max']
    return bounds([matrix @ Vector((x,y,z)) for x in [lo[0],hi[0]]
                   for y in [lo[1],hi[1]] for z in [lo[2],hi[2]]])


def check_kitchen(receipt):
    failures = receipt['failures']
    def require(condition, message, details=None):
        if not condition:
            failures.append({'check': message, 'details': details})
        return condition

    native = HOME/'model/modern-block.blend'
    if not require(Path(bpy.data.filepath).resolve() == native.resolve(), 'Saved home must be freshly opened'):
        return
    receipt['native_sha256'] = hashlib.sha256(native.read_bytes()).hexdigest()
    receipt['native_reopened'] = True
    bpy.context.view_layer.update()
    graph = bpy.context.evaluated_depsgraph_get()
    instances = {obj.name: obj for obj in bpy.context.scene.objects
                 if obj.instance_type == 'COLLECTION' and obj.instance_collection
                 and obj.name.startswith(('Kitchen ', 'Pantry '))}
    required = ['Kitchen bridge sink', 'Kitchen cream sink base',
                'Kitchen concealed dishwasher 1', 'Kitchen concealed dishwasher 2',
                'Kitchen cream brass range', 'Kitchen cream capture hood',
                'Kitchen concealed refrigeration', 'Kitchen island microwave',
                'Kitchen island microwave housing', 'Kitchen island waste and recycling',
                'Pantry appliance garage', 'Pantry enclosed food storage']
    missing = [name for name in required if name not in instances]
    if not require(not missing, 'Required kitchen equipment is present', missing):
        return

    closed, metadata = {}, {}
    for name, obj in instances.items():
        require(all(abs(x-1) < .00001 for x in obj.scale), 'Rigid linked asset scale', name)
        library = obj.instance_collection.library
        if not require(library is not None, 'Kitchen instances use pinned linked collections', name):
            continue
        path = Path(bpy.path.abspath(library.filepath)).resolve()
        manifest_path = path.parent/'asset.json'
        if not require(manifest_path.is_file(), 'Asset manifest exists', str(path.relative_to(ROOT))):
            continue
        meta = json.loads(manifest_path.read_text())
        metadata[name] = (meta, path)
        declared_closed = meta.get('blender',{}).get('collection')
        if declared_closed:
            require(obj.instance_collection.name == declared_closed,
                    'Canonical saved operating state is closed', name)
        closed[name] = collection_parts(obj.instance_collection, obj.matrix_world, graph, name)
        require(bool(closed[name]), 'Evaluated linked mesh geometry exists', name)
    if failures:
        return
    receipt['closed_instances'] = {name: {'asset_id': metadata[name][0]['id'],
         'version': metadata[name][0]['version'], 'parts': len(parts),
         'actual_world_bounds_m': serial_bounds(parts)} for name, parts in closed.items()}
    chase=[o.name for o in bpy.context.scene.objects if o.name.startswith('Kitchen cream hood service chase')]
    require(len(chase)==4,'Hood duct has four modeled service-chase faces',chase)
    receipt['hood_service_chase_objects']=chase

    # Actual local host meshes and actual partition segments, including doors.
    host = []
    region = (9.5,12.7,-.02,19.4,20.3,3.7)
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH':
            continue
        if not (obj.name.startswith(('Kitchen ', 'Pantry ', 'Service ', 'Main rear', 'Main courtyard'))):
            continue
        p = part(obj, obj.matrix_world, graph, obj.name)
        if p and overlap(p['bounds'], region):
            host.append(p)
    counters = [p for p in host if p['owner'].startswith('Kitchen cleanup counter stone')]
    island = [p for p in host if p['owner'].startswith('Kitchen island stone')]
    require(len(counters) == 4, 'Sink counter is four separate regions around a real opening', len(counters))
    require(len(island) == 1, 'Island has one continuous top', len(island))
    if not counters or not island:
        return
    ib = union(island)
    require(all(abs(a-b) < .001 for a,b in zip((ib[0],ib[1],ib[3],ib[4]), k.ISLAND)),
            'Actual island matches coordinated footprint', list(ib))
    require(abs(ib[3]-ib[0]-1.45) < .001 and abs(ib[4]-ib[1]-3.4) < .001,
            'Island remains 3.4 by 1.45 meters')
    require(abs(ib[5]-(d.GROUND+k.COUNTER_TOP)) < .001, 'Finished countertop height', ib[5])

    # Rays through the actual counter reject a solid mesh hidden inside the bowl.
    sx, sy = k.SINK
    aperture_hits = []
    for x in [sx-.30,sx,sx+.30]:
        for y in [sy-.20,sy,sy+.20]:
            for p in counters:
                hit = tree(p).ray_cast(Vector((x,y,d.GROUND+k.COUNTER_TOP+.10)),Vector((0,0,-1)),.20)[0]
                if hit is not None:
                    aperture_hits.append([x,y,p['name']])
    require(not aperture_hits, 'Counter opening has no hidden faces beneath sink bowl', aperture_hits)
    bowl = [p for p in closed['Kitchen bridge sink'] if p['bounds'][2] < d.GROUND+k.COUNTER_TOP-.01]
    bowl_collisions = []
    for a in bowl:
        for b in counters + closed['Kitchen cream sink base']:
            if penetrates(a,b):
                bowl_collisions.append([a['name'],b['name']])
    require(bool(bowl) and not bowl_collisions, 'Actual bowl fits counter cutout and sink-base cavity', bowl_collisions)
    receipt['sink'] = {'counter_regions':len(counters), 'aperture_rays':9,
                       'bowl_parts':len(bowl), 'bowl_host_collisions':bowl_collisions}

    # Cavity fit is checked using the complete installed microwave, not its name.
    microwave = closed['Kitchen island microwave']
    housing = closed['Kitchen island microwave housing']
    cavity = metadata['Kitchen island microwave housing'][0]['installation']['appliance_opening_m']
    housing_obj = instances['Kitchen island microwave housing']
    local_points = [housing_obj.matrix_world.inverted() @ v for p in microwave for v in p['vertices']]
    mb = bounds(local_points)
    require(mb[0] >= -cavity['width']/2-TOL and mb[3] <= cavity['width']/2+TOL
            and mb[2] >= cavity['bottom_z']-TOL and mb[5] <= cavity['top_z']+TOL,
            'Microwave actual envelope fits cabinet opening', list(mb))
    micro_collisions = [[a['name'],b['name']] for a in microwave for b in housing if penetrates(a,b)]
    require(not micro_collisions, 'Microwave does not intersect housing or shelf', micro_collisions)
    supports = [p for p in housing if 'load support shelf' in p['name'].lower()]
    require(bool(supports), 'Microwave has a modeled load-support shelf')
    support_gap = min(p['bounds'][2] for p in microwave)-max(p['bounds'][5] for p in supports) if supports else None
    require(support_gap is not None and -.001 <= support_gap <= .010,
            'Microwave mounting plane is within 10mm fitting/shim allowance of shelf', support_gap)
    receipt['microwave_cavity'] = {'actual_local_bounds_m':list(mb), 'opening_m':cavity,
                                  'support_gap_m':support_gap, 'collisions':micro_collisions}

    # Cooking equipment is truly full size and is beside, not across, the window.
    rb = union(closed['Kitchen cream brass range'])
    hb = union(closed['Kitchen cream capture hood'])
    require(abs((rb[3]-rb[0])-1.2192) < .012, 'Range actual width is 48 inches', rb[3]-rb[0])
    require(abs((hb[3]-hb[0])-1.2192) < .012, 'Hood actual width is 48 inches', hb[3]-hb[0])
    openings = json.loads((HOME/'model/opening-schedule.json').read_text())
    rear_windows = [o for o in openings if o['name']=='Main rear' and o['kind']=='window'
                    and max(o['a'][0],o['b'][0]) < 13]
    require(bool(rear_windows), 'Existing north cleanup window is recorded')
    window_right = max(max(o['a'][0],o['b'][0]) for o in rear_windows) if rear_windows else 0
    require(hb[0]-window_right >= .05, 'Hood clears north window by at least 50mm', hb[0]-window_right)
    receipt['cooking'] = {'range_bounds_m':list(rb), 'hood_bounds_m':list(hb),
                           'hood_to_window_horizontal_m':hb[0]-window_right}

    opened, temporary = {}, []
    try:
        for name,(meta,path) in metadata.items():
            open_name = meta.get('blender',{}).get('operating_collections',{}).get('open')
            if not open_name:
                continue
            with bpy.data.libraries.load(str(path),link=True) as (source,target):
                if not require(open_name in source.collections, 'Declared open collection exists', name):
                    continue
                target.collections = [open_name]
            collection = target.collections[0]
            obj = bpy.data.objects.new('Verification temporary '+name,None)
            obj.instance_type='COLLECTION'; obj.instance_collection=collection
            obj.matrix_world=instances[name].matrix_world.copy()
            bpy.context.scene.collection.objects.link(obj); temporary.append(obj)
        bpy.context.view_layer.update()
        graph = bpy.context.evaluated_depsgraph_get()
        for obj in temporary:
            name = obj.name.removeprefix('Verification temporary ')
            opened[name] = collection_parts(obj.instance_collection,obj.matrix_world,graph,name)
        for name in required[2:]:
            if name not in ['Kitchen island microwave housing']:
                require(name in opened, 'Required equipment has an actual open-state collection', name)

        operation_results = {}
        all_fixed = host + [p for parts in closed.values() for p in parts]
        for name,parts in opened.items():
            motions = [p for p in parts if p['moving']]
            if not motions:
                # A decorative island back has no mechanism despite an exported
                # matching collection; it is not counted as an operating check.
                if name in required[2:]:
                    require(False, 'Open state contains explicitly marked moving geometry', name)
                continue
            static_obstacles = [p for p in all_fixed if p['owner'] != name]
            collisions = []
            for a in motions:
                for b in static_obstacles:
                    if penetrates(a,b):
                        collisions.append([a['name'],b['owner'],b['name']])
            require(not collisions, 'Open equipment clears neighboring cabinets, counters and partitions: '+name, collisions)
            meta = metadata[name][0]
            envelope = meta.get('operating_envelope',meta.get('installation',{}).get('operating_envelope',{}))
            declared = envelope.get('open_bounds_m')
            actual = union(parts)
            if declared:
                expected = transform_bounds(declared,instances[name].matrix_world)
                require(all(abs(a-b)<.003 for a,b in zip(actual,expected)),
                        'Actual open bounds agree with published state: '+name,
                        {'actual':list(actual),'declared':list(expected)})
            operation_results[name] = {'moving_meshes':len(motions),
                'actual_open_bounds_m':list(actual),'collisions':collisions}

        # These groups correspond to the demonstrable simultaneous-use scenes.
        groups = {
            'rear_equipment': ['Kitchen concealed dishwasher 1','Kitchen concealed dishwasher 2',
                               'Kitchen cream brass range','Kitchen concealed refrigeration'],
            'island_equipment': ['Kitchen island microwave','Kitchen island waste and recycling'],
            'pantry_equipment': ['Pantry appliance garage','Pantry enclosed food storage'],
        }
        receipt['simultaneous_open_groups'] = {}
        for group,names in groups.items():
            collisions=[]
            for i,a_name in enumerate(names):
                for b_name in names[i+1:]:
                    for a in opened.get(a_name,[]):
                        for b in opened.get(b_name,[]):
                            if (a['moving'] or b['moving']) and penetrates(a,b):
                                collisions.append([a_name,a['name'],b_name,b['name']])
            require(not collisions,'Simultaneous open group clears: '+group,collisions)
            receipt['simultaneous_open_groups'][group]={'instances':names,'collisions':collisions}

        # Evaluate a real standing zone beyond each open footprint. Bounds are
        # conservative, and only obstacles spanning the person's width/height
        # participate. This is an explicit concept target, not a code assertion.
        operator_results={}
        operator_names=[n for names in groups.values() for n in names]
        for name in operator_names:
            if name not in opened:
                continue
            transform=instances[name].matrix_world
            front=(transform.to_3x3() @ Vector((0,-1,0))).normalized()
            transverse=(transform.to_3x3() @ Vector((1,0,0))).normalized()
            front_edge=max(v.dot(front) for p in opened[name] for v in p['vertices'])
            center=instances[name].location.dot(transverse)
            nearest=10.0; blocker=None
            for p in all_fixed:
                if p['owner']==name or p['bounds'][5] < d.GROUND+.06 or p['bounds'][2] > d.GROUND+1.85:
                    continue
                vals=[v.dot(transverse) for v in p['vertices']]
                if max(vals) < center-.30 or min(vals) > center+.30:
                    continue
                projected=[v.dot(front) for v in p['vertices']]
                if max(projected) <= front_edge+TOL:
                    continue
                distance=max(0,min(projected)-front_edge)
                if distance<nearest:
                    nearest=distance;blocker=p['owner']
            require(nearest>=.80-TOL,'800mm operator space beyond open equipment: '+name,
                    {'clear_m':nearest,'nearest_obstacle':blocker})
            operator_results[name]={'clear_m':nearest if blocker else None,
                                    'target_zone_clear':nearest>=.80-TOL,
                                    'nearest_obstacle':blocker,
                                    'reserved_width_m':.60,'required_depth_m':.80}
        receipt['operator_spaces']=operator_results

        fridge_name='Kitchen concealed refrigeration'
        fmeta=metadata[fridge_name][0]
        swept=fmeta.get('operating_envelope',{}).get('conservative_swept_bounds_m')
        require(swept is not None,'Refrigerator publishes sampled full-sweep bounds')
        if swept:
            sw=transform_bounds(swept,instances[fridge_name].matrix_world)
            partitions=[p for p in host if p['owner'].startswith('Service west')
                        and p['bounds'][1]<sw[4] and p['bounds'][4]>sw[1]]
            require(bool(partitions),'East partition exists beside refrigerator sweep')
            clearance=min(p['bounds'][0] for p in partitions)-sw[3] if partitions else None
            require(clearance is not None and clearance>=.005,
                    'Entire declared refrigerator sweep clears east partition by at least 5mm',clearance)
            receipt['refrigerator_sweep']={'actual_open_bounds_m':list(union(opened[fridge_name])),
                'published_conservative_sweep_world_bounds_m':list(sw),'east_partition_clearance_m':clearance,
                'basis':'Published sampled mechanism envelope transformed by actual rigid installation; actual final-state moving meshes checked separately.'}
        receipt['open_states']=operation_results
    finally:
        for obj in temporary:
            bpy.data.objects.remove(obj,do_unlink=True)


def main():
    receipt={'status':'failed','native_reopened':False,'blender':bpy.app.version_string,
             'failures':[], 'limitations':[
        'Concept geometry only; no manufacturer, electrical, gas, ventilation or code certification.',
        'Surface intersections and sampled containment use 0.6mm broad-phase tolerance; exact fittings remain unselected.',
        'Open collections verify explicit final operating states. Only the refrigerator additionally checks its published sampled full-sweep bound against the east partition.',
        'Operator zones reserve 600mm width and 800mm depth beyond open equipment against scoped kitchen/pantry assets and adjacent host partitions. A null clear_m means no obstacle was found in the scanned geometry, not unlimited clearance; these checks do not certify accessibility or concurrent human movement.',
        'Microwave shelf allows up to 10mm fitting/shim space; exact anchorage and ventilation require product selection.'
    ]}
    try:
        check_kitchen(receipt)
    except Exception as error:
        receipt['failures'].append({'check':'Verification exception','details':str(error)})
        receipt['exception_traceback']=traceback.format_exc()
    if not receipt['failures']:
        receipt['status']='passed'
    output=HOME/'model/kitchen-validation.json'
    output.write_text(json.dumps(receipt,indent=2)+'\n')
    print('MODERN_BLOCK_KITCHEN_'+receipt['status'].upper(),json.dumps(receipt),flush=True)
    if receipt['failures']:
        raise RuntimeError('Kitchen verification failed; see model/kitchen-validation.json')


if __name__=='__main__':
    main()
