"""Original procedural trees, shrubs, grasses and stones; reusable across homes."""
import bpy,random,math
from mathutils import Vector
from . import geometry as g
from .geometry import rod,box,F
def foliage_mesh(name,clusters,mat,seed=1,leaves_per_cluster=130,leaf_size=.17):
    rng=random.Random(seed);verts=[];faces=[]
    for center,spread in clusters:
        center=Vector(center)
        for i in range(leaves_per_cluster):
            p=center+Vector((rng.uniform(-1,1)*spread,rng.uniform(-1,1)*spread,rng.uniform(-.7,.7)*spread))
            a=rng.random()*math.tau;u=Vector((math.cos(a),math.sin(a),rng.uniform(-.6,.6))).normalized();v=u.cross(Vector((0,0,1))).normalized();ln=leaf_size*rng.uniform(.7,1.3)
            base=len(verts);verts.append(tuple((p+Vector((0,0,.025)))*F))
            for k in range(8):
                a=math.tau*k/8;verts.append(tuple((p+u*math.cos(a)*ln+v*math.sin(a)*ln*.38)*F))
            for k in range(8):faces.append((base,base+1+k,base+1+(k+1)%8))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.materials.append(mat)
    o=bpy.data.objects.new(name,mesh);g.ACTIVE.objects.link(o);return o
def tree(name,x,y,height,trunk,leaf,seed=1):
    rng=random.Random(seed);s=height/10
    rod(name+' trunk',(x,y,0),(x+.25*s,y,6*s),.17*s,trunk)
    clusters=[]
    for i in range(14):
        a=i*2.399;r=rng.uniform(1.5,3.5)*s;tip=(x+math.cos(a)*r,y+math.sin(a)*r,rng.uniform(5.8,9)*s)
        rod(name+' branch',(x,y,3.7*s),tip,.048*s,trunk);clusters.append((tip,1.25*s))
    return foliage_mesh(name+' canopy',clusters,leaf,seed,750,.18*s)
def shrub(name,x,y,size,mat,seed):
    return foliage_mesh(name,[((x,y,size*.62),size*.68),((x+.2,y-.1,size*.88),size*.48)],mat,seed,200,size*.11)
def grasses(name,x,y,size,mat,seed):
    rng=random.Random(seed);verts=[];faces=[]
    for i in range(65):
        a=rng.random()*math.tau;ln=rng.uniform(.6,1.4)*size;bend=rng.uniform(.3,.9)*size;w=.025*size;p=Vector((x+rng.uniform(-.2,.2),y+rng.uniform(-.2,.2),.02));side=Vector((-math.sin(a),math.cos(a),0))*w
        middle=p+Vector((math.cos(a)*bend*.3,math.sin(a)*bend*.3,ln*.8));tip=p+Vector((math.cos(a)*bend,math.sin(a)*bend,ln*.75));base=len(verts)
        for v in [p-side,p+side,middle+side*.6,middle-side*.6,tip]:verts.append(tuple(v*F))
        faces.extend([(base,base+1,base+2,base+3),(base+3,base+2,base+4)])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.materials.append(mat);o=bpy.data.objects.new(name,mesh);g.ACTIVE.objects.link(o);return o
def rock(name,x,y,size,mat,seed):
    rng=random.Random(seed);bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=F,location=(x*F,y*F,size*.25*F));o=g.move(bpy.context.object);o.name=name
    for v in o.data.vertices:v.co*=rng.uniform(.82,1.12)
    o.scale=(size,size*.72,size*.5);o.rotation_euler.z=rng.random()*math.tau;o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    return o
