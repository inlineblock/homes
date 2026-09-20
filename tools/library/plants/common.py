"""Shared original, batched botanical geometry. All inputs use meters.

Leaf ``center`` is the blade center; ``direction`` is its long axis and roll is
in radians. A caller attaches a leaf at a twig by using twig + axis*length/2
as center. Meshes are actual folded blades, not alpha cards or crown spheres.
These illustrative assets do not certify botanical or site suitability.
"""
from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]


def reset():
    """Clear the authoring process; never use on an unsaved user scene."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0
    bpy.context.scene.render.threads_mode = 'FIXED'
    bpy.context.scene.render.threads = 2


def collection(name):
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    coll.use_fake_user = True
    return coll


def material(name, color, roughness=0.6, subsurface=0.0):
    """Original procedural shader with modest variation, in linear RGB."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    rgba = tuple(color[:3]) + (float(color[3]) if len(color) > 3 else 1.0,)
    mat.diffuse_color = rgba
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    shader = nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = rgba
    shader.inputs['Roughness'].default_value = roughness
    shader.inputs['Subsurface Weight'].default_value = subsurface
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 36.0
    noise.inputs['Detail'].default_value = 2.0
    tex = nodes.new('ShaderNodeTexCoord')
    links.new(tex.outputs['Object'], noise.inputs['Vector'])
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = tuple(c * .78 for c in rgba[:3]) + (rgba[3],)
    ramp.color_ramp.elements[1].color = tuple(min(c * 1.12, 1.0) for c in rgba[:3]) + (rgba[3],)
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], shader.inputs['Base Color'])
    rough = nodes.new('ShaderNodeMapRange')
    rough.inputs['To Min'].default_value = max(0, roughness - .05)
    rough.inputs['To Max'].default_value = min(1, roughness + .05)
    links.new(noise.outputs['Fac'], rough.inputs['Value'])
    links.new(rough.outputs['Result'], shader.inputs['Roughness'])
    return mat


def bark_material(name, color):
    mat = material(name, color, .84)
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    coords = nodes.new('ShaderNodeTexCoord')
    stretch = nodes.new('ShaderNodeVectorMath')
    stretch.operation = 'MULTIPLY'
    stretch.inputs[1].default_value = (18, 18, 2.4)
    links.new(coords.outputs['Object'], stretch.inputs[0])
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 3
    noise.inputs['Detail'].default_value = 3
    links.new(stretch.outputs['Vector'], noise.inputs['Vector'])
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = .3
    bump.inputs['Distance'].default_value = .008
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], nodes.get('Principled BSDF').inputs['Normal'])
    return mat


def _axis(direction):
    v = Vector(direction)
    if v.length < 1e-9:
        raise ValueError('Botanical direction must have nonzero length')
    return v.normalized()


def _basis(axis):
    ref = Vector((0, 0, 1)) if abs(axis.z) < .92 else Vector((0, 1, 0))
    side = axis.cross(ref).normalized()
    return side, side.cross(axis).normalized()


