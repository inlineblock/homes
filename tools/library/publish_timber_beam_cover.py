"""Original hollow nonstructural wood-look beam cover; shared cut-to-length stock.

blender -b --factory-startup --python tools/library/publish_timber_beam_cover.py
blender -b --factory-startup --python tools/library/publish_timber_beam_cover.py -- --verify --render
"""
from pathlib import Path
import bpy, hashlib, json, sys
from mathutils import Vector
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tools/library'))
from common import geometry as g
from common.timber_materials import grain_uv
from publish_modern_block import box, bounds, linked_mat
SLUG = 'cedar-steel-beam-cover-300x400'
ID = 'assemblies/' + SLUG
NAME = 'Hollow cedar-look steel beam cover 300x400 | v001'
FOLDER = ROOT / 'library' / ID / 'v001'
NATIVE = FOLDER / (SLUG + '.blend')
GEN = 'tools/library/publish_timber_beam_cover.py'


def publish():
    if NATIVE.exists():
        print('PRESERVE existing immutable asset', flush=True)
        return
    bpy.ops.wm.read_factory_settings(use_empty=True)
    c = g.collection(NAME)
    c['asset_id'] = ID
    c['asset_version'] = 'v001'
    mat = linked_mat('warm-vertical-cedar', 'v003')
    for name, loc, size in [
        ('Cover bottom soffit', (0, 0, .01), (1, .30, .02)),
        ('Cover left cheek', (0, -.14, .21), (1, .02, .38)),
        ('Cover right cheek', (0, .14, .21), (1, .02, .38)),
    ]:
        ob = box(name, loc, size, mat, .0006)
        grain_uv(ob)
        ob['component_role'] = 'Nonstructural wood-look finish cover; steel not included'
    bpy.context.view_layer.update()
    lo, hi = bounds(c)
    FOLDER.mkdir(parents=True, exist_ok=True)
    bpy.data.libraries.write(str(NATIVE), {c}, fake_user=True, path_remap='RELATIVE_ALL')
    meta = {
        'schema_version': 1, 'id': ID, 'version': 'v001', 'name': NAME, 'units': 'meters',
        'dimensions_m': [hi[i]-lo[i] for i in range(3)], 'bounds_m': {'min': lo, 'max': hi},
        'blender': {'collection': NAME},
        'placement': {'origin': 'Length/width center XY, bottom exposed soffit face Z=0',
                      'front_direction': 'Length along X, section width Y, open top +Z',
                      'allowed_scaling': 'Only local X length scaling 1.0 to 7.3152; Y and Z remain exactly 1. Rigid orientation may follow the host beam, including a roof pitch. Section and finish thickness cannot be scaled.',
                      'length_note': 'Native stock is 1 m long. X scale equals installed length in meters. Cut ends remain open; host supplies fitted terminations.'},
        'section': {'overall_width_m': .30, 'overall_height_m': .40, 'finish_thickness_m': .02,
                    'clear_cavity_y_m': [-.13, .13], 'clear_cavity_z_m': [.02, .40],
                    'suggested_steel_installation_gap_m': .01,
                    'steel_envelope_with_gap_m': {'y': [-.12, .12], 'z': [.03, .39]},
                    'basis': 'Geometric cover envelope only. Finish thickness and 10 mm steel gap are visualization assumptions, not a selected proprietary system.'},
        'mounting': 'Host-owned steel and concealed brackets support this non-load-bearing three-sided cover. Open top permits assembly around framing. Provide actual fastening, demountability, fire protection, movement allowance, end closures and weather detailing with selected materials.',
        'operating_envelope': {'state': 'Fixed three-board hollow U section', 'moving_parts': False,
                               'host_checked': False, 'basis': 'Host checks steel cavity, connection intersections and cover terminations.'},
        'appearance': {'material': 'Linked warm-vertical-cedar v003; subdued umber wood appearance.',
                       'mapping': 'Timber meters UV along native X. Cross-grain widths stay physical under permitted X scaling; longitudinal grain features elongate with stock length. This is an explicit visual approximation. For measured meter-scale longitudinal grain use a separately published length variant with regenerated UVs.',
                       'material_specification': 'Wood-look appearance only; no actual species, veneer, composite, fire rating or outdoor durability product specified.'},
        'dependencies': [{'id': 'materials/warm-vertical-cedar', 'version': 'v003', 'path': '../../../materials/warm-vertical-cedar/v003/warm-vertical-cedar.blend'}],
        'source': {'kind': 'original', 'generator': GEN, 'command': 'blender -b --factory-startup --python ' + GEN},
        'software': {'blender': bpy.app.version_string}, 'license': 'CC-BY-4.0',
        'rights': 'Original Homes project contributors geometry and linked original material; attribution Homes project contributors. No manufacturer or third-party source geometry.',
        'files': {'blender': NATIVE.name, 'preview': 'preview.png', 'validation': 'validation.json'},
        'product_status': 'Original concept cover only. Steel member selection and structural/fire/weather performance remain unverified. The cover is not a structural beam.'
    }
    (FOLDER/'asset.json').write_text(json.dumps(meta, indent=2)+'\n')
    print('PUBLISHED', ID, meta['dimensions_m'], flush=True)


