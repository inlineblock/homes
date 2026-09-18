"""Meter-based scene assembly adapters; shared primitives retain their feet API."""
import math
import bpy
from mathutils import Vector
from common import geometry as g
from common.library import linked_collection

F = .3048

def box(name, loc, size, mat=None, bevel=0):
    x,y,z=[v/2 for v in size]
    obj=mesh(name,[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)],
             [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
    obj.location=loc
    if bevel:
        mod=obj.modifiers.new('Soft manufactured edges','BEVEL');mod.width=bevel;mod.segments=3
        obj.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return obj

def rod(name, a, b, radius, mat):
    delta=Vector(b)-Vector(a);obj=cyl(name,(Vector(a)+Vector(b))/2,radius,delta.length,mat,16)
    obj.rotation_euler=delta.to_track_quat('Z','Y').to_euler();return obj

def cyl(name, loc, radius, depth, mat, vertices=32):
    points=[(math.cos(i*math.tau/vertices)*radius,math.sin(i*math.tau/vertices)*radius,z) for z in [-depth/2,depth/2] for i in range(vertices)]
    faces=[tuple(reversed(range(vertices))),tuple(range(vertices,2*vertices))]+[(i,(i+1)%vertices,(i+1)%vertices+vertices,i+vertices) for i in range(vertices)]
    obj=mesh(name,points,faces,mat);obj.location=loc
    for face in obj.data.polygons:
        if len(face.vertices)==4:face.use_smooth=True
    return obj

def mesh(name, vertices, faces, mat=None):
    data=bpy.data.meshes.new(name); data.from_pydata(vertices, [], faces); data.update()
    if mat: data.materials.append(mat)
    obj=bpy.data.objects.new(name, data); g.ACTIVE.objects.link(obj)
    return obj

def prism(name, polygon, bottom, top, mat):
    n=len(polygon)
    verts=[(x,y,z) for z in [bottom,top] for x,y in polygon]
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return mesh(name,verts,faces,mat)

def beam(name,a,b,width,depth,mat):
    d=Vector(b)-Vector(a)
    obj=box(name,(Vector(a)+Vector(b))/2,(width,depth,d.length),mat,.008)
    obj.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    return obj

def instance(name,coll,loc,rotation=0,scale=1):
    obj=bpy.data.objects.new(name,None);obj.instance_type='COLLECTION';obj.instance_collection=coll
    g.ACTIVE.objects.link(obj);obj.location=loc;obj.rotation_euler.z=rotation
    obj.scale=(scale,)*3 if isinstance(scale,(float,int)) else scale
    obj['shared_asset_id']=coll.get('asset_id',coll.name);obj['shared_asset_version']=coll.get('asset_version','v001')
    return obj

def area(name,loc,target,power,size,color=(1,.90,.78)):
    return g.area(name,[v/F for v in loc],[v/F for v in target],power,size/F,color)

def camera(name,loc,target,lens):
    return g.camera(name,[v/F for v in loc],[v/F for v in target],lens)

def material(root,slug,version='v001'):
    path=root/'library/materials'/slug/version/(slug+'.blend')
    with bpy.data.libraries.load(str(path),link=True) as (a,b):b.materials=[a.materials[0]]
    return b.materials[0]

def transform_new(before, loc=(0,0,0), rotation=0):
    from mathutils import Matrix
    transform=Matrix.Translation(Vector(loc))@Matrix.Rotation(rotation,4,'Z')
    for obj in set(bpy.data.objects)-before:
        if obj.library is None:obj.matrix_world=transform@obj.matrix_world

def tag(obj,kind='IfcBuildingElementProxy',level='Main floor'):
    obj['ifc_class']=kind;obj['ifc_storey']=level
    return obj
