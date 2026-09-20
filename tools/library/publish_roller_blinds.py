"""Original measured roller-blind concepts, with real open and closed geometry.

Blender -b --factory-startup --python tools/library/publish_roller_blinds.py
Blender -b --factory-startup --python tools/library/publish_roller_blinds.py -- --verify --render

No fabric opacity trick, simulated motion, product rating or blackout claim.
"""
from pathlib import Path
import hashlib
import json
import sys

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from common import geometry as g

SIZES = {
    'roller-blackout-42in-78in': (1.0668, 1.9812),
    'roller-blackout-54in-78in': (1.3716, 1.9812),
    'roller-blackout-48in-107p4in': (1.2192, 2.72796),
    'roller-blackout-60in-107p4in': (1.524, 2.72796),
}
FABRIC_PATH = ROOT / 'library/materials/woven-oatmeal/v001/woven-oatmeal.blend'
OPEN_DROP = .30


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def box(name, loc, size, material, part, bevel=.001):
    obj = g.box(name, [v / g.F for v in loc], [v / g.F for v in size], material, bevel / g.F)
    obj['blind_part'] = part
    return obj


def palette():
    with bpy.data.libraries.load(str(FABRIC_PATH), link=True) as (src, dst):
        assert len(src.materials) == 1, src.materials
        dst.materials = [src.materials[0]]
    fabric = dst.materials[0]
    return {
        'fabric': fabric,
        'case': g.material('Blind warm ivory powder-coated cassette concept', (.52, .49, .43), .45, .05),
        'cap': g.material('Blind restrained bronze end cap concept', (.085, .065, .043), .4, .50),
        'bracket': g.material('Blind generic mounting bracket', (.20, .21, .20), .40, .70),
    }


def build_state(slug, width, full_drop, state, mats):
    c = g.collection(slug + ' ' + state)
    c['asset_id'] = 'openings/' + slug
    c['asset_version'] = 'v001'
    c['state'] = state
    c['nominal_opening_width_m'] = width
    c['nominal_full_drop_m'] = full_drop
    c['actual_drop_m'] = OPEN_DROP if state == 'open' else full_drop
    c['origin'] = 'Header-center; Z0; hanging -Z; front -Y'
    w = width - .012
    drop = c['actual_drop_m']
    box('Cassette closed housing', (0, 0, 0), (w, .110, .090), mats['case'], 'cassette', .009)
    box('Cassette narrow front lower lip', (0, -.057, -.032), (w - .018, .007, .012), mats['case'], 'cassette', .002)
    for sign in [-1, 1]:
        box('Cassette removable end cap', (sign * (w / 2 - .004), 0, 0), (.008, .102, .080), mats['cap'], 'end_cap', .004)
        box('Rear mounting tab', (sign * (w / 2 - .09), .0625, .009), (.034, .015, .055), mats['bracket'], 'mount', .002)
    cloth_top = -.038
    cloth_bottom = -drop + .015
    panel = box('Opaque woven oatmeal shade', (0, -.027, (cloth_top + cloth_bottom) / 2),
                (width - .050, .0025, cloth_top - cloth_bottom), mats['fabric'], 'fabric', .0003)
    panel['privacy_geometry'] = 'Opaque actual mesh panel; no material-opacity state switching'
    box('Weighted bottom rail', (0, -.027, -drop + .009), (width - .045, .021, .018), mats['case'], 'bottom_rail', .003)
    bpy.context.view_layer.update()
    return c


def bounds(c):
    points = [o.matrix_world @ Vector(p) for o in c.all_objects if o.type == 'MESH' for p in o.bound_box]
    return {'min': [min(p[i] for p in points) for i in range(3)],
            'max': [max(p[i] for p in points) for i in range(3)]}


def dimensions(b):
    return [b['max'][i] - b['min'][i] for i in range(3)]


