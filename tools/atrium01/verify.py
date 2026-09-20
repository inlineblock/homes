"""Fresh native verification for the metric Atrium 01 courtyard concept.

Run Blender --factory-startup --background homes/atrium-01/model/atrium-01.blend
--python-exit-code 1 --python tools/atrium01/verify.py. Never saves the model.
Measured geometry and conceptual clearance reservations are reported separately.
"""
import hashlib
import json
import math
import sys
import traceback
from collections import deque
from pathlib import Path
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
import design as d
HOME = ROOT / 'homes/atrium-01'
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
            'moving': is_moving, 'blind_part': obj.get('blind_part'), 'bvh': None}


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



def rect_union_area(rectangles):
    xs = sorted({r[i] for r in rectangles for i in (0, 2)})
    area = 0.0
    for left, right in zip(xs, xs[1:]):
        ys = sorted((r[1], r[3]) for r in rectangles if r[0] < (left+right)/2 < r[2])
        length = 0.0
        end = -math.inf
        for low, high in ys:
            length += max(0, high-max(low, end))
            end = max(end, high)
        area += (right-left)*length
    return area


def convex_hull(points):
    pts = sorted({(round(v[0], 5), round(v[1], 5)) for v in points})
    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    halves = []
    for sequence in (pts, list(reversed(pts))):
        half = []
        for p in sequence:
            while len(half) >= 2 and cross(half[-2], half[-1], p) <= 0:
                half.pop()
            half.append(p)
        halves.append(half[:-1])
    return halves[0]+halves[1]


