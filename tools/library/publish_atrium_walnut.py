"""Publish immutable warm-walnut derivatives with unchanged measured interfaces.

Blender -b --factory-startup --python tools/library/publish_atrium_walnut.py
Blender -b --factory-startup --python tools/library/publish_atrium_walnut.py -- --verify --render
"""
from pathlib import Path
import hashlib
import json
import sys

import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from common import geometry as g
from common.timber_materials import timber, grain_uv

MATERIAL = 'Warm walnut | natural brown | v001'
MATERIAL_DIR = ROOT / 'library/materials/warm-walnut/v001'
FAMILIES = {
    'walnut-drawer-base-2ft': ('cabinetry', 'smoked-oak-drawer-base-2ft'),
    'walnut-sink-base-36in': ('cabinetry', 'smoked-oak-sink-base-36in'),
    'walnut-oven-base-36in': ('cabinetry', 'smoked-oak-oven-base-36in'),
    'walnut-waste-pullout-18in': ('cabinetry', 'smoked-oak-waste-pullout-18in'),
    'walnut-pantry-shelf-2ft': ('cabinetry', 'smoked-oak-pantry-shelf-2ft'),
    'walnut-wardrobe-2ft': ('cabinetry', 'oak-wardrobe-2ft'),
    'walnut-cleaning-cabinet-2ft': ('cabinetry', 'oak-wardrobe-2ft'),
    'walnut-vanity-base-24in': ('cabinetry', 'smoked-oak-sink-base-36in'),
    'walnut-panel-ready-fridge-48in': ('appliances', 'smoked-oak-panel-ready-fridge-48in'),
    'walnut-panel-ready-dishwasher-24in': ('appliances', 'smoked-oak-panel-ready-dishwasher-24in'),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def select_collection(src, meta):
    explicit = meta.get('collection') or meta.get('blender', {}).get('collection')
    candidates = [n for n in src.collections if not any(w in n.lower() for w in ('preview', 'studio'))]
    if explicit:
        assert explicit in src.collections
        return explicit
    assert len(candidates) == 1, candidates
    return candidates[0]


def load_collection(path, meta, link=False):
    with bpy.data.libraries.load(str(path), link=link) as (src, dst):
        dst.collections = [select_collection(src, meta)]
    return dst.collections[0]


def objects(c, transform=Matrix.Identity(4)):
    for obj in c.objects:
        world = transform @ obj.matrix_world
        yield obj, world
        if obj.instance_type == 'COLLECTION' and obj.instance_collection:
            yield from objects(obj.instance_collection, world)
    for child in c.children:
        yield from objects(child, transform)


def bounds(c):
    points = [world @ Vector(p) for obj, world in objects(c) if obj.type in {'MESH', 'CURVE'} for p in obj.bound_box]
    return ([min(p[i] for p in points) for i in range(3)], [max(p[i] for p in points) for i in range(3)])


def geometry_signature(c):
    """UV/material edits are excluded; all parent geometry and placement remain."""
    records = []
    for obj, world in objects(c):
        r = {'type': obj.type, 'matrix': [list(row) for row in world]}
        if obj.type == 'MESH':
            r['vertices'] = [list(v.co) for v in obj.data.vertices]
            r['polygons'] = [list(p.vertices) for p in obj.data.polygons]
        elif obj.type == 'CURVE':
            r['splines'] = [[list(p.co) for p in s.bezier_points] for s in obj.data.splines]
            r['bevel'] = obj.data.bevel_depth
        else:
            continue
        records.append(r)
    return hashlib.sha256(json.dumps(sorted(records, key=lambda r: json.dumps(r, sort_keys=True)), sort_keys=True).encode()).hexdigest()


def vanity_dimensions(c):
    """Resize specific solid boards; preserve depth, hardware and plumbing access."""
    def resize(obj, axis, value):
        lo = min(v.co[axis] for v in obj.data.vertices)
        hi = max(v.co[axis] for v in obj.data.vertices)
        center = (lo + hi) / 2
        for v in obj.data.vertices:
            v.co[axis] = center + (v.co[axis] - center) * value / (hi - lo)
        obj.data.update()
    for obj in c.objects:
        if obj.instance_type == 'COLLECTION':
            obj.location.z -= .15122
        elif obj.type == 'MESH':
            if obj.name.startswith('Smoked oak cabinet side'):
                obj.location.x = (.3048 - .009) * (-1 if obj.location.x < 0 else 1)
                obj.location.z = (.72 + .1016) / 2
                resize(obj, 2, .72 - .1016)
            elif obj.name.startswith('Sink hinged door'):
                obj.location.x = .6096 / 4 * (-1 if obj.location.x < 0 else 1)
                obj.location.z -= .15122 / 2
                resize(obj, 0, .6096 / 2 - .004)
                resize(obj, 2, .619 - .15122)
            else:
                resize(obj, 0, max(v.co.x for v in obj.data.vertices) - min(v.co.x for v in obj.data.vertices) - .3048)
                if obj.name.startswith(('Countertop support rail', 'Sink fixed false front')):
                    obj.location.z -= .15122
    bpy.context.view_layer.update()


def material_manifest():
    return {
        'schema_version': 1, 'id': 'materials/warm-walnut', 'version': 'v001',
        'name': MATERIAL, 'units': 'meters', 'license': 'CC-BY-4.0',
        'rights': 'Original Homes project contributors material; attribution Homes project contributors',
        'source': {'kind': 'original', 'generator': 'tools/library/publish_atrium_walnut.py', 'shader': 'tools/common/timber_materials.py', 'software': bpy.app.version_string},
        'derived_from': {'id': 'materials/smoked-oak', 'version': 'v001', 'basis': 'Existing physical-meter grain algorithm with distinct warm walnut linear-color palette; no claim of an exact natural specimen.'},
        'dependencies': [], 'files': {'blender': 'warm-walnut.blend', 'preview': 'preview.png', 'validation': 'validation.json'},
        'blender': {'material': MATERIAL},
        'placement': 'Material-only asset; host supplies geometry and Timber meters UV mapping.',
        'texture_scale': {'uv_map': 'Timber meters', 'across_grain_m': .025, 'fiber_width_m': .003, 'mapping': 'common.timber_materials.grain_uv maps physical mesh meters along longest local axis; apply transforms before authoring UVs.'},
        'palette_linear': {'dark': [.025, .010, .004], 'mid': [.070, .028, .012], 'light': [.160, .070, .026]},
        'variation': 'Per-object seeded grain phase and .72–1.24 tone variation; matte finish. No external texture files.',
        'host_integration': {'checked': False, 'required': 'Inspect sunny/shaded host views and grain direction on vertical and horizontal members.'},
    }


def publish():
    material_path = MATERIAL_DIR / 'warm-walnut.blend'
    if not material_path.exists():
        bpy.ops.wm.read_factory_settings(use_empty=True)
        meta = material_manifest()
        palette = meta['palette_linear']
        mat = timber(MATERIAL, palette['dark'], palette['mid'], palette['light'])
        MATERIAL_DIR.mkdir(parents=True, exist_ok=True)
        bpy.data.libraries.write(str(material_path), {mat}, fake_user=True)
        (MATERIAL_DIR / 'asset.json').write_text(json.dumps(meta, indent=2) + '\n')
    for slug, (category, parent_slug) in FAMILIES.items():
        folder = ROOT / 'library' / category / slug / 'v001'
        path = folder / (slug + '.blend')
        if path.exists():
            print('IMMUTABLE_EXISTING', slug, flush=True)
            continue
        bpy.ops.wm.read_factory_settings(use_empty=True)
        parent_folder = ROOT / 'library' / category / parent_slug / 'v001'
        meta = json.loads((parent_folder / 'asset.json').read_text())
        parent_path = parent_folder / meta['files']['blender']
        c = load_collection(parent_path, meta)
        bpy.context.scene.collection.children.link(c)
        bpy.context.view_layer.update()
        parent_signature = geometry_signature(c)
        cleaning = slug == 'walnut-cleaning-cabinet-2ft'
        vanity = slug == 'walnut-vanity-base-24in'
        removed = []
        if cleaning:
            for obj in list(c.objects):
                if 'hanging rail' in obj.name.lower():
                    removed.append(obj.name)
                    bpy.data.objects.remove(obj, do_unlink=True)
            assert removed, 'Expected wardrobe rail for deliberate cleaning-storage variation'
        if vanity:
            vanity_dimensions(c)
        derived_signature = geometry_signature(c)
        with bpy.data.libraries.load(str(material_path), link=True) as (src, dst):
            dst.materials = [MATERIAL]
        walnut = dst.materials[0]
        count = 0
        for obj, _ in objects(c):
            if obj.library or obj.type != 'MESH':
                continue
            changed = False
            for slot in obj.material_slots:
                if slot.material and ('oak' in slot.material.name.lower() or (slot.material.library and 'oak' in slot.material.library.filepath.lower())):
                    slot.material = walnut
                    changed = True
            if changed:
                grain_uv(obj)
                count += 1
        assert count, (slug, 'No parent wood found')
        assert geometry_signature(c) == derived_signature
        c.name = slug + ' | v001'
        c['asset_id'] = category + '/' + slug
        c['asset_version'] = 'v001'
        c['finish_variation'] = 'Warm walnut; upper shelf retained, hanging rail removed for cleaning tools' if cleaning else 'Warm walnut; parent geometry and hardware unchanged'
        if vanity:
            c['finish_variation'] = 'Warm walnut vanity;720mm case height,609.6mm width; rigid original hardware'
            c['cabinet_height_m'] = .72
        lo, hi = bounds(c)
        folder.mkdir(parents=True, exist_ok=True)
        bpy.data.libraries.write(str(path), {c}, fake_user=True, path_remap='RELATIVE_ALL')
        meta.update(id=category + '/' + slug, version='v001', name=slug.replace('-', ' ').capitalize(),
                    dimensions_m=[hi[i] - lo[i] for i in range(3)], bounds_m={'min': lo, 'max': hi},
                    blender={'collection': c.name},
                    files={'blender': path.name, 'preview': 'preview.png', 'validation': 'validation.json'},
                    derived_from={'id': category + '/' + parent_slug, 'version': 'v001', 'basis': 'Upper shelf, doors and case retained; hanging rail removed for tall cleaning tools. Warm-walnut/v001 finish and physical-meter UVs added.' if cleaning else 'Identical measured native geometry, interfaces and hardware; wood changed to linked warm-walnut/v001 with physical-meter grain UVs.', 'parent_blend_sha256': digest(parent_path), 'parent_geometry_signature_sha256': parent_signature, 'geometry_signature_sha256': derived_signature, 'removed_objects': removed},
                    source={'kind': 'original', 'generator': 'tools/library/publish_atrium_walnut.py', 'software': bpy.app.version_string},
                    host_integration={'checked': False, 'required': 'Adopting home must check installation, service space and operating envelopes.'})
        deps = [d for d in meta.get('dependencies', []) if not ('materials/' in d['id'] and 'oak' in d['id'])]
        deps.insert(0, {'id': 'materials/warm-walnut', 'version': 'v001', 'path': '../../../materials/warm-walnut/v001/warm-walnut.blend'})
        meta['dependencies'] = deps
        if vanity:
            meta['description'] = 'Walnut two-door vanity base with open plumbing cavity; host supplies countertop and vessel basin.'
            meta['nominal_carcass_dimensions_m'] = [.6096, .6096, .72]
            meta['derived_from']['basis'] = 'Existing 36in sink-base geometry narrowed to24in and lowered to720mm by resizing individual case/door boards. Hardware retained rigid; sink cavity and open rear retained. Physical-meter walnut finish added.'
            meta['installation'] = {'mounting': 'Floor-supported 24in-wide,24in-deep,720mm-high vanity base. Host supplies30mm top for750mm top datum and approximately885mm vessel rim.', 'operating_envelope': {'modeled_state': 'Two closed editable doors', 'basis': 'Original reduced-width door geometry; unselected hardware', 'intended_open_angle_degrees': 100, 'reserve_front_door_projection_m': .305, 'reserve_front_depth_including_operator_m': 1.105, 'host_open_state_checked': False}, 'service_requirements': ['Open interior and rear preserve basin waste, trap and supply access; host must cut waste/faucet holes in top and avoid drawer boxes behind plumbing.', 'Host supplies wet-area finish suitability, wall anchorage and actual product coordination.'], 'compatible_fixture': {'id': 'fixtures/vanity-basin-mixer-mirror', 'version': 'v001', 'mounting_z_m': .75, 'mounting_center_y_m': -.0427, 'basis': 'Fixture mirror rear .3475m behind origin aligns with cabinet rear .3048m; host wall/backing and countertop depth remain coordinated.'}}
        if slug in {'walnut-wardrobe-2ft', 'walnut-cleaning-cabinet-2ft'}:
            meta['placement'] = {'origin': 'Floor-center of nominal footprint, Z=0', 'front_direction': '-Y', 'up': 'Z', 'allowed_scaling': 'Rigid translation and Z rotation only; no scaling.'}
            meta['installation'] = {'mounting': 'Floor-supported 2×2×8ft wardrobe; host supplies anti-tip anchorage and access to shelf/rail.', 'operating_envelope': {'modeled_state': 'Two closed editable hinged doors', 'intended_open_angle_degrees': 100, 'reserve_front_door_projection_m': .30, 'reserve_front_depth_including_operator_m': 1.10, 'host_open_state_checked': False, 'basis': 'Original .28956m door leaves with rounded concept operator allowance; hinges not animated.'}, 'service_requirements': ['Preserve standing space, bedroom door operation, accessible rail/shelf and wall-fixing access; no load or accessibility certification.']}
            if cleaning:
                meta['description'] = 'Walnut cleaning cupboard with upper shelf and clear lower volume for tall tools; no clothing rail.'
                meta['installation']['mounting'] = 'Floor-supported 2×2×8ft cleaning cupboard; host supplies anti-tip anchorage and accessible opening. Lower storage is clear of hanging rail.'
                meta['installation']['service_requirements'] = ['Preserve standing space and door operation; coordinate child-safe cleaning-product storage, ventilation and leak containment with selected contents. No load or accessibility certification.']
        (folder / 'asset.json').write_text(json.dumps(meta, indent=2) + '\n')
        basis = 'Individual case and door boards resized to24in width and720mm height; hardware retained rigid, with an open plumbing cavity.' if vanity else ('Upper shelf, doors and case retained; hanging rail removed for tall cleaning tools.' if cleaning else 'Geometry, hardware and measured interfaces are preserved.')
        (folder / 'README.md').write_text('# ' + meta['name'] + '\n\n[Manifest](asset.json) · [Native source](' + path.name + ') · [Validation](validation.json)\n\n![Native preview](preview.png)\n\nOriginal finish sibling of `' + category + '/' + parent_slug + '/v001`. ' + basis + ' The host must validate mounting, operating clearances and service access. The warm walnut material uses physical-meter grain mapping. CC BY 4.0; attribution Homes project contributors.\n')
        print('PUBLISHED', slug, 'wood meshes', count, flush=True)


def studio(folder, size, material_sample=False, filename='preview.png'):
    g.collection('Preview studio')
    s = bpy.context.scene
    h = size[2]
    extent = max(size[0], size[1], h)
    s.camera = g.camera('Asset preview', (extent * 2.0 / g.F, -extent * 2.8 / g.F, h * 1.45 / g.F), (0, 0, h * .49 / g.F), 55)
    neutral = g.material('Neutral studio floor', (.27, .28, .27), .85)
    g.box('Studio floor', (0, 0, -.016 / g.F), (200, 200, .032 / g.F), neutral)
    g.area('Neutral soft key', (2 / g.F, -3 / g.F, 4 / g.F), (0, 0, h * .5 / g.F), 600, 3 / g.F, (1, 1, 1))
    g.area('Neutral fill', (-2 / g.F, -1 / g.F, 2.5 / g.F), (0, 0, h * .5 / g.F), 240, 3 / g.F, (1, 1, 1))
    s.world = bpy.data.worlds.new('Neutral studio world')
    s.world.use_nodes = True
    s.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .30
    s.render.engine = 'CYCLES'
    s.cycles.device = 'CPU'
    s.cycles.samples = 24
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
    s.render.filepath = str(folder / filename)
    bpy.ops.render.render(write_still=True)


def verify(render=False):
    material_path = MATERIAL_DIR / 'warm-walnut.blend'
    bpy.ops.wm.open_mainfile(filepath=str(material_path))
    mat = bpy.data.materials.get(MATERIAL)
    assert mat and mat.use_nodes and mat['mapping'] == 'Timber meters'
    receipt = {'fresh_native_reopen': True, 'physical_meter_grain': True, 'external_textures': False, 'host_installation_checked': False, 'blend_sha256': digest(material_path)}
    if render:
        g.collection('Walnut sample')
        for i in range(6):
            o = g.box('Vertical walnut board', ((i - 2.5) * .19 / g.F, 0, .70 / g.F), (.184 / g.F, .035 / g.F, 1.4 / g.F), mat, .001 / g.F)
            grain_uv(o)
        o = g.box('Horizontal walnut member', (0, -.065 / g.F, .26 / g.F), (1.28 / g.F, .085 / g.F, .17 / g.F), mat, .001 / g.F)
        grain_uv(o)
        studio(MATERIAL_DIR, (1.3, .15, 1.4), True)
    receipt['preview_rendered'] = (MATERIAL_DIR / 'preview.png').exists()
    if receipt['preview_rendered']:
        receipt['preview_sha256'] = digest(MATERIAL_DIR / 'preview.png')
    receipt['preview_settings'] = {'renderer': 'Cycles CPU', 'samples': 24, 'resolution': [640, 640], 'view_transform': 'AgX', 'look': 'Medium High Contrast', 'exposure': 0, 'lights': 'Neutral key, fill and world'}
    (MATERIAL_DIR / 'validation.json').write_text(json.dumps(receipt, indent=2) + '\n')
    for slug, (category, parent_slug) in FAMILIES.items():
        folder = ROOT / 'library' / category / slug / 'v001'
        path = folder / (slug + '.blend')
        meta = json.loads((folder / 'asset.json').read_text())
        bpy.ops.wm.open_mainfile(filepath=str(path))
        assert all(lib.filepath.startswith('//') for lib in bpy.data.libraries), [(l.name, l.filepath) for l in bpy.data.libraries]
        assert all(Path(bpy.path.abspath(lib.filepath, library=lib.parent)).exists() for lib in bpy.data.libraries)
        bpy.ops.wm.read_factory_settings(use_empty=True)
        c = load_collection(path, meta, link=True)
        bpy.context.scene.collection.children.link(c)
        bpy.context.view_layer.update()
        lo, hi = bounds(c)
        dims = [hi[i] - lo[i] for i in range(3)]
        assert all(abs(dims[i] - meta['dimensions_m'][i]) < 1e-6 for i in range(3))
        assert abs(lo[2]) < 1e-6
        assert geometry_signature(c) == meta['derived_from']['geometry_signature_sha256']
        wood = [obj for obj, _ in objects(c) if obj.type == 'MESH' and any(m and m.name == MATERIAL for m in obj.data.materials)]
        assert wood and all(o.data.uv_layers.get('Timber meters') for o in wood)
        assert all(m.library and 'warm-walnut' in m.library.filepath for obj in wood for m in obj.data.materials if m and m.name == MATERIAL)
        receipt = {'fresh_native_reopen': True, 'fresh_link': True, 'relative_dependencies_resolved': True, 'geometry_identical_to_parent': slug not in {'walnut-cleaning-cabinet-2ft', 'walnut-vanity-base-24in'}, 'geometry_signature_sha256': meta['derived_from']['geometry_signature_sha256'], 'dimensions_m': dims, 'floor_contact': True, 'wood_meshes_with_meter_uv': len(wood), 'linked_walnut_material': True, 'host_installation_checked': False, 'operating_state': 'Closed or open shelf; no host motion verification', 'blend_sha256': digest(path), 'preview_settings': {'renderer': 'Cycles CPU', 'samples': 24, 'resolution': [640, 640], 'view_transform': 'AgX', 'look': 'Medium High Contrast', 'exposure': 0, 'lights': 'Neutral key, fill and world'}}
        if slug == 'walnut-cleaning-cabinet-2ft':
            assert not any('hanging rail' in o.name.lower() for o, _ in objects(c))
            assert any('upper shelf' in o.name.lower() for o, _ in objects(c))
            receipt['cleaning_storage'] = {'hanging_rail_removed': True, 'upper_shelf_retained': True, 'clear_lower_storage': 'Continuous lower case below retained upper shelf; contents and host integration not verified.'}
        if render:
            studio(folder, dims)
            if slug in {'walnut-cleaning-cabinet-2ft', 'walnut-vanity-base-24in'}:
                bpy.ops.wm.read_factory_settings(use_empty=True)
                cutaway = load_collection(path, meta, link=False)
                bpy.context.scene.collection.children.link(cutaway)
                hidden = []
                for obj in cutaway.objects:
                    if any(label in obj.name.lower() for label in ('hinged', 'door pull', 'pull mount')):
                        obj.hide_render = True
                        hidden.append(obj.name)
                assert hidden
                studio(folder, dims, filename='preview-interior.png')
                receipt['interior_review_preview'] = {'file': 'preview-interior.png', 'mode': 'Front doors and handles hidden for cavity inspection; not a modeled open-door operation', 'hidden_objects': hidden}
                meta['files']['interior_preview'] = 'preview-interior.png'
                (folder / 'asset.json').write_text(json.dumps(meta, indent=2) + '\n')
        receipt['preview_rendered'] = (folder / 'preview.png').exists()
        if receipt['preview_rendered']:
            receipt['preview_sha256'] = digest(folder / 'preview.png')
        receipt['dependency_sha256'] = {d['id'] + '/' + d['version']: digest((folder / d['path']).resolve()) for d in meta['dependencies']}
        if (folder / 'preview-interior.png').exists():
            receipt['interior_review_preview'] = {'file': 'preview-interior.png', 'sha256': digest(folder / 'preview-interior.png'), 'mode': 'Front doors and handles hidden for cavity inspection; not a modeled open-door operation'}
        (folder / 'validation.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print('VERIFIED', slug, flush=True)


if __name__ == '__main__':
    if '--verify' in sys.argv:
        verify('--render' in sys.argv)
    else:
        publish()
