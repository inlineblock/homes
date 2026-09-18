"""Publish original reviewed timber revisions without changing adopted assets."""
import bpy, json, sys, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from common.timber_materials import timber, grain_uv
from common import geometry as g
from common.geometry import box, area, camera

SPECS = [
    ('warm-vertical-cedar', 'v003', 'v002', 'Cedar | smoked umber | physical grain',
     (.026, .018, .010), (.063, .043, .023), (.125, .090, .050)),
    ('mountain-thermo-ash', 'v002', 'v001', 'Thermo ash | deep natural brown | physical grain',
     (.018, .013, .008), (.048, .033, .018), (.100, .070, .036)),
]


def publish(root=ROOT):
    for slug, ver, parent, name, dark, mid, light in SPECS:
        folder = root / 'library/materials' / slug / ver
        path = folder / (slug + '.blend')
        if path.exists():
            continue
        folder.mkdir(parents=True, exist_ok=True)
        m = timber(name, dark, mid, light)
        bpy.data.libraries.write(str(path), {m}, fake_user=True)
        meta = {
            'schema_version': 1, 'id': 'materials/' + slug, 'version': ver,
            'name': name, 'units': 'meters', 'license': 'CC-BY-4.0',
            'rights': 'Original procedural material; attribution Homes project contributors',
            'derived_from': {'id': 'materials/' + slug, 'version': parent},
            'source': {'kind': 'original', 'generator': 'tools/library/publish_timber.py',
                       'shader': 'tools/common/timber_materials.py'},
            'files': {'blender': path.name, 'preview': 'preview.png'},
            'dependencies': [], 'software': {'blender': bpy.app.version_string},
            'texture_scale': {'uv_map': 'Timber meters', 'U': 'meters across grain',
                              'V': 'meters along grain', 'growth_width_m': .025,
                              'fiber_width_m': .003, 'bump_distance_m': .00065},
            'placement': {'mapping': 'Run common.timber_materials.grain_uv on applied local meshes; longest local axis defines grain.',
                          'allowed_variation': 'Seeded per-object growth grain and 0.72–1.24 tonal multiplier; keep meter UV scale.',
                          'limitations': 'Original finish visualization; no species, coating durability or fire/performance certification. End faces use transverse grain rather than a product-specific growth-ring scan.'},
            'change_from_parent': 'Neutral deeper brown, unique growth sample and tone per board, two grain scales, varied matte roughness and length-aligned physical UVs.',
            'preview_command': 'Blender --background --python-exit-code 1 --python tools/library/publish_timber.py -- --previews',
        }
        (folder / 'asset.json').write_text(json.dumps(meta, indent=2) + '\n')


def previews():
    for slug, ver, *_ in SPECS:
        folder = ROOT / 'library/materials' / slug / ver
        bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
        with bpy.data.libraries.load(str(folder / (slug + '.blend')), link=True) as (a, b):
            b.materials = [a.materials[0]]
        m = b.materials[0]; g.collection('Timber material review')
        for i in range(9):
            o = box('Individually seeded vertical sample board', ((i - 4) * .51, 0, 3), (.49, .16, 6), m, .006)
            grain_uv(o)
        o = box('Long horizontal beam sample', (0, -.17, .48), (4.8, .30, .48), m, .015); grain_uv(o)
        world = bpy.data.worlds.new('Neutral preview daylight'); world.use_nodes = True
        world.node_tree.nodes['Background'].inputs[0].default_value = (.65, .70, .75, 1)
        world.node_tree.nodes['Background'].inputs[1].default_value = .4
        bpy.context.scene.world = world
        area('Large neutral daylight', (-4, -6, 8), (0, 0, 3), 280, 5, (1, 1, 1))
        s = bpy.context.scene; s.camera = camera('Material portrait', (6, -10, 6), (0, 0, 3), 52)
        s.render.engine = 'CYCLES'; s.cycles.samples = 128; s.cycles.use_denoising = True
        s.render.resolution_x = 1200; s.render.resolution_y = 1400; s.render.resolution_percentage = 100
        s.view_settings.view_transform = 'AgX'; s.view_settings.look = 'AgX - Medium High Contrast'; s.view_settings.exposure = -.35
        prefs = bpy.context.preferences.addons['cycles'].preferences; prefs.compute_device_type = 'METAL'; prefs.get_devices()
        for dev in prefs.devices: dev.use = dev.type == 'METAL'
        s.cycles.device = 'GPU'; s.render.filepath = str(folder / 'preview.png')
        bpy.ops.render.render(write_still=True)
        print('TIMBER_PREVIEW', slug, ver, flush=True)


if __name__ == '__main__':
    publish()
    if '--previews' in sys.argv: previews()
