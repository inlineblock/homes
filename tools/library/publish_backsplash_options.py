"""Publish three original/reused backsplash options; immutable v001 files.

Blender -b --factory-startup --python tools/library/publish_backsplash_options.py
Blender -b --factory-startup --python tools/library/publish_backsplash_options.py -- --verify --render
Blender -b --factory-startup --python tools/library/publish_backsplash_options.py -- --installation-preview
"""
from pathlib import Path
import json
import math
import sys
import bpy
import bmesh
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from common import geometry as g

GEN = 'tools/library/publish_backsplash_options.py'
SLUGS = ['cream-veined-slab-backsplash-48x24', 'warm-ivory-handmade-tile-4in', 'sage-stacked-backsplash-12x24']
NAMES = ['Cream veined slab backsplash 48 x 24 in', 'Warm ivory handmade-look tile 4 in', 'Sage stacked backsplash 12 x 24 in']


def folder(slug):
    return ROOT / 'library/surfaces' / slug / 'v001'


def box(name, pos, size, mat, bevel=0):
    return g.box(name, Vector(pos) / g.F, Vector(size) / g.F, mat, bevel / g.F)


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def points(collection, matrix=None):
    matrix = matrix if matrix is not None else Matrix.Identity(4)
    for ob in collection.objects:
        transform = matrix @ ob.matrix_world
        if ob.instance_type == 'COLLECTION' and ob.instance_collection:
            yield from points(ob.instance_collection, transform @ Matrix.Translation(-ob.instance_collection.instance_offset))
        elif ob.type == 'MESH':
            for corner in ob.bound_box:
                yield transform @ Vector(corner)
    for child in collection.children:
        yield from points(child, matrix)


def bounds(collection):
    pts = list(points(collection))
    return [min(p[i] for p in pts) for i in range(3)], [max(p[i] for p in pts) for i in range(3)]


def instance(collection, target, name, xyz):
    ob = bpy.data.objects.new(name, None)
    ob.instance_type = 'COLLECTION'
    ob.instance_collection = target
    ob.location = xyz
    collection.objects.link(ob)
    return ob


def dependency(slug, category='materials'):
    return {'id': category + '/' + slug, 'version': 'v001', 'path': '../../../' + category + '/' + slug + '/v001/' + slug + '.blend'}


def glaze():
    mat = g.material('Original warm ivory ceramic glaze | backsplash v001', (.74, .69, .59), .24)
    n, l = mat.node_tree.nodes, mat.node_tree.links
    p = n.get('Principled BSDF')
    p.inputs['Coat Weight'].default_value = .25
    p.inputs['Coat Roughness'].default_value = .16
    info = n.new('ShaderNodeObjectInfo')
    ramp = n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (.66, .61, .50, 1)
    ramp.color_ramp.elements[1].color = (.83, .79, .69, 1)
    l.new(info.outputs['Random'], ramp.inputs[0])
    l.new(ramp.outputs[0], p.inputs['Base Color'])
    geo = n.new('ShaderNodeNewGeometry')
    noise = n.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 620
    l.new(geo.outputs['Position'], noise.inputs['Vector'])
    bump = n.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = .08
    bump.inputs['Distance'].default_value = .00008
    l.new(noise.outputs['Fac'], bump.inputs['Height'])
    l.new(bump.outputs[0], p.inputs['Normal'])
    return mat


