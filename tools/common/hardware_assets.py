"""Original architectural hardware library. Geometry dimensions use inches.

Host placement uses feet and radians, like common.shared_assets. Front is -Y,
Z is up, origin is the mounting face center. Published files never overwrite.
"""
import json
import math
from pathlib import Path
import bpy
from mathutils import Vector
from . import geometry as g
from .library import linked_collection, instance

FINISHES = {
    'satin-bronze': ((.32, .19, .075), .31, .88),
    'matte-black': ((.018, .021, .023), .40, .65),
    'brushed-steel': ((.46, .49, .51), .28, .92),
}
KINDS = {
    'round-knob': ('Round cabinet knob', '1.125 in diameter; 1.10 in projection. Origin at face center. Single center fixing.'),
    'bar-pull': ('Slender cabinet bar pull', '6 in mounting centers; 6.4 in overall width; 1.25 in projection. Horizontal by default. Rotate local Y 90 degrees for vertical orientation.'),
    'edge-pull': ('Cabinet top-edge pull', '4 in width; 1.125 in front projection; .65 in top return. Origin at front top edge. Grip lip drops .42 in below top edge. Requires a .12 in recessed top mounting rebate for a flush front.'),
    'door-lever': ('Interior door lever on rose', '2 in diameter rose; lever extends 5 in toward +X from spindle; 2.25 in front projection. Origin at spindle on door face. Single side only; host supplies opposite handle, latch and door.'),
    'flush-pull': ('Recessed sliding-door finger pull', '1.75 x 5 in faceplate; .10 in front projection; .55 in pocket depth into +Y. Host needs a 1.45 x 4.70 in pocket cutout, .65 in minimum depth; do not place on an uncut solid door.'),
}
CATALOG = {(kind, finish): ('hardware', f'{kind}-{finish}', 'v001')
           for kind in KINDS for finish in FINISHES}


def load(root, kind='bar-pull', finish='satin-bronze'):
    """Link the pinned reusable collection; missing publication is an error."""
    category, slug, version = CATALOG[(kind, finish)]
    native = (Path(root)/'library'/category/slug/version/(slug+'.blend')).resolve()
    for collection in bpy.data.collections:
        if collection.library and Path(bpy.path.abspath(collection.library.filepath)).resolve() == native:
            return collection
    return linked_collection(root, category, slug, version)


def place(root, kind, finish, name, loc_ft, rotation_z=0):
    """Place linked hardware at a host face, feet / Z-up / front -Y."""
    asset = load(root, kind, finish)
    obj = instance(name, asset, loc_ft, rotation_z)
    obj['shared_asset_id'] = '/'.join(CATALOG[(kind, finish)][:2])
    obj['shared_asset_version'] = 'v001'
    obj['mounting_face_normal'] = 'local -Y'
    return obj


def dependencies(choices):
    return [{'id': '/'.join(CATALOG[pair][:2]), 'version': 'v001',
             'path': '../../library/' + '/'.join(CATALOG[pair]) + '/'}
            for pair in dict.fromkeys(choices)]


def _box(name, loc, size, mat, bevel=.035):
    return g.box(name, [v/12 for v in loc], [v/12 for v in size], mat, bevel/12)


def _rod(name, a, b, r, mat):
    obj = g.rod(name, [v/12 for v in a], [v/12 for v in b], r/12, mat)
    mod = obj.modifiers.new('Manufactured end bevel', 'BEVEL')
    mod.width = .025*.0254
    mod.segments = 3
    obj.modifiers.new('Weighted end normals', 'WEIGHTED_NORMAL')
    return obj


def _disk(name, center, radius, depth, mat):
    obj = g.cyl(name, [v/12 for v in center], radius/12, depth/12, mat, 64)
    obj.rotation_euler.x = math.pi/2
    bevel = obj.modifiers.new('Turned edge radius', 'BEVEL')
    bevel.width = .035*.0254
    bevel.segments = 4
    obj.modifiers.new('Turned weighted normals', 'WEIGHTED_NORMAL')
    return obj