class MeshBuilder:
    """Accumulate many connected botanical pieces into one material mesh."""
    def __init__(self, name, material):
        self.name = name
        self.material = material
        self.vertices = []
        self.faces = []

    def tube(self, points, radii, sides=7):
        points = [Vector(p) for p in points]
        if len(points) < 2:
            return self
        if isinstance(radii, (int, float)):
            radii = [float(radii)] * len(points)
        if len(radii) != len(points):
            raise ValueError('One tube radius is required per path point')
        sides = max(3, int(sides))
        base = len(self.vertices)
        prev_side = None
        for i, (point, radius) in enumerate(zip(points, radii)):
            axis = _axis(points[min(i+1, len(points)-1)] - points[max(0, i-1)])
            side, up = _basis(axis)
            if prev_side is not None:
                projected = prev_side - axis * prev_side.dot(axis)
                if projected.length > .01:
                    side = projected.normalized()
                    up = side.cross(axis).normalized()
            prev_side = side
            for k in range(sides):
                a = k * 2 * math.pi / sides
                self.vertices.append(tuple(point + float(radius) * (side*math.cos(a) + up*math.sin(a))))
        for j in range(len(points)-1):
            for k in range(sides):
                a = base + j*sides + k
                b = base + j*sides + (k+1)%sides
                self.faces.append((a, a+sides, b+sides, b))
        self.faces.append(tuple(base+i for i in range(sides)))
        end = base + (len(points)-1)*sides
        self.faces.append(tuple(end+i for i in reversed(range(sides))))
        return self

    def leaf(self, center, direction, length, width, style='oval', roll=0):
        if style not in {'oval','lance','heart','lobed','needle','fan'}:
            raise ValueError(f'Unknown leaf style: {style}')
        axis = _axis(direction)
        side, normal = _basis(axis)
        side, normal = (side*math.cos(roll)+normal*math.sin(roll),
                        normal*math.cos(roll)-side*math.sin(roll))
        center = Vector(center)
        base = len(self.vertices)
        count = 8 if style in {'lobed', 'fan'} else 6
        for i in range(count+1):
            t = i/count
            profile = math.sin(math.pi*t)
            if style == 'lance':
                profile = profile ** 1.25
            elif style == 'heart':
                profile = math.sin(math.pi*t) ** .65 * (1.28-.5*t)
            elif style == 'lobed':
                profile *= .78 + .22*math.cos(t*8*math.pi)
            elif style == 'needle':
                profile = min(1.0, t*8, (1-t)*8)
            elif style == 'fan':
                profile = math.sin(math.pi*t/2) * min(1, (1-t)*10)
            mid = center + axis*((t-.5)*length) + normal*(length*.075*math.sin(math.pi*t) - length*.06*t*t)
            half = max(.00001, profile*width*.5)
            fold = half*.15
            self.vertices.extend([tuple(mid-side*half-normal*fold),tuple(mid),tuple(mid+side*half-normal*fold)])
        for i in range(count):
            a = base+i*3
            self.faces.extend([(a,a+1,a+4,a+3),(a+1,a+2,a+5,a+4)])
        return self

    def ellipsoid(self, center, scale, segments=10, rings=6):
        center, scale = Vector(center), Vector(scale)
        segments, rings = max(4,int(segments)), max(3,int(rings))
        base = len(self.vertices)
        self.vertices.append(tuple(center+Vector((0,0,scale.z))))
        for j in range(1,rings):
            lat = math.pi*j/rings
            for i in range(segments):
                lon = math.tau*i/segments
                self.vertices.append(tuple(center+Vector((math.sin(lat)*math.cos(lon)*scale.x, math.sin(lat)*math.sin(lon)*scale.y, math.cos(lat)*scale.z))))
        bottom = len(self.vertices)
        self.vertices.append(tuple(center-Vector((0,0,scale.z))))
        for i in range(segments):
            self.faces.append((base,base+1+i,base+1+(i+1)%segments))
        for j in range(rings-2):
            row = base+1+j*segments
            for i in range(segments):
                self.faces.append((row+i,row+segments+i,row+segments+(i+1)%segments,row+(i+1)%segments))
        row = base+1+(rings-2)*segments
        for i in range(segments):
            self.faces.append((row+i,bottom,row+(i+1)%segments))
        return self

    def finish(self, collection):
        if not self.vertices or not self.faces:
            return None  # A dormant/nonfruiting state need not create an empty mesh.
        mesh = bpy.data.meshes.new(self.name)
        mesh.from_pydata(self.vertices, [], self.faces)
        mesh.update()
        obj = bpy.data.objects.new(self.name, mesh)
        collection.objects.link(obj)
        if self.material:
            mesh.materials.append(self.material)
        for polygon in mesh.polygons:
            polygon.use_smooth = True
        return obj


def bounds(collection):
    """Measured world-space native mesh bounds, including child collections."""
    lo, hi = [float('inf')]*3, [float('-inf')]*3
    count = 0
    for obj in collection.all_objects:
        if obj.type != 'MESH':
            continue
        for vertex in obj.data.vertices:
            co = obj.matrix_world @ vertex.co
            count += 1
            for a in range(3):
                lo[a] = min(lo[a],co[a]); hi[a] = max(hi[a],co[a])
    if not count:
        raise ValueError(f'Collection {collection.name} contains no native mesh vertices')
    return {'min': lo, 'max': hi, 'dimensions': [hi[a]-lo[a] for a in range(3)]}


