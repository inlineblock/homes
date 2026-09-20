"""Original smoked-oak appliance siblings; preserve published parents.

Blender --background --python tools/library/build_timber_kitchen_appliances.py
Blender --background --python tools/library/build_timber_kitchen_appliances.py -- --verify --render
"""
from pathlib import Path
import json
import sys
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from common import geometry as g
from common.timber_materials import grain_uv

GENERATOR = 'tools/library/build_timber_kitchen_appliances.py'
ASSETS = {
    'smoked-oak-panel-ready-fridge-48in': 'panel-ready-fridge-48in',
    'smoked-oak-panel-ready-dishwasher-24in': 'dishwasher-24in',
}


def folder(slug):
    return ROOT / 'library/appliances' / slug / 'v001'


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def evaluated_bounds(collection):
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    points = []
    for obj in collection.all_objects:
        if obj.type != 'MESH':
            continue
        ev = obj.evaluated_get(dg)
        mesh = ev.to_mesh()
        points.extend(ev.matrix_world @ v.co for v in mesh.vertices)
        ev.to_mesh_clear()
    return ([min(v[i] for v in points) for i in range(3)],
            [max(v[i] for v in points) for i in range(3)])


def build(slug, parent):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    parent_path = folder(parent) / (parent + '.blend')
    assert parent_path.exists(), parent_path
    with bpy.data.libraries.load(str(parent_path), link=False) as (src, dst):
        dst.collections = [src.collections[0]]
    collection = dst.collections[0]
    collection.name = slug + ' | v001'
    bpy.context.scene.collection.children.link(collection)
    collection['asset_id'] = 'appliances/' + slug
    collection['asset_version'] = 'v001'
    collection['derived_from'] = 'appliances/' + parent + '/v001'
    g.ACTIVE = collection
    oak_path = ROOT / 'library/materials/smoked-oak/v001/smoked-oak.blend'
    with bpy.data.libraries.load(str(oak_path), link=True) as (src, dst):
        dst.materials = ['Smoked oak | warm umber | v001']
    oak = dst.materials[0]
    bronze = g.material('Appliance satin dark bronze | original concept', (.115, .072, .034), .31, .82)
    if 'fridge' in slug:
        for obj in collection.all_objects:
            if obj.type != 'MESH':
                continue
            if 'oak' in obj.name.lower():
                obj.data.materials.clear()
                obj.data.materials.append(oak)
                grain_uv(obj)
            elif 'pull' in obj.name.lower():
                obj.data.materials.clear()
                obj.data.materials.append(bronze)
    else:
        # Retain actual published enclosure and recessed toe kick; replace the
        # stainless door, exposed fascia, marks and original handles entirely.
        for obj in list(collection.all_objects):
            if not any(word in obj.name for word in ['appliance enclosure', 'recessed toe kick']):
                bpy.data.objects.remove(obj, do_unlink=True)
        dark = g.material('Integrated dishwasher concealed top controls', (.016, .019, .018), .48)
        panel = g.box('Integrated dishwasher smoked-oak door panel',
                      (0, -1.006, 1.575), (1.975, .065, 2.49), oak, .007)
        grain_uv(panel)
        # Panel rear=-.9735ft, enclosure front=-.94ft: 10.2mm clear
        # gap. Top controls sit on top edge behind the closed panel.
        g.box('Integrated dishwasher concealed top control deck',
              (0, -.956, 2.814), (1.86, .025, .012), dark, .003)
        for x in [-.57, -.38, -.19]:
            g.box('Integrated dishwasher top-edge button',
                  (x, -.956, 2.822), (.08, .018, .004), bronze, .001)
        g.rod('Integrated dishwasher satin bronze pull',
              (-.70, -1.16, 2.46), (.70, -1.16, 2.46), .027, bronze)
        for x in [-.67, .67]:
            g.rod('Integrated dishwasher pull standoff',
                  (x, -1.0385, 2.46), (x, -1.16, 2.46), .023, bronze)
    return collection


