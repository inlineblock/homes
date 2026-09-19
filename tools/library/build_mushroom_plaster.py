"""Original subdued mushroom mineral plaster; native assets CC BY 4.0, code MIT.

Run with Blender --factory-startup --background --python this_file -- publish,
preview, or verify. Preview uses CPU only. Existing adopted assets are immutable.
"""
from pathlib import Path
import json
import sys
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from library.build_lindon_palette import mineral
from library.build_lindon_assets import cube, material

SLUG = 'mushroom-mineral-plaster'
NAME = 'Mushroom mineral plaster | warm gray-brown | v001'
FOLDER = ROOT / 'library/materials' / SLUG / 'v001'
NATIVE = FOLDER / (SLUG + '.blend')
DARK = (.260, .235, .210)
LIGHT = (.320, .293, .265)

def publish():
    if NATIVE.exists():
        raise FileExistsError(f'Preserve adopted versions: {NATIVE}')
    parent = ROOT / 'library/materials/warm-limestone-plaster/v001/asset.json'
    assert parent.exists(), parent
    bpy.ops.wm.read_factory_settings(use_empty=True)
    m = mineral(NAME, DARK, LIGHT, 180, .88, 0, .00018)
    m.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value = .22
    FOLDER.mkdir(parents=True, exist_ok=True)
    bpy.data.libraries.write(str(NATIVE), {m}, fake_user=True, compress=True)
    meta = {
        'schema_version': 1, 'id': 'materials/' + SLUG, 'version': 'v001',
        'name': NAME, 'units': 'meters', 'license': 'CC-BY-4.0',
        'rights': 'Original procedural asset; attribution Homes project contributors',
        'derived_from': {'id': 'materials/warm-limestone-plaster', 'version': 'v001',
                         'basis': 'Existing original mineral shader, lower albedo and muted gray-brown palette; parent preserved.'},
        'source': {'kind': 'original', 'generator': 'tools/library/build_mushroom_plaster.py',
                   'helper': 'tools/library/build_lindon_palette.py:mineral',
                   'command': 'Blender --factory-startup --background --python tools/library/build_mushroom_plaster.py -- publish'},
        'files': {'blender': NATIVE.name, 'preview': 'preview.png'},
        'blender': {'material': NAME}, 'dependencies': [],
        'software': {'blender': bpy.app.version_string},
        'placement': 'Material-only asset with no geometric origin or operating envelope. Host supplies wall or panel geometry and real junctions.',
        'texture_scale': {'coordinates': 'World position in meters', 'noise_scale_per_m': 180,
                          'noise_detail': 2, 'bump_distance_m': .00018, 'bump_strength': .15},
        'linear_rgb': {'dark': list(DARK), 'light': list(LIGHT)},
        'roughness': .88, 'metallic': 0, 'specular_ior_level': .22,
        'variation': 'Subtle fine mineral texture only; fixed physical scale. Do not stretch texture or add broad cloudy marbling. Host supplies seams, reveals and weather details.',
        'changes_from_parent': 'Substantially reduced albedo, low-chroma mushroom/taupe warm gray-brown body color and softer specular response. Intended to avoid stark white, cream or pink facade fields.',
        'host_integration': {'checked': False, 'required': 'Review actual sunny and shaded host facades alongside adopted red brick and charcoal; a neutral sample is not host verification.'},
        'preview_settings': {'renderer': 'Cycles CPU', 'samples': 48, 'resolution_px': [1000, 860],
                             'color_management': 'AgX Medium High Contrast', 'exposure': 0,
                             'illumination': 'Neutral gray world strength 0.32; neutral broad and grazing area lights'},
        'limitations': 'Original concept finish, not a specified commercial plaster, assembly, color code or weather/fire certification.'
    }
    (FOLDER / 'asset.json').write_text(json.dumps(meta, indent=2) + '\n')
    (FOLDER / 'README.md').write_text('# Mushroom mineral plaster\n\n![Native neutral preview](preview.png)\n\n'
        'A subdued mushroom/taupe warm gray-brown finish for deliberate facade fields beside red brick and charcoal. '
        'Derived from warm-limestone-plaster/v001 with substantially darker low-chroma albedo; the original remains unchanged.\n\n'
        'Link material `' + NAME + '` from `' + NATIVE.name + '`. Texture coordinates are world meters, '
        'with fine mineral noise at 180 per meter, 0.18 mm bump distance and roughness 0.88. '
        'Linear color endpoints are (0.260, 0.235, 0.210) and (0.320, 0.293, 0.265).\n\n'
        'Original Homes project contributors asset, CC BY 4.0. Reproducible source: `tools/library/build_mushroom_plaster.py` (MIT). '
        'Run its `publish`, `preview`, and `verify` commands in Blender. CPU preview uses neutral light, AgX Medium High Contrast and exposure 0.\n\n'
        'Host sun/shade review is separate. This is an appearance concept without a commercial color, installation, durability or fire-performance specification.\n')
    (FOLDER / 'AGENTS.md').write_text('# Mushroom mineral plaster\n\n'
        '- Preserve this adopted version; publish the next version for changes.\n'
        '- Link the exact named native material and record host adoption. Read asset.json before placement.\n'
        '- Preserve subdued warm gray-brown body color; do not turn this option white, cream or pink.\n'
        '- Review neutral sample and actual sunny/shaded facade next to the other finishes. Correct unsuitable base albedo instead of masking it with scene exposure.\n'
        '- Maintain world-meter texture scale. Wall build-up, joints, flashing and performance remain host responsibilities.\n')
    print('MUSHROOM_PLASTER_PUBLISHED', NATIVE, flush=True)

