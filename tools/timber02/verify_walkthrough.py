"""Fresh-process verification for the separate presentation walkthrough scene.

blender --factory-startup -b --python-exit-code 1 --python tools/timber02/verify_walkthrough.py
"""
import hashlib
import json
from pathlib import Path

import bpy
from mathutils import Vector

def route_clearance(scene, record):
    """Conservative body sweep against evaluated fixed-mesh world bounds.

    A clear expanded AABB establishes clearance; an overlap is only a candidate
    conflict and must be investigated against actual geometry. It is not a code,
    accessibility, door-mechanism or landscape-maintenance certification.
    """
    deps = bpy.context.evaluated_depsgraph_get()
    meshes = []
    skipped_landscape = 0
    def expand(obj, parent=None):
        world = obj.matrix_world if parent is None else parent @ obj.matrix_local
        if obj.hide_render:
            return
        if obj.type in {'MESH', 'CURVE'}:
            evaluated = obj.evaluated_get(deps)
            mesh = evaluated.to_mesh()
            if mesh and mesh.vertices:
                points = [world @ v.co for v in mesh.vertices]
                low = [min(p[i] for p in points) for i in range(3)]
                high = [max(p[i] for p in points) for i in range(3)]
                if high[2] > .05 and low[2] < 1.80:
                    meshes.append((obj.name, low, high))
            evaluated.to_mesh_clear()
        if obj.instance_type == 'COLLECTION' and obj.instance_collection:
            for child in obj.instance_collection.objects:
                expand(child, world)
    for obj in scene.objects:
        if obj.library is not None:
            continue
        if any(c.name.startswith('06 Landscape') for c in obj.users_collection):
            skipped_landscape += 1
            continue
        expand(obj)
    conflicts = []
    nearest = None
    poses = record['poses']
    for index, pose in enumerate(poses):
        a = pose['position_m']; b = poses[min(index + 1, len(poses) - 1)]['position_m']
        low = [min(a[0], b[0]) - .35, min(a[1], b[1]) - .35, .05]
        high = [max(a[0], b[0]) + .35, max(a[1], b[1]) + .35, 1.80]
        for name, mesh_low, mesh_high in meshes:
            if all(min(high[i], mesh_high[i]) - max(low[i], mesh_low[i]) > .00001 for i in range(3)):
                conflicts.append({'frame': pose['frame'], 'next_frame': poses[min(index + 1, len(poses) - 1)]['frame'], 'object': name, 'mesh_bounds_m': [mesh_low, mesh_high]})
            else:
                dx = max(mesh_low[0] - high[0], low[0] - mesh_high[0], 0)
                dy = max(mesh_low[1] - high[1], low[1] - mesh_high[1], 0)
                gap = (dx * dx + dy * dy) ** .5
                if nearest is None or gap < nearest['gap_m']:
                    nearest = {'frame': pose['frame'], 'object': name, 'gap_m': gap}
    return {'passed': not conflicts, 'body_width_m': .700, 'body_height_m': 1.80,
            'eye_height_m': record['eye_height_m'], 'lower_check_height_m': .05,
            'sampled_poses': len(poses), 'continuous_segments': len(poses) - 1,
            'evaluated_fixed_meshes': len(meshes), 'excluded_landscape_objects': skipped_landscape,
            'candidate_conflicts': conflicts, 'nearest_conservative_bounds_gap': nearest,
            'method': '700mm-wide square body bounds swept continuously between every pair of the 721 actual camera poses against evaluated fixed-mesh world bounds, including linked furniture/appliance instances. This conservatively contains a 700mm circular footprint.',
            'limitations': 'Fixed presentation state only; excludes vegetation/landscape collection and floor contact below50mm. Does not verify walking surface support, trip hazards, hardware operations, code or accessibility.'}


ROOT = Path(__file__).resolve().parents[2]
HOME = ROOT / 'homes/timber-courtyard-02'
OUT = HOME / 'outputs/videos'
record = json.loads((OUT / 'camera-route.json').read_text())
source = HOME / record['source']
assert hashlib.sha256(source.read_bytes()).hexdigest() == record['source_sha256']
published_scene = HOME / record.get('published_presentation_scene', 'model/timber-walkthrough.blend')
published_scene_hash = hashlib.sha256(published_scene.read_bytes()).hexdigest()
if 'published_presentation_scene_sha256' in record:
    assert published_scene_hash == record['published_presentation_scene_sha256'], 'Published presentation scene changed.'

bpy.ops.wm.open_mainfile(filepath=str(published_scene), use_scripts=False)
scene = bpy.context.scene
camera = scene.camera
assert camera.name == 'Timber continuous walkthrough'
assert scene.frame_start == 1 and scene.frame_end == 721 and scene.render.fps == 24
assert abs(camera.data.lens - 25) < 1e-6
links = []
resolved_links = []
for library in bpy.data.libraries:
    assert library.filepath.startswith('//'), library.filepath
    path = Path(bpy.path.abspath(library.filepath)).resolve()
    assert path.is_file() and path.is_relative_to(ROOT / 'library'), path
    links.append(library.filepath)
    resolved_links.append(path)
    expected = record['linked_asset_sha256'][str(path.relative_to(ROOT))]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, f'Linked asset changed: {path}'
manifest=json.loads((HOME/'project.json').read_text())
assert len(links) >= len(manifest['asset_dependencies'])
for dependency in manifest['asset_dependencies']:
    directory = (HOME / dependency['path']).resolve()
    assert any(path.parent == directory for path in resolved_links), f'Missing pinned asset: {dependency}'
for pose in record['poses']:
    scene.frame_set(pose['frame'])
    assert (camera.location - Vector(pose['position_m'])).length < 1e-5
    assert abs(camera.location.z - record['eye_height_m']) < 1e-5
    actual = camera.rotation_quaternion @ Vector((0, 0, -1))
    expected = (Vector(pose['target_m']) - camera.location).normalized()
    assert actual.dot(expected) > 0.99999
for opening in record['opening_overrides']:
    obj = bpy.data.objects[opening['object']]
    assert (obj.location - Vector(opening['open_location_m'])).length < 1e-5
for name in ['09 Roof | hide for cutaway', '08 Structure | cedar']:
    assert not bpy.data.collections[name].hide_render
clearance = route_clearance(scene, record)
report = {
    'native_reopened': True,
    'route_clearance': clearance,
    'canonical_source_sha256_unchanged': record['source_sha256'],
    'published_presentation_scene_sha256': published_scene_hash,
    'historical_render_source_scene_sha256': record.get('render_source_scene_sha256', record['presentation_source_sha256']),
    'camera_poses_verified': len(record['poses']),
    'fixed_lens_mm': camera.data.lens,
    'eye_height_m': record['eye_height_m'],
    'presentation_open_leaves_verified': len(record['opening_overrides']),
    'relative_libraries': links,
    'all_manifest_pins_linked': True,
    'linked_asset_hashes_verified': len(resolved_links),
    'blender_version': bpy.app.version_string,
    'scope': 'Camera and presentation-state checks; not a whole-home design or construction approval.'
}
(OUT / 'native-verification.json').write_text(json.dumps(report, indent=2) + '\n')
assert clearance['passed'], f'Route has candidate fixed-geometry conflicts: {clearance}'
print('WALKTHROUGH_NATIVE_VERIFIED', report, flush=True)