def distance_to_polygon(x, y, polygon):
    inside_poly = True
    minimum = math.inf
    for a, b in zip(polygon, polygon[1:]+polygon[:1]):
        dx, dy = b[0]-a[0], b[1]-a[1]
        if dx*(y-a[1])-dy*(x-a[0]) < -1e-8:
            inside_poly = False
        t = max(0, min(1, ((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy or 1)))
        minimum = min(minimum, math.hypot(x-a[0]-t*dx, y-a[1]-t*dy))
    return 0 if inside_poly else minimum


def shifted_part(p, transform):
    points = [transform @ v for v in p['vertices']]
    return dict(p, vertices=points, bounds=bounds(points), bvh=None)


def room_contains(rect, location, margin=0):
    return rect[0]+margin <= location[0] <= rect[2]-margin and rect[1]+margin <= location[1] <= rect[3]-margin


class Audit:
    def __init__(self):
        self.report = {'status': 'failed', 'blender': bpy.app.version_string,
                       'failures': [], 'checks': {}, 'limitations': [
            'Architectural concept checks, not product selection, engineering, permit or code approval.',
            'Solid collision checks use evaluated meshes, surface intersections and sampled containment with 0.6mm broad-phase tolerance.',
            'Legacy appliance and cabinet motion is a published conservative reservation, not an animated native mechanism. Hinged architectural leaves are sampled every five degrees; intermediate continuous collision is not certified.',
            'Routes use a 600mm diameter body, 100mm grid and actual obstacle footprints; this is a concept reachability check, not accessibility certification.',
            'Area is gross enclosed floor footprint including wall thickness, excluding courtyard, parking, canopy and terraces; not net usable floor area.',
        ]}

    def require(self, condition, name, details=None):
        if not condition:
            self.report['failures'].append({'check': name, 'details': details})
        return condition

    def run(self):
        native = HOME/'model/atrium-01.blend'
        if not self.require(Path(bpy.data.filepath).resolve() == native.resolve(), 'Freshly reopened target native'):
            return
        self.report['native_sha256'] = hashlib.sha256(native.read_bytes()).hexdigest()
        self.report['native_reopened'] = True
        self.require(bpy.context.scene.unit_settings.scale_length == 1, 'Native unit scale is meters')
        libraries = []
        for lib in bpy.data.libraries:
            path = Path(bpy.path.abspath(lib.filepath)).resolve()
            self.require(lib.filepath.startswith('//') and path.is_file() and path.is_relative_to(ROOT/'library'),
                         'Portable pinned library dependency', lib.filepath)
            libraries.append({'relative_path': lib.filepath, 'resolved': path.is_file()})
        self.report['asset_links'] = libraries
        bpy.context.view_layer.update()
        graph = bpy.context.evaluated_depsgraph_get()
        self.instances = {o.name:o for o in bpy.context.scene.objects if o.instance_type == 'COLLECTION' and o.get('asset_id')}
        self.assets, self.meta = {}, {}
        for name, obj in self.instances.items():
            asset_id, version = obj['asset_id'], obj['asset_version']
            self.require(all(abs(v-1)<1e-5 for v in obj.scale), 'Rigid linked asset scale', name)
            path = ROOT/'library'/asset_id/version/'asset.json'
            self.require(path.is_file(), 'Pinned asset manifest exists', name)
            if not path.is_file():
                continue
            self.meta[name] = json.loads(path.read_text())
            # Exclude thousands of plant leaves/tile flutes from interior geometry QA.
            if asset_id.split('/')[0] in ('furniture','cabinetry','appliances','fixtures') and not any(w in asset_id for w in ('lighting-', 'pendant', 'outlet')):
                self.require(not obj.hide_render and any(not c.hide_render for c in obj.users_collection),
                             'Required furnishings remain visible in canonical render collections',name)
                self.assets[name] = collection_parts(obj.instance_collection, obj.matrix_world, graph, name)
                self.require(bool(self.assets[name]), 'Evaluated asset has actual mesh geometry', name)
        self.host = []
        self.objects = {}
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                p = part(obj, obj.matrix_world, graph, obj.name)
                if p:
                    self.host.append(p)
                    self.objects[obj.name] = obj
        self.solids = [p for p in self.host if self.objects[p['name']].get('ifc_class') in ('IfcWall','IfcWindow','IfcColumn')]
        self.interior_fixed = self.solids + [p for p in self.host if p['name'].startswith(('Kitchen ', 'Island ', 'Cleanup ', 'Cooking ', 'Pantry ', 'Primary ', 'Ensuite ', 'Shared ', 'Laundry ', 'Utility ', 'Entry ', 'Living ', 'Dining ', 'Foyer ', 'Bedroom ')) or self.objects[p['name']].get('concept_allowance_only')]
        self.all_parts = self.interior_fixed + [p for parts in self.assets.values() for p in parts]
        self.report['linked_instances'] = {name:{'asset_id':self.instances[name]['asset_id'], 'parts':len(parts),
            'actual_world_bounds_m':serial_bounds(parts)} for name,parts in self.assets.items()}
        self.metadata = json.loads((HOME/'model/design-metadata.json').read_text())
        self.area_and_heights()
        self.program_and_fits()
        self.kitchen()
        self.fixture_and_storage_access()
        self.arrival()
        open_doors = self.doors()
        self.sliders()
        self.shades()
        self.routes(open_doors)

    def area_and_heights(self):
        floors = [p for p in self.host if self.objects[p['name']].get('floor_area_role') == 'conditioned']
        self.require(len(floors)==4, 'Four measured conditioned floor regions', len(floors))
        rectangles = [(p['bounds'][0],p['bounds'][1],p['bounds'][3],p['bounds'][4]) for p in floors]
        area = rect_union_area(rectangles)
        self.require(abs(area/d.FT**2-2400)<.05, 'Measured gross enclosed footprint is 2400 square feet', area/d.FT**2)
        self.require(all(abs(p['bounds'][5])<.001 for p in floors), 'Actual finished floor datum is zero')
        self.floor_rects = rectangles
        groups = [('main_beams',('Primary bay beam','Longitudinal support beam'),d.BEAM_CLEAR),
                  ('ceiling_plane',('Pale tongue-and-groove ceiling',),d.HEIGHT),
                  ('service_ceilings',('Service zone ceiling',),d.SERVICE_CLEAR)]
        heights = {}
        for name, prefixes, expected in groups:
            parts = [p for p in self.host if any((w in p['name'] if w.startswith(' ') else p['name'].startswith(w)) for w in prefixes)]
            values = [p['bounds'][2] for p in parts]
            self.require(bool(values) and all(abs(z-expected)<.001 for z in values), 'Measured underside '+name, values)
            heights[name] = {'count':len(values),'lowest_m':min(values) if values else None,'required_m':expected}
        center = Vector(((d.ATRIUM[0]+d.ATRIUM[2])/2,(d.ATRIUM[1]+d.ATRIUM[3])/2,5))
        roof = [p for p in self.host if self.objects[p['name']].get('ifc_class') == 'IfcRoof']
        court_hits = [p['name'] for p in floors+roof if tree(p).ray_cast(center,Vector((0,0,-1)),6)[0] is not None]
        self.require(not court_hits, 'Atrium remains open sky and excluded floor area', court_hits)
        self.report['gross_enclosed_area_sqft'] = area/d.FT**2
        self.report['checks']['area_and_heights'] = {'floor_bounds_m':rectangles,'ceilings':heights,'courtyard_hits':court_hits}

    def program_and_fits(self):
        rooms = {name:rect for name,rect,label in d.ROOMS}
        beds = [name for name in self.assets if self.instances[name].get('bed_count')==1]
        self.require(len(beds)==3, 'Exactly three actual full-size linked beds', beds)
        for room in ('primary','bedroom-2','bedroom-3'):
            found = [name for name in beds if room_contains(rooms[room],self.instances[name].location)]
            self.require(len(found)==1, 'One actual bed in '+room, found)
            for name in found:
                inv = self.instances[name].matrix_world.inverted()
                b = bounds([inv @ v for p in self.assets[name] for v in p['vertices']])
                self.require(b[3]-b[0]>=1.45 and b[4]-b[1]>=1.90, 'Full-size bed envelope', {'name':name,'bounds_m':b})
        wardrobes = [name for name in self.assets if 'wardrobe' in self.instances[name]['asset_id']]
        for room, storage in [('primary',None),('bedroom-2','wardrobe-2'),('bedroom-3','wardrobe-3')]:
            zones = [rooms[room]] + ([rooms[storage]] if storage else [])
            found = [name for name in wardrobes if any(room_contains(r,self.instances[name].location) for r in zones)]
            self.require(bool(found), 'Modeled wardrobe storage for '+room, found)
        fixtures = {}
        for room in ('primary-bath','bath-2','bath-3'):
            zones = [rooms[room]] + ([rooms['primary-wc']] if room=='primary-bath' else [])
            actual = [name for name in self.assets if any(room_contains(r,self.instances[name].location) for r in zones)]
            for fixture in ('toilet','shower','vanity-basin'):
                matched = [name for name in actual if fixture in self.instances[name]['asset_id']]
                self.require(bool(matched),'Actual '+fixture+' in '+room,actual)
            fixtures[room] = actual
        primary = fixtures['primary-bath']
        self.require(any('freestanding-tub' in self.instances[n]['asset_id'] for n in primary), 'Primary separate tub')
        self.require(sum('vanity-basin' in self.instances[n]['asset_id'] for n in primary)==2, 'Primary double vanity')
        fixture_heights = {}
        for name,parts in self.assets.items():
            if 'vanity-basin' in self.instances[name]['asset_id']:
                basin = [p for p in parts if 'basin' in p['name'].lower() and 'mirror' not in p['name'].lower()]
                top = max(p['bounds'][5] for p in basin) if basin else None
                self.require(top is not None and .80<=top<=.97, 'Realistic vanity basin rim height', {'name':name,'rim_m':top})
                fixture_heights[name] = top
        collisions=[]
        for name,parts in self.assets.items():
            slug=self.instances[name]['asset_id']
            if slug.split('/')[0] not in ('furniture','cabinetry','appliances') and not any(w in slug for w in ('toilet-','freestanding-tub','shower-tray')):
                continue
            for a in parts:
                for b in self.solids:
                    if penetrates(a,b):
                        collisions.append([name,a['name'],b['name']])
        self.require(not collisions, 'Actual rigid interior equipment clears walls, glass and columns', collisions)
        self.report['bedrooms']=len(beds)
        self.report['bathrooms']=len(fixtures)
        self.report['checks']['program']={'beds':beds,'wardrobes':wardrobes,'bathroom_assets':fixtures,'vanity_rims_m':fixture_heights,'envelope_collisions':collisions}

    def find_metadata(self, key):
        pending = [self.metadata]
        while pending:
            value = pending.pop()
            if isinstance(value,dict):
                if key in value:
                    return value[key]
                pending.extend(value.values())
            elif isinstance(value,list):
                pending.extend(value)
        return None

    def front_clearance(self, obj, front_edge, parts, excluded=(), width=.60):
        front=(obj.matrix_world.to_3x3() @ Vector((0,-1,0))).normalized()
        transverse=(obj.matrix_world.to_3x3() @ Vector((1,0,0))).normalized()
        center=obj.location.dot(transverse)
        nearest=math.inf
        blocker=None
        for p in parts:
            if p['owner'] in excluded or p['bounds'][5]<.06 or p['bounds'][2]>1.85:
                continue
            vals=[v.dot(transverse) for v in p['vertices']]
            if max(vals)<center-width/2 or min(vals)>center+width/2:
                continue
            projected=[v.dot(front) for v in p['vertices']]
            if max(projected)<=front_edge+TOL:
                continue
            gap=max(0,min(projected)-front_edge)
            if gap<nearest:
                nearest=gap;blocker=p['owner']
        return nearest,blocker

    def kitchen(self):
        records={}
        required=('Kitchen oven 30 inch','Kitchen refrigerator freezer 48 inch',
                  'Kitchen integrated dishwasher','Kitchen real bowl and mixer')
        if not self.require(all(name in self.assets for name in required), 'Full-size kitchen equipment is installed', list(self.assets)):
            return
        openings=self.find_metadata('counter_openings') or []
        self.require(len(openings)>=2,'Sink and cooktop have recorded counter apertures',openings)
        for opening in openings:
            x0,y0,x1,y1=opening['bounds_m']; z=opening['top_m']
            counters=[p for p in self.host if p['name'].startswith(opening['counter'])]
            hits=[]
            for tx in (.1,.5,.9):
                for ty in (.1,.5,.9):
                    origin=Vector((x0+(x1-x0)*tx,y0+(y1-y0)*ty,z+.03))
                    for p in counters:
                        if tree(p).ray_cast(origin,Vector((0,0,-1)),.13)[0] is not None:
                            hits.append(p['name'])
            self.require(bool(counters) and not hits,'Actual countertop hole '+opening['counter'],hits)
        sink=self.assets['Kitchen real bowl and mixer']
        sink_base=self.assets.get('Kitchen accessible sink cabinet',[])
        counter=[p for p in self.host if p['name'].startswith('Kitchen cleanup worktop')]
        bowl=[p for p in sink if p['bounds'][2]<.90]
        hits=[[a['name'],b['name']] for a in bowl for b in sink_base+counter if penetrates(a,b)]
        self.require(bool(bowl) and bool(sink_base) and not hits,'Actual sink bowl fits host counter and cabinet',hits)
        oven=self.assets['Kitchen oven 30 inch']
        housing=self.assets.get('Kitchen open oven housing',[])
        hits=[[a['name'],b['name']] for a in oven for b in housing if penetrates(a,b)]
        self.require(bool(housing) and not hits,'Actual oven fits open housing',hits)
        oven_z=union(oven)[2]
        support=[p for p in housing if 'support' in p['name'].lower() and p['bounds'][5]<=oven_z+.002]
        support_gap=oven_z-max(p['bounds'][5] for p in support) if support else None
        self.require(support_gap is not None and -.001<=support_gap<=.010,'Oven has actual load shelf within10mm fitting allowance',support_gap)
        island=[p for p in self.host if p['name'].startswith('Island pale stone worktop')]
        ib=union(island) if island else None
        self.require(ib is not None and all(abs(a-b)<.002 for a,b in zip((ib[0],ib[1],ib[3],ib[4]),d.KITCHEN_ISLAND)), 'Actual island matches plan',ib)
        equipment=[('Kitchen refrigerator freezer 48 inch',None),('Kitchen integrated dishwasher',None),
                   ('Kitchen oven 30 inch',.72)]
        for name,fallback in equipment:
            obj=self.instances[name];meta=self.meta[name]
            envelope=meta.get('operating_envelope',meta.get('installation',{}).get('operating_envelope',{}))
            swept=envelope.get('conservative_swept_bounds_m',envelope.get('door_sweep_bounds_m'))
            front=(obj.matrix_world.to_3x3() @ Vector((0,-1,0))).normalized()
            closed_edge=max(v.dot(front) for p in self.assets[name] for v in p['vertices'])
            if swept:
                sw=transform_bounds(swept,obj.matrix_world)
                corners=[Vector((x,y,z)) for x in (sw[0],sw[3]) for y in (sw[1],sw[4]) for z in (sw[2],sw[5])]
                open_edge=max(v.dot(front) for v in corners)
                clashes=[p['owner'] for p in self.all_parts if p['owner']!=name and overlap(sw,p['bounds'])]
                self.require(not clashes,'Published conservative equipment sweep clears host: '+name,sorted(set(clashes)))
                basis='Published conservative whole-sweep reservation transformed by actual rigid installation.'
            else:
                self.require(fallback is not None,'Equipment operating envelope supplied',name)
                open_edge=closed_edge+(fallback or 0)
                sw=None
                basis='Concept 720mm oven-door projection from actual closed outer face; no selected hinge specification.'
            excluded=[name]
            gap,blocker=self.front_clearance(obj,open_edge,self.all_parts,excluded)
            self.require(gap>=.8-TOL,'800mm centered operator space beyond open equipment: '+name,{'clear_m':gap if math.isfinite(gap) else None,'blocker':blocker})
            closed_gap,_=self.front_clearance(obj,closed_edge,self.all_parts,excluded)
            service=envelope.get('service_front_clear_m',0)
            self.require(closed_gap>=service-TOL,'Published service-front clearance: '+name,{'clear_m':closed_gap if math.isfinite(closed_gap) else None,'required_m':service})
            records[name]={'basis':basis,'swept_bounds_m':list(sw) if sw else None,
                'operator_depth_m':gap if math.isfinite(gap) else None,'operator_target_m':.8,'operator_obstacle':blocker,
                'closed_service_depth_m':closed_gap if math.isfinite(closed_gap) else None,'published_service_target_m':service}
        self.report['checks']['kitchen']={'counter_apertures':openings,'oven_support_gap_m':support_gap,'equipment_operation':records}

    def doors(self):
        results={};opened=[];states={}
        leaves=[p for p in self.host if self.objects[p['name']].get('door_id')]
        self.require(len(leaves)>=12,'Architectural room doors have actual tagged leaves',len(leaves))
        door_obstacles=self.all_parts
        for leaf in leaves:
            obj=self.objects[leaf['name']]
            door_id=obj['door_id']
            width=obj.get('leaf_width_m',0)
            self.require(width>=.72,'Room leaf has usable concept width',{'door':door_id,'width_m':width})
            collisions=[]
            if 'pocket_translation_m' in obj:
                travel=Vector(obj['pocket_translation_m'])
                transforms=[Matrix.Translation(travel*t/10) for t in range(11)]
                mode='Pocket translation sampled in eleven positions'
            else:
                self.require(all(k in obj for k in ('hinge_x_m','hinge_y_m','closed_rotation_rad','open_rotation_rad')),'Door operating metadata',door_id)
                hinge=Vector((obj.get('hinge_x_m',0),obj.get('hinge_y_m',0),0))
                closed=obj.get('closed_rotation_rad',0);target=obj.get('open_rotation_rad',0)
                actual=obj.rotation_euler.z
                samples=max(2,math.ceil(abs(target-closed)/math.radians(5))+1)
                transforms=[Matrix.Translation(hinge) @ Matrix.Rotation(closed+(target-closed)*t/(samples-1)-actual,4,'Z') @ Matrix.Translation(-hinge) for t in range(samples)]
                mode='Actual leaf geometry sampled every five degrees or finer'
            states[door_id]=[]
            for step, transform in enumerate(transforms):
                moving_leaf=shifted_part(leaf,transform)
                states[door_id].append(moving_leaf)
                for obstacle in door_obstacles:
                    # Own frame/door hardware are construction interfaces, not room obstacles.
                    if obstacle['owner'].startswith(door_id):
                        continue
                    if penetrates(moving_leaf,obstacle):
                        collisions.append([step,obstacle['owner'],obstacle['name']])
            self.require(not collisions,'Door operating sweep clears actual fixtures and walls: '+door_id,collisions)
            final=shifted_part(leaf,transforms[-1]);opened.append(final)
            results[door_id]={'mode':mode,'samples':len(transforms),'collisions':collisions,'open_bounds_m':list(final['bounds'])}
        paired=[]
        names=list(states)
        for i,name in enumerate(names):
            for other in names[i+1:]:
                if not overlap(union(states[name]),union(states[other])):
                    continue
                hits=[]
                for a_index,a in enumerate(states[name]):
                    for b_index,b in enumerate(states[other]):
                        if penetrates(a,b):
                            hits.append([a_index,b_index])
                if hits:
                    paired.append({'doors':[name,other],'sample_pairs':hits})
        self.require(not paired,'Independent architectural door operating states clear each other',paired)
        self.report['checks']['paired_door_states']=paired
        self.report['checks']['architectural_door_states']=results
        return opened

    def fixture_and_storage_access(self):
        results={}
        for name,parts in self.assets.items():
            obj=self.instances[name];slug=obj['asset_id']
            env=self.meta[name].get('installation',{}).get('operating_envelope',{})
            target=None
            if slug.startswith('cabinetry/'):
                target=env.get('reserve_front_depth_including_operator_m',env.get('reserve_front_depth_m'))
                if target is None and 'reserve_front_operator_depth_m' in env:
                    target=env['reserve_front_operator_depth_m']+env.get('reserve_front_door_projection_m',0)
            elif 'shower-tray' in slug:
                target=env.get('reserve_front_approach_depth_m')
            elif 'vanity-basin' in slug:
                target=env.get('reserve_front_standing_depth_m')
            elif 'toilet-' in slug:
                target=.80
            if target is None:
                continue
            front=(obj.matrix_world.to_3x3() @ Vector((0,-1,0))).normalized()
            installation=parts
            excluded=[name]
            if slug.startswith('cabinetry/'):
                cb=union(parts)
                for p in self.host:
                    pb=p['bounds']
                    top_name=any(word in p['name'].lower() for word in ('worktop','counter','landing',' top'))
                    planar_overlap=all(min(cb[i+3],pb[i+3])-max(cb[i],pb[i])>.001 for i in (0,1))
                    if top_name and planar_overlap and cb[5]-.02<=pb[2]<=cb[5]+.10 and pb[5]<=cb[5]+.16:
                        installation=installation+[p]
                        excluded.append(p['owner'])
            if 'vanity-basin' in slug:
                prefix=name.removesuffix(' basin and mirror')
                installation=[p for p in self.all_parts if p['owner'].startswith(prefix)]
                excluded=list({p['owner'] for p in installation})
                counters=[p for p in installation if 'stone worktop' in p['name']]
                origin=obj.location.copy();origin.z=.78
                hits=[p['name'] for p in counters if tree(p).ray_cast(origin,Vector((0,0,-1)),.10)[0] is not None]
                self.require(bool(counters) and not hits,'Vanity has real waste opening through counter: '+name,hits)
            edge=max(v.dot(front) for p in installation for v in p['vertices'])
            gap,blocker=self.front_clearance(obj,edge,self.all_parts,excluded)
            self.require(gap>=target-TOL,'Published fixture/storage approach: '+name,
                         {'clear_m':gap if math.isfinite(gap) else None,'target_m':target,'blocker':blocker})
            results[name]={'clear_m':gap if math.isfinite(gap) else None,'required_m':target,'nearest_obstacle':blocker}
        # Wet fixtures must be separate usable bodies, not intersecting proxies.
        wet=[name for name in self.assets if any(w in self.instances[name]['asset_id'] for w in ('toilet-','shower-tray','freestanding-tub','vanity-basin'))]
        collisions=[]
        for i,name in enumerate(wet):
            for other in wet[i+1:]:
                for a in self.assets[name]:
                    for b in self.assets[other]:
                        if penetrates(a,b):
                            collisions.append([name,a['name'],other,b['name']])
        self.require(not collisions,'Actual bathroom fixtures do not intersect one another',collisions)
        self.report['checks']['fixture_storage_access']=results
        self.report['checks']['bathroom_fixture_collisions']=collisions

    def sliders(self):
        states=self.find_metadata('door_states') or []
        results={}
        for state in states:
            if 'clear_start_m' not in state or 'clear_end_m' not in state:
                continue
            name=state['id']
            a=Vector((*state['clear_start_m'],0));b=Vector((*state['clear_end_m'],0))
            tangent=(b-a).normalized();normal=Vector((-tangent.y,tangent.x,0))
            moving_parts=[p for p in self.host if p['name'].startswith(name+' parked moving leaf')]
            self.require(bool(moving_parts),'Slider has actual separate moving mesh group',name)
            if not moving_parts:
                continue
            moving_names={p['name'] for p in moving_parts}
            fixed=[p for p in self.host if p['name'] not in moving_names and not self.objects[p['name']].get('qa_only')
                   and not (p['name'].startswith(name) and any(word in p['name'] for word in ('head track','threshold track','sliding pull')))]
            aperture_hits=[]
            for fraction in (.20,.50,.80):
                for z in (.30,1.00,1.75):
                    origin=a+(b-a)*fraction-normal*.15;origin.z=z
                    for p in fixed:
                        if tree(p).ray_cast(origin,normal,.30)[0] is not None:
                            aperture_hits.append(p['name'])
            self.require((b-a).length>=.80 and not aperture_hits,'Actual open sliding aperture clears passage: '+name,aperture_hits)
            travel=(b-a).length+.075
            collisions=[]
            for index in range(11):
                transform=Matrix.Translation(-tangent*travel*index/10)
                for p in moving_parts:
                    motion=shifted_part(p,transform)
                    for obstacle in fixed:
                        if penetrates(motion,obstacle):
                            collisions.append([index,p['name'],obstacle['name']])
            self.require(not collisions,'Sliding glazing sampled translation clears fixed architecture: '+name,collisions)
            results[name]={'open_width_m':(b-a).length,'translation_m':travel,'samples':11,
                           'aperture_rays':9,'collisions':collisions,'aperture_hits':aperture_hits,
                           'limits':'Own guide-track/handle interfaces excluded; concept translation only, not roller or hardware certification.'}
        expected=len(d.COURTYARD_SLIDERS)+sum(opening[4]=='slider' for _,_,_,_,openings in d.WALLS for opening in openings)
        self.require(len(results)==expected and expected>=3,'Courtyard and rear sliders are represented in operating checks',list(results))
        self.report['checks']['sliding_glazing']=results

    def routes(self, open_doors):
        resolution=.10;radius=.30
        nx=math.ceil(d.WIDTH/resolution);ny=math.ceil(d.DEPTH/resolution)
        blocked=set()
        def xy(cell):
            return ((cell[0]+.5)*resolution,(cell[1]+.5)*resolution)
        def on_floor(x,y):
            return any(room_contains(r,(x,y)) for r in self.floor_rects)
        for i in range(nx):
            for j in range(ny):
                x,y=xy((i,j))
                if not all(on_floor(x+radius*math.cos(t*math.pi/4),y+radius*math.sin(t*math.pi/4)) for t in range(8)):
                    blocked.add((i,j))
        obstacle_count=0
        for p in self.all_parts+open_doors:
            b=p['bounds']
            if b[5]<.08 or b[2]>1.85:
                continue
            if b[3]<0 or b[4]<0 or b[0]>d.WIDTH or b[1]>d.DEPTH:
                continue
            polygon=convex_hull(p['vertices'])
            if len(polygon)<3:
                continue
            obstacle_count+=1
            for i in range(max(0,int((b[0]-radius)/resolution)),min(nx,math.ceil((b[3]+radius)/resolution))):
                for j in range(max(0,int((b[1]-radius)/resolution)),min(ny,math.ceil((b[4]+radius)/resolution))):
                    if (i,j) not in blocked:
                        x,y=xy((i,j))
                        if distance_to_polygon(x,y,polygon)<radius:
                            blocked.add((i,j))
        entry=next(r for name,r,label in d.ROOMS if name=='entry')
        candidates=[(i,j) for i in range(nx) for j in range(ny) if (i,j) not in blocked and room_contains(entry,xy((i,j)),.25)]
        if not self.require(bool(candidates),'Foyer has an actual usable standing position'):
            return
        target=d.p(36,4)
        start=min(candidates,key=lambda c:math.dist(xy(c),target))
        reached={start};queue=deque([start])
        while queue:
            i,j=queue.popleft()
            for cell in ((i+1,j),(i-1,j),(i,j+1),(i,j-1)):
                if 0<=cell[0]<nx and 0<=cell[1]<ny and cell not in blocked and cell not in reached:
                    reached.add(cell);queue.append(cell)
        goals={}
        for name,rect,label in d.ROOMS:
            if name.startswith('wardrobe-'):
                continue
            available=[cell for cell in reached if room_contains(rect,xy(cell),.25)]
            self.require(len(available)>=3,'Indoor route from foyer to '+name,{'reachable_standing_cells':len(available)})
            goals[name]={'reachable_standing_cells':len(available),'sample_point_m':xy(available[0]) if available else None}
        self.report['checks']['indoor_routes']={'body_diameter_m':2*radius,'grid_m':resolution,'start_m':xy(start),
             'obstacle_meshes':obstacle_count,'reachable_cells':len(reached),'courtyard_excluded':True,'rooms':goals}

    def shades(self):
        records=self.find_metadata('bedroom_shades') or []
        self.require(len(records)==10,'All ten bedroom glazing bays have paired privacy states',len(records))
        results={};groups={};closed_sets=[]
        graph=bpy.context.evaluated_depsgraph_get()
        beams=[p for p in self.host if p['name'].startswith(('Primary bay beam','Longitudinal support beam'))]
        lowest_beam=min(p['bounds'][2] for p in beams)
        for row in records:
            name=row['id'];open_obj=self.instances.get(row['open_instance']);closed_obj=self.instances.get(row['closed_instance'])
            if not self.require(open_obj is not None and closed_obj is not None,'Installed open and closed shade instances exist',name):
                continue
            self.require(not open_obj.hide_render and not open_obj.hide_viewport and closed_obj.hide_render and closed_obj.hide_viewport,
                         'Only open shade state is canonical-visible',name)
            # Viewport-hidden alternates require temporary evaluation. Never save.
            original_hidden=closed_obj.hide_viewport
            try:
                closed_obj.hide_viewport=False;bpy.context.view_layer.update()
                graph=bpy.context.evaluated_depsgraph_get()
                self.require(all(abs(open_obj.matrix_world[i][j]-closed_obj.matrix_world[i][j])<.0001 for i in range(4) for j in range(4)),
                             'Shade states have identical rigid mounting transforms',name)
                opened=collection_parts(open_obj.instance_collection,open_obj.matrix_world,graph,open_obj.name)
                closed=collection_parts(closed_obj.instance_collection,closed_obj.matrix_world,graph,closed_obj.name)
            finally:
                closed_obj.hide_viewport=original_hidden
            meta=self.meta[open_obj.name]
            for state,obj,parts in [('open',open_obj,opened),('closed',closed_obj,closed)]:
                expected=transform_bounds(meta['state_bounds_m'][state],obj.matrix_world)
                self.require(bool(parts) and all(abs(a-b)<.001 for a,b in zip(union(parts),expected)),
                             'Actual shade state matches published rigid geometry: '+name+' '+state)
            fabric=[p for p in closed if p['blind_part']=='fabric']
            self.require(len(fabric)==1,'Closed shade has one actual full fabric panel',name)
            if not fabric:
                continue
            material_ok=True
            for obj in closed_obj.instance_collection.all_objects:
                if obj.get('blind_part')!='fabric':
                    continue
                for mat in obj.data.materials:
                    principled=[n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'] if mat and mat.use_nodes else []
                    if not principled or any(n.inputs['Alpha'].is_linked or n.inputs['Alpha'].default_value<.999 or n.inputs['Transmission Weight'].is_linked or n.inputs['Transmission Weight'].default_value>.001 for n in principled):
                        material_ok=False
            self.require(material_ok,'Shade fabric material is opaque in native scene',name)
            tangent=(open_obj.matrix_world.to_3x3() @ Vector((1,0,0))).normalized()
            normal=(open_obj.matrix_world.to_3x3() @ Vector((0,1,0))).normalized()
            center=open_obj.location.dot(tangent);plane=open_obj.location.dot(normal)
            glazing=[]
            for p in self.solids:
                if self.objects[p['name']].get('ifc_class')!='IfcWindow':
                    continue
                middle=sum(p['vertices'],Vector())/len(p['vertices'])
                if abs(middle.dot(tangent)-center)<.025 and abs(middle.dot(normal)-plane)<.25:
                    glazing.append(p)
            self.require(len(glazing)==1,'One actual bedroom glass light corresponds to shade',{'shade':name,'glass':[p['name'] for p in glazing]})
            overlaps=None
            if len(glazing)==1:
                glass=glazing[0]
                gf=[v.dot(tangent) for v in glass['vertices']];ff=[v.dot(tangent) for v in fabric[0]['vertices']]
                overlaps=[min(gf)-min(ff),max(ff)-max(gf)]
                self.require(all(abs(value-.017)<.002 for value in overlaps), 'Actual opaque fabric overlaps both glass jamb edges by17mm: '+name,overlaps)
                fb=fabric[0]['bounds'];gb=glass['bounds']
                self.require(fb[2]<=gb[2]+TOL and fb[5]>=gb[5]-TOL,'Closed fabric covers actual glass sill-to-head height: '+name,
                             {'fabric_z':[fb[2],fb[5]],'glass_z':[gb[2],gb[5]]})
            collisions=[]
            for state,parts in [('open',opened),('closed',closed)]:
                for a in parts:
                    for obstacle in self.all_parts+beams:
                        if penetrates(a,obstacle):
                            collisions.append([state,a['name'],obstacle['owner'],obstacle['name']])
            self.require(not collisions,'Both shade states clear walls, beams and furnishings: '+name,collisions)
            cb=union(closed);clearance=lowest_beam-cb[5]
            self.require(clearance>=.020-TOL,'Shade cassette remains at least20mm below main beam underside',{'shade':name,'clear_m':clearance})
            cassette=[p for p in closed if p['blind_part'] in ('cassette','end_cap')]
            lateral=[v.dot(tangent) for p in cassette for v in p['vertices']]
            group=(round(open_obj.rotation_euler.z,3),round(plane,3),round(open_obj.location.z,3))
            groups.setdefault(group,[]).append((min(lateral),max(lateral),name))
            closed_sets.append((name,closed))
            results[name]={'open_bounds_m':list(union(opened)),'closed_bounds_m':list(cb),
                'jamb_overlap_m':overlaps,'beam_clearance_m':clearance,'collisions':collisions,
                'opaque_native_material':material_ok,'product_blackout_performance_tested':False}
        neighbor_gaps=[]
        for group,items in groups.items():
            items.sort()
            for left,right in zip(items,items[1:]):
                gap=right[0]-left[1]
                self.require(gap>=.012-TOL,'Adjacent shade cassettes retain12mm minimum gap',{'pair':[left[2],right[2]],'gap_m':gap})
                neighbor_gaps.append({'pair':[left[2],right[2]],'gap_m':gap})
        self.report['checks']['bedroom_shades']={'states':results,'neighbor_cassette_gaps':neighbor_gaps,
             'limits':'Modeled opaque coverage and rigid endpoint fit only; no tested blackout, edge sealing, motor, fixing or product approval.'}

    def arrival(self):
        qa=[p for p in self.host if self.objects[p['name']].get('qa_role')]
        bodies=[p for p in qa if self.objects[p['name']]['qa_role']=='vehicle_body']
        door_reserves=[p for p in qa if self.objects[p['name']]['qa_role']=='vehicle_side_door_reserve']
        walks=[p for p in qa if self.objects[p['name']]['qa_role']=='sheltered_walk_clearance']
        self.require(len(bodies)==2 and len(door_reserves)==4 and len(walks)==1,'Actual parking and covered-route clearance volumes')
        for p in bodies:
            b=p['bounds']
            self.require(all(abs(a-bb)<.001 for a,bb in zip((b[3]-b[0],b[4]-b[1],b[5]-b[2]),(1.9,4.8,1.6))), 'Full-size parked vehicle reserve',p['name'])
        posts=[p for p in self.host if self.objects[p['name']].get('ifc_class')=='IfcColumn']
        collisions=[]
        for p in bodies+door_reserves+walks:
            for q in posts:
                if penetrates(p,q):
                    collisions.append([p['name'],q['name']])
        for i,p in enumerate(door_reserves):
            for q in door_reserves[i+1:]+walks:
                if penetrates(p,q):
                    collisions.append([p['name'],q['name']])
        if walks:
            b=walks[0]['bounds']
            self.require(b[4]-b[1]>=1.524-.001,'Measured covered walk is at least five feet wide',b[4]-b[1])
        self.require(not collisions,'Actual parking door reserves and covered walk clear posts and each other',collisions)
        self.report['checks']['arrival']={'vehicle_bodies':[list(p['bounds']) for p in bodies],
            'side_door_reserves':[list(p['bounds']) for p in door_reserves],
            'covered_walk':list(walks[0]['bounds']) if walks else None,'collisions':collisions,
            'basis':'Editable full-size concept vehicle/access reservations, not selected vehicle meshes or turning-path analysis.'}


def main():
    audit=Audit()
    try:
        audit.run()
    except Exception as error:
        audit.require(False,'Verifier exception',str(error))
        audit.report['exception_traceback']=traceback.format_exc()
    if not audit.report['failures']:
        audit.report['status']='passed'
    path=HOME/'model/model-validation.json'
    path.write_text(json.dumps(audit.report,indent=2,allow_nan=False)+'\n')
    print('ATRIUM_NATIVE_'+audit.report['status'].upper(),json.dumps(audit.report['failures']),flush=True)
    if audit.report['failures']:
        raise RuntimeError('Atrium native verification failed; see model/model-validation.json')


if __name__=='__main__':
    main()