def publish():
    for slug, (width, drop) in SIZES.items():
        folder = ROOT / 'library/openings' / slug / 'v001'
        path = folder / (slug + '.blend')
        if path.exists():
            print('IMMUTABLE_EXISTING', slug, flush=True)
            continue
        bpy.ops.wm.read_factory_settings(use_empty=True)
        mats = palette()
        states = {state: build_state(slug, width, drop, state, mats) for state in ('open', 'closed')}
        measured = {state: bounds(c) for state, c in states.items()}
        folder.mkdir(parents=True, exist_ok=True)
        bpy.data.libraries.write(str(path), set(states.values()), fake_user=True, path_remap='RELATIVE_ALL')
        meta = {
            'schema_version': 1, 'id': 'openings/' + slug, 'version': 'v001',
            'name': slug.replace('-', ' ').capitalize() + ' | two states', 'units': 'meters',
            'license': 'CC-BY-4.0', 'rights': 'Original Homes project contributors geometry; attribution Homes project contributors. Existing woven-oatmeal material retains its original license.',
            'source': {'kind': 'original', 'generator': 'tools/library/publish_roller_blinds.py', 'software': bpy.app.version_string},
            'derived_from': None,
            'dependencies': [{'id': 'materials/woven-oatmeal', 'version': 'v001', 'path': '../../../materials/woven-oatmeal/v001/woven-oatmeal.blend'}],
            'files': {'blender': path.name, 'preview': 'preview.png', 'closed_preview': 'preview-closed.png', 'validation': 'validation.json'},
            'blender': {'collection': slug + ' open', 'states': {'open': slug + ' open', 'closed': slug + ' closed'}},
            'dimensions_m': dimensions(measured['open']), 'bounds_m': measured['open'],
            'nominal_opening_m': {'width': width, 'drop': drop, 'width_basis': 'Full framed bay pitch; host visible glazing is pitch minus84mm'},
            'state_bounds_m': measured,
            'state_dimensions_m': {state: dimensions(b) for state, b in measured.items()},
            'placement': {'origin': 'Cassette/header center at Z0; closed bottom-rail lower edge is at -nominal drop', 'front_direction': '-Y; hanging -Z; width along X', 'up': 'Z', 'allowed_scaling': 'Rigid translation and rotation only; use exact dimensioned sibling. Choose one state collection per installed blind.'},
            'installation': {
                'mounting': 'Interior wall/header-mounted concept, with rear tabs. Host supplies blocking, fixing and clear separation from glazing, sash/door motion and handles.',
                'fixed_envelope_m': {'cassette_width': width - .012, 'cassette_body_depth': .110, 'cassette_top_z': .045, 'rear_tab_y_max': .070},
                'fabric_plane_y_m': -.027, 'fabric_thickness_m': .0025, 'fabric_width_m': width - .050,
                'adjacent_bay_fit': {'nominal_width_is_bay_pitch': True, 'visible_glass_width_m': width - .084, 'fabric_overlap_each_jamb_m': .017, 'cassette_gap_between_adjacent_equal_pitch_bays_m': .012, 'basis': 'Host frame has42mm sightline each side. Actual optical edge sealing and host alignment must be checked.'},
                'operating_envelope': {'modeled_states': ['open', 'closed'], 'default_state': 'open', 'open_drop_m': OPEN_DROP, 'closed_drop_m': drop, 'motion': 'Two discrete static collection states with different physical fabric lengths and rail elevations; no rig or animation.', 'host_open_state_checked': False, 'basis': 'Original concept geometry sized to nominal opening; no selected manufacturer.', 'sweep': 'Shade travels vertically within the same fabric and rail depth envelope.'},
                'service_requirements': ['Keep right (+X) end-cap service access available; conceptual 150mm side access is a starting allowance, not a manufacturer specification.', 'Cordless/motor-ready appearance only; actual actuation, power, controls, safety, attachments, cleaning and replaceability must be selected by host.', 'Opaque fabric geometry alone does not establish edge light sealing, tested blackout, fire performance, acoustic properties or any certification.'],
            },
            'host_integration': {'checked': False, 'required': 'Check final header/sill placement, state selection, window operation, handle clearance, edge coverage and privacy from the actual view.'},
            'limitations': 'Original generic interior shade concept. Blackout is a design intent in the asset name, not a tested product-performance claim. No commercial product or manufacturer CAD.',
        }
        (folder / 'asset.json').write_text(json.dumps(meta, indent=2) + '\n')
        (folder / 'README.md').write_text('# ' + meta['name'] + '\n\n[Manifest](asset.json) · [Native source](' + path.name + ') · [Validation](validation.json)\n\n| Open: 300mm drop | Closed: full nominal drop |\n| --- | --- |\n| ![Open shade](preview.png) | ![Closed shade](preview-closed.png) |\n\nChoose exactly one of the two declared collections per installed blind. Both retain the same cassette, mounting tabs and end caps. The closed state contains an actual opaque woven-oatmeal panel and lowered weighted rail. Header-center origin, front −Y, hangs −Z; scale1 only.\n\nThe host resolves attachments, opening/handle clearance, edge coverage, actuation and maintenance. Opaque concept geometry is not tested blackout performance. Original CC BY4.0 geometry; attribution Homes project contributors.\n')
        print('PUBLISHED', slug, flush=True)


def studio(folder, width, full_drop, state):
    g.collection('Blind preview studio')
    s = bpy.context.scene
    shown_drop = OPEN_DROP if state == 'open' else full_drop
    center = -shown_drop / 2
    extent = max(width, shown_drop)
    s.camera = g.camera('Blind preview', (extent * .65 / g.F, -extent * 2.9 / g.F, (center + extent * .26) / g.F), (0, 0, center / g.F), 60)
    wall = g.material('Neutral warm gray preview backdrop', (.34, .35, .33), .90)
    g.box('Studio wall', (0, .25 / g.F, center / g.F), (12 / g.F, .08 / g.F, 12 / g.F), wall)
    g.area('Neutral large key', (-1.8 / g.F, -2.5 / g.F, 1.4 / g.F), (0, 0, center / g.F), 450, 2.5 / g.F, (1, 1, 1))
    g.area('Neutral soft fill', (1.8 / g.F, -2 / g.F, -1 / g.F), (0, 0, center / g.F), 180, 2.5 / g.F, (1, 1, 1))
    s.world = bpy.data.worlds.new('Neutral preview world')
    s.world.use_nodes = True
    s.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .25
    s.render.engine = 'CYCLES'
    s.cycles.device = 'CPU'
    s.cycles.samples = 20
    s.cycles.use_denoising = True
    s.render.threads_mode = 'FIXED'
    s.render.threads = 4
    s.render.resolution_x = 640
    s.render.resolution_y = 640
    s.render.resolution_percentage = 100
    s.view_settings.view_transform = 'AgX'
    s.view_settings.look = 'AgX - Medium High Contrast'
    s.view_settings.exposure = 0
    s.render.image_settings.file_format = 'PNG'
    s.render.filepath = str(folder / ('preview.png' if state == 'open' else 'preview-closed.png'))
    bpy.ops.render.render(write_still=True)


