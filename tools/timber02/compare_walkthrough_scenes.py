"""Compare stated scene properties across a relocatable presentation resave.

Read-only CPU operation; never renders or saves either source scene.
blender --factory-startup --background --python-exit-code 1 \
    --python tools/timber02/compare_walkthrough_scenes.py

The ignored render-work scene must still exist. The receipt is written to
outputs/work/walkthrough/scene-equivalence.json for review before promotion.
This is not proof of arbitrary Blender binary equivalence.
"""
import hashlib
import json
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[2]
HOME = ROOT / 'homes/timber-courtyard-02'
WORK = HOME / 'outputs/work/walkthrough'


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value_hash(value):
    data = json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(data).hexdigest()


def serial(value):
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    try:
        return [serial(item) for item in value]
    except TypeError:
        return str(value)


def node_signature(tree):
    if not tree:
        return None
    nodes = []
    for node in tree.nodes:
        image = getattr(node, 'image', None)
        path = Path(bpy.path.abspath(image.filepath)) if image else None
        nodes.append({
            'name': node.name,
            'type': node.bl_idname,
            'inputs': [(item.name, serial(item.default_value))
                       for item in node.inputs if hasattr(item, 'default_value')],
            'image': file_hash(path) if path and path.is_file() else None,
        })
    return {
        'nodes': sorted(nodes, key=lambda item: item['name']),
        'links': sorted((link.from_node.name, link.from_socket.name,
                         link.to_node.name, link.to_socket.name)
                        for link in tree.links),
    }


def scene_signature(path):
    bpy.ops.wm.open_mainfile(filepath=str(path), use_scripts=False)
    scene = bpy.context.scene
    scene.frame_set(scene.frame_start)
    deps = bpy.context.evaluated_depsgraph_get()
    geometry = []
    for instance in deps.object_instances:
        obj = instance.object
        if obj.type != 'MESH':
            continue
        mesh = obj.to_mesh()
        geometry.append({
            'name': obj.original.name,
            'matrix': serial(instance.matrix_world),
            'vertices': value_hash([serial(vertex.co) for vertex in mesh.vertices]),
            'polygons': value_hash([list(face.vertices) for face in mesh.polygons]),
            'material_indices': value_hash([face.material_index for face in mesh.polygons]),
            'materials': [material.name if material else None for material in obj.data.materials],
            'hide_render': obj.hide_render,
        })
        obj.to_mesh_clear()
    poses = []
    for frame in range(scene.frame_start, scene.frame_end + 1):
        scene.frame_set(frame)
        poses.append([frame, serial(scene.camera.matrix_world), scene.camera.data.lens])
    signature = {
        'geometry': value_hash(sorted(geometry, key=lambda item: json.dumps(item, sort_keys=True))),
        'mesh_instance_count': len(geometry),
        'camera_animation': value_hash(poses),
        'camera_frame_range': [scene.frame_start, scene.frame_end],
        'camera_pose_count': len(poses),
        'materials': value_hash({material.name: node_signature(material.node_tree)
                                 for material in bpy.data.materials}),
        'lights': value_hash({obj.name: {
            'matrix': serial(obj.matrix_world), 'type': obj.data.type,
            'energy': obj.data.energy, 'color': serial(obj.data.color),
            'nodes': node_signature(obj.data.node_tree),
        } for obj in scene.objects if obj.type == 'LIGHT'}),
        'world': value_hash(node_signature(scene.world.node_tree)),
        'collections': value_hash({collection.name: {
            'hide_render': collection.hide_render,
            'objects': sorted(obj.name for obj in collection.objects),
        } for collection in bpy.data.collections}),
        'linked_asset_sha256': {
            str(Path(bpy.path.abspath(library.filepath)).resolve().relative_to(ROOT)):
                file_hash(Path(bpy.path.abspath(library.filepath)))
            for library in bpy.data.libraries
        },
        'render': {
            'engine': scene.render.engine,
            'resolution': [scene.render.resolution_x, scene.render.resolution_y,
                           scene.render.resolution_percentage],
            'fps': scene.render.fps, 'samples': scene.cycles.samples,
            'seed': scene.cycles.seed, 'animated_seed': scene.cycles.use_animated_seed,
            'view_transform': scene.view_settings.view_transform,
            'exposure': scene.view_settings.exposure,
        },
    }
    print('SCENE_SNAPSHOT', path, flush=True)
    return {'scene': str(path.relative_to(HOME)), 'sha256': file_hash(path), 'signature': signature}


def main():
    paths = [WORK / 'timber-walkthrough.blend', HOME / 'model/timber-walkthrough.blend']
    before = [file_hash(path) for path in paths]
    records = [scene_signature(path) for path in paths]
    differences = [key for key in records[0]['signature']
                   if records[0]['signature'][key] != records[1]['signature'][key]]
    result = {
        'passed': not differences,
        'different_properties': differences,
        'source_files_unchanged': before == [file_hash(path) for path in paths],
        'checker_sha256': file_hash(Path(__file__)),
        'software': bpy.app.version_string,
        'method': 'Fresh Blender reopen of render-work and published-resave scenes. Compare all evaluated mesh-instance local vertices, polygon topology, material assignments, world matrices and render visibility at each scene start frame; collection membership/visibility; material node inputs/links and external image hashes; lights and world nodes; camera transforms/lenses throughout each actual scene frame range; shared-library content hashes; selected render/color settings. Normalize dependency paths to hashes; binary resave bytes need not match.',
        'limitations': 'Only the stated properties are compared, not every Blender field. Non-camera animation is not sampled beyond scene start-frame geometry. Unsupported node attributes, packed images and compositor properties are not exhaustive. This establishes scoped presentation-resave consistency, not regenerated frames, construction validation or arbitrary binary equivalence.',
        'scenes': records,
    }
    (WORK / 'scene-equivalence.json').write_text(json.dumps(result, indent=2) + '\n')
    assert result['passed'] and result['source_files_unchanged'], result
    print('SCENE_EQUIVALENCE_VERIFIED', flush=True)


if __name__ == '__main__':
    main()
