"""Pinned original library collections shared by home generators.

Run Blender with tools/library/publish_shared.py once. load_catalog only links
existing immutable assets; publishing is explicit. Locations use feet, Z-up.
"""
import json
import math
import random
from pathlib import Path

import bpy
from mathutils import Vector

from . import geometry as g
from .geometry import box, rod, F
from .landscape import grasses, shrub, tree
from .library import linked_collection, instance

CATALOG = {
    'grass': ('landscape', 'ornamental-grass-clump', 'v002'),
    'shrub': ('landscape', 'sage-shrub', 'v002'),
    'olive': ('landscape', 'olive-tree', 'v001'),
    'paver': ('surfaces', 'honed-limestone-paver-4ft', 'v001'),
    'wardrobe': ('cabinetry', 'oak-wardrobe-2ft', 'v001'),
    'base_cabinet': ('cabinetry', 'oak-drawer-base-2ft', 'v001'),
    'oven': ('appliances', 'built-in-oven-30in', 'v001'),
    'dishwasher': ('appliances', 'dishwasher-24in', 'v001'),
    'cooktop': ('appliances', 'induction-cooktop-36in', 'v001'),
    'hood': ('appliances', 'wall-hood-36in', 'v001'),
    'fireplace': ('fixtures', 'closed-glass-fireplace-48in', 'v001'),
    'fridge': ('appliances', 'panel-ready-fridge-48in', 'v001'),
    'bathtub': ('fixtures', 'freestanding-tub-72in', 'v001'),
    'toilet': ('fixtures', 'toilet-elongated', 'v001'),
    'downlight': ('fixtures', 'lighting-recessed-downlight-3in', 'v001'),
    'taskbar': ('fixtures', 'lighting-undercabinet-bar-4ft', 'v001'),
    'linear_pendant': ('fixtures', 'lighting-linear-pendant-4ft', 'v001'),
}


def load_catalog(root, keys=None):
    """Link exact versions; missing assets fail rather than silently regenerate."""
    return {key: linked_collection(root, *CATALOG[key])
            for key in (keys if keys is not None else CATALOG)}


def place(name, asset, loc, rotation=0, scale=1):
    """Place collection with feet origin, radian Z rotation, uniform scale.

    Plants allow restrained natural scale variation. Keep cabinetry and pavers
    at scale 1; change module count or publish a new dimensional asset instead.
    """
    obj = instance(name, asset, loc, rotation, scale)
    obj['shared_asset_id'] = asset.get('asset_id', asset.name)
    obj['shared_asset_version'] = asset.get('asset_version', 'v001')
    return obj


def dependencies(root, keys=None):
    return [{'id': '/'.join(CATALOG[k][:2]), 'version': CATALOG[k][2],
             'path': '../../library/' + '/'.join(CATALOG[k]) + '/'}
            for k in (keys if keys is not None else CATALOG)]


def _linked_material(root, slug):
    path = Path(root) / 'library/materials' / slug / 'v001' / (slug + '.blend')
    with bpy.data.libraries.load(str(path), link=True) as (src, dst):
        dst.materials = [src.materials[0]]
    return dst.materials[0]


def _materials(root):
    return {
        'oak': _linked_material(root, 'coastal-white-oak'),
        'stone': _linked_material(root, 'coastal-honed-limestone'),
        'grass': g.material('Shared meadow grass | olive green', (.24, .285, .125), .85),
        'leaf': g.material('Shared sage and olive leaves', (.125, .18, .075), .8),
        'bark': g.material('Shared olive bark', (.12, .085, .049), .92),
        'dark': g.material('Shared cabinet shadow reveal', (.028, .025, .020), .7),
        'metal': g.material('Shared brushed warm metal', (.24, .205, .14), .3, .7),
    }