def operating(slug):
    if 'fridge' in slug:
        return {
            'modeled_state': 'Closed double doors; generic integrated refrigeration envelope',
            'motion': 'Each 0.5913m leaf rotates 110 degrees about its outer vertical hinge; concept only.',
            'hinges_m': [[-.593, -.381, .116], [.593, -.381, .116]],
            'door_sweep_bounds_m': {'min': [-.82, -1.02, .116], 'max': [.82, -.34, 2.1336]},
            'service_front_clear_m': 1.22,
            'side_hinge_relief_m_each': .22,
            'basis': 'Conservative rounded concept swept volume including pulls; unselected manufacturer may require more.',
            'host_open_state_checked': False,
        }
    return {
        'modeled_state': 'Closed integrated drop-down door; hidden top-edge controls',
        'motion': 'Bottom hinged panel, 90-degree opening, approximately 0.759m leaf length.',
        'hinge_axis_m': {'start': [-.301, -.31, .101], 'end': [.301, -.31, .101]},
        'door_sweep_bounds_m': {'min': [-.305, -1.13, .04], 'max': [.305, -.285, .865]},
        'front_clear_from_closed_face_m': .82,
        'service_front_clear_m': 1.0,
        'basis': 'Conservative rounded concept envelope includes handle and door thickness; actual hinge/slide mechanism unselected.',
        'host_open_state_checked': False,
    }


def publish():
    for slug, parent in ASSETS.items():
        target = folder(slug)
        path = target / (slug + '.blend')
        if path.exists():
            print('PRESERVED existing immutable version', slug, flush=True)
            continue
        c = build(slug, parent)
        lo, hi = evaluated_bounds(c)
        target.mkdir(parents=True, exist_ok=True)
        bpy.data.libraries.write(str(path), {c}, fake_user=True, path_remap='RELATIVE_ALL')
        is_fridge = 'fridge' in slug
        meta = {
            'schema_version': 1, 'id': 'appliances/' + slug, 'version': 'v001',
            'name': 'Original smoked-oak integrated ' + ('48-inch refrigerator' if is_fridge else '24-inch dishwasher'),
            'units': 'meters', 'dimensions_m': [hi[i] - lo[i] for i in range(3)],
            'bounds_m': {'min': lo, 'max': hi},
            'blender': {'collection': c.name},
            'placement': {'origin': 'Floor center, local Z=0', 'front_direction': '-Y', 'up': '+Z',
                          'allowed_scaling': 'Rigid translation/rotation only; no appliance scaling'},
            'nominal_size_inches': [48, 30, 84] if is_fridge else [24, 24, 34],
            'installation': {
                'mounting': 'Level floor, host anti-tip restraint and selected manufacturer installation required',
                'clear_opening_concept_m': [1.2312, .792, 2.146] if is_fridge else [.6096, .635, .875],
                'opening_note': 'Clear opening excludes projecting pulls; actual selected product determines gaps and ventilation.',
                'countertop_note': 'Refrigerator is a full-height unit.' if is_fridge else 'Counter underside at least .875m concept height; countertop spans opening with support supplied by host. No cabinet carcass or drawer front occupies this bay.',
                'operating_envelope': operating(slug),
                'services': ['Electrical supply and optional water connection; removable front grille; verify ventilation area and heat release.'] if is_fridge else ['Adjacent sink water, drain and electrical service; access without trapping hoses or blocking toe-kick removal.'],
                'host_integration_checked': False,
            },
            'derived_from': {'id': 'appliances/' + parent, 'version': 'v001',
                             'path': '../../' + parent + '/v001/' + parent + '.blend',
                             'method': 'Append the actual published collection; retain physical size and origin.',
                             'changes': 'Replace white-oak materials with linked smoked oak and physical-meter UV; satin bronze pulls.' if is_fridge else 'Retain original enclosure/toe kick; remove stainless face, exposed controls and pull. Add separated smoked-oak panel, hidden top controls and satin bronze pull without altering standard enclosure size.'},
            'dependencies': [{'id': 'materials/smoked-oak', 'version': 'v001',
                              'path': '../../../materials/smoked-oak/v001/smoked-oak.blend'}],
            'source': {'kind': 'original derivative', 'generator': GENERATOR,
                       'command': 'Blender --background --python ' + GENERATOR,
                       'upstream_generator': 'tools/common/appliances.py'},
            'license': 'CC-BY-4.0', 'rights': 'Original concept geometry and materials by Homes project contributors; retain attribution. No manufacturer model or certified installation claim.',
            'files': {'blender': slug + '.blend', 'preview': 'preview.png', 'validation': 'validation.json'},
            'software': {'blender': bpy.app.version_string},
            'limitations': 'Original visualization appliance, closed-state modeled only. Operating envelopes are concept allowances, not manufacturer or code approval; host must verify actual open state and services.',
        }
        write_json(target / 'asset.json', meta)
        print('PUBLISHED', slug, meta['dimensions_m'], flush=True)


