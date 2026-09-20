"""Linked comparative nursery: original placement test, not a proposed garden.

Build: blender -b --factory-startup -t 2 --python tools/library/plants/nursery.py
Fresh verify: blender -b --factory-startup -t 2 --python tools/library/plants/nursery.py -- --verify
Render: blender -b --factory-startup -t 4 --python tools/library/plants/nursery.py -- --render
The build never changes source plant assets and deliberately renders nothing.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / 'library/landscape/nursery'
NATIVE = OUTPUT / 'nursery.blend'
GROUPS = {
    'mountain': ['quaking-aspen', 'rocky-mountain-maple', 'saskatoon-serviceberry', 'red-osier-dogwood', 'kinnikinnick'],
    'desert': ['blue-palo-verde', 'desert-willow', 'ocotillo', 'parry-agave', 'fishhook-barrel-cactus'],
    'xeric': ['blue-grama', 'little-bluestem', 'pineleaf-penstemon', 'fernbush', 'prairie-coneflower'],
    'coastal': ['shore-pine', 'coast-silktassel', 'beach-strawberry', 'sea-oats', 'yaupon-holly'],
    'suburban': ['eastern-redbud', 'panicle-hydrangea', 'ninebark', 'american-hornbeam', 'japanese-laceleaf-maple'],
    'fruit': ['lemon-tree', 'lime-tree', 'sweet-orange-tree', 'satsuma-mandarin-tree', 'grapefruit-tree', 'kumquat-tree', 'avocado-tree', 'fig-tree', 'pomegranate-tree', 'apple-tree'],
}
GAP = 1.0
PATH = 3.0


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def material(name, color, roughness=.75):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    shader = m.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color, 1)
    shader.inputs['Roughness'].default_value = roughness
    return m


def box(name, center, dimensions, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    o = bpy.context.object
    o.name = name
    o.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    return o


def label(text, pos, size, mat):
    curve = bpy.data.curves.new('Nursery lettering', 'FONT')
    curve.body = text
    curve.align_x = 'CENTER'
    curve.align_y = 'CENTER'
    curve.size = size
    obj = bpy.data.objects.new(text, curve)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = pos
    obj.data.materials.append(mat)
    return obj


def camera(name, lower, upper):
    lo, hi = Vector(lower), Vector(upper)
    center = (lo+hi)*.5
    diagonal = max((hi-lo).length, 4)
    data = bpy.data.cameras.new(name)
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = center + Vector((.12, -1.2, .95))*diagonal
    obj.rotation_euler = (center-obj.location).to_track_quat('-Z', 'Y').to_euler()
    data.type = 'ORTHO'
    data.clip_end = 1000
    inverse = obj.rotation_euler.to_quaternion().inverted()
    projected = [inverse @ (Vector((x,y,z))-center) for x in [lo.x,hi.x] for y in [lo.y,hi.y] for z in [lo.z,hi.z]]
    wide = max(p.x for p in projected)-min(p.x for p in projected)
    high = max(p.y for p in projected)-min(p.y for p in projected)
    data.ortho_scale = max(wide, high*1.6)*1.12
    return obj


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = 2400, 1500
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 2
    scene.view_settings.view_transform = 'AgX'
    scene.world = bpy.data.worlds.new('Daylight')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.75,.85,1,1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value = .55
    bpy.ops.object.light_add(type='SUN', location=(0,0,30))
    sun = bpy.context.object
    sun.name = 'Nursery daylight'
    sun.rotation_euler = (math.radians(28), math.radians(-20), math.radians(-25))
    sun.data.energy = 2.1
    sun.data.angle = .12
    soil = material('Demonstration soil', (.11,.085,.055))
    path = material('Demonstration pale gravel', (.43,.42,.37))
    stone = material('Demonstration edging', (.30,.31,.28))
    ink = material('Nursery charcoal lettering', (.018,.025,.023))
    layouts = []
    for group, slugs in GROUPS.items():
        columns = 3 if group != 'fruit' else 4
        entries = []
        for slug in slugs:
            folder = ROOT/'library/landscape'/slug/'v001'
            meta = json.loads((folder/'asset.json').read_text())
            variant = meta['blender']['variants'][1]
            entries.append({'slug': slug, 'folder': folder, 'meta': meta, 'variant': variant})
        rows = math.ceil(len(entries)/columns)
        widths = [max((e['variant']['dimensions_m'][0] for i,e in enumerate(entries) if i%columns==col), default=0) for col in range(columns)]
        depths = [max(e['variant']['dimensions_m'][1] for e in entries[row*columns:(row+1)*columns]) for row in range(rows)]
        width, depth = sum(widths)+GAP*(columns+1), sum(depths)+GAP*(rows+1)
        layouts.append({'name': group, 'entries': entries, 'columns': columns, 'widths': widths, 'depths': depths, 'width': width, 'depth': depth})
    block_width = max(g['width'] for g in layouts)+PATH*2
    block_depth = max(g['depth'] for g in layouts)+PATH*2
    records = []
    group_records = []
    for gidx, layout in enumerate(layouts):
        group = layout['name']
        ox, oy = (gidx%2)*block_width, (gidx//2)*block_depth
        width, depth = layout['width'], layout['depth']
        box(group+' soil bed', (ox+width/2,oy+depth/2,-.12), (width,depth,.24), soil)
        for loc, dim in [((ox-.10,oy+depth/2,-.04),(.15,depth+.30,.18)), ((ox+width+.10,oy+depth/2,-.04),(.15,depth+.30,.18)), ((ox+width/2,oy-.10,-.04),(width+.35,.15,.18)), ((ox+width/2,oy+depth+.10,-.04),(width+.35,.15,.18))]:
            box(group+' bed edging', loc, dim, stone)
        label(group.upper()+'  /  COMPARATIVE PLANTING', (ox+width/2,oy-1.35,-.035), min(.42,width/44), ink)
        height = 0
        for i, entry in enumerate(layout['entries']):
            row, col = divmod(i,layout['columns'])
            variant = entry['variant']
            local_x = GAP*(col+1)+sum(layout['widths'][:col])
            local_y = GAP*(row+1)+sum(layout['depths'][:row])
            # Each measured canopy begins within its own cell; origins retain grade Z=0.
            x = ox+local_x-variant['bounds_m']['min'][0]
            y = oy+local_y-variant['bounds_m']['min'][1]
            # Keep the same bed/cell envelopes, but place the two tall canopy
            # specimens behind their lower companions for a readable comparison.
            # Using each specimen's own depth avoids enlarging the bed merely
            # because the solitary third-column specimen is deeper than a shrub.
            if group in {'mountain','desert','coastal'}:
                if i < 2:
                    y = oy+depth-GAP-variant['bounds_m']['max'][1]
                elif i >= 3:
                    y = oy+GAP-variant['bounds_m']['min'][1]
            native = entry['folder']/entry['meta']['files']['blender']
            with bpy.data.libraries.load(str(native),link=True,relative=False) as (available, loaded):
                assert variant['collection'] in available.collections
                loaded.collections = [variant['collection']]
            obj = bpy.data.objects.new('Plant | '+entry['slug'],None)
            obj.instance_type = 'COLLECTION'
            obj.instance_collection = loaded.collections[0]
            obj.location = (x,y,0)
            obj['family'] = entry['slug']
            obj['variant'] = variant['id']
            obj['bed'] = group
            scene.collection.objects.link(obj)
            bbox = {'min':[variant['bounds_m']['min'][0]+x,variant['bounds_m']['min'][1]+y,variant['bounds_m']['min'][2]], 'max':[variant['bounds_m']['max'][0]+x,variant['bounds_m']['max'][1]+y,variant['bounds_m']['max'][2]]}
            height = max(height,bbox['max'][2])
            records.append({'family': entry['slug'], 'group':group, 'variant':variant['id'], 'collection':variant['collection'], 'object':obj.name, 'location_m':[x,y,0], 'bounds_m':bbox, 'source':str(native.relative_to(ROOT)), 'source_sha256':digest(native)})
        cam = camera('Nursery_'+group, (ox-.5,oy-2,-.1), (ox+width+.5,oy+depth+.5,height))
        group_records.append({'group':group,'bed_bounds_xy':[ox,oy,ox+width,oy+depth],'camera':cam.name})
    total_w, total_d = block_width*2-PATH, block_depth*3-PATH
    box('Continuous clear gravel paths',(total_w/2-1,total_d/2-1,-.18),(total_w+5,total_d+5,.24),path)
    scene.camera = camera('Nursery_overview', (-2,-2,0),(total_w,total_d,max(r['bounds_m']['max'][2] for r in records)))
    scene['nursery_records'] = json.dumps(records)
    scene['nursery_groups'] = json.dumps(group_records)
    scene['purpose'] = 'Comparative linked-asset placement test. Climate groups are separate demonstrations, not a combined proposed garden.'
    OUTPUT.mkdir(parents=True,exist_ok=True)
    scene.render.filepath = '//overview.png'
    bpy.ops.wm.save_as_mainfile(filepath=str(NATIVE),compress=True)
    # Resolve links against the saved scene, then make all libraries portable.
    for lib in bpy.data.libraries:
        absolute = bpy.path.abspath(lib.filepath)
        lib.filepath = bpy.path.relpath(absolute,start=str(OUTPUT))
    bpy.ops.wm.save_as_mainfile(filepath=str(NATIVE),compress=True)
    readme = ['# Comparative plant nursery','',
              'A linked Blender placement demonstration of all 35 new plant families, separated into six labeled beds. These climate tags are browse groups: this is not a proposed garden that combines incompatible growing conditions.','',
              'The native scene links one representative variant per family. Every family file also contains its other two variants. Plant origins remain at planting grade Z=0; spacing uses measured canopy bounds with at least one meter between adjacent planting cells. Gravel paths stay outside the beds.','',
              'This demonstrates linked placement and portability. It does not adopt these assets into any existing home or establish horticultural suitability, root-zone sizing, irrigation or mature spacing.','',
              '## Cameras','',
              '| Bed | Native camera |','|---|---|']
    readme.extend(f"| {r['group'].title()} | `{r['camera']}` |" for r in group_records)
    readme.extend(['| Whole nursery | `Nursery_overview` |','',
                  'Scene: [nursery.blend](nursery.blend). Fresh-process geometry and relative-link checks: [validation.json](validation.json). Native images are generated separately after reopening this scene.','',
                  'Source: [nursery.py](../../../tools/library/plants/nursery.py). Run its `--verify` mode in a separate Blender process after building.','',
                  'All geometry/materials are original. Plant assets: CC BY 4.0, attribution Homes project contributors. Authoring code: MIT.',''])
    readme_path=OUTPUT/'README.md'
    previous=readme_path.read_text() if readme_path.exists() else ''
    retained_gallery=''
    if '## Native placement gallery' in previous:
        retained_gallery='\n## Native placement gallery'+previous.split('## Native placement gallery',1)[1]
    readme_path.write_text('\n'.join(readme)+retained_gallery)
    print('NURSERY_BUILT',len(records),[g['camera'] for g in group_records],flush=True)


def verify():
    bpy.ops.wm.open_mainfile(filepath=str(NATIVE),use_scripts=False)
    scene = bpy.context.scene
    records = json.loads(scene['nursery_records'])
    groups = json.loads(scene['nursery_groups'])
    assert len(records)==35 and len({r['family'] for r in records})==35
    assert len(bpy.data.libraries)==35
    for library in bpy.data.libraries:
        assert library.filepath.startswith('//'),library.filepath
        assert Path(bpy.path.abspath(library.filepath)).is_file(),library.filepath
    evaluated = {}
    bpy.context.view_layer.update()
    for instance in bpy.context.evaluated_depsgraph_get().object_instances:
        if not instance.is_instance or instance.object.type!='MESH':
            continue
        owner = instance.parent.name
        info = evaluated.setdefault(owner,{'min':[float('inf')]*3,'max':[float('-inf')]*3,'meshes':0,'vertices':0})
        mesh = instance.object.data
        if not mesh.vertices:
            continue
        info['meshes'] += 1
        info['vertices'] += len(mesh.vertices)
        for corner in instance.object.bound_box:
            point = instance.matrix_world @ Vector(corner)
            for axis in range(3):
                info['min'][axis]=min(info['min'][axis],point[axis])
                info['max'][axis]=max(info['max'][axis],point[axis])
    receipt = []
    for r in records:
        obj = bpy.data.objects[r['object']]
        assert abs(obj.location.z)<1e-6
        assert obj.instance_type=='COLLECTION' and obj.instance_collection.library
        bounds = evaluated[r['object']]
        assert bounds['meshes']>0 and bounds['vertices']>0
        assert -.08<=bounds['min'][2]<=.015,(r['family'],'ground',bounds['min'][2])
        error=max(abs(bounds[k][axis]-r['bounds_m'][k][axis]) for k in ['min','max'] for axis in range(3))
        assert error<.003,(r['family'],'stale bounds',error)
        assert digest(ROOT/r['source'])==r['source_sha256'],(r['family'],'source changed; rebuild nursery')
        bed=next(g for g in groups if g['group']==r['group'])['bed_bounds_xy']
        assert bounds['min'][0]>=bed[0]+.25 and bounds['min'][1]>=bed[1]+.25
        assert bounds['max'][0]<=bed[2]-.25 and bounds['max'][1]<=bed[3]-.25
        receipt.append({**r,'evaluated':bounds,'maximum_bounds_error_m':error})
    minimum_gap=float('inf')
    for i, a in enumerate(receipt):
        for b in receipt[i+1:]:
            aa,bb=a['evaluated'],b['evaluated']
            dx=max(0,aa['min'][0]-bb['max'][0],bb['min'][0]-aa['max'][0])
            dy=max(0,aa['min'][1]-bb['max'][1],bb['min'][1]-aa['max'][1])
            gap=math.hypot(dx,dy)
            assert gap>=.25,(a['family'],b['family'],gap)
            minimum_gap=min(minimum_gap,gap)
    report={'purpose':scene['purpose'],'native_reopened':True,'native_sha256':digest(NATIVE),'family_count':35,'group_count':6,'relative_library_links':35,'minimum_measured_canopy_gap_m':minimum_gap,'origin_grade_m':0,'paths_clear_of_measured_canopies':True,'groups':groups,'placements':receipt,'visual_review':'Pending separate native camera inspection','home_adoption':'None; comparative linked nursery placement demonstration only','software':{'blender':bpy.app.version_string}}
    (OUTPUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('NURSERY_VERIFIED',len(receipt),'minimum_gap_m',minimum_gap,flush=True)


def render(selected=None, samples=64):
    """Render the saved scene without changing its native source or links."""
    bpy.ops.wm.open_mainfile(filepath=str(NATIVE),use_scripts=False)
    scene=bpy.context.scene
    preferences=bpy.context.preferences.addons['cycles'].preferences
    preferences.compute_device_type='METAL'
    preferences.get_devices()
    gpu=[device for device in preferences.devices if device.type=='METAL']
    if not gpu:
        raise RuntimeError('No Metal GPU found; nursery rendering requires the coordinated GPU queue')
    for device in preferences.devices:
        device.use=device.type=='METAL'
    scene.render.engine='CYCLES'
    scene.cycles.device='GPU'
    scene.cycles.samples=samples
    scene.cycles.use_denoising=True
    scene.cycles.adaptive_threshold=.03
    scene.render.threads_mode='FIXED'
    scene.render.threads=4
    scene.render.resolution_x=2400
    scene.render.resolution_y=1500
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    names=selected or ['overview',*GROUPS]
    for name in names:
        scene.camera=bpy.data.objects['Nursery_'+name]
        scene.render.filepath=str(OUTPUT/f'{name}.png')
        bpy.ops.render.render(write_still=True)
        print('NURSERY_RENDERED',name,flush=True)
    # Only expose images that actually exist, and preserve the usage text.
    readme=OUTPUT/'README.md'
    text=readme.read_text().split('## Native placement gallery')[0].rstrip()
    available=[name for name in ['overview',*GROUPS] if (OUTPUT/f'{name}.png').is_file()]
    if available:
        text+='\n\n## Native placement gallery\n\nActual renders of the linked nursery scene. These demonstrate geometry and planting contact in separate comparative beds; they are not Image Gen interpretations.\n\n'
        for name in available:
            text+=f'### {name.title()}\n\n![{name.title()} comparative planting bed]({name}.png)\n\n'
    readme.write_text(text.rstrip()+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    modes=parser.add_mutually_exclusive_group()
    modes.add_argument('--verify',action='store_true')
    modes.add_argument('--render',action='store_true')
    parser.add_argument('--cameras',nargs='+',choices=['overview',*GROUPS])
    parser.add_argument('--samples',type=int,default=64)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if args.verify:
        verify()
    elif args.render:
        render(args.cameras,args.samples)
    else:
        build()