def _connected_shrub(M):
    """Original woody shrub: every leaf attaches to a modeled branchlet."""
    rng = random.Random(1818)
    stem_verts, stem_faces, leaf_verts, leaf_faces = [], [], [], []

    def stem(a, b, radius):
        a, b = Vector(a), Vector(b)
        direction = (b-a).normalized()
        u = direction.cross(Vector((0,0,1)))
        if u.length < .01:
            u = Vector((1,0,0))
        u.normalize()
        v = direction.cross(u).normalized()
        first = len(stem_verts)
        for point, rad in [(a,radius),(b,radius*.65)]:
            for k in range(6):
                offset = u*math.cos(k*math.tau/6)*rad + v*math.sin(k*math.tau/6)*rad
                stem_verts.append(tuple((point+offset)*F))
        for k in range(6):
            stem_faces.append((first+k,first+(k+1)%6,first+6+(k+1)%6,first+6+k))

    def leaf(origin, direction, length):
        direction = Vector(direction).normalized()
        side = direction.cross(Vector((0,0,1))).normalized()
        origin = Vector(origin)
        first = len(leaf_verts)
        leaf_verts.extend(tuple(p*F) for p in [origin,origin+direction*length*.48+Vector((0,0,.024)),origin+direction*length])
        for t in [.16,.40,.65,.85]:
            width = math.sin(math.pi*t)*length*.19
            center = origin+direction*length*t
            leaf_verts.extend([tuple((center-side*width)*F),tuple((center+side*width)*F)])
        for side_index in [0,1]:
            rim = [first] + [first+3+2*i+side_index for i in range(4)] + [first+2]
            for a,b in zip(rim[:-1],rim[1:]):
                leaf_faces.append((first+1,a,b))

    stem((0,0,0),(0,0,.7),.055)
    for branch in range(24):
        angle = branch*2.399
        radial = Vector((math.cos(angle),math.sin(angle),0))
        base = Vector((0,0,rng.uniform(.1,.55)))
        tip = radial*rng.uniform(.6,1.25)+Vector((0,0,rng.uniform(1.4,2.7)))
        stem(base,tip,.018)
        main_dir = (tip-base).normalized()
        for twig in range(6):
            t=.30+twig*.115
            start=base.lerp(tip,t)
            side=Vector((-radial.y,radial.x,0))*(1 if twig%2 else -1)
            end=start+side*rng.uniform(.27,.52)+radial*.10+Vector((0,0,.12))
            stem(start,end,.007)
            twig_dir=(end-start).normalized()
            for pair in range(5):
                origin=start.lerp(end,.16+pair*.17)
                for sign in [-1,1]:
                    direction=(radial*sign*.7+twig_dir*.38+Vector((0,0,.16)))
                    leaf(origin,direction,rng.uniform(.17,.25))
            leaf(end,twig_dir+Vector((0,0,.15)),.22)
    for name,verts,faces,mat in [('Connected sage woody branches',stem_verts,stem_faces,M['bark']),
                               ('Attached sage leaves',leaf_verts,leaf_faces,M['leaf'])]:
        mesh=bpy.data.meshes.new(name)
        mesh.from_pydata(verts,[],faces)
        mesh.materials.append(mat)
        obj=bpy.data.objects.new(name,mesh)
        g.ACTIVE.objects.link(obj)


def _curved_grass(M):
    """Continuous tapered ribbons, avoiding the old angular two-segment blades."""
    rng = random.Random(1717)
    verts, faces = [], []
    for blade in range(110):
        angle = rng.random()*math.tau
        radial = Vector((math.cos(angle), math.sin(angle), 0))
        side = Vector((-math.sin(angle), math.cos(angle), 0))
        root = Vector((rng.uniform(-.17,.17),rng.uniform(-.17,.17),0))
        height = rng.uniform(.9,2.25)
        outward = rng.uniform(.25,1.25)
        width = rng.uniform(.012,.030)
        first = len(verts)
        for step in range(13):
            t = step/12
            center = root + radial*(outward*t*t) + Vector((0,0,height*(t-.28*t*t*t)))
            half = side*width*(1-t)**.7
            verts.extend([tuple((center-half)*F),tuple((center+half)*F)])
            if step:
                faces.append((first+2*step-2,first+2*step-1,first+2*step+1,first+2*step))
    mesh=bpy.data.meshes.new('Original curved tapered meadow grass')
    mesh.from_pydata(verts,[],faces)
    mesh.materials.append(M['grass'])
    obj=bpy.data.objects.new('Original curved tapered meadow grass',mesh)
    g.ACTIVE.objects.link(obj)


