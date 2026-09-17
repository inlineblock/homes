"""Small Blender geometry helpers. Author-facing dimensions are in feet."""
import bpy, math
from mathutils import Vector
F = .3048
ACTIVE = None
def collection(name):
    global ACTIVE
    c=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); ACTIVE=c
    return c
def move(obj):
    if ACTIVE:
        for c in list(obj.users_collection): c.objects.unlink(obj)
        ACTIVE.objects.link(obj)
    return obj
def material(name,color,roughness=.5,metallic=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=roughness; p.inputs['Metallic'].default_value=metallic
    return m
def box(name,loc,size,mat=None,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=[v*F for v in loc]); o=move(bpy.context.object); o.name=name
    o.dimensions=[v*F for v in size]; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if mat: o.data.materials.append(mat)
    if bevel:
        mod=o.modifiers.new('Soft manufactured edges','BEVEL');mod.width=bevel*F;mod.segments=3
        o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o
def cyl(name,loc,radius,depth,mat,vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius*F,depth=depth*F,location=[v*F for v in loc])
    o=move(bpy.context.object);o.name=name;o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    return o
def sphere(name,loc,scale,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=F,location=[v*F for v in loc]);o=move(bpy.context.object);o.name=name
    o.scale=scale;o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    return o
def rod(name,a,b,r,mat):
    d=Vector(b)-Vector(a); o=cyl(name,(Vector(a)+Vector(b))/2,r,d.length,mat,16)
    o.rotation_euler=d.to_track_quat('Z','Y').to_euler(); return o
def curve(name,points,r,mat):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r*F;d.bevel_resolution=3
    s=d.splines.new('BEZIER');s.bezier_points.add(len(points)-1)
    for p,co in zip(s.bezier_points,points):p.co=[v*F for v in co];p.handle_left_type=p.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,d);ACTIVE.objects.link(o);o.data.materials.append(mat);return o
def area(name,loc,target,power,size,color=(1,.84,.66),shape='DISK',size_y=None):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.color=color;d.shape=shape;d.size=size*F
    if size_y and shape=='RECTANGLE':d.size_y=size_y*F
    o=bpy.data.objects.new(name,d);ACTIVE.objects.link(o);o.location=Vector(loc)*F;o.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y').to_euler();return o
def camera(name,loc,target,lens):
    d=bpy.data.cameras.new(name);d.lens=lens;d.clip_end=500
    o=bpy.data.objects.new(name,d);ACTIVE.objects.link(o);o.location=Vector(loc)*F;o.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y').to_euler();return o