def preview(c, target, lo, hi):
    g.collection('Preview studio only')
    h = hi[2]
    center = Vector((0, 0, h * .5)) / g.F
    span = max(hi[i] - lo[i] for i in range(3)) / g.F
    bpy.context.scene.camera = g.camera('Native front three-quarter', center + Vector((span * 1.32, -span * 2.15, span * .85)), center, 55)
    ground = g.material('Neutral studio ground', (.29, .30, .29), .89)
    g.box('Studio ground', (0, 0, -.03), (100, 100, .06), ground)
    g.area('Large softbox', (-span, -span, span * 2), center, span * span * 14, span * 1.9, (1, .96, .91))
    g.area('Fill', (span, -span * .7, span), center, span * span * 6, span * 1.3, (.91, .95, 1))
    s = bpy.context.scene
    s.world = bpy.data.worlds.new('Neutral world')
    s.world.use_nodes = True
    s.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .35
    s.render.engine = 'CYCLES'
    s.cycles.device = 'CPU'
    s.cycles.samples = 32
    s.cycles.use_denoising = True
    s.render.threads_mode = 'FIXED'
    s.render.threads = 4
    s.render.resolution_x = 640
    s.render.resolution_y = 720
    s.render.resolution_percentage = 100
    s.render.image_settings.file_format = 'PNG'
    s.render.filepath = str(target / 'preview.png')
    s.view_settings.view_transform = 'AgX'
    bpy.ops.render.render(write_still=True)


def verify(render):
    for slug in ASSETS:
        target = folder(slug)
        path = target / (slug + '.blend')
        bpy.ops.wm.open_mainfile(filepath=str(path))
        assert all(lib.filepath.startswith('//') for lib in bpy.data.libraries)
        assert all(Path(bpy.path.abspath(lib.filepath, library=lib.parent)).exists() for lib in bpy.data.libraries)
        bpy.ops.wm.read_factory_settings(use_empty=True)
        with bpy.data.libraries.load(str(path), link=True) as (src, dst):
            dst.collections = [slug + ' | v001']
        c = dst.collections[0]
        bpy.context.scene.collection.children.link(c)
        lo, hi = evaluated_bounds(c)
        meta = json.loads((target / 'asset.json').read_text())
        assert all(abs(hi[i] - lo[i] - meta['dimensions_m'][i]) < 1e-5 for i in range(3))
        assert abs(lo[2]) < 1e-5
        oak_objects = [o for o in c.all_objects if o.type == 'MESH' and any(m and 'Smoked oak' in m.name for m in o.data.materials)]
        assert oak_objects and all('Timber meters' in o.data.uv_layers for o in oak_objects)
        panel_clearance = None
        if 'dishwasher' in slug:
            def y_bounds(o):
                return [min((o.matrix_world @ Vector(v)).y for v in o.bound_box),
                        max((o.matrix_world @ Vector(v)).y for v in o.bound_box)]
            panel = next(o for o in c.all_objects if 'smoked-oak door panel' in o.name)
            body = next(o for o in c.all_objects if 'appliance enclosure' in o.name)
            panel_rear = y_bounds(panel)[1]
            body_front = y_bounds(body)[0]
            panel_clearance = body_front - panel_rear
            assert panel_clearance > .010
            for obj in c.all_objects:
                if 'control deck' in obj.name or 'top-edge button' in obj.name:
                    mn, mx = y_bounds(obj)
                    assert panel_rear < mn < mx < body_front
        if render:
            preview(c, target, lo, hi)
        write_json(target / 'validation.json', {
            'fresh_native_reopen': True, 'fresh_collection_link': True,
            'relative_material_dependencies_resolve': True, 'evaluated_dimensions_m': [hi[i] - lo[i] for i in range(3)],
            'evaluated_bounds_m': {'min': lo, 'max': hi}, 'object_count': len(c.all_objects),
            'meter_grain_uv_objects': len(oak_objects), 'floor_origin_checked': True,
            'dishwasher_panel_to_enclosure_gap_m': panel_clearance,
            'preview_rendered': (target / 'preview.png').exists(),
            'preview_settings': {'renderer': 'Cycles CPU', 'samples': 32, 'size_px': [640, 720], 'view_transform': 'AgX'},
            'host_integration_checked': False, 'operating_state_geometry_checked': False,
            'software': {'blender': bpy.app.version_string},
        })
        print('VERIFIED', slug, flush=True)


if __name__ == '__main__':
    if '--verify' in sys.argv:
        verify('--render' in sys.argv)
    else:
        publish()