def fixed_signature(c):
    data = []
    for o in c.objects:
        if o.get('blind_part') in {'cassette', 'end_cap', 'mount'}:
            data.append({'part': o['blind_part'], 'transform': [list(r) for r in o.matrix_world], 'vertices': [list(v.co) for v in o.data.vertices]})
    return hashlib.sha256(json.dumps(sorted(data, key=lambda d: json.dumps(d, sort_keys=True)), sort_keys=True).encode()).hexdigest()


def verify(render):
    for slug, (width, full_drop) in SIZES.items():
        folder = ROOT / 'library/openings' / slug / 'v001'
        path = folder / (slug + '.blend')
        meta = json.loads((folder / 'asset.json').read_text())
        bpy.ops.wm.open_mainfile(filepath=str(path))
        assert all(l.filepath.startswith('//') for l in bpy.data.libraries)
        assert all(Path(bpy.path.abspath(l.filepath, library=l.parent)).exists() for l in bpy.data.libraries)
        states = {}
        fixed = []
        for state in ('open', 'closed'):
            bpy.ops.wm.read_factory_settings(use_empty=True)
            name = meta['blender']['states'][state]
            with bpy.data.libraries.load(str(path), link=True) as (src, dst):
                assert name in src.collections
                dst.collections = [name]
            c = dst.collections[0]
            bpy.context.scene.collection.children.link(c)
            bpy.context.view_layer.update()
            measured = bounds(c)
            drop = OPEN_DROP if state == 'open' else full_drop
            assert abs(measured['min'][2] + drop) < 1e-5
            assert abs(measured['max'][2] - .045) < 1e-5
            assert abs(dimensions(measured)[0] - (width - .012)) < 1e-5
            assert all(abs(measured[k][i] - meta['state_bounds_m'][state][k][i]) < 1e-5 for k in ('min', 'max') for i in range(3))
            panels = [o for o in c.objects if o.get('blind_part') == 'fabric']
            assert len(panels) == 1
            panel = panels[0]
            assert panel.type == 'MESH' and len(panel.data.polygons) >= 6
            assert abs(panel.dimensions.x - (width - .050)) < 1e-5
            mat = panel.data.materials[0]
            assert mat.library and 'woven-oatmeal' in mat.library.filepath
            principled = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
            assert not principled.inputs['Alpha'].is_linked and principled.inputs['Alpha'].default_value == 1
            assert not principled.inputs['Transmission Weight'].is_linked and principled.inputs['Transmission Weight'].default_value == 0
            fixed.append(fixed_signature(c))
            states[state] = {'fresh_link': True, 'bounds_m': measured, 'physical_opaque_panel': True, 'panel_width_m': float(panel.dimensions.x), 'jamb_overlap_for_declared_host_frame_m': (float(panel.dimensions.x) - (width - .084)) / 2, 'cassette_gap_at_nominal_pitch_m': width - dimensions(measured)[0], 'bottom_rail_bottom_z_m': -drop}
            if render:
                studio(folder, width, full_drop, state)
            preview = folder / ('preview.png' if state == 'open' else 'preview-closed.png')
            states[state]['preview_exists'] = preview.exists()
            if preview.exists():
                states[state]['preview_sha256'] = digest(preview)
        assert fixed[0] == fixed[1]
        receipt = {'fresh_native_reopen': True, 'relative_dependencies_resolved': True, 'same_fixed_hardware_both_states': True, 'fixed_geometry_signature_sha256': fixed[0], 'state_checks': states, 'blend_sha256': digest(path), 'fabric_dependency_sha256': digest(FABRIC_PATH), 'host_installation_checked': False, 'blackout_performance_tested': False, 'preview_settings': {'renderer': 'Cycles CPU', 'threads': 4, 'samples': 20, 'resolution': [640, 640], 'view_transform': 'AgX', 'look': 'Medium High Contrast', 'exposure': 0, 'lights': 'Neutral key/fill and gray backdrop'}}
        (folder / 'validation.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print('VERIFIED', slug, flush=True)


if __name__ == '__main__':
    if '--verify' in sys.argv:
        verify('--render' in sys.argv)
    else:
        publish()
