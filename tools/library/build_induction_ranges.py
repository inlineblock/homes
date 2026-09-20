"""Original integrated induction ranges; all dimensions meters.

Blender --background --python tools/library/build_induction_ranges.py -- --build
Blender --background --python tools/library/build_induction_ranges.py -- --verify
Creates only missing v001 assets. Use a new version for adopted modifications.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from common import geometry as g

F = g.F
SOURCE = ROOT / 'library/appliances/built-in-oven-30in/v001/built-in-oven-30in.blend'
NAMES = {'steel': 'Original appliance brushed stainless',
         'dark': 'Original appliance graphite enamel',
         'marks': 'Original appliance etched control marks',
         'glass': 'Original appliance low-tint glass'}


def box(name, xyz, whd, mat, bevel=.0015):
    return g.box(name, [v/F for v in xyz], [v/F for v in whd], mat, bevel/F)


def rod(name, a, b, radius, mat):
    return g.rod(name, [v/F for v in a], [v/F for v in b], radius/F, mat)


def cylinder(name, xyz, radius, length, mat):
    return g.cyl(name, [v/F for v in xyz], radius/F, length/F, mat, 48)


def bounds(collection):
    bpy.context.view_layer.update()
    points = [o.matrix_world @ Vector(c) for o in collection.all_objects
              if o.type == 'MESH' for c in o.bound_box]
    lo = [min(p[i] for p in points) for i in range(3)]
    hi = [max(p[i] for p in points) for i in range(3)]
    return {'min': [round(x, 6) for x in lo], 'max': [round(x, 6) for x in hi]}, [round(hi[i]-lo[i], 6) for i in range(3)]


def publish(width_in):
    slug = f'induction-range-{width_in}in'
    folder = ROOT / 'library/appliances' / slug / 'v001'
    if (folder / 'asset.json').exists():
        print('Immutable published asset retained:', slug)
        return
    folder.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    with bpy.data.libraries.load(str(SOURCE), link=True) as (src, dst):
        assert all(v in src.materials for v in NAMES.values()), src.materials
        dst.materials = list(NAMES.values())
    M = dict(zip(NAMES, dst.materials))
    M['rubber'] = g.material('Induction range resilient black feet', (.012,.013,.014), .85)
    # Existing oven's material family lacks a ceramic top in its saved file.
    # Original local ceramic adds no external material dependencies.
    M['ceramic'] = g.material('Induction range black glass ceramic', (.009, .014, .018), .13, .22)
    asset = g.collection(f'ASSET_{slug}_v001')
    width, depth, height = width_in*.0254, .635, .9144
    front, back = -depth/2, depth/2
    # Hollow insulated appliance enclosure. No solid cube behind the window.
    for x in [-width/2+.015, width/2-.015]:
        box('Insulated stainless side casing', (x, 0, .475), (.030, depth, .86), M['steel'])
        box('Interior porcelain enamel liner side', (x*.89, .014, .48), (.014, .525, .61), M['dark'])
    box('Insulated rear wall', (0, back-.025, .478), (width-.06, .05, .86), M['steel'])
    box('Dark cavity rear liner', (0, back-.057, .48), (width-.11, .015, .61), M['dark'])
    for z in [.178, .765]:
        box('Oven cavity insulated floor or roof', (0, .004, z), (width-.06, .574, .038), M['dark'])
    box('Range recessed plinth', (0, -.004, .061), (width-.062, depth-.09, .085), M['rubber'])
    for x in [-width/2+.066, width/2-.066]:
        for y in [-.230, .238]:
            cylinder('Adjustable leveling foot', (x, y, .018), .022, .036, M['rubber'])
    box('Lower storage drawer', (0, front-.006, .118), (width-.042, .035, .104), M['steel'])
    box('Recessed drawer grip', (0, front-.026, .152), (width-.15, .010, .010), M['dark'])
    box('Upper control fascia', (0, front+.004, .831), (width-.012, .047, .11), M['steel'], .003)
    # Rear spill lip and oven exhaust: distinct from the host extraction hood.
    box('Rear low upstand', (0, back-.012, .928), (width, .024, .051), M['steel'])
    box('Oven exhaust vent recess', (0, .258, .908), (width-.10, .063, .018), M['dark'])
    for x in range(21):
        box('Rear exhaust grille slot rib', ((x-10)*(width-.14)/21, .258, .920), (.006, .053, .006), M['steel'], .001)
    box('Glass ceramic cooking surface', (0, -.034, .9034), (width-.018, .550, .022), M['ceramic'], .005)
    zones = [(-.195, -.155, .102), (-.195, .101, .086),
             (.195, -.151, .091), (.195, .102, .104)] if width_in == 30 else [
             (-.296, -.158, .097), (-.296, .100, .086),
             (.296, -.158, .097), (.296, .100, .086), (0, -.025, .112)]
    for i, (x, y, r) in enumerate(zones):
        bpy.ops.mesh.primitive_torus_add(major_segments=80, minor_segments=6,
                                      major_radius=r, minor_radius=.00065,
                                      location=(x, y, .9151))
        ring = g.move(bpy.context.object)
        ring.name = f'Etched induction zone {i+1}'
        ring.data.materials.append(M['marks'])
        for axis in range(2):
            a, b = [x, y, .915], [x, y, .915]
            a[axis] -= .012; b[axis] += .012
            rod('Zone registration cross', a, b, .0006, M['marks'])
    # One cooking control per zone plus one oven mode selector.
    knobs = len(zones)+1
    for i in range(knobs):
        x = (i-(knobs-1)/2)*(width-.15)/(knobs-1)
        o = cylinder(f'Control dial {i+1}', (x, front-.033, .834), .023, .026, M['steel'])
        o.rotation_euler.x = math.pi/2
        o = cylinder('Dark dial face', (x, front-.048, .834), .019, .004, M['dark'])
        o.rotation_euler.x = math.pi/2
        box('Dial index', (x, front-.051, .846), (.002, .0015, .009), M['marks'], .0004)
        box('Control label tick', (x, front-.021, .872), (.014, .001, .002), M['marks'], .0003)
    # Rear convection fan and rack slides visible through actual glass.
    fan = cylinder('Convection fan circular guard', (0, .248, .485), .097, .010, M['steel'])
    fan.rotation_euler.x = math.pi/2
    for angle in range(0, 360, 30):
        x, z = .078*math.cos(math.radians(angle)), .078*math.sin(math.radians(angle))
        rod('Fan radial guard', (0, .239, .485), (x, .239, .485+z), .002, M['dark'])
    inner = width/2-.067
    for z in [.28, .40, .52, .64]:
        for x in [-inner, inner]:
            rod('Oven rack support runner', (x, front+.061, z), (x, .241, z), .003, M['steel'])
    for z in [.40, .64]:
        for x in [-inner+.008, inner-.008]:
            rod('Rack side frame', (x, front+.065, z), (x, .228, z), .0035, M['steel'])
        for i in range(13):
            y = front+.066+i*.038
            rod('Oven wire rack', (-inner+.008, y, z), (inner-.008, y, z), .0026, M['steel'])
    # Bottom-hinged door has a physical pivot for operation review.
    door = bpy.data.objects.new('OVEN_DOOR_HINGE_rotate_X_90deg_to_open', None)
    asset.objects.link(door); door.location = (0, front-.025, .192)
    door['open_angle_degrees'] = 90
    bpy.context.view_layer.update()
    before = set(asset.objects)
    for x in [-width/2+.036, width/2-.036]:
        box('Oven door stainless stile', (x, front-.023, .48), (.043, .045, .580), M['steel'], .003)
    for z in [.212, .747]:
        box('Oven door stainless rail', (0, front-.023, z), (width-.032, .045, .048), M['steel'], .003)
    for x in [-width/2+.071, width/2-.071]:
        box('Door black ceramic perimeter', (x, front-.027, .479), (.027, .037, .515), M['dark'])
    for z in [.248, .710]:
        box('Door black ceramic perimeter', (0, front-.027, z), (width-.12, .037, .030), M['dark'])
    box('Transparent oven viewing glass', (0, front-.028, .479), (width-.166, .009, .440), M['glass'], .002)
    for x in [-width/2+.113, width/2-.113]:
        rod('Door handle stand-off', (x, front-.047, .703), (x, front-.101, .703), .012, M['steel'])
    rod('Rounded oven door bar pull', (-width/2+.085, front-.101, .703),
        (width/2-.085, front-.101, .703), .013, M['steel'])
    bpy.context.view_layer.update()
    for obj in set(asset.objects)-before:
        world = obj.matrix_world.copy(); obj.parent = door; obj.matrix_world = world
    bpy.context.view_layer.update()
    closed_bounds, dims = bounds(asset)
    swept = []
    for angle in range(0, 91, 5):
        door.rotation_euler.x = math.radians(angle)
        measured, _ = bounds(asset); swept.append(measured)
    swept_bounds = {k: [round((min if k == 'min' else max)(b[k][i] for b in swept), 6)
                       for i in range(3)] for k in ['min', 'max']}
    door.rotation_euler.x = 0; bpy.context.view_layer.update()
    # Presentation set is separate from the reusable asset collection.
    g.collection('PREVIEW_STUDIO_do_not_link_into_home')
    mat = g.material('Studio warm gray', (.32, .33, .32), .7)
    box('Studio floor', (0, 0, -.022), (200, 200, .04), mat, 0)
    scene.camera = g.camera('Preview camera', (1.30/F, -1.95/F, 1.60/F), (0, -.015/F, .46/F), 56)
    g.area('Large key', (1.5/F, -1.7/F, 2.6/F), (0, 0, .45/F), 450, 2/F, (1,.95,.87))
    g.area('Soft fill', (-1.7/F, -.3/F, 1.6/F), (0, 0, .45/F), 300, 1.8/F, (.83,.91,1))
    g.area('Rim', (0, 1.4/F, 2.1/F), (0, 0, .50/F), 450, 1.6/F, (1,1,1))
    scene.world = bpy.data.worlds.new('Studio world'); scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.18,.20,.23,1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value = .3
    scene.render.engine = 'CYCLES'; scene.cycles.device = 'CPU'
    scene.cycles.samples = 24; scene.cycles.use_denoising = True
    scene.render.threads_mode = 'FIXED'; scene.render.threads = 3
    scene.render.resolution_x = 720; scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = '//preview.png'
    scene.render.film_transparent = False
    scene.view_settings.view_transform = 'AgX'
    for lib in bpy.data.libraries:
        import os
        lib.filepath = '//' + os.path.relpath(bpy.path.abspath(lib.filepath), folder)
    scene['asset_collection'] = asset.name
    scene['concept_only'] = 'Original visualization, not a manufacturer specification.'
    bpy.ops.wm.save_as_mainfile(filepath=str(folder / f'{slug}.blend'))
    bpy.ops.render.render(write_still=True)
    door.rotation_euler.x = math.pi/2
    scene.camera.location = (1.38, -2.35, 1.7)
    scene.camera.rotation_euler = (Vector((0,-.12,.44))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath = str(folder/'preview-open.png')
    bpy.ops.render.render(write_still=True)
    manifest = {
        'schema_version': 1, 'id': f'appliances/{slug}', 'version': 'v001',
        'name': f'Original {width_in}-inch induction range with single oven',
        'units': 'meters', 'dimensions_m': dims, 'bounds_m': closed_bounds,
        'nominal_body_dimensions_m': [width, depth, height],
        'description': f'Generic freestanding or flush-counter slide-in concept: {len(zones)} induction zones, tactile controls, full-width single convection oven with two wire racks, glazed bottom-hinged door, lower storage drawer and rear oven vent. No branded product or performance claim.',
        'collection': asset.name,
        'placement': {'origin': 'Floor at center of nominal body footprint', 'front_direction': '-Y', 'up_axis': '+Z',
                      'mounting': 'Level supported floor; adjacent worktop at 0.9144 m nominal. Low rear upstand reaches 0.9535 m.',
                      'allowed_scaling': 'None: choose the dimensioned 30-inch or 36-inch option. Do not scale to fit.'},
        'interfaces': {'nominal_width_m': width, 'worktop_height_m': height,
                       'host_opening_concept_m': [round(width+.006,4), .6604],
                       'rear_service_gap_concept_m': .0254,
                       'power': 'Concept 240 V dedicated electric supply. Rating, circuit, disconnect and receptacle position require selected product and local design.',
                       'extraction': 'Separate compatible hood and continuous route to exterior required in host; rear grille serves appliance oven, not room extraction.',
                       'anti_tip': 'Host must coordinate listed anti-tip restraint and accessible service isolation with selected product.'},
        'operation': {'modeled_state': 'Oven closed', 'hinge_object': door.name, 'hinge_axis': 'Local +X',
                      'open_angle_degrees': 90, 'opening_basis': 'Measured concept door geometry at 5-degree increments',
                      'swept_bounds_m': swept_bounds, 'front_projection_beyond_body_open_m': round(-swept_bounds['min'][1]+front,6),
                      'person_space_additional_concept_m': .6,
                      'host_open_state_checked': False,
                      'storage_drawer': 'Closed fixed mesh; allow additional 0.40 m front travel, unvalidated concept assumption.',
                      'clearance_warning': 'Envelope is geometry only; selected-product heat, combustible, service and user circulation clearances remain unverified.'},
        'dependencies': [{'id':'appliances/built-in-oven-30in','version':'v001',
                          'file':'library/appliances/built-in-oven-30in/v001/built-in-oven-30in.blend',
                          'use':'Pinned linked metal, enamel, marking and glass materials', 'datablocks':list(NAMES.values())}],
        'source': {'kind':'original','generator':'tools/library/build_induction_ranges.py',
                   'command':'Blender --background --python tools/library/build_induction_ranges.py -- --build',
                   'dimension_basis':'Original representative 30/36-inch range envelope; no manufacturer source used.'},
        'license':'CC-BY-4.0','rights':'Original project geometry; attribution: Homes project contributors. Generator MIT.',
        'files': {'blender':f'{slug}.blend','preview':'preview.png','open_preview':'preview-open.png','validation':'validation.json'},
        'software': {'blender':bpy.app.version_string},
        'review': {'fresh_reopen':'pending separate --verify invocation','visual':'pending agent inspection','host_adoption':'Not yet adopted'}
    }
    (folder/'asset.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (folder/'README.md').write_text(f'# {manifest["name"]}\n\n![Closed native preview](preview.png)\n\n![Door open native preview](preview-open.png)\n\nLink only `{asset.name}` from `{slug}.blend`. Origin is the body footprint center on the floor; front is -Y. Exact measured bounds and the opening envelope are in [asset.json](asset.json). Rotate the named oven-door hinge +90 degrees about local X to inspect opening. Never scale an appliance to fit.\n\nThis original concept has a real hollow oven, two racks, a glass viewing pane, rear convection guard, induction-zone markings, metal controls and pull, oven ventilation and leveling feet. It is not a selected commercial appliance or a certified installation. Host design must coordinate an actual opening, anti-tip restraint, separate hood/exhaust, power, service access and safe circulation around the open door.\n\nMaterial datablocks link to the existing built-in oven v001; geometry is original and this new size/type coexists with the separate cooktop and built-in oven. CC BY 4.0, Homes project contributors.\n')


def verify(width_in):
    slug = f'induction-range-{width_in}in'
    folder = ROOT/'library/appliances'/slug/'v001'
    metadata = json.loads((folder/'asset.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(folder/f'{slug}.blend'))
    asset = bpy.data.collections[metadata['collection']]
    actual, dims = bounds(asset)
    assert actual == metadata['bounds_m'], (actual,metadata['bounds_m'])
    assert dims == metadata['dimensions_m']
    assert all(o.scale == Vector((1,1,1)) for o in asset.all_objects if o.type=='MESH')
    libraries = []
    for lib in bpy.data.libraries:
        assert lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).exists()
        libraries.append(lib.filepath)
    assert len(libraries)==1
    door = bpy.data.objects[metadata['operation']['hinge_object']]
    door.rotation_euler.x = math.pi/2
    opened,_ = bounds(asset)
    assert opened['min'][1] < -.85 and opened['min'][2] >= -.001, opened
    receipt = {'status':'passed','software':bpy.app.version_string,'checks':[
        'Fresh Blender native reopening','Measured closed bounds match manifest','Mesh scale unity',
        'Pinned relative material dependency exists','90-degree door opens forward above floor'],
        'closed_bounds_m':actual,'dimensions_m':dims,'open_bounds_m':opened,
        'relative_libraries':libraries,'asset_mesh_count':sum(o.type=='MESH' for o in asset.all_objects),
        'host_integration_checked':False,'visual_review':'pending'}
    (folder/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
    metadata['review']['fresh_reopen']='passed; see validation.json'
    (folder/'asset.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print('VERIFIED', slug, dims)


if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('--build',action='store_true'); p.add_argument('--verify',action='store_true')
    p.add_argument('--width',type=int,choices=[30,36])
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    for size in ([args.width] if args.width else [30,36]):
        if args.build: publish(size)
        if args.verify: verify(size)