def preview():
    g.collection('Cover preview studio only')
    floor = g.material('Cover preview warm gray', (.25, .26, .24), .9)
    box('Preview ground', (0,0,-.025), (200,200,.04), floor)
    s = bpy.context.scene
    target = Vector((0,0,.20))
    s.camera = g.camera('Hollow cover native preview', Vector((1.5,-1.5,1.2))/g.F, target/g.F, 57)
    g.area('Large soft key', Vector((1,-2,3))/g.F, target/g.F, 350, 2/g.F, (1,.97,.92))
    g.area('Gentle fill', Vector((-1,2,2))/g.F, target/g.F, 160, 2/g.F, (.93,.96,1))
    s.world = bpy.data.worlds.new('Cover neutral world')
    s.world.use_nodes = True
    s.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .35
    s.render.engine = 'CYCLES'; s.cycles.device = 'CPU'; s.cycles.samples = 32
    s.cycles.use_denoising = True; s.render.threads_mode = 'FIXED'; s.render.threads = 3
    s.render.resolution_x = 960; s.render.resolution_y = 720; s.render.resolution_percentage = 100
    s.render.image_settings.file_format = 'PNG'; s.render.filepath = str(FOLDER/'preview.png')
    s.view_settings.view_transform = 'AgX'; s.view_settings.exposure = 0
    bpy.ops.render.render(write_still=True)


def verify(render):
    sha_before = hashlib.sha256(NATIVE.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(NATIVE))
    assert all(l.filepath.startswith('//') for l in bpy.data.libraries)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(str(NATIVE), link=True) as (src, dst):
        assert NAME in src.collections
        dst.collections = [NAME]
    c = dst.collections[0]
    bpy.context.scene.collection.children.link(c)
    lo, hi = bounds(c)
    assert len(c.objects) == 3
    assert all(abs(hi[i]-lo[i]-v)<1e-5 for i,v in enumerate([1,.30,.40]))
    assert abs(lo[2])<1e-6
    assert all(Path(bpy.path.abspath(l.filepath, library=l.parent)).exists() for l in bpy.data.libraries)
    boxes = {o.name: tuple(o.dimensions) for o in c.objects}
    assert abs(boxes['Cover bottom soffit'][2]-.02)<1e-5
    assert all(abs(boxes[n][1]-.02)<1e-5 for n in ('Cover left cheek','Cover right cheek'))
    # Rays through the open top at cavity center must first hit the bottom soffit,
    # not a phantom solid timber body. Check seven transverse cavity positions.
    hits = []
    deps = bpy.context.evaluated_depsgraph_get()
    for y in (-.12,-.08,-.04,0,.04,.08,.12):
        hit, point, normal, face, obj, matrix = bpy.context.scene.ray_cast(deps, Vector((0,y,.6)), Vector((0,0,-1)))
        assert hit and abs(point.z-.02)<1e-5
        hits.append({'y_m': y, 'first_cover_z_m': point.z})
    if render: preview()
    assert hashlib.sha256(NATIVE.read_bytes()).hexdigest() == sha_before
    report = {'fresh_native_open': True, 'fresh_link': True, 'relative_dependencies_resolve': True,
              'collection': NAME, 'mesh_objects': 3, 'actual_dimensions_m': [hi[i]-lo[i] for i in range(3)],
              'origin_at_soffit': True, 'thickness_verified_m': .02, 'open_cavity_rays': hits,
              'native_sha256': sha_before, 'native_unchanged_by_review': True,
              'preview_rendered': (FOLDER/'preview.png').exists(), 'host_integration_checked': False,
              'preview_settings': {'renderer': 'Cycles CPU', 'threads': 3, 'samples': 32, 'resolution_px': [960,720]}}
    if (FOLDER/'preview.png').exists(): report['preview_sha256'] = hashlib.sha256((FOLDER/'preview.png').read_bytes()).hexdigest()
    (FOLDER/'validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print('VERIFIED', ID, flush=True)


if __name__ == '__main__':
    if '--verify' in sys.argv: verify('--render' in sys.argv)
    else: publish()