def load():
    with bpy.data.libraries.load(str(NATIVE), link=True, relative=True) as (src, dst):
        assert NAME in src.materials, src.materials
        dst.materials = [NAME]
    return dst.materials[0]

def preview():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    m = load(); s = bpy.context.scene; c = s.collection
    floor = material('Neutral review floor', (.34, .33, .31), .85)
    cube('Neutral floor', (0, 0, -.07), (200, 200, .12), floor, c)
    cube('Mushroom plaster corner sample', (0, .12, 1.2), (2.7, .24, 2.4), m, c, .003)
    target = Vector((0, 0, 1.15))
    for name, pos, energy, size in [('Neutral broad key', (-3,-4,5), 420, 4), ('Neutral grazing light', (3,-2,4), 170, 2.5)]:
        light = bpy.data.lights.new(name, 'AREA'); light.energy = energy; light.shape = 'DISK'; light.size = size
        ob = bpy.data.objects.new(name, light); c.objects.link(ob); ob.location = pos
        ob.rotation_euler = (target-ob.location).to_track_quat('-Z','Y').to_euler()
    camera = bpy.data.cameras.new('Native material review'); ob = bpy.data.objects.new(camera.name, camera)
    c.objects.link(ob); ob.location = (3.7,-6.7,3.1); ob.rotation_euler = (target-ob.location).to_track_quat('-Z','Y').to_euler()
    camera.lens = 55; s.camera = ob
    s.world = bpy.data.worlds.new('Neutral material environment'); s.world.use_nodes = True
    s.world.node_tree.nodes['Background'].inputs[0].default_value = (.6,.6,.6,1)
    s.world.node_tree.nodes['Background'].inputs[1].default_value = .32
    s.render.engine = 'CYCLES'; s.cycles.device = 'CPU'; s.cycles.samples = 48; s.cycles.use_denoising = True
    s.render.resolution_x = 1000; s.render.resolution_y = 860; s.render.resolution_percentage = 100
    s.view_settings.view_transform = 'AgX'; s.view_settings.look = 'AgX - Medium High Contrast'; s.view_settings.exposure = 0
    s.render.image_settings.file_format = 'PNG'; s.render.filepath = str(FOLDER/'preview.png')
    bpy.ops.render.render(write_still=True)
    print('MUSHROOM_PLASTER_CPU_PREVIEW', s.render.filepath, flush=True)

def verify():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    m = load(); assert m.library and Path(bpy.path.abspath(m.library.filepath)).resolve() == NATIVE
    assert len(bpy.data.images) == 0, 'Procedural asset must not acquire image dependencies'
    assert not m.library.parent
    nodes = m.node_tree.nodes
    texture = next(n for n in nodes if n.bl_idname == 'ShaderNodeTexNoise')
    assert abs(texture.inputs['Scale'].default_value-180) < 1e-5
    p = nodes.get('Principled BSDF'); assert p.inputs['Base Color'].is_linked and p.inputs['Normal'].is_linked
    assert abs(p.inputs['Roughness'].default_value-.88) < 1e-5
    ramp = next(n for n in nodes if n.bl_idname == 'ShaderNodeValToRGB')
    colors = [list(e.color[:3]) for e in ramp.color_ramp.elements]
    assert all(abs(a-b) < 1e-5 for x,y in zip(colors,[DARK,LIGHT]) for a,b in zip(x,y))
    bpy.ops.wm.open_mainfile(filepath=str(NATIVE))
    assert NAME in bpy.data.materials and not bpy.data.libraries
    receipt = {'native_linked_in_fresh_process': True, 'native_reopened': True,
               'blender': bpy.app.version_string, 'material': NAME,
               'linear_rgb_verified': colors, 'physical_texture_scale_per_m': 180,
               'external_dependencies': [], 'host_integration_checked': False,
               'visual_preview_review': 'Pending actual CPU image inspection'}
    dest=FOLDER/'verification.json'
    if dest.exists():receipt['visual_preview_review']=json.loads(dest.read_text()).get('visual_preview_review',receipt['visual_preview_review'])
    dest.write_text(json.dumps(receipt,indent=2)+'\n')
    print('MUSHROOM_PLASTER_VERIFIED', json.dumps(receipt), flush=True)

if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['publish']
    {'publish':publish,'preview':preview,'verify':verify}[args[0]]()