def _wardrobe(M):
    # A usable 24 inch bay, with internal volume instead of a single solid box.
    for x in [-.97, .97]:
        box('Wardrobe side panel', (x, 0, 4), (.06, 2, 8), M['oak'], .009)
    box('Wardrobe back panel', (0, .97, 4), (1.88, .06, 8), M['oak'], .006)
    for z in [.3, 7.97]:
        box('Wardrobe bottom or top', (0, 0, z), (1.88, 1.94, .06), M['oak'], .006)
    box('Wardrobe recessed toe kick', (0, .04, .13), (1.86, 1.75, .26), M['dark'], .01)
    box('Wardrobe upper shelf', (0, .06, 6.65), (1.88, 1.80, .065), M['oak'], .006)
    rod('Wardrobe hanging rail', (-.92, .05, 6.22), (.92, .05, 6.22), .036, M['metal'])
    for x in [-.48, .48]:
        box('Wardrobe editable hinged oak door', (x, -.965, 4.12), (.95, .065, 7.70), M['oak'], .01)
        handle_x = -.10 if x < 0 else .10
        rod('Wardrobe door pull', (handle_x, -1.075, 3.45), (handle_x, -1.075, 4.15), .019, M['metal'])
        for z in [3.49, 4.11]:
            rod('Wardrobe pull mount', (handle_x, -1.00, z), (handle_x, -1.075, z), .017, M['metal'])


def _base_cabinet(M):
    for x in [-.965, .965]:
        box('Base cabinet side', (x, 0, 1.55), (.07, 2, 2.62), M['oak'], .008)
    box('Base cabinet rear', (0, .965, 1.55), (1.86, .07, 2.62), M['oak'], .006)
    box('Base cabinet bottom', (0, 0, .28), (1.86, 1.90, .08), M['oak'], .006)
    box('Base cabinet recessed toe kick', (0, .10, .13), (1.86, 1.70, .26), M['dark'], .008)
    for z, h in [(.76, .9), (1.70, .90), (2.50, .66)]:
        box('Base cabinet drawer front', (0, -1.005, z), (1.975, .07, h), M['oak'], .012)
        box('Drawer box with usable volume', (0, .01, z - h/2 + .08), (1.72, 1.72, .065), M['oak'], .008)
        for x in [-.86, .86]:
            box('Drawer side', (x, .01, z), (.05, 1.72, max(.15, h-.17)), M['oak'], .006)
        box('Drawer recessed finger grip', (0, -1.045, z + h/2 - .05), (1.73, .02, .035), M['dark'], .004)


def _bounds(collection):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    pts = []
    for obj in collection.all_objects:
        if obj.type in {'MESH', 'CURVE'}:
            evaluated = obj.evaluated_get(depsgraph)
            pts.extend(evaluated.matrix_world @ Vector(v) for v in evaluated.bound_box)
    lo = [min(p[i] for p in pts) for i in range(3)]
    hi = [max(p[i] for p in pts) for i in range(3)]
    return lo, hi