def handmade_tile(c):
    # Closed ceramic mesh: gently undulating front and irregular perimeter,
    # bounded by 98mm square; rear plane is exactly Y=0.
    N, w = 12, .098
    verts = []
    for j in range(N + 1):
        for i in range(N + 1):
            u, v = i / N, j / N
            x = (u - .5) * w
            z = v * w
            if i in [0, N]:
                x += (1 if i == 0 else -1) * .00045 * math.sin(math.pi * v) ** 2
            if j in [0, N]:
                z += (1 if j == 0 else -1) * .0004 * math.sin(math.pi * u) ** 2
            y = .0088 + .00055 * math.sin(math.pi * u) * math.sin(2 * math.pi * v + .7)
            verts.append((x, y, z))
    faces = []
    for j in range(N):
        for i in range(N):
            k = j * (N + 1) + i
            faces.append((k, k + N + 1, k + N + 2, k + 1))
    ring = list(range(N + 1)) + [j * (N + 1) + N for j in range(1, N + 1)] + [N * (N + 1) + i for i in range(N - 1, -1, -1)] + [j * (N + 1) for j in range(N - 1, 0, -1)]
    back = len(verts)
    verts.extend((verts[k][0], 0, verts[k][2]) for k in ring)
    for i, k in enumerate(ring):
        nxt = (i + 1) % len(ring)
        faces.append((k, ring[nxt], back + nxt, back + i))
    faces.append(tuple(back + i for i in range(len(ring))))
    mesh = bpy.data.meshes.new('Original hand-shaped ceramic closed tile mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.materials.append(glaze())
    mesh.update()
    ob = bpy.data.objects.new('98 mm handmade-look ceramic tile', mesh)
    c.objects.link(ob)
    bevel = ob.modifiers.new('Soft ceramic edge 0.5 mm', 'BEVEL')
    bevel.width = .0005
    bevel.segments = 3
    bevel.limit_method = 'ANGLE'
    ob.modifiers.new('Weighted normals', 'WEIGHTED_NORMAL')
    for face in mesh.polygons:
        if len(face.vertices) == 4:
            face.use_smooth = True


def publish(slug):
    out = folder(slug)
    native = out / (slug + '.blend')
    if native.exists():
        print('IMMUTABLE_EXISTING', slug, flush=True)
        return
    bpy.ops.wm.read_factory_settings(use_empty=True)
    name = NAMES[SLUGS.index(slug)]
    c = g.collection(name)
    c['asset_id'], c['asset_version'] = 'surfaces/' + slug, 'v001'
    meta = {
        'schema_version': 1, 'id': 'surfaces/' + slug, 'version': 'v001', 'name': name,
        'units': 'meters', 'blender': {'collection': name},
        'placement': {'origin': 'Centered X, rear mounting plane Y=0, bottom Z=0', 'front_direction': '+Y', 'up': 'Z', 'allowed_scaling': 'Rigid placement/rotation only. Repeat linked full modules at documented pitch; do not stretch.'},
        'source': {'kind': 'original', 'author': 'Homes project contributors', 'generator': GEN, 'command': 'Blender -b --factory-startup --python ' + GEN, 'software': bpy.app.version_string},
        'license': 'CC-BY-4.0', 'rights': 'Original Homes project contributor geometry and procedural appearance. Attribution: Homes project contributors. No third-party downloads.',
        'dependencies': [],
        'installation': {
            'mounting': 'Host provides stable continuous substrate, product-selected bonding/support, and substrate waterproofing behind Y=0. Adhesive thickness is not represented.',
            'joints': 'Leave perimeter and changes of plane as correctly specified flexible joints; do not fill movement joints with hard grout. Bottom datum is finish edge: host leaves a coordinated countertop junction below it.',
            'wet_limitations': 'Visual concept only. Neither geometry nor glaze establishes water absorption, stain resistance, waterproofing or cleaning compatibility. Verify selected material, grout, sealants and backing before wet use.',
            'heat_limitations': 'No flame, temperature or combustible-clearance rating. Range/cooktop instructions and the actual finish/bonding system govern all heat clearances; do not infer approval from ceramic or stone appearance.',
            'required_host_checks': ['Countertop and end junctions', 'Outlets and fixture penetrations with correctly detailed edge cuts', 'Substrate capacity, adhesion, movement and waterproofing', 'Actual appliance heat clearances and finish suitability'],
            'host_installation_checked': False,
            'operating_envelope': {'state': 'Fixed finish module', 'moving_parts': False}},
        'variation': {'cuts': 'Project-specific boundary and outlet cuts may trim a copy of the mesh, retaining material scale and finish thickness; document cuts. Full modules stay linked. Exposed cuts need the host-selected finished edge or trim.'},
        'files': {'blender': native.name, 'preview': 'preview.png', 'validation': 'validation.json'},
        'limitations': 'Editable architectural visualization asset; not a commercial product, tested assembly, construction detail or code approval. Available library option; no new home adoption is claimed.'}
    if slug == SLUGS[0]:
        dep = dependency('cream-veined-stone')
        with bpy.data.libraries.load(str((out / dep['path']).resolve()), link=True) as (_, dst):
            dst.materials = ['Cream veined stone | v001']
        box('20 mm cream stone slab with eased exposed edges', (0, .01, .3048), (1.2192, .020, .6096), dst.materials[0], .001)
        meta['dependencies'] = [dep]
        meta['module'] = {'width_m': 1.2192, 'height_m': .6096, 'depth_m': .020, 'edge_bevel_m': .001, 'suggested_joint_m': .003, 'pitch_m': [1.2222, .6126], 'joint_basis': 'Concept 3 mm field joint; actual slab, sealant and movement specification unresolved.'}
        meta['installation']['mounting'] += ' Full 20 mm stone thickness requires verified weight support; no brackets, anchors or engineered backing are modeled.'
        meta['reuse'] = 'New physical slab geometry; exact existing cream-veined-stone/v001 linked unchanged. Stone species and commercial slab size availability are not specified.'
    elif slug == SLUGS[1]:
        handmade_tile(c)
        meta['module'] = {'width_m': .098, 'height_m': .098, 'nominal_pitch_m': [.1016, .1016], 'minimum_joint_m': .0036, 'approx_depth_m': .00935, 'edge_bevel_m': .0005, 'joint_basis': '3.6 mm minimum between bounding square tile envelopes; gently irregular edges locally widen the joint.'}
        meta['material'] = {'type': 'Original procedural warm ivory ceramic glaze embedded with tile', 'roughness': .24, 'coat_weight': .25, 'texture_scale': 'Procedural microtexture at 620 per meter, 0.08 mm bump distance; actual front mesh relief up to 0.55 mm. Object-instance random creates restrained glaze-tone variation.'}
        meta['preview_content'] = 'Preview contains an 8-column x 6-row demonstration of linked tile modules with recessed warm-gray grout. Native collection contains only ONE tile; demo grout is not part of module. Hosts provide grout and backing.'
    else:
        dep = dependency('sage-fluted-tile')
        with bpy.data.libraries.load(str((out / dep['path']).resolve()), link=True) as (_, dst):
            dst.collections = ['Sage fluted tile | 3 x 12 in | v001']
        tile = dst.collections[0]
        grout = g.material('Original warm gray sage tile grout | backsplash v001', (.41, .42, .36), .90)
        box('Physical recessed grout bed and joints', (0, .0035, .3048), (.3048, .007, .6096), grout)
        for row in range(2):
            for col in range(4):
                instance(c, tile, f'Linked sage tile column {col + 1} row {row + 1}', (-.1143 + col * .0762, .008858, .1524 + row * .3048))
        meta['dependencies'] = [dep]
        meta['module'] = {'width_m': .3048, 'height_m': .6096, 'tile_pitch_m': [.0762, .3048], 'array_columns_rows': [4, 2], 'tile_body_m': [.073152, .301752], 'joint_m': .003048, 'array_repeat_pitch_m': [.3048, .6096], 'seam_rule': 'Module includes half a grout joint at each outer edge; adjoining modules butt at pitch to preserve 3.048 mm tile-to-tile joint. Do not add an extra field gap between array modules.', 'grout_front_y_m': .007}
        meta['derived_from'] = {'id': 'materials/sage-fluted-tile', 'version': 'v001', 'basis': 'Eight linked instances of the actual source tile collection, unchanged geometry/glaze; original new recessed grout assembly and mounting datum.'}
        meta['preview_content'] = 'Native collection is a repeatable four-column x two-row vertical stacked field (8 actual linked source tiles). Preview shows that one field; source tile material and flute geometry remain linked.'
    bpy.context.view_layer.update()
    lo, hi = bounds(c)
    meta['dimensions_m'] = [hi[i] - lo[i] for i in range(3)]
    meta['bounds_m'] = {'min': lo, 'max': hi}
    out.mkdir(parents=True, exist_ok=True)
    bpy.data.libraries.write(str(native), {c}, fake_user=True, path_remap='RELATIVE_ALL')
    write_json(out / 'asset.json', meta)
    (out / 'README.md').write_text('# ' + name + '\n\n![Actual native preview](preview.png)\n\nOriginal reusable architectural concept, CC BY 4.0 with attribution to Homes project contributors. This is an available library option; host installation is unverified.\n\n' + meta.get('preview_content', meta.get('reuse', '')) + '\n\nThe [manifest](asset.json) records meter dimensions, +Y front, rear mounting plane Y=0, bottom Z=0, joints, dependencies, cut rules and unresolved wet/heat interfaces. Link the explicitly named collection at scale 1. Do not stretch modules or infer tested performance from the preview.\n\nNative source: [' + native.name + '](' + native.name + '). Generator: [`' + GEN + '`](../../../../' + GEN + '). Rebuild only absent versions; never overwrite an adopted version.\n\nRun the generator in Blender to publish; add `-- --verify --render` in a separate fresh process for native reopening, relative-link verification and CPU preview. See [validation](validation.json) for the actual verification and visual inspection status.\n')
    print('PUBLISHED', slug, meta['dimensions_m'], flush=True)


def verify(slug, render):
    out = folder(slug)
    native = out / (slug + '.blend')
    meta = json.loads((out / 'asset.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(native))
    assert all(lib.filepath.startswith('//') for lib in bpy.data.libraries), 'non-relative saved library'
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(str(native), link=True) as (_, dst):
        dst.collections = [meta['blender']['collection']]
    c = dst.collections[0]
    bpy.context.scene.collection.children.link(c)
    bpy.context.view_layer.update()
    lo, hi = bounds(c)
    assert all(abs(hi[i] - lo[i] - meta['dimensions_m'][i]) < 1e-6 for i in range(3))
    assert abs(lo[1]) < 1e-5 and abs(lo[2]) < 1e-5
    assert all(Path(bpy.path.abspath(lib.filepath, library=lib.parent)).exists() for lib in bpy.data.libraries)
    assert not [im for im in bpy.data.images if im.source == 'FILE' and not im.packed_file and not Path(bpy.path.abspath(im.filepath, library=im.library)).exists()]
    if slug == SLUGS[1]:
        tile = next(ob for ob in c.objects if ob.type == 'MESH')
        bm = bmesh.new()
        bm.from_mesh(tile.data)
        assert all(edge.is_manifold for edge in bm.edges), 'Ceramic tile must be a closed mesh'
        assert bm.calc_volume(signed=True) > 0, 'Ceramic normals must face outward'
        bm.free()
    if slug == SLUGS[2]:
        assert len([ob for ob in c.objects if ob.instance_type == 'COLLECTION']) == 8
    if render:
        studio = g.collection('Preview studio - never install')
        width, height = hi[0] - lo[0], hi[2] - lo[2]
        if slug == SLUGS[1]:
            bpy.context.scene.collection.children.unlink(c)
            width, height = 8 * .1016, 6 * .1016
            for row in range(6):
                for col in range(8):
                    instance(studio, c, f'Preview linked ivory tile {row}-{col}', ((col - 3.5) * .1016, 0, row * .1016))
            grout = g.material('Preview only recessed warm ivory grout', (.50, .47, .40), .92)
            box('Preview only grout field', (0, -.0005, height / 2 - .0018), (width, .010, height), grout)
        neutral = g.material('Preview neutral background', (.21, .23, .23), .85)
        box('Studio ground', (0, 0, -.015), (200, 200, .02), neutral)
        scene = bpy.context.scene
        cam_xyz = Vector((width * 1.25, max(width, height) * 2.8, height * 1.30))
        target = Vector((0, .006, height * .5))
        scene.camera = g.camera('Actual native module camera', cam_xyz / g.F, target / g.F, 55)
        scene.camera.data.type = 'ORTHO'
        scene.camera.data.ortho_scale = max(width * 1.42, height * 1.64)
        key = g.area('Neutral broad softbox', Vector((-1.3, 1.6, 2.2)) / g.F, target / g.F, 150, 1.6 / g.F, (1, .98, .94))
        rim = g.area('Grazing edge light', Vector((1.5, .9, .8)) / g.F, target / g.F, 65, .9 / g.F, (.94, .97, 1))
        key.visible_glossy = rim.visible_glossy = True
        scene.world = bpy.data.worlds.new('Neutral preview world')
        scene.world.use_nodes = True
        scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .3
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 32
        scene.cycles.use_denoising = True
        scene.render.threads_mode, scene.render.threads = 'FIXED', 4
        scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 960, 720, 100
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = str(out / 'preview.png')
        scene.view_settings.view_transform = 'AgX'
        scene.view_settings.exposure = 0
        bpy.ops.render.render(write_still=True)
    write_json(out / 'validation.json', {'fresh_native_open': True, 'fresh_link': True, 'relative_dependencies_resolve': True, 'missing_textures': [], 'dimensions_m': [hi[i] - lo[i] for i in range(3)], 'bounds_m': {'min': lo, 'max': hi}, 'origin_front_check': 'Rear Y=0, bottom Z=0 verified; front +Y', 'preview_rendered': (out / 'preview.png').exists(), 'preview_settings': {'renderer': 'Cycles CPU', 'threads': 4, 'samples': 32, 'color_management': 'AgX', 'exposure': 0}, 'visual_inspection': 'Pending actual image inspection', 'tile_closed_outward_mesh_checked': slug == SLUGS[1], 'eight_linked_sage_tiles_checked': slug == SLUGS[2], 'host_installation_checked': False, 'software': bpy.app.version_string})
    print('VERIFIED', slug, flush=True)


def installation_preview(slug):
    """Actual linked finish in an illustrative wall/counter interface specimen."""
    out = folder(slug)
    meta = json.loads((out / 'asset.json').read_text())
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(str(out / (slug + '.blend')), link=True) as (_, dst):
        dst.collections = [meta['blender']['collection']]
    c = dst.collections[0]
    studio = g.collection('Installation demonstration - not a native library assembly')
    grout = g.material('Studio specimen recessed grout', (.44, .42, .36), .90)
    flexible = g.material('Studio specimen warm-gray flexible sealant', (.28, .27, .23), .65)
    wall = g.material('Studio specimen backing wall', (.63, .62, .57), .93)
    counter = g.material('Studio specimen neutral countertop', (.66, .64, .58), .30)
    cabinet = g.material('Studio specimen warm charcoal cabinetry', (.16, .18, .17), .65)
    if slug == SLUGS[0]:
        width, height, front = 2 * 1.2192 + .003, .6096, .020
        for sign in [-1, 1]:
            instance(studio, c, 'Linked stone panel left' if sign < 0 else 'Linked stone panel right', (sign * (.6096 + .0015), 0, 0))
        box('Actual 3 mm vertical flexible panel joint', (0, .010, height / 2), (.003, .019, height), flexible)
        end_note = 'Actual 20 mm slab thickness and 1 mm eased outer edge remain exposed; two full source panels have a separate 3 mm flexible vertical joint.'
    elif slug == SLUGS[1]:
        width, height, front = 7 * .1016 + .098, 5 * .1016 + .098, .00935
        for row in range(6):
            for col in range(8):
                instance(studio, c, f'Installed linked ivory tile {row}-{col}', ((col - 3.5) * .1016, 0, row * .1016))
        box('Studio grout recessed behind individual ceramic tile faces', (0, -.0005, height / 2), (width, .010, height), grout)
        end_note = 'Illustrative 1 mm thick metal L-profile caps exposed side edges; 98 mm tiles retain their real 3.6 mm minimum field joints.'
    else:
        width, height, front = .6096, .6096, .0201356
        for sign in [-1, 1]:
            instance(studio, c, 'Linked sage field left' if sign < 0 else 'Linked sage field right', (sign * .1524, 0, 0))
        end_note = 'Two linked sage arrays meet at documented 304.8 mm pitch without an extra panel gap; an illustrative 1 mm thick metal L-profile caps exposed side edges.'
    if slug != SLUGS[0]:
        trim = g.material('Studio specimen brushed bronze termination trim', (.26, .23, .18), .35, .7)
        for sign in [-1, 1]:
            x = sign * (width / 2 + .0005)
            box('Studio side termination trim web', (x, front / 2, height / 2), (.001, front + .001, height), trim)
            box('Studio side termination trim face lip', (sign * (width / 2 - .001), front + .0005, height / 2), (.003, .001, height), trim)
    # Counter top is exactly 3 mm below the finish bottom. A separate physical
    # sealant strip fills this joint; no finish geometry penetrates the counter.
    seal = box('Actual 3 mm horizontal flexible counter junction', (0, front - .002, -.0015), (width, .006, .003), flexible)
    box('Studio continuous substrate wall', (0, -.025, .31), (width + .18, .045, .78), wall)
    countertop = box('Studio countertop with top at Z minus 3 mm', (0, .29, -.019), (width + .20, .64, .032), counter, .001)
    box('Studio cabinet below countertop', (0, .26, -.22), (width + .12, .56, .37), cabinet, .002)
    scene = bpy.context.scene
    target = Vector((0, .06, .25))
    scene.camera = g.camera('Counter transition and end detail camera', Vector((width * .9, max(width, 1) * 2.25, 1.25)) / g.F, target / g.F, 58)
    scene.camera.data.type = 'ORTHO'
    scene.camera.data.ortho_scale = max(width * 1.30, 1.80)
    key = g.area('Broad installation softbox', Vector((-1.1, 1.6, 2.0)) / g.F, target / g.F, 200, 1.5 / g.F, (1, .98, .94))
    key.visible_glossy = True
    g.area('Installation edge light', Vector((2, 1, 1.5)) / g.F, target / g.F, 90, 1 / g.F, (.94, .97, 1))
    scene.world = bpy.data.worlds.new('Neutral installation study world')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .35
    scene.render.engine, scene.cycles.device = 'CYCLES', 'CPU'
    scene.cycles.samples, scene.cycles.use_denoising = 32, True
    scene.render.threads_mode, scene.render.threads = 'FIXED', 4
    scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 1400, 1000, 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = str(out / 'installation-preview.png')
    scene.view_settings.view_transform, scene.view_settings.exposure = 'AgX', 0
    bpy.context.view_layer.update()
    counter_top = max((countertop.matrix_world @ Vector(p)).z for p in countertop.bound_box)
    seal_bottom = min((seal.matrix_world @ Vector(p)).z for p in seal.bound_box)
    seal_top = max((seal.matrix_world @ Vector(p)).z for p in seal.bound_box)
    assert abs(counter_top + .003) < 1e-6
    assert abs(seal_bottom - counter_top) < 1e-6 and abs(seal_top) < 1e-6
    assert all(Path(bpy.path.abspath(lib.filepath, library=lib.parent)).exists() for lib in bpy.data.libraries)
    for ob in studio.objects:
        if ob.instance_type == 'COLLECTION':
            lo, hi = bounds(ob.instance_collection)
            assert lo[2] + ob.location.z >= -1e-5
    bpy.ops.render.render(write_still=True)
    info = {'kind': 'Illustrative studio installation specimen using actual linked native finish', 'countertop_top_z_m': -.003, 'finish_bottom_datum_z_m': 0, 'flexible_counter_joint_m': .003, 'counter_joint_fill': 'Separate physical 3 mm high concept sealant strip; adhesion, movement capacity and commercial sealant unresolved', 'vertical_slab_joint_m': .003 if slug == SLUGS[0] else None, 'termination': end_note, 'counter_and_sealant_bounds_verified': True, 'native_geometry_modified': False, 'real_home_installation_checked': False, 'product_or_code_approval': False, 'visual_inspection': 'Pending actual image inspection', 'render_settings': {'engine': 'Cycles CPU', 'threads': 4, 'samples': 32, 'color_management': 'AgX', 'exposure': 0}}
    meta['files']['installation_preview'] = 'installation-preview.png'
    meta['installation_preview'] = info
    write_json(out / 'asset.json', meta)
    validation = json.loads((out / 'validation.json').read_text())
    validation['installation_preview'] = info
    write_json(out / 'validation.json', validation)
    readme = out / 'README.md'
    text = readme.read_text().split('\n## Studio installation specimen')[0]
    readme.write_text(text + '\n## Studio installation specimen\n\n![Actual linked finish above a countertop](installation-preview.png)\n\nThis separate CPU render installs the actual linked native finish on an illustrative backing wall above a neutral countertop. The countertop top is 3 mm below the finish bottom; a modeled flexible sealant strip fills that junction. ' + end_note + '\n\nThis checks the shown studio interface only. It does not approve a real home, proprietary trim, waterproofing, bonding system, movement capacity, appliance clearance or selected commercial product. Studio wall, counter, sealant and edge trim are demonstration geometry and are not embedded in the reusable native finish collection.\n\nReproduce with the generator command plus `-- --installation-preview`.\n')
    print('INSTALLATION_PREVIEW', slug, flush=True)


if __name__ == '__main__':
    selected = [sys.argv[sys.argv.index('--asset') + 1]] if '--asset' in sys.argv else SLUGS
    for slug in selected:
        assert slug in SLUGS
        if '--installation-preview' in sys.argv:
            installation_preview(slug)
        elif '--verify' in sys.argv:
            verify(slug, '--render' in sys.argv)
        else:
            publish(slug)