def save_family(slug, name, variants, metadata):
    """Create a new family version only; previews/validation are separate gates.

    variants: [(variant_id, collection, description), ...]. Metadata accepts
    generator, command, botanical_name, browse_tags, selection_notes, sources,
    and any additional descriptive fields. Tracked v001 content causes a hard
    failure; a new untracked candidate may be rebuilt during visual review.
    """
    folder = ROOT/'library'/'landscape'/slug/'v001'
    native = folder/f'{slug}.blend'
    tracked = subprocess.run(['git','ls-files','--',str(folder.relative_to(ROOT))],
                             cwd=ROOT, capture_output=True, text=True, check=True)
    if tracked.stdout.strip():
        raise FileExistsError(f'Will not overwrite published family: {folder}')
    if not variants or len({v[0] for v in variants}) != len(variants):
        raise ValueError('Family requires uniquely named variants')
    folder.mkdir(parents=True, exist_ok=True)
    bpy.context.view_layer.update()
    rows = []
    for variant_id, coll, description in variants:
        coll.use_fake_user = True
        measured = bounds(coll)
        rows.append({'id': variant_id, 'collection': coll.name,
                     'description': description, 'dimensions_m': measured['dimensions'],
                     'bounds_m': {'min': measured['min'], 'max': measured['max']}})
    metadata = dict(metadata)
    generator = metadata.pop('generator', 'tools/library/plants/README.md')
    command = metadata.pop('command', f'blender -b --factory-startup -t 2 --python {generator}')
    record = {
        **metadata,
        'schema_version': 1, 'id': f'landscape/{slug}', 'version': 'v001',
        'name': name, 'units': 'meters', 'dimensions_m': rows[0]['dimensions_m'],
        'bounds_m': rows[0]['bounds_m'],
        'blender': {'collection': rows[0]['collection'], 'variants': rows},
        'dependencies': [],
        'placement': {'origin': 'Ground-contact point at XY 0,0 and planting grade Z=0',
                      'front_direction': 'No prescribed front; Z up',
                      'allowed_scaling': 'Uniform 0.9 to 1.1 and Z rotation; choose a modeled variant for substantial size or growth-form changes'},
        'mounting': 'Place at actual host planting grade in a suitable open soil volume.',
        'clearances': {'host_checked': False, 'basis': 'Modeled canopy bounds are measurable geometry, not mature spread or a root-zone prescription. Confirm real site requirements separately.'},
        'product_status': 'Original illustrative botanical geometry; not a certified species identification, nursery specification, or climate suitability approval.',
        'modeled_state': 'Individually attached branching stems and shaped mesh leaves, with species-specific flowers or fruit where described; no billboard textures.',
        'license': 'CC-BY-4.0',
        'rights': 'Original Homes project contributors geometry and procedural materials. Attribution: Homes project contributors. No third-party mesh, photographs or textures.',
        'source': {'kind': 'original', 'generator': generator, 'command': command},
        'software': {'blender': bpy.app.version_string},
        'files': {'blender': native.name},
        'review': {'native_reopen_checked': False, 'native_preview_checked': False, 'host_placement_checked': False},
    }
    bpy.ops.wm.save_as_mainfile(filepath=str(native), check_existing=False, compress=True)
    (folder/'asset.json').write_text(json.dumps(record, indent=2)+'\n')
    readme = [f'# {name}', '', record['product_status'], '',
              'Original editable mesh asset, in meters with Z up and the plant base at the origin.', '',
              '## Collections', '',
              'Link one collection from the Blender file for each planting instance; variants share the same origin intentionally.', '',
              '| Variant | Collection | Modeled size (W × D × H, m) | Description |',
              '|---|---|---|---|']
    for row in rows:
        size = ' × '.join(f'{n:.2f}' for n in row['dimensions_m'])
        readme.append(f"| {row['id']} | `{row['collection']}` | {size} | {row['description']} |")
    readme.extend(['', '## Source and use', '',
                   f'Generator: `{generator}`. Regeneration command is recorded in `asset.json`.', '',
                   'The generator permits rebuilding this candidate while untracked. Once versioned, publish a new version rather than modifying this one.', '',
                   'CC BY 4.0; attribution: Homes project contributors. All geometry and procedural materials are original.', '',
                   'Choose variants by modeled size and state. These dimensions are not expected mature spread; consult the selection notes for site limitations. A library model does not establish host adoption.', ''])
    (folder/'README.md').write_text('\n'.join(readme))
    print(f'PLANT_FAMILY_SAVED {slug} {len(rows)} variants', flush=True)
    return record