def _build(kind, mat):
    if kind == 'round-knob':
        _disk('Mounting base', (0,-.05,0), .31, .10, mat)
        _rod('Knob neck', (0,-.07,0), (0,-.85,0), .19, mat)
        _disk('Round finger grip', (0,-.93,0), .5625, .34, mat)
    elif kind == 'bar-pull':
        for x in [-3,3]:
            _disk('Bar fixing foot', (x,-.045,0), .21, .09, mat)
            _rod('Bar standoff', (x,-.06,0), (x,-1.0625,0), .15, mat)
        _rod('Horizontal grip bar', (-3.2,-1.0625,0), (3.2,-1.0625,0), .1875, mat)
    elif kind == 'edge-pull':
        _box('Rebated top mounting return', (0,.325,-.06), (4,.65,.12), mat, .022)
        _box('Projecting finger ledge', (0,-.5625,-.06), (4,1.125,.12), mat, .03)
        _box('Downturned grip edge', (0,-1.065,-.23), (4,.12,.38), mat, .035)
    elif kind == 'door-lever':
        _disk('Round door rosette', (0,-.12,0), 1, .24, mat)
        _disk('Spindle collar', (0,-.32,0), .37, .20, mat)
        _rod('Lever spindle', (0,-.36,0), (0,-1.95,0), .24, mat)
        _box('Soft rectangular lever grip', (2.42,-1.97,0), (5.16,.56,.46), mat, .18)
    elif kind == 'flush-pull':
        # Four separate solid frame members leave an actual finger aperture.
        for x in [-.80,.80]:
            _box('Flush pull face side', (x,-.05,0), (.15,.10,5), mat, .025)
            _box('Recess side wall', (x,.26,0), (.15,.62,4.7), mat, .025)
        for z in [-2.425,2.425]:
            _box('Flush pull face end', (0,-.05,z), (1.6,.10,.15), mat, .025)
        for z in [-2.30,2.30]:
            _box('Recess end wall', (0,.26,z), (1.6,.62,.10), mat, .02)
        _box('Recess rear wall', (0,.52,0), (1.6,.06,4.6), mat, .025)


def _bounds(collection):
    bpy.context.view_layer.update()
    points = [o.matrix_world @ Vector(corner) for o in collection.all_objects
              if o.type == 'MESH' for corner in o.bound_box]
    lo = [min(p[i] for p in points) for i in range(3)]
    hi = [max(p[i] for p in points) for i in range(3)]
    return lo, hi


def publish(root):
    """Explicit original geometry publication; does not replace existing versions."""
    root = Path(root)
    previous = g.ACTIVE
    for (kind,finish), (category,slug,version) in CATALOG.items():
        folder = root/'library'/category/slug/version
        native = folder/(slug+'.blend')
        if native.exists():
            if not (folder/'asset.json').exists():
                raise RuntimeError(f'Incomplete existing publication: {folder}')
            continue
        folder.mkdir(parents=True,exist_ok=True)
        coll = g.collection(f'{KINDS[kind][0]} | {finish}')
        coll['asset_id'] = f'{category}/{slug}'
        coll['asset_version'] = version
        color,roughness,metal = FINISHES[finish]
        material = g.material(f'Hardware | {finish}', color, roughness, metal)
        p = material.node_tree.nodes.get('Principled BSDF')
        p.inputs['Anisotropic'].default_value = .18 if finish == 'brushed-steel' else .08
        _build(kind, material)
        lo,hi = _bounds(coll)
        bpy.data.libraries.write(str(native), {coll}, fake_user=True, path_remap='RELATIVE_ALL')
        metadata = {
            'schema_version':1,'id':f'{category}/{slug}','version':version,
            'name':f'{KINDS[kind][0]} — {finish.replace("-"," ")}',
            'units':'meters','dimensions_m':[round(hi[i]-lo[i],6) for i in range(3)],
            'bounds_m':{'min':lo,'max':hi},
            'placement': 'Origin at host mounting face center, front -Y, Z-up. '+KINDS[kind][1],
            'variation': 'Keep scale 1. Choose the explicit pinned finish asset. Uniform scaling changes fixing centers and is not appropriate for specification.',
            'source':{'kind':'original','generator':'tools/common/hardware_assets.py',
                      'command':'Blender --background --python tools/library/publish_hardware.py'},
            'license':'CC-BY-4.0','rights':'Original project geometry; attribution: Homes project contributors',
            'files':{'blender':native.name,'preview':'preview.png'},'dependencies':[],
            'software':{'blender':bpy.app.version_string},
            'limitations':'Generic design component, not a manufacturer SKU or installation approval. Host is responsible for panel drilling/rebates, latch clearances and mounting height.'}
        (folder/'asset.json').write_text(json.dumps(metadata,indent=2)+'\n')
        for obj in list(coll.objects): bpy.data.objects.remove(obj,do_unlink=True)
        bpy.data.collections.remove(coll)
    g.ACTIVE = previous
