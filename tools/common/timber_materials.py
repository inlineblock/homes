"""Original meter-scale timber shaders and grain-aligned UVs for applied meshes."""
import bpy

UV_NAME = 'Timber meters'


def timber(name, dark, mid, light):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = (*mid, 1)
    n, links = m.node_tree.nodes, m.node_tree.links
    p = n.get('Principled BSDF')
    p.inputs['Specular IOR Level'].default_value = .25
    p.inputs['Coat Weight'].default_value = .025
    p.inputs['Coat Roughness'].default_value = .6
    uv = n.new('ShaderNodeUVMap'); uv.uv_map = UV_NAME
    uv.label = 'Across grain / along grain in meters'
    info = n.new('ShaderNodeObjectInfo')
    seed = n.new('ShaderNodeMath'); seed.operation = 'MULTIPLY'
    seed.inputs[1].default_value = 173.1
    links.new(info.outputs['Random'], seed.inputs[0])

    def noise(label, stretch):
        v = n.new('ShaderNodeVectorMath'); v.operation = 'MULTIPLY'
        v.inputs[1].default_value = stretch
        links.new(uv.outputs[0], v.inputs[0])
        t = n.new('ShaderNodeTexNoise'); t.noise_dimensions = '4D'
        t.label = label; t.inputs['Scale'].default_value = 1
        t.inputs['Detail'].default_value = 3
        t.inputs['Roughness'].default_value = .65
        links.new(v.outputs[0], t.inputs['Vector'])
        links.new(seed.outputs[0], t.inputs['W'])
        return t.outputs['Fac']

    # Broad flowing latewood and fine fibers are independently scaled, never
    # stretched by the member length. Each board has a separate growth sample.
    broad = noise('Flowing growth grain, 25 mm across / 0.8 m along', (40, 1.25, 1))
    fine = noise('Fine fibers, 3 mm across / 0.25 m along', (330, 4, 1))
    grain = n.new('ShaderNodeMixRGB'); grain.blend_type = 'MIX'
    grain.inputs[0].default_value = .18
    links.new(broad, grain.inputs[1]); links.new(fine, grain.inputs[2])
    ramp = n.new('ShaderNodeValToRGB'); ramp.label = 'Neutral umber timber; linear colors'
    ramp.color_ramp.elements[0].position = .22
    ramp.color_ramp.elements[0].color = (*dark, 1)
    ramp.color_ramp.elements[1].position = .78
    ramp.color_ramp.elements[1].color = (*light, 1)
    ramp.color_ramp.elements.new(.5).color = (*mid, 1)
    links.new(grain.outputs[0], ramp.inputs[0])
    tone = n.new('ShaderNodeMapRange')
    tone.inputs['To Min'].default_value = .72
    tone.inputs['To Max'].default_value = 1.24
    links.new(info.outputs['Random'], tone.inputs['Value'])
    color = n.new('ShaderNodeMixRGB'); color.blend_type = 'MULTIPLY'
    color.inputs[0].default_value = 1
    links.new(ramp.outputs[0], color.inputs[1]); links.new(tone.outputs[0], color.inputs[2])
    # Thin, wandering growth lines keep the broad color figure from reading
    # as blurred stripes. All frequencies remain in physical meter UVs.
    def math_node(operation, a, b=None):
        node = n.new('ShaderNodeMath'); node.operation = operation
        if isinstance(a, (int, float)): node.inputs[0].default_value = a
        else: links.new(a, node.inputs[0])
        if b is not None:
            if isinstance(b, (int, float)): node.inputs[1].default_value = b
            else: links.new(b, node.inputs[1])
        return node.outputs[0]

    axes = n.new('ShaderNodeSeparateXYZ'); links.new(uv.outputs[0], axes.inputs[0])
    wander = math_node('MULTIPLY', math_node('SUBTRACT', noise('Irregular growth wander', (7, 1.7, 1)), .5), .016)
    phase = math_node('MULTIPLY', math_node('ADD', axes.outputs['X'], wander), 534.07)
    phase = math_node('ADD', phase, seed.outputs[0])
    line = math_node('POWER', math_node('ADD', math_node('MULTIPLY', math_node('SINE', phase), .5), .5), 16)
    pores = math_node('MAXIMUM', math_node('SUBTRACT', noise('Fine elongated open pores', (600, 24, 1)), .59), 0)
    detail = math_node('SUBTRACT', math_node('SUBTRACT', 1, math_node('MULTIPLY', line, .23)), math_node('MULTIPLY', pores, .55))
    final_color = n.new('ShaderNodeMixRGB'); final_color.blend_type = 'MULTIPLY'
    final_color.inputs[0].default_value = 1
    links.new(color.outputs[0], final_color.inputs[1]); links.new(detail, final_color.inputs[2])
    links.new(final_color.outputs[0], p.inputs['Base Color'])
    rough = n.new('ShaderNodeMapRange')
    rough.inputs['To Min'].default_value = .48
    rough.inputs['To Max'].default_value = .78
    links.new(fine, rough.inputs['Value']); links.new(rough.outputs[0], p.inputs['Roughness'])
    bump = n.new('ShaderNodeBump'); bump.inputs['Distance'].default_value = .00065
    bump.inputs['Strength'].default_value = .32
    links.new(grain.outputs[0], bump.inputs['Height'])
    fiber_bump = n.new('ShaderNodeBump'); fiber_bump.inputs['Distance'].default_value = .00012
    fiber_bump.inputs['Strength'].default_value = .22
    links.new(detail, fiber_bump.inputs['Height']); links.new(bump.outputs[0], fiber_bump.inputs['Normal'])
    links.new(fiber_bump.outputs[0], p.inputs['Normal'])
    m['mapping'] = UV_NAME
    m['texture_units'] = 'meters; U across grain, V along grain'
    return m


def grain_uv(obj):
    """Map physical meters along each solid's longest LOCAL mesh axis.

    Applied box meshes and rotated beam meshes both work. Broad-face UVs
    preserve millimeter-scale fibers; end faces have a transverse mapping.
    No geometry, transforms, openings or world-space bounds are changed.
    """
    if obj.type != 'MESH' or obj.library:
        return
    mesh = obj.data
    spans = [max(v.co[i] for v in mesh.vertices) - min(v.co[i] for v in mesh.vertices) for i in range(3)]
    axis = max(range(3), key=lambda i: spans[i])
    transverse = [i for i in range(3) if i != axis]
    uv = mesh.uv_layers.get(UV_NAME) or mesh.uv_layers.new(name=UV_NAME)
    for poly in mesh.polygons:
        if abs(poly.normal[axis]) > .85:
            u, v = transverse
        else:
            u = min(transverse, key=lambda i: abs(poly.normal[i])); v = axis
        for li in poly.loop_indices:
            co = mesh.vertices[mesh.loops[li].vertex_index].co
            uv.data[li].uv = (co[u], co[v])
    obj['timber_grain_local_axis'] = 'XYZ'[axis]
    obj['timber_mapping'] = UV_NAME


def apply_grain(materials):
    wanted = set(materials)
    count = 0
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and not obj.library and any(s.material in wanted for s in obj.material_slots):
            grain_uv(obj); count += 1
    return count