def publish_catalog(root):
    """Create missing pinned versions; existing versions are never modified."""
    root = Path(root)
    M = _materials(root)
    descriptions = {
        'grass': ('Ornamental meadow grass clump', 'Grade at Z=0, centered XY. Nominal two-foot ornamental clump; illustrative planting, species not specified.'),
        'shrub': ('Fine-leaved sage shrub', 'Grade at Z=0, centered XY. Nominal three-foot shrub; illustrative planting, not a botanical specification.'),
        'olive': ('Original olive tree', 'Trunk base at Z=0, centered XY. Nominal fourteen-foot ornamental tree with original branches and leaf geometry.'),
        'paver': ('Four-foot honed limestone paver', 'Top face Z=0, centered XY. Exactly 4 x 4 feet, 1.2 inches thick. Use 4.02-foot placement pitch for a 0.24-inch joint; perimeter pieces may be project-specific cuts.'),
        'wardrobe': ('Two-foot oak wardrobe bay', 'Floor center origin, front toward -Y. Nominal 2 x 2 x 8 feet; handles project 0.094 feet beyond front. Two editable doors, top shelf and hanging rail. Allow door swing and standing clearance in host home.'),
        'base_cabinet': ('Two-foot oak three-drawer base cabinet', 'Floor center origin, front toward -Y. Nominal 2 x 2 x 2.86 feet, fronts slightly proud. Worktop deliberately excluded so a continuous host counter can span several linked modules.'),
    }
    from .appliances import DESCRIPTIONS, build_appliance
    descriptions.update(DESCRIPTIONS)
    from .bath_fixtures import DESCRIPTIONS as BATH_DESCRIPTIONS, METADATA as BATH_METADATA, build_bath_fixture
    descriptions.update(BATH_DESCRIPTIONS)
    for key, (category, slug, version) in CATALOG.items():
        folder = root / 'library' / category / slug / version
        path = folder / (slug + '.blend')
        if path.exists():
            continue
        if key not in descriptions:
            raise FileNotFoundError(f'{path}: publish this fixture with tools/library/publish_lighting.py first')
        prior = g.ACTIVE
        coll = g.collection(descriptions[key][0])
        coll['asset_id'] = category + '/' + slug
        coll['asset_version'] = version
        if key == 'grass':
            if version == 'v001':
                grasses('Original arching grass blades', 0, 0, 1.9, M['grass'], 1717)
            else:
                _curved_grass(M)
        elif key == 'shrub':
            if version == 'v001':
                # Retained generator for the first published draft version.
                shrub('Original sage leaves', 0, 0, 2.2, M['leaf'], 1818)
                for dx, dy in [(-.3, .1), (.3, -.1), (0, .3)]:
                    rod('Original woody sage branch', (0, 0, 0), (dx, dy, 1.45), .027, M['bark'])
            else:
                _connected_shrub(M)
        elif key == 'olive':
            tree('Original olive', 0, 0, 14, M['bark'], M['leaf'], 1919)
        elif key == 'paver':
            box('Honed limestone tile | 48 x 48 x 1.2 inches', (0, 0, -.05), (4, 4, .1), M['stone'], .009)
        elif key == 'wardrobe':
            _wardrobe(M)
        elif key == 'base_cabinet':
            _base_cabinet(M)
        elif key in DESCRIPTIONS:
            build_appliance(key, root)
        elif key in BATH_DESCRIPTIONS:
            build_bath_fixture(key)
        bpy.context.view_layer.update()
        lo, hi = _bounds(coll)
        linked = []
        for slug_material in (['coastal-honed-limestone'] if key == 'paver' else
                              ['coastal-white-oak'] if key in {'wardrobe', 'base_cabinet', 'fridge'} else []):
            linked.append({'id': 'materials/' + slug_material, 'version': 'v001',
                           'path': '../../../materials/' + slug_material + '/v001/' + slug_material + '.blend'})
        folder.mkdir(parents=True, exist_ok=True)
        bpy.data.libraries.write(str(path), {coll}, fake_user=True, path_remap='RELATIVE_ALL')
        data = {'schema_version': 1, 'id': category+'/'+slug, 'version': version,
                'name': descriptions[key][0], 'units': 'meters',
                'dimensions_m': [round(hi[i]-lo[i], 6) for i in range(3)],
                'bounds_m': {'min': lo, 'max': hi},
                'placement': descriptions[key][1], 'description': descriptions[key][1],
                'source': {'kind': 'original', 'generator': ('tools/common/appliances.py' if key in DESCRIPTIONS else 'tools/common/bath_fixtures.py' if key in BATH_DESCRIPTIONS else 'tools/common/shared_assets.py'),
                           'command': 'Blender --background --python tools/library/publish_shared.py'},
                'license': 'CC-BY-4.0', 'rights': 'Original project geometry; attribution: Homes project contributors',
                'files': {'blender': path.name}, 'dependencies': linked,
                'software': {'blender': bpy.app.version_string}}
        data.update(BATH_METADATA.get(key, {}))
        (folder/'asset.json').write_text(json.dumps(data, indent=2)+'\n')
        for obj in list(coll.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(coll)
        g.ACTIVE = prior
        print('SHARED_ASSET_PUBLISHED', category+'/'+slug, version, flush=True)
