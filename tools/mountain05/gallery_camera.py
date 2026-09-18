"""Add the living/fireplace gallery camera without rebuilding the approved home.

Run against the saved native model. Use -- --verify for a fresh-file preservation
check. Rendering remains the separate render.py workflow and never saves view state.
"""
from pathlib import Path
import array
import hashlib
import json
import sys

CAMERA_NAME = '09 Living fireplace'
CAMERA_SPEC = ((22, 37, 6), (1, 30.2, 4.5), 30)
OUTPUT_SLUG = '09-living-fireplace'


def fingerprint():
    """Hash noncamera geometry, transforms, material assignments and lighting."""
    import bpy
    rows = []
    for obj in sorted(bpy.data.objects, key=lambda item: item.name):
        if obj.type == 'CAMERA':
            continue
        row = [obj.name, obj.type, [list(v) for v in obj.matrix_world],
               obj.hide_render, obj.hide_viewport,
               sorted(c.name for c in obj.users_collection),
               obj.instance_collection.name if obj.instance_collection else None]
        if obj.type == 'MESH':
            values = array.array('f', [0]) * (len(obj.data.vertices) * 3)
            obj.data.vertices.foreach_get('co', values)
            loops = array.array('i', [0]) * len(obj.data.loops)
            obj.data.loops.foreach_get('vertex_index', loops)
            row += [hashlib.sha256(values.tobytes() + loops.tobytes()).hexdigest(),
                    [m.name if m else None for m in obj.data.materials]]
        elif obj.type == 'LIGHT':
            row += [obj.data.type, obj.data.energy, list(obj.data.color),
                    getattr(obj.data, 'size', None), getattr(obj.data, 'size_y', None)]
        elif obj.type == 'CURVE':
            row += [obj.data.bevel_depth, obj.data.use_fill_caps,
                    [[list(p.co) for p in sp.bezier_points] for sp in obj.data.splines]]
        rows.append(row)
    materials = []
    for mat in sorted(bpy.data.materials, key=lambda item: item.name):
        nodes = []
        if mat.node_tree:
            for node in sorted(mat.node_tree.nodes, key=lambda item: item.name):
                sockets = []
                for socket in node.inputs:
                    if hasattr(socket, 'default_value'):
                        value = socket.default_value
                        try:
                            value = list(value)
                        except TypeError:
                            pass
                        sockets.append([socket.name, str(value)])
                nodes.append([node.name, node.bl_idname, sockets])
            links = sorted([l.from_node.name, l.from_socket.name, l.to_node.name, l.to_socket.name]
                           for l in mat.node_tree.links)
        else:
            links = []
        materials.append([mat.name, nodes, links])
    world = bpy.context.scene.world
    skies = [[n.name, n.sun_rotation, n.sun_elevation] for n in world.node_tree.nodes
             if n.type == 'TEX_SKY']
    return hashlib.sha256(json.dumps([rows, materials, skies], sort_keys=True).encode()).hexdigest()


def install():
    import bpy
    from mathutils import Vector
    name = CAMERA_NAME
    obj = bpy.data.objects.get(name)
    if obj is None:
        obj = bpy.data.objects.new(name, bpy.data.cameras.new(name))
        bpy.data.collections['10 Lighting and cameras'].objects.link(obj)
    loc, target, lens = CAMERA_SPEC
    obj.location = Vector(loc) * .3048
    obj.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    obj.data.lens = lens
    obj.data.clip_end = 500
    return obj


if __name__ == '__main__':
    import bpy
    root = Path(__file__).resolve().parents[2]
    home = root / 'homes/mountain-house'
    receipt_path = home / 'model/gallery-validation.json'
    if '--verify' in sys.argv:
        from mathutils import Vector
        receipt = json.loads(receipt_path.read_text())
        assert fingerprint() == receipt['preserved_scene_sha256']
        cam = bpy.data.objects[CAMERA_NAME]
        assert max(abs(cam.location[i] / .3048 - CAMERA_SPEC[0][i]) for i in range(3)) < 1e-4
        assert abs(cam.data.lens - CAMERA_SPEC[2]) < 1e-5
        expected = (Vector(CAMERA_SPEC[1]) - Vector(CAMERA_SPEC[0])).to_track_quat('-Z', 'Y')
        assert cam.rotation_euler.to_quaternion().rotation_difference(expected).angle < 1e-4
        for lib in bpy.data.libraries:
            assert lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).exists()
        receipt['fresh_native_reopen'] = 'passed: preservation hash, source camera position/orientation/lens and relative libraries'
        receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
        print('MOUNTAIN_GALLERY_NATIVE_VERIFIED', flush=True)
    else:
        before = fingerprint()
        previous = {o.name: [list(o.location), list(o.rotation_euler), o.data.lens]
                    for o in bpy.data.objects if o.type == 'CAMERA' and o.name != CAMERA_NAME}
        install()
        bpy.context.view_layer.update()
        assert fingerprint() == before
        assert previous == {o.name: [list(o.location), list(o.rotation_euler), o.data.lens]
                            for o in bpy.data.objects if o.type == 'CAMERA' and o.name != CAMERA_NAME}
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        receipt = {'schema_version': 1, 'scope': 'Gallery camera only; existing home and IFC geometry unchanged',
                   'software': {'blender': bpy.app.version_string},
                   'camera': CAMERA_NAME, 'camera_spec_feet': CAMERA_SPEC,
                   'output': 'outputs/images/' + OUTPUT_SLUG + '.png',
                   'preserved_scene_sha256': before, 'existing_cameras_preserved': len(previous),
                   'fresh_native_reopen': 'pending', 'visual_review': 'pending; render not yet promoted'}
        receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
        print('MOUNTAIN_GALLERY_CAMERA_ADDED', flush=True)
